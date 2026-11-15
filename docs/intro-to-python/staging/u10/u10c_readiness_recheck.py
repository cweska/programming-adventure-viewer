"""Unit 10 "Campaign Readiness Check" ("Before We Continue"), part c, in the order students meet it: Part 1 form C
(the same 13 skills as forms A and B, a third time, with new names, numbers and situations: first the quiz
rc-part1-c-questions with the 12 questions of the 9 predict / mc / explain items, so the first win is a prediction,
then the testout rc-part1-c with its 9 code tasks), and the spaced re-check (rc-recheck-questions, then rc-recheck,
5.6: unaided, about a week after the Readiness Check, before the next campaign module). Mar'tu's review notes
(rc-review, the review routing of 5.2 / 5.5) moved to u10a, right after Part 1 form A; this file keeps an identical
copy of ROUTES for its `review=` meta lines.

Spec: design/curriculum.md "## Unit 10" ("u10c: Part 1 form C and the spaced re-check items") and "# 5. Campaign
Readiness Check" (5.1 to 5.6): "Forms B and C reuse the skills with new names and data ... Form C: Gearshift's fuel
sheet, `option 4`, and so on." With the teacher's decisions (design/teacher-decisions.md). Introduces nothing
(concept_map.json plans nothing for u10c). Independent of Strings (T1): no code a student sees uses a Unit 9 token
(const:escape, attr:upper, attr:title, attr:split, attr:join, attr:strip, attr:replace, attr:find, node:FString), and
no optional-only token either (tuples, zip, comprehensions, .items(), defaults, keyword arguments, lambda, map, match,
assert, input, int, **, %, //). The READY path is proved by running the harness on a copy of the staging folder with
no concept_map.json (so the gate is built only from the real files u01-u07, u10a, u10b): 0 errors, and a control
`.upper()` is rejected there.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. Form C is the third parallel form:
a second retake, or the "parallel item from another form" after a review cycle (5.5), so it repeats no item of form A
or B. Its summary (form B's words) says so: "A retake form. Open it when Mar'tu's notes send you here, for the one
task they name." The re-check is for everyone (G4 R8), about a week after the Readiness Check, before the next
campaign module (teacher decision 2 overrides the spec's "before Module 2": Modules 1 and 2 are already played).
Every student has their own device and does every item alone: no pair talk here (the evidence must be each student's
own). Every task's Learn text, in form C and in the re-check, ends with form A's line "Stuck? Skip it, and come back.
A task you pass here stays ticked."

Part 1 form C, item for item with forms A and B (curriculum 5.3; each item's notes give `rc_item`, its skill tags, what
this part checks, the campaign part it prepares, and `review=` its routes into the earlier units):
   1  predict      concat-str                         Q1  `"Ore: " + str(ore)`, then `+ "/" + str(max_ore)`
   2  code         replace-pass                       C1  step_north (the scout), the comment's example goes west
   3  predict+code chain-methods, store-then-pass     Q2  get_alarm tidies "REFUEL SOON, GEARSHIFT."; C2
                                                          present_reading (store, then pass on)
   4  predict x2   boundary, return-comparison,       Q3  climb_check, needed = 16, at 17 / 16 / 15; Q4 the ledger
                   trace-call                             shape (fuel_burn(4, 2) + 6), typed, no choices
   5  predict+code elif-chain, quote-text             Q5  trace on "option 4", which falls to `else`; C3 mend
                                                          `elif choice == option 4:`
   6  code+predict dict-read, dict-nested, dict-write, C4  Gearshift's fuel sheet, `book[charm_name] = charm`; Q6
                   dict-in, dict-key-from-variable        `in` on keys
   7  predict+code repeat-string                      Q7  `"█" * 2 + "░" * 5`; C5 mend `"░" * max_ore - ore`
   8  mc+code      randint, randint-param             Q8  a d12; C6 toss_die(sides)
   9  explain+pred func-as-value, call-stored-func    Q9  `fixes["patch"]` vs `fixes["patch"](bomb_shell)`; Q10
  10  trace+explain list-of-dicts, for-each           Q11 how many calls (4 heroes), with what; Q12 what `friend` holds
  11  code (3 CPs) read-traceback                     C7  KeyError 'ore' (a skipped level), TypeError (str + int),
                                                          NameError 'legg' (the loop variable mistyped)
  12  code         dict-write, reassign,              C8  spend `cost` from `lucky["mana"]`
                   combine-values
  13  code         param-use, return-right-name,      C9  fuel_cost(miles, ore_per_mile), Example `times_ten(n)`,
                   exact-names                            numbered comments as form A's glug_cost

The spaced re-check rc-recheck (5.6), parallel to no form's item:
  R1  code (2 CPs) combine-values, reassign           need = trips * ore_per_trip, then take it out of `ore`
  R2  code (3 CPs) item 6: dict-read, dict-nested,    Lucky's sheet, `tricks[trick_name] = trick`: the class-wide
                   dict-write, dict-key-from-variable     sheet errors (a skipped level, a quoted name, a typed value)
  R3  code (2 CPs) item 4b: trace-call                the ledger for cart_load(2, 4), typed rows, paste_stop
  R4  code         param-use, return-right-name,      bar_gap(max_mana, mana), Example `take_two(n)`, numbered
                   exact-names                            comments as C9
  RQ1-RQ4 (quiz rc-recheck-questions): item 4a (lock_check, needed 12), item 6d (`in` on keys), item 9 (explain,
  then predict: `moves["hop"]` stored in `go`, then called twice). questions_to_pass=3 (one miss allowed).

How the parts are represented with the schema's existing fields (as forms A and B do; no new fields):
  * Part 1 and the re-check are unaided: the testouts' exercises are support="none" (no hints, Another way,
    Assemble it, tracer, predict or Compare) and explainer="lean". The glossary and read-aloud stay on. Their hints
    exist only because the schema needs two; they never hold a finished line. No assemble, no another_way, no
    tracer. Every typed task is behavior-checked with other values (CMB, PAR, CALL, RND, KEY, STO), never OUT alone.
    Check messages are lean: the slip and the evidence, never the fix (as QC2, QC-R1 and QC-R2), in words the class
    reads correctly, as form A's: "typed" ("`mana_now` holds a typed 14. Mar'tu's check put another sheet in
    `gearshift`, and `mana_now` still said 14."), and `None` as "Python's word for nothing".
  * The 12 questions are the quiz rc-part1-c-questions; questions_to_pass=10 on the testout approximates "Part 1 >=
    11/13", as forms A and B (every code task is required; two question misses allowed). Q4 (item 4b, the ledger
    shape) is typed with no choices, as form B, so the answer is in no visible text, and its explanation traces
    another call.
  * Honest tracing in the re-check: R3, the item-4b parallel, is a ledger task in the testout (as QC-R1's
    trace-the-call): the program sits in Mar'tu's text, the editor holds only the two row lines, the hidden setup
    paste_stop() stops a pasted program before it runs (so its number never shows), and the paste guard check names
    it. No assemble (its pieces would be the rows), no Another way. The rows' slips are each named without the number.
  * Review routing (5.2, 5.5): the article rc-review now lives in u10a, right after Part 1 form A, with the master
    ROUTES and its routing helpers. It lists, item by item, the titles students saw, a "Start here" lesson (the
    item's first route), the other lessons to open again, each in a different representation from the check (a
    worked example, Assemble it, the tracer, the ledger), and the twin tasks of the other forms by title (form C's
    titles here must stay as rc-review names them). ROUTES below is an identical copy (checked by script), kept so
    every Part 1 form C item's notes, and the re-check's, carry `review=<unit>/<lesson>/<exercise>,...`.

Check codes (curriculum 2.5), built from one helper prelude (_CX, form B's _BX). check() puts in front of each check
only the helpers it uses (as u07a / u10a / u10b do). Every call a check makes uses fresh values the task never uses
(lint b), with prints kept private; nothing a check does shows in the console:
  NAME/DEF  _find / _params: a function made with `def`, its exact name (near misses, a variable made with `=`), its
           exact parameters in order. Lean wording, never the `def` line.
  CALL     C1: the scout recorder (setup) moves once, north, only when `step_north()` is called. C2: the ley board
           recorder gets the helper's line once. C7: each traceback's function is called with fresh values.
  CMB      _rerun() runs the program again in a fresh namespace (prints private) with a line slipped in right after the
           statement that makes a name: another `choice` (and "option 5", which only `else` answers), another sheet
           in `gearshift` / `lucky`, another `charm_name` and `charm`, `trick_name` and `trick`, other ore, another
           cost, other trips. A typed value cannot follow, and is named in form A's words: "`need` holds a typed 12.
           Mar'tu's check tried other trips and other ore, and `need` still said 12."; "The key is a typed `"Fire
           Coil"`. ... and the key still said `"Fire Coil"`."; "`empty` holds a typed 6 blocks. ... and `empty` still
           had 6 blocks, not 4."; a typed `max_ore` / `ore` in the gauge, a typed cost / start in C8, and a typed
           `need` / start in R1 are each named ("The line takes away a typed 6, not what `cost` holds. ..."). The
           evidence is in short sentences, with no brackets inside brackets. C2 also swaps `get_reading` for one that
           returns another line.
  STO      C2: inside present_reading, the helper's result is stored in a variable, and that variable is passed on (a
           copy of it, or the variable inside a call, counts). When the board does show the line, form A's words come
           first: "Your line runs, and the board shows the line. But `show_on_ley_board()` does not get a variable
           that holds what `get_reading()` returns. The campaign checks for that stored variable." Stored, then
           returned, has its own message: "The function returns the line, so it goes back to the caller and never
           reaches the ley board."
  KEEP     the finished helper `get_reading` is unchanged (AST compare).
  KEY      C4 / R2: the page is stored under the name in `charm_name` / `trick_name` (a quoted variable name, a typed
           key, a rebuilt book that loses its first page, a page that is not the dictionary); C8: the new mana under
           another key.
  STREXACT C3: a compared text that differs from an option only in capitals or spaces.
  RND      C6: `random.randint` swapped for a scripted die that records its arguments; sizes 6 and 10.
  PAR / PAR-CONST / RET / RET-PARAM / PNM / RNM  C9: fuel_cost called with (5, 2) and (7, 6) (the task's own call
           is (4, 3): 12, and neither fresh set gives 12); R4: bar_gap called with (26, 12) and (24, 7) (the task's
           own call is (20, 14): 6); form A's None messages (print, no `return` line, a blank `return`, a `return`
           that never ran: "... so the call gets back `None`, Python's word for nothing."), the same answer twice
           ("both returned `12`: the numbers are typed in the function, so the answer does not follow `miles` and
           `ore_per_mile`."), a typed number with a parameter never read ("it multiplies by a typed 10, not by
           `ore_per_mile`", "it takes away a typed 14, not `mana`", "it starts from a typed 20, not from
           `max_mana`"), a parameter returned as it came in, a near-miss parameter, the Example's box.
  UNCALLED _uncalled (form B's): a line that names one of the code's functions with no brackets, or prints the
           function itself, never runs it (C1, C2, C6, C9, R4).
  ROW      R3: the ledger rows, with the constants, the values handed over, the + 10 too early or dropped, one
           variable only, and text each named without the number.
Messages use invented Tor names only in check data (Knobble, Thorn, Moss Knot, Moth Dance, "A grumpy moth") and the
party's real values; a student's own text is never repeated back (text shows as "some text"). No worksheet name
appears in any check (no `total`, `points`, `bonus`, `health`, `character`, `power_up`).

The class's slips, each proven by a wrong_answers entry (in the task named):
  * typed values instead of reading or handing over (CMB): C2 (a typed board line, a typed store), C3 (the chain
    replaced by one print), C4 (14, 9, `book["Fire Coil"]`, a typed copy of the page), C5 (`"░" * 6`, `"░░░░░░"`), C6
    (`randint(1, 20)`), C7 (`return 9`, a typed gauge line, `return 7`), C8 (`lucky["mana"] = 20`, a typed cost), C9
    (`return 12`, `miles = 4` inside), R1 (`need = 12`, `ore = 18`, a typed start), R2 (26, 13, a typed key, a typed
    page), R4 (`return 6`);
  * print instead of return: C6 (print the roll), C7 (print the label, print the sum), C9, R4; = vs ==: C3
    (`elif choice = ...`), C8 (`==` for `=`), R1 (`==` for `=`); > vs >= at the boundary: Q3, RQ1; unquoted text:
    C1 (`north`), C3 (`option 4`, the starter); quoted names (KEY): C4 (`book["charm_name"]`), R2
    (`tricks["trick_name"]`); a missing colon: C1, C3, C9, R4; a missing indent: C1 (the scout line at the left
    edge, an unindented body), C2 (the pass-on line at the left edge), C3 (the reply at the left edge); def vs =:
    C1 (`def step_north = ...`, `step_north = ...`), C9 (`def fuel_cost = ...`), R4; calling vs handing over (): C2
    (no `()` on the helper, the variable called), Q9 / Q10, RQ3 / RQ4; skipping a nesting level: C4
    (`gearshift["ore"]`), C7 CP1 (the traceback itself), R2 (`lucky["magical_affinity"]`); str() before +: C7 CP2
    (and the call mended instead of the line); parentheses in "░" * (max_ore - ore): C5; resetting a total inside a
    loop: C7 CP3 (`used = 0` moved into the loop); approximate parameter names: C6 (`die_size`, the campaign's
    name), C9 (`ore`, `def fuel_cost(mile, ore):`), R4 (`mana_max`, the parameters swapped); editing a helper you
    were told to leave alone: C2 (`get_reading`).
  Added by the check-breaking pass (each hole closed in the check, then proven by its own wrong_answers entry):
  half-typed values the old reruns let through or could not name: C4 (`gearshift["max_mana"] - 6`: Knobble's sheet
  had Gearshift's own gap of 6, so it passed CP1; Knobble now has 5 of 12 mana), C5 (`"░" * (15 - 9)` and blocks typed
  into the print line, which passed; a count that stays the same across reruns is now named as typed), C7 (the
  global `gear` read inside `ore_in`), R1 (`ore - 12`), C8 / R1 (a typed number after the student changed the data);
  quoted names (KEY) the checks only called "other words": C2 (`show_on_ley_board("reading")`), C6 (`return "roll"`),
  C9 / R4 (`return "need"`, `return "used"`); calling vs handing over: C1 (`scout.step` with no brackets), C6
  (`return random.randint`); `=` for a call: C2 (`show_on_ley_board = reading`); a print that looks right: C1 (the
  scout's own line printed); a missing outdent: C7 CP3 (`return` inside the loop, the first leg only); str() before
  +: C7 CP2 (`str("Gauge: " + ore)`) and a dropped space; RET-PARAM misnamed by chance: R4 `max_mana - 14` gave 12,
  the mana handed in, and was called "a parameter" (now only a parameter returned by every call is).
  Loosened in the same pass (correct or personal work that failed): a changed `ore` / `max_ore` (C5), `cost` (C8)
  or `trips` / `ore_per_trip` / `ore` (R1) is followed on the student's own run (the reruns still use fixed values);
  a reply's own words may change (C3 judges a reply by its speaker); `from random import randint` (C6). The pass
  lines of C5, C8 and R1 no longer name the starter's numbers.
  Added in the teacher's revision (messages in the class's words, each proven by its own wrong_answers entry):
  typed values named in form A's "holds a typed N ... still said N" words in C4, C5, C8, R1 and R2, with new
  entries for a typed `max_ore` (`15 - ore`) and a typed `ore` (`max_ore - 9`) in C5, a typed cost after the student
  changed `cost` in C8, and a typed key the student chose (named as "a typed name", never repeated back) in C4; C9 /
  R4 typed numbers with a parameter never read (`miles * 10`, `miles * 3`, `4 * ore_per_mile`, `miles + 3`,
  `max_mana - 2`, `max_mana - 14`, `20 - mana`) and one call's numbers typed (`4 * 3`); print instead of return and
  no return in C9 / R4 with `None` as "Python's word for nothing" (also a blank `return`, and a `return` inside a
  test that never runs), the same words in C6 and C7; stored, then returned, and returned straight away, in C2 (the
  line goes back to the caller); the STO case where the board shows the line (C2: form A's "Your line runs, and the
  board shows the line. But ..."); calling vs handing over without (): `step_north` (C1) and `present_reading` (C2)
  named with no brackets, `print(toss_die)` (C6), `print(fuel_cost)` (C9), `print(bar_gap)` (R4); def vs =:
  `fuel_cost = 12` (C9, the visible call stops).

Deviations from the spec, each small and noted on its item:
  * Q5 (item 5a) traces `choice = "option 4"` through option 1 / option 2 / else, so `else` runs: the first branch is
    still the spec's distractor. C3 (item 5b) mends `option 4` (the spec's form C) on the last `elif` of four, with an
    `else` fallback, so a test that is only the text (always True) shows when the check tries "option 5".
  * C2 (item 3b) has two checkpoints, store then pass on, as form B.
  * C7 (item 11) puts each slip in its own small function with the calls at the bottom, as form B. No partials:
    Python stops at the first slip, so a program with one slip mended still crashes at the next.
  * The re-check's spec is a list, not a script ("typed items on combine-values, exact-names, param-use and
    return-right-name, the class-wide sheet errors; parallel items for 4, 6 and 9; each student's misses"). R1-R4 and
    RQ1-RQ4 cover the list; "each student's misses" needs the site to draw the parallel item of another form.

What the site does not yet support (listed for the handback; no field was invented):
  * Readiness scoring (5.5) and Review routing as links: the routes are data in `notes` (meta lines) and named
    in rc-review's text (u10a); prose has no item links, so a student finds the lesson by its unit and title. The
    "after two review cycles, continue anyway" rule and the teacher's "Needs you now" flag are site work.
  * Spaced re-check scheduling (site request): rc-recheck should stay hidden until it is due (about a week after the
    student's Readiness Check, before the next campaign module), and passing it must never mark the unit, the
    mini-boss or rc-explain done or tested out. Nothing yet opens it when due, re-verifies tested-out skills there,
    or reverts a missed skill to "practicing".
  * Testouts as a check, not a skip (site request 1): the site lifts every testout out of the item list and marks
    the unit tested out when any form passes. Only form A's rc-part1-a is required (optional=False); forms B and C
    and the re-check are optional, and a pass on any of them must not test the rest of the unit out.
  * Form choice: nothing draws form C for a second retake or a review cycle, opens the one task Mar'tu's notes name,
    or draws another form's questions for a quiz retake.

Phone width: starters, examples, question code, Mar'tu's fenced program, partials and solutions keep to 36
characters, except one line: R2's solution and partial hold the campaign's own nested read, `aff_now =
lucky["abilities"]["magical_affinity"]` (48), the hold-the-barrier shape the class skips a level of. A testout never
shows its solution, and forms A and B kept the campaign's shapes the same way. Checked by script.

Python's messages were checked in CPython 3.13 (the site runs 3.13): `elif choice == option 4:` -> "invalid syntax";
`elif choice = "option 4":` -> "invalid syntax. Maybe you meant '==' or ':=' instead of '='?"; a missing colon ->
"expected ':'"; `def step_north = ...` -> "expected '('"; an unindented body -> "expected an indented block";
`"░" * max_ore - ore` -> "unsupported operand type(s) for -: 'str' and 'int'"; `sheet["ore"]` -> KeyError: 'ore';
`"Gauge: " + ore` -> "can only concatenate str (not "int") to str"; `legg` -> "name 'legg' is not defined";
`get_reading() = reading` -> "cannot assign to function call"; `book[charm] = charm_name` -> "unhashable type:
'dict'"; `random.randint(sides)` -> "missing 1 required positional argument: 'b'".

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u10c
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
# check only the helpers it uses, and the helpers those use, so the unit JSON stays small (as u07a / u10b do).
# This is form B's prelude (_BX), so the three forms judge alike, with form B's _uncalled, plus three additions from
# the check-breaking pass: _rolled also swaps a bare `randint` (`from random import randint`), and _given /
# _quoted_name are new.
# ---------------------------------------------------------------------------------------------

_CX = r'''import ast as _ast
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
    # A scripted randint: records what it was asked, and rolls one below the top face (a d10 rolls 9).
    def randint(_a, _b):
        _log.append((_a, _b))
        if type(_a).__name__ == 'int' and type(_b).__name__ == 'int' and _b > _a:
            return _b - 1
        return _a
    return randint


def _rolled(_f, _args=()):
    # The pretend die stands in for `random.randint`, and for a bare `randint` from `from random import randint`.
    _log = []
    _real = _random.randint
    _fake = _die(_log)
    _G = getattr(_f, '__globals__', {})
    _also = [_k for _k, _v in list(_G.items()) if _v is _real and not _k.startswith('_')]
    _random.randint = _fake
    for _k in _also:
        _G[_k] = _fake
    try:
        _val, _rows, _e = _call(_f, _args)
    finally:
        _random.randint = _real
        for _k in _also:
            _G[_k] = _real
    return _val, _rows, _e, _log


def _given(_name, _default):
    # The plain value the program's first top-level `_name = ...` line holds (the starter's data, or a number the
    # student changed it to), or _default when that line is gone or is not a plain value of the same kind.
    for _n in _tree.body:
        if type(_n).__name__ == 'Assign' and _name in _made_by(_n):
            try:
                _v = _ast.literal_eval(_n.value)
            except Exception:
                return _default
            return _v if type(_v).__name__ == type(_default).__name__ else _default
    return _default


def _quoted_name(_v, _fn):
    # KEY: _v is text that spells the name of a variable or parameter of the student's function `_fn`.
    _d = _defs().get(_fn)
    if _d is None or type(_v).__name__ != 'str':
        return False
    _mine = set(_a.arg for _a in _d.args.args)
    for _n in _ast.walk(_d):
        if _n is not _d:
            _mine.update(_made_by(_n))
    return _v in _mine


def _uncalled():
    # A top-level line that names one of the code's own functions with no brackets after it, so it never runs
    # (or prints the function itself). '' when there is none. (Form B's helper.)
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


def _cx_parts():
    """_CX split into its setup lines and its helper functions, each with the helper names it uses."""
    import ast

    tree = ast.parse(_CX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_CX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_CX_HEAD, _CX_DEFS = _cx_parts()


def check(label, body, setup="", **values):
    """(label, code): the _CX setup lines, the helpers this check uses (and the helpers those use), then the body."""
    import re

    code = fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _CX_DEFS and name not in need:
            need.add(name)
            todo |= _CX_DEFS[name][1]
    head = "\n".join(_CX_HEAD).replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))
    helpers = [text for name, (text, _) in _CX_DEFS.items() if name in need]
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

# No new terms: every [[link]] in this file is defined in an earlier unit.
GLOSSARY = []


# =============================================================================================
# Review routing (5.2 "Review routing", 5.5 "Review first"): for each Part 1 item, the earlier exercises to open
# again, each in a different representation from the unaided check. (unit order, unit id, lesson id, lesson title,
# exercise id, exercise title, the help to use there). The first route of each item is its "Start here" lesson.
# rc-review (Mar'tu's Notes: Where to Look Again), its routing helpers and the master ROUTES now live in u10a, right
# after Part 1 form A. This is an IDENTICAL COPY of u10a's ROUTES, kept only for the `review=` meta lines of form C's
# tasks and questions and of the re-check: THE TWO MUST MATCH (change both, or neither; checked by script).
# =============================================================================================

ROUTES = {
    1: ("glue text with `+` and `str()`", "concat-str", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "glue-words", "Glue words together", "the worked example"),
        (1, "hello-world", "math-and-glue", "Math and Glue", "status-line", "A status line", "Assemble it"),
    ]),
    2: ("replace `pass`", "replace-pass", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "replace-pass", "Replace pass", "Assemble it"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "call-it", "Call it", "the worked example"),
    ]),
    3: ("tidy a line, store it, then pass it on", "chain-methods,store-then-pass", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "store-then-pass", "Store, then pass it on",
         "Assemble it"),
        (7, "spell-recipes", "recipes-read-sheets", "Recipes That Read Stat Sheets", "bar-then-draw",
         "Build the bar, then draw it", "the tracer"),
    ]),
    4: ("exactly enough, and tracing a call", "boundary,return-comparison,trace-call", [
        (2, "control-flow", "true-or-false-yes", "True or False, Yes?", "enough-to-pass", "Enough to pass",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "return-a-comparison", "Return a comparison",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "be-the-ledger", "Be the ledger",
         "the ledger"),
    ]),
    5: ("which branch runs, and text in quotes", "elif-chain,quote-text", [
        (2, "control-flow", "if-the-clock-turns-red", "If the Clock Turns Red", "clock-colors", "Clock colors",
         "the tracer"),
        (1, "hello-world", "words-in-quotes", "Words in Quotes", "words-need-quotes", "Words need quotes",
         "the worked example"),
    ]),
    6: ("read and write a stat sheet", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable", [
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "read-by-key", "Read by key", "the worked example"),
        (5, "dictionaries", "sheets-inside-sheets", "Sheets Inside Sheets", "abilities-inside", "Abilities inside",
         "the worked example"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "key-from-a-box", "A key from a box", "Assemble it"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "is-it-in", "Is it in the book?", "the worked example"),
    ]),
    7: ("a bar of blocks", "repeat-string", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "repeat-a-mark", "Repeat a mark", "Assemble it"),
        (7, "spell-recipes", "recipes-read-sheets", "Recipes That Read Stat Sheets", "bar-then-draw",
         "Build the bar, then draw it", "the tracer"),
    ]),
    8: ("roll a die", "randint,randint-param", [
        (2, "control-flow", "if-the-clock-turns-red", "If the Clock Turns Red", "roll-a-die", "Roll a die",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "roll-recipe", "A rolling recipe",
         "Assemble it"),
    ]),
    9: ("a function stored in a dictionary", "func-as-value,call-stored-func", [
        (7, "spell-recipes", "spells-you-can-hand-over", "Spells You Can Hand Over", "name-without-parentheses",
         "A name without parentheses", "the tracer"),
        (7, "spell-recipes", "spells-you-can-hand-over", "Spells You Can Hand Over", "cast-from-the-book",
         "Cast from the book", "Assemble it"),
    ]),
    10: ("a loop over a list of sheets", "list-of-dicts,for-each", [
        (6, "loops", "for-each-yes", "For Each, Yes?", "predict-the-loop", "Predict the loop", "the tracer"),
        (5, "dictionaries", "sheets-inside-sheets", "Sheets Inside Sheets", "the-roster", "The roster",
         "the worked example"),
    ]),
    11: ("read a traceback", "read-traceback", [
        (2, "control-flow", "when-spells-fizzle", "When Spells Fizzle: Reading Errors", "debug-routine",
         "The four-step routine", "Assemble it"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "key-errors", "Key errors", "Assemble it"),
        (6, "loops", "for-each-yes", "For Each, Yes?", "running-total", "Running total", "the tracer"),
    ]),
    12: ("spend mana from a sheet", "dict-write,reassign,combine-values", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "spend-mana", "Spend some mana", "the tracer"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "write-by-key", "Write by key", "the worked example"),
    ]),
    13: ("write a function from its goal", "param-use,return-right-name,exact-names", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "use-the-ingredients", "Use the ingredients",
         "Assemble it"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "return-the-right-box", "Return the right box",
         "Assemble it"),
        (1, "hello-world", "boxes-with-labels", "Boxes With Labels", "exact-names", "Exact names", "Assemble it"),
    ]),
}


def _review(item):
    """`review=` for a meta line: the item's routes as unit/lesson/exercise ids."""
    return ",".join(f"{unit}/{lesson}/{ex}" for _, unit, lesson, _, ex, _, _ in ROUTES[item][2])


def _rc(item, part, skills, checks, prepares, **more):
    """The meta line every Part 1 item carries (5.3): its item number, its skill tags (the same as forms A and B's,
    item for item), the tags this part checks, the campaign part it prepares, and its review routes."""
    return meta(rc_item=item, form="C", part=part, skills=skills, checks=checks, prepares=prepares, solo="true",
                review=_review(item), **more)


_P1_NOTE = ("Part 1 is unaided: support='none' (no hints, Another way, Assemble it, tracer or Compare) and "
            "explainer='lean'; glossary and read-aloud stay on. The hints exist because the schema needs two; they "
            "never hold a finished line. Check messages are lean: the slip and the evidence, never the fix.")
# The last line of every Part 1 form C task's and every re-check task's Learn text, as forms A and B.
_STUCK = "Stuck? Skip it, and come back. A task you pass here stays ticked."


# =============================================================================================
# Shared check bodies (filled with fill(); every message is lean: the slip and the evidence, never the fix)
# =============================================================================================

# NAME + CALL on the scout recorder: one step, in the function's direction, only when the function is called.
_STEP = r'''
_fn, _dir, _known = __FN__, __DIR__, __KNOWN__
_f, _m = _find(_fn)
assert _f, _m
_sc = _f.__globals__.get('scout')
assert type(_sc).__name__ == '_Scout', ('A variable of your own is named `scout`, so the scout from the starter is '
                                        'gone.')
_at = len(_sc.steps)
_what = 'called `' + _fn + '()`'
_v, _rows, _e = _call(_f)
_new = _sc.steps[_at:]
del _sc.steps[_at:]
if type(_e).__name__ == 'NameError':
    _nm = getattr(_e, 'name', '') or ''
    assert not (_nm == 'party' or _nm.startswith('move_')), (
        '`' + _nm + "` is from the campaign's cabin door, not from this program."
        + _ev(_what, 'Python stopped with a NameError'))
    assert _nm.lower() not in _known, ('`' + _nm + '` has no quotes, so Python looked for a variable with that '
                                       'name.' + _ev(_what, 'Python stopped with a NameError'))
if type(_e).__name__ == 'AttributeError' and getattr(_e, 'obj', None) is _sc:
    assert False, ('The scout has no `.' + str(getattr(_e, 'name', '') or '') + '`.'
                   + _ev(_what, 'Python stopped with an AttributeError'))
assert _e is None, 'Calling `' + _fn + '()` stopped Python: ' + _err(_e) + '.' + _ev(_what)
if not _new:
    _loose = [_c for _n in _top() for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
              and type(_c.func).__name__ == 'Attribute' and _c.func.attr == 'step']
    assert not _loose, ('The scout line runs on its own, at the left edge, not when the function is called.'
                        + _ev(_what, 'the scout did not move'))
    _d = _defs().get(_fn)
    _named = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Attribute' and _n.attr == 'step'] if _d else []
    _called = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Attribute'
               and _n.func.attr == 'step'] if _d else []
    assert len(_named) <= len(_called), ('`scout.step` has no brackets after it, so nothing calls it.'
                                         + _ev(_what, 'the scout did not move'))
    assert not _rows, '`' + _fn + '` printed a line, but the scout did not move.' + _ev(_what, 'the scout stayed put')
    assert False, 'Nothing in `' + _fn + '` moves the scout.' + _ev(_what, 'the scout did not move')
assert len(_new) == 1, 'The function moves the scout ' + str(len(_new)) + ' times.' + _ev(_what)
_s = _new[0]
if _s != _dir:
    assert not (type(_s).__name__ == 'str' and _s.strip().lower() == _dir), (
        "The direction has other letters than the function's name: capitals and spaces count." + _ev(_what))
    assert False, ('The scout moved ' + (_s if _s in _known else 'another way') + ", not the way the function's "
                   'name says.' + _ev(_what))
_u = _uncalled()
assert not _u, _u
'''

# STO + KEEP: the finished helper is unchanged, and a variable inside the function holds the result of a call to it.
_STORE = r'''
_helper, _fn = __HELPER__, __FN__
_k = _keep(_helper, __ORIG__)
assert _k != 'gone', 'The finished `' + _helper + '()` is gone from the code.'
assert not _k, '`' + _helper + '()` is not the same as in the starter, and it was marked finished.'
_fs, _m = _find(_fn)
assert _fs, _m
_d = _defs()[_fn]
if not _from_call(_d, _helper):
    _bare = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Name'
             and _n.value.id == _helper]
    assert not _bare, '`' + _fn + '()` stores the function `' + _helper + '` itself: nothing calls it.'
    _outside = [_n for _n in _top() if type(_n).__name__ == 'Assign' and _is_call(_n.value, _helper)]
    assert not _outside, 'The result of `' + _helper + '()` is stored outside `' + _fn + '()`, at the left edge.'
    _direct = [_c for _c in _calls_in([_d], 'show_on_ley_board') if [_a for _a in _c.args if _is_call(_a, _helper)]]
    if _direct:
        # Run it once, privately: when the board does show the line, say so first (form A's STO wording).
        _bd = _fs.__globals__.get('_board')
        _at = len(_bd) if type(_bd).__name__ == 'list' else 0
        _v, _rows, _e = _call(_fs)
        _shown = _bd[_at:] if type(_bd).__name__ == 'list' else []
        _line = _call(_fs.__globals__.get(_helper))[0]
        assert not (_e is None and _shown == [_line]), (
            'Your line runs, and the board shows the line. But `show_on_ley_board()` does not get a variable that '
            'holds what `' + _helper + '()` returns. The campaign checks for that stored variable.')
        assert False, ('`' + _fn + '()` hands `' + _helper + '()` straight to the board: no variable holds the '
                       'result first.')
    _typed = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Constant']
    assert not _typed, '`' + _fn + '()` stores typed words, not the result of `' + _helper + '()`.'
    _only = all(type(_s).__name__ == 'Pass' or (type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Constant')
                for _s in _d.body)
    assert not _only, '`' + _fn + '()` still holds only `pass`.'
    assert False, 'No variable inside `' + _fn + '()` holds the result of `' + _helper + '()`.'
'''

# CALL + CMB + STO: the board gets the helper's line once, follows a swapped helper, and is handed the stored variable.
_PASS_ON = r'''
_helper, _fn, _swap = __HELPER__, __FN__, __SWAP__
_fs, _m = _find(_fn)
assert _fs, _m
_G = _fs.__globals__
_board = _G['_board']
_what = 'called `' + _fn + '()`'
_at = len(_board)
_v, _rows, _e = _call(_fs)
assert _e is None, 'Calling `' + _fn + '()` stopped Python: ' + _err(_e) + '.' + _ev(_what)
_shown = _board[_at:]
_d = _defs()[_fn]
if not _shown:
    _over = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and 'show_on_ley_board' in _made_by(_n)]
    assert not _over, ('A line with `=` makes a new variable called `show_on_ley_board`, so nothing calls the '
                       'board.' + _ev(_what, 'the board stayed empty'))
    assert not _rows, '`' + _fn + '()` printed a line, but nothing reached the board.' + _ev(_what)
    # Stored, then returned (or returned straight away): the line goes back to the caller, never to the board.
    assert not (_v is not None and _v == _call(_G.get(_helper))[0]), (
        'The function returns the line, so it goes back to the caller and never reaches the ley board.' + _ev(_what))
    assert False, '`' + _fn + '()` put nothing on the board.' + _ev(_what)
assert len(_shown) == 1, '`' + _fn + '()` put ' + str(len(_shown)) + ' things on the board.' + _ev(_what)
assert type(_shown[0]).__name__ != 'function', ('The board was handed the function `' + _shown[0].__name__
                                                + '` itself, not its words.' + _ev(_what))
assert not _quoted_name(_shown[0], _fn), ("The board was handed a variable's name in quotes: those exact letters, "
                                          'not what the variable holds.' + _ev(_what))
_real = _G.get(_helper)
_want = _call(_real)[0]
assert _shown[0] == _want, 'The board showed other words than `' + _helper + '()` returns.' + _ev(_what)
_said = 'made `' + _helper + '()` return other words'
_G[_helper] = lambda: _swap
try:
    _at = len(_board)
    _v, _rows, _e = _call(_fs)
finally:
    _G[_helper] = _real
assert _e is None, 'With other words from `' + _helper + '()`, Python stopped: ' + _err(_e) + '.' + _ev(_said)
_shown = _board[_at:]
assert _shown and _shown[0] == _swap, (
    'When `' + _helper + '()` returned other words, the board still showed the old ones.' + _ev(_said))
_d = _defs()[_fn]
_stored = _from_call(_d, _helper)
_more = True
while _more:
    # a variable copied from the stored one (`words = reading`) holds the result too (as form B)
    _more = False
    for _n in _ast.walk(_d):
        if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Name' and _n.value.id in _stored:
            for _x in _made_by(_n):
                if _x not in _stored:
                    _stored.append(_x)
                    _more = True
_args = [_a for _c in _calls_in([_d], 'show_on_ley_board') for _a in list(_c.args) + [_k.value for _k in _c.keywords]]
if not [_x for _a in _args for _x in _ast.walk(_a) if type(_x).__name__ == 'Name' and _x.id in _stored]:
    # The board did show the line (both runs above), so the STO message says so first, in form A's words.
    assert not [_a for _a in _args if _is_call(_a, _helper)], (
        'Your line runs, and the board shows the line. But the board was handed a new call of `' + _helper + '()`, '
        'not the variable that holds the result.')
    assert False, ('Your line runs, and the board shows the line. But `show_on_ley_board()` does not get a variable '
                   'that holds what `' + _helper + '()` returns. The campaign checks for that stored variable.')
_u = _uncalled()
assert not _u, _u
'''

# CMB over every option (and one more, which only `else` answers) + STREXACT.
_REPLY = r'''
_RUNS, _ORDER = __RUNS__, __ORDER__
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


# A reply counts by its speaker, so a reply's own words may be changed (made the student's own).
_WHO = [_who(_l) for _l in _LINES]
for _i in _ORDER:
    _c, _want = _RUNS[_i]
    _ns, _ls, _e, _miss = _rerun([('choice', 'choice = ' + repr(_c))])
    assert not _miss, _gone('choice')
    _said = 'set `choice = "' + _c + '"`'
    _with = 'With `choice = "' + _c + '"`, '
    assert _e is None, _with + 'Python stopped: ' + _err(_e) + '.' + _ev(_said)
    _got = [_l for _l in _ls if _who(_l) in _WHO]
    if [_who(_x) for _x in _got] == [_who(_want)]:
        continue
    assert not _near, ('Line ' + str(_near[0]) + ' compares `choice` with a text that differs from an option only in '
                       'its capitals or spaces.' + _ev(_said, _who(_want) + "'s reply did not print"))
    assert _got, _with + 'none of the replies printed.' + _ev(_said)
    assert len(_got) == 1, _with + str(len(_got)) + ' replies printed.' + _ev(_said)
    assert False, _with + _who(_got[0]) + "'s reply printed, not " + _who(_want) + "'s." + _ev(_said)
'''

# A read from a sheet (or a value built from the program's numbers, `mult`): the value now, then CMB with another
# sheet or other numbers (a typed number cannot follow).
_FOLLOW = r'''
_T, _WANT, _PLACE, _MULT = __TARGET__, __WANT__, __PLACE__, __MULT__
if _MULT:
    # The value is built from the program's own numbers, so a number the student changed is followed too.
    _WANT = 1
    for _nm, _dv in _MULT:
        _WANT = _WANT * _given(_nm, _dv)
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
        # CMB, in form A's words: the value was typed, and the other values did not change it.
        assert _got != _WANT, ('`' + _T + '` holds a typed ' + str(_WANT) + ". Mar'tu's check " + _what + ', and `'
                               + _T + '` still said ' + str(_got) + '.')
        assert False, 'With ' + _said + ', `' + _T + '` held ' + _show(_got) + ', not ' + _show(_want) + '.' + _ev(_what)
'''

# KEY + CMB: the dictionary gets the value under the name the key variable holds, keeps its first page, and follows
# another name and another value.
_STORE_BY_NAME = r'''
_BK, _KV, _VV, _KEPT, _NEWKEY, _FIELD, _PAGE = __BK__, __KV__, __VV__, __KEPT__, __NEWKEY__, __FIELD__, __PAGE__
_OLDKEY = __OLDKEY__
_b = _g.get(_BK)
assert type(_b).__name__ == 'dict', '`' + _BK + '` is not a dictionary any more.'
assert _KEPT in _b, '`' + _BK + '` lost its ' + _KEPT + ' ' + _PAGE + '.'
_wn = _g.get(_KV)
assert not (_KV in _b and _wn != _KV), (
    '`' + _BK + '` got ' + ('an ' if _PAGE[0] in 'aeiou' else 'a ') + _PAGE + ' under the key `"' + _KV + '"`: those '
    'exact letters, not the name the variable holds.')
assert type(_wn).__name__ == 'str' and _wn in _b, '`' + _BK + '` has no ' + _PAGE + ' under the name that `' + _KV + '` holds.'
_p = _b[_wn]
assert type(_p).__name__ == 'dict', 'The new ' + _PAGE + ' holds ' + _show(_p) + ', not the `' + _VV + '` dictionary.'
for _changes, _val, _said, _what in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _nb = _ns.get(_BK)
    if type(_nb).__name__ == 'dict' and _NEWKEY not in _nb and _wn in _nb:
        # CMB, in form A's words: the key was typed, and another name in the key variable did not change it. The
        # starter's own name is shown; a name the student chose is not repeated back (2.11).
        _was = '`"' + _wn + '"`' if _wn == _OLDKEY else 'the name you typed'
        assert False, ('The key is a typed ' + ('`"' + _wn + '"`' if _wn == _OLDKEY else 'name') + ". Mar'tu's check "
                       'put another name in `' + _KV + '`, and the key still said ' + _was + '.')
    assert type(_nb).__name__ == 'dict' and _NEWKEY in _nb, (
        'With ' + _said + ', `' + _BK + '` got nothing under ' + _NEWKEY + ': the key does not follow `' + _KV + '`.'
        + _ev(_what))
    _np = _nb[_NEWKEY]
    assert type(_np).__name__ == 'dict' and _np.get(_FIELD) == _val, (
        'With ' + _said + ', the ' + _NEWKEY + ' ' + _PAGE + ' did not hold the new `' + _VV + '`.' + _ev(_what))
'''

# A bar of blocks: `empty` holds one `░` per point used, now (with the program's own numbers) and with other
# numbers; `full` and the printed bar follow.
_BAR = r'''
_first = None
for _changes, _m, _mx, _said, _what in __RUNS__:
    if _changes:
        _ns, _ls, _e, _miss = _rerun(_changes)
        assert not _miss, _gone(_miss[0])
        assert _e is None, _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
        _lead, _tail = _said + ', ', _ev(_what)
    else:
        # The student's own run follows the program's own numbers, so a changed `ore` or `max_ore` is fine.
        _m, _mx = _given('ore', _m), _given('max_ore', _mx)
        _m0, _x0 = _m, _mx
        _ns, _ls, _lead, _tail = _g, _lines(), '', ''
    _em, _fu = _ns.get('empty'), _ns.get('full')
    assert type(_em).__name__ == 'str', _lead + '`empty` holds ' + _show(_em) + ', not blocks.' + _tail
    assert _em == '░' * len(_em), _lead + '`empty` holds other marks, not only `░` blocks.' + _tail
    if len(_em) != _mx - _m:
        # CMB, in form A's words: a typed count, a typed `max_ore` or a typed `ore` did not follow the check's numbers.
        _not = ' blocks, not ' + str(_mx - _m) + '.'
        _put = "Mar'tu's check put " + str(_m) + ' in `ore` and ' + str(_mx) + ' in `max_ore`'
        assert not (_changes and len(_em) == _first), ('`empty` holds a typed ' + str(_first) + ' blocks. ' + _put
                                                       + ', and `empty` still had ' + str(_first) + _not)
        assert not (_changes and _mx != _x0 and len(_em) == max(0, _x0 - _m)), (
            'Your `empty` line holds a typed ' + str(_x0) + ". Mar'tu's check put " + str(_mx) + ' in `max_ore`, and '
            '`empty` still had ' + str(_x0) + ' minus `ore`: ' + str(len(_em)) + _not)
        assert not (_changes and _m != _m0 and len(_em) == max(0, _mx - _m0)), (
            'Your `empty` line holds a typed ' + str(_m0) + ". Mar'tu's check put " + str(_m) + ' in `ore`, and '
            '`empty` still had `max_ore` minus ' + str(_m0) + ': ' + str(len(_em)) + _not)
        assert False, _lead + '`empty` held ' + str(len(_em)) + ' blocks, not ' + str(_mx - _m) + '.' + _tail
    if _first is None:
        _first = len(_em)
    assert type(_fu).__name__ == 'str' and _fu == '█' * _m, (
        _lead + '`full` did not hold ' + str(_m) + ' `█` blocks.' + _tail)
    _bar = [_l for _l in _ls if _fu + _em in _l and _l.count('░') == len(_em) and _l.count('█') == len(_fu)]
    assert _bar, _lead + 'the bar line did not show `full`, then `empty`, and only those blocks.' + _tail
'''

# RND: a scripted die records the roll; one roll, from 1 to the size handed in, and that roll returned.
_ROLL = r'''
_fn, _p, _sizes = __FN__, __PARAM__, __SIZES__
_f, _m = _find(_fn)
assert _f, _m
_ps = _params(_f)
assert _ps == [_p], 'The `def` line of `' + _fn + '` has ' + _names(_ps) + ', and the starter has `' + _p + '`.'
_d = _defs()[_fn]
_inner = [_n for _n in _ast.walk(_d) if _n is not _d and _p in _made_by(_n)]
_typed = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Call' and len(_c.args) == 2
          and ((type(_c.func).__name__ == 'Attribute' and _c.func.attr == 'randint') or _is_call(_c, 'randint'))
          and type(_c.args[1]).__name__ == 'Constant']
for _size in _sizes:
    _c = '`' + _fn + '(' + str(_size) + ')`'
    _what = 'called ' + _c + ' with a pretend die that rolls one below its top face'
    _val, _rows, _e, _log = _rolled(_f, (_size,))
    assert _e is None, _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    assert _log, _c + ' returned ' + _show(_val) + ' and rolled no die.' + _ev(_what)
    assert len(_log) == 1, _c + ' rolled ' + str(len(_log)) + ' times.' + _ev(_what)
    _a, _b = _log[0]
    if (_a, _b) != (1, _size):
        _span = _c + ' rolled from ' + str(_a) + ' to ' + str(_b)
        assert not _inner, _span + ': a line inside the function sets `' + _p + '`.' + _ev(_what)
        assert not _typed, _span + ': the top face is a typed number.' + _ev(_what)
        assert _a != 0, _span + ': a die has no 0 face.' + _ev(_what)
        assert _b != _size + 1, _span + ': one face too many.' + _ev(_what)
        assert False, _span + '.' + _ev(_what)
    if _val != _b - 1:
        assert not (_val is None and _rows), (_c + " printed the roll and returned `None`, Python's word for "
                                              'nothing.' + _ev(_what))
        assert _val is not None, _c + " rolled, then returned `None`, Python's word for nothing." + _ev(_what)
        assert not _quoted_name(_val, _fn), (_c + " returned a variable's name in quotes: those exact letters, not "
                                             'what the variable holds.' + _ev(_what))
        assert False, _c + ' rolled ' + str(_b - 1) + ' but returned ' + _show(_val) + '.' + _ev(_what)
_u = _uncalled()
assert not _u, _u
'''

# Spend from a sheet: the new mana is stored back under "mana", and follows another sheet and another cost.
_SPEND = r'''
_SV, _START, _WANT = __SV__, __START__, __WANT__
# The student's own run follows the program's own numbers (the sheet's first mana and `cost`), so a changed cost is
# fine; the reruns still try fixed other values.
_s0 = _given(_SV, {})
_START = _s0['mana'] if type(_s0.get('mana')).__name__ == 'int' else _START
_COST = _given('cost', _START - _WANT)
_WANT = _START - _COST
_lbl = '`' + _SV + '["mana"]`'
_o = _g.get(_SV)
assert type(_o).__name__ == 'dict', '`' + _SV + '` is not a dictionary any more.'
_m = _o.get('mana')
if _m != _WANT:
    if _m == _START:
        _still = _lbl + ' is still ' + str(_START)
        assert not [_k for _k in _o if _k not in ('name', 'mana')], _still + ': the new value went under another key.'
        _cmp = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare']
        assert not _cmp, _still + ': the line with `==` compares, and stores nothing.'
        _bare = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
        assert not _bare, _still + ': the subtraction is worked out, then forgotten.'
        _shown = [_c for _c in _calls_in(_top(), 'print') if [_a for _a in _c.args if type(_a).__name__ == 'BinOp']]
        assert not _shown, _still + ': the new mana is printed, not stored.'
        _box = [_x for _n in _top() if type(_n).__name__ in ('Assign', 'AugAssign')
                and type(_n.value).__name__ == 'BinOp' for _x in _made_by(_n)]
        assert not _box, _still + ': the new mana went into `' + _box[0] + '`.'
        assert False, _still + '.'
    assert False, _lbl + ' is ' + _show(_m) + ', not `' + str(_WANT) + '`.'
for _changes, _want, _said, _what, _who, _start, _cost in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _no = _ns.get(_SV)
    _got = _no.get('mana') if type(_no).__name__ == 'dict' else None
    if _got != _want:
        # CMB, in form A's words: the result, the cost or the start was typed, and the check's values did not
        # change it.
        assert _got != _WANT, (_lbl + ' holds a typed ' + str(_WANT) + ". Mar'tu's check " + _what + ', and '
                               + _lbl + ' still said ' + str(_got) + '.')
        assert not (_cost != _COST and _got == _start - _COST), (
            'The line takes away a typed ' + str(_COST) + ", not what `cost` holds. Mar'tu's check put "
            + str(_cost) + ' in `cost`, and the line still took away ' + str(_COST) + ': ' + _who + "'s mana ended "
            'at ' + str(_got) + '.')
        assert not (_start != _START and _got == _START - _cost), (
            'The line starts from a typed ' + str(_START) + ', not from ' + _lbl + ". Mar'tu's check put " + _who
            + "'s sheet in `" + _SV + '`, mana ' + str(_start) + ', and the line still started from ' + str(_START)
            + ': ' + _who + "'s mana ended at " + str(_got) + '.')
        assert False, ('With ' + _said + ', ' + _lbl + ' ended at ' + _show(_got) + ', not `' + str(_want) + '`.'
                       + _ev(_what))
'''

# NAME + PAR / PAR-CONST / RET / RET-PARAM / PNM / RNM: the function, called with two fresh argument sets.
_FUNC = r'''
_fn, _want_ps, _cases, _foreign, _follow = __FN__, __PARAMS__, __CASES__, __FOREIGN__, __FOLLOW__
_f, _m = _find(_fn)
assert _f, _m
_ps = _params(_f)
assert _ps == _want_ps, ('The `def` line of `' + _fn + '` has ' + _names(_ps) + ', and the task names '
                         + _names(_want_ps) + '.')
_d = _defs().get(_fn)
_rets = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return'] if _d is not None else []
# A whole number typed into a sum inside the function, with a parameter the function never reads (`miles * 10`,
# `max_mana - 14`, `20 - mana`): the typed-number slip, named before the plain 'not N' (form A's wording).
_read = set(_n.id for _n in (_ast.walk(_d) if _d is not None else []) if type(_n).__name__ == 'Name'
            and type(_n.ctx).__name__ == 'Load')
_unread = [_p for _p in _ps if _p not in _read]
_how = {'Mult': ('multiplies by', 'not by'), 'Add': ('adds', 'not'), 'Sub': ('takes away', 'not')}
_typed = [(('starts from', 'not from') if type(_b.op).__name__ == 'Sub' and _x is _b.left
           else _how[type(_b.op).__name__], _x.value)
          for _b in (_ast.walk(_d) if _d is not None else []) if type(_b).__name__ == 'BinOp'
          and type(_b.op).__name__ in _how for _x in (_b.left, _b.right)
          if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'int' and _x.value not in (0, 1)]
_res = []
for _args, _want in _cases:
    _c = '`' + _fn + '(' + ', '.join(str(_a) for _a in _args) + ')`'
    _val, _rows, _e = _call(_f, tuple(_args))
    assert _e is None, (_c + ' stopped Python: ' + _err(_e) + '.' + _stopped(_fn, _ps, _e, _foreign)
                        + _ev('called ' + _c))
    _res.append((_c, _val, _rows, _want, tuple(_args)))
_what = 'called ' + ' and '.join(_r[0] for _r in _res)
# `None` in the class's words (form A's messages): Python's word for nothing.
_word = ", Python's word for nothing."
_none = ', so the call gets back `None`' + _word
for _c, _val, _rows, _want, _args in _res:
    if _val is None:
        assert not _rows, '`' + _fn + '` prints its answer, but the call gets back `None`' + _word + _ev(_what)
        assert _rets, '`' + _fn + '` has no `return` line' + _none + _ev(_what)
        assert [_x for _x in _rets if _x.value is not None], '`return` stands on its own' + _none + _ev(_what)
        assert False, 'No `return` line ran for ' + _c + _none + _ev(_what)
(_c1, _v1), (_c2, _v2) = [(_r[0], _r[1]) for _r in _res]
assert not (_v1 == _v2 and _quoted_name(_v1, _fn)), (_c1 + ' and ' + _c2 + " both returned a variable's name in "
                                                     'quotes: those exact letters, not what the variable holds.'
                                                     + _ev(_what))
assert not (_v1 == _v2 and _v1 != _res[0][3]), (_c1 + ' and ' + _c2 + ' both returned ' + _show(_v1) + ': the '
                                                'numbers are typed in the function, so the answer does not follow '
                                                + _names(_ps) + '.' + _ev(_what))
# RET-PARAM only when every call hands back the same parameter as it came in (one match can be chance).
_same = [_i for _i in range(len(_ps)) if all(_r[1] == _r[4][_i] for _r in _res)]
for _c, _val, _rows, _want, _args in _res:
    if _val != _want:
        assert not _same, _c + ' returned ' + _show(_val) + ': a parameter, just as it came in.' + _ev(_what)
        if _typed and _unread:
            (_verb, _nob), _k = _typed[0]
            assert False, (_c + ' returned ' + _show(_val) + ': it ' + _verb + ' a typed ' + str(_k) + ', ' + _nob
                           + ' `' + _unread[0] + '`, so the answer does not follow '
                           + _follow.get(_unread[0], '`' + _unread[0] + '`') + '.' + _ev(_what))
        assert False, _c + ' returned ' + _show(_val) + ', not `' + str(_want) + '`.' + _ev(_what)
_u = _uncalled()
assert not _u, _u
'''


# =============================================================================================
# Part 1 form C, code tasks (testout rc-part1-c)
# =============================================================================================

DIRECTIONS = ["north", "south", "east", "west"]

# Hidden setup recorders (engine-like helpers, 2.12 rule 3): the scout and the ley board.
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
)
BOARD_SETUP = (
    "_board = []\n"
    "\n"
    "\n"
    "def show_on_ley_board(text):\n"
    "    _board.append(text)\n"
    "    print(\"[Ley board] \" + str(text))\n"
)

# ---------------------------------------------------------------------------------------------
# C1 (item 2) step north: replace-pass. NAME + CALL on the scout recorder.
# ---------------------------------------------------------------------------------------------

NORTH_OK = '    scout.step("north")'


def _north(body="    pass", calls=True, head="def step_north():"):
    return (
        "# Replace pass with a command\n"
        "# that moves the scout north.\n"
        "# The scout moves like this:\n"
        "#     scout.step(\"west\")\n"
        f"{head}\n"
        f"{body}\n"
        + ("\n\n# Mar'tu's test call. Leave it.\nstep_north()\n" if calls else "")
    )


NORTH_STARTER = _north()
NORTH_SOLUTION = _north(NORTH_OK)

STEP_NORTH = dict(
    id="step-north",
    title="Step north",
    martu=(
        "A campaign-style starter, like the cabin door. `step_north` only says `pass`. Make it move the scout north.\n"
        "My check calls it, only inside the check.\n" + _STUCK
    ),
    names=["step_north", "scout"],
    setup=SCOUT_SETUP,
    support="none",
    explainer="lean",
    starter=NORTH_STARTER,
    checkpoints=[
        dict(
            id="replace-pass-north",
            text="Replace `pass` with a command that moves the scout north.",
            dictated=False,
            hints=[
                "Read the comment: it shows how the scout moves. Which word of the function's name says where?",
                "`pass` holds the place of one indented line.",
                "A word the scout must follow goes in quotes, in small letters.",
            ],
            checks=[check("step_north moves the scout north", _STEP, fn="step_north", dir="north", known=DIRECTIONS)],
            pass_line="The scout steps north. Good, yes?",
        ),
    ],
    solution=NORTH_SOLUTION,
    wrong_answers=[
        dict(why="the starter (pass)", code=NORTH_STARTER, fails_at=1, message_contains="Nothing in `step_north`"),
        dict(why="unquoted text: scout.step(north) (the run stops at the test call)",
             code=_north("    scout.step(north)"), fails_at=0, message_contains="name 'north' is not defined"),
        dict(why="unquoted text, the test call removed (the check names it)",
             code=_north("    scout.step(north)", calls=False), fails_at=1, message_contains="has no quotes"),
        dict(why="the comment's example direction copied", code=_north('    scout.step("west")'), fails_at=1,
             message_contains="moved west"),
        dict(why="the opposite direction", code=_north('    scout.step("south")'), fails_at=1,
             message_contains="moved south"),
        dict(why="a capital letter in the text", code=_north('    scout.step("North")'), fails_at=1,
             message_contains="capitals"),
        dict(why="the step at the left edge, pass kept (a missing indent: it runs at once, not when called)",
             code=_north('    pass\nscout.step("north")'), fails_at=1, message_contains="runs on its own"),
        dict(why="the body not indented, pass removed (IndentationError)", code=_north('scout.step("north")'),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="print instead of a command", code=_north('    print("north")'), fails_at=1,
             message_contains="printed a line, but the scout did not move"),
        dict(why="the scout's line printed instead of moving it (looks right in the console)",
             code=_north('    print("The scout steps north.")'), fails_at=1,
             message_contains="printed a line, but the scout did not move"),
        dict(why="no brackets after scout.step: named, not called (calling vs handing over)",
             code=_north("    scout.step", calls=False), fails_at=1, message_contains="has no brackets"),
        dict(why="unquoted text with a capital, the test call removed", code=_north("    scout.step(North)", calls=False),
             fails_at=1, message_contains="`North` has no quotes"),
        dict(why="two steps in one call", code=_north(NORTH_OK + "\n" + NORTH_OK), fails_at=1,
             message_contains="2 times"),
        dict(why="the campaign's party.move copied (the run stops at the test call)",
             code=_north('    party.move("north")'), fails_at=0, message_contains="name 'party' is not defined"),
        dict(why="the campaign's party.move, the test call removed", code=_north('    party.move("north")', calls=False),
             fails_at=1, message_contains="campaign's cabin door"),
        dict(why="scout.move for scout.step, the test call removed", code=_north('    scout.move("north")', calls=False),
             fails_at=1, message_contains="has no `.move`"),
        dict(why="a missing colon on the def line", code=_north(NORTH_OK, head="def step_north()"), fails_at=0,
             message_contains="expected ':'"),
        dict(why="def used like = (def vs =)", code="def step_north = scout.step(\"north\")\n", fails_at=0,
             message_contains="expected '('"),
        dict(why="= used to make the function, the test call removed (def vs =)",
             code="step_north = scout.step(\"north\")\n", fails_at=1, message_contains="a line with `=`"),
        dict(why="the test call left without () (calling vs naming): it never runs, so the check names it",
             code=_north(NORTH_OK, calls=False) + "\n\nstep_north\n", fails_at=1,
             message_contains="names `step_north` with no brackets after it"),
        dict(why="a capital in the function's name, the test call removed (NAME)",
             code=_north(NORTH_OK, calls=False, head="def Step_north():"), fails_at=1,
             message_contains="letter for letter"),
    ],
    notes=_rc(2, "code", "replace-pass", "replace-pass", "program-movement", starter_level="S4", path="READY",
              dictates="", foreign_names="west") + "\n"
    "C1, item 2 (form A: step_west, its comment's example south; form B: step_east). Campaign-style starter (G3 R18): "
    "the `def` line and `pass`, with the test call below, as form A. NAME + CALL: the check calls `step_north()` "
    "itself and reads the scout recorder (setup): one step, `\"north\"`, and only when called (a step at the left "
    "edge runs at load and is named). Fails on (spec): `scout.step(north)` -> crash (the explainer's NameError row; "
    "with the call removed the check names the missing quotes); the comment's `\"west\"` -> CALL. A test call left "
    "with no brackets (`step_north`) is named (form B's _uncalled). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C2 (item 3b) present the reading: store-then-pass (3a, chain-methods, is quiz Q2). STO, CALL, CMB, KEEP.
# ---------------------------------------------------------------------------------------------

READING_DEF = (
    "def get_reading():\n"
    '    line = "ORE GAUGE: HALF FULL."\n'
    "    line = line.lower()\n"
    "    line = line.capitalize()\n"
    "    return line\n"
)


def _reading(present="    pass\n", helper=READING_DEF, tail="\n\npresent_reading()\n"):
    return (
        "# get_reading() is finished.\n"
        "# Leave it as it is.\n"
        + helper +
        "\n\n"
        "# Finish present_reading():\n"
        "# 1. Store the result of\n"
        "#    get_reading() in a variable.\n"
        "# 2. Pass that variable to\n"
        "#    show_on_ley_board().\n"
        "def present_reading():\n"
        + present + tail
    )


RD_STORE = "    reading = get_reading()\n"
RD_PASS = "    show_on_ley_board(reading)\n"
READING_STARTER = _reading()
READING_SOLUTION = _reading(RD_STORE + RD_PASS)
_RD = dict(helper="get_reading", fn="present_reading")

PRESENT_READING = dict(
    id="present-reading",
    title="Store, then pass it on",
    martu=(
        "`get_reading()` hands back a tidy line from Gearshift's ore gauge. `present_reading()` must put that line on "
        "the Ley board.\n"
        "Campaign style: the numbered comments say what to do. My check calls `present_reading()` with other words, "
        "only inside the check.\n" + _STUCK
    ),
    setup=BOARD_SETUP,
    names=["get_reading", "present_reading", "show_on_ley_board"],
    support="none",
    explainer="lean",
    starter=READING_STARTER,
    checkpoints=[
        dict(
            id="store-the-reading",
            text="Finish `present_reading()`: store the result of `get_reading()` in a variable.",
            dictated=False,
            hints=[
                "Look at comment 1, inside `present_reading()`, where `pass` is.",
                "A variable can hold what a function hands back, if the function is called.",
                "Any variable name works. The call needs its brackets.",
            ],
            checks=[check("the reading is stored in a variable", _STORE, orig=READING_DEF, **_RD)],
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
            checks=[check("present_reading shows the line on the board", _PASS_ON,
                          swap="A grumpy moth reads the gauge.", **_RD)],
            pass_line="Gearshift: Half full. Visor dims. Logged.",
        ),
    ],
    solution=READING_SOLUTION,
    partials=[_reading(RD_STORE)],
    wrong_answers=[
        dict(why="the starter (pass)", code=READING_STARTER, fails_at=1, message_contains="only `pass`"),
        dict(why="no store: the call passed straight on (STO: the board shows the line, so that is said first)",
             code=_reading("    show_on_ley_board(get_reading())\n"), fails_at=1,
             message_contains="Your line runs, and the board shows the line. But `show_on_ley_board()` does not get"),
        dict(why="no store, and the line handed straight on twice (the board does not show it once)",
             code=_reading("    show_on_ley_board(get_reading())\n    show_on_ley_board(get_reading())\n"),
             fails_at=1, message_contains="straight to the board"),
        dict(why="no () on the helper: the function stored, not its line",
             code=_reading("    reading = get_reading\n" + RD_PASS), fails_at=1, message_contains="nothing calls it"),
        dict(why="a typed line stored instead of the result (CMB)",
             code=_reading('    reading = "Ore gauge: half full."\n' + RD_PASS), fails_at=1,
             message_contains="typed words"),
        dict(why="stored, then typed words passed to the board (CMB: the swap shows it)",
             code=_reading(RD_STORE + '    show_on_ley_board("Ore gauge: half full.")\n'), fails_at=2,
             message_contains="still showed the old ones"),
        dict(why="print instead of handing it to the board", code=_reading(RD_STORE + "    print(reading)\n"),
             fails_at=2, message_contains="nothing reached the board"),
        dict(why="stored, then returned (the line goes back to the caller)",
             code=_reading(RD_STORE + "    return reading\n"), fails_at=2,
             message_contains="The function returns the line, so it goes back to the caller and never reaches the "
                              "ley board."),
        dict(why="the helper's line returned straight away, never stored or shown",
             code=_reading("    return get_reading()\n"), fails_at=1,
             message_contains="No variable inside `present_reading()` holds the result"),
        dict(why="stored, then nothing done with it", code=_reading(RD_STORE), fails_at=2,
             message_contains="put nothing on the board"),
        dict(why="stored at the left edge, outside the function",
             code=_reading("    pass\n", tail="\n\nreading = get_reading()\nshow_on_ley_board(reading)\n"
                                              "present_reading()\n"),
             fails_at=1, message_contains="outside `present_reading()`"),
        dict(why="the store line reversed (cannot assign to a call)",
             code=_reading("    get_reading() = reading\n" + RD_PASS), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="the finished helper edited (a helper you were told to leave alone)",
             code=_reading(RD_STORE + RD_PASS, helper=READING_DEF.replace("    line = line.lower()\n", "")),
             fails_at=1, message_contains="marked finished"),
        dict(why="the variable called like a function: reading()",
             code=_reading(RD_STORE + "    show_on_ley_board(reading())\n"), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="the pass-on line at the left edge (a missing indent: reading is not defined there)",
             code=_reading(RD_STORE, tail="show_on_ley_board(reading)\n\n\npresent_reading()\n"), fails_at=0,
             message_contains="name 'reading' is not defined"),
        dict(why="stored, then a second call handed over instead of the variable",
             code=_reading(RD_STORE + "    show_on_ley_board(get_reading())\n"), fails_at=2,
             message_contains="Your line runs, and the board shows the line. But the board was handed a new call"),
        dict(why="stored, then a variable made at the left edge handed over (CMB: the swap shows it)",
             code=_reading(RD_STORE + "    show_on_ley_board(line)\n",
                           tail="\n\nline = get_reading()\npresent_reading()\n"), fails_at=2,
             message_contains="still showed the old ones"),
        dict(why="the last line left without () (calling vs naming): the board stays empty in the student's own run",
             code=_reading(RD_STORE + RD_PASS, tail="\n\npresent_reading\n"), fails_at=2,
             message_contains="no brackets after it"),
        dict(why="the variable's name in quotes handed to the board (KEY)",
             code=_reading(RD_STORE + '    show_on_ley_board("reading")\n'), fails_at=2,
             message_contains="a variable's name in quotes"),
        dict(why="= for a call: the line put into a new variable named show_on_ley_board",
             code=_reading(RD_STORE + "    show_on_ley_board = reading\n"), fails_at=2,
             message_contains="makes a new variable called `show_on_ley_board`"),
        dict(why="the board handed the function itself (no () when passing)",
             code=_reading(RD_STORE + "    show_on_ley_board(get_reading)\n"), fails_at=2,
             message_contains="the function `get_reading` itself"),
    ],
    notes=_rc(3, "b", "chain-methods,store-then-pass", "store-then-pass", "program-dialogue-prompt,mana-bars",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C2, item 3b (form A: get_warning / present_warning; form B: get_farewell / present_farewell). Item 3a "
    "(chain-methods) is quiz Q2, with other words, so running this task first gives nothing away there. CP1 STO + "
    "KEEP: the finished `get_reading` is unchanged (AST compare), and a variable inside `present_reading` holds the "
    "result of a call to it (no store, no `()`, a typed line, the store at the left edge and `pass` left are each "
    "named). CP2 CALL + CMB: the check calls `present_reading()` and reads the board recorder (setup), then swaps "
    "`get_reading` for one that returns 'A grumpy moth reads the gauge.': the board must follow, and the call must "
    "hand over the stored variable (a copy of it, or the variable inside a call, counts). The STO messages use form "
    "A's wording when the board does show the line ('Your line runs, and the board shows the line. But ...'; CP1 "
    "runs the function once, privately, to know). Stored then returned has form A's own message ('The function "
    "returns the line, so it goes back to the caller and never reaches the ley board.'), apart from 'put nothing "
    "on the board'. A last line with no brackets (`present_reading`) is named (form B's _uncalled). Fails on "
    "(spec): a typed line -> CMB; no store -> STO; no `()` -> CALL. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C3 (item 5b) mend the reply: quote-text in an elif chain (5a, the trace, is quiz Q5). CMB over every option.
# ---------------------------------------------------------------------------------------------

REPLIES = [
    ("option 1", "Oogrish: We rest here."),
    ("option 2", "Gearshift: Ore is low."),
    ("option 3", "Bomb Shell: Got it."),
    ("option 4", "Lucky: What's in it?"),
    ("option 5", "Mar'tu: Pick one."),
]


def _replies(line9="elif choice == option 4:", body10="    print(\"Lucky: What's in it?\")",
             line7='elif choice == "option 3":', fallback=True):
    return (
        'choice = "option 4"\n'
        "\n"
        'if choice == "option 1":\n'
        '    print("Oogrish: We rest here.")\n'
        'elif choice == "option 2":\n'
        '    print("Gearshift: Ore is low.")\n'
        f"{line7}\n"
        '    print("Bomb Shell: Got it.")\n'
        f"{line9}\n"
        f"{body10}\n"
        + ("else:\n    print(\"Mar'tu: Pick one.\")\n" if fallback else "")
    )


REPLY_STARTER = _replies()
REPLY_SOLUTION = _replies('elif choice == "option 4":')

MEND_THE_REPLY = dict(
    id="mend-the-reply",
    title="Mend the reply",
    martu=(
        "Four options, four replies, and one more for anything else, like the campaign's dialogue boxes. Python stops "
        "before anyone speaks.\n"
        "My check tries every option, and one more, only inside the check.\n" + _STUCK
    ),
    names=["choice"],
    support="none",
    explainer="lean",
    starter=REPLY_STARTER,
    checkpoints=[
        dict(
            id="mend-line-9",
            text="Mend line 9, so each option gets its own reply.",
            dictated=False,
            hints=[
                "Run it, and read the last line of what Python says. It names line 9.",
                "Compare line 9 with the lines above it, mark by mark.",
                "Line 9 compares `choice` with something. What kind of value is `choice`?",
            ],
            checks=[check("each option gets its own reply", _REPLY, runs=REPLIES, order=[3, 0, 1, 2, 4])],
            pass_line="Lucky: Option 4. Fine, I'm listening.",
        ),
    ],
    solution=REPLY_SOLUTION,
    wrong_answers=[
        dict(why="the starter: unquoted text after == (SyntaxError)", code=REPLY_STARTER, fails_at=0,
             message_contains="invalid syntax"),
        dict(why="= for == on line 9", code=_replies('elif choice = "option 4":'), fails_at=0,
             message_contains="Maybe you meant '=='"),
        dict(why="a capital letter in the text (STREXACT)", code=_replies('elif choice == "Option 4":'), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="the space left out (STREXACT)", code=_replies('elif choice == "option4":'), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="a missing colon", code=_replies('elif choice == "option 4"'), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the test is only the text (always True: else never runs)", code=_replies('elif "option 4":'),
             fails_at=1, message_contains="Lucky's reply printed, not Mar'tu's"),
        dict(why="a name for the text: option_4 (NameError)", code=_replies("elif choice == option_4:"), fails_at=0,
             message_contains="name 'option_4' is not defined"),
        dict(why="if for elif on line 9 (two replies for option 1)", code=_replies('if choice == "option 4":'),
             fails_at=1, message_contains="2 replies printed"),
        dict(why="the chain replaced by one typed print (CMB)",
             code='choice = "option 4"\n\nprint("Lucky: What\'s in it?")\n', fails_at=1,
             message_contains="Lucky's reply printed, not Oogrish's"),
        dict(why="the reply under line 9 not indented (IndentationError)",
             code=_replies('elif choice == "option 4":', body10="print(\"Lucky: What's in it?\")"), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="lines 9 and 10 deleted to stop the error (option 4 falls to else)",
             code=_replies(line9="", body10="").replace("\n\n\nelse", "\nelse").replace(
                 '    print("Bomb Shell: Got it.")\n\n\n', '    print("Bomb Shell: Got it.")\n'),
             fails_at=1, message_contains="Mar'tu's reply printed, not Lucky's"),
        dict(why="option 4 deleted to stop the error (its reply goes with the chain's else)",
             code=_replies('else:', body10="    print(\"Lucky: What's in it?\")", fallback=False), fails_at=1,
             message_contains="Lucky's reply printed, not Mar'tu's"),
    ],
    notes=_rc(5, "b", "elif-chain,quote-text", "quote-text,elif-chain", "program-dialogue-options",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C3, item 5b (form A mends `option 3`, form B `option 2`; form C mends the spec's `option 4`, on the last elif). "
    "The starter is the campaign's four-option shape, plus an `else` fallback, with one bare text. CMB: the check "
    "reruns the program with `choice` set to each option (option 4 first) and to \"option 5\", which only `else` "
    "answers; exactly that reply must print, alone. The fallback is what catches a test that is only the text "
    "(always True) on the last elif. STREXACT: a compared text that differs from an option only in capitals or "
    "spaces is named. A reply counts by its speaker (the words before the colon), so a reply the student rewords "
    "still counts. Fails on (spec): left unquoted -> crash (the explainer's 'two bare words after ==' row). "
    + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C4 (items 6a-6c) read and write the sheets: Gearshift's fuel sheet. dict-read, dict-nested, dict-write,
# dict-key-from-variable. Item 6d (dict-in) is quiz Q6. CMB and KEY.
# ---------------------------------------------------------------------------------------------

FUEL_SHEET = (
    "gearshift = {\n"
    '    "name": "Gearshift",\n'
    '    "mana": 14,\n'
    '    "max_mana": 20,\n'
    '    "fuel": {\n'
    '        "ore": 9,\n'
    '        "max_ore": 15,\n'
    "    },\n"
    "}\n"
)


def _fuel(mana="mana_now = 0", ore="ore_now = 0", store="", book='book = {"Flicker": {"mana_cost": 1}}'):
    return (
        FUEL_SHEET + "\n"
        "# 1. Make mana_now hold Gearshift's\n"
        "#    mana, read from the sheet.\n"
        + mana + "\n"
        "\n"
        "# 2. Make ore_now hold Gearshift's\n"
        "#    ore, read from the sheet.\n"
        + ore + "\n"
        "\n"
        + book + "\n"
        'charm_name = "Fire Coil"\n'
        'charm = {"mana_cost": 5}\n'
        "# 3. Store charm in book, using\n"
        "#    charm_name as the key.\n"
        + store + "\n"
        "\n"
        "print(mana_now, ore_now)\n"
        "print(book)\n"
    )


MANA_READ = 'mana_now = gearshift["mana"]'
ORE_READ = 'ore_now = gearshift["fuel"]["ore"]'
BOOK_WRITE = "book[charm_name] = charm"
FUEL_STARTER = _fuel()
FUEL_SOLUTION = _fuel(MANA_READ, ORE_READ, BOOK_WRITE)
KNOBBLE_SHEET = {"name": "Knobble", "mana": 5, "max_mana": 12, "fuel": {"ore": 3, "max_ore": 8}}
_OTHER_FUEL = [("gearshift", "gearshift = " + repr(KNOBBLE_SHEET))]
_FUEL_SAID = "another sheet in `gearshift` (Knobble: 5 of 12 mana, 3 of 8 ore)"
_FUEL_WHAT = "put another sheet in `gearshift`"
_CHARM_RERUNS = [([("charm_name", 'charm_name = "Moss Knot"'), ("charm", 'charm = {"mana_cost": 8}')], 8,
                  '`charm_name = "Moss Knot"` and `charm = {"mana_cost": 8}`',
                  "set `charm_name` and `charm` to other values")]

READ_THE_FUEL_SHEET = dict(
    id="read-the-fuel-sheet",
    title="Read and write the sheets",
    martu=(
        "Gearshift's fuel sheet is a [[dictionary]], with a [[nested dictionary]] inside it. Read two values from it, "
        "then write one page into a book of charms.\n"
        "My check puts other sheets and other pages in, only inside the check.\n" + _STUCK
    ),
    names=["mana_now", "ore_now", "book", "charm_name", "charm"],
    support="none",
    explainer="lean",
    starter=FUEL_STARTER,
    checkpoints=[
        dict(
            id="read-the-mana",
            text="Make `mana_now` hold Gearshift's mana, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 1, and at the sheet's keys.",
                "Square brackets after a dictionary's name read the value under one key.",
                "The key is text, so it keeps its quotes.",
            ],
            checks=[check(
                "mana_now reads the mana from the sheet", _FOLLOW, target="mana_now", want=14, place=0, mult=[],
                rules=[(20, "`mana_now` holds 20, the sheet's `\"max_mana\"`."),
                       (9, "`mana_now` holds 9, Gearshift's ore.")],
                reruns=[(_OTHER_FUEL, 5, _FUEL_SAID, _FUEL_WHAT)],
            )],
        ),
        dict(
            id="read-the-ore",
            text="Make `ore_now` hold Gearshift's ore, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 2. Where on the sheet is `\"ore\"`?",
                "A dictionary inside a dictionary is read one key at a time, outer key first.",
                "Two pairs of square brackets in a row.",
            ],
            checks=[check(
                "ore_now reads the ore from inside the fuel", _FOLLOW, target="ore_now", want=9, place=0, mult=[],
                rules=[(15, "`ore_now` holds 15, the sheet's `\"max_ore\"`."),
                       (14, "`ore_now` holds 14, Gearshift's mana.")],
                reruns=[(_OTHER_FUEL, 3, _FUEL_SAID, _FUEL_WHAT)],
            )],
        ),
        dict(
            id="store-the-charm",
            text="Store `charm` in `book`, using `charm_name` as the key.",
            dictated=False,
            hints=[
                "Look at comment 3, under the three lines about the book.",
                "Square brackets on the left of `=` write a page into a dictionary.",
                QUOTES_RULE,
            ],
            checks=[check("the charm is stored under the name in charm_name", _STORE_BY_NAME, bk="book",
                          kv="charm_name", vv="charm", kept="Flicker", newkey="Moss Knot", oldkey="Fire Coil",
                          field="mana_cost",
                          page="page", reruns=_CHARM_RERUNS)],
            pass_line="Gearshift: Fire Coil. Logged. Math checks out.",
        ),
    ],
    solution=FUEL_SOLUTION,
    partials=[_fuel(MANA_READ), _fuel(MANA_READ, ORE_READ)],
    wrong_answers=[
        dict(why="the starter (0 placeholders)", code=FUEL_STARTER, fails_at=1, message_contains="still holds"),
        dict(why="CP1 a typed 14 (CMB)", code=_fuel("mana_now = 14"), fails_at=1,
             message_contains="`mana_now` holds a typed 14. Mar'tu's check put another sheet in `gearshift`, and "
                              "`mana_now` still said 14."),
        dict(why="CP1 max_mana read instead of mana", code=_fuel('mana_now = gearshift["max_mana"]'), fails_at=1,
             message_contains="max_mana"),
        dict(why="CP1 half typed: max_mana less a gap worked out by hand (CMB; Knobble's gap differs)",
             code=_fuel('mana_now = gearshift["max_mana"] - 6'), fails_at=1, message_contains="held `6`, not `5`"),
        dict(why="CP1 the key with a capital (KeyError)", code=_fuel('mana_now = gearshift["Mana"]'), fails_at=0,
             message_contains="KeyError: 'Mana'"),
        dict(why="CP1 the key without quotes (NameError)", code=_fuel("mana_now = gearshift[mana]"), fails_at=0,
             message_contains="name 'mana' is not defined"),
        dict(why="CP1 a dot for brackets (AttributeError)", code=_fuel("mana_now = gearshift.mana"), fails_at=0,
             message_contains="has no attribute 'mana'"),
        dict(why="CP1 the read in quotes (text)", code=_fuel("mana_now = 'gearshift[\"mana\"]'"), fails_at=1,
             message_contains="holds text"),
        dict(why="CP2 a skipped nesting level (KeyError)", code=_fuel(MANA_READ, 'ore_now = gearshift["ore"]'),
             fails_at=0, message_contains="KeyError: 'ore'"),
        dict(why="CP2 only the outer key: the whole fuel dictionary",
             code=_fuel(MANA_READ, 'ore_now = gearshift["fuel"]'), fails_at=2, message_contains="whole dictionary"),
        dict(why="CP2 a typed 9 (CMB)", code=_fuel(MANA_READ, "ore_now = 9"), fails_at=2,
             message_contains="`ore_now` holds a typed 9. Mar'tu's check put another sheet in `gearshift`"),
        dict(why="CP2 half typed: max_ore less a gap worked out by hand (CMB)",
             code=_fuel(MANA_READ, 'ore_now = gearshift["fuel"]["max_ore"] - 6'), fails_at=2,
             message_contains="held `2`, not `3`"),
        dict(why="CP2 the wrong inner key", code=_fuel(MANA_READ, 'ore_now = gearshift["fuel"]["max_ore"]'),
             fails_at=2, message_contains="max_ore"),
        dict(why="CP2 the keys in the wrong order (KeyError)", code=_fuel(MANA_READ, 'ore_now = gearshift["ore"]["fuel"]'),
             fails_at=0, message_contains="KeyError: 'ore'"),
        dict(why="CP3 the variable's name quoted as the key (KEY)",
             code=_fuel(MANA_READ, ORE_READ, 'book["charm_name"] = charm'), fails_at=3, message_contains='"charm_name"'),
        dict(why="CP3 a typed key (CMB: the rerun's name is not there)",
             code=_fuel(MANA_READ, ORE_READ, 'book["Fire Coil"] = charm'), fails_at=3,
             message_contains="The key is a typed `\"Fire Coil\"`. Mar'tu's check put another name in `charm_name`, "
                              "and the key still said `\"Fire Coil\"`."),
        dict(why="CP3 a typed key after the student chose another name (the name is not repeated back)",
             code=_fuel(MANA_READ, ORE_READ, 'book["Sun Wick"] = charm').replace('"Fire Coil"', '"Sun Wick"'),
             fails_at=3, message_contains="The key is a typed name. Mar'tu's check put another name in `charm_name`"),
        dict(why="CP3 the book rebuilt: the first page lost", code=_fuel(MANA_READ, ORE_READ,
                                                                      "book = {charm_name: charm}"),
             fails_at=3, message_contains="lost its Flicker page"),
        dict(why="CP3 key and value swapped (TypeError: a dict as a key)",
             code=_fuel(MANA_READ, ORE_READ, "book[charm] = charm_name"), fails_at=0,
             message_contains="unhashable type: 'dict'"),
        dict(why="CP3 == for = (the comparison reads a page that is not there)",
             code=_fuel(MANA_READ, ORE_READ, "book[charm_name] == charm"), fails_at=0,
             message_contains="KeyError: 'Fire Coil'"),
        dict(why="CP3 the variable's name in quotes as the value",
             code=_fuel(MANA_READ, ORE_READ, 'book[charm_name] = "charm"'), fails_at=3,
             message_contains="not the `charm` dictionary"),
        dict(why="CP3 a typed copy of the page (CMB: the rerun's page is not there)",
             code=_fuel(MANA_READ, ORE_READ, 'book[charm_name] = {"mana_cost": 5}'), fails_at=3,
             message_contains="did not hold the new `charm`"),
        dict(why="CP3 .append on a dictionary (AttributeError)", code=_fuel(MANA_READ, ORE_READ, "book.append(charm)"),
             fails_at=0, message_contains="has no attribute 'append'"),
    ],
    notes=_rc(6, "a-c", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable",
              "dict-read,dict-nested,dict-write,dict-key-from-variable", "spell-book,hold-the-barrier",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C4, items 6a-6c (form A: `hero[\"mana\"]`, `hero[\"abilities\"][\"wisdom\"]`, `book[spell_name] = spell`; form "
    "B: Bomb Shell's sheet, `book[ward_name] = ward`). Form C is the spec's Gearshift's fuel sheet: his real max mana "
    "(20), with 14 mana left and 9 of 15 starlode ore inside `\"fuel\"`, so `\"max_mana\"` read for the mana, or the "
    "ore read for the mana, shows in the student's own run. CP1 and CP2 CMB: the program reruns with Knobble's sheet "
    "slipped in after the student's `gearshift` line (5 of 12 mana, 3 of 8 ore; its gaps, 7 and 5, differ from "
    "Gearshift's 6 and 6, so a half-typed `gearshift[\"max_mana\"] - 6` cannot follow either): a typed number "
    "cannot follow. CP3 "
    "KEY + CMB: the page must be under the name `charm_name` holds, the Flicker page must stay, and a rerun with "
    "`charm_name = \"Moss Knot\"` and another `charm` must store that page. Fails on (spec): `gearshift[\"ore\"]` (the "
    "skipped level, KeyError); `book[\"charm_name\"]`. Typed values are named in form A's words ('`mana_now` holds "
    "a typed 14. Mar'tu's check put another sheet in `gearshift`, and `mana_now` still said 14.'; 'The key is a "
    "typed `\"Fire Coil\"`. ... and the key still said `\"Fire Coil\"`.'); a key the student chose is called "
    "'a typed name', never repeated back. Mar'tu says 'a book of charms' (the book holds charms). The Ready rule's "
    "'item 6 at >= 3 of 4 parts' counts CP1-CP3 here and Q6 (site scoring work). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C5 (item 7b) mend the gauge: repeat-string, the parentheses (7a is quiz Q7). CMB with other ore.
# ---------------------------------------------------------------------------------------------


def _gauge(empty='empty = "░" * max_ore - ore', full='full = "█" * ore'):
    return (
        "ore = 9\n"
        "max_ore = 15\n"
        "\n"
        f"{full}\n"
        f"{empty}\n"
        'print("Ore [" + full + empty + "]")\n'
    )


GAUGE_STARTER = _gauge()
GAUGE_SOLUTION = _gauge('empty = "░" * (max_ore - ore)')

_GAUGE_RUNS = [
    ((), 9, 15, "", ""),
    ([("ore", "ore = 3"), ("max_ore", "max_ore = 7")], 3, 7, "With `ore = 3` and `max_ore = 7`",
     "tried `ore = 3` and `max_ore = 7`"),
    ([("ore", "ore = 10"), ("max_ore", "max_ore = 12")], 10, 12, "With `ore = 10` and `max_ore = 12`",
     "tried `ore = 10` and `max_ore = 12`"),
]

MEND_THE_GAUGE = dict(
    id="mend-the-gauge",
    title="Mend the gauge",
    martu=(
        "Gearshift's ore gauge works like a mana bar: a `█` for each lump of ore left, a `░` for each one burned. The "
        "blocks are typed for you.\n"
        "Python stops on line 5. My check tries other ore, only inside the check.\n" + _STUCK
    ),
    names=["empty", "full", "ore", "max_ore"],
    support="none",
    explainer="lean",
    starter=GAUGE_STARTER,
    checkpoints=[
        dict(
            id="mend-line-5",
            text="Mend line 5, so `empty` holds one `░` for each lump of ore burned.",
            dictated=False,
            hints=[
                "Run it, and read the last line of what Python says.",
                "Python does `*` before `-`, so it works out the blocks first.",
                "Which part of line 5 should be worked out first?",
            ],
            checks=[check("empty holds a block for each lump burned", _BAR, runs=_GAUGE_RUNS)],
            pass_line="Gearshift: Ore left, ore burned. The gauge tells the truth.",
        ),
    ],
    solution=GAUGE_SOLUTION,
    wrong_answers=[
        dict(why="the starter: no parentheses (TypeError)", code=GAUGE_STARTER, fails_at=0,
             message_contains="unsupported operand type(s) for -: 'str' and 'int'"),
        dict(why="a typed count (CMB)", code=_gauge('empty = "░" * 6'), fails_at=1,
             message_contains="`empty` holds a typed 6 blocks. Mar'tu's check put 3 in `ore` and 7 in `max_ore`, and "
                              "`empty` still had 6 blocks, not 4."),
        dict(why="typed blocks (CMB)", code=_gauge('empty = "░░░░░░"'), fails_at=1,
             message_contains="`empty` holds a typed 6 blocks"),
        dict(why="the parentheses added, around typed numbers (CMB)", code=_gauge('empty = "░" * (15 - 9)'), fails_at=1,
             message_contains="`empty` holds a typed 6 blocks"),
        dict(why="a typed 15 for max_ore (CMB)", code=_gauge('empty = "░" * (15 - ore)'), fails_at=1,
             message_contains="Your `empty` line holds a typed 15. Mar'tu's check put 7 in `max_ore`, and `empty` "
                              "still had 15 minus `ore`: 12 blocks, not 4."),
        dict(why="a typed 9 for ore (CMB)", code=_gauge('empty = "░" * (max_ore - 9)'), fails_at=1,
             message_contains="Your `empty` line holds a typed 9. Mar'tu's check put 3 in `ore`, and `empty` still "
                              "had `max_ore` minus 9: 0 blocks, not 4."),
        dict(why="line 5 mended, then the blocks typed into the print line (CMB)",
             code=GAUGE_SOLUTION.replace('full + empty + "]"', 'full + "░░░░░░" + "]"'), fails_at=1,
             message_contains="only those blocks"),
        dict(why="only the max: the subtraction dropped", code=_gauge('empty = "░" * max_ore'), fails_at=1,
             message_contains="held 15 blocks"),
        dict(why="the subtraction reversed (no blocks)", code=_gauge('empty = "░" * (ore - max_ore)'), fails_at=1,
             message_contains="held 0 blocks"),
        dict(why="blocks minus blocks (TypeError)", code=_gauge('empty = "░" * max_ore - "░" * ore'), fails_at=0,
             message_contains="for -: 'str' and 'str'"),
        dict(why="brackets around the wrong part", code=_gauge('empty = ("░" * max_ore) - ore'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the sum in quotes (TypeError: text times text)", code=_gauge('empty = "░" * "max_ore - ore"'),
             fails_at=0, message_contains="can't multiply sequence"),
        dict(why="full typed as well (CMB)", code=_gauge('empty = "░" * (max_ore - ore)', full='full = "█████████"'),
             fails_at=1, message_contains="`full` did not hold 3"),
        dict(why="the wrong block for the burned ore", code=_gauge('empty = "█" * (max_ore - ore)'), fails_at=1,
             message_contains="other marks"),
    ],
    notes=_rc(7, "b", "repeat-string", "repeat-string", "mana-bars", starter_level="S4", path="READY", dictates="",
              foreign_names="") + "\n"
    "C5, item 7b (form A mends `\"░\" * 10 - 3`; form B `\"░\" * max_mana - mana`). Form C is Gearshift's ore gauge, "
    "the mana-bar shape with other names, so the mend can be rerun with other values: CMB with 3 of 7 and 10 of 12 "
    "ore, and `full` and the printed bar must follow. Fails on (spec): no parentheses -> the TypeError row (lean "
    "names the line). Typed counts and typed blocks fail the reruns, named as typed when the count stays the same; "
    "the printed bar must hold exactly `full`'s and `empty`'s blocks. Typed values are named in form A's words: "
    "'`empty` holds a typed 6 blocks. Mar'tu's check put 3 in `ore` and 7 in `max_ore`, and `empty` still had 6 "
    "blocks, not 4.', and a typed `max_ore` (`15 - ore`) or a typed `ore` (`max_ore - 9`) gets its own line. The "
    "student's own run follows the program's own `ore` and `max_ore` (_given), so changed numbers pass. "
    + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C6 (item 8b) toss the die: randint-param (8a, randint, is quiz Q8). RND.
# ---------------------------------------------------------------------------------------------


def _toss(body="    return 1\n", tail="\n\nprint(toss_die(20))\n", head="def toss_die(sides):\n"):
    return "import random\n\n\n" + head + body + tail


TOSS_STARTER = _toss()
TOSS_SOLUTION = _toss("    return random.randint(1, sides)\n")

TOSS_THE_DIE = dict(
    id="toss-the-die",
    title="Roll the die",
    martu=(
        "Campaign style: `toss_die(sides)` must roll a die with `sides` faces. Right now it always says 1.\n"
        "My check rolls other dice with a pretend die, only inside the check.\n" + _STUCK
    ),
    names=["toss_die", "sides"],
    support="none",
    explainer="lean",
    starter=TOSS_STARTER,
    checkpoints=[
        dict(
            id="roll-from-1-to-sides",
            text="Replace `return 1` with a random whole number from 1 to `sides`.",
            dictated=False,
            hints=[
                "Look at the `import` line at the top: it brings in the tools for random numbers.",
                "[[randint]] takes the lowest and the highest number, and both can come up.",
                "The highest face is whatever was handed in, so it is the parameter, not a number.",
            ],
            checks=[check("toss_die rolls from 1 to sides", _ROLL, fn="toss_die", param="sides", sizes=[6, 10])],
            pass_line="Lucky: Any die you like. I'll still say it was luck.",
        ),
    ],
    solution=TOSS_SOLUTION,
    wrong_answers=[
        dict(why="the starter (return 1)", code=TOSS_STARTER, fails_at=1, message_contains="rolled no die"),
        dict(why="a typed d20 (RND: the literal size)", code=_toss("    return random.randint(1, 20)\n"), fails_at=1,
             message_contains="typed number"),
        dict(why="a typed d6 (it passes the d6, not the d10)", code=_toss("    return random.randint(1, 6)\n"),
             fails_at=1, message_contains="typed number"),
        dict(why="the exclusive-range belief: sides + 1", code=_toss("    return random.randint(1, sides + 1)\n"),
             fails_at=1, message_contains="one face too many"),
        dict(why="from 0", code=_toss("    return random.randint(0, sides)\n"), fails_at=1,
             message_contains="no 0 face"),
        dict(why="print instead of return", code=_toss("    print(random.randint(1, sides))\n"), fails_at=1,
             message_contains="printed the roll and returned `None`, Python's word for nothing."),
        dict(why="rolled, but no return", code=_toss("    random.randint(1, sides)\n"), fails_at=1,
             message_contains="rolled, then returned `None`, Python's word for nothing."),
        dict(why="sides set inside (the parameter thrown away)",
             code=_toss("    sides = 20\n    return random.randint(1, sides)\n"), fails_at=1,
             message_contains="sets `sides`"),
        dict(why="the size returned with no roll", code=_toss("    return sides\n"), fails_at=1,
             message_contains="rolled no die"),
        dict(why="no brackets after randint: the function handed back, not called", code=_toss("    return random.randint\n"),
             fails_at=1, message_contains="returned the function `randint`"),
        dict(why="the roll stored, then its name returned in quotes (KEY)",
             code=_toss('    roll = random.randint(1, sides)\n    return "roll"\n'), fails_at=1,
             message_contains="a variable's name in quotes"),
        dict(why="from random import randint, with a typed d20 (RND still sees the bare randint)",
             code="from random import randint\n\n\ndef toss_die(sides):\n    return randint(1, 20)\n\n\nprint(toss_die(20))\n",
             fails_at=1, message_contains="typed number"),
        dict(why="the function printed, not called (handing over vs calling: no (20))",
             code=TOSS_SOLUTION.replace("print(toss_die(20))", "print(toss_die)"), fails_at=1,
             message_contains="prints the function `toss_die` itself: nothing calls it"),
        dict(why="randint with one value (TypeError)", code=_toss("    return random.randint(sides)\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="randint without random. (NameError)", code=_toss("    return randint(1, sides)\n"), fails_at=0,
             message_contains="name 'randint' is not defined"),
        dict(why="the parameter in quotes", code=_toss('    return random.randint(1, "sides")\n'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="an approximate parameter name: the campaign's die_size (NameError)",
             code=_toss("    return random.randint(1, die_size)\n"), fails_at=0,
             message_contains="name 'die_size' is not defined"),
        dict(why="the parameter renamed on the def line, the call removed (the check names it)",
             code=_toss("    return random.randint(1, die_size)\n", tail="\n", head="def toss_die(die_size):\n"),
             fails_at=1, message_contains="the starter has `sides`"),
    ],
    notes=_rc(8, "b", "randint,randint-param", "randint-param", "skill-checks", starter_level="S4", path="READY",
              dictates="", foreign_names="") + "\n"
    "C6, item 8b (form A: `roll_die(die_size)`; form B: `throw_die(die_size)`). Form C's parameter is `sides`, so the "
    "campaign's `die_size` typed from memory is an approximate parameter name (NameError). Item 8a (randint, a d12) "
    "is quiz Q8. Campaign-style starter (`perform_roll`'s `return 1`). RND: the check swaps `random.randint` for a "
    "scripted die that records its arguments and rolls one below the top face, then calls `toss_die(6)` and "
    "`toss_die(10)`: one roll, from 1 to the size handed in, and that roll returned. The visible call is "
    "`toss_die(20)`, so 6 and 10 are fresh. Fails on (spec): `randint(1, 6)` -> RND (the d6 passes, the d10 does "
    "not); also the typed 20, `sides + 1` (the exclusive-range belief), 0, print for return, and a line that sets "
    "`sides` inside. `None` is named as Python's word for nothing (form A's words), and `print(toss_die)` is named "
    "(form B's _uncalled). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C7 (item 11) three tracebacks: read-traceback. Each slip in its own function; CALL + CMB with fresh values.
# ---------------------------------------------------------------------------------------------

TB_ORE_BAD = 'def ore_in(sheet):\n    return sheet["ore"]\n'
TB_ORE_GOOD = 'def ore_in(sheet):\n    return sheet["fuel"]["ore"]\n'
TB_LABEL_BAD = 'def gauge_label(ore):\n    return "Gauge: " + ore\n'
TB_LABEL_GOOD = 'def gauge_label(ore):\n    return "Gauge: " + str(ore)\n'
TB_USED_HEAD = "def ore_used(legs):\n    used = 0\n    for leg in legs:\n"
TB_USED_BAD = TB_USED_HEAD + "        used = used + legg\n    return used\n"
TB_USED_GOOD = TB_USED_HEAD + "        used = used + leg\n    return used\n"
TB_CALLS = (
    'gear = {"fuel": {"ore": 9}}\n'
    "print(ore_in(gear))\n"
    "print(gauge_label(9))\n"
    "print(ore_used([2, 4, 1]))\n"
)


def _tb(ore=TB_ORE_BAD, label=TB_LABEL_BAD, used=TB_USED_BAD, calls=TB_CALLS):
    return ore + "\n\n" + label + "\n\n" + used + "\n\n" + calls


TB_STARTER = _tb()
TB_SOLUTION = _tb(TB_ORE_GOOD, TB_LABEL_GOOD, TB_USED_GOOD)

_TB_ORE = r'''
_f, _m = _find('ore_in')
assert _f, _m
for _s in ({'fuel': {'ore': 4, 'max_ore': 9}}, {'fuel': {'ore': 12, 'max_ore': 15}}):
    _o = _s['fuel']['ore']
    _c = '`ore_in` on a sheet with ' + str(_o) + ' ore'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (_s,))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    assert _val == _o, '`ore_in` returned ' + _show(_val) + ' for a sheet with ' + str(_o) + ' ore.' + _ev(_what)
'''

_TB_LABEL = r'''
_f, _m = _find('gauge_label')
assert _f, _m
for _ore in (30, 7):
    _c = '`gauge_label(' + str(_ore) + ')`'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (_ore,))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    if _val != 'Gauge: ' + str(_ore):
        assert not (_val is None and _rows), (_c + " printed a label and returned `None`, Python's word for "
                                              'nothing.' + _ev(_what))
        _bare = ('Gauge: ' + str(_ore)).replace(' ', '')
        assert not (type(_val).__name__ == 'str' and _val.replace(' ', '') == _bare), (
            _c + ' returned a label that differs from `Gauge: ' + str(_ore) + '` only in its spaces.' + _ev(_what))
        assert False, _c + ' returned ' + _show(_val) + ', not the label for ' + str(_ore) + ' ore.' + _ev(_what)
'''

_TB_USED = r'''
_f, _m = _find('ore_used')
assert _f, _m
for _legs, _want in (([6, 1, 4, 2], 13), ([9], 9)):
    _c = '`ore_used(' + str(_legs) + ')`'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (list(_legs),))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    if _val != _want:
        assert not (_val is None and _rows), (_c + " printed a number and returned `None`, Python's word for "
                                              'nothing.' + _ev(_what))
        assert not (len(_legs) > 1 and _val == _legs[-1]), (
            _c + ' returned ' + _show(_val) + ', only the last leg: the sum starts again on every pass.' + _ev(_what))
        assert not (len(_legs) > 1 and _val == _legs[0]), (
            _c + ' returned ' + _show(_val) + ', only the first leg: the function hands back on the first pass.'
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
    names=["ore_in", "gauge_label", "ore_used"],
    support="none",
    explainer="lean",
    starter=TB_STARTER,
    checkpoints=[
        dict(
            id="first-traceback",
            text="Run it, then mend the line Python names, so `ore_in` returns a sheet's ore.",
            dictated=False,
            hints=[
                "Read the last line of the message first: the kind of error, then what it says.",
                "Then find the line it names, inside one of the functions.",
                "Mend that one line, not the data or the call below it.",
            ],
            checks=[check("ore_in returns the sheet's ore", _TB_ORE)],
            pass_line="Mar'tu: One mended. Python got further, yes?",
        ),
        dict(
            id="second-traceback",
            text="Run again, then mend the next line Python names, so `gauge_label` returns a label like `Gauge: 9`.",
            dictated=False,
            hints=[
                "Read the new last line. It is a different kind of error now.",
                "It names a line inside another function.",
                "Mend the line itself, so any number handed in works.",
            ],
            checks=[check("gauge_label returns the label", _TB_LABEL)],
        ),
        dict(
            id="third-traceback",
            text="Run again, then mend the last line Python names, so `ore_used` returns the ore of every leg, added up.",
            dictated=False,
            hints=[
                "Read the last line once more. Python may suggest a name.",
                "Python matches names letter for letter.",
                "Mend that line so the loop adds each leg.",
            ],
            checks=[check("ore_used returns every leg added up", _TB_USED)],
            pass_line="Mar'tu: Three tracebacks, three mends, and no hints. You read them yourself.",
        ),
    ],
    solution=TB_SOLUTION,
    wrong_answers=[
        dict(why="the starter: the first traceback (KeyError: the skipped level)", code=TB_STARTER, fails_at=0,
             message_contains="KeyError: 'ore'"),
        dict(why="only the first slip mended: the second traceback (TypeError)", code=_tb(TB_ORE_GOOD), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="two slips mended: the third traceback (NameError)", code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD), fails_at=0,
             message_contains="name 'legg' is not defined"),
        dict(why="CP1 the data mended, not the line (the ore moved out of fuel in gear)",
             code=_tb(TB_ORE_BAD, TB_LABEL_GOOD, TB_USED_GOOD, TB_CALLS.replace('{"fuel": {"ore": 9}}', '{"ore": 9}')),
             fails_at=1, message_contains="KeyError: 'ore'"),
        dict(why="CP1 a typed 9 (CMB)", code=_tb('def ore_in(sheet):\n    return 9\n', TB_LABEL_GOOD, TB_USED_GOOD),
             fails_at=1, message_contains="returned `9`"),
        dict(why="CP1 the global gear read inside, not the sheet handed in (CMB)",
             code=_tb('def ore_in(sheet):\n    return gear["fuel"]["ore"]\n', TB_LABEL_GOOD, TB_USED_GOOD), fails_at=1,
             message_contains="returned `9` for a sheet with 4 ore"),
        dict(why="CP1 only the outer key (the whole fuel dictionary)",
             code=_tb('def ore_in(sheet):\n    return sheet["fuel"]\n', TB_LABEL_GOOD, TB_USED_GOOD), fails_at=1,
             message_contains="returned a dictionary"),
        dict(why="CP2 the call mended, not the line: the ore handed over as text",
             code=_tb(TB_ORE_GOOD, TB_LABEL_BAD, TB_USED_GOOD, TB_CALLS.replace("gauge_label(9)", 'gauge_label("9")')),
             fails_at=2, message_contains="can only concatenate str"),
        dict(why="CP2 a typed label (CMB)", code=_tb(TB_ORE_GOOD, 'def gauge_label(ore):\n    return "Gauge: 9"\n',
                                                     TB_USED_GOOD), fails_at=2, message_contains="not the label for 30"),
        dict(why="CP2 str() around a typed number",
             code=_tb(TB_ORE_GOOD, 'def gauge_label(ore):\n    return "Gauge: " + str(9)\n', TB_USED_GOOD), fails_at=2,
             message_contains="not the label for 30"),
        dict(why="CP2 str() around the whole sum, not the number (str() before +)",
             code=_tb(TB_ORE_GOOD, 'def gauge_label(ore):\n    return str("Gauge: " + ore)\n', TB_USED_GOOD), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="CP2 the space after the colon dropped",
             code=_tb(TB_ORE_GOOD, 'def gauge_label(ore):\n    return "Gauge:" + str(ore)\n', TB_USED_GOOD), fails_at=2,
             message_contains="only in its spaces"),
        dict(why="CP2 print instead of return",
             code=_tb(TB_ORE_GOOD, 'def gauge_label(ore):\n    print("Gauge: " + str(ore))\n', TB_USED_GOOD),
             fails_at=2, message_contains="printed a label and returned `None`, Python's word for nothing."),
        dict(why="CP3 the sum reset inside the loop (resetting a total inside a loop)",
             code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD, (
                 "def ore_used(legs):\n    for leg in legs:\n        used = 0\n        used = used + leg\n"
                 "    return used\n")), fails_at=3, message_contains="starts again on every pass"),
        dict(why="CP3 return indented into the loop (a missing outdent: it hands back on the first pass)",
             code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD, TB_USED_HEAD + "        used = used + leg\n        return used\n"),
             fails_at=3, message_contains="only the first leg"),
        dict(why="CP3 a typed 7 (CMB)", code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD,
                                                 TB_USED_HEAD + "        used = used + leg\n    return 7\n"),
             fails_at=3, message_contains="returned `7`"),
        dict(why="CP3 print instead of return", code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD,
                                                         TB_USED_HEAD + "        used = used + leg\n    print(used)\n"),
             fails_at=3, message_contains="printed a number and returned `None`, Python's word for nothing."),
        dict(why="CP3 the list added, not the leg (TypeError)",
             code=_tb(TB_ORE_GOOD, TB_LABEL_GOOD, TB_USED_HEAD + "        used = used + legs\n    return used\n"),
             fails_at=0, message_contains="unsupported operand type(s) for +: 'int' and 'list'"),
        dict(why="the calls deleted to stop the tracebacks (the slips are still there)",
             code=_tb(calls=""), fails_at=1, message_contains="KeyError: 'ore'"),
    ],
    notes=_rc(11, "code", "read-traceback", "read-traceback", "every part", starter_level="S4", path="READY",
              dictates="", foreign_names="") + "\n"
    "C7, item 11 (form A: KeyError 'dexterity', the str + int TypeError, NameError 'mana_cots'; form B: KeyError "
    "'Mana', TypeError, NameError 'totl'). Form C: KeyError 'ore' (a skipped nesting level, the class's sheet slip), "
    "the same TypeError in a returned label, and NameError 'legg' (the loop variable mistyped). Each slip sits in its "
    "own small function with the calls at the bottom, so every traceback is live, in order, and each checkpoint "
    "calls its function with fresh values (CALL + CMB): a typed 9, a typed label, a typed 7, the data or the call "
    "mended instead of the line, and the calls deleted each fail. CP3's loop also catches the reset slip (`used = 0` "
    "moved into the loop). No partials: Python stops at the first slip left, so a program with one slip mended still "
    "crashes at the next, before any check can run. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C8 (item 12) spend the mana: dict-write, reassign, combine-values. CMB with another cost and start.
# ---------------------------------------------------------------------------------------------

SPEND_HEAD = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    "}\n"
    "cost = 6\n"
    "\n"
    '# Spend cost from lucky["mana"].\n'
)


def _spend(line=""):
    return SPEND_HEAD + line + "\n\nprint(lucky[\"mana\"])\n"


SPEND_STARTER = _spend()
SPEND_SOLUTION = _spend('lucky["mana"] = lucky["mana"] - cost\n')

# (changes, the mana wanted, said, what the check did, whose sheet, its mana, the cost)
_SPEND_RERUNS = [
    ([("lucky", 'lucky = {"name": "Knobble", "mana": 15}'), ("cost", "cost = 4")], 11,
     "Knobble's sheet (15 mana) and `cost = 4`", "put Knobble's sheet in `lucky` and tried `cost = 4`",
     "Knobble", 15, 4),
    ([("lucky", 'lucky = {"name": "Thorn", "mana": 9}'), ("cost", "cost = 9")], 0,
     "Thorn's sheet (9 mana) and `cost = 9`", "put Thorn's sheet in `lucky` and tried `cost = 9`",
     "Thorn", 9, 9),
]

SPEND_THE_MANA = dict(
    id="spend-the-mana",
    title="Spend the mana",
    martu=(
        "Lucky casts, for once. The spell costs `cost`, and it comes out of his sheet.\n"
        "My check tries another sheet and another cost, only inside the check.\n" + _STUCK
    ),
    names=["lucky", "cost"],
    support="none",
    explainer="lean",
    starter=SPEND_STARTER,
    checkpoints=[
        dict(
            id="spend-the-cost",
            text="Spend `cost` from `lucky[\"mana\"]`.",
            dictated=False,
            hints=[
                "Look at the comment: one line goes under it.",
                "The new mana is worked out from the old mana and the cost, then stored back.",
                "Read the old value on the right of `=`, and store the new one on the left.",
            ],
            checks=[check("lucky's mana goes down by cost", _SPEND, sv="lucky", start=26, want=20,
                          reruns=_SPEND_RERUNS)],
            pass_line="Lucky: Spent. And yes, I'm keeping track.",
        ),
    ],
    solution=SPEND_SOLUTION,
    wrong_answers=[
        dict(why="the starter (nothing spent)", code=SPEND_STARTER, fails_at=1, message_contains="still 26"),
        dict(why="a typed 20 (CMB)", code=_spend('lucky["mana"] = 20\n'), fails_at=1,
             message_contains="`lucky[\"mana\"]` holds a typed 20. Mar'tu's check put Knobble's sheet in `lucky` and "
                              "tried `cost = 4`, and `lucky[\"mana\"]` still said 20."),
        dict(why="the subtraction with no store", code=_spend('lucky["mana"] - cost\n'), fails_at=1,
             message_contains="worked out, then forgotten"),
        dict(why="a typed cost (CMB)", code=_spend('lucky["mana"] = lucky["mana"] - 6\n'), fails_at=1,
             message_contains="The line takes away a typed 6, not what `cost` holds. Mar'tu's check put 4 in `cost`, "
                              "and the line still took away 6: Knobble's mana ended at 9."),
        dict(why="the new mana in a new variable (NEWBOX)", code=_spend('mana = lucky["mana"] - cost\n'), fails_at=1,
             message_contains="went into `mana`"),
        dict(why="the subtraction reversed", code=_spend('lucky["mana"] = cost - lucky["mana"]\n'), fails_at=1,
             message_contains="`-20`"),
        dict(why="== for = (a comparison, nothing stored)", code=_spend('lucky["mana"] == lucky["mana"] - cost\n'),
             fails_at=1, message_contains="compares"),
        dict(why="printed, not stored", code=_spend('print(lucky["mana"] - cost)\n'), fails_at=1,
             message_contains="printed, not stored"),
        dict(why="a capital key: the new value under another key (KEY)",
             code=_spend('lucky["Mana"] = lucky["mana"] - cost\n'), fails_at=1, message_contains="another key"),
        dict(why="the cost overwritten", code=_spend('cost = lucky["mana"] - cost\n'), fails_at=1,
             message_contains="went into `cost`"),
        dict(why="the sheet replaced by a number (TypeError at the print)",
             code=_spend('lucky = lucky["mana"] - cost\n'), fails_at=0, message_contains="not subscriptable"),
        dict(why="a typed start (CMB)", code=_spend('lucky["mana"] = 26 - cost\n'), fails_at=1,
             message_contains="The line starts from a typed 26, not from `lucky[\"mana\"]`. Mar'tu's check put "
                              "Knobble's sheet in `lucky`, mana 15, and the line still started from 26: Knobble's "
                              "mana ended at 22."),
        dict(why="a typed number after the student changed the cost (CMB: the reruns still catch it)",
             code=_spend('lucky["mana"] = 21\n').replace("cost = 6", "cost = 5"), fails_at=1,
             message_contains="`lucky[\"mana\"]` holds a typed 21"),
        dict(why="a typed cost after the student changed the cost (the typed 5 is named)",
             code=_spend('lucky["mana"] = lucky["mana"] - 5\n').replace("cost = 6", "cost = 5"), fails_at=1,
             message_contains="The line takes away a typed 5, not what `cost` holds"),
    ],
    notes=_rc(12, "code", "dict-write,reassign,combine-values", "dict-write,reassign,combine-values",
              "hold-the-barrier", starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C8, item 12 (form A: `hero[\"mana\"]` and `cost`; form B: `oogrish[\"mana\"]`). Typed (G2 R17). Lucky's real "
    "max mana (26), cost 6. CMB: the program reruns with Knobble's sheet (15 mana, cost 4: 11) and Thorn's (9 mana, "
    "cost 9: exactly 0) slipped in after the student's own lines, so the typed 20, a typed cost and a typed start "
    "fail. Fails on (spec): `lucky[\"mana\"] = 20` -> CMB; the subtraction with no store. Also the new mana in a new "
    "variable (NEWBOX), `==` for `=`, printed not stored, a capital key, and the subtraction reversed. "
    "`lucky[\"mana\"] -= cost` passes too, and so does a changed `cost` (the student's own run follows the "
    "program's own sheet and cost; the reruns stay fixed). Typed values are named in form A's words: a typed result "
    "('`lucky[\"mana\"]` holds a typed 20. ... still said 20.'), a typed cost ('The line takes away a typed 6, not "
    "what `cost` holds. ...') and a typed start ('The line starts from a typed 26, not from `lucky[\"mana\"]`. "
    "...'), each with the evidence in short sentences. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C9 (item 13) fuel cost: param-use, return-right-name, exact-names. PAR, PAR-CONST, RET, PNM, RNM.
# ---------------------------------------------------------------------------------------------

# The same numbered comments, in the same shape, as form A's glug_cost and form B's shield_cost.
FUEL_HEAD = (
    "# 1. Make fuel_cost, with the\n"
    "#    parameters miles and\n"
    "#    ore_per_mile.\n"
    "# 2. Return the ore the whole\n"
    "#    trip needs.\n"
)
FUEL_CALL = "\n\nprint(fuel_cost(4, 3))\n"


def _fuel_cost(body=""):
    return FUEL_HEAD + body + FUEL_CALL


FUEL_DEF = "def fuel_cost(miles, ore_per_mile):\n"
FUEL_COST_STARTER = _fuel_cost()
FUEL_COST_SOLUTION = _fuel_cost(FUEL_DEF + "    need = miles * ore_per_mile\n    return need\n")
TIMES_TEN_EXAMPLE = "def times_ten(n):\n    big = n * 10\n    return big\n\n\nprint(times_ten(7))\n"
_FUEL_CASES = [[[5, 2], 10], [[7, 6], 42]]

FUEL_COST = dict(
    id="fuel-cost",
    title="Fuel cost",
    martu=(
        "Gearshift burns ore on every mile. Write the whole function, yes? The Example shows the shape, with other "
        "names.\n"
        "My check calls your function with other numbers, only inside the check.\n" + _STUCK
    ),
    example=TIMES_TEN_EXAMPLE,
    example_output="70",
    names=["fuel_cost", "miles", "ore_per_mile"],
    support="none",
    explainer="lean",
    starter=FUEL_COST_STARTER,
    checkpoints=[
        dict(
            id="write-fuel-cost",
            text="Write `fuel_cost(miles, ore_per_mile)`, which returns the ore the whole trip needs.",
            dictated=False,
            hints=[
                "Look at the Example: a `def` line, the work, and a `return` line.",
                "A function gets its numbers when it is called, through its parameters.",
                "Use this task's names, letter for letter, not the Example's.",
            ],
            checks=[check("fuel_cost returns the miles times the ore for one mile", _FUNC, fn="fuel_cost",
                          params=["miles", "ore_per_mile"], cases=_FUEL_CASES, foreign=["times_ten", "n", "big"],
                          follow={"miles": "the miles", "ore_per_mile": "the ore for one mile"})],
            pass_line="Gearshift: Twelve ore for four miles at three. Math checks out.",
        ),
    ],
    solution=FUEL_COST_SOLUTION,
    wrong_answers=[
        dict(why="the starter (no function)", code=FUEL_COST_STARTER, fails_at=0,
             message_contains="name 'fuel_cost' is not defined"),
        dict(why="the Example's name returned (RNM)", code=_fuel_cost(FUEL_DEF + "    need = miles * ore_per_mile\n"
                                                                                "    return big\n"),
             fails_at=0, message_contains="name 'big' is not defined"),
        dict(why="RNM with the call removed: the check names the Example's box",
             code=FUEL_HEAD + FUEL_DEF + "    need = miles * ore_per_mile\n    return big\n", fails_at=1,
             message_contains="a name from the Example"),
        dict(why="a near-miss parameter (PNM): ore", code=_fuel_cost(FUEL_DEF + "    return ore * miles\n"), fails_at=0,
             message_contains="name 'ore' is not defined"),
        dict(why="PNM with the call removed: the check names the near miss",
             code=FUEL_HEAD + FUEL_DEF + "    return miles * per_mile\n", fails_at=1,
             message_contains="not one of this function's parameters"),
        dict(why="the Example's 10 kept (PAR: a typed multiplier, a parameter never read)",
             code=_fuel_cost(FUEL_DEF + "    return miles * 10\n"), fails_at=1,
             message_contains="returned `50`: it multiplies by a typed 10, not by `ore_per_mile`, so the answer does "
                              "not follow the ore for one mile."),
        dict(why="the task's 3 ore a mile typed in (PAR: a typed multiplier)",
             code=_fuel_cost(FUEL_DEF + "    return miles * 3\n"), fails_at=1,
             message_contains="multiplies by a typed 3, not by `ore_per_mile`"),
        dict(why="the task's 4 miles typed in (PAR: the other parameter never read)",
             code=_fuel_cost(FUEL_DEF + "    return 4 * ore_per_mile\n"), fails_at=1,
             message_contains="multiplies by a typed 4, not by `miles`, so the answer does not follow the miles."),
        dict(why="a typed number added, a parameter never read (PAR)",
             code=_fuel_cost(FUEL_DEF + "    return miles + 3\n"), fails_at=1,
             message_contains="it adds a typed 3, not `ore_per_mile`"),
        dict(why="a literal (PAR-CONST)", code=_fuel_cost(FUEL_DEF + "    return 12\n"), fails_at=1,
             message_contains="both returned `12`: the numbers are typed in the function, so the answer does not "
                              "follow `miles` and `ore_per_mile`."),
        dict(why="one call's numbers typed (PAR-CONST)", code=_fuel_cost(FUEL_DEF + "    return 4 * 3\n"), fails_at=1,
             message_contains="both returned `12`: the numbers are typed in the function"),
        dict(why="print instead of return (RET)", code=_fuel_cost(FUEL_DEF + "    print(miles * ore_per_mile)\n"),
             fails_at=1, message_contains="`fuel_cost` prints its answer, but the call gets back `None`, Python's "
                                          "word for nothing."),
        dict(why="no return at all", code=_fuel_cost(FUEL_DEF + "    need = miles * ore_per_mile\n"), fails_at=1,
             message_contains="`fuel_cost` has no `return` line, so the call gets back `None`, Python's word for "
                              "nothing."),
        dict(why="a blank return", code=_fuel_cost(FUEL_DEF + "    need = miles * ore_per_mile\n    return\n"),
             fails_at=1, message_contains="`return` stands on its own, so the call gets back `None`"),
        dict(why="the return inside a test that never runs",
             code=_fuel_cost(FUEL_DEF + "    need = miles * ore_per_mile\n    if need > 100:\n        return need\n"),
             fails_at=1, message_contains="No `return` line ran for `fuel_cost(5, 2)`, so the call gets back `None`"),
        dict(why="the function printed, not called (handing over vs calling: no (4, 3))",
             code=FUEL_COST_SOLUTION.replace(FUEL_CALL, "\n\nprint(fuel_cost)\n"), fails_at=1,
             message_contains="prints the function `fuel_cost` itself"),
        dict(why="approximate parameter names", code=_fuel_cost("def fuel_cost(mile, ore):\n    return mile * ore\n"),
             fails_at=1, message_contains="the task names"),
        dict(why="def used like = (def vs =)", code=_fuel_cost("def fuel_cost = miles * ore_per_mile\n"), fails_at=0,
             message_contains="expected '('"),
        dict(why="a missing colon", code=_fuel_cost(FUEL_DEF.replace("):", ")") + "    return miles * ore_per_mile\n"),
             fails_at=0, message_contains="expected ':'"),
        dict(why="+ for * (PAR)", code=_fuel_cost(FUEL_DEF + "    return miles + ore_per_mile\n"), fails_at=1,
             message_contains="returned `7`, not `10`"),
        dict(why="the task's numbers typed inside (PAR-CONST)",
             code=_fuel_cost(FUEL_DEF + "    miles = 4\n    ore_per_mile = 3\n    return miles * ore_per_mile\n"),
             fails_at=1, message_contains="both returned `12`: the numbers are typed in the function"),
        dict(why="= used like def (def vs =): a number, not a function (TypeError at the visible call)",
             code=_fuel_cost("fuel_cost = 12\n"), fails_at=0, message_contains="'int' object is not callable"),
        dict(why="a parameter handed back as it came in (RET-PARAM)", code=_fuel_cost(FUEL_DEF + "    return miles\n"),
             fails_at=1, message_contains="a parameter, just as it came in"),
        dict(why="the box's name returned in quotes (KEY)",
             code=_fuel_cost(FUEL_DEF + '    need = miles * ore_per_mile\n    return "need"\n'), fails_at=1,
             message_contains="a variable's name in quotes"),
        dict(why="numbers on the def line (SyntaxError)", code=_fuel_cost("def fuel_cost(4, 3):\n    return 12\n"),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="the Example's name kept for the function (NAME)",
             code=FUEL_HEAD + "def times_ten(miles, ore_per_mile):\n    return miles * ore_per_mile\n", fails_at=1,
             message_contains="No function called `fuel_cost`"),
    ],
    notes=_rc(13, "code", "param-use,return-right-name,exact-names", "param-use,return-right-name,exact-names",
              "every part with parameters", starter_level="S1", path="READY", dictates="",
              foreign_names="times_ten,n,big", par="(5, 2),(7, 6)") + "\n"
    "C9, item 13 (form A: `glug_cost(sips, price_per_sip)` with `triple`; form B: `shield_cost(plates, "
    "price_per_plate)` with `double`). Directive 4.6: the goal plus an Example (`times_ten(n)`, its box `big`), on "
    "screen with Run. The starter has form A's numbered comments, each line at most 36 characters (1. make "
    "fuel_cost with the parameters miles and ore_per_mile; 2. return the ore the whole trip needs), and Mar'tu says "
    "'Write the whole function, yes?'. Messages in form A's words: the None branches (a print, no `return` line, a "
    "blank `return`, a `return` that never ran) each name `None` as Python's word for nothing; the same answer "
    "twice says the numbers are typed in the function, so the answer does not follow `miles` and `ore_per_mile`; a "
    "typed number with a parameter never read is named before the plain 'not 10' (`miles * 10`: 'it multiplies by "
    "a typed 10, not by `ore_per_mile`, so the answer does not follow the ore for one mile.'). `print(fuel_cost)` "
    "is named (form B's _uncalled). NAME: the exact name and the exact parameters, in order. PAR with (5, 2) -> 10 "
    "and (7, 6) -> 42; the task's own call is (4, 3) -> 12, and neither fresh set gives 12 (lint b). Fails on (spec): the "
    "Example's box -> RNM; `miles * 10` -> PAR (the Example's number kept); `ore * miles` -> PNM; a literal -> "
    "PAR-CONST. RNM and PNM crash at the visible call first, so they reach the student as the explainer's NameError "
    "rows 2 and 3; the check names them too when the visible call is gone. " + _P1_NOTE,
)


# The summary of rc-part1-c and of its questions, in form B's words (both are retake forms).
_P1_SUMMARY = (
    "A retake form. Open it when Mar'tu's notes send you here, for the one task they name. Twelve questions, then "
    "nine short tasks. The glossary, read-aloud and the error explainer stay on; hints are off."
)

RC_PART1_C = dict(
    kind="testout",
    id="rc-part1-c",
    title="Readiness Check · Part 1 · Form C",
    optional=True,
    minutes=20,
    summary=_P1_SUMMARY,
    questions_to_pass=10,
    exercises=[STEP_NORTH, PRESENT_READING, MEND_THE_REPLY, READ_THE_FUEL_SHEET, MEND_THE_GAUGE, TOSS_THE_DIE,
               THREE_TRACEBACKS, SPEND_THE_MANA, FUEL_COST],
    notes=(
        "Readiness Check Part 1, form C (curriculum 5.2 / 5.3): the 9 code tasks of items 2, 3b, 5b, 6a-c, 7b, 8b, 11, "
        "12 and 13, in item order. The 12 questions (items 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, 10a, 10b) live in "
        "rc-part1-c-questions, listed first (ITEMS), as forms A and B, so the first win is a prediction; "
        "questions_to_pass=10 approximates 'Part 1 >= 11/13', as forms A and B. The third parallel form, for a "
        "second retake or a review cycle: the same skills as forms A and B, item for item, with new names, numbers "
        "and situations (5.2; the spec's 'Gearshift's fuel sheet, option 4'). The summary (shared with the "
        "questions, in form B's words) says it is a retake form, opened from Mar'tu's notes for the one task they "
        "name, and that hints are off. Every task's Learn text ends with form A's Stuck line. Optional: form A is "
        "the one the class takes first, and only form A's rc-part1-a is a required testout. 20 minutes here plus 8 "
        "for the questions = the spec's ~28. support='none' and explainer='lean' on every task: no hints, tracer, "
        "Another way, Assemble it or Compare; glossary and read-aloud stay on. Every typed task is behavior-checked "
        "(CMB, PAR, CALL, RND, STO, KEY), never OUT alone. Each task's notes carry review= routes (this file's "
        "ROUTES copy; rc-review, in u10a, names them by title, with form C's titles as the twins). Site work: the 5.5 "
        "scoring (11/13 items, item 6 at 3 of 4, item 13 required), skill-tag routing from the notes' meta lines, "
        "drawing form C for a retake (and another form's questions for a quiz retake), opening one named task from "
        "Mar'tu's notes, and a pass here that never marks the rest of the unit (the mini-boss, rc-explain) tested "
        "out."
    ),
)


# =============================================================================================
# Part 1 form C, questions (quiz rc-part1-c-questions: 10 of the 12 right, questions_to_pass=10)
# =============================================================================================

ORE_LINE = (
    "ore = 8\n"
    "max_ore = 15\n"
    'text = "Ore: " + str(ore)\n'
    'print(text + "/" + str(max_ore))\n'
)
ALARM_PREDICT = (
    "def get_alarm():\n"
    '    line = "REFUEL SOON, GEARSHIFT."\n'
    "    line = line.lower()\n"
    "    line = line.capitalize()\n"
    "    return line\n"
    "\n\n"
    "print(get_alarm())\n"
)
CLIMB_PREDICT = (
    "def climb_check(roll):\n"
    "    needed = 16\n"
    "    return roll >= needed\n"
    "\n\n"
    "print(climb_check(17))\n"
    "print(climb_check(16))\n"
    "print(climb_check(15))\n"
)
LEDGER_PREDICT = (
    "def fuel_burn(miles, loads):\n"
    "    road = miles * 3\n"
    "    haul = loads * 5\n"
    "    return road + haul\n"
    "\n\n"
    "burn = fuel_burn(4, 2) + 6\n"
    "print(burn)\n"
)
OPTION_PREDICT = (
    'choice = "option 4"\n'
    "\n"
    'if choice == "option 1":\n'
    '    print("Oogrish: Wait here.")\n'
    'elif choice == "option 2":\n'
    '    print("Gearshift: On it.")\n'
    "else:\n"
    '    print("Lucky: Not me.")\n'
    'print("The wind drops.")\n'
)
IN_PREDICT = (
    'book = {"Coil": 3, "Flare": 7}\n'
    "print(7 in book)\n"
    'print("Flare" in book)\n'
)
FIXES_HEAD = (
    "def patch(hero):\n"
    '    print(hero["name"], "is fixed.")\n'
    "\n\n"
    'fixes = {"patch": patch}\n'
    'bomb_shell = {"name": "Bomb Shell"}\n'
)
FIXES_LINES = 'fixes["patch"]\nfixes["patch"](bomb_shell)\n'
FIXES_PREDICT = FIXES_HEAD + 'fixes["patch"]\nprint("Next.")\nfixes["patch"](bomb_shell)\n'
TEAM_CODE = (
    "def greet(friend):\n"
    '    name = friend["name"]\n'
    '    print("Welcome,", name)\n'
    "\n\n"
    "team = [\n"
    '    {"name": "Oogrish", "die": 6},\n'
    '    {"name": "Lucky", "die": 6},\n'
    '    {"name": "Gearshift", "die": 8},\n'
    '    {"name": "Mar\'tu", "die": 4},\n'
    "]\n"
    "for friend in team:\n"
    "    greet(friend)\n"
)

RC_PART1_C_QUESTIONS = dict(
    kind="quiz",
    id="rc-part1-c-questions",
    title="Readiness Check · Part 1 · Form C questions",
    optional=True,
    minutes=8,
    summary=_P1_SUMMARY,
    questions=[
        dict(
            type="predict",
            id="glue-the-ore-line",
            q="What will the last line print?",
            code=ORE_LINE,
            choices=["Ore: 8 / 15", "Ore: 23", "Ore:8/15", "Ore: 8/15"],
            answer="Ore: 8/15",
            explain=(
                "`+` glues text exactly as it is, and adds no spaces. The only space is the one inside `\"Ore: \"`. "
                "`str(ore)` is the text `8`, so nothing is added up."
            ),
            notes=_rc(1, "predict", "concat-str", "concat-str", "mana-bars") + "\n"
            "Q1, item 1 (form A: `\"Mana: \" + str(7) + \"/\" + str(10)`; form B: the shield line). The glue is split "
            "over two lines with variables, the mana-bars shape, so every line fits a phone. Fails on (spec): "
            "`Ore:8/15`, `Ore: 8 / 15`. `Ore: 23` is the 'adds the numbers' belief.",
        ),
        dict(
            type="predict",
            id="tidy-the-alarm",
            q="`get_alarm()` tidies its line, then the last line prints it. What will it print?",
            code=ALARM_PREDICT,
            choices=["Refuel soon, Gearshift.", "refuel soon, gearshift.", "Refuel soon, gearshift.",
                     "REFUEL SOON, GEARSHIFT."],
            answer="Refuel soon, gearshift.",
            explain=(
                "`.lower()` makes every letter small. Then `.capitalize()` makes only the very first letter big, so "
                "even Gearshift's name stays small. Each line stores its result back in `line`."
            ),
            notes=_rc(3, "a", "chain-methods,store-then-pass", "chain-methods", "program-dialogue-prompt") + "\n"
            "Q2, item 3a (form A: `get_warning()`; form B: `get_farewell()`). Other words than C2's helper, so running "
            "C2 gives nothing away. Distractors: the name kept big (`.capitalize()` read as fixing names), `.lower()` "
            "only, no tidy at all.",
        ),
        dict(
            type="predict",
            id="exactly-enough-climb",
            q="`climb_check` needs 16. What will these three lines print?",
            code=CLIMB_PREDICT,
            choices=["True\nFalse\nFalse", "True\nTrue\nTrue", "False\nTrue\nFalse", "True\nTrue\nFalse"],
            answer="True\nTrue\nFalse",
            explain=(
                "`>=` means *at least*. 17 is more than 16, so `True`. 16 is exactly enough, so `True`. 15 is short, "
                "so `False`. The function returns the comparison's answer."
            ),
            notes=_rc(4, "a", "boundary,return-comparison,trace-call", "boundary,return-comparison",
                      "skill-checks") + "\n"
            "Q3, item 4a (form A: `latch_check`, needed 11; form B: `dodge_check`, needed 14). The rolls go down this "
            "time. Fails on (spec): the exact roll -> False (`>` read for `>=`). Also every roll passes, and `==` read "
            "for `>=`.",
        ),
        dict(
            type="predict",
            id="be-the-ledger",
            q="Trace it in your head, then type the number this program prints.",
            code=LEDGER_PREDICT,
            answer="28",
            explain=(
                "Trace with what is IN the variables. With another call, `fuel_burn(1, 3) + 6`: `miles` is 1 and "
                "`loads` is 3, so `road` is 3 and `haul` is 15. The function returns 18, and the line adds 6: 24. "
                "Not the numbers written in the function, and not the numbers handed in."
            ),
            notes=_rc(4, "b", "boundary,return-comparison,trace-call", "trace-call", "skill-checks") + "\n"
            "Q4, item 4b, the ledger shape (`ward_strength`-style) with new numbers. Typed, with no choices, as form "
            "B: honest tracing, the answer is in no visible text, and the explanation traces another call (24). Fails "
            "on (spec): the 15-type value (the constants in the function: 3 + 5, then 14 with the + 6) and the "
            "7-type value (the numbers handed in: 4 + 2, then 12). 22 is 'forgot the + 6'.",
        ),
        dict(
            type="predict",
            id="which-branch-runs",
            q="What will this program print?",
            code=OPTION_PREDICT,
            choices=["Oogrish: Wait here.\nThe wind drops.", "Lucky: Not me.", "Lucky: Not me.\nThe wind drops.",
                     "The wind drops."],
            answer="Lucky: Not me.\nThe wind drops.",
            explain=(
                "Python asks each test in order. Neither test is `True`, so it skips both branches and runs `else`. "
                "The last `print` is not indented, so it is outside the chain and always runs."
            ),
            notes=_rc(5, "a", "elif-chain,quote-text", "elif-chain", "program-dialogue-options") + "\n"
            "Q5, item 5a (form A traces `option 2`, form B `option 3`, each landing on an elif). Form C's choice "
            "matches no test, so `else` runs. Fails on (spec): the first branch. Also the unindented last line taken "
            "as part of the chain, and 'nothing in the chain runs'.",
        ),
        dict(
            type="predict",
            id="in-looks-at-keys",
            q="What will these two lines print?",
            code=IN_PREDICT,
            choices=["True\nTrue", "False\nTrue", "True\nFalse", "False\nFalse"],
            answer="False\nTrue",
            explain=(
                "`in` on a dictionary looks at its keys only. 7 is a value, not a key, so `False`. `\"Flare\"` is a "
                "key, so `True`."
            ),
            notes=_rc(6, "d", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable", "dict-in",
                      "spell-book,hold-the-barrier") + "\n"
            "Q6, item 6d (form A: `\"Glow\" in book`; form B: `\"Glimmer\" in book`). The value comes first this time. "
            "Fails on (spec): a value -> True (`in` read as looking at values).",
        ),
        dict(
            type="predict",
            id="stamp-the-gauge",
            q="What will this line print?",
            code='print("█" * 2 + "░" * 5)\n',
            choices=["█2░5", "██ ░░░░░", "██░░░░░", "███████"],
            answer="██░░░░░",
            explain="`*` with text stamps it that many times: two `█`, then five `░`. `+` glues them, with no space.",
            notes=_rc(7, "a", "repeat-string", "repeat-string", "mana-bars") + "\n"
            "Q7, item 7a (form A: `\"█\" * 3 + \"░\" * 2`; form B: 4 and 3). Fails on (spec): `█2░5`. Also a space "
            "added by `+`, and every block the same.",
        ),
        dict(
            type="mc",
            id="faces-of-a-d12",
            q="A d12 roll is `random.randint(1, 12)`. Which numbers can it give?",
            choices=["1 to 11, because the last number is left out", "1 to 12, and both 1 and 12 can come up",
                     "0 to 12, because counting starts at 0", "Only 1 or 12, the two numbers in the brackets"],
            answer=1,
            why_wrong={
                0: "[[randint]] includes its last number, so 12 can come up, like the top face of a real d12.",
                2: "A die has no 0 face: the first number, 1, is the lowest it can give.",
                3: "It gives any whole number from the first to the last, not only the two ends.",
            },
            explain=(
                "`random.randint(1, 12)` gives a whole number from 1 to 12, and both ends can come up, like a real d12."
            ),
            notes=_rc(8, "a", "randint,randint-param", "randint", "skill-checks") + "\n"
            "Q8, item 8a (form A: a d6; form B: a d8). Fails on (spec): 1-11, the exclusive-range belief. Also 0 to 12 "
            "and the two ends only.",
        ),
        dict(
            type="mc",
            id="read-or-call",
            q="`fixes` holds a function under the key `\"patch\"`. What is the difference between these two lines?",
            code=FIXES_HEAD + "\n" + FIXES_LINES,
            choices=[
                "Both lines run the function, so Bomb Shell is fixed twice.",
                "The first runs the function. The second only reads what is stored under the key.",
                "The first is the text `\"patch\"`, the key's name. The second runs the function with it.",
                "The first is the function itself, and runs nothing. The second calls it, with `bomb_shell`.",
            ],
            answer=3,
            why_wrong={
                0: "Only the brackets on the end call a function. Without them, the line only reads what is stored.",
                1: "It is the other way round: the line with `(bomb_shell)` on the end is the one that calls.",
                2: "`fixes[\"patch\"]` is what is stored under the key: the function `patch` itself, not text.",
            },
            explain=(
                "`fixes[\"patch\"]` reads the value under the key: the [[function as a value|function]] itself. Adding "
                "`(bomb_shell)` calls it and hands it `bomb_shell`, like `patch(bomb_shell)`."
            ),
            notes=_rc(9, "a", "func-as-value,call-stored-func", "func-as-value", "spell-book,hold-the-barrier") + "\n"
            "Q9, item 9 explain (form A: `spells[\"glow\"]`; form B: `charms[\"spark\"]`). Fails on (spec): 'both run "
            "the spell'. Distractors: the reverse, and the stored value taken for its key's text.",
        ),
        dict(
            type="predict",
            id="what-the-fix-does",
            q="What will this program print?",
            code=FIXES_PREDICT,
            choices=["Bomb Shell is fixed.\nNext.\nBomb Shell is fixed.", "Next.", "Next.\nBomb Shell is fixed.",
                     "patch\nNext.\nBomb Shell is fixed."],
            answer="Next.\nBomb Shell is fixed.",
            explain=(
                "The line `fixes[\"patch\"]` on its own reads the function and does nothing with it, so nothing "
                "prints. Then `Next.` prints. Only `fixes[\"patch\"](bomb_shell)` calls it: one more line."
            ),
            notes=_rc(9, "b", "func-as-value,call-stored-func", "call-stored-func", "spell-book,hold-the-barrier")
            + "\n"
            "Q10, item 9 predict. The bare read comes first and a print sits between, so 'both run' shows as its own "
            "order. Fails on (spec): 'both run the spell' (the fix twice). Also the call missed, and a bare read "
            "taken to print the key.",
        ),
        dict(
            type="mc",
            id="how-many-calls",
            q="How many times does `greet` run, and what is it handed each time?",
            code=TEAM_CODE,
            choices=[
                "Once, with the whole team.",
                "4 times, with the whole team each time.",
                "4 times, with one hero's sheet each time.",
                "Once, with Mar'tu's sheet only.",
            ],
            answer=2,
            why_wrong={
                0: "The call is inside the [[for loop]], so it runs once on every pass, and `friend` is one hero each "
                   "time.",
                1: "`greet(friend)` hands over `friend`, one sheet from the team, not the whole list.",
                3: "The loop goes through every sheet in `team`, not only the last one.",
            },
            explain=(
                "The loop runs once for each sheet in `team`: 4 passes. On each pass `friend` holds one hero's sheet, "
                "and `greet(friend)` hands that one sheet over."
            ),
            notes=_rc(10, "a", "list-of-dicts,for-each", "list-of-dicts,for-each", "spell-book,mana-bars") + "\n"
            "Q11, item 10 trace (form A: `show_status(hero)` over 3; form B: `check_in(member)` over 3). Four sheets "
            "this time, Mar'tu last. Fails on (spec): 'one call with the whole roster'. Also the whole team each "
            "time, and the last sheet only.",
        ),
        dict(
            type="mc",
            id="what-friend-holds",
            q="Same program. While the loop runs, what does `friend` hold?",
            code=TEAM_CODE,
            choices=[
                "The whole team, all four sheets at once, on every pass.",
                "Each hero's sheet in turn: Oogrish's, then Lucky's, then Gearshift's, then Mar'tu's.",
                "The text `\"friend\"`, the same on every pass of the loop.",
                "A count of the heroes so far: 1, then 2, then 3, then 4.",
            ],
            answer=1,
            why_wrong={
                0: "The team is `team`. `friend` holds one item of it on each pass.",
                2: "`friend` has no quotes: it is a variable, the [[loop variable]].",
                3: "The loop does not count the heroes. It hands over each sheet, in order.",
            },
            explain=(
                "`for friend in team:` puts each item of `team` in `friend`, one pass at a time, in order. Each item "
                "is a hero's sheet, a [[dictionary]]."
            ),
            notes=_rc(10, "b", "list-of-dicts,for-each", "for-each", "spell-book,mana-bars") + "\n"
            "Q12, item 10 explain (one click). Distractors: the whole list, the name taken as text, a count.",
        ),
    ],
    notes=(
        "Readiness Check Part 1, form C questions, scored with rc-part1-c: every code task plus 10 of these 12 "
        "(questions_to_pass=10 on the form, as forms A and B). Item order: 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, "
        "10a, 10b; each question's notes give its item, skill tags, the campaign part it prepares (5.3) and its "
        "review routes. No hints; read-aloud and glossary stay on. Q4, the trace, is typed with no choices (honest "
        "tracing). Right answers sit at varied positions (the site also shuffles)."
    ),
)


# =============================================================================================
# The spaced re-check rc-recheck (5.6): unaided, about a week after the Readiness Check, before the next campaign
# module (teacher decision 2: Modules 1 and 2 are already played, so "before Module 2" no longer applies), for
# everyone. Typed items on combine-values, exact-names, param-use and return-right-name, the class-wide sheet errors,
# and parallel items for 4, 6 and 9 (the questions quiz rc-recheck-questions holds 4a, 6d and 9).
# =============================================================================================


def _rk(parallel, skills, checks, prepares, **more):
    """The meta line for a re-check item: what it re-checks (5.6), its skills and the campaign part it prepares."""
    return meta(recheck="5.6", parallel_of=parallel, skills=skills, checks=checks, prepares=prepares, solo="true",
                path="READY", **more)


_RK_NOTE = ("The spaced re-check is unaided, like Part 1: support='none' and explainer='lean'; glossary and "
            "read-aloud stay on. A miss reverts the skill to 'practicing' (site work).")

# ---------------------------------------------------------------------------------------------
# R1 the trip's ore: combine-values, then reassign. CMB with other trips and other ore.
# ---------------------------------------------------------------------------------------------


def _trip(need="need = 0", take=""):
    return (
        "trips = 3\n"
        "ore_per_trip = 4\n"
        "ore = 30\n"
        "\n"
        "# 1. Make need hold the ore for\n"
        "#    every trip, built from trips\n"
        "#    and ore_per_trip.\n"
        + need + "\n"
        "\n"
        "# 2. Take need out of ore.\n"
        + take + "\n"
        "\n"
        "print(need, ore)\n"
    )


NEED_LINE = "need = trips * ore_per_trip"
TAKE_LINE = "ore = ore - need"
TRIP_STARTER = _trip()
TRIP_SOLUTION = _trip(NEED_LINE, TAKE_LINE)
_TRIP_A = [("trips", "trips = 5"), ("ore_per_trip", "ore_per_trip = 2"), ("ore", "ore = 40")]
_TRIP_B = [("trips", "trips = 2"), ("ore_per_trip", "ore_per_trip = 7"), ("ore", "ore = 14")]
_TRIP_A_SAID = "`trips = 5`, `ore_per_trip = 2` and `ore = 40`"
_TRIP_B_SAID = "`trips = 2`, `ore_per_trip = 7` and `ore = 14`"
_TRIP_WHAT = "tried other trips and other ore"

_TAKE = r'''
_T, _START, _WANT, _OK, _BUILD = __T__, __START__, __WANT__, __OK__, __BUILD__
# The student's own run follows the program's own numbers: `_T`'s first value, less the product of the _BUILD numbers
# (a changed number is fine; the reruns still try fixed other values).
_need = 1
for _nm, _dv in _BUILD:
    _need = _need * _given(_nm, _dv)
_START = _given(_T, _START)
_WANT = _START - _need
assert _T in _g, 'No variable called `' + _T + '` is left in the code.'
_v = _g[_T]
if _v != _WANT:
    if _v == _START:
        _still = '`' + _T + '` is still ' + str(_START)
        _cmp = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare']
        assert not _cmp, _still + ': the line with `==` compares, and stores nothing.'
        _bare = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
        assert not _bare, _still + ': the subtraction is worked out, then forgotten.'
        _shown = [_c for _c in _calls_in(_top(), 'print') if [_a for _a in _c.args if type(_a).__name__ == 'BinOp']]
        assert not _shown, _still + ': the new value is printed, not stored.'
        _box = [_x for _n in _top() if type(_n).__name__ in ('Assign', 'AugAssign')
                and type(_n.value).__name__ == 'BinOp' for _x in _made_by(_n) if _x not in _OK + [_T]]
        assert not _box, _still + ': the new value went into `' + _box[0] + '`.'
        assert False, _still + '.'
    assert False, '`' + _T + '` is ' + _show(_v) + ', not `' + str(_WANT) + '`.'
for _changes, _want, _said, _what, _start, _nd in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _got = _ns.get(_T)
    if _got != _want:
        # CMB, in form A's words: the result, the amount taken or the start was typed, and the check's numbers did
        # not change it.
        assert _got != _WANT, ('`' + _T + '` holds a typed ' + str(_WANT) + ". Mar'tu's check " + _what + ', and `'
                               + _T + '` still said ' + str(_got) + '.')
        assert not (_nd != _need and _got == _start - _need), (
            'The line takes away a typed ' + str(_need) + ', not what `' + _OK[0] + "` holds. Mar'tu's check "
            + _what + ', so `' + _OK[0] + '` held ' + str(_nd) + ', and the line still took away ' + str(_need)
            + ': `' + _T + '` ended at ' + str(_got) + '.')
        assert not (_start != _START and _got == _START - _nd), (
            'The line starts from a typed ' + str(_START) + ', not from `' + _T + "`. Mar'tu's check put "
            + str(_start) + ' in `' + _T + '`, and the line still started from ' + str(_START) + ': `' + _T
            + '` ended at ' + str(_got) + '.')
        assert False, 'With ' + _said + ', `' + _T + '` ended at ' + _show(_got) + ', not `' + str(_want) + '`.' + _ev(_what)
'''

TRIP_ORE = dict(
    id="the-trip-ore",
    title="Ore for the trips",
    martu=(
        "The same skills as before, a week on, with new numbers. No hints, as in Part 1.\n"
        "Gearshift makes `trips` trips, and each one burns `ore_per_trip` ore. My check tries other numbers, only "
        "inside the check.\n" + _STUCK
    ),
    names=["need", "trips", "ore_per_trip", "ore"],
    support="none",
    explainer="lean",
    starter=TRIP_STARTER,
    checkpoints=[
        dict(
            id="build-need",
            text="Make `need` hold the ore for every trip, built from `trips` and `ore_per_trip`.",
            dictated=False,
            hints=[
                "Look at comment 1, and at the three variables at the top.",
                "Build it from the variables, so it follows when they change.",
                "Each trip burns the same ore. How do you get it for every trip?",
            ],
            checks=[check(
                "need is built from trips and ore_per_trip", _FOLLOW, target="need", want=12, place=0,
                mult=[["trips", 3], ["ore_per_trip", 4]],
                rules=[(7, "`need` holds 7: the two numbers added."),
                       (30, "`need` holds 30, the ore Gearshift has.")],
                reruns=[(_TRIP_A, 10, _TRIP_A_SAID, _TRIP_WHAT), (_TRIP_B, 14, _TRIP_B_SAID, _TRIP_WHAT)],
            )],
        ),
        dict(
            id="take-need-out",
            text="Take `need` out of `ore`.",
            dictated=False,
            hints=[
                "Look at comment 2: one line goes under it.",
                "The new ore is worked out from the old ore and `need`, then stored back.",
                "Read the old value on the right of `=`, and store the new one on the left.",
            ],
            checks=[check("ore goes down by need", _TAKE, t="ore", start=30, want=18, ok=["need"],
                          build=[["trips", 3], ["ore_per_trip", 4]],
                          reruns=[(_TRIP_A, 30, _TRIP_A_SAID, _TRIP_WHAT, 40, 10),
                                  (_TRIP_B, 0, _TRIP_B_SAID, _TRIP_WHAT, 14, 14)])],
            pass_line="Gearshift: Every trip paid for. Math checks out.",
        ),
    ],
    solution=TRIP_SOLUTION,
    partials=[_trip(NEED_LINE)],
    wrong_answers=[
        dict(why="the starter (the 0 left)", code=TRIP_STARTER, fails_at=1, message_contains="still holds the starter's 0"),
        dict(why="CP1 a typed 12 (CMB)", code=_trip("need = 12"), fails_at=1,
             message_contains="`need` holds a typed 12. Mar'tu's check tried other trips and other ore, and `need` "
                              "still said 12."),
        dict(why="CP1 + for *", code=_trip("need = trips + ore_per_trip"), fails_at=1, message_contains="added"),
        dict(why="CP1 the sum in quotes (text)", code=_trip('need = "trips * ore_per_trip"'), fails_at=1,
             message_contains="holds text"),
        dict(why="CP1 one typed number in the build (CMB)", code=_trip("need = trips * 4"), fails_at=1,
             message_contains="held `20`, not `10`"),
        dict(why="CP1 an approximate name (NameError)", code=_trip("need = trip * ore_per_trip"), fails_at=0,
             message_contains="name 'trip' is not defined"),
        dict(why="CP2 a typed 18 (CMB)", code=_trip(NEED_LINE, "ore = 18"), fails_at=2,
             message_contains="`ore` holds a typed 18. Mar'tu's check tried other trips and other ore, and `ore` "
                              "still said 18."),
        dict(why="CP2 a typed start (CMB)", code=_trip(NEED_LINE, "ore = 30 - need"), fails_at=2,
             message_contains="The line starts from a typed 30, not from `ore`. Mar'tu's check put 40 in `ore`, and "
                              "the line still started from 30: `ore` ended at 20."),
        dict(why="CP2 a typed 12 in place of need (CMB)", code=_trip(NEED_LINE, "ore = ore - 12"), fails_at=2,
             message_contains="The line takes away a typed 12, not what `need` holds. Mar'tu's check tried other "
                              "trips and other ore, so `need` held 10, and the line still took away 12: `ore` ended "
                              "at 28."),
        dict(why="CP1 a typed number after the student changed trips (CMB: the reruns still catch it)",
             code=_trip("need = 16").replace("trips = 3", "trips = 4"), fails_at=1,
             message_contains="`need` holds a typed 16"),
        dict(why="CP2 the subtraction with no store", code=_trip(NEED_LINE, "ore - need"), fails_at=2,
             message_contains="worked out, then forgotten"),
        dict(why="CP2 == for =", code=_trip(NEED_LINE, "ore == ore - need"), fails_at=2, message_contains="compares"),
        dict(why="CP2 the new ore in a new variable (NEWBOX)", code=_trip(NEED_LINE, "ore_left = ore - need"),
             fails_at=2, message_contains="went into `ore_left`"),
        dict(why="CP2 the subtraction reversed", code=_trip(NEED_LINE, "ore = need - ore"), fails_at=2,
             message_contains="`-18`"),
        dict(why="CP2 printed, not stored", code=_trip(NEED_LINE, "print(ore - need)"), fails_at=2,
             message_contains="printed, not stored"),
        dict(why="CP2 need overwritten (the new ore went into need)", code=_trip(NEED_LINE, "need = ore - need"),
             fails_at=1, message_contains="`need` holds `18`, not `12`"),
    ],
    notes=_rk("1,12", "combine-values,reassign", "combine-values,reassign", "mana-bars,hold-the-barrier",
              starter_level="S2", dictates="", foreign_names="", review=_review(12)) + "\n"
    "R1 (5.6: a typed item on combine-values, for everyone). CP1 CMB: `need` is built from `trips` and "
    "`ore_per_trip` (3 x 4 = 12); the program reruns with 5 trips of 2 (10) and 2 trips of 7 (14), so a typed 12 or "
    "one typed number in the build fails. CP2 reassign + CMB: `ore` goes down by `need` (30 -> 18); the reruns also "
    "change the start (40 -> 30, 14 -> 0, exactly empty), so a typed 18 and a typed start fail. Also the subtraction "
    "with no store, `==` for `=`, NEWBOX, reversed, printed. `ore -= need` passes too, and so do changed numbers "
    "(the student's own run follows the program's own `trips`, `ore_per_trip` and `ore`; the reruns stay fixed). "
    "Typed values are named in form A's words ('`need` holds a typed 12. Mar'tu's check tried other trips and other "
    "ore, and `need` still said 12.'; 'The line takes away a typed 12, not what `need` holds. ...'; 'The line "
    "starts from a typed 30, not from `ore`. ...'). " + _RK_NOTE,
)


# ---------------------------------------------------------------------------------------------
# R2 Lucky's sheet: item 6's parallel and the class-wide sheet errors (a skipped level, a quoted name, typed values).
# ---------------------------------------------------------------------------------------------

LUCKY_SHEET = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    '    "abilities": {\n'
    '        "personality": 15,\n'
    '        "magical_affinity": 13,\n'
    "    },\n"
    "}\n"
)


def _lucky(mana="mana_now = 0", aff="aff_now = 0", store="", tricks='tricks = {"Dumb Luck": {"uses": 1}}'):
    return (
        LUCKY_SHEET + "\n"
        "# 1. Make mana_now hold Lucky's\n"
        "#    mana, read from the sheet.\n"
        + mana + "\n"
        "\n"
        "# 2. Make aff_now hold Lucky's\n"
        "#    magical affinity, read from\n"
        "#    the sheet.\n"
        + aff + "\n"
        "\n"
        + tricks + "\n"
        'trick_name = "Hedge Hop"\n'
        'trick = {"uses": 2}\n'
        "# 3. Store trick in tricks, using\n"
        "#    trick_name as the key.\n"
        + store + "\n"
        "\n"
        "print(mana_now, aff_now)\n"
        "print(tricks)\n"
    )


L_MANA = 'mana_now = lucky["mana"]'
L_AFF = 'aff_now = lucky["abilities"]["magical_affinity"]'
L_STORE = "tricks[trick_name] = trick"
LUCKY_STARTER = _lucky()
LUCKY_SOLUTION = _lucky(L_MANA, L_AFF, L_STORE)
THORN_SHEET = {"name": "Thorn", "mana": 8, "abilities": {"personality": 4, "magical_affinity": 11}}
_OTHER_LUCKY = [("lucky", "lucky = " + repr(THORN_SHEET))]
_LUCKY_SAID = "another sheet in `lucky` (Thorn: 8 mana, magical affinity 11)"
_LUCKY_WHAT = "put another sheet in `lucky`"
_TRICK_RERUNS = [([("trick_name", 'trick_name = "Moth Dance"'), ("trick", 'trick = {"uses": 5}')], 5,
                  '`trick_name = "Moth Dance"` and `trick = {"uses": 5}`',
                  "set `trick_name` and `trick` to other values")]

LUCKY_SHEET_TASK = dict(
    id="lucky-sheet",
    title="Lucky's sheet",
    martu=(
        "Lucky's stat sheet, with his abilities in a [[nested dictionary]]. Read two values, then write one entry "
        "into his book of tricks.\n"
        "My check puts other sheets and other entries in, only inside the check.\n" + _STUCK
    ),
    names=["mana_now", "aff_now", "tricks", "trick_name", "trick"],
    support="none",
    explainer="lean",
    starter=LUCKY_STARTER,
    checkpoints=[
        dict(
            id="read-the-mana",
            text="Make `mana_now` hold Lucky's mana, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 1, and at the sheet's keys.",
                "Square brackets after a dictionary's name read the value under one key.",
                "The key is text, so it keeps its quotes.",
            ],
            checks=[check(
                "mana_now reads the mana from the sheet", _FOLLOW, target="mana_now", want=26, place=0, mult=[],
                rules=[(13, "`mana_now` holds 13, Lucky's magical affinity."),
                       (15, "`mana_now` holds 15, Lucky's personality.")],
                reruns=[(_OTHER_LUCKY, 8, _LUCKY_SAID, _LUCKY_WHAT)],
            )],
        ),
        dict(
            id="read-the-affinity",
            text="Make `aff_now` hold Lucky's magical affinity, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 2. Where on the sheet is `\"magical_affinity\"`?",
                "A dictionary inside a dictionary is read one key at a time, outer key first.",
                "Two pairs of square brackets in a row.",
            ],
            checks=[check(
                "aff_now reads the affinity from inside the abilities", _FOLLOW, target="aff_now", want=13, place=0, mult=[],
                rules=[(15, "`aff_now` holds 15, Lucky's personality."),
                       (26, "`aff_now` holds 26, Lucky's mana.")],
                reruns=[(_OTHER_LUCKY, 11, _LUCKY_SAID, _LUCKY_WHAT)],
            )],
        ),
        dict(
            id="store-the-trick",
            text="Store `trick` in `tricks`, using `trick_name` as the key.",
            dictated=False,
            hints=[
                "Look at comment 3, under the three lines about the tricks.",
                "Square brackets on the left of `=` write an entry into a dictionary.",
                QUOTES_RULE,
            ],
            checks=[check("the trick is stored under the name in trick_name", _STORE_BY_NAME, bk="tricks",
                          kv="trick_name", vv="trick", kept="Dumb Luck", newkey="Moth Dance", oldkey="Hedge Hop",
                          field="uses",
                          page="entry", reruns=_TRICK_RERUNS)],
            pass_line="Lucky: Hedge Hop. Landed in a hedge once. Worth it.",
        ),
    ],
    solution=LUCKY_SOLUTION,
    partials=[_lucky(L_MANA), _lucky(L_MANA, L_AFF)],
    wrong_answers=[
        dict(why="the starter (0 placeholders)", code=LUCKY_STARTER, fails_at=1, message_contains="still holds"),
        dict(why="CP1 a typed 26 (CMB)", code=_lucky("mana_now = 26"), fails_at=1,
             message_contains="`mana_now` holds a typed 26. Mar'tu's check put another sheet in `lucky`, and "
                              "`mana_now` still said 26."),
        dict(why="CP1 the affinity read for the mana", code=_lucky('mana_now = lucky["abilities"]["magical_affinity"]'),
             fails_at=1, message_contains="magical affinity"),
        dict(why="CP1 the key without quotes (NameError)", code=_lucky("mana_now = lucky[mana]"), fails_at=0,
             message_contains="name 'mana' is not defined"),
        dict(why="CP2 a skipped nesting level (KeyError)", code=_lucky(L_MANA, 'aff_now = lucky["magical_affinity"]'),
             fails_at=0, message_contains="KeyError: 'magical_affinity'"),
        dict(why="CP2 an approximate key (KeyError)", code=_lucky(L_MANA, 'aff_now = lucky["abilities"]["affinity"]'),
             fails_at=0, message_contains="KeyError: 'affinity'"),
        dict(why="CP2 only the outer key: the whole abilities dictionary",
             code=_lucky(L_MANA, 'aff_now = lucky["abilities"]'), fails_at=2, message_contains="whole dictionary"),
        dict(why="CP2 a typed 13 (CMB)", code=_lucky(L_MANA, "aff_now = 13"), fails_at=2,
             message_contains="`aff_now` holds a typed 13. Mar'tu's check put another sheet in `lucky`"),
        dict(why="CP2 the wrong inner key", code=_lucky(L_MANA, 'aff_now = lucky["abilities"]["personality"]'),
             fails_at=2, message_contains="personality"),
        dict(why="CP3 the variable's name quoted as the key (KEY)",
             code=_lucky(L_MANA, L_AFF, 'tricks["trick_name"] = trick'), fails_at=3, message_contains='"trick_name"'),
        dict(why="CP3 a typed key (CMB)", code=_lucky(L_MANA, L_AFF, 'tricks["Hedge Hop"] = trick'), fails_at=3,
             message_contains="The key is a typed `\"Hedge Hop\"`. Mar'tu's check put another name in `trick_name`, "
                              "and the key still said `\"Hedge Hop\"`."),
        dict(why="CP3 the book rebuilt: the first entry lost", code=_lucky(L_MANA, L_AFF, "tricks = {trick_name: trick}"),
             fails_at=3, message_contains="lost its Dumb Luck entry"),
        dict(why="CP3 a typed copy of the entry (CMB)", code=_lucky(L_MANA, L_AFF, 'tricks[trick_name] = {"uses": 2}'),
             fails_at=3, message_contains="did not hold the new `trick`"),
        dict(why="CP3 the trick's name stored, not the trick", code=_lucky(L_MANA, L_AFF, "tricks[trick_name] = trick_name"),
             fails_at=3, message_contains="not the `trick` dictionary"),
    ],
    notes=_rk("6", "dict-read,dict-nested,dict-write,dict-key-from-variable", "dict-read,dict-nested,dict-write,"
              "dict-key-from-variable", "spell-book,hold-the-barrier", starter_level="S2", dictates="",
              foreign_names="", review=_review(6)) + "\n"
    "R2 (5.6: the parallel item for 6, and the class-wide sheet errors, for everyone). Lucky's real values (26 mana, "
    "magical affinity 13), with an invented personality of 15. CP1 / CP2 CMB: reruns with Thorn's sheet (8 mana, "
    "affinity 11). CP2 catches the skipped level (`lucky[\"magical_affinity\"]`, KeyError) and an approximate key "
    "(`\"affinity\"`), the campaign's hold-the-barrier read. CP3 KEY + CMB: the entry under the name `trick_name` "
    "holds, the Dumb Luck entry kept, and a rerun with `trick_name = \"Moth Dance\"`. Item 6d (dict-in) is RQ2. "
    + _RK_NOTE,
)


# ---------------------------------------------------------------------------------------------
# R3 trace the call: item 4b's parallel, the ledger (trace-call). Typed rows, the paste guard and paste_stop.
# ---------------------------------------------------------------------------------------------

LEDGER_FN = "cart_load"
LEDGER_PROGRAM = (
    "def cart_load(crates, sacks):\n"
    "    heavy = crates * 9\n"
    "    light = sacks * 2\n"
    "    return heavy + light\n"
    "\n\n"
    "weight = cart_load(2, 4) + 10\n"
    "print(weight)\n"
)
LEDGER_BACK, LEDGER_SHOWN = 26, 36            # 2 * 9 + 4 * 2 = 26; 26 + 10 = 36
LEDGER_CONST, LEDGER_RAW = 11, 6              # 9 + 2 (the constants); 2 + 4 (the values handed over)
LEDGER_ONE = (18, 8)                          # one variable only


def paste_stop(fn):
    """Hidden `setup` (as u03a / u03b's ledgers): when the editor holds a `def`, a call to `fn` or a `print(`, the
    program is stopped before it runs (SystemExit ends it quietly), so a pasted program prints nothing and the console
    never shows the answer. The paste guard check then names the slip. Code that does not parse runs as usual."""
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


def paste_guard(fn):
    """The ledger's guard (as u03b): the program may not be pasted in and run. No `def`, no call, no `print(`."""
    code = (
        "import ast as _ast\n"
        "_bad = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef' or "
        "(type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id in "
        f"({fn!r}, 'print'))]\n"
        "assert not _bad, ('The editor holds more than the two row lines: a `def`, a call to the function or a '\n"
        "                  '`print`. This task is traced by reading, yes?')\n"
    )
    return ("the program is traced, not run", code)


def row_check(label, name, want, rules, default):
    """The ledger shape (as u03b's row_check): `name` holds `want`. rules = {wrong value: targeted message}. Lean: the
    messages name the slip, never the number or the fix."""
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


_CONST = "That adds the numbers written in the function, not what is IN each variable when `return` runs."
_RAW = "That adds the values handed over, not what the function worked out."
_ONE = "That is what one variable holds, not what `return` hands back."
_BACK_RULES = {LEDGER_CONST: _CONST, LEDGER_RAW: _RAW, LEDGER_SHOWN: "That adds the 10 from the last line too.",
               LEDGER_ONE[0]: _ONE, LEDGER_ONE[1]: _ONE}
_SHOWN_RULES = {
    LEDGER_BACK: "That leaves out the 10 the last line adds.",
    LEDGER_CONST + 10: "That adds the numbers written in the function, then 10.",
    LEDGER_RAW + 10: "That adds the values handed over, then 10.",
    LEDGER_CONST: _CONST,
    LEDGER_RAW: _RAW,
}
# Each row's slips differ from each other and from the row's answer, so every slip gets its own message.
assert len(set(_BACK_RULES)) == 5 and LEDGER_BACK not in _BACK_RULES
assert len(set(_SHOWN_RULES)) == 5 and LEDGER_SHOWN not in _SHOWN_RULES
assert (2 * 9 + 4 * 2, 2 * 9 + 4 * 2 + 10) == (LEDGER_BACK, LEDGER_SHOWN)


def _rows(back=0, shown=0, quote=False):
    q = '"' if quote else ""
    return (f"# The ledger for {LEDGER_FN}(2, 4)\n"
            f"handed_back_row = {q}{back}{q}\n"
            f"printed_row = {shown}\n")


LEDGER_STARTER = _rows()
LEDGER_SOLUTION = _rows(LEDGER_BACK, LEDGER_SHOWN)
_GUARD = paste_guard(LEDGER_FN)

TRACE_THE_CALL = dict(
    id="trace-the-call",
    title="Trace the call",
    martu=(
        "Trace it like a ledger: what does the call hand back, and what does the last line print? Read it, do not "
        "run it.\n"
        "```python\n" + LEDGER_PROGRAM + "```\n" + _STUCK
    ),
    names=["handed_back_row", "printed_row"],
    support="none",
    explainer="lean",
    # A pasted program is stopped before it runs, so its printed number never shows (as QC-R1's ledger).
    setup=paste_stop(LEDGER_FN),
    starter=LEDGER_STARTER,
    checkpoints=[
        dict(
            id="handed-back-row",
            text=f"Set `handed_back_row` to the number `{LEDGER_FN}(2, 4)` hands back.",
            dictated=False,
            hints=[
                "Look at the `return` line. What is in `heavy` and `light` when it runs?",
                "Work out each line from what is IN the variables, not from the numbers you see first.",
                "The call fills `crates` and `sacks`, in order.",
            ],
            checks=[_GUARD, row_check("handed_back_row is what the call hands back", "handed_back_row", LEDGER_BACK, _BACK_RULES,
                                      f"That is not what `{LEDGER_FN}(2, 4)` hands back.")],
        ),
        dict(
            id="printed-row",
            text="Set `printed_row` to the number the last line prints.",
            dictated=False,
            hints=[
                "Look at the `weight` line: the call becomes what it handed back.",
                "Then the rest of that line is worked out.",
                "Your first row is where this one starts.",
            ],
            checks=[_GUARD, row_check("printed_row is what the last line prints", "printed_row", LEDGER_SHOWN, _SHOWN_RULES,
                                      "That is not what the last line prints.")],
            pass_line="Mar'tu: Traced, not guessed. That is the ledger, yes?",
        ),
    ],
    solution=LEDGER_SOLUTION,
    partials=[_rows(LEDGER_BACK)],
    wrong_answers=[
        dict(why="the starter (the 0 left)", code=LEDGER_STARTER, fails_at=1, message_contains="still holds the starter's 0"),
        dict(why=f"handed back = {LEDGER_CONST}: the numbers written in the function (the 15-type answer)",
             code=_rows(LEDGER_CONST), fails_at=1, message_contains="numbers written in the function"),
        dict(why=f"handed back = {LEDGER_RAW}: the values handed over (the 7-type answer)", code=_rows(LEDGER_RAW),
             fails_at=1, message_contains="values handed over"),
        dict(why=f"handed back = {LEDGER_SHOWN}: the + 10 from the last line added in", code=_rows(LEDGER_SHOWN),
             fails_at=1, message_contains="10 from the last line"),
        dict(why=f"handed back = {LEDGER_ONE[0]}: one variable only", code=_rows(LEDGER_ONE[0]), fails_at=1,
             message_contains="one variable holds"),
        dict(why="handed back in quotes", code=_rows(LEDGER_BACK, quote=True), fails_at=1,
             message_contains="because of the quotes"),
        dict(why="the program pasted in and run (the paste guard; paste_stop keeps the console empty)",
             code=LEDGER_PROGRAM + "\n" + LEDGER_SOLUTION, fails_at=1, message_contains="more than the two row lines"),
        dict(why=f"printed = {LEDGER_BACK}: the + 10 dropped", code=_rows(LEDGER_BACK, LEDGER_BACK), fails_at=2,
             message_contains="leaves out the 10"),
        dict(why=f"printed = {LEDGER_CONST + 10}: the numbers in the function, then 10",
             code=_rows(LEDGER_BACK, LEDGER_CONST + 10), fails_at=2,
             message_contains="numbers written in the function, then 10"),
        dict(why=f"printed = {LEDGER_RAW + 10}: the values handed over, then 10", code=_rows(LEDGER_BACK, LEDGER_RAW + 10),
             fails_at=2, message_contains="values handed over, then 10"),
        dict(why="printed row: the 0 left", code=_rows(LEDGER_BACK), fails_at=2, message_contains="still holds the starter's 0"),
        dict(why="a print added to check the rows (the guard: no print in the editor)",
             code=LEDGER_SOLUTION + "print(handed_back_row)\n", fails_at=1, message_contains="more than the two row lines"),
    ],
    notes=_rk("4b", "trace-call", "trace-call", "skill-checks", starter_level="S2", dictates="",
              foreign_names="", review=_review(4)) + "\n"
    f"R3 (5.6: the parallel item for 4b, the ledger shape). Typed and gated in the testout, as QC-R1's trace-the-call: "
    f"{LEDGER_FN}(2, 4) hands back {LEDGER_BACK}, the last line prints {LEDGER_SHOWN}. Honest tracing: the program "
    "sits in Mar'tu's fenced block, no visible text holds a row's number, and no hint does; the paste guard fails any "
    "`def`, call to the function or `print(` in the editor, and the hidden setup (paste_stop) stops such a program "
    "before it runs, so the console never shows its number. No assemble (its pieces would be the rows), no Another "
    f"way. Every slip gets a message that names it without the number: {LEDGER_CONST} (the constants), {LEDGER_RAW} "
    f"(the values handed over), {LEDGER_SHOWN} in the first row (the + 10 too early), {LEDGER_ONE[0]} / "
    f"{LEDGER_ONE[1]} (one variable), then {LEDGER_BACK} printed (the + 10 dropped), {LEDGER_CONST + 10} and "
    f"{LEDGER_RAW + 10} (the same slips, then 10). Item 4a is RQ1. " + _RK_NOTE,
)


# ---------------------------------------------------------------------------------------------
# R4 the bar's gap: exact-names, param-use, return-right-name. PAR, PAR-CONST, RET, RET-PARAM, PNM, RNM.
# ---------------------------------------------------------------------------------------------

# The same numbered comments, in the same shape, as fuel_cost's (and forms A and B's).
GAP_HEAD = (
    "# 1. Make bar_gap, with the\n"
    "#    parameters max_mana and\n"
    "#    mana.\n"
    "# 2. Return how many points\n"
    "#    are used up.\n"
)
GAP_CALL = "\n\nprint(bar_gap(20, 14))\n"


def _gap(body=""):
    return GAP_HEAD + body + GAP_CALL


GAP_DEF = "def bar_gap(max_mana, mana):\n"
GAP_STARTER = _gap()
GAP_SOLUTION = _gap(GAP_DEF + "    used = max_mana - mana\n    return used\n")
TAKE_TWO_EXAMPLE = "def take_two(n):\n    smaller = n - 2\n    return smaller\n\n\nprint(take_two(9))\n"
_GAP_CASES = [[[26, 12], 14], [[24, 7], 17]]

BAR_GAP = dict(
    id="bar-gap",
    title="The bar's gap",
    martu=(
        "A mana bar draws a `░` for each point used up. Write the whole function that counts them. The Example shows "
        "the shape, with other names.\n"
        "My check calls your function with other numbers, only inside the check.\n" + _STUCK
    ),
    example=TAKE_TWO_EXAMPLE,
    example_output="7",
    names=["bar_gap", "max_mana", "mana"],
    support="none",
    explainer="lean",
    starter=GAP_STARTER,
    checkpoints=[
        dict(
            id="write-bar-gap",
            text="Write `bar_gap(max_mana, mana)`, which returns how many points of mana are used up.",
            dictated=False,
            hints=[
                "Look at the Example: a `def` line, the work, and a `return` line.",
                "A function gets its numbers when it is called, through its parameters, in order.",
                "Use this task's names, letter for letter, not the Example's.",
            ],
            checks=[check("bar_gap returns the mana used up", _FUNC, fn="bar_gap", params=["max_mana", "mana"],
                          cases=_GAP_CASES, foreign=["take_two", "n", "smaller"],
                          follow={"max_mana": "the max mana", "mana": "the mana"})],
            pass_line="Mar'tu: Six used, six `░`. The bar can be drawn now.",
        ),
    ],
    solution=GAP_SOLUTION,
    wrong_answers=[
        dict(why="the starter (no function)", code=GAP_STARTER, fails_at=0, message_contains="name 'bar_gap' is not defined"),
        dict(why="the Example's name returned (RNM)", code=_gap(GAP_DEF + "    used = max_mana - mana\n    return smaller\n"),
             fails_at=0, message_contains="name 'smaller' is not defined"),
        dict(why="RNM with the call removed: the check names the Example's box",
             code=GAP_HEAD + GAP_DEF + "    used = max_mana - mana\n    return smaller\n", fails_at=1,
             message_contains="a name from the Example"),
        dict(why="a near-miss parameter (PNM): mana_max", code=_gap(GAP_DEF + "    return mana_max - mana\n"), fails_at=0,
             message_contains="name 'mana_max' is not defined"),
        dict(why="PNM with the call removed", code=GAP_HEAD + GAP_DEF + "    return mana_max - mana\n", fails_at=1,
             message_contains="not one of this function's parameters"),
        dict(why="the subtraction reversed", code=_gap(GAP_DEF + "    return mana - max_mana\n"), fails_at=1,
             message_contains="returned `-14`, not `14`"),
        dict(why="the Example's 2 kept (PAR: a typed number, a parameter never read)",
             code=_gap(GAP_DEF + "    return max_mana - 2\n"), fails_at=1,
             message_contains="returned `24`: it takes away a typed 2, not `mana`, so the answer does not follow the "
                              "mana."),
        dict(why="the task's 20 typed in (PAR: the max never read)", code=_gap(GAP_DEF + "    return 20 - mana\n"),
             fails_at=1, message_contains="it starts from a typed 20, not from `max_mana`, so the answer does not "
                                          "follow the max mana."),
        dict(why="a literal (PAR-CONST)", code=_gap(GAP_DEF + "    return 6\n"), fails_at=1,
             message_contains="both returned `6`: the numbers are typed in the function, so the answer does not "
                              "follow `max_mana` and `mana`."),
        dict(why="print instead of return (RET)", code=_gap(GAP_DEF + "    print(max_mana - mana)\n"), fails_at=1,
             message_contains="`bar_gap` prints its answer, but the call gets back `None`, Python's word for "
                              "nothing."),
        dict(why="no return at all", code=_gap(GAP_DEF + "    used = max_mana - mana\n"), fails_at=1,
             message_contains="`bar_gap` has no `return` line, so the call gets back `None`, Python's word for "
                              "nothing."),
        dict(why="a blank return", code=_gap(GAP_DEF + "    used = max_mana - mana\n    return\n"), fails_at=1,
             message_contains="`return` stands on its own, so the call gets back `None`"),
        dict(why="a parameter handed back as it came in (RET-PARAM)", code=_gap(GAP_DEF + "    return mana\n"), fails_at=1,
             message_contains="a parameter, just as it came in"),
        dict(why="a typed mana (PAR: a typed number): 26 - 14 is 12, the same as the mana handed in, but no "
                 "parameter came back",
             code=_gap(GAP_DEF + "    return max_mana - 14\n"), fails_at=1,
             message_contains="returned `12`: it takes away a typed 14, not `mana`, so the answer does not follow "
                              "the mana."),
        dict(why="the box's name returned in quotes (KEY)",
             code=_gap(GAP_DEF + '    used = max_mana - mana\n    return "used"\n'), fails_at=1,
             message_contains="a variable's name in quotes"),
        dict(why="the parameters swapped on the def line", code=_gap("def bar_gap(mana, max_mana):\n"
                                                                     "    return max_mana - mana\n"),
             fails_at=1, message_contains="the task names `max_mana` and `mana`"),
        dict(why="approximate parameter names", code=_gap("def bar_gap(max, now):\n    return max - now\n"), fails_at=1,
             message_contains="the task names"),
        dict(why="def used like = (def vs =)", code=_gap("def bar_gap = max_mana - mana\n"), fails_at=0,
             message_contains="expected '('"),
        dict(why="a missing colon", code=_gap(GAP_DEF.replace("):", ")") + "    return max_mana - mana\n"), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the task's numbers typed inside (PAR-CONST)",
             code=_gap(GAP_DEF + "    max_mana = 20\n    mana = 14\n    return max_mana - mana\n"), fails_at=1,
             message_contains="both returned `6`: the numbers are typed in the function"),
        dict(why="the function printed, not called (handing over vs calling: no (20, 14))",
             code=GAP_SOLUTION.replace(GAP_CALL, "\n\nprint(bar_gap)\n"), fails_at=1,
             message_contains="prints the function `bar_gap` itself"),
    ],
    notes=_rk("13", "param-use,return-right-name,exact-names", "param-use,return-right-name,exact-names",
              "mana-bars,every part with parameters", starter_level="S1", dictates="",
              foreign_names="take_two,n,smaller", par="(26, 12),(24, 7)", review=_review(13)) + "\n"
    "R4 (5.6: typed items on exact-names, param-use and return-right-name, for everyone). The mana-bars count, "
    "`max_mana - mana`, as a function from its goal with an Example (`take_two(n)`, its box `smaller`). PAR with "
    "(26, 12) -> 14 and (24, 7) -> 17; the task's own call is (20, 14) -> 6, and neither fresh set gives 6 (lint b). "
    "The order of the parameters matters here, so a swapped `def` line is named. The starter has C9's numbered "
    "comments (1. make bar_gap with the parameters max_mana and mana; 2. return how many points are used up), and "
    "Mar'tu says 'Write the whole function that counts them.'. The same messages as C9 (form A's): `None` as "
    "Python's word for nothing, the same answer twice as typed numbers, and a typed number with a parameter never "
    "read (`max_mana - 2`, `max_mana - 14`: 'it takes away a typed 14, not `mana`'; `20 - mana`: 'it starts from "
    "a typed 20, not from `max_mana`'). " + _RK_NOTE,
)


_RECHECK_SUMMARY = (
    "The re-check, about a week after the Readiness Check, before the next campaign module. Four short tasks and "
    "four questions, with no hints. Pass every task and 3 of the 4 questions."
)

RC_RECHECK = dict(
    kind="testout",
    id="rc-recheck",
    title="Readiness Re-check",
    optional=True,
    minutes=9,
    summary=_RECHECK_SUMMARY,
    questions_to_pass=3,
    exercises=[TRIP_ORE, LUCKY_SHEET_TASK, TRACE_THE_CALL, BAR_GAP],
    notes=(
        "The spaced re-check (curriculum 5.6, 5.2: ~12 minutes, unaided, for everyone, G4 R8), about a week after "
        "the Readiness Check, before the next campaign module (teacher decision 2: the class already played Modules "
        "1 and 2, so the spec's 'before Module 2' becomes 'before the next module'): R1 combine-values (and "
        "reassign), R2 the parallel item for 6 with the class-wide sheet errors, R3 the parallel item for 4b (the "
        "ledger, paste_stop), R4 exact-names / param-use / return-right-name. Its questions (rc-recheck-questions, "
        "listed first, as the Part 1 forms) are the parallel items for 4a, 6d and 9; questions_to_pass=3 allows one "
        "miss. 9 minutes here plus 3 for the questions. Every item is new: no form's item repeats. Optional, so it "
        "never holds the unit open. Site request: keep it hidden until it is due (about a week after the student's "
        "Readiness Check), and never let a pass here mark the unit, the mini-boss or rc-explain done or tested out "
        "(today it would sit in the unit page's Quick Check offer, and a pass would mark the unit tested out). Site "
        "work too: scheduling it, re-verifying tested-out skills here, reverting a missed skill to 'practicing', "
        "and adding each student's own misses (the parallel items of another form)."
    ),
)


# =============================================================================================
# The re-check's questions (quiz rc-recheck-questions: 3 of the 4 right, questions_to_pass=3)
# =============================================================================================

LOCK_PREDICT = (
    "def lock_check(roll):\n"
    "    needed = 12\n"
    "    return roll >= needed\n"
    "\n\n"
    "print(lock_check(12))\n"
    "print(lock_check(11))\n"
    "print(lock_check(13))\n"
)
KIT_PREDICT = (
    'kit = {"Rope": 2, "Lamp": 1}\n'
    "print(1 in kit)\n"
    'print("Rope" in kit)\n'
)
MOVES_HEAD = (
    "def hop(hero):\n"
    '    print(hero["name"], "hops.")\n'
    "\n\n"
    'moves = {"hop": hop}\n'
    'lucky = {"name": "Lucky"}\n'
)
MOVES_LINES = 'moves["hop"]\nmoves["hop"](lucky)\n'
MOVES_PREDICT = MOVES_HEAD + 'go = moves["hop"]\nprint("Set.")\ngo(lucky)\ngo(lucky)\n'

RC_RECHECK_QUESTIONS = dict(
    kind="quiz",
    id="rc-recheck-questions",
    title="Readiness Re-check questions",
    optional=True,
    minutes=3,
    summary="Four questions that go with the re-check. Get 3 of the 4 right.",
    questions=[
        dict(
            type="predict",
            id="exactly-enough-lock",
            q="`lock_check` needs 12. What will these three lines print?",
            code=LOCK_PREDICT,
            choices=["False\nFalse\nTrue", "True\nFalse\nTrue", "True\nTrue\nTrue", "True\nFalse\nFalse"],
            answer="True\nFalse\nTrue",
            explain=(
                "`>=` means *at least*. 12 is exactly enough, so `True`. 11 is short, so `False`. 13 is more than "
                "enough, so `True`."
            ),
            notes=_rk("4a", "boundary,return-comparison", "boundary,return-comparison", "skill-checks") + "\n"
            "RQ1, the parallel item for 4a. The exact roll comes first. Fails on (spec): 12 -> False (`>` read for "
            "`>=`). Also every roll passes, and only the exact roll passing.",
        ),
        dict(
            type="predict",
            id="in-looks-at-keys",
            q="What will these two lines print?",
            code=KIT_PREDICT,
            choices=["True\nTrue", "True\nFalse", "False\nFalse", "False\nTrue"],
            answer="False\nTrue",
            explain=(
                "`in` on a dictionary looks at its keys only. 1 is a value, not a key, so `False`. `\"Rope\"` is a "
                "key, so `True`."
            ),
            notes=_rk("6d", "dict-in", "dict-in", "spell-book,hold-the-barrier") + "\n"
            "RQ2, the parallel item for 6d. Fails on (spec): a value -> True.",
        ),
        dict(
            type="mc",
            id="read-or-call",
            q="`moves` holds a function under the key `\"hop\"`. What is the difference between these two lines?",
            code=MOVES_HEAD + "\n" + MOVES_LINES,
            choices=[
                "The first is the function itself, and runs nothing. The second calls it, with `lucky`.",
                "Both lines run the function, so Lucky hops twice.",
                "The first makes Lucky hop. The second only reads what is stored under the key.",
                "The first is the text `\"hop\"`, the key's name. The second turns that text into a function.",
            ],
            answer=0,
            why_wrong={
                1: "Only the brackets on the end call a function. Without them, the line only reads what is stored.",
                2: "It is the other way round: the line with `(lucky)` on the end is the one that calls.",
                3: "`moves[\"hop\"]` is what is stored under the key: the function `hop` itself, not text.",
            },
            explain=(
                "`moves[\"hop\"]` reads the value under the key: the [[function as a value|function]] itself. Adding "
                "`(lucky)` calls it and hands it `lucky`, like `hop(lucky)`."
            ),
            notes=_rk("9a", "func-as-value,call-stored-func", "func-as-value", "spell-book,hold-the-barrier") + "\n"
            "RQ3, the parallel item for 9 (explain). Fails on (spec): 'both run the spell'.",
        ),
        dict(
            type="predict",
            id="what-go-does",
            q="What will this program print?",
            code=MOVES_PREDICT,
            choices=["Set.", "Lucky hops.\nSet.\nLucky hops.\nLucky hops.", "Set.\nLucky hops.\nLucky hops.",
                     "Set.\nLucky hops."],
            answer="Set.\nLucky hops.\nLucky hops.",
            explain=(
                "`go = moves[\"hop\"]` stores the function itself in `go`, and runs nothing. Then `Set.` prints. Each "
                "`go(lucky)` calls it once: two lines."
            ),
            notes=_rk("9b", "func-as-value,call-stored-func", "call-stored-func", "spell-book,hold-the-barrier") + "\n"
            "RQ4, the parallel item for 9 (predict): the function stored in a variable, then called twice. Fails on "
            "(spec): 'both run' (the store line taken to run it). Also the stored function never called, and two "
            "calls read as one.",
        ),
    ],
    notes=(
        "The re-check's questions, scored with rc-recheck: every task plus 3 of these 4 (questions_to_pass=3). The "
        "parallel items for 4a, 6d and 9 (explain, then predict), each new. No hints; read-aloud and glossary stay "
        "on. Right answers sit at varied positions (the site also shuffles)."
    ),
)


# The questions come first, as in forms A and B, so the first win is a prediction. rc-review lives in u10a.
ITEMS = [RC_PART1_C_QUESTIONS, RC_PART1_C, RC_RECHECK_QUESTIONS, RC_RECHECK]
