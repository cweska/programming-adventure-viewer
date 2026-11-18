"""Unit 6 "Loops", part a: Mar'tu remembers (5a-remembers), Lesson 5A "For Each, Yes?", Mar'tu remembers
(5b-remembers), Lesson 5B "While the Clock Ticks" and Quiz 5.

Spec: design/curriculum.md, "## Unit 6 · Loops", items 1 to 3 (5a-remembers; 5A-01 to 5A-08 and 5A-S;
5b-remembers; 5B-01 to 5B-04 and 5B-S; Quiz 5). Introduces node:For (5A-01), node:While (5B-01) and node:Break
(5B-03). Everything else comes from earlier units: `range()` and `len()` (Unit 4), `if` (Unit 2), `def` / `return`
(Unit 3), and from Unit 5 (planned concepts only, u05a-c): dictionary literals, reading by key, nested reads and a
list of dictionaries. No `continue`, comprehensions, `x if c else y` or `.items()` (u06b), no f-strings (Unit 9),
no `None` written in code (u07b): `None` only ever appears as printed output or in a message.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`for member in party.members:` at the bottom of the spell-book and mana-bars parts (already written for them),
`get_mana_bar(caster)`, the chalk wall's gaps and Mar'tu's "The decay is accelerating", and
`caster["mana"] = caster["mana"] - spell["mana_cost"]` in hold-the-barrier. Campaign links are "you've seen this,
now you'll get it". Every student has their own device; pair talk is optional and every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them): hints[0] Where to look (point), the middle hints
Teach me (a tiny example with other names), the last hint Show me how: the step's own line in backticks, whose
start up to its first `(` or `=` becomes Start me off (so that start is always in the solution). another_way, then
assemble (More structure), then Compare. In debug steps hints[0] is "Read Python's last line" (for a quiet bug:
what the program printed). Terminology (2.9): "variable" (Mar'tu may still say "box"), "recipe", "ingredient" and
"hands back" as in Unit 3; "gaps" and "shrink" for the chalk wall; "pass" for one time round a loop.

Check builders (one shared prelude, _PRE, then each check's own body; plain Python run in the student's namespace
after their code, every name starting with `_`, builtins taken from `builtins`):
  _rerun(values)  CMB / LOOP: the student's program again in a fresh namespace, with the FIRST top-level
                `name = <literal>` line of each named variable swapped for another value (another roster, another
                wall, another start). A roster the hidden setup makes (5A-03, 5A-07) is swapped after the setup
                runs. `_drop=(names)` leaves out the top-level lines that mention those names (5B-01 checks its
                countdown without the candles loop below it). Prints go to a private buffer. A rerun is guarded
                twice, so a loop that only never ends with the check's values cannot freeze the page: the
                buffer stops at 20,000 characters, and a line
                budget (sys.settrace, main.py frames only) stops it after 20,000 lines. Either one becomes the
                message "With other values, your loop never stopped".
  _case(None)   the student's own run as it is (no evidence bracket); _case(values) a rerun.
  _call(f, arg) calls a student recipe with a fresh sheet, guarded the same way, and keeps what it printed.
  _typed_for() / _quoted_for()  `for` loops over a typed list, or over the list's name in quotes (the loop
                walks the letters); `_quoted_msg(name)` names the task's own list, never the student's text.
  Messages follow the plain-language guide 4.3 (design/plain-language-guide.md): what happened, then the one thing
  to try, then the labelled evidence with no brackets, "Mar'tu tested your code with a test roster of 5 made-up
  heroes.", about 35 words or fewer. SOLO messages (solo-5a, solo-5b; explainer "lean") say what went wrong and
  keep the evidence, with no fix.
  Messages use invented values only (Tester, Pell, Brakka, Moss, Glug, Ivo) and never repeat a student's own text.

INFINITE LOOPS (read before 5B): the site gives a run 5 seconds (src/lib/languages/python/run.ts, then "Ran too
long") and stops a run that prints more than 200,000 characters (public/workers/course_helpers.py, TooMuchOutput,
then the "Printing forever?" explainer, which is always full, even for a lean SOLO). The harness gives a run 6
seconds. So every while loop a student can break in this file PRINTS inside its body: a missing update, an update
outside the loop, or an update that moves the wrong way prints forever and stops in milliseconds with
"TooMuchOutput: This program printed more than 200,000 characters, so it was stopped." That is the honest message
each such wrong answer proves (fails_at 0). No wrong answer here is a silent endless loop, so none waits for the
6-second timeout. There is no separate "step limit" on the site: the curriculum's "step-limit row" is these two
rows, and 5B-02's Learn pane and its "What the limit is" angle say so plainly.

The class's slips for this unit, each proven by a wrong_answers entry:
  the for line's colon (5A-01, 5A-02) or the body's indent (5A-01, 5A-02, 5A-08 CP1, 5B-03); printing the list,
  not the item (5A-01, 5A-02, 5A-03 `roster`, 5A-08 CP4, 5B-03); `total = 0` inside the loop (5A-04, 5A-08 CP3,
  Quiz 5 bug); the final print inside the loop (5A-04, 5B-01, 5B-02) or the filter's `if` outside it (5A-06);
  `for i in len(...)` ('int' object is not iterable, 5A-05) and the bare number (`for i in 6`, 5A-05); the item used
  as an index (5A-02 `chalk_wall[gap]`, 5A-03 `roster[hero]`, 5A-S `roster[member]`, the solo's bug); the list's
  name in quotes (5A-01, 5A-02, 5B-03); neighbors one past the end (5A-05 `[i + 1]`);
  `roster["name"]` for `member["name"]` (5A-03, 5A-08 CP2, 5A-S); a while loop with no update, the update outside
  the loop, or an update the wrong way (5B-02, 5B-S); `if` for `while` (5B-01, 5B-02) and `while` for `if` (5B-03);
  `break` in the wrong place (5B-03); values typed by hand (5A-02, 5A-03, 5A-04, 5A-05, 5A-06, 5A-07, 5A-08, 5B-01,
  5B-03); the example's list name copied (5A-02 `colors`, 5A-03 `jars`, 5A-04 `bag`, 5A-05 `marks`, 5B-03 the coin
  list).
  Check-breaker pass (adversarial review), each also proven by a wrong_answers entry: a loop over a typed copy of
  the list (`for gap in [48, 48, ...]:`, named by `_typed_for()` in 5A-01, 5A-02, 5A-03, 5A-04, 5A-06, 5A-08 CP4,
  5B-03); the loop deleted and every line typed (5A-01); the adding line below the loop, four sheets added by
  position, or `sum()` below the loop (5A-04, 5A-08 CP3: `_total_adds()`); 88 printed by hand (5A-04); a typed
  `range(1, 7)` (5A-05); the filter's print after the loop and the same typed name on every line (5A-06); the max
  typed into the recipe and the loop that builds the bar again without calling `mana_bar` (5A-07); the answer typed
  into the test, `if gap == 44:` (5B-03); the update above the print (5B-01, 5B-02, 5B-S); a `while` question
  flipped or bent to fit the wrong-way update (5B-S). Loosened so right answers pass: a label in front (`Gap: 48
  hours`, `Shrink: 1`, `Hours left: 5`, `First gap under 45: 44`), a trace print of each mana in 5A-04, an `else:`
  line for the rested heroes in 5A-06, a print inside the recipe in 5A-07, `Burst! Everyone inside!` or a line after
  the burst in 5B-01, and a `Done.` line after the loop in 5B-03.

Data: the real party table (Oogrish 9 / 18, Gearshift 10 / 20, Bomb Shell 12 / 24, Lucky 13 / 26: affinity, max
mana) and the real chalk wall 48, 48, 47, 46, 44, 41, 37. Full mana totals 88 (5A-04, Quiz 5). "After a night
holding the barrier" (5A-06, 5A-07, Quiz 5 Q6) the mana is Oogrish 6, Gearshift 14, Bomb Shell 3, Lucky 22.

Phone width: fenced pictures, examples, predict code and quiz code keep lines to 36 characters or fewer. Two
exceptions, both editor code, kept whole on one line because a wrapped list reads as two lists: the real wall
(`chalk_wall = [...]`, 41 characters) and a visible roster sheet (`{"name": "Bomb Shell", "mana": 24},`, up to 39
characters, one sheet per line). Two more, dictated by the teacher's ruling on the Unit 6 reviews and kept as
dictated: 5A-03's Example line (`print(jar["spice"] + ": " + str(jar["left"]))`, 49 characters: one glued text,
no comma) and 5A-07 CP2's Teach rung (the jar `return`, 60 characters, kept on one line as an inline code span,
which wraps on a phone: a fenced line over 36 characters fails content.test.ts). Quiz 5 keeps the wall short
as `wall = [...]` (35) and the night roster in setup.
campaign_link snippets are the campaign's own lines, as in Units 2-4.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u06a
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


_PRE = r'''import ast as _ast
import copy as _copy
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_len, _str, _int, _rng, _any, _all, _zip, _enum, _set = (_B.len, _B.str, _B.int, _B.range, _B.any, _B.all,
                                                         _B.zip, _B.enumerate, _B.set)
def _tn(_v):
    return _B.type(_v).__name__
_SETUP = __SETUP__
_FROM_SETUP = __FROM_SETUP__
_LIT = ('List', 'Dict', 'Constant', 'Tuple', 'UnaryOp')
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
def _sh(_v):
    _k = _tn(_v)
    if _k == 'str':
        return '"' + _v + '"'
    if _k in ('list', 'tuple'):
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    if _k == 'dict':
        return '{' + ', '.join([_sh(_a) + ': ' + _sh(_b) for _a, _b in _v.items()]) + '}'
    if _k == 'function':
        return 'a recipe'
    return _B.str(_v)
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
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
def _mentions(_n, _names):
    return _any(_tn(_x) == 'Name' and _x.id in _names for _x in _ast.walk(_n))
def _top_part(_t, _drop=()):
    # The top-level lines of the program, without the ones that mention a name in _drop (5B-01: the countdown
    # alone, without the candles loop below it).
    return [_n for _n in _t.body if not (_drop and _mentions(_n, _drop))]
def _rerun(_values=None, _drop=()):
    _t = _ast.parse(_source)
    _t.body = _top_part(_t, _drop)
    _vals = _B.dict(_values or {})
    _seen = []
    for _n in _t.body:
        if (_tn(_n) == 'Assign' and _B.len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id in _vals and _n.targets[0].id not in _seen and _tn(_n.value) in _LIT):
            _n.value = _lit(_vals[_n.targets[0].id], _n.value)
            _seen.append(_n.targets[0].id)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__'}
    _out = _sys.stdout
    _buf = _Cap()
    _err = ''
    _sys.stdout = _buf
    try:
        if _SETUP:
            _B.exec(_B.compile(_SETUP, '<setup>', 'exec'), _ns)
        for _k in _vals:
            if _k in _FROM_SETUP:
                _ns[_k] = _copy.deepcopy(_vals[_k])
        _code = _B.compile(_t, 'main.py', 'exec')
        _guarded(lambda: _B.exec(_code, _ns))
    except _Runaway as _e:
        _err = 'Runaway: ' + _B.str(_e)
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    _miss = [_k for _k in _vals if _k not in _seen and _k not in _FROM_SETUP]
    return _ns, _rows, _err, _miss
def _case(_vals):
    # None: the student's own run, as it is now (no evidence bracket).
    if _vals is None:
        return globals(), _lines(), '', []
    return _rerun(_vals)
def _call(_f, _arg):
    _out = _sys.stdout
    _buf = _Cap()
    _got, _err = None, ''
    _sys.stdout = _buf
    try:
        _got = _guarded(lambda: _f(_arg))
    except _Runaway as _e:
        _err = 'Runaway: ' + _B.str(_e)
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
    return _buf.getvalue(), _got, _err
def _keep(_name):
    return ("Mar'tu can't find a line that starts `" + _name + " = `. Keep that line the way it was at the start: "
            "he tests your code by changing it to other values.")
def _stop(_err, _ev, _fix='Make your code work for another roster too.'):
    if _err.startswith('Runaway'):
        return 'With other values, your loop never stopped. Make sure the loop can end, whatever the values.' + _ev
    return 'With other values, your code stopped with an error, ' + _err.split(':')[0] + '. ' + _fix + _ev
def _nums(_l):
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?!\d)(?!\.\d)', _l)]
def _parsed():
    return _ast.parse(_source)
def _typed_for():
    # `for x in [...]`: a loop over a list typed out in the code, so it never follows the task's own list.
    return [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'For' and _tn(_n.iter) in ('List', 'Tuple')]
def _quoted_for():
    # `for x in "spell_colors":`: the list's name in quotes, so the loop walks the letters of that text.
    return [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'For' and _tn(_n.iter) == 'Constant'
            and _tn(_n.iter.value) == 'str']
def _quoted_msg(_name):
    return ('Your `for` line has `' + _name + '` in quotes, so the loop walks its letters, one at a time. Take the '
            'quotes off `' + _name + '`. No quotes means look inside the list.')
def _total_adds(_name):
    # (inside, outside): non-literal assignments to `_name` inside a for loop, and at the top level.
    _t = _parsed()
    def _is_add(_n):
        if _tn(_n) == 'AugAssign':
            return _tn(_n.target) == 'Name' and _n.target.id == _name
        return (_tn(_n) == 'Assign' and _tn(_n.value) != 'Constant'
                and _any(_tn(_x) == 'Name' and _x.id == _name for _x in _n.targets))
    _in = [_n for _f in _ast.walk(_t) if _tn(_f) == 'For' for _n in _ast.walk(_f) if _is_add(_n)]
    _out = [_n for _n in _t.body if _is_add(_n)]
    return _in, _out
'''


def chk(label, body, setup="", from_setup=(), **subs):
    """A check: the shared _PRE (with this exercise's hidden setup), then `body` with each __NAME__ replaced by
    repr(value)."""
    pre = _PRE.replace("__SETUP__", repr(setup)).replace("__FROM_SETUP__", repr(tuple(from_setup)))
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    return (label, pre + body)


# ---------------------------------------------------------------------------------------------
# The data
# ---------------------------------------------------------------------------------------------

WALL = [48, 48, 47, 46, 44, 41, 37]
WALL_LINE = "chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"


def sheet(name, mana, max_mana=None, affinity=None):
    out = {"name": name, "mana": mana}
    if max_mana is not None:
        out["max_mana"] = max_mana
    if affinity is not None:
        out["abilities"] = {"magical_affinity": affinity}
    return out


def roster_code(sheets):
    """A visible roster, one sheet per line, name and mana only (up to 39 characters a line)."""
    lines = ["roster = ["] + ['    {"name": "%s", "mana": %d},' % (s["name"], s["mana"]) for s in sheets] + ["]"]
    return "\n".join(lines) + "\n"


def setup_roster(sheets, board=False):
    """Hidden setup: the prebuilt roster (2.12 rule 3), and the ley board recorder when asked for."""
    code = ""
    if board:
        code += (
            "_board = []\n"
            "def show_on_ley_board(text):\n"
            "    _board.append(text)\n"
            '    print("[Ley board] " + str(text))\n'
        )
    return code + "roster = " + repr(sheets) + "\n"


# The party at full mana (5A-03, 5A-04, 5A-08, 5A-S): 18 + 20 + 24 + 26 = 88.
FULL = [sheet("Oogrish", 18), sheet("Gearshift", 20), sheet("Bomb Shell", 24), sheet("Lucky", 26)]
FULL_SHEETS = [sheet("Oogrish", 18, 18, 9), sheet("Gearshift", 20, 20, 10), sheet("Bomb Shell", 24, 24, 12),
               sheet("Lucky", 26, 26, 13)]
# After a night holding the barrier (5A-06, 5A-07, Quiz 5).
NIGHT = [sheet("Oogrish", 6), sheet("Gearshift", 14), sheet("Bomb Shell", 3), sheet("Lucky", 22)]
NIGHT_SHEETS = [sheet("Oogrish", 6, 18, 9), sheet("Gearshift", 14, 20, 10), sheet("Bomb Shell", 3, 24, 12),
                sheet("Lucky", 22, 26, 13)]
# Five other heroes (invented names): the LOOP rerun. A program written for 4 lines cannot follow 5.
OTHER5 = [sheet("Pell", 31), sheet("Brakka", 7), sheet("Moss", 15), sheet("Glug", 3), sheet("Ivo", 9)]
OTHER_SHEETS = [sheet("Pell", 31, 34, 17), sheet("Brakka", 7, 12, 6), sheet("Moss", 15, 16, 8),
                sheet("Glug", 3, 10, 5), sheet("Ivo", 9, 22, 11)]

# The labelled evidence (plain-language guide 4.3.3), last in a message, with no brackets.
EV_FIVE = " Mar'tu tested your code with a test roster of 5 made-up heroes."


def ev_mana(values):
    return (" Mar'tu tested your code with test mana for the same heroes: " + ", ".join(str(v) for v in values[:-1])
            + " and " + str(values[-1]) + ".")


def ev_wall(wall):
    return " Mar'tu tested your code with a test wall, `chalk_wall = %s`." % (wall,)


def ev_box(name, value):
    return " Mar'tu tested your code with a test number, `%s = %s`." % (name, value)


# =============================================================================================
# UNIT (repeated in every part file of loops)
# =============================================================================================

UNIT = dict(
    id="loops",
    order=6,
    title="Loops",
    subtitle="Every Member of the Party",
    published=True,
    martu_intro=(
        "A loop runs the same lines once for each item in a list, so you write those lines only once. Read it "
        "like English: `for member in roster:` means *for each member of the roster, do the lines under me*.\n"
        "You've seen loops already: `for member in party.members:` at the bottom of the spell book and the mana "
        "bars. Somebody else wrote them for you. Now you'll write them yourself.\n"
        "Four heroes. Four bars to draw. Write it four times? No. Write it once, yes?"
    ),
    goals=[
        "Make Python repeat some lines once for each item in a list",
        "Do the same thing for every hero on a list: show each name, or draw each mana bar",
        "Add up every hero's mana into one total",
        "Pick out only some items, like the heroes who are low on mana",
        "Compare each gap on the chalk wall with the one before it, and see how fast the gaps shrink",
        "Repeat lines while something is true, fix a loop that never ends, and stop a loop early",
    ],
    campaign_links=["friends-in-low-places"],
)

# New terms only. Earlier units define list, index, range(), len(), indent, colon, block, recipe, return, pass...
GLOSSARY = [
    dict(
        term="for loop",
        aliases=["for loops", "loop", "loops"],
        plain=(
            "Lines that run once for each item in a list, like reading down a class list and calling out each "
            "name. Each time through, the name after `for` holds the next item."
        ),
        example="for snack in snacks:\n    print(snack)",
    ),
    dict(
        term="loop variable",
        aliases=["loop variables"],
        plain=(
            "The name right after `for`. You pick it. Each time through the loop, it holds the next item of the "
            "list, the way x takes each value in an input-output table in math class."
        ),
        example="for snack in snacks:",
    ),
    dict(
        term="running total",
        aliases=["running totals", "accumulator", "tally"],
        plain=(
            "A number that starts at 0 above a loop and grows on every pass. It's like adding up a column of "
            "numbers one at a time. If it is set to 0 inside the loop, it starts over every pass."
        ),
        example="total = 0\nfor coins in [3, 5]:\n    total = total + coins",
    ),
    dict(
        term="while loop",
        aliases=["while loops", "while"],
        plain=(
            "Repeats its lines while a question is `True`, like *stir while the soup is cold*. A line inside the "
            "loop must change something, so the question can turn `False`."
        ),
        example="while steps > 0:\n    steps = steps - 1",
    ),
    dict(
        term="infinite loop",
        aliases=["infinite loops", "endless loop", "a loop that never ends"],
        plain=(
            "A loop that never stops, because its question never turns `False`. It's like walking the wrong way "
            "on a number line: you never reach 0. The site stops it after a lot of printing, or after 5 seconds."
        ),
        example="while drops > 0:\n    print(drops)",
    ),
    dict(
        term="break",
        aliases=["break statement"],
        plain=(
            "Leaves a loop right away, like closing the dictionary once you find your word. Python goes on with "
            "the first line after the loop."
        ),
        example="if score > 90:\n    print(score)\n    break",
    ),
]


# =============================================================================================
# Mar'tu remembers... (5a-remembers)
# =============================================================================================

BOMB_CODE = (
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "abilities": {\n'
    '        "dexterity": 6,\n'
    '        "wisdom": 8,\n'
    "    },\n"
    "}\n"
    'abilities = bomb_shell["abilities"]\n'
    'print(abilities["wisdom"])\n'
)

REMEMBERS_5A = dict(
    kind="quiz",
    id="5a-remembers",
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from Units 5 and 3, before you start loops. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 5A. Q1 is the spec's Unit 5 nested read, "
        "`bomb_shell[\"abilities\"][\"wisdom\"]` (Bomb Shell's real wisdom, 8), read in two steps so every line fits "
        "the phone width (`print(bomb_shell[\"abilities\"][\"wisdom\"])` is 40 characters); the explain shows the "
        "one-line form. Q2 is the spec's Unit 3 def/return item (`return roll >= 12`, the campaign's strength "
        "check), the def/return item every warm-up carries from Unit 4 on. A miss shows the answer and a one-line "
        "why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="wisdom-inside",
            q="What will this print?",
            code=BOMB_CODE,
            choices=["6", "8", "{'dexterity': 6, 'wisdom': 8}", "KeyError: 'wisdom'"],
            answer="8",
            explain=(
                "`bomb_shell[\"abilities\"]` is the sheet inside the sheet. Then `[\"wisdom\"]` looks up wisdom "
                "in it: 8. In one line it is `bomb_shell[\"abilities\"][\"wisdom\"]`: the outside tag first."
            ),
        ),
        dict(
            type="predict",
            id="strength-check",
            q="What will this print?",
            code=(
                "def strength_check(roll):\n"
                "    required_roll = 12\n"
                "    return roll >= required_roll\n"
                "\n"
                "print(strength_check(12))\n"
            ),
            choices=["False", "12", "True", "None"],
            answer="True",
            explain=(
                "12 >= 12 is `True`: 12 counts, like the filled dot on a number line. The recipe hands back `True`, "
                "and `print` shows it. You saw this check at the trap door."
            ),
        ),
    ],
)

# =============================================================================================
# Lesson 5A "For Each, Yes?"
# =============================================================================================

# ---- 5A-01 predict-the-loop -------------------------------------------------------------------------------

COLORS_STARTER = (
    "spell_colors = [\n"
    '    "gold",\n'
    '    "fire orange",\n'
    '    "teal",\n'
    '    "silver",\n'
    "]\n"
    "for color in spell_colors:\n"
    "    print(color)\n"
)
COLORS_SOLUTION = COLORS_STARTER.replace('    "silver",\n', '    "silver",\n    "violet",\n')

COLORS_CHECK = chk(
    "a fifth color is in the list, and the loop prints all five",
    r'''
assert not _quoted_for(), _quoted_msg('spell_colors')
_w = globals().get('spell_colors')
assert _tn(_w) == 'list', ("Python can't find the list `spell_colors`. Put back the line that starts "
                           "`spell_colors = [`, the way it was at the start.")
_START = __START__
# A missing comma glues two colors into one: 4 items, and the last is `silver` with more stuck on.
assert not (_len(_w) == 4 and _tn(_w[-1]) == 'str' and _w[-1].startswith('silver') and _w[-1] != 'silver'), (
    'Two colors got glued into one, because a comma is missing. Check the commas: each color needs a comma '
    'after it.')
_rows = _lines()
if _w == _START:
    # A color printed on its own, below the loop, is not in the list (named without repeating it).
    _lone = [_a for _n in _parsed().body if _tn(_n) == 'Expr' and _tn(_n.value) == 'Call'
             and _tn(_n.value.func) == 'Name' and _n.value.func.id == 'print' for _a in _n.value.args
             if _tn(_a) == 'Constant' and _tn(_a.value) == 'str' and _a.value not in _w]
    assert not _lone, (
        'Your color has a `print` of its own, so it is not in the list. Put it inside the list instead, on the '
        'line after `"silver",`.')
    assert False, ('The list still holds the 4 colors it started with. Add your color on a new line inside the '
                   'list, after `"silver",`.')
assert _len(_w) == 5, ('The list holds ' + _str(_len(_w)) + ' colors. It should hold 5 colors: the 4 that were '
                       'there, then one of your own.')
assert _all(_tn(_c) == 'str' for _c in _w), ('One item in the list is not text. Put your color in quotes, like '
                                             '`"violet"`.')
assert _all(_c.strip() for _c in _w), 'One item has no letters between its quotes. Write a color there, like `"violet"`.'
assert not _any(_l.startswith('[') for _l in _rows), (
    'Each line shows the whole list, because the loop prints `spell_colors`. Print the loop variable, `color`, '
    'not the whole list.')
assert _len(_rows) == 5, (
    'Your program printed ' + _str(_len(_rows)) + ' lines, not 5. Keep `print(color)` indented under the `for` '
    'line, so it prints one line for each color.')
assert _all(_r.startswith(_c.strip()) for _r, _c in _zip(_rows, _w)), (
    'The lines in the Console are not the colors of the list, in order. Print `color`, the loop variable, so '
    'each pass prints its own color.')
assert _any(_tn(_n) == 'For' for _n in _ast.walk(_parsed())), (
    'Your program has no loop, only a `print` for each color. Put back the `for` loop, so one `print` line '
    'shows every color.')
assert not _typed_for(), ('Your `for` line walks a list you typed out, so it will not change when `spell_colors` '
                          'does. Loop over the list by its name: `for color in spell_colors:`.')
_ns, _rr, _err, _miss = _rerun({'spell_colors': __OTHER__})
_w2 = _ns.get('spell_colors')
assert not _err and _tn(_w2) == 'list' and [_r.split(' ')[0] for _r in _rr] == [_str(_c).split(' ')[0] for _c in _w2], (
    'With another list, your program printed the wrong lines. Keep `print(color)` inside the loop, so the loop '
    'prints the colors.' + __EV__)
''',
    START=["gold", "fire orange", "teal", "silver"],
    OTHER=["red", "blue", "green"],
    EV=" Mar'tu tested your code with a test list, `spell_colors = [\"red\", \"blue\", \"green\"]`.",
)

COLORS_BONUS = chk(
    "each line says the color, then light",
    r'''
_w = globals().get('spell_colors')
_rows = _lines()
assert _tn(_w) == 'list' and _rows == [_str(_c) + ' light' for _c in _w], (
    'Your lines do not end in ` light` yet. Glue it on, so each line reads like `gold light`: '
    '`print(color + " light")`.')
''',
)

PREDICT_THE_LOOP = dict(
    id="predict-the-loop",
    title="Predict the loop",
    martu=(
        "A [[for loop]] runs the same [[indent|indented]] lines once for each item in a list. Read it like "
        "English: `for color in spell_colors:` means *for each color in the list, do the lines under me*. A "
        "teacher calling roll does the same: for each name on the class list, say it out loud.\n"
        "`color` is the [[loop variable]]. Each time through the loop, it holds the next item:\n"
        "```text\npass 1: color is \"gold\"\npass 2: color is \"fire orange\"\npass 3: color is \"teal\"\n"
        "pass 4: color is \"silver\"\n```\n"
        "One time through the loop is called a *pass*. A line that says only `pass` means something else: *nothing "
        "here yet*. You'll replace those lines.\n"
        "The `for` line ends with a [[colon]], like an `if` line. Four colors, one `print` line, yes?"
    ),
    introduces=["node:For"],
    example='snacks = ["bread", "cheese"]\nfor snack in snacks:\n    print(snack)\n',
    example_output="bread\ncheese",
    names=["spell_colors", "color"],
    predict=dict(
        q="Before you press Run: what will this print?",
        choices=[
            "['gold', 'fire orange', 'teal', 'silver']",
            "gold\nfire orange\nteal\nsilver",
            "color\ncolor\ncolor\ncolor",
            "gold",
        ],
        answer=1,
        explain=(
            "One line for each item. On each pass, `color` holds the next color, and `print(color)` shows it. "
            "Four colors, four lines. `print` never shows the quotes."
        ),
    ),
    pair_talk=(
        "Pair talk: before you press Run, each of you says how many lines will show in the Console. Compare, then "
        "press Run."
    ),
    tracer=True,
    starter=COLORS_STARTER,
    checkpoints=[
        dict(
            id="add-violet",
            text=(
                "Add a fifth color to the list, in quotes, on a new line right after `\"silver\",`. Mar'tu would "
                "pick `\"violet\"`. Then press Run. You should see five colors in the Console."
            ),
            dictated=False,
            hints=[
                "Look at lines 1 to 6, the list. Each color sits on its own line, in quotes, with a comma after "
                "it. Where does a fifth color go?",
                "A new item goes inside the square brackets, in quotes, with a comma after it:\n```python\nsnacks = "
                "[\n    \"bread\",\n    \"cheese\",\n    \"plums\",\n]\n```\nThe loop finds the new item by itself. "
                "The `for` line stays as it is.",
                "Write `\"violet\",` (or a color of your own, in quotes) on the line after `\"silver\",`, with four "
                "spaces in front.",
            ],
            checks=[COLORS_CHECK],
            pass_line="One `print` line showed all five colors: the loop did the walking. Mar'tu: Yes!",
        ),
    ],
    solution=COLORS_SOLUTION,
    assemble=dict(
        lines=["spell_colors = [", '    "gold",', '    "fire orange",', '    "teal",', '    "silver",',
               '    "violet",', "]", "for color in spell_colors:", "    print(color)"],
        distractors=["    print(spell_colors)", "for color in spell_colors", 'print("violet")'],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="Down the line",
            text=(
                "Mar'tu walks down the line of heroes and taps each one on the shoulder: gold, fire orange, teal, "
                "silver. The same tap, once for each hero. The loop is the walk, and `print(color)` is the tap."
            ),
        ),
        dict(
            angle="picture",
            label="A finger on the list",
            text=(
                "```text\n[gold] [fire orange] [teal] [silver]\n  ^\n  color\n```\n"
                "Your finger starts on the first item. Each pass, it moves one item along. When it runs out of "
                "items, the loop is done."
            ),
        ),
        dict(
            angle="step-by-step",
            label="The loop table",
            text=(
                "```text\npass  color          prints\n1     \"gold\"         gold\n2     \"fire orange\"  "
                "fire orange\n3     \"teal\"         teal\n4     \"silver\"       silver\n```\n"
                "It's like an input-output table in math class: one row for each item. Add a fifth color, and the "
                "table gets a fifth row by itself."
            ),
        ),
        dict(angle="shorter", text="`for color in spell_colors:` means: for each color in the list, do the indented lines."),
    ],
    bonus=dict(
        by="lucky",
        title="Light show",
        text=(
            "Lucky wants a light show. Change `print(color)` so each line shows the color, then the word `light`, "
            "like `gold light`."
        ),
        hints=[
            "`+` glues text, like a compound word: `snack + \" pie\"` gives `bread pie`. The space goes inside the "
            "quotes.",
            "Write `print(color + \" light\")` in place of `print(color)`.",
        ],
        checks=[COLORS_BONUS],
        solution=COLORS_SOLUTION.replace("    print(color)\n", '    print(color + " light")\n'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet='for member in party.members:\n    add_spell(member["spell_book"], "Strengthen Magic", 10, 8, strengthen_magic)',
        why=(
            "You've seen this loop at the bottom of the spell book, already written for you. Now you'll get it. It "
            "has today's parts: `for`, a name, `in`, a list, a colon, then an indented line that runs once for "
            "each member."
        ),
    ),
    takeaway="`for item in items:` runs the indented lines once for each item, in order.",
    wrong_answers=[
        dict(why="the starter: only four colors", code=COLORS_STARTER, fails_at=1,
             message_contains="Add your color on a new line"),
        dict(why="the quoted list name: the loop walks the letters of the text spell_colors",
             code=COLORS_SOLUTION.replace("for color in spell_colors:", 'for color in "spell_colors":'), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="no comma after silver: Python glues silverviolet",
             code=COLORS_STARTER.replace('    "silver",\n', '    "silver"\n    "violet",\n'), fails_at=1,
             message_contains="Check the commas"),
        dict(why="no comma after silver, before a color of the student's own: Python glues them",
             code=COLORS_STARTER.replace('    "silver",\n', '    "silver"\n    "sea green",\n'), fails_at=1,
             message_contains="Check the commas"),
        dict(why="the color typed without quotes (NameError)",
             code=COLORS_STARTER.replace('    "silver",\n', '    "silver",\n    violet,\n'), fails_at=0,
             message_contains="is not defined"),
        dict(why="a number for the fifth color, not text",
             code=COLORS_STARTER.replace('    "silver",\n', '    "silver",\n    5,\n'), fails_at=1,
             message_contains="in quotes"),
        dict(why="violet printed on its own after the loop, not put in the list",
             code=COLORS_STARTER + 'print("violet")\n', fails_at=1, message_contains="inside the list"),
        dict(why="the whole list printed each pass (the list, not the item)",
             code=COLORS_SOLUTION.replace("    print(color)\n", "    print(spell_colors)\n"), fails_at=1,
             message_contains="not the whole list"),
        dict(why="a sixth color too", code=COLORS_SOLUTION.replace('    "violet",\n', '    "violet",\n    "pink",\n'),
             fails_at=1, message_contains="5 colors"),
        dict(why="violet printed twice: in the list and again after the loop",
             code=COLORS_SOLUTION + 'print("violet")\n', fails_at=1, message_contains="printed 6"),
        dict(why="the print line not indented under the for line",
             code=COLORS_SOLUTION.replace("    print(color)\n", "print(color)\n"), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="the for line without its colon",
             code=COLORS_SOLUTION.replace("for color in spell_colors:", "for color in spell_colors"), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the loop deleted: five typed prints, violet in the list (the output matches)",
             code=COLORS_SOLUTION.replace("for color in spell_colors:\n    print(color)\n", "").replace(
                 "]\n", ']\nprint("gold")\nprint("fire orange")\nprint("teal")\nprint("silver")\nprint("violet")\n'),
             fails_at=1, message_contains="no loop"),
        dict(why="the loop runs over a typed copy of the list, not spell_colors (the output matches)",
             code=COLORS_SOLUTION.replace(
                 "for color in spell_colors:",
                 'for color in ["gold", "fire orange", "teal", "silver", "violet"]:'),
             fails_at=1, message_contains="by its name"),
        dict(why="the first color every pass (spell_colors[0] for color)",
             code=COLORS_SOLUTION.replace("    print(color)\n", "    print(spell_colors[0])\n"), fails_at=1,
             message_contains="its own color"),
        dict(why="the loop kept but empty, the five colors typed in prints after it",
             code=COLORS_SOLUTION.replace("    print(color)\n", "    pass\n")
             + 'print("gold")\nprint("fire orange")\nprint("teal")\nprint("silver")\nprint("violet")\n',
             fails_at=1, message_contains="With another list"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="for-each", solo="false", dictates="",
             foreign_names="snacks,snack", stages="P,R,I,M", trace="static loop table (Learn pane, open by default)")
        + "\n"
        "5A-01. Intro node:For. Predict (the four colors, one per line) before Run; the loop table is in the Learn "
        "pane (open by default) and again as the step-by-step angle. The Learn text separates a *pass* (one time "
        "round) from a `pass` line (nothing here yet). CP1 [ND] (teacher ruling on the Unit 6 reviews): a fifth "
        "color of the student's own, in quotes; Mar'tu's is \"violet\" (the solution). The list is written "
        "one color per line (phone width: the spec's one-line `for color in [...]` is 56 characters), which also "
        "makes the new item a one-line edit. Checks: first, a quoted list name (`for color in \"spell_colors\":`, "
        "`_quoted_for()`); then any non-empty text as the fifth item passes, capitals included. A missing comma "
        "after silver (4 items, the last `silver` with more glued on) is named without repeating the student's "
        "text (2.11), and so is a color printed on its own below the loop. The loop prints exactly five lines "
        "in list order (`print(spell_colors)` is caught). The loop must stay, over `spell_colors` itself "
        "(five typed prints, or a typed copy of the list in the `for` line, are named), and a rerun with "
        "`[\"red\", \"blue\", \"green\"]` proves the print follows the list. Lucky's side quest (combining loop + glue) keeps "
        "the step green, because each line still starts with its color. Pair talk: predict-and-compare."
    ),
)

# ---- 5A-02 each-mark ---------------------------------------------------------------------------------------

MARK_STARTER = WALL_LINE + "for ___ in chalk_wall:\n    # Print it as \"48 hours\".\n    pass\n"


def _mark(head="for gap in chalk_wall:", body='    print(gap, "hours")', tail=""):
    return WALL_LINE + head + "\n    # Print it as \"48 hours\".\n" + body + "\n" + tail


MARK_SOLUTION = _mark()

EVERY_GAP = chk(
    "every gap prints as hours, and the loop follows the wall",
    r'''
assert not _quoted_for(), _quoted_msg('chalk_wall')
_t0 = _parsed()
_blank = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For' and _tn(_n.target) == 'Name' and _n.target.id == '___']
assert not _blank, ('Line 2 still has `___` where the loop variable goes. Put a name of your own in place of '
                    '`___`, like `gap`, and print that name.')
for _vals, _ev in ((None, ''), ({'chalk_wall': __W3__}, __EV3__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_err, _ev, 'Make your code work for another wall too.')
    _wall = _ns.get('chalk_wall')
    assert _tn(_wall) == 'list', _keep('chalk_wall')
    _want = [_str(_g) + ' hours' for _g in _wall]
    # Only the lines that mention hours: a heading of the student's own is fine, and so is a label in front
    # (`Gap: 48 hours`), as long as each line ends with `<gap> hours`.
    _got = [_l.rstrip('.!') for _l in _rows if 'hour' in _l.lower()]
    if _len(_got) == _len(_want) and _all(_g == _w or (_len(_g) > _len(_w) + 1 and _g.endswith(' ' + _w)
                                                            and _g[-_len(_w) - 2] not in '-.0123456789')
                                         for _g, _w in _zip(_got, _want)):
        continue
    assert _rows, ('Nothing printed. Put a `print(...)` line in place of `pass`, with four spaces in front, so it '
                   'runs inside the loop.')
    assert not _any('[' in _l for _l in _rows), ('Each line shows the whole wall, because the loop prints '
                                                 '`chalk_wall`. Print the loop variable instead.' + _ev)
    assert not (_vals is not None and _typed_for()), (
        'Your `for` line walks a list you typed out, so it will not change when the wall does. Loop over the wall '
        'by its name: `for gap in chalk_wall:`.' + _ev)
    assert not (_vals is not None and _len(_rows) == 7), (
        'With 3 gaps on the wall, your program still printed 7 lines. Let the loop do the printing: one `print` '
        'line, indented under the `for` line.' + _ev)
    assert _len(_rows) != 1, ('Your `print` line is not indented under the `for` line. It ran once. Indent it 4 '
                              'spaces, so it runs for every gap.' + _ev)
    assert not _all(_re.fullmatch(r'-?\d+', _l) for _l in _rows), ('Each line shows only the gap. Add the word hours '
                                                                    'after it, like `48 hours`.')
    assert not _any(_re.fullmatch(r'-?\d+hours[.!]?', _l) for _l in _rows), (
        'The gap and `hours` touch, with no space between them. Put a space there, like `48 hours`: a comma inside '
        '`print` adds one for you.')
    assert _any(_re.search(r'\d', _l) for _l in _rows), (
        'Your lines show no numbers, because the loop variable is in quotes. Take the quotes off the loop variable. '
        'Quotes mean these exact letters. No quotes means look inside the box with this label.')
    assert not (_len(_rows) > 1 and _len(_set(_rows)) == 1), (
        'Every line shows the same gap. Print the loop variable, so each pass shows its own gap.' + _ev)
    assert 'hours' not in [_l.lower() for _l in _rows], (
        'The gap and `hours` each went on a line of their own. Put them in one `print`, with a comma between them.')
    assert False, ('Your lines do not match `48 hours`, one line for each gap. Print each gap with `hours` after '
                   'it.' + _ev)
''',
    W3=[40, 36, 31],
    EV3=ev_wall([40, 36, 31]),
)

MARK_BONUS = chk(
    "gaps under 45 get a !, and the rest do not",
    r'''
for _vals, _ev in ((None, ''), ({'chalk_wall': [46, 44, 40]}, " Mar'tu tested your code with a test wall, `chalk_wall = [46, 44, 40]`.")):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev, 'Make your code work for another wall too.')
    _wall = _ns.get('chalk_wall')
    _want = [_str(_g) + ' hours' + ('!' if _g < 45 else '') for _g in _wall]
    assert [_l.rstrip('.') for _l in _rows] == _want, (
        'Only the gaps under 45 should get a `!`. Inside the loop, use `if gap < 45:` for the line with `!`, and '
        '`else:` for the plain line.' + _ev)
''',
)

EACH_MARK = dict(
    id="each-mark",
    title="Each mark on the wall",
    martu=(
        "You make up the [[loop variable]]'s name. It's like the x in an input-output table in math class: call "
        "it n or t, and the table still works. `for gap in chalk_wall:` and `for mark in chalk_wall:` do the same "
        "thing, as long as you use the same name inside the loop.\n"
        "My rule: *a name you make up is yours. A name the task gives you is a promise.* `chalk_wall` is a "
        "promise: the task gave you that name, so keep it exactly.\n"
        "A *gap* is the hours between two bursts, the blasts from the leylines. My chalk wall lists the gaps, "
        "oldest first."
    ),
    example='colors = ["gold", "teal"]\nfor color in colors:\n    print(color, "light")\n',
    example_output="gold light\nteal light",
    names=["chalk_wall"],
    pick="# Mar'tu's pick for the name: gap",
    starter=MARK_STARTER,
    checkpoints=[
        dict(
            id="every-gap",
            text=(
                "Two spots to fill:\n"
                "1. On line 2, replace `___` with a loop variable name of your own, like `gap`.\n"
                "2. On line 4, replace `pass` with a `print` that shows that name, then `hours`, like `48 hours`."
            ),
            dictated=False,
            hints=[
                "Look at line 2 and line 4. `___` needs a name, and `pass` needs a `print`. Do both use the same "
                "name?",
                "A comma inside `print` puts a space between two values:\n```python\nfor color in colors:\n"
                "    print(color, \"light\")\n```\nThat shows `gold light`, then `teal light`.",
                "Write `print(gap, \"hours\")` in place of `pass`, and `gap` in place of `___`.",
            ],
            checks=[EVERY_GAP],
            pass_line="One `print` line showed all seven gaps on the wall. Oogrish: Steady, now.",
        ),
    ],
    solution=MARK_SOLUTION,
    assemble=dict(
        lines=[WALL_LINE.strip(), "for gap in chalk_wall:", '    print(gap, "hours")'],
        distractors=['    print(chalk_wall, "hours")', '    print(gap + " hours")', "for gap in chalk_wall"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A sticky note",
            text=(
                "```text\n48  48  47  46  44  41  37\n^\ngap\n```\n"
                "`gap` is a sticky note. Each pass, Python moves it to the next mark. You wrote the name on the "
                "note, so you can pick any name."
            ),
        ),
        dict(
            angle="everyday",
            label="Your name, their name",
            text=(
                "You can name your pet anything you like: that name is yours. Your school's name isn't yours to "
                "change, because other people use it. The loop variable is your pet. `chalk_wall` is the school."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Python takes the first gap, 48, and puts it in your loop variable.\n"
                "2. It runs the indented line: `48 hours`.\n"
                "3. Next gap, 48 again. Then 47. Seven gaps, seven lines.\n"
                "4. No gaps left, so the loop ends."
            ),
        ),
        dict(angle="shorter", text="Pick a name after `for`. Print that name, then `\"hours\"`."),
    ],
    bonus=dict(
        by="lucky",
        title="Danger marks",
        text=(
            "Lucky wants the scary gaps marked. Keep every gap printing, and add `!` only to the gaps under 45, "
            "like `44 hours!`."
        ),
        hints=[
            "Put an `if` and an `else:` inside the loop. The `!` line goes under the `if`, and the plain line goes "
            "under `else:`. Lines inside them get 8 spaces.",
            "Write `if gap < 45:` inside the loop, then `print(gap, \"hours!\")` under it, and the plain line under "
            "`else:`.",
        ],
        checks=[MARK_BONUS],
        solution=_mark(body='    if gap < 45:\n        print(gap, "hours!")\n    else:\n        print(gap, "hours")'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "In the campaign, Oogrish ran a finger down this column: *every forty-eight hours, at first.* Your loop "
            "is that finger. Your loop variable holds each number, one at a time."
        ),
    ),
    takeaway="You pick the loop variable's name. The list's name is a promise: keep it exactly.",
    wrong_answers=[
        dict(why="the starter: ___ kept, nothing printed", code=MARK_STARTER, fails_at=1, message_contains="name of your own"),
        dict(why="seven separate print lines (the loop not used)",
             code=WALL_LINE + "".join(f'print({g}, "hours")\n' for g in WALL), fails_at=1, message_contains="3 gaps"),
        dict(why="the whole list printed each pass", code=_mark(body='    print(chalk_wall, "hours")'), fails_at=1,
             message_contains="whole wall"),
        dict(why="the print after the loop, not indented: it runs once",
             code=_mark(body="    pass", tail='print(gap, "hours")\n'), fails_at=1, message_contains="It ran once"),
        dict(why="the loop variable in quotes", code=_mark(body='    print("gap", "hours")'), fails_at=1,
             message_contains="Take the quotes off the loop variable"),
        dict(why="the quoted list name: the loop walks the letters of the text chalk_wall",
             code=_mark(head='for gap in "chalk_wall":'), fails_at=1, message_contains="Take the quotes off `chalk_wall`"),
        dict(why="no word hours", code=_mark(body="    print(gap)"), fails_at=1, message_contains="word hours"),
        dict(why="no space before hours", code=_mark(body='    print(str(gap) + "hours")'), fails_at=1,
             message_contains="space"),
        dict(why="the first gap every pass", code=_mark(body='    print(chalk_wall[0], "hours")'), fails_at=1,
             message_contains="same gap"),
        dict(why="___ kept as the name and printed", code=_mark(head="for ___ in chalk_wall:", body='    print(___, "hours")'),
             fails_at=1, message_contains="name of your own"),
        dict(why="the for line without its colon", code=_mark(head="for gap in chalk_wall"), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the body not indented", code=_mark(body='print(gap, "hours")'), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="a number glued to text with + (no str())", code=_mark(body='    print(gap + " hours")'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the item used as an index", code=_mark(body='    print(chalk_wall[gap], "hours")'), fails_at=0,
             message_contains="out of range"),
        dict(why="the example's list name copied", code=_mark(head="for color in colors:", body='    print(color, "hours")'),
             fails_at=0, message_contains="'colors' is not defined"),
        dict(why="the values typed by hand: the loop runs over a typed copy of the wall",
             code=_mark(head="for gap in [48, 48, 47, 46, 44, 41, 37]:"), fails_at=1, message_contains="by its name"),
        dict(why="the gap and the word in two prints: each on a line of its own",
             code=_mark(body='    print(gap)\n    print("hours")'), fails_at=1, message_contains="in one `print`"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="for-each", solo="false", dictates="",
             foreign_names="colors,color") + "\n"
        "5A-02. The naming rule (G2 R24) is the Learn text, word for word. CP1 [ND]: every gap as `<gap> hours`; a "
        "trailing `.` or `!` is allowed (so Lucky's side quest keeps the step green), and so is a label in front "
        "(`Gap: 48 hours`). LOOP: a rerun with the 3-gap "
        "wall [40, 36, 31], so seven typed prints fail with '3 gaps' (spec WA). The Example's loop variable "
        "(`color`) is fine, as the spec says; only its LIST name (`colors`) is a NameError (WA). The check's first "
        "line names a quoted list name, `for gap in \"chalk_wall\":` (`_quoted_for()`: the loop walks the "
        "letters), so 'Take the quotes off the loop variable' only meets `print(\"gap\", ...)`, the case it was "
        "written for. Lucky's side quest says to keep every gap printing, and its first rung puts the `if` and "
        "`else:` inside the loop (the old text read as 'print only the ones under 45'). `___` itself is a "
        "legal Python name, so a check asks for a name of the student's own. The starter's `pass` keeps it valid "
        "Python (a `for` with only a comment is a SyntaxError). Mar'tu's pick is a note (`gap`)."
    ),
)

# ---- 5A-03 each-member -------------------------------------------------------------------------------------

MEMBER_SETUP = setup_roster(FULL_SHEETS, board=True)
MEMBER_HEAD = (
    "# roster holds 4 hero sheets.\n"
    "# roster[0][\"name\"] is \"Oogrish\"\n"
    "# roster[0][\"mana\"] is 18\n"
    "for member in roster:\n"
    "    # Show \"Oogrish: 18\" and so on\n"
    "    # on the ley board.\n"
)
MEMBER_STARTER = MEMBER_HEAD + "    pass\n"
MEMBER_LINE = '    line = member["name"] + ": " + str(member["mana"])\n    show_on_ley_board(line)'


def _member(body=MEMBER_LINE, head=MEMBER_HEAD, tail=""):
    return head + body + "\n" + tail


MEMBER_SOLUTION = _member()

BOARD_EACH = chk(
    "the ley board shows each member's name and mana, in order",
    r'''
_b = globals().get('_board')
assert _tn(_b) == 'list', ('The ley board stopped working, because your code made a variable named `_board`. '
                           'Pick another name for it.')
_want = [(_m['name'], _m['mana']) for _m in __SHEETS__]
_names = [_n for _n, _x in _want]
_rows = [_l for _l in _lines() if not _l.startswith('[Ley board]')]
if not _b:
    assert not _any(_n in _l for _l in _rows for _n in _names), (
        'The ley board stayed empty, because your lines went to `print`. Show each line with '
        '`show_on_ley_board(...)`, not `print`.')
    assert False, ('Nothing reached the ley board. Call `show_on_ley_board(...)` inside the loop, with four spaces '
                   'in front.')
assert not _any(_tn(_t) == 'dict' for _t in _b), (
    'The board shows a whole sheet, curly braces and all. Show only the name and the mana: build the text from '
    '`member["name"]` and `member["mana"]`.')
assert not _any(_tn(_t) == 'list' for _t in _b), (
    'The board shows the whole roster on each line. Show one member at a time: use `member`, not `roster`.')
assert _len(_b) != 1, ('Your `show_on_ley_board` line is not indented under the `for` line. It ran once. Indent it '
                       '4 spaces, so it runs for every member.')
_texts = [_str(_t) for _t in _b]
assert not (_len(_set(_texts)) == 1), ('Every line on the board is the same. Read each sheet through `member`, the '
                                       'loop variable, so each pass shows its own hero.')
assert _len(_texts) == 4, ('The board got ' + _str(_len(_texts)) + ' lines for 4 members. Show one line for each '
                           'member.')
for (_n, _m), _t in _zip(_want, _texts):
    if _t.startswith(_n + ': ') and _nums(_t)[:1] == [_m]:
        continue
    _first = [_x for _x in _names if _t.startswith(_x)]
    assert _first, ("A line on the board does not start with a hero's name. Start each line with "
                    "`member[\"name\"]`, then `: ` and the mana, like `Oogrish: 18`.")
    assert _first[0] == _n, ('A typed name stays the same on every pass. Read each name from `member`, so it '
                             'changes every pass.')
    assert _t.startswith(_n + ': '), ('After the name, the line needs `: `. Glue it on with `+`: '
                                      '`member["name"] + ": "`. The ley board takes one piece of text, so a comma '
                                      "won't work.")
    assert False, 'After the name and `: `, the line needs the mana. Add `member["mana"]`, like `Oogrish: 18`.'
''',
    SHEETS=FULL_SHEETS,
)

BOARD_FIVE = chk(
    "the loop follows a roster of 5",
    r'''
_ns, _rows, _err, _miss = _rerun({'roster': __OTHER__})
assert not _err, _stop(_err, __EV__)
_b = _ns.get('_board') or []
_want = [(_m['name'], _m['mana']) for _m in __OTHER__]
_texts = [_str(_t) for _t in _b]
_ok = _len(_texts) == _len(_want) and _all(_t.startswith(_n + ': ') and _nums(_t)[:1] == [_m]
                                           for (_n, _m), _t in _zip(_want, _texts))
if not _ok:
    assert not _typed_for(), ('Your `for` line walks a list you typed out, and a list you typed stays the same '
                              'when the roster changes. Loop over the sheets themselves: `for member in roster:`.'
                              + __EV__)
    assert _len(_texts) != 4, ('With 5 heroes in `roster`, the board showed 4 lines. Let the loop make the calls: '
                               'one `show_on_ley_board` line inside it.' + __EV__)
    assert False, ('With another roster, the board showed the wrong lines. Build each line from `member`, so it '
                   'works for any roster: `member["name"]`, then `: `, then the mana.' + __EV__)
''',
    setup=MEMBER_SETUP,
    from_setup=("roster",),
    OTHER=OTHER_SHEETS,
    EV=EV_FIVE,
)

MEMBER_BONUS = chk(
    "each line shows the affinity too",
    r'''
for _vals, _ev in ((None, ''), ({'roster': __OTHER__}, __EV__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev)
    _b = [_str(_t) for _t in (_ns.get('_board') or [])]
    _r = _ns['roster']
    assert _len(_b) == _len(_r) and _all(_nums(_t)[1:2] == [_m['abilities']['magical_affinity']]
                                         for _t, _m in _zip(_b, _r)), (
        "The board does not show each hero's affinity after the mana yet. Add it: "
        '`str(member["abilities"]["magical_affinity"])`, like `Oogrish: 18, affinity 9`.' + _ev)
''',
    setup=MEMBER_SETUP,
    from_setup=("roster",),
    OTHER=OTHER_SHEETS,
    EV=EV_FIVE,
)

EACH_MEMBER = dict(
    id="each-member",
    title="Each member of the party",
    martu=(
        "A *roster* is a list of sheets (dictionaries), one sheet for each hero. A loop over it hands you one "
        "sheet each pass, like reading a class roster one student's row at a time. `for member in roster:` puts "
        "the first sheet in `member`, runs the indented lines, then moves on to the next sheet.\n"
        "Inside the loop, read the sheet through `member`: `member[\"name\"]`, and `member[\"mana\"]` for the "
        "hero's mana, their magic power. Not `roster[\"name\"]`: `roster` is the whole list, and a list has "
        "positions, not tags (keys).\n"
        "The *ley board* is my board on the wall. `show_on_ley_board(line)` shows one piece of text there, so "
        "glue the parts together with `+` first, yes?"
    ),
    example=(
        "jars = [\n"
        '    {"spice": "salt", "left": 3},\n'
        '    {"spice": "sage", "left": 2},\n'
        "]\n"
        "for jar in jars:\n"
        '    print(jar["spice"] + ": " + str(jar["left"]))\n'
    ),
    example_output="salt: 3\nsage: 2",
    setup=MEMBER_SETUP,
    names=["roster", "member", "show_on_ley_board"],
    pair_talk=(
        "Pair talk: point at `member` and tell your partner which sheet it holds on the second pass. Then each of "
        "you writes the loop."
    ),
    starter=MEMBER_STARTER,
    checkpoints=[
        dict(
            id="show-each-member",
            text=(
                "Replace `pass` on line 7 with lines that show each hero as `<name>: <mana>` on the ley board, like "
                "`Oogrish: 18`. Use `show_on_ley_board(...)`, not `print`."
            ),
            dictated=False,
            hints=[
                "Look at line 7, `pass`. Inside the loop, `member` holds one sheet. Which two tags do you read "
                "from it, and how do you join them into one piece of text?",
                "With other names:\n```python\nfor jar in jars:\n    label = jar[\"spice\"] + \": \"\n"
                "    print(label + str(jar[\"left\"]))\n```\nA number needs `str()` before you glue it to text.",
                "Write `line = member[\"name\"] + \": \" + str(member[\"mana\"])` in place of `pass`, then "
                "`show_on_ley_board(line)` under it, with four spaces in front of each.",
            ],
            checks=[BOARD_EACH, BOARD_FIVE],
            pass_line="The ley board shows all four heroes, one line each. Gearshift: Visor dims. Barrier's holding.",
        ),
    ],
    solution=MEMBER_SOLUTION,
    assemble=dict(
        lines=["for member in roster:"] + MEMBER_LINE.split("\n"),
        distractors=['    line = roster["name"] + ": " + str(member["mana"])', "    show_on_ley_board(member)",
                     "for member in roster"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Trace table",
            text=(
                "```text\npass  member[\"name\"]  board\n1     \"Oogrish\"     Oogrish: 18\n"
                "2     \"Gearshift\"   Gearshift: 20\n3     \"Bomb Shell\"  Bomb Shell: 24\n"
                "4     \"Lucky\"       Lucky: 26\n```\n"
                "`member` is a different sheet on every pass, so the same line shows a different hero."
            ),
        ),
        dict(
            angle="picture",
            label="A stack of cards",
            text=(
                "The roster is a stack of four cards, one card for each hero. Each pass, Python hands you the next "
                "card and calls it `member`. You read the card in your hand, never the whole stack."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "At the bottom of the mana bars: `for member in party.members:` then `show_mana(member)`. "
                "`party.members` was the roster, and `member` held each sheet, one at a time."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's affinity",
        text=(
            "Lucky wants each hero's affinity, how strong their magic is, on the board too. Show it after the mana, "
            "like `Oogrish: 18, affinity 9`."
        ),
        hints=[
            "The affinity sits on the sheet inside the sheet, under `\"abilities\"`. Read the outside tag first, "
            "then the inside one.",
            "Add `+ \", affinity \" + str(member[\"abilities\"][\"magical_affinity\"])` at the end of the text.",
        ],
        checks=[MEMBER_BONUS],
        solution=_member(
            body='    line = member["name"] + ": " + str(member["mana"]) + ", affinity " '
                 '+ str(member["abilities"]["magical_affinity"])\n    show_on_ley_board(line)'
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="for member in party.members:\n    show_mana(member)",
        why=(
            "You've seen this at the bottom of the mana bars. `party.members` was the roster, and "
            "`show_mana(member)` ran once for each sheet. Now you'll get it: your loop does the same with "
            "`show_on_ley_board`."
        ),
    ),
    takeaway="Inside `for member in roster:`, read each sheet through `member`: `member[\"name\"]`.",
    wrong_answers=[
        dict(why="the starter: pass, nothing on the board", code=MEMBER_STARTER, fails_at=1, message_contains="Nothing reached"),
        dict(why="roster[\"name\"] for member[\"name\"] (TypeError)",
             code=_member('    show_on_ley_board(roster["name"] + ": " + str(member["mana"]))'), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="the whole roster shown each pass (roster where member belongs)",
             code=_member("    show_on_ley_board(roster)"), fails_at=1, message_contains="whole roster"),
        dict(why="the whole sheet shown", code=_member("    show_on_ley_board(member)"), fails_at=1,
             message_contains="whole sheet"),
        dict(why="print instead of the ley board", code=_member('    print(member["name"] + ": " + str(member["mana"]))'),
             fails_at=1, message_contains="not `print`"),
        dict(why="four typed calls, no loop (CALL passes, LOOP fails)",
             code="".join(f'show_on_ley_board("{s["name"]}: {s["mana"]}")\n' for s in FULL), fails_at=1,
             message_contains="5 heroes"),
        dict(why="the call after the loop, not indented: it runs once",
             code=_member("    pass", tail='show_on_ley_board(member["name"] + ": " + str(member["mana"]))\n'),
             fails_at=1, message_contains="It ran once"),
        dict(why="the first sheet every pass (roster[0])",
             code=_member('    show_on_ley_board(roster[0]["name"] + ": " + str(roster[0]["mana"]))'), fails_at=1,
             message_contains="same"),
        dict(why="the name typed by hand", code=_member('    show_on_ley_board("Oogrish: " + str(member["mana"]))'),
             fails_at=1, message_contains="typed name"),
        dict(why="no colon after the name", code=_member('    show_on_ley_board(member["name"] + " " + str(member["mana"]))'),
             fails_at=1, message_contains="Glue"),
        dict(why="a comma, as in print: the ley board takes one text (TypeError)",
             code=_member('    show_on_ley_board(member["name"], member["mana"])'), fails_at=0,
             message_contains="takes 1 positional argument"),
        dict(why="the name alone on the board: no colon, no mana",
             code=_member('    show_on_ley_board(member["name"])'), fails_at=1, message_contains="Glue"),
        dict(why="the two-line form with the list's key read through roster (TypeError)",
             code=_member('    line = roster["name"] + ": " + str(member["mana"])\n    show_on_ley_board(line)'),
             fails_at=0, message_contains="list indices must be integers"),
        dict(why="mana glued without str() (TypeError)",
             code=_member('    show_on_ley_board(member["name"] + ": " + member["mana"])'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="the item used as an index (roster[hero])",
             code=_member('    show_on_ley_board(roster[member]["name"])'), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="the list's name in quotes: the loop walks the letters of the text roster (TypeError)",
             code=_member(head=MEMBER_HEAD.replace("in roster:", 'in "roster":')), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="the example's list name copied",
             code=_member('    show_on_ley_board(jar["spice"])', head=MEMBER_HEAD.replace("for member in roster:", "for jar in jars:")),
             fails_at=0, message_contains="'jars' is not defined"),
        dict(why="the for line without its colon",
             code=_member(head=MEMBER_HEAD.replace("for member in roster:", "for member in roster")), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the values typed by hand: a loop over four typed lines (CALL passes, LOOP fails)",
             code=_member("    show_on_ley_board(member)", head=MEMBER_HEAD.replace(
                 "for member in roster:",
                 'for member in ["Oogrish: 18", "Gearshift: 20", "Bomb Shell: 24", "Lucky: 26"]:')),
             fails_at=1, message_contains="a list you typed"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="for-each,list-of-dicts", solo="false", dictates="",
             foreign_names="jars,jar,spice,left,label") + "\n"
        "5A-03. Setup (spec): the four sheets at full mana (real table values) and `show_on_ley_board(text)`, a "
        "CALL recorder (Unit 3's helper: it keeps each text and prints `[Ley board] ...`). The starter's comments "
        "show the keys and the first line to make. CP1 [ND]. Checks: CALL (four board lines, in roster order, each "
        "`<name>: <mana>`; a line may carry more after the mana, so Lucky's side quest stays green) and LOOP (a "
        "rerun with 5 other heroes swapped in after the setup runs: four typed calls show 4 lines). Catches "
        "(spec): `roster[\"name\"]` (the TypeError row, 'list indices must be integers or slices, not str') and "
        "`roster` where `member` belongs; also `roster[member]` (the item as an index), the whole sheet, `print`, "
        "`roster[0]`, a typed name, no `str()`, the example's `jars`. The board takes one text, so the Example "
        "glues with `+` and models no comma (teacher ruling); a comma in the call is Python's TypeError ('takes "
        "1 positional argument'), and a name with no `\": \"` is told to glue it on with `+`. The Example's one "
        "print line is 49 characters, the teacher's dictated line, wider than the 36-character phone rule. The "
        "Show rung, the solution and Assemble it use the same two lines (`line = ...`, then "
        "`show_on_ley_board(line)`), as the Teach rung does, so Start me off (`line =`) is in the solution. PA "
        "distractors: `roster[\"name\"]` in the `line` form, the whole sheet and the colon-less `for` line."
    ),
)

# ---- 5A-04 running-total -----------------------------------------------------------------------------------

FULL_ROSTER_CODE = roster_code(FULL)
TOTAL_STARTER = FULL_ROSTER_CODE + "total = 0\nfor member in roster:\n    # Add this member's mana.\n    pass\nprint(total)\n"


def _total(body='    total = total + member["mana"]', head="total = 0\nfor member in roster:\n",
           tail="print(total)\n"):
    return FULL_ROSTER_CODE + head + "    # Add this member's mana.\n" + body + "\n" + tail


TOTAL_SOLUTION = _total()
MANA_OTHER = [sheet("Oogrish", 12), sheet("Gearshift", 9), sheet("Bomb Shell", 30), sheet("Lucky", 5)]

TOTAL_CHECK = chk(
    "total holds the party's mana, and follows other sheets",
    r'''
_t0 = _parsed()
_fors = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For']
_reset = [_n for _f in _fors for _n in _ast.walk(_f) if _tn(_n) == 'Assign' and _tn(_n.value) == 'Constant'
          and _any(_tn(_x) == 'Name' and _x.id == 'total' for _x in _n.targets)]
_bare = [_n for _f in _fors for _n in _ast.walk(_f) if _tn(_n) == 'Expr' and _tn(_n.value) == 'BinOp']
_in, _out = _total_adds('total')
_INSIDE = ('Your total is worked out once, outside the loop. Do the adding inside the loop, indented under '
           '`for member in roster:`, so it runs once for each member.')
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__), ({'roster': __FIVE__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('roster')
    assert not _err, _stop(_err, _ev)
    _r = _ns.get('roster')
    assert _tn(_r) == 'list' and _r and _all(_tn(_m) == 'dict' and 'mana' in _m for _m in _r), _keep('roster')
    assert 'total' in _ns, "Python can't find `total`. Put back `total = 0` on line 7, above the loop."
    _want = 0
    for _m in _r:
        _want = _want + _m['mana']
    _got = _ns['total']
    if _got == _want:
        continue
    _last = _r[-1]['mana']
    assert not (_got == _last and _reset), ('Your total restarts every pass, because `total = 0` is inside the loop. '
                                            'Move `total = 0` above the loop.' + _ev)
    assert not (_bare and _got == 0), (
        'Your adding line has no `total = ` in front, so Python works it out and throws it away. Store the answer '
        'in `total`: `total = total + ...`.')
    assert _got != 0, ("`total` is still 0, the placeholder it started with. Inside the loop, add this member's "
                       "mana to it.")
    assert not (_vals is not None and _typed_for()), (
        'Your `for` line walks numbers you typed in, so they stay the same when the sheets change. Loop over '
        '`roster` and add `member["mana"]`.' + _ev)
    assert not (_vals is not None and _got == 88), (
        'With other mana on the sheets, `total` stayed 88, because the answer is typed in. Build the total in the '
        'loop, from each `member["mana"]`.' + _ev)
    assert not (_out and not _in), _INSIDE + _ev
    assert _got != _last, ("`total` ended as only the last member's mana, " + _str(_last) + ", because your line "
                           "replaces it. Add to `total`, don't replace it: `total = total + ...`." + _ev)
    assert False, ('`total` ended as ' + _sh(_got) + ', not ' + _str(_want) + ". Add each member's mana to "
                   "`total`, inside the loop." + _ev)
# The right total, but worked out somewhere else (`total = sum(...)` below the loop): the task is the loop.
assert _in, _INSIDE
''',
    MANA=MANA_OTHER,
    EVM=ev_mana([12, 9, 30, 5]),
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

PRINT_ONCE = chk(
    "the total prints once, after the loop",
    r'''
_r = globals().get('roster')
_t = globals().get('total')
_part = []
_s = 0
for _m in _r[:-1]:
    _s = _s + _m['mana']
    _part.append(_s)
# A running total that is also one hero's mana (the first one) could be a trace line: skip it.
_part = [_p for _p in _part if _p not in [_m['mana'] for _m in _r]]
_seen = [_n for _l in _lines() for _n in _nums(_l)]
assert not _any(_p in _seen for _p in _part), (
    '`print(total)` is inside the loop, so it printed every pass. Take the spaces off the front of '
    '`print(total)`, so it runs once, after the loop.')
assert _t in _seen, ("The Console doesn't show `total`. Put `print(total)` back at the bottom, below the loop, with "
                     "no spaces in front.")
_ns, _rows, _err, _miss = _rerun({'roster': __MANA__})
_want = 0
for _m in _ns.get('roster') or []:
    _want = _want + _m['mana']
assert _err or _any(_want in _nums(_l) for _l in _rows), (
    'With other mana, your program did not show the new total, ' + _str(_want) + '. Print `total` itself after '
    'the loop: `print(total)`.' + __EVM__)
''',
    MANA=MANA_OTHER,
    EVM=ev_mana([12, 9, 30, 5]),
)

TOTAL_BONUS = chk(
    "the average mana prints, and follows other sheets",
    r'''
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev)
    _r = _ns['roster']
    _avg = 0
    for _m in _r:
        _avg = _avg + _m['mana']
    _avg = _avg / _len(_r)
    _hit = [_l for _l in _rows if _re.search(r'(?<![\d.])' + _re.escape(_str(_avg)) + r'(?![\d])', _l)]
    assert _hit, ('The Console does not show the average yet. After the loop, print `total / len(roster)`: the '
                  'total shared out over the heroes.' + _ev)
''',
    MANA=MANA_OTHER,
    EVM=ev_mana([12, 9, 30, 5]),
)

RUNNING_TOTAL = dict(
    id="running-total",
    title="Running total",
    martu=(
        "A [[running total]] is a number that starts at 0 and grows on every pass of a loop. In math class, you "
        "add a column of numbers one at a time: 5, then 5 + 2 is 7, then 7 + 4 is 11. `coins = coins + bag` "
        "does that: the old total plus one more.\n"
        "So `coins = 0` goes *above* the loop, once, and the adding line goes *inside* it. Lines inside the loop "
        "run every pass, so a `= 0` line in there would set the total back to 0 every time.\n"
        "In algebra, x = x + 5 has no answer. In Python, `=` isn't a math statement: Python works out the right "
        "side with the old total, then puts the answer back in the box."
    ),
    example="coins = 0\nfor bag in [5, 2, 4]:\n    coins = coins + bag\nprint(coins)\n",
    example_output="11",
    names=["total", "roster", "member"],
    predict=dict(
        q="Before you write yours: here, the `= 0` line is inside the loop. What will this print?",
        code="for bag in [5, 2, 4]:\n    coins = 0\n    coins = coins + bag\nprint(coins)\n",
        choices=["11", "0", "4", "5\n7\n11"],
        answer=2,
        explain=(
            "`coins = 0` is inside the loop, so it runs every pass: the total goes back to 0, then one bag is "
            "added. After the last pass it holds only the last bag: 4. That's why the `= 0` line goes above the "
            "loop."
        ),
    ),
    tracer=True,
    starter=TOTAL_STARTER,
    checkpoints=[
        dict(
            id="add-up-the-mana",
            text=(
                "Replace `pass` on line 10 with a line that adds this member's mana to `total`. Then press Run: the "
                "Console shows the whole party's mana."
            ),
            dictated=False,
            hints=[
                "Look at line 7, `total = 0`: the total starts at 0, above the loop. On line 10, inside the loop, "
                "what should `total` grow by on each pass?",
                "The column of numbers, with other names:\n```python\ncoins = 0\nfor bag in [5, 2, 4]:\n"
                "    coins = coins + bag\n```\nThe right side reads the old total and adds one more bag.",
                "Write `total = total + member[\"mana\"]` in place of `pass`.",
            ],
            checks=[TOTAL_CHECK, PRINT_ONCE],
            pass_line="Your loop added up the whole party's mana, 88, one pass at a time. Mar'tu: Good.",
        ),
    ],
    solution=TOTAL_SOLUTION,
    assemble=dict(
        lines=[FULL_ROSTER_CODE.strip(), "total = 0", "for member in roster:", '    total = total + member["mana"]',
               "print(total)"],
        distractors=["    total = 0", '    total = member["mana"]', "    print(total)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The tally jar",
            text=(
                "```text\nstart:      jar = 0\nOogrish:    0 + 18 = 18\nGearshift: 18 + 20 = 38\n"
                "Bomb Shell: 38 + 24 = 62\nLucky:     62 + 26 = 88\n```\n"
                "Each pass, the jar keeps what it had and gets one more handful of mana."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Trace table",
            text=(
                "```text\npass  member[\"mana\"]  total\nstart  -              0\n1      18             18\n"
                "2      20             38\n3      24             62\n4      26             88\n```\n"
                "`total = total + member[\"mana\"]` reads the old total on the right, then stores the new one."
            ),
        ),
        dict(
            angle="everyday",
            label="Counting coins",
            text=(
                "Count coins out loud: 5, then 7, then 11. You never start again from zero between coins. You "
                "start at zero once, before the first coin."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "Holding the barrier: `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]`. Same shape: the "
                "right side reads the old value, works out a new one, and `=` stores it back."
            ),
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="Run the math",
        text=(
            "Gearshift wants the average mana, the mean from math class. On a new line at the bottom, print the "
            "total shared out over the heroes: `total / len(roster)`."
        ),
        hints=[
            "`len(roster)` counts the sheets: 4. In math class, the mean is the total divided by how many there "
            "are.",
            "Write `print(total / len(roster))` at the very end, with no spaces in front.",
        ],
        checks=[TOTAL_BONUS],
        solution=TOTAL_SOLUTION + "print(total / len(roster))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "You've seen this line in `cast_spell`. The right side reads the old mana and takes the cost away, and "
            "`=` puts the new mana back. Your running total is the same move, adding instead."
        ),
    ),
    takeaway="A running total starts at 0 above the loop, and grows inside it: `total = total + ...`.",
    wrong_answers=[
        dict(why="the starter: pass, total stays 0", code=TOTAL_STARTER, fails_at=1, message_contains="still 0"),
        dict(why="total = 0 inside the loop (spec)",
             code=_total(body='    total = 0\n    total = total + member["mana"]'), fails_at=1,
             message_contains="restarts every pass"),
        dict(why="the total typed by hand", code=_total(body="    pass", tail="total = 18 + 20 + 24 + 26\nprint(total)\n"),
             fails_at=1, message_contains="stayed 88"),
        dict(why="replaced, not added: total = member[\"mana\"]", code=_total(body='    total = member["mana"]'), fails_at=1,
             message_contains="don't replace it"),
        dict(why="a sum on its own line, not stored", code=_total(body='    total + member["mana"]'), fails_at=1,
             message_contains="Store the answer"),
        dict(why="print(total) indented inside the loop: it prints every pass",
             code=_total(body='    total = total + member["mana"]\n    print(total)', tail=""), fails_at=1,
             message_contains="every pass"),
        dict(why="the whole sheet added (TypeError)", code=_total(body="    total = total + member"), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="roster[\"mana\"] for member[\"mana\"] (TypeError)", code=_total(body='    total = total + roster["mana"]'),
             fails_at=0, message_contains="list indices must be integers"),
        dict(why="total = 0 deleted (NameError)", code=_total(head="for member in roster:\n"), fails_at=0,
             message_contains="'total' is not defined"),
        dict(why="the example's names copied", code=_total(body="    total = total + bag"), fails_at=0,
             message_contains="'bag' is not defined"),
        dict(why="the adding line below the loop, not indented: it runs once, on the last member",
             code=_total(body="    pass", tail='total = total + member["mana"]\nprint(total)\n'), fails_at=1,
             message_contains="inside the loop"),
        dict(why="the four sheets added by position, below the loop (passes 88 and other mana, not 5 heroes)",
             code=_total(body="    pass", tail='total = roster[0]["mana"] + roster[1]["mana"] + roster[2]["mana"] '
                                             '+ roster[3]["mana"]\nprint(total)\n'),
             fails_at=1, message_contains="inside the loop"),
        dict(why="sum() below the loop: the right total, but the loop does nothing (skips the goal)",
             code=_total(body="    pass", tail='total = sum([m["mana"] for m in roster])\nprint(total)\n'), fails_at=1,
             message_contains="inside the loop"),
        dict(why="the values typed by hand: the loop runs over typed numbers, not the sheets",
             code=FULL_ROSTER_CODE + "total = 0\nfor mana in [18, 20, 24, 26]:\n    total = total + mana\nprint(total)\n",
             fails_at=1, message_contains="numbers you typed"),
        dict(why="the total built right, but 88 printed by hand",
             code=_total(tail="print(88)\n"), fails_at=1, message_contains="Print `total` itself"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="accumulate", solo="false", dictates="",
             foreign_names="coins,bag", trace="static trace table (another_way), tracer=True") + "\n"
        "5A-04. The roster is visible (name and mana only, one sheet per line, 39 characters at most), so the "
        "student can see where 88 comes from. Predict (P) is the spec's catch in advance: the reset inside the "
        "loop prints only the last bag. CP1 [ND]. Checks: 88 for the real party; CMB (other mana on the same "
        "sheets, 12 + 9 + 30 + 5 = 56, so a typed 88 or `18 + 20 + 24 + 26` fails with 'stayed 88'); LOOP (5 "
        "other heroes, 65). The reset inside the loop gets the spec's message word for word. The long form is "
        "taught; `+=` passes (it is not in any message). The adding must happen inside the loop: the add line below "
        "the loop, four sheets added by position, and `sum()` below the loop are named ('inside the loop'). A "
        "second check: `print(total)` runs once, after the loop (the running totals 38 and 62 must not print; 18 is "
        "also Oogrish's own mana, so a trace print of each member's mana passes), and a rerun with other mana must "
        "print the new total (a typed `print(88)` fails). Bonus by Gearshift: the average (combining accumulate + "
        "division)."
    ),
)

# ---- 5A-05 how-much-each-gap-shrank ------------------------------------------------------------------------

SHRINK_HEAD = WALL_LINE + "for i in range(1, len(chalk_wall)):\n"
SHRINK_STARTER = SHRINK_HEAD + "    shrink = 0\n    print(shrink)\n"
SHRINK_LINE = "    shrink = chalk_wall[i - 1] - chalk_wall[i]"


def _shrink(line=SHRINK_LINE, head=SHRINK_HEAD, show="    print(shrink)\n", tail=""):
    return head + line + "\n" + show + tail


SHRINK_SOLUTION = _shrink()
W5 = [70, 68, 65, 64, 60]  # shrinks 2, 3, 1, 4: growth 1, -2, 3 (no repeats, so nothing typed fits)

SHRINK_CHECK = chk(
    "each shrink is the gap before minus this gap, on any wall",
    r'''
def _shrinks(_rows):
    # The last whole number on each line, so a label (`Shrink: 1`, `48 47 1`, `1 hours`) is fine.
    return [_nums(_l)[-1] for _l in _rows if '[' not in _l and _nums(_l)]
_own = _shrinks(_lines())
_fixed = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'For' and _tn(_n.iter) == 'Call'
          and _tn(_n.iter.func) == 'Name' and _n.iter.func.id == 'range' and _n.iter.args
          and _all(_tn(_a) == 'Constant' for _a in _n.iter.args)]
for _vals, _ev in ((None, ''), ({'chalk_wall': __W5__}, __EVW5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not (_err.startswith('IndexError') and _fixed), (
        'With a shorter wall, your range ran past the end, because its number is typed in. Use `len(chalk_wall)` '
        'in the range, so the loop fits any wall.' + _ev)
    assert not _err, _stop(_err, _ev, 'Make your code work for another wall too.')
    _w = _ns.get('chalk_wall')
    assert _tn(_w) == 'list' and _len(_w) > 2, _keep('chalk_wall')
    _want = [_w[_i - 1] - _w[_i] for _i in _rng(1, _len(_w))]
    _got = _shrinks(_rows)
    if _got[:_len(_want)] == _want:
        continue
    assert _rows, 'Nothing printed. Keep `print(shrink)` inside the loop, so it shows a shrink every pass.'
    assert _got, 'No line in the Console shows a number. Print the shrink on each pass: `print(shrink)`.'
    assert _got != [0] * _len(_want), ('Every shrink is 0, because line 3 still says `shrink = 0`. Replace the 0 '
                                       'with `chalk_wall[i - 1] - chalk_wall[i]`.')
    assert _got[:_len(_want)] != [-_x for _x in _want], (
        'Your shrinks came out below 0, because the subtraction is the wrong way around. Take this gap away from '
        'the gap before: `chalk_wall[i - 1] - chalk_wall[i]`.' + _ev)
    assert not (_len(_got) == _len(_want) + 1 and _got[1:] == _want), (
        'Your first shrink compares the first gap with the last one, because the range starts at 0. Keep '
        '`range(1, len(chalk_wall))`: start at 1. Position 0 has no gap before it.' + _ev)
    assert not (_vals is not None and _got == _own), (
        'Another wall printed the same shrinks as yours, so they do not come from the wall. Work each shrink out '
        'with `i`, so it works for any wall.' + _ev)
    assert _len(_got) != 1, ('`print(shrink)` is not indented inside the loop, so it printed once. Indent it 4 '
                             'spaces, so it prints every pass.' + _ev)
    assert False, ('Your shrinks are not the gap before minus this gap. Make `shrink` '
                   '`chalk_wall[i - 1] - chalk_wall[i]`.' + _ev)
''',
    W5=W5,
    EVW5=ev_wall(W5),
)

SHRINK_BONUS = chk(
    "after the shrinks, each shrink's growth prints",
    r'''
for _vals, _ev in ((None, ''), ({'chalk_wall': __W5__}, __EVW5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev, 'Make your code work for another wall too.')
    _w = _ns['chalk_wall']
    _s = [_w[_i - 1] - _w[_i] for _i in _rng(1, _len(_w))]
    _g = [_s[_i] - _s[_i - 1] for _i in _rng(1, _len(_s))]
    _got = [_nums(_l)[-1] for _l in _rows if '[' not in _l and _nums(_l)]
    _n = _len(_s)
    assert _got[_n:_n + _len(_g)] == _g, (
        'The Console does not show how much each shrink grew. After the shrinks, print this shrink minus the one '
        'before it, for each shrink.' + _ev)
''',
    W5=W5,
    EVW5=ev_wall(W5),
)

SHRINK_BONUS_SOLUTION = (
    SHRINK_HEAD.replace("for i", "shrinks = []\nfor i") + SHRINK_LINE + "\n    print(shrink)\n    shrinks.append(shrink)\n"
    "for i in range(1, len(shrinks)):\n    print(shrinks[i] - shrinks[i - 1])\n"
)

HOW_MUCH_EACH_GAP_SHRANK = dict(
    id="how-much-each-gap-shrank",
    title="How much each gap shrank",
    martu=(
        "A loop over `range(1, len(chalk_wall))` hands you positions, not gaps: 1, 2, 3, 4, 5, 6. With position "
        "`i`, this gap is `chalk_wall[i]`, and the gap right before it is `chalk_wall[i - 1]`. It's like an "
        "input-output table in math class, where you find the change from one row to the next.\n"
        "The *shrink* is how many hours shorter a gap is than the one before it. 48, then 47, is a shrink of 1: "
        "the gap before, minus this gap.\n"
        "Why start at 1? Position 0 is the first gap, and nothing comes before it.\n"
        "Gearshift says the gaps shrink faster every time. Don't take his word for it. Take the wall's, yes?"
    ),
    example="marks = [9, 7, 4]\nfor i in range(1, len(marks)):\n    print(i, marks[i])\n",
    example_output="1 7\n2 4",
    names=["chalk_wall", "shrink", "i"],
    predict=dict(
        q="Before you press Run: this loop prints each gap with the gap right before it. What will it print?",
        code="wall = [48, 48, 47, 46]\nfor i in range(1, len(wall)):\n    print(wall[i - 1], wall[i])\n",
        choices=["48 48\n48 47\n47 46", "48 48\n48 47\n47 46\n46 48", "48\n48\n47\n46", "1 48\n2 47\n3 46"],
        answer=0,
        explain=(
            "`i` is 1, then 2, then 3. Each pass prints the gap before (`wall[i - 1]`) and this gap (`wall[i]`):\n"
            "```text\ni  wall[i-1]  wall[i]\n1  48         48\n2  48         47\n3  47         46\n```\n"
            "Four gaps make three pairs."
        ),
    ),
    pair_talk=(
        "Pair talk: once it passes, look at the shrinks together. Tell your partner what you think the next gap "
        "will be, and why. Then share it with the class."
    ),
    starter=SHRINK_STARTER,
    checkpoints=[
        dict(
            id="neighbor-minus-this",
            text=(
                "On line 3, replace the `0` in `shrink = 0` with the gap before minus this gap. Use `chalk_wall` "
                "with `i` and `i - 1`, not numbers."
            ),
            dictated=False,
            hints=[
                "Look at line 3, `shrink = 0`. Keep `shrink = ` and change only the `0`. Which two gaps does each "
                "pass compare?",
                "At `i = 5`, which two gaps does `shrink` use? `chalk_wall[4]` is 44, the gap before, and "
                "`chalk_wall[5]` is 41, this one. 44 - 41 is 3.",
                "With other names: in `marks = [9, 7, 4]`, at `i = 1`, `marks[i - 1] - marks[i]` is 9 - 7, which "
                "is 2. The gap before, minus this one.",
                "Write `shrink = chalk_wall[i - 1] - chalk_wall[i]` in place of `shrink = 0`.",
            ],
            checks=[SHRINK_CHECK],
            pass_line="The shrinks keep growing: 0, 1, 1, 2, 3, 4. Mar'tu: The decay is accelerating. Now you've seen it yourself.",
        ),
    ],
    solution=SHRINK_SOLUTION,
    assemble=dict(
        lines=[WALL_LINE.strip(), "for i in range(1, len(chalk_wall)):", SHRINK_LINE, "    print(shrink)"],
        distractors=["    shrink = chalk_wall[i] - chalk_wall[i + 1]", "for i in len(chalk_wall):",
                     "    shrink = chalk_wall[i] - chalk_wall[i - 1]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Neighbors on the wall",
            text=(
                "```text\n48  48  47  46  44  41  37\n  0   1   1   2   3   4\n```\n"
                "Each shrink sits between two gaps: the gap before, minus the gap after it."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Trace table",
            text=(
                "```text\ni  wall[i-1]  wall[i]  shrink\n1  48         48       0\n2  48         47       1\n"
                "3  47         46       1\n4  46         44       2\n5  44         41       3\n"
                "6  41         37       4\n```\n"
                "`i` stops at 6, the last position. `[i - 1]` never reaches past the start."
            ),
        ),
        dict(
            angle="why",
            label="Why the loop stops one early",
            text=(
                "Seven gaps make only six pairs. Starting at 1 and looking back gives six passes. Starting at 0 "
                "and looking ahead at `[i + 1]` must stop at 5, or the last pass asks for position 7. There is "
                "none, so Python stops with an IndexError."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Gaps between the gaps",
        text=(
            "Lucky smells a pattern. After the shrinks, print how much each shrink grew from the one before: "
            "1, 0, 1, 1, 1. Keep the shrinks in a list as you go."
        ),
        hints=[
            "Make `shrinks = []` above the loop, and `.append(shrink)` inside it. Then a second loop compares "
            "neighbors in `shrinks`.",
            "Write `print(shrinks[i] - shrinks[i - 1])` inside a second loop over `range(1, len(shrinks))`.",
        ],
        checks=[SHRINK_BONUS],
        solution=SHRINK_BONUS_SOLUTION,
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "In the campaign, Gearshift's visor dimmed as he ran the math: *the gaps are getting shorter, and "
            "they're shrinking faster every time.* Mar'tu said: *the decay is accelerating*: the shrinks keep "
            "getting bigger. Now you'll get it: your loop ran Gearshift's math."
        ),
    ),
    takeaway="`for i in range(1, len(wall)):` compares each gap with the one before: `wall[i - 1] - wall[i]`.",
    wrong_answers=[
        dict(why="the starter: shrink stays 0", code=SHRINK_STARTER, fails_at=1, message_contains="still says `shrink = 0`"),
        dict(why="neighbors one past the end: [i + 1] with range(1, len) (IndexError)",
             code=_shrink("    shrink = chalk_wall[i] - chalk_wall[i + 1]"), fails_at=0, message_contains="out of range"),
        dict(why="neighbors one past the end: range(len) looking ahead (IndexError)",
             code=_shrink("    shrink = chalk_wall[i] - chalk_wall[i + 1]", head=WALL_LINE + "for i in range(len(chalk_wall)):\n"),
             fails_at=0, message_contains="out of range"),
        dict(why="the subtraction backwards: this minus before", code=_shrink("    shrink = chalk_wall[i] - chalk_wall[i - 1]"),
             fails_at=1, message_contains="below 0"),
        dict(why="range starts at 0: the first pass reads the last gap",
             code=_shrink(head=WALL_LINE + "for i in range(0, len(chalk_wall)):\n"), fails_at=1,
             message_contains="start at 1"),
        dict(why="for i in len(...) ('int' object is not iterable)", code=_shrink(head=WALL_LINE + "for i in len(chalk_wall):\n"),
             fails_at=0, message_contains="not iterable"),
        dict(why="for i in 6: a bare number, not range ('int' object is not iterable)",
             code=_shrink(head=WALL_LINE + "for i in 6:\n"), fails_at=0, message_contains="not iterable"),
        dict(why="the shrinks typed by hand", code=WALL_LINE + "".join(f"print({s})\n" for s in [0, 1, 1, 2, 3, 4]),
             fails_at=1, message_contains="works for any wall"),
        dict(why="the print taken out of the loop: it prints once",
             code=_shrink(show="", tail="print(shrink)\n"), fails_at=1, message_contains="printed once"),
        dict(why="the item used as an index", code=_shrink("    shrink = chalk_wall[gap - 1] - chalk_wall[gap]",
                                                           head=WALL_LINE + "for gap in chalk_wall:\n"),
             fails_at=0, message_contains="out of range"),
        dict(why="square brackets on range (TypeError)", code=_shrink(head=WALL_LINE + "for i in range[1, len(chalk_wall)]:\n"),
             fails_at=0, message_contains="not subscriptable"),
        dict(why="the wall's length typed by hand: range(1, 7) (right for this wall, past the end of a shorter one)",
             code=_shrink(head=WALL_LINE + "for i in range(1, 7):\n"), fails_at=1, message_contains="its number is typed in"),
        dict(why="the values typed by hand: a typed copy of the wall under another name",
             code=_shrink("    shrink = wall[i - 1] - wall[i]",
                          head=WALL_LINE + "wall = [48, 48, 47, 46, 44, 41, 37]\nfor i in range(1, len(wall)):\n"),
             fails_at=1, message_contains="works for any wall"),
        dict(why="the example's list name copied (marks)", code=_shrink(head=WALL_LINE + "for i in range(1, len(marks)):\n"),
             fails_at=0, message_contains="'marks' is not defined"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="range-len,neighbors", solo="false", dictates="",
             foreign_names="marks,wall", stages="P,I,M", story_beat="protected", moment="the decay reveal (class discussion)")
        + "\n"
        "5A-05, the protected story beat (renamed G2 R13). Starter as spec. Predict-heavy: the neighbors predict "
        "(its explain is the static trace table), then CP1 [ND] (teacher ruling on the Unit 6 reviews: the spec's "
        "[D] line is no longer dictated; the text gives the goal, and the line sits in the check messages and the "
        "Show rung). The ladder: point, a Teach rung on the real wall at `i = 5` (44 - 41 is 3), the marks rung, "
        "Show. The Learn text no longer mentions the look-ahead `[i + 1]`; the 'why' angle keeps the "
        "stop-one-early rule. Checks: OUT 0 1 1 2 3 4 "
        "(the student's own wall) and LOOP on `[70, 68, 65, 64, 60]` (shrinks 2, 3, 1, 4), so typed shrinks "
        "fail. The pass line is Mar'tu's spec line. `range(len(x) - 1)` with `[i] - [i + 1]` passes too (it stops "
        "one early); `[i + 1]` without stopping early is the IndexError WA (the class slip). The 'why' angle is "
        "the stop-one-early rule. Lucky's side quest (G4 R16): the gaps between the gaps, 1 0 1 1 1, checked on "
        "the student's wall and the rerun wall (growth 1, -2, 3). Pair talk feeds the class discussion "
        "(Mar'tu moment, run-kit)."
    ),
)

# ---- 5A-06 loop-with-a-check -------------------------------------------------------------------------------

NIGHT_ROSTER_CODE = "# After a night holding the barrier:\n" + roster_code(NIGHT)
TIRED_COMMENTS = (
    "# 1. Loop over the roster.\n"
    "# 2. If a member has less than 10\n"
    "#    mana, print their name and\n"
    "#    \"needs rest\".\n"
)
TIRED_STARTER = NIGHT_ROSTER_CODE + TIRED_COMMENTS
TIRED_BODY = '    if member["mana"] < 10:\n        print(member["name"], "needs rest")'


def _tired(body=TIRED_BODY, head="for member in roster:", tail=""):
    return NIGHT_ROSTER_CODE + TIRED_COMMENTS + head + "\n" + body + "\n" + tail


TIRED_SOLUTION = _tired()
# Same heroes, other mana: Bomb Shell sits at exactly 10 (not less than 10), so `<=` is caught.
TIRED_MANA = [sheet("Oogrish", 12), sheet("Gearshift", 9), sheet("Bomb Shell", 10), sheet("Lucky", 2)]

TIRED_CHECK = chk(
    "only the members under 10 mana print, with needs rest",
    r'''
_t0 = _parsed()
_fors = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For']
_targets = [_n.target.id for _n in _fors if _tn(_n.target) == 'Name']
_outside = [_n for _n in _t0.body if _tn(_n) == 'If'
            and _any(_tn(_x) == 'Name' and _x.id in _targets for _x in _ast.walk(_n.test))]
_lte = _any(_tn(_n) == 'LtE' for _n in _ast.walk(_t0))
# Names the loop sets (its variable, and anything assigned inside it), and the prints inside and after it.
_inloop = _set(_targets) | _set([_x.id for _f in _fors for _x in _ast.walk(_f) if _tn(_x) == 'Name'
                                 and _tn(_x.ctx) == 'Store'])
def _is_print(_n):
    return _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'print'
_for_prints = [_n for _f in _fors for _n in _ast.walk(_f) if _is_print(_n)]
_late = [_n for _n in _t0.body if _tn(_n) == 'Expr' and _is_print(_n.value)
         and _any(_tn(_x) == 'Name' and _x.id in _inloop for _x in _ast.walk(_n.value))]
_own = None
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__), ({'roster': __FIVE__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('roster')
    assert not _err, _stop(_err, _ev)
    _r = _ns.get('roster')
    assert _tn(_r) == 'list' and _all(_tn(_m) == 'dict' for _m in _r), _keep('roster')
    _names = [_m['name'] for _m in _r]
    _want = [_m['name'] for _m in _r if _m['mana'] < 10]
    # The heroes named on any line, and the heroes named on a line that says `needs rest`. Other lines (a
    # heading, or `Gearshift keeps watch` from an `else:`) are fine.
    _named, _said = [], []
    for _l in _rows:
        _hit = [_n for _n in _names if _n in _l]
        if _hit:
            _named.append(_hit[0])
            if 'needs rest' in _l.lower():
                _said.append(_hit[0])
    if _vals is None:
        _own = _said
    if _said == _want:
        continue
    assert not _any(_l.startswith('[') for _l in _rows), ('Each line shows the whole roster. Print one name at a '
                                                          'time: `member["name"]`, not the whole roster.')
    assert not _any(_l.startswith('{') for _l in _rows), ('A line shows a whole sheet, curly braces and all. Print '
                                                          'only the name: `member["name"]`, not the whole sheet.')
    assert _fors, 'Your code has no loop yet. Start with `for member in roster:`, then put the `if` inside the loop.'
    assert not _outside, ('Your `if` is not indented under the `for` line, so it ran once, after the loop. Indent it '
                          '4 spaces, so it checks every member.')
    assert not (_late and not _for_prints), (
        'Your print ran once, after the loop, because it is not indented. Put it inside the loop, under the `if`, '
        'with 8 spaces in front.')
    assert _rows, 'Nothing printed. Inside the loop, put an `if` that prints the members with less than 10 mana.' + _ev
    assert not _typed_for(), ('Your `for` line walks a list you typed out, and a list you typed stays the same when '
                              'the sheets change. Loop over the sheets, `for member in roster:`, and test '
                              '`member["mana"]`.' + _ev)
    assert _said != _names, ('Every member printed. Put the print inside an `if`, so only the members with less '
                             'than 10 mana print.' + _ev)
    _ten = [_m['name'] for _m in _r if _m['mana'] == 10 and _m['name'] in _said]
    assert not (_lte and _ten), (_ten[0] + ', with exactly 10 mana, printed too. Use `<`: exactly 10 is not less '
                                 'than 10.' + _ev)
    assert not (_len(_said) > 1 and _len(_set(_said)) == 1), (
        'Every line named ' + _said[0] + '. Print `member["name"]`, so each line names this pass\'s hero.' + _ev)
    assert not (_vals is not None and _said == _own), (
        "With other mana, the same names printed, so your names don't come from the sheets. Read each name and "
        "mana from `member`." + _ev)
    assert not (_named == _want and not _said), ('The right names printed, but without `needs rest`. After each '
                                                 'name, add `needs rest`, like `Oogrish needs rest`.' + _ev)
    assert False, ('The wrong members printed `needs rest`. Print it for each member with less than 10 mana, and '
                   'for no one else.' + _ev)
''',
    MANA=TIRED_MANA,
    EVM=ev_mana([12, 9, 10, 2]),
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

TIRED_BONUS = chk(
    "resting counts the tired members, and follows other mana",
    r'''
for _vals, _ev in ((None, ''), ({'roster': __COUNT__}, __EVC__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev)
    _want = _len([_m for _m in _ns['roster'] if _m['mana'] < 10])
    assert 'resting' in _ns, "Python can't find `resting`. Make a variable named `resting`, set to 0 above the loop."
    assert _ns['resting'] == _want, ('`resting` ended as ' + _sh(_ns['resting']) + ', not ' + _str(_want) + '. Add 1 '
                                     'to `resting` inside the `if`, and set it to 0 above the loop.' + _ev)
    assert _any(_nums(_l)[-1:] == [_want] for _l in _rows), ("The Console doesn't show `resting`. Print it once, "
                                                             "after the loop." + _ev)
''',
    COUNT=[sheet("Oogrish", 5), sheet("Gearshift", 9), sheet("Bomb Shell", 1), sheet("Lucky", 30)],
    EVC=ev_mana([5, 9, 1, 30]),
)

LOOP_WITH_A_CHECK = dict(
    id="loop-with-a-check",
    title="A check inside the loop",
    martu=(
        "An `if` inside a loop asks its question on every pass, and only the items that answer `True` get "
        "through. A teacher does this with a stack of quizzes: read every one, and pull out only the ones under "
        "70. `if member[\"mana\"] < 10:` under `for member in roster:` asks each hero, one at a time.\n"
        "Count the spaces: 4 in front of the `if`, so it runs every pass, and 8 in front of the `print` under it, "
        "so it runs only when the answer is `True`.\n"
        "After a night holding the barrier, the shield around the cabin, some heroes are low on mana, their magic "
        "power. Not sure where to start? Press Run first: my check tells you your first line."
    ),
    example=(
        "for jar in [3, 0, 5]:\n"
        "    if jar < 1:\n"
        '        print("Refill a jar.")\n'
    ),
    example_output="Refill a jar.",
    names=["roster", "member"],
    starter=TIRED_STARTER,
    checkpoints=[
        dict(
            id="who-needs-rest",
            text=(
                "Under the notes, write a loop. For each member with less than 10 mana, it prints the name and "
                "`needs rest`, like `Oogrish needs rest`."
            ),
            dictated=False,
            hints=[
                "Look at the notes on lines 8 to 11: a loop, then an `if` inside it. Your first line is `for member "
                "in roster:`. What question does the `if` under it ask about `member`?",
                "With other names:\n```python\nfor jar in jars:\n    if jar[\"left\"] < 1:\n"
                "        print(jar[\"spice\"], \"empty\")\n```\nOnly the empty jars print. The `if` has 4 spaces in "
                "front, and the `print` has 8.",
                "Write `for member in roster:`, then `if member[\"mana\"] < 10:` under it, then "
                "`print(member[\"name\"], \"needs rest\")` under that.",
            ],
            checks=[TIRED_CHECK],
            pass_line="Only the tired heroes printed. Oogrish: Bomb Shell and I will sit this one out. Steady, now.",
        ),
    ],
    solution=TIRED_SOLUTION,
    assemble=dict(
        lines=[NIGHT_ROSTER_CODE.strip(), "for member in roster:", '    if member["mana"] < 10:',
               '        print(member["name"], "needs rest")'],
        distractors=['    if member["mana"] <= 10:', 'if member["mana"] < 10:', '    if roster["mana"] < 10:'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A gate in the corridor",
            text=(
                "```text\nOogrish  6  -> gate -> needs rest\nGearshift 14 -> gate -> (walks on)\n"
                "Bomb Shell 3 -> gate -> needs rest\nLucky   22  -> gate -> (walks on)\n```\n"
                "Everyone walks down the corridor. The `if` is a gate that stops only the tired ones."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Pass 1: `member` is Oogrish. Is 6 < 10? `True`, so the print runs.\n"
                "2. Pass 2: Gearshift. Is 14 < 10? `False`, so Python skips the print.\n"
                "3. Bomb Shell: 3 < 10, prints. Lucky: 22 < 10, skips."
            ),
        ),
        dict(
            angle="in Tor",
            label="The night watch",
            text=(
                "After a night holding the barrier, Mar'tu checks each hero at the door. Low on mana? To bed. "
                "Everyone else keeps watch."
            ),
        ),
        dict(angle="shorter", text="`for` visits everyone. The `if` inside it picks who prints."),
    ],
    bonus=dict(
        by="bomb-shell",
        title="Head count",
        text=(
            "Bomb Shell wants a number. Count the tired members in a variable named `resting`, and print it once, "
            "after the loop."
        ),
        hints=[
            "It's a running total that adds 1 each time, like a tally mark: `resting = 0` above the loop, and "
            "`+ 1` inside the `if`.",
            "Write `resting = resting + 1` inside the `if`, with `resting = 0` above the loop and `print(resting)` "
            "below it.",
        ],
        checks=[TIRED_BONUS],
        solution=_tired(
            head="resting = 0\nfor member in roster:",
            body=TIRED_BODY + "\n        resting = resting + 1",
            tail="print(resting)\n",
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "Holding the barrier asked this kind of question about one caster: is the mana too low? Now you'll get "
            "it: a loop asks it about every member, one pass at a time."
        ),
    ),
    takeaway="An `if` inside a loop runs every pass, and lets only some items through.",
    wrong_answers=[
        dict(why="the starter: no loop yet", code=TIRED_STARTER, fails_at=1, message_contains="Start with"),
        dict(why="the filter's if outside the loop (runs once, after it)",
             code=_tired(body="    pass", tail='if member["mana"] < 10:\n    print(member["name"], "needs rest")\n'),
             fails_at=1, message_contains="ran once"),
        dict(why="every member printed (no if)", code=_tired(body='    print(member["name"], "needs rest")'), fails_at=1,
             message_contains="Every member printed"),
        dict(why="<= for < (boundary)", code=_tired(body=TIRED_BODY.replace("< 10", "<= 10")), fails_at=1,
             message_contains="exactly 10"),
        dict(why="the names typed by hand",
             code=NIGHT_ROSTER_CODE + 'print("Oogrish needs rest")\nprint("Bomb Shell needs rest")\n', fails_at=1,
             message_contains="Start with"),
        dict(why="the names typed inside a loop that checks nothing real",
             code=_tired(body='    pass', tail='print("Oogrish needs rest")\nprint("Bomb Shell needs rest")\n'),
             fails_at=1, message_contains="same names"),
        dict(why="the whole sheet printed", code=_tired(body='    if member["mana"] < 10:\n        print(member)'), fails_at=1,
             message_contains="whole sheet"),
        dict(why="the whole roster printed", code=_tired(body='    if member["mana"] < 10:\n        print(roster)'), fails_at=1,
             message_contains="whole roster"),
        dict(why="no needs rest", code=_tired(body='    if member["mana"] < 10:\n        print(member["name"])'), fails_at=1,
             message_contains="needs rest"),
        dict(why="roster[\"mana\"] for member[\"mana\"] (TypeError)",
             code=_tired(body=TIRED_BODY.replace('member["mana"]', 'roster["mana"]')), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="four typed ifs on roster[0] to roster[3] (follows mana, not a 5th hero)",
             code=NIGHT_ROSTER_CODE + "".join(
                 f'if roster[{k}]["mana"] < 10:\n    print(roster[{k}]["name"], "needs rest")\n' for k in range(4)),
             fails_at=1, message_contains="Start with"),
        dict(why="the print not indented under the if (IndentationError)",
             code=_tired(body='    if member["mana"] < 10:\n    print(member["name"], "needs rest")'), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="the filter's print outside the loop: it runs once, on the last member",
             code=_tired(body='    if member["mana"] < 10:\n        pass', tail='print(member["name"], "needs rest")\n'),
             fails_at=1, message_contains="Your print ran once"),
        dict(why="each tired name stored inside the loop, but printed once after it",
             code=_tired(body='    if member["mana"] < 10:\n        tired = member["name"]',
                         tail='print(tired, "needs rest")\n'),
             fails_at=1, message_contains="Your print ran once"),
        dict(why="a name typed in the print: the same hero on every line",
             code=_tired(body='    if member["mana"] < 10:\n        print("Oogrish needs rest")'), fails_at=1,
             message_contains="Every line named Oogrish"),
        dict(why="the values typed by hand: a loop over the two tired names",
             code=_tired(body='    print(name, "needs rest")', head='for name in ["Oogrish", "Bomb Shell"]:'),
             fails_at=1, message_contains="a list you typed"),
        dict(why="the names typed in the if: name tests, not mana (follows a 5th hero badly, other mana not at all)",
             code=_tired(body='    if member["name"] == "Oogrish" or member["name"] == "Bomb Shell":\n'
                              '        print(member["name"], "needs rest")'),
             fails_at=1, message_contains="same names"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="loop-with-if", solo="false", dictates="",
             foreign_names="jars,jar,spice,left") + "\n"
        "5A-06. S2: numbered comments, kept as they are (teacher ruling): the one core step where students write "
        "the `for` line themselves. The Learn text ends 'Press Run first: my check names your first line' (the "
        "starter's Run gets 'Start with `for member in roster:` ...'). The night roster (6, 14, 3, 22) is "
        "visible. CP1 [ND]. Checks: the heroes "
        "named on `needs rest` lines (any capitals or separator; other lines, like an `else:` that prints `keeps "
        "watch`, are fine) are exactly the members under 10, in order; CMB with the same heroes at 12, 9, 10, 2 (Bomb Shell at exactly 10, "
        "so `<=` fails, and typed names fail); LOOP with 5 other heroes (four typed `if roster[k]` blocks fail, and "
        "no `for` at all is named first). The filter's `if` outside the loop is named from the code (it runs once, "
        "on Lucky, and prints nothing). Bonus by Bomb Shell (combining filter + count): `resting`, checked on the "
        "night roster (2) and on 5, 9, 1, 30 (3)."
    ),
)

# ---- 5A-07 bars-for-everyone -------------------------------------------------------------------------------

BAR_SETUP = setup_roster(NIGHT_SHEETS)
BAR_DEF = (
    "def mana_bar(hero):\n"
    '    full = "█"\n'
    '    empty = "░"\n'
    "    # Full blocks for the mana,\n"
    "    # empty ones for the mana used.\n"
)
BAR_LOOP = (
    "\n"
    "# roster: 4 sheets with \"name\",\n"
    "# \"mana\" and \"max_mana\".\n"
    "for member in roster:\n"
    "    # Print the name and the bar.\n"
)
BAR_RETURN = '    used = hero["max_mana"] - hero["mana"]\n    return full * hero["mana"] + empty * used'
BAR_PRINT = '    print(member["name"], mana_bar(member))'


def _bar(ret=BAR_RETURN, show=BAR_PRINT):
    return BAR_DEF + ret + "\n" + BAR_LOOP + show + "\n"


BAR_STARTER = _bar('    return ""', "    pass")
BAR_SOLUTION = _bar()
BAR_TESTS = [{"name": "Tester", "mana": 3, "max_mana": 8}, {"name": "Tester", "mana": 0, "max_mana": 5},
             {"name": "Tester", "mana": 7, "max_mana": 7}]

_BAR_WHY = r'''
def _missing(_err):
    # The name in `NameError: name 'used' is not defined`, or ''.
    _m = _re.search(r"name '(\w+)' is not defined", _err)
    return _m.group(1) if _m and _err.startswith('NameError') else ''
def _why(_err, _ev):
    if "can't multiply sequence by non-int of type 'dict'" in _err:
        # `return full * hero`: the whole sheet, where one number from it is meant.
        if _re.search(r'full\s*\*\s*hero\b(?!\s*\[)', _source):
            return ('`hero` is a whole sheet. Multiply `full` by one number from it, the mana: `hero["mana"]`.' + _ev)
        return ('`hero` is a whole sheet. Multiply by one number from it, read by its tag (key), like '
                '`hero["mana"]`.' + _ev)
    if 'unsupported operand' in _err and "'str' and 'int'" in _err:
        return ('Python stopped, because it multiplied before it subtracted. Put parentheses around the mana used: '
                '`empty * (hero["max_mana"] - hero["mana"])`. It is PEMDAS: parentheses first.' + _ev)
    if _err.startswith('KeyError'):
        return ('Python found no tag ' + _err[10:] + ' on the sheet. Use the tags `"mana"` and `"max_mana"`, '
                'spelled exactly.' + _ev)
    if 'list indices' in _err:
        return 'Your recipe reads `roster`, a whole list. Read the sheet it is handed, `hero`, not `roster`.' + _ev
    _n = _missing(_err)
    if _n in ('member', 'roster'):
        return ('Python stopped, because the recipe uses `' + _n + '`, a name it cannot see. Inside the recipe, '
                'the sheet is called `hero`.' + _ev)
    if _n == 'hero':
        return ("Python can't find `hero`, because the `def` line changed. Keep `def mana_bar(hero):` the way it "
                "was at the start, so the sheet is called `hero` inside it." + _ev)
    if _n in ('mana', 'max_mana', 'name'):
        # `return full * mana`: a tag on the sheet, used as a name of its own.
        return ('`' + _n + '` is a tag (key) on the sheet. Inside the recipe, read it from `hero`: `hero["' + _n
                + '"]`.' + _ev)
    if _n:
        return ('Python stopped, because the recipe uses `' + _n + '` before it makes it. Make `' + _n + '` inside '
                'the recipe before you use it, or hand back a name the recipe made.' + _ev)
    _plain = {'TypeError': "a line there mixes kinds of values that don't go together",
              'IndexError': "a line there asks for a position that isn't there",
              'AttributeError': "a line there uses a dot tool the value doesn't have",
              'ZeroDivisionError': 'a line there divides by zero'}.get(_err.split(':')[0], 'a line there has a mistake')
    return ("When Mar'tu called `mana_bar` with a test sheet, Python stopped inside the recipe: " + _plain + '. '
            'Read the numbers from the sheet it is handed, like `hero["mana"]`.' + _ev)
def _evh(_h):
    return " Mar'tu tested your recipe with a test sheet, `" + _sh(_h) + "`."
def _try_bar(_h, _probe):
    # (printed, value, error, probed) for a fresh copy of _h. With _probe (the full-blocks step only), a recipe
    # that stops on a name it never made gets one more try with that name set to 0, so a slip in the empty part
    # (the next step) does not hide a full part that is right. `probed` is that try's text, or None.
    _out, _v, _err = _call(mana_bar, _copy.deepcopy(_h))
    _n = _missing(_err)
    if not (_probe and _n) or _n in ('member', 'roster', 'hero'):
        return _out, _v, _err, None
    _g = mana_bar.__globals__
    _g[_n] = 0
    try:
        _o2, _v2, _e2 = _call(mana_bar, _copy.deepcopy(_h))
    finally:
        _g.pop(_n, None)
    return _out, _v, _err, (_v2 if not _e2 and _tn(_v2) == 'str' else None)
def _lead(_v):
    return _len(_v) - _len(_v.lstrip('█'))
'''


def _bar_ret(probe):
    return chk(
        "mana_bar hands back the bar as text",
        _BAR_WHY + r'''
assert _tn(globals().get('mana_bar')) == 'function', ("Python can't find the recipe `mana_bar`. Keep "
                                                      "`def mana_bar(hero):` the way it was at the start.")
_h = __TESTS__[0]
_ev = _evh(_h)
_out, _got, _err, _pv = _try_bar(_h, __PROBE__)
if _err:
    # Full-blocks step: a name the empty part still needs is the next step's slip. The full-blocks check
    # below judges the rest, and names the crash if the full part is not right either.
    assert _pv is not None, _why(_err, _ev)
else:
    if _got is None:
        assert not _out.strip(), ('`mana_bar` printed the bar, then handed back `None`: nothing. Hand the bar back '
                                  'with `return`, not `print`.' + _ev)
        assert False, '`mana_bar` handed back `None`: nothing came back. Hand the bar back with `return`.' + _ev
    assert _got != '', ("`mana_bar` still hands back empty text, `\"\"`, the placeholder it started with. Build the "
                        "bar from `full` and `hero`, then return it.")
    assert _tn(_got) == 'str', ('`mana_bar` handed back ' + _sh(_got) + ', not text. Hand back the bar as text, made '
                                'of blocks.' + _ev)
''',
        TESTS=BAR_TESTS,
        PROBE=probe,
    )


BAR_RET_FULL = _bar_ret(True)
BAR_RET = _bar_ret(False)

BAR_FULL = chk(
    "each bar starts with a full block for each point of mana",
    _BAR_WHY + r'''
_tests = __TESTS__
_got = []
for _h in _tests:
    _out, _v, _err, _pv = _try_bar(_h, True)
    if _err:
        assert _pv is not None and _lead(_pv) == _h['mana'], _why(_err, _evh(_h))
        _v = _pv
    assert _tn(_v) == 'str', ('`mana_bar` handed back ' + _sh(_v) + ', not text. Hand back the bar as text, made '
                              'of blocks.' + _evh(_h))
    _got.append(_v)
assert _len(_set(_got)) > 1, (
    '`mana_bar` gave back the same bar for three different sheets. Read the sheet it is handed, `hero`.'
    + " Mar'tu tested your recipe with three test sheets.")
for _h, _v in _zip(_tests, _got):
    _m, _x = _h['mana'], _h['max_mana']
    if _lead(_v) == _m:
        continue
    _ev = _evh(_h)
    assert _v != '█' * _x, ('Every block came out full. Use `hero["mana"]` for the full blocks, not the max.'
                            + _ev)
    assert _v != '░' * _m + '█' * (_x - _m), (
        'Your full and empty blocks are swapped. Full blocks are for the mana, and empty blocks for the mana '
        'used.' + _ev)
    assert False, ('This bar started with ' + _str(_lead(_v)) + ' full blocks, not ' + _str(_m) + '. Start the bar '
                   'with one full block for each point of mana: `full * hero["mana"]`.' + _ev)
''',
    TESTS=BAR_TESTS,
)

BAR_PAR = chk(
    "mana_bar works for any hero: no mana, some, and full",
    _BAR_WHY + r'''
_tests = __TESTS__
_got = []
for _h in _tests:
    _out, _v, _err = _call(mana_bar, _copy.deepcopy(_h))
    assert not _err, _why(_err, _evh(_h))
    _got.append(_v)
_wants = ['█' * _h['mana'] + '░' * (_h['max_mana'] - _h['mana']) for _h in _tests]
if _got != _wants:
    _lens = _set([_len(_v) for _v in _got if _tn(_v) == 'str'])
    assert not (_all(_tn(_v) == 'str' for _v in _got) and _len(_lens) == 1), (
        'Every bar came out ' + _str(_lens.pop()) + ' blocks long, because the max is typed in. Read the max from '
        'the sheet, `hero["max_mana"]`, so each bar is as long as that hero' + chr(39) + 's max.'
        " Mar'tu tested your recipe with three test sheets, with max 8, 5 and 7.")
    for _h, _v, _w in _zip(_tests, _got, _wants):
        if _v == _w:
            continue
        _ev = _evh(_h)
        assert _tn(_v) == 'str', ('`mana_bar` handed back ' + _sh(_v) + ', not text. Hand back the bar as text, '
                                  'made of blocks.' + _ev)
        _m, _x = _h['mana'], _h['max_mana']
        assert _v != '█' * _m, ('The bar has no empty blocks. Add the empty blocks: one `empty` for each point of mana '
                                'used.' + _ev)
        assert _len(_v) != _m + _x, ('The bar came out ' + _str(_len(_v)) + ' blocks long, not ' + _str(_x) + '. Glue '
                                     'on one empty block for each point used: `hero["max_mana"] - hero["mana"]`.' + _ev)
        assert False, ('The bar is not right for this sheet. Build it from the sheet: `full` times the mana, then '
                       '`empty` times the mana used.' + _ev)
''',
    TESTS=BAR_TESTS,
)

BAR_LOOP_CHECK = chk(
    "each member's name and bar print, and the loop follows a roster of 5",
    r'''
def _bar(_m):
    return '█' * _m['mana'] + '░' * (_m['max_mana'] - _m['mana'])
def _runs(_l):
    return _re.findall('[█░]+', _l)
assert not _any('<function' in _l for _l in _lines()), (
    'The Console shows `<function ...>`, because the recipe is named but not called. Call it with parentheses '
    'and the sheet: `mana_bar(member)`.')
for _vals, _ev in ((None, ''), ({'roster': __OTHER__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev)
    _r = _ns.get('roster')
    _names = [_m['name'] for _m in _r]
    _bars = [_l for _l in _rows if _runs(_l)]
    # A bar line names a member. A bar printed on its own (a print inside the recipe, say) is not counted.
    _nb = [_l for _l in _bars if _any(_n in _l for _n in _names)]
    if _len(_nb) == _len(_r) and _all(_m['name'] in _l and _bar(_m) in _runs(_l) for _m, _l in _zip(_r, _nb)):
        continue
    assert _rows, 'Nothing printed. Inside the loop, print the name, then `mana_bar(member)`.' + _ev
    assert _bars, 'No bar printed. Print the bar too: `mana_bar(member)`, after the name.' + _ev
    assert not (_len(_bars) == 1 and _len(_r) > 1), (
        'Your print is not indented under the `for` line, so it printed once. Indent it 4 spaces, so it runs for '
        'every member.' + _ev)
    assert not (_vals is not None and _len(_bars) == 4), (
        'With 5 heroes in `roster`, 4 bars printed. Let the loop print every member.' + _ev)
    assert _nb, "The bars print with no names. Print each member's name next to the bar: `member[\"name\"]`." + _ev
    assert _len(_nb) == _len(_r) and _all(_m['name'] in _l for _m, _l in _zip(_r, _nb)), (
        "A name is on the wrong line, because it is typed in. Print this pass's member: `member[\"name\"]`." + _ev)
    assert False, "A bar does not match its member. Hand the recipe this pass's sheet: `mana_bar(member)`." + _ev
# The bars are right, but are they the recipe's? A loop that builds the bar again never calls `mana_bar`.
_t0 = _parsed()
_calls = [_n for _top in _t0.body if not (_tn(_top) == 'FunctionDef' and _top.name == 'mana_bar')
          for _n in _ast.walk(_top) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'mana_bar']
assert _calls, ('Your loop builds the bar again on its own, so `mana_bar` never ran. Call your recipe in the loop: '
                '`mana_bar(member)`.')
''',
    setup=BAR_SETUP,
    from_setup=("roster",),
    OTHER=OTHER_SHEETS,
    EV5=EV_FIVE,
)

BAR_BONUS = chk(
    "each bar ends with mana/max_mana",
    r'''
for _vals, _ev in ((None, ''), ({'roster': __OTHER__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _stop(_err, _ev)
    _bars = [_l for _l in _rows if '█' in _l or '░' in _l]
    _r = _ns['roster']
    assert _len(_bars) == _len(_r) and _all(_l.endswith(_str(_m['mana']) + '/' + _str(_m['max_mana']))
                                            for _m, _l in _zip(_r, _bars)), (
        'Your lines do not end with the numbers yet. End each line with the mana, a slash and the max, like '
        '`6/18`: glue on `str(member["mana"])`, `"/"` and `str(member["max_mana"])`.' + _ev)
''',
    setup=BAR_SETUP,
    from_setup=("roster",),
    OTHER=OTHER_SHEETS,
    EV5=EV_FIVE,
)

BARS_FOR_EVERYONE = dict(
    id="bars-for-everyone",
    title="Bars for everyone",
    martu=(
        "A loop can call a recipe once for each item: `mana_bar(member)` inside the loop hands the recipe this "
        "pass's sheet. It's like f(x) in math class: one rule, worked out for each x in the table. In the "
        "campaign, a recipe drew one hero's mana bar, and a loop at the bottom called it for everyone. Somebody "
        "else wrote that loop. Now both parts are yours.\n"
        "First the recipe: `mana_bar(hero)` hands back a bar for *any* sheet it's handed. A full block `█` for "
        "each point of mana. An empty block `░` for each point used: the max mana, the most a hero can hold, "
        "minus the mana.\n"
        "Then the loop: call the recipe once for each `member`."
    ),
    example=(
        'def stars(n):\n    return "*" * n\n\nfor count in [2, 4]:\n    print(count, stars(count))\n'
    ),
    example_output="2 **\n4 ****",
    setup=BAR_SETUP,
    names=["mana_bar", "hero", "member", "roster"],
    predict=dict(
        q="Oogrish has 6 mana, and his max is 18. How many empty blocks are in his bar?",
        code="mana = 6\nmax_mana = 18\nused = max_mana - mana\nprint(used)\n",
        choices=["6", "12", "18", "24"],
        answer=1,
        explain="The empty blocks are the mana used: 18 − 6 = 12. The 6 full blocks are his mana.",
    ),
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="the-bar-recipe",
            text=(
                "In the recipe, replace `return \"\"` so `mana_bar` hands back a full block for each point of the "
                "hero's mana. Use `full` and `hero`."
            ),
            dictated=False,
            hints=[
                "Look at `return \"\"`, inside the recipe. There, the sheet is called `hero`. How do you read the "
                "mana from it?",
                "Text times a number repeats it, like a stamp. With other names:\n```python\ndef gauge(lamp):\n"
                "    return \"#\" * lamp[\"oil\"]\n```\nA lamp with 3 oil hands back `###`.",
                "Write `return full * hero[\"mana\"]` in place of `return \"\"`.",
            ],
            checks=[BAR_RET_FULL, BAR_FULL],
            pass_line="Your bar starts with a full block for each point of mana. Next: the empty part.",
        ),
        dict(
            id="the-empty-blocks",
            text=(
                "On your `return` line, glue an empty block onto the bar for each point of mana used: the max mana "
                "minus the mana. Use `empty`, `+` and `hero`."
            ),
            dictated=False,
            hints=[
                "Look at your `return` line: it makes only the full blocks. How many empty blocks come after them, "
                "and what glues them on?",
                "With other names: `return \"#\" * jar[\"left\"] + \".\" * (jar[\"size\"] - jar[\"left\"])`. "
                "The parentheses do the subtracting first, like PEMDAS in math class.",
                "The mana used is the max minus the mana: `hero[\"max_mana\"] - hero[\"mana\"]`. Glue `empty` times "
                "that onto the full part, with `+`.",
                "Write `used = hero[\"max_mana\"] - hero[\"mana\"]` above `return full * hero[\"mana\"]`. Then make "
                "that line `return full * hero[\"mana\"] + empty * used`.",
            ],
            checks=[BAR_RET, BAR_PAR],
            pass_line="Your recipe builds the whole bar: full blocks, then an empty block for each point used. Twelve for Oogrish.",
        ),
        dict(
            id="a-bar-for-everyone",
            text=(
                "In the loop, replace `pass` with a line that prints each member's name and their bar. Call "
                "`mana_bar` with `member`."
            ),
            dictated=False,
            hints=[
                "Look at `pass`, at the bottom, in the loop. Which sheet do you hand the recipe on this pass?",
                "From the Example: `print(count, stars(count))` shows a value, then what the recipe hands back. "
                "The parentheses call the recipe.",
                "Write `print(member[\"name\"], mana_bar(member))` in place of `pass`.",
            ],
            checks=[BAR_LOOP_CHECK],
            pass_line="Four names, four bars, from one recipe and one loop. Bomb Shell: Mine is short. Noted.",
        ),
    ],
    solution=BAR_SOLUTION,
    partials=[_bar('    return full * hero["mana"]', '    pass'), _bar(show="    pass")],
    assemble=dict(
        lines=["def mana_bar(hero):", '    full = "█"', '    empty = "░"', '    used = hero["max_mana"] - hero["mana"]',
               '    return full * hero["mana"] + empty * used', "for member in roster:", BAR_PRINT],
        distractors=['    return full * hero["max_mana"]', '    print(member["name"], mana_bar)',
                     '    used = roster["max_mana"] - roster["mana"]'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Oogrish's bar",
            text=(
                "```text\nmana 6, max 18\n██████░░░░░░░░░░░░\n6 full   12 empty\n```\n"
                "The empty part is the mana used: 18 − 6 = 12."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The loop hands `mana_bar` one sheet: `mana_bar(member)`.\n"
                "2. Inside the recipe, that sheet is called `hero`.\n"
                "3. The recipe builds the bar and hands it back.\n"
                "4. `print` shows the name and the bar. Next member."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "`get_mana_bar(caster)` built `filled = \"█\" * caster[\"mana\"]` and `empty = \"░\" * "
                "(caster[\"max_mana\"] - caster[\"mana\"])`. Your `mana_bar` is the same recipe, with `hero`."
            ),
        ),
        dict(angle="shorter", text="Full times mana, plus empty times (max minus mana). Then call it for each `member`."),
    ],
    bonus=dict(
        by="lucky",
        title="Numbers too",
        text="Lucky wants the numbers. Add ` <mana>/<max_mana>` after each bar, like `Oogrish ██████░░░… 6/18`.",
        hints=[
            "Glue the numbers into one piece of text with `str()` and `\"/\"`, then print it after the bar.",
            "Write `print(member[\"name\"], mana_bar(member), str(member[\"mana\"]) + \"/\" + "
            "str(member[\"max_mana\"]))` in the loop.",
        ],
        checks=[BAR_BONUS],
        solution=_bar(show='    print(member["name"], mana_bar(member), str(member["mana"]) + "/" + str(member["max_mana"]))'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet=(
            'def get_mana_bar(caster):\n    filled = "█" * caster["mana"]\n'
            '    empty = "░" * (caster["max_mana"] - caster["mana"])'
        ),
        why=(
            "You finished `get_mana_bar` in the campaign by replacing two zeros. Now you'll get it: today you "
            "wrote the whole recipe, and the loop that calls it, yourself."
        ),
    ),
    takeaway="A loop can call a recipe for each item: `print(member[\"name\"], mana_bar(member))`.",
    wrong_answers=[
        dict(why="the starter: the recipe hands back empty text", code=BAR_STARTER, fails_at=1,
             message_contains="still hands back empty text"),
        dict(why="every block full (max_mana for mana)", code=_bar('    return full * hero["max_mana"]'), fails_at=1,
             message_contains="Every block came out full"),
        dict(why="the whole sheet multiplied: full * hero (TypeError inside the recipe)",
             code=_bar("    return full * hero", "    pass"), fails_at=1,
             message_contains='Multiply `full` by one number from it, the mana: `hero["mana"]`'),
        dict(why="the sheet's tag used as a name: full * mana (NameError inside the recipe)",
             code=_bar("    return full * mana", "    pass"), fails_at=1,
             message_contains='Inside the recipe, read it from `hero`: `hero["mana"]`'),
        dict(why="no empty blocks", code=_bar('    return full * hero["mana"]'), fails_at=2,
             message_contains="Add the empty blocks"),
        dict(why="empty blocks for the max, not the mana used",
             code=_bar('    return full * hero["mana"] + empty * hero["max_mana"]'), fails_at=2,
             message_contains="blocks long"),
        dict(why="the bar stored under one name, another name handed back (NameError inside the recipe)",
             code=_bar('    bar = full * hero["mana"]\n    return result', "    pass"), fails_at=1,
             message_contains="a name the recipe made"),
        dict(why="empty * used with no used line (NameError in the empty part: the full part is right)",
             code=_bar('    return full * hero["mana"] + empty * used', "    pass"), fails_at=2,
             message_contains="Make `used`"),
        dict(why="the recipe's ingredient name used in the loop's call, with the name (NameError)",
             code=_bar(show='    print(member["name"], mana_bar(hero))'), fails_at=0,
             message_contains="'hero' is not defined"),
        dict(why="the outside name read inside the recipe, before any loop has run (NameError: member)",
             code=_bar('    return full * member["mana"]', "    pass").replace("for member in roster:\n", "")
             .replace("    pass\n", ""), fails_at=1, message_contains="the sheet is called `hero`"),
        dict(why="full blocks for the max, empty blocks after: the bar starts too long",
             code=_bar('    return full * hero["max_mana"] + empty * hero["mana"]', "    pass"), fails_at=1,
             message_contains="started with 8 full blocks, not 3"),
        dict(why="no brackets round the subtraction (TypeError inside the recipe)",
             code=_bar('    return full * hero["mana"] + empty * hero["max_mana"] - hero["mana"]'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the same, with the loop not written yet (the check names the brackets)",
             code=_bar('    return full * hero["mana"] + empty * hero["max_mana"] - hero["mana"]', "    pass"),
             fails_at=1, message_contains="parentheses"),
        dict(why="print for return", code=_bar('    print(full * hero["mana"] + empty * (hero["max_mana"] - hero["mana"]))', "    pass"),
             fails_at=1, message_contains="not `print`"),
        dict(why="the outside name read inside the recipe (member)",
             code=_bar('    return full * member["mana"] + empty * (member["max_mana"] - member["mana"])'), fails_at=1,
             message_contains="same bar"),
        dict(why="a bar typed by hand", code=_bar('    return "██████░░░░░░░░░░░░"'), fails_at=1, message_contains="same bar"),
        dict(why="the blocks swapped", code=_bar('    return empty * hero["mana"] + full * (hero["max_mana"] - hero["mana"])'),
             fails_at=1, message_contains="swapped"),
        dict(why="the key misspelled (KeyError)", code=_bar('    return full * hero["Mana"]', "    pass"), fails_at=1,
             message_contains="spelled exactly"),
        dict(why="no round brackets on the call: the recipe itself printed",
             code=_bar(show='    print(member["name"], mana_bar)'), fails_at=3, message_contains="parentheses"),
        dict(why="no round brackets, glued with + (the TypeError row)",
             code=_bar(show='    print(member["name"] + " " + mana_bar)'), fails_at=0, message_contains="can only concatenate"),
        dict(why="the roster handed to the recipe (TypeError)", code=_bar(show="    print(mana_bar(roster))"), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="the recipe's ingredient name used in the loop (NameError)", code=_bar(show="    print(mana_bar(hero))"),
             fails_at=0, message_contains="'hero' is not defined"),
        dict(why="no name, only the bar", code=_bar(show="    print(mana_bar(member))"), fails_at=3, message_contains="name"),
        dict(why="the print after the loop: it runs once",
             code=_bar(show="    pass") + 'print(member["name"], mana_bar(member))\n', fails_at=3,
             message_contains="printed once"),
        dict(why="four bars typed by hand: one print each",
             code=BAR_DEF + BAR_RETURN + "\n" + "".join(
                 f'print("{s["name"]}", mana_bar(roster[{k}]))\n' for k, s in enumerate(NIGHT_SHEETS)),
             fails_at=3, message_contains="5 heroes"),
        dict(why="the max typed by hand (18, Oogrish's): every bar is 18 blocks long",
             code=_bar('    return full * hero["mana"] + empty * (18 - hero["mana"])'), fails_at=2,
             message_contains="Read the max from the sheet"),
        dict(why="the recipe never called: the loop builds the bar again (right bars, skips the goal)",
             code=_bar(show='    print(member["name"], "█" * member["mana"] + "░" * (member["max_mana"] - member["mana"]))'),
             fails_at=3, message_contains="Call your recipe"),
        dict(why="a name typed in the loop: the same name on every bar",
             code=_bar(show='    print("Oogrish", mana_bar(member))'), fails_at=3, message_contains="this pass's member"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="repeat-string,func-takes-dict,for-each", solo="false", dictates="",
             foreign_names="stars,n,count", par="({mana: 3, max_mana: 8},),({mana: 0, max_mana: 5},),({mana: 7, max_mana: 7},)")
        + "\n"
        "5A-07 (recipe-shaped, D11). Setup: the night roster with max_mana (6/18, 14/20, 3/24, 22/26), so every bar "
        "has both kinds of block. Starter as spec, with the comment split for phone width and `pass` in the loop. "
        "Teacher ruling on the Unit 6 reviews (a cliff for the weaker groups): the recipe is split into full blocks, "
        "then empty blocks, and a predict (Oogrish's 12 empty blocks, the mana used) replaces the pair talk, "
        "before CP1. Lesson 5A goes from 37 to 38 minutes for the extra Run. CP1 [ND] full blocks: RET (a value "
        "comes back, as text; print-for-return and the starter's `\"\"` named) and FULL on three test sheets the "
        "task never uses (mana 3 of 8, 0 of 5 and 7 of 7: the spec's 'mana 0 and full'): each bar starts with "
        "exactly `hero[\"mana\"]` full blocks, and anything after them is the next step's, so the finished recipe "
        "passes. FULL holds PAR-CONST (the same bar for three sheets: the outside `member`, or a typed bar), the "
        "all-full bar (`max_mana`) and the swapped bar. CP1 probes a NameError once: a name the recipe never made "
        "(not `member`, `roster` or `hero`) is set to 0 for one more call, inside the check only, so "
        "`full * hero[\"mana\"] + empty * used` with no `used` line passes CP1 (its full part is right) and fails "
        "CP2 with 'Make `used` inside the recipe'; `bar = ...` then `return result` still fails CP1 ('a name the "
        "recipe made'). The NameError message names `hero` only when the missing name is `member` or `roster`. "
        "CP2 [ND] empty blocks: RET and PAR (exact bars; the max typed by hand, no empty blocks, empties for the "
        "max). The CP2 Teach rung is the teacher's one-line jar return, kept whole as an inline code span (60 "
        "characters; a fence that wide fails the 36-character phone rule in content.test.ts). CP3 [ND]: LOOP on the student's run and on 5 other sheets; each "
        "printed bar must be exactly that member's (blocks read as one run, so a longer bar never passes for a "
        "shorter one). Catches (spec): the missing call brackets, both as the printed recipe (CP3) and as the "
        "TypeError row with `+`. Partials: the full-only recipe, then the whole recipe with the loop's `pass`. "
        "Lucky's box is `get_mana_bar`. PA: the recipe and the loop (distractors: the full-only bar, the call "
        "without brackets, `roster` for `hero`). Bonus: ` <mana>/<max_mana>` after each bar."
    ),
)

# ---- 5A-08 broken-spell-5a ---------------------------------------------------------------------------------

BROKEN_WAKE = 'for member in roster:\nprint(member["name"] + " wakes up.")'
BROKEN_MANA = 'for member in roster:\n    print(roster["name"], member["mana"])'
BROKEN_TOTAL = 'for member in roster:\n    total = 0\n    total = total + member["mana"]'
BROKEN_NAMES = "for member in roster:\n    print(roster)"
GOOD_WAKE = 'for member in roster:\n    print(member["name"] + " wakes up.")'
GOOD_MANA = 'for member in roster:\n    print(member["name"], member["mana"])'
GOOD_TOTAL = 'total = 0\nfor member in roster:\n    total = total + member["mana"]'
GOOD_NAMES = 'for member in roster:\n    print(member["name"])'


def _broken(wake=GOOD_WAKE, mana=GOOD_MANA, total=GOOD_TOTAL, names=GOOD_NAMES):
    return (
        FULL_ROSTER_CODE
        + "# 1. Wake everyone up.\n" + wake + "\n"
        + "# 2. Show each hero's mana.\n" + mana + "\n"
        + "# 3. Add up the mana.\n" + total + '\nprint("Total mana:", total)\n'
        + "# 4. Each name, one per line.\n" + names + "\n"
    )


BROKEN_STARTER = _broken(BROKEN_WAKE, BROKEN_MANA, BROKEN_TOTAL, BROKEN_NAMES)
BROKEN_SOLUTION = _broken()

_BROKEN_HEAD = r'''
def _rows_of(_vals):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('roster')
    assert not _err, _stop(_err, __EV5__)
    return _ns.get('roster'), _rows
'''

BROKEN_WAKE_CHECK = chk(
    "every hero wakes up, on any roster",
    _BROKEN_HEAD + r'''
for _vals, _ev in ((None, ''), ({'roster': __FIVE__}, __EV5__)):
    _r, _rows = _rows_of(_vals)
    _want = [_m['name'] + ' wakes up.' for _m in _r]
    _got = [_l for _l in _rows if _l.endswith('wakes up.')]
    if _got == _want:
        continue
    assert _got, ('No line says `wakes up.` any more. Keep the first loop printing `<name> wakes up.` for each hero, '
                  'with four spaces in front of the print.')
    assert _len(_got) != 1, ('Line 9 is not inside the loop. It ran once. Indent it 4 spaces, so it belongs to the '
                             'loop and runs for every hero.' + _ev)
    assert not (_vals is not None and _len(_got) == 4), (
        'With 5 heroes, 4 lines printed, because the lines are typed in. Let the loop print each line, from '
        '`member["name"]`.' + _ev)
    assert False, ('The first loop does not print `<name> wakes up.` for each hero. Print `member["name"] + " wakes '
                   'up."` inside it.' + _ev)
''',
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

BROKEN_MANA_CHECK = chk(
    "each hero's name and mana print, on any roster",
    _BROKEN_HEAD + r'''
for _vals, _ev in ((None, ''), ({'roster': __FIVE__}, __EV5__)):
    _r, _rows = _rows_of(_vals)
    _want = [_m['name'] + ' ' + _str(_m['mana']) for _m in _r]
    _got = [_l for _l in _rows if _any(_l == _w for _w in _want)]
    if _got == _want:
        continue
    _names = [_m['name'] for _m in _r]
    _same = [_l for _l in _rows if _re.fullmatch(r'[A-Za-z ]+ \d+', _l)]
    assert not (_len(_same) > 1 and _len(_set([_l.rsplit(' ', 1)[0] for _l in _same])) == 1), (
        'Every line shows the same name. Read the name through `member`, the sheet for this pass: '
        '`member["name"]`.' + _ev)
    assert not (_vals is not None and _len(_same) == 4), (
        'With 5 heroes, 4 lines printed. Let the loop print each line, from `member`.' + _ev)
    assert False, ("The second loop does not print each hero's name and mana, like `Oogrish 18`. Print "
                   '`member["name"]` and `member["mana"]`.' + _ev)
''',
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

BROKEN_TOTAL_CHECK = chk(
    "Total mana adds up every hero, on any roster",
    _BROKEN_HEAD + r'''
for _vals, _ev in ((None, ''), ({'roster': __FIVE__}, __EV5__)):
    _r, _rows = _rows_of(_vals)
    _want = 0
    for _m in _r:
        _want = _want + _m['mana']
    _got = [_nums(_l)[-1] for _l in _rows if _l.startswith('Total mana') and _nums(_l)]
    if _got == [_want]:
        continue
    assert _got, ('No line starts with `Total mana`. Put back `print("Total mana:", total)` below the third loop, '
                  'with no spaces in front.')
    if _got == [_r[-1]['mana']]:
        _in, _out = _total_adds('total')
        assert not (_out and not _in), (
            '`total = total + member["mana"]` is not inside the third loop. It ran once, after the loop, and added '
            "only the last hero. Indent it under the third loop's `for` line." + _ev)
        assert False, ('Your total restarts every pass, because `total = 0` is inside the loop. Move `total = 0` '
                       'above the loop.' + _ev)
    assert not (_vals is not None and _got == [88]), (
        'With another roster, the total stayed 88, because it is typed in. Build the total in the loop, from each '
        '`member["mana"]`.' + _ev)
    assert False, ('The total came out ' + _str(_got[-1]) + ', not ' + _str(_want) + ". Add each hero's mana to "
                   "`total` inside the third loop." + _ev)
''',
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

BROKEN_NAMES_CHECK = chk(
    "each name prints once, on its own line",
    _BROKEN_HEAD + r'''
for _vals, _ev in ((None, ''), ({'roster': __FIVE__}, __EV5__)):
    _r, _rows = _rows_of(_vals)
    _names = [_m['name'] for _m in _r]
    _got = [_l for _l in _rows if _l in _names]
    if _got == _names:
        continue
    assert not _any(_l.startswith('[') for _l in _rows), (
        "Each line shows the whole roster. In the last loop, print `member[\"name\"]`, one sheet's name, not "
        "`roster`.")
    assert not _any(_l.startswith('{') for _l in _rows), ('A line shows a whole sheet. Print only the name, '
                                                          '`member["name"]`, not the whole sheet.')
    assert not (_vals is not None and _typed_for()), (
        'Your last loop walks a list of names you typed, so it stays the same when the roster changes. Keep the '
        'last loop as `for member in roster:`, and print `member["name"]`.' + _ev)
    assert not (_vals is not None and _len(_got) == 4), 'With 5 heroes, 4 names printed. Let the loop print each name.' + _ev
    assert False, ('The last loop does not print each name on a line of its own. Print `member["name"]` in it.'
                   + _ev)
''',
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

BROKEN_SPELL_5A = dict(
    id="broken-spell-5a",
    title="Broken spell",
    martu=(
        "This spell has four loops and four bugs. Two are loud: Python stops with an error in the Console. Two "
        "are quiet: your code runs, but shows the wrong thing. *Mend* means fix.\n"
        "For a loud bug, read the box in the Console. Its title says what went wrong, *Python's last line* says "
        "it in Python's words, and the line number says where. Fix that line, then press Run again.\n"
        "When nothing stops, read what your code printed in the Console. Compare it with the note above each "
        "loop, the way you check an answer against the question in math class."
    ),
    names=["roster", "member", "total"],
    pair_talk=(
        "Pair talk: you may hunt these bugs together. One of you reads the title of the error box out loud, and "
        "the other points at the line it names. Each of you fixes it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-the-indent",
            text="Mend line 9 so it belongs to the first loop, the one on line 8.",
            dictated=False,
            hints=[
                "Read the box in the Console. First its title: it says what went wrong. Then Python's last line: "
                "`IndentationError: expected an indented block after 'for' statement on line 8`. The block it "
                "expects is line 9.",
                "Line 9 starts at the left edge. Lines that belong to a `for` start with 4 spaces, like the "
                "points indented under a main point in an outline.",
                "The indent is what puts a line inside the loop:\n```python\nfor jar in jars:\n    print(jar)\n```",
                "Put four spaces in front of `print(member[\"name\"] + \" wakes up.\")` on line 9.",
            ],
            checks=[BROKEN_WAKE_CHECK],
            pass_line="Line 9 is inside the loop now, and Python got further. One loud bug down, yes?",
        ),
        dict(
            id="mend-the-sheet",
            text="Mend line 12 so it reads the name from `member`, this pass's sheet.",
            dictated=False,
            hints=[
                "Read the box in the Console. Its title says what went wrong. Python's last line says it in "
                "Python's words: `TypeError: list indices must be integers or slices, not str`.",
                "Line 12 asks `roster` for a tag (key). `roster` is the whole list, and a list has positions, not "
                "tags. Which variable holds one sheet?",
                "Inside the loop, read the sheet through the loop variable: `jar[\"spice\"]`, never "
                "`jars[\"spice\"]`.",
                "Write `print(member[\"name\"], member[\"mana\"])` in place of `print(roster[\"name\"], member[\"mana\"])`.",
            ],
            checks=[BROKEN_MANA_CHECK],
            pass_line="Two loud bugs down, and nothing stops now. Next: the quiet ones. Read what the Console shows.",
        ),
        dict(
            id="mend-the-total",
            text="Mend the third loop, under `# 3. Add up the mana.`, so `total` adds up every hero's mana.",
            dictated=False,
            hints=[
                "Read what the Console shows: `Total mana: 26`. That's only Lucky's mana, the last hero's. Which "
                "line sets the total back?",
                "Line 15, `total = 0`, is inside the loop, so it runs every pass: the total starts over from 0 each "
                "time. Where should it start, once?",
                "A running total starts once, above its loop:\n```python\ncoins = 0\nfor bag in [5, 2, 4]:\n"
                "    coins = coins + bag\n```",
                "Move `total = 0` above the third loop's `for` line, with no spaces in front.",
            ],
            checks=[BROKEN_TOTAL_CHECK],
            pass_line="`Total mana: 88`, the whole party. Gearshift: That matches my count.",
        ),
        dict(
            id="mend-the-names",
            text="Mend the last loop, under `# 4. Each name, one per line.`, so each name prints on a line of its own.",
            dictated=False,
            hints=[
                "Read the bottom of the Console: it shows the whole roster, four times.",
                "The last line prints `roster`, the whole list, on every pass. Which name holds only this pass's "
                "sheet?",
                "Inside a loop, the loop variable holds one item: `for jar in jars:` then `print(jar[\"spice\"])` "
                "shows one spice a line.",
                "Write `print(member[\"name\"])` in place of `print(roster)`.",
            ],
            checks=[BROKEN_NAMES_CHECK],
            pass_line="All four bugs fixed: two loud, two quiet. You read what your code printed, not only the errors.",
        ),
    ],
    solution=BROKEN_SOLUTION,
    assemble=dict(
        lines=[FULL_ROSTER_CODE.strip(), GOOD_WAKE, GOOD_MANA, GOOD_TOTAL, 'print("Total mana:", total)', GOOD_NAMES],
        distractors=[BROKEN_WAKE, BROKEN_TOTAL, BROKEN_NAMES],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Press Run. Python reads the whole file first, so the indent on line 9 stops it before anything "
                "runs.\n"
                "2. Fix it and press Run again. A new error is good news: Python got further.\n"
                "3. Line 12 stops it next. Fix it.\n"
                "4. Now nothing stops. Read the Console against the note above each loop: two loops print the "
                "wrong thing."
            ),
        ),
        dict(
            angle="picture",
            label="Four bugs, four clues",
            text=(
                "```text\nline 9   no indent   -> stops\nline 12  roster[\"name\"]\n"
                "                     -> stops\nloop 3   = 0 inside  -> 26\nloop 4   print(roster)\n"
                "                     -> lists\n```"
            ),
        ),
        dict(angle="shorter", text="Indent under `for`. Read `member`, not `roster`. Start the total once, above the loop."),
    ],
    takeaway="Indent the body, read `member` not `roster`, and start a total above its loop.",
    wrong_answers=[
        dict(why="the starter: the body not indented (IndentationError first)", code=BROKEN_STARTER, fails_at=0,
             message_contains="expected an indented block"),
        dict(why="indent mended, roster[\"name\"] left (TypeError)",
             code=_broken(GOOD_WAKE, BROKEN_MANA, BROKEN_TOTAL, BROKEN_NAMES), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="the loud bugs mended, total = 0 still inside the loop",
             code=_broken(total=BROKEN_TOTAL, names=BROKEN_NAMES), fails_at=3, message_contains="restarts every pass"),
        dict(why="three mended, the last loop still prints roster", code=_broken(names=BROKEN_NAMES), fails_at=4,
             message_contains="not `roster`"),
        dict(why="mended to roster[0][\"name\"]: the same name every line",
             code=_broken(mana='for member in roster:\n    print(roster[0]["name"], member["mana"])'), fails_at=2,
             message_contains="same name"),
        dict(why="the first loop replaced by four typed prints",
             code=_broken(wake="".join(f'print("{s["name"]} wakes up.")\n' for s in FULL).rstrip("\n")), fails_at=1,
             message_contains="With 5 heroes"),
        dict(why="the wake print moved below the loop, not indented: it runs once",
             code=_broken(wake='for member in roster:\n    pass\nprint(member["name"] + " wakes up.")'), fails_at=1,
             message_contains="It ran once"),
        dict(why="total = 0 deleted instead of moved (NameError)",
             code=_broken(total='for member in roster:\n    total = total + member["mana"]'), fails_at=0,
             message_contains="'total' is not defined"),
        dict(why="the total typed by hand", code=_broken(total="total = 88"), fails_at=3, message_contains="stayed 88"),
        dict(why="the last loop prints the whole sheet", code=_broken(names="for member in roster:\n    print(member)"),
             fails_at=4, message_contains="whole sheet"),
        dict(why="total = 0 moved up, but the adding line moved out of the loop too: it runs once",
             code=_broken(total='total = 0\nfor member in roster:\n    pass\ntotal = total + member["mana"]'), fails_at=3,
             message_contains="It ran once, after the loop"),
        dict(why="the values typed by hand: the last loop runs over typed names",
             code=_broken(names='for name in ["Oogrish", "Gearshift", "Bomb Shell", "Lucky"]:\n    print(name)'),
             fails_at=4, message_contains="names you typed"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="for-each,accumulate,read-traceback", solo="false", dictates="",
             foreign_names="jars,jar,spice") + "\n"
        "5A-08. Spec bugs, one checkpoint each, in the order Python's messages arrive (verified, Python 3.13): the "
        "body that isn't indented (IndentationError, found before anything runs; 'expected an indented block after "
        "'for' statement on line 8'), `print(roster[\"name\"], ...)` (TypeError 'list indices must be integers or "
        "slices, not str'), then the quiet two: `total = 0` inside the loop (Total mana: 26) and a loop over "
        "`roster` that prints `roster`. A crash fails every checkpoint, so the two loud bugs fail at 0 and there "
        "are no partials (as Unit 4's broken spell): a partial that mends only bug 1 still crashes. Every "
        "checkpoint also reruns with 5 other heroes, so a mend that types the lines in is caught. Rung 0 is "
        "'Read Python's last line' for the loud bugs and 'Read what it printed' for the quiet ones. Pairs allowed; "
        "each student mends on their own screen."
    ),
)

# ---- 5A-S solo-5a ------------------------------------------------------------------------------------------

SOLO_A_LINE = '    print(member["name"] + " keeps watch.")'


def _solo_a(body=SOLO_A_LINE):
    return FULL_ROSTER_CODE + "for member in roster:\n" + body + "\n"


SOLO_A_STARTER = _solo_a('    print(roster[member]["name"] + " keeps watch.")')

SOLO_A_CHECK = chk(
    "every hero keeps watch, on any roster",
    r'''
for _vals, _ev in ((None, ''), ({'roster': __FIVE__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, "The line that starts `roster = [` is gone, so Mar'tu can't test your code with other heroes."
    assert not _err, 'With another roster, your code stopped with an error, ' + _err.split(':')[0] + '.' + _ev
    _r = _ns.get('roster')
    _want = [_m['name'] + ' keeps watch.' for _m in _r]
    _got = [_l for _l in _rows if 'keeps watch' in _l]
    if _got == _want:
        continue
    assert _got, 'No line in the Console says `keeps watch`.' + _ev
    assert not _any(_l.startswith('[') or _l.startswith('{') for _l in _got), (
        'A line shows a whole roster or a whole sheet, not a name.' + _ev)
    assert not (_len(_got) > 1 and _len(_set(_got)) == 1), 'Every line names the same hero.' + _ev
    assert not (_vals is not None and _len(_got) == 4), ('Another roster still printed 4 lines, so the lines are '
                                                         'typed in.' + _ev)
    assert _len(_got) != 1, 'Only one line printed: the print runs once.' + _ev
    assert False, 'The lines do not say `<name> keeps watch.` for each hero, in order.' + _ev
''',
    FIVE=OTHER5,
    EV5=EV_FIVE,
)

SOLO_5A = dict(
    id="solo-5a",
    title="Show Mar'tu",
    martu=(
        "One bug, all yours. Read the box in the Console: its title, then Python's last line, then the line it "
        "names. Every hero should keep watch, yes?"
    ),
    solo=True,
    explainer="lean",
    names=["roster", "member"],
    starter=SOLO_A_STARTER,
    checkpoints=[
        dict(
            id="everyone-keeps-watch",
            text="Mend line 8 so the loop prints `<name> keeps watch.` for every hero.",
            dictated=False,
            hints=[
                "Read the box in the Console: its title first, then Python's last line, `TypeError: list indices "
                "must be integers or slices, not dict`.",
                "`member` already holds one sheet. What is `roster[member]` asking the list for?",
                "Inside a loop, read the sheet through the loop variable, never through the whole list.",
            ],
            checks=[SOLO_A_CHECK],
            pass_line="Every hero keeps watch. You did that on your own. Mar'tu: I saw.",
        ),
    ],
    solution=_solo_a(),
    another_way=[
        dict(
            angle="step-by-step",
            text="`member` is a sheet, not a position. A list's positions are numbers.",
        ),
        dict(angle="shorter", text="Read the card in your hand, not the whole stack."),
    ],
    takeaway="On your own: inside a loop over `roster`, read each sheet through `member`.",
    wrong_answers=[
        dict(why="the starter: the item used as an index, roster[member] (TypeError)", code=SOLO_A_STARTER, fails_at=0,
             message_contains="not dict"),
        dict(why="roster[\"name\"] for member[\"name\"] (TypeError)",
             code=_solo_a('    print(roster["name"] + " keeps watch.")'), fails_at=0, message_contains="not str"),
        dict(why="the first sheet every pass", code=_solo_a('    print(roster[0]["name"] + " keeps watch.")'), fails_at=1,
             message_contains="same hero"),
        dict(why="four typed lines", code=FULL_ROSTER_CODE + "".join(f'print("{s["name"]} keeps watch.")\n' for s in FULL),
             fails_at=1, message_contains="typed in"),
        dict(why="the whole sheet printed", code=_solo_a("    print(member)"), fails_at=1, message_contains="says `keeps watch`"),
        dict(why="the sheet glued to text (TypeError)", code=_solo_a('    print(member + " keeps watch.")'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the key without quotes (NameError)", code=_solo_a('    print(member[name] + " keeps watch.")'), fails_at=0,
             message_contains="'name' is not defined"),
        dict(why="the whole roster printed with the words", code=_solo_a('    print(roster, "keeps watch.")'), fails_at=1,
             message_contains="whole roster"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="for-each,list-of-dicts", solo="true", dictates="",
             foreign_names="", seat_b="an unindented loop body (the IndentationError row)") + "\n"
        "SOLO, one bug (C6), explainer='lean'. Seat A (and anyone solo): `print(roster[member][\"name\"] + ...)` "
        "inside the loop, the item used as an index (TypeError 'list indices must be integers or slices, not "
        "dict'): a class slip no step has had them mend (teacher ruling on the Unit 6 reviews; the old "
        "`roster[\"name\"]` bug was mended with a partner in 5A-08 CP2 two minutes earlier, and stays a wrong "
        "answer here). The skills are unchanged, so the map tick stays. The lean explainer names the kind of slip "
        "and the line, and Python's last line "
        "stays on screen. Check: the student's run prints `<name> keeps watch.` for the four heroes in order, and "
        "a rerun with 5 other heroes follows (typed lines fail). Lean messages name the slip and keep the evidence "
        "bracket, with no fix. No Assemble rung (as Units 3-5's SOLOs): its pieces would hand over the mended line. "
        "Seat B would get an unindented body once pair mode ships. Recorded, never blocking, "
        "never shown to a partner. The pass line is Unit 2's ruled SOLO wording."
    ),
)

LESSON_5A = dict(
    kind="lesson",
    id="for-each-yes",
    title="For Each, Yes?",
    minutes=38,
    summary=(
        "Make Python repeat lines for each item in a list. Show every gap and every hero, add up the mana, and see "
        "how fast the gaps shrink."
    ),
    notes=(
        "Lesson 5A (CC: 5A-R, 5A-01, 5A-02, 5A-03, 5A-07, 5A-S; the rest SC). Preceded by 5a-remembers. Exactly one "
        "SOLO (solo-5a). Every checkpoint is non-dictated: 5A-01 to 5A-06, 5A-07 (all three), 5A-08 (all four) "
        "and 5A-S. No checkpoint is dictated now (5A-01 and 5A-05 changed by teacher ruling on the Unit 6 "
        "reviews). 38 minutes (37 in the spec): 5A-07's predict replaces its pair talk, and its full / empty "
        "split costs about one extra Run. Campaign links are 'you have seen this': the spell "
        "book's and the mana bars' bottom loops (`for member in party.members:`), `get_mana_bar`, the chalk wall "
        "and the hold-the-barrier arithmetic."
    ),
    exercises=[
        PREDICT_THE_LOOP, EACH_MARK, EACH_MEMBER, RUNNING_TOTAL, HOW_MUCH_EACH_GAP_SHRANK, LOOP_WITH_A_CHECK,
        BARS_FOR_EVERYONE, BROKEN_SPELL_5A, SOLO_5A,
    ],
)

# =============================================================================================
# Mar'tu remembers... (5b-remembers)
# =============================================================================================

REMEMBERS_5B = dict(
    kind="quiz",
    id="5b-remembers",
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from Units 5 and 3, before the lesson While the Clock Ticks. Nothing is scored.",
    notes=(
        "meta: path=SC; unscored warm-up shown inline before Lesson 5B. Q1 is the spec's Unit 5 item, "
        "`\"Glow\" in spell_book`, with the value-not-key twin (`2 in spell_book`). Q2 is added for the 2.1 rule "
        "(from Unit 4 on, one warm-up item is always def/return): Unit 3's `max_mana_for`, with Bomb Shell's real "
        "affinity (12 -> 24). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="glow-in-the-book",
            q="What will this print?",
            code='spell_book = {\n    "Glow": 2,\n    "Warm Hands": 3,\n}\nprint("Glow" in spell_book)\nprint(2 in spell_book)\n',
            choices=["True\nTrue", "False\nTrue", "True\nFalse", "2\nFalse"],
            answer="True\nFalse",
            explain=(
                "`in` looks at the tags (keys) only. `\"Glow\"` is a tag, so `True`. 2 is a value, not a tag, so "
                "`False`."
            ),
        ),
        dict(
            type="predict",
            id="max-mana-for",
            q="What will this print?",
            code="def max_mana_for(affinity):\n    return affinity * 2\n\nprint(max_mana_for(12))\n",
            choices=["12", "affinity * 2", "None", "24"],
            answer="24",
            explain=(
                "The call hands over 12, so `affinity` is 12. The recipe hands back 12 * 2, which is 24: Bomb "
                "Shell's max mana."
            ),
        ),
    ],
)

# =============================================================================================
# Lesson 5B "While the Clock Ticks"
# =============================================================================================

# ---- 5B-01 countdown ---------------------------------------------------------------------------------------

COUNT_LOOP = "hours_left = 5\nwhile hours_left > 0:\n    print(hours_left)\n    hours_left = hours_left - 1\n"
COUNT_NOTE = "# After the loop: print Burst!\n"
# Hidden setup: the blank is a name that is False, so the starter's `while ___:` runs safely (no passes) until
# the student fills it, and CP1 can pass with the blank still there. Reruns run the setup too.
COUNT_SETUP = "___ = False\n"


def _turn(test="___"):
    """The candles loop below the burst line: the student fills the `while` question."""
    return "\n# Your turn:\ncandles = 3\nwhile " + test + ":\n    print(candles)\n    candles = candles - 1\n"


COUNT_TURN = _turn()
COUNT_STARTER = COUNT_LOOP + COUNT_NOTE + COUNT_TURN


def _count(loop=COUNT_LOOP, tail='print("Burst!")\n', turn=COUNT_TURN):
    return loop + COUNT_NOTE + tail + turn


COUNT_SOLUTION = _count(turn=_turn("candles > 0"))

COUNTDOWN_CHECK = chk(
    "it counts down to 1, then Burst! prints once (any start)",
    r"""
# Only the countdown counts here: the candles loop below it (lines that mention `candles` or the blank) is
# left out of these runs, so its numbers are never read as numbers after the burst.
_PARTS = ('candles', '___')
_whiles = [_n for _top in _top_part(_parsed(), _PARTS) for _n in _ast.walk(_top) if _tn(_n) == 'While']
for _start in (5, 3):
    _ev = " Mar'tu tested your code with a test number, `hours_left = " + _str(_start) + "`."
    _ns, _rows, _err, _miss = _rerun({'hours_left': _start}, _drop=_PARTS)
    assert not _miss, _keep('hours_left')
    assert not _err, _stop(_err, _ev, 'Make your code work for another start too.')
    _want = list(_rng(_start, 0, -1))
    # The countdown is the last whole number on each line before the burst (so `Hours left: 5` is fine), and
    # the burst is a line that starts with `Burst!` (so `Burst! Everyone inside!` is fine, and so is a line after it).
    _bi = [_i for _i, _l in _enum(_rows) if _l.startswith('Burst!')]
    _counts = [_nums(_l)[-1] for _l in _rows[:_bi[0] if _bi else _len(_rows)] if _nums(_l)]
    _after = [_l for _l in _rows[_bi[0] + 1:] if _nums(_l)] if _bi else []
    if _len(_bi) == 1 and _counts == _want and not _after:
        continue
    _near = [_l for _l in _rows if not _l.startswith('Burst!') and _l.lower().strip('!. ').startswith('burst')]
    assert not _near, ('Your burst line is not exactly `Burst!`. Print it with a capital B and `!` at the end: every '
                       'letter and mark counts.')
    assert _bi, ('No line says `Burst!`. Add `print("Burst!")` under the note `# After the loop: print Burst!`, with '
                 'no spaces in front.' + _ev)
    assert _len(_bi) == 1, (
        '`Burst!` printed every pass, because its line is inside the loop. Take the spaces off the front of '
        '`print("Burst!")`, so it runs once, after the loop.' + _ev)
    assert not _after, ('A number printed after `Burst!`. Put `print("Burst!")` below the loop, so it prints after '
                        'the countdown.' + _ev)
    assert _counts != list(_rng(_start - 1, -1, -1)), (
        'Your countdown printed ' + _str(_start - 1) + ' down to 0, because it takes 1 away before it prints. '
        'Print `hours_left` before you take 1 away: keep `print(hours_left)` above the `- 1` line.' + _ev)
    assert 0 not in _counts, ('Your loop ran one pass too many, and printed 0. Keep `while hours_left > 0:`.' + _ev)
    assert not (_start == 3 and _counts == [5, 4, 3, 2, 1]), (
        'With another start, your code still printed 5 to 1, so the countdown is typed in. Keep the `while` loop '
        'that counts down from `hours_left`.' + _ev)
    assert _whiles or _len(_counts) != 1, (
        'Only ' + _str(_counts[0]) + ' printed, because an `if` runs its lines once. Use `while`: it repeats its '
        'lines while its question is `True`.' + _ev)
    assert False, ('Your countdown does not go from `hours_left` down to 1, then `Burst!` once. Count down with the '
                   'loop, then print `Burst!` after it.' + _ev)
""",
    setup=COUNT_SETUP,
)

CANDLES_CHECK = chk(
    "the candles count down to 1 (any start)",
    r"""
_blank = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'While' and _tn(_n.test) == 'Name' and _n.test.id == '___']
assert not _blank, ('Your `while ___:` still has the blank in it. Write a question in place of `___`, like the '
                    "countdown's `hours_left > 0`.")
# The countdown's own lines: a run without the candles part (the top-level lines that mention `candles` or the
# blank). The candles' lines are what the whole program prints after the lines it shares with that run (a
# `Burst!` printed at the very end has no number, so it is never read as a candle).
_b0, _base, _berr, _bm = _rerun({}, _drop=('candles', '___'))
for _start in (3, 4, 2):
    _ev = '' if _start == 3 else " Mar'tu tested your code with a test number, `candles = " + _str(_start) + "`."
    _ns, _rows, _err, _miss = _rerun({'candles': _start})
    assert not _miss, _keep('candles')
    assert not _err, _stop(_err, _ev, 'Make your code work for another start too.')
    _k = 0
    while not _berr and _k < _len(_base) and _k < _len(_rows) and _rows[_k] == _base[_k]:
        _k = _k + 1
    _rows = _rows[_k:]
    _want = list(_rng(_start, 0, -1))
    _got = [_nums(_l)[-1] for _l in _rows if _nums(_l)]
    if _got == _want:
        continue
    # `if candles > 0:` for `while`: it asks once, so only the start prints (the class's if/while mix-up).
    _asks = lambda _k: [_n for _n in _ast.walk(_parsed()) if _tn(_n) == _k
                        and _any(_tn(_x) == 'Name' and _x.id == 'candles' for _x in _ast.walk(_n.test))]
    assert not (_asks('If') and not _asks('While')), (
        'Your code checks the candles once, with `if`, so only ' + _str(_start) + ' prints. Use `while`: it asks '
        'again before every pass.' + _ev)
    assert _got, ('Your loop never ran: its question was `False` at the start. Ask a question that is `True` while '
                  'candles are left, as `hours_left > 0` is.' + _ev)
    assert 0 not in _got, ('Your loop ran one pass too many, and printed 0. Ask whether any candles are left, as '
                           '`hours_left > 0` does.' + _ev)
    assert not (_got == _want[:_len(_got)] and _len(_got) < _len(_want)), (
        'Your loop stopped at ' + _str(_got[-1]) + ', not 1. Let the loop run while any candles are left, down to '
        '1.' + _ev)
    assert False, ('The candles do not count down to 1. Fill the `___` so the loop runs one pass for each candle.'
                   + _ev)
""",
    setup=COUNT_SETUP,
)

COUNTDOWN = dict(
    id="countdown",
    title="Countdown",
    martu=(
        "A [[while loop]] repeats its indented lines *while* a question is `True`, like *keep stirring while the "
        "soup is cold*. `while hours_left > 0:` asks its question before every pass. `True`? Run the indented "
        "lines, then ask again. `False`? Leave the loop, and go on with the line below it. An `if` asks once. A "
        "`while` asks again before every pass.\n"
        "Inside, `hours_left = hours_left - 1` makes the number smaller each pass, so in the end the answer is "
        "`False`. Then comes the burst, the blast from the leylines.\n"
        "Predict, then press Run. Try this if you like (it's not a step): change the 5 on line 1 to 3, predict "
        "again, and press Run."
    ),
    introduces=["node:While"],
    example='torches = 2\nwhile torches > 0:\n    print("A torch burns out.")\n    torches = torches - 1\nprint("Dark.")\n',
    example_output="A torch burns out.\nA torch burns out.\nDark.",
    setup=COUNT_SETUP,
    names=["hours_left", "candles"],
    predict=dict(
        q="Before you press Run: what will the loop print?",
        code=COUNT_LOOP,
        choices=["5\n4\n3\n2\n1\n0", "5\n4\n3\n2\n1", "4\n3\n2\n1\n0", "5\n5\n5\n5\n5"],
        answer=1,
        explain=(
            "```text\nhours_left  > 0?   prints\n5           True   5\n4           True   4\n3           True   3\n"
            "2           True   2\n1           True   1\n0           False  (stops)\n```\n"
            "At 0, the question is `False`, so 0 never prints."
        ),
    ),
    tracer=True,
    starter=COUNT_STARTER,
    checkpoints=[
        dict(
            id="burst-after-the-loop",
            text=(
                "Under the note `# After the loop: print Burst!`, type `print(\"Burst!\")` with no spaces in front, "
                "so it runs once, after the loop."
            ),
            dictated=True,
            hints=[
                "Look at the note `# After the loop: print Burst!`. Your line goes under it, at the left edge. Why "
                "does the left edge keep it out of the loop?",
                "A line with no indent runs after the loop is done:\n```python\nwhile torches > 0:\n"
                "    torches = torches - 1\nprint(\"Dark.\")\n```\n`Dark.` prints once, at the end.",
                "Write `print(\"Burst!\")` under `# After the loop: print Burst!`, with no spaces in front.",
            ],
            checks=[COUNTDOWN_CHECK],
            pass_line="Your countdown ran 5, 4, 3, 2, 1, then `Burst!` once. Mar'tu: Everyone inside, yes?",
        ),
        dict(
            id="candles-count-down",
            text="Under `# Your turn:`, replace `___` in `while ___:` with a question, so the candles count down 3, 2, 1.",
            dictated=False,
            hints=[
                "Look at `while ___:` under `# Your turn:`. A `while` line holds a question, like `hours_left > 0` "
                "in the loop above. What question keeps the candles going?",
                "Ask the question the countdown asks: are any left? `hours_left > 0` means *more than 0 hours are "
                "left*.",
                "Write `candles > 0` in place of `___`.",
            ],
            checks=[CANDLES_CHECK],
            pass_line="Three candles, three passes, then the loop stopped. You wrote the question yourself.",
        ),
    ],
    solution=COUNT_SOLUTION,
    partials=[_count()],
    assemble=dict(
        lines=["hours_left = 5", "while hours_left > 0:", "    print(hours_left)", "    hours_left = hours_left - 1",
               'print("Burst!")', "candles = 3", "while candles > 0:", "    print(candles)", "    candles = candles - 1"],
        distractors=['    print("Burst!")', "while candles >= 0:", "if hours_left > 0:"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Trace table",
            text=(
                "```text\nhours_left  > 0?   prints\n5           True   5\n4           True   4\n"
                "3           True   3\n2           True   2\n1           True   1\n0           False  -\n```\n"
                "Then the loop is over, and the line below it runs: `Burst!`."
            ),
        ),
        dict(
            angle="everyday",
            label="A race start",
            text=(
                "Three, two, one, go! You count while there are numbers left. When you reach zero, you stop "
                "counting and shout once. The shout is not part of the counting."
            ),
        ),
        dict(
            angle="in Tor",
            label="The Ley Clock",
            text=(
                "The Ley Clock counts down to the next burst. Its hand creeps toward the arc, and every hour it "
                "asks the same question: are we there yet? While the answer is no, the hand moves on. Then the "
                "burst."
            ),
        ),
        dict(angle="shorter", text="`while` asks, runs, changes, asks again. When the answer is `False`, it stops."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="ley-clock",
        why=(
            "You watched the Ley Clock count down to a burst in the campaign. Now you'll get it: a `while` loop is "
            "that clock. It keeps ticking until its question says stop."
        ),
    ),
    takeaway="`while question:` repeats its lines while the question is `True`. Something inside must change it.",
    wrong_answers=[
        dict(why="the starter: no Burst!", code=COUNT_STARTER, fails_at=1, message_contains='Add `print("Burst!")`'),
        dict(why="Burst! indented inside the loop: it prints every pass",
             code=_count(loop=COUNT_LOOP + '    print("Burst!")\n', tail=""), fails_at=1, message_contains="every pass"),
        dict(why=">= 0: one pass too many (off by one)", code=_count(loop=COUNT_LOOP.replace("> 0", ">= 0")), fails_at=1,
             message_contains="printed 0"),
        dict(why="if for while: the lines run once",
             code=_count(loop=COUNT_LOOP.replace("while", "if")), fails_at=1, message_contains="an `if` runs its lines once"),
        dict(why="the countdown typed by hand",
             code="hours_left = 5\n" + "".join(f"print({n})\n" for n in range(5, 0, -1)) + COUNT_NOTE
             + 'print("Burst!")\n' + COUNT_TURN,
             fails_at=1, message_contains="still printed 5 to 1"),
        dict(why="burst in small letters", code=_count(tail='print("burst!")\n'), fails_at=1, message_contains="capital B"),
        dict(why="Burst! above the loop", code='print("Burst!")\n' + COUNT_STARTER, fails_at=1, message_contains="below the loop"),
        dict(why="the update removed: the loop never ends (prints forever)",
             code=_count(loop=COUNT_LOOP.replace("    hours_left = hours_left - 1\n", "")), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update outside the loop: it never ends",
             code=_count(loop=COUNT_LOOP.replace("    hours_left = hours_left - 1\n", "hours_left = hours_left - 1\n")),
             fails_at=0, message_contains="printed more than"),
        dict(why="the update moved above the print: it prints 4 down to 0",
             code=_count(loop="hours_left = 5\nwhile hours_left > 0:\n    hours_left = hours_left - 1\n"
                              "    print(hours_left)\n"),
             fails_at=1, message_contains="before you take 1 away"),
        dict(why="the candles: the blank left in place (CP1 done)", code=_count(), fails_at=2,
             message_contains="in place of `___`"),
        dict(why="the candles: >= 0, one pass too many (prints 0)", code=_count(turn=_turn("candles >= 0")),
             fails_at=2, message_contains="printed 0"),
        dict(why="the candles: > 1, the loop stops at 2", code=_count(turn=_turn("candles > 1")), fails_at=2,
             message_contains="stopped at 2"),
        dict(why="the candles: if for while (asks once: only 3 prints)",
             code=_count(turn=_turn("candles > 0").replace("while candles", "if candles")), fails_at=2,
             message_contains="checks the candles once, with `if`"),
        dict(why="the candles: a question that is False at the start (the loop never runs)",
             code=_count(turn=_turn("candles < 0")), fails_at=2, message_contains="never ran"),
        dict(why="the candles: a question that never becomes False (candles < 10): prints forever, stopped at once",
             code=_count(turn=_turn("candles < 10")), fails_at=0, message_contains="printed more than"),
        dict(why="the candles: a question about the countdown, not the candles (hours_left is 0 by then)",
             code=_count(turn=_turn("hours_left > 0")), fails_at=2, message_contains="never ran"),
        dict(why="the candles filled, the burst not written yet: the countdown's step comes first",
             code=_count(tail="", turn=_turn("candles > 0")), fails_at=1, message_contains='Add `print("Burst!")`'),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="while-loop", solo="false", dictates="1",
             foreign_names="torches", stages="P,R,I", trace="static trace table (predict explain, another_way), tracer=True")
        + "\n"
        "5B-01. Intro node:While. The starter is a countdown that ENDS (5B-02 is where a loop never ends), so the "
        "first while loop a student runs is safe. Predict (P), Run (R), then the Investigate prompt in the Learn "
        "text (change 5 to 3). CP1 [D]: `Burst!` once, after the loop. Checks: OUT and CMB together, by rerunning "
        "with the check's own `hours_left` (5, then 3), so a student who left 3 in place after the Investigate "
        "still passes (Unit 2's first-if ruling). Catches: Burst! inside the loop (every pass), `>= 0` (prints 0), "
        "`if` for `while`, a typed countdown (CMB), and the two endless loops, which print, so they stop in "
        "milliseconds with TooMuchOutput (see the file header). CP2 [ND] (teacher ruling on the Unit 6 reviews: one "
        "`while` blank to fill): *Your turn* below the burst line, `candles = 3` / `while ___:` with the print and "
        "the update already written. A hidden setup `___ = False` (2.12 rule 3: a blank, not data) keeps the "
        "untouched blank safe, so CP1 passes with it in place and the candles loop simply never runs; the "
        "reruns run that setup too. The two parts are checked apart: CP1's reruns leave out every top-level "
        "line that mentions `candles` or `___` (`_top_part()`), so the candles' numbers are never read as numbers "
        "after the burst; CP2 reruns the whole program with `candles` 3, 4 and 2 and reads only what prints "
        "after the countdown's own lines (a question about `hours_left` there never runs: 'never ran'). "
        "CP2 names the blank left in place first, then `>= 0` (prints 0), `> 1` (stops at 2) and a question "
        "that is False at the start (never runs). The candles loop prints inside its body, so a question that "
        "never turns False (`candles < 10`) stops in milliseconds with TooMuchOutput, like the file's other "
        "endless loops (fails at 0, proven). The Example's name is now `torches`, so the task's `candles` "
        "is not an Example name (2.12 rule 5)."
    ),
)

# ---- 5B-02 the-loop-that-never-ends ------------------------------------------------------------------------

GLUG_HEAD = 'glug = 3\nwhile glug > 0:\n    print("Sip. Glug left:", glug)\n'
GLUG_TAIL = 'print("The canteen is empty.")\n'
GLUG_STARTER = GLUG_HEAD + GLUG_TAIL


def _glug(update="    glug = glug - 1\n", head=GLUG_HEAD, tail=GLUG_TAIL):
    return head + update + tail


GLUG_SOLUTION = _glug()

GLUG_CHECK = chk(
    "Lucky sips until the glug runs out, then the canteen is empty (any amount)",
    r'''
_t0 = _parsed()
_whiles = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'While']
for _start in (3, 5):
    _ev = " Mar'tu tested your code with a test number, `glug = " + _str(_start) + "`."
    _ns, _rows, _err, _miss = _rerun({'glug': _start})
    assert not _miss, _keep('glug')
    assert not _err, _stop(_err, _ev, 'Make your code work for another amount too.')
    _want = ['Sip. Glug left: ' + _str(_i) for _i in _rng(_start, 0, -1)] + ['The canteen is empty.']
    if _rows == _want:
        continue
    _sips = [_nums(_l)[-1] for _l in _rows if 'left' in _l and _nums(_l)]
    _empty = [_l for _l in _rows if 'empty' in _l]
    assert _len(_empty) <= 1, (
        '`The canteen is empty.` printed every pass, because its line is inside the loop. Take the spaces off the '
        'front of `print("The canteen is empty.")`, so it runs once, after the loop.' + _ev)
    assert _sips, ('No line shows a sip. Put back the `while` loop and its `print` line, the way they were at the '
                   'start.')
    assert not (_start == 5 and _sips == [3, 2, 1]), (
        'With `glug = 5`, your code still took 3 sips, so the sips are typed in. Keep the loop, so it works for any '
        'amount.' + _ev)
    assert _whiles, ('Your code takes one sip and stops, because an `if` runs once. Keep `while`: it keeps going '
                     'while `glug > 0` is `True`.' + _ev)
    assert _sips != list(_rng(_start - 1, -1, -1)), (
        'Your loop printed ' + _str(_start - 1) + ' down to 0, because it takes the sip before the print. Put '
        '`glug = glug - 1` under the print, so each line shows the glug before the sip.' + _ev)
    assert 0 not in _sips, 'The loop ran one pass too many: it printed 0. Keep `while glug > 0:`.' + _ev
    assert _sips != [_start], 'The loop stopped after 1 pass. Take one sip at a time: `glug = glug - 1`.' + _ev
    assert _len(_sips) >= _start, 'Some sips were skipped. Take one sip at a time: `glug = glug - 1`.' + _ev
    assert _empty, ("The Console doesn't show `The canteen is empty.` Put `print(\"The canteen is empty.\")` back "
                    "below the loop, with no spaces in front.")
    assert False, ('Lucky does not take one sip each pass. Take one sip each pass with `glug = glug - 1`, inside '
                   'the loop.' + _ev)
''',
)

LOOP_THAT_NEVER_ENDS = dict(
    id="the-loop-that-never-ends",
    title="The loop that never ends",
    martu=(
        "An [[infinite loop]] is a loop that never stops, because its question never turns `False`. On a number "
        "line, it's like trying to reach 0 without ever taking a step. Lucky's canteen holds 3 sips of glug, his "
        "drink. Nothing inside his loop changes `glug`, so `glug > 0` is `True` forever. Press Run, and watch.\n"
        "The site won't let it freeze your screen. A loop that prints too much is stopped with *printed more than "
        "200,000 characters*. A loop that prints nothing is stopped after 5 seconds. Both mean the same thing: "
        "find the line inside the loop that should change its question. *Mend* means fix."
    ),
    names=["glug"],
    pair_talk="Pair talk: before you fix it, tell your partner why `glug > 0` never turns `False`.",
    starter=GLUG_STARTER,
    checkpoints=[
        dict(
            id="mend-the-glug-loop",
            text=(
                "Mend the loop so Lucky runs out of glug: 3 sips, then `The canteen is empty.` The fix is one new "
                "line inside the loop."
            ),
            dictated=False,
            hints=[
                "Read the box in the Console. Its title says what went wrong, and Python's last line says: "
                "`TooMuchOutput: This program printed more than 200,000 characters, so it was stopped.`",
                "The loop asks `glug > 0` every pass. Which line inside the loop changes `glug`? There is none.",
                "In the countdown, `candles = candles - 1` sat inside the loop, so the loop could end. Which line "
                "should do that job here?",
                "Write `glug = glug - 1` on the line after `print(\"Sip. Glug left:\", glug)`, with four spaces in front.",
            ],
            checks=[GLUG_CHECK],
            pass_line="Three sips, then the empty canteen: your loop ends now. Lucky: Smells terrible. Worth it.",
        ),
    ],
    solution=GLUG_SOLUTION,
    assemble=dict(
        lines=["glug = 3", "while glug > 0:", '    print("Sip. Glug left:", glug)', "    glug = glug - 1",
               'print("The canteen is empty.")'],
        distractors=["glug = glug - 1", "    glug = glug + 1", "    glug = 0"],
    ),
    another_way=[
        dict(
            angle="why",
            label="What the limit is",
            text=(
                "A loop that never ends would freeze your screen. So the site stops a run in one of two ways: after "
                "200,000 characters of printing, or after 5 seconds. Either one means the loop's question never "
                "became `False`. Look inside the loop for the line that should change it."
            ),
        ),
        dict(
            angle="picture",
            label="The same question, forever",
            text=(
                "```text\nglug  glug > 0?\n3     True\n3     True\n3     True\n... forever\n```\n"
                "With no change inside the loop, every pass asks the same question about the same number."
            ),
        ),
        dict(
            angle="everyday",
            label="Are we there yet?",
            text=(
                "Someone in the back seat asks: are we there yet? If the car never moves, the answer is always no, "
                "and the asking never stops. The line that changes `glug` is the car moving."
            ),
        ),
        dict(angle="shorter", text="Every `while` loop needs a line inside it that moves toward stopping."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "Every cast in `cast_spell` took mana away with this line. Picture a loop that casts while the caster "
            "has mana. Without this line the mana never drops, so that loop would never end."
        ),
    ),
    takeaway="A while loop needs a line inside it that changes the question's value, or it never ends.",
    wrong_answers=[
        dict(why="the starter: no update, the loop never ends (prints forever)", code=GLUG_STARTER, fails_at=0,
             message_contains="printed more than"),
        dict(why="the update outside the loop: it never ends", code=_glug(update="glug = glug - 1\n"), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update the wrong way: it never ends", code=_glug(update="    glug = glug + 1\n"), fails_at=0,
             message_contains="printed more than"),
        dict(why="glug = 0 inside: one sip", code=_glug(update="    glug = 0\n"), fails_at=1, message_contains="after 1 pass"),
        dict(why="two sips at a time", code=_glug(update="    glug = glug - 2\n"), fails_at=1, message_contains="skipped"),
        dict(why="if for while (no loop at all)", code=_glug(head=GLUG_HEAD.replace("while", "if")), fails_at=1,
             message_contains="Keep `while`"),
        dict(why="the empty line indented: it prints every pass",
             code=_glug(update='    glug = glug - 1\n    print("The canteen is empty.")\n', tail=""), fails_at=1,
             message_contains="every pass"),
        dict(why="the sips typed by hand",
             code='glug = 3\n' + "".join(f'print("Sip. Glug left:", {n})\n' for n in (3, 2, 1)) + GLUG_TAIL, fails_at=1,
             message_contains="still took 3 sips"),
        dict(why=">= 0: one sip too many", code=_glug(head=GLUG_HEAD.replace("> 0", ">= 0")), fails_at=1,
             message_contains="printed 0"),
        dict(why="the update above the print: it shows 2, 1, 0",
             code='glug = 3\nwhile glug > 0:\n    glug = glug - 1\n    print("Sip. Glug left:", glug)\n' + GLUG_TAIL,
             fails_at=1, message_contains="under the print"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="while-loop,infinite-loop", solo="false", dictates="",
             foreign_names="") + "\n"
        "5B-02 (spec: the glug loop forgets `glug = glug - 1`; run it, read the limit row, fix it). The starter "
        "PRINTS inside the loop, so its Run stops in milliseconds with TooMuchOutput ('This program printed more "
        "than 200,000 characters, so it was stopped.'), and the site shows its always-full 'Printing forever?' "
        "explainer; rung 0 quotes that line, and a Teach rung (teacher ruling on the Unit 6 reviews) points back "
        "to Countdown's `candles = candles - 1`, the update inside the loop. WT 'What the step limit is' is the "
        "'why' angle, written as what the "
        "site really does (an output limit and a 5-second limit; there is no line-count limit), and the Learn "
        "text says the same. CP1 [ND]. Checks: OUT + CMB via reruns with `glug` 3 and 5 (the rerun itself is "
        "guarded, so a loop that only never ends with 5 cannot hang the check). Catches (each proven): no update "
        "(the starter), the update outside the loop, the update the wrong way (all three print forever and fail "
        "at 0 with the honest message), `glug = 0`, two at a time, `if` for `while`, the empty line every pass, "
        "typed sips, `>= 0`. The campaign link is the hold-the-barrier mana line, the update the campaign used."
    ),
)

# ---- 5B-03 stop-at-the-first -------------------------------------------------------------------------------

FIRST_HEAD = WALL_LINE + "for gap in chalk_wall:\n"
FIRST_NOTE = "    # 1. If gap is under 45:\n    # 2.   print it, then break.\n"
FIRST_STARTER = FIRST_HEAD + FIRST_NOTE + "    pass\n"
FIRST_BODY = "    if gap < 45:\n        print(gap)\n        break"


def _first(body=FIRST_BODY, head=FIRST_HEAD, tail=""):
    return head + FIRST_NOTE + body + "\n" + tail


FIRST_SOLUTION = _first()
FIRST_WALL = [50, 49, 43, 40, 38]

FIRST_CHECK = chk(
    "exactly one line prints: the first gap under 45 (any wall)",
    r'''
_t0 = _parsed()
_fors = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For']
_top_break = [_n for _f in _fors for _n in _f.body if _tn(_n) == 'Break']
_early = False
for _n in _ast.walk(_t0):
    _b = _B.getattr(_n, 'body', None)
    if _tn(_b) == 'list':
        _k = [_tn(_x) for _x in _b]
        if 'Break' in _k and _k.index('Break') < _len(_k) - 1:
            _early = True
# Only lines with a number count, so `First gap under 45: 44` is fine, and so is a `Done.` after the loop.
_own = [_l for _l in _lines() if _nums(_l)]
for _vals, _ev in ((None, ''), ({'chalk_wall': __W__}, __EVW__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_err, _ev, 'Make your code work for another wall too.')
    _w = _ns.get('chalk_wall')
    assert _tn(_w) == 'list', _keep('chalk_wall')
    _first = [_g for _g in _w if _g < 45][:1]
    _rows = [_l for _l in _rows if _nums(_l)]
    if _len(_rows) == 1 and _nums(_rows[0])[-1:] == _first:
        continue
    assert not _any('[' in _l for _l in _rows), 'A line shows the whole wall. Print `gap`, one gap, not the whole wall.' + _ev
    if not _rows:
        assert not _top_break, ('Nothing printed, because `break` is not inside the `if`: the loop stopped at the very '
                                'first gap. Put `break` inside the `if`, under the print.')
        assert not _early, ('Nothing printed, because Python leaves the loop at `break`, so a line under it never '
                            'runs. Put the print above `break`.')
        assert _vals is None, ('Another wall printed nothing. Test each gap with `if gap < 45:`, so the loop finds the '
                               'first gap under 45 on any wall.' + _ev)
        assert False, 'Nothing printed. Inside the `if`, print the gap, then `break`.' + _ev
    assert not _typed_for(), ('Your `for` line walks a list you typed out, so it will not change when the wall does. '
                              'Loop over the wall by its name: `for gap in chalk_wall:`.' + _ev)
    assert not (_vals is not None and _rows == _own), (
        'Another wall printed the same line, so the gap is typed in. Print `gap`, the loop variable, so it works '
        'for any wall.' + _ev)
    # `while gap < 45:` for `if`, with `break` inside it: `break` leaves only the `while`, and the `for` goes on.
    _inner = [_w for _f in _fors for _w in _ast.walk(_f) if _tn(_w) == 'While'
              and _any(_tn(_b) == 'Break' for _b in _ast.walk(_w))]
    assert not _inner, ('Your `while` sits inside the `for`, so `break` leaves only the `while`, and the `for` goes '
                        'on to the next gap. Use `if`: it asks once for each gap.' + _ev)
    assert _len(_rows) == 1 or _uses('node:Break'), (
        'Your loop printed ' + _str(_len(_rows)) + ' gaps, because nothing stops it. Add `break` under the print, '
        'inside the `if`, so the loop stops at the first one.' + _ev)
    assert _len(_rows) == 1, (_str(_len(_rows)) + ' lines printed. Print only the first gap under 45, then `break`.'
                              + _ev)
    assert False, 'The line printed is not the first gap under 45. Test each gap with `if gap < 45:`.' + _ev
''',
    W=FIRST_WALL,
    EVW=ev_wall(FIRST_WALL),
)

BREAK_USED = chk(
    "the loop stops with break",
    r'''
assert _uses('node:Break'), ("Your loop doesn't use `break`. Stop the loop with `break`, inside the `if`, right "
                             "after the print.")
''',
)

STOP_AT_THE_FIRST = dict(
    id="stop-at-the-first",
    title="Stop at the first",
    martu=(
        "[[break|`break`]] leaves a loop right away, and Python goes on with the first line below the loop. It's "
        "like looking up a word in the dictionary: once you find it, you close the book. In the Example, `break` "
        "stops the loop at 9, the first coin over 8.\n"
        "I want one number: the first gap under 45, not all of them. A gap is the hours between two bursts. So "
        "test each gap. When one is under 45, print it, then `break`.\n"
        "You know `return` from Unit 3: it hands a value back, and it also stops the recipe right there. "
        "`break` stops a loop the same way."
    ),
    introduces=["node:Break"],
    example="for coin in [2, 9, 4, 12]:\n    if coin > 8:\n        print(coin)\n        break\n",
    example_output="9",
    names=["chalk_wall", "gap"],
    starter=FIRST_STARTER,
    checkpoints=[
        dict(
            id="first-under-45",
            text=(
                "Replace `pass` on line 5 with an `if` that prints the first gap under 45, then stops the loop with "
                "`break`."
            ),
            dictated=False,
            hints=[
                "Look at line 5, `pass`, and the notes above it. What question does the `if` ask about `gap`, and "
                "which two lines go inside it?",
                "With other names:\n```python\nfor coin in [2, 9, 4]:\n    if coin > 8:\n        print(coin)\n"
                "        break\n```\nIt prints 9 and stops. 4 is never looked at.",
                "Write `if gap < 45:` in place of `pass`. Under it, with eight spaces each: `print(gap)`, then "
                "`break`.",
            ],
            checks=[FIRST_CHECK, BREAK_USED],
            pass_line="Your loop printed 44, the first gap under 45, then stopped. Gearshift: Efficient.",
        ),
    ],
    solution=FIRST_SOLUTION,
    assemble=dict(
        lines=[WALL_LINE.strip(), "for gap in chalk_wall:", "    if gap < 45:", "        print(gap)", "        break"],
        distractors=["    break", "    while gap < 45:", "        print(chalk_wall)"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "1. 48: under 45? No. Next.\n"
                "2. 48, 47, 46: no, no, no.\n"
                "3. 44: yes! Print 44, then `break`.\n"
                "4. 41 and 37 are never looked at."
            ),
        ),
        dict(
            angle="everyday",
            label="Finding your keys",
            text=(
                "You check your pockets one by one. When you find the keys, you stop. You don't keep searching "
                "the other pockets. `break` is that stop."
            ),
        ),
        dict(
            angle="why",
            label="Like `return`",
            text=(
                "You know `return` from Unit 3: it hands a value back, and it also stops the recipe right there. "
                "`break` stops a loop the same way: early, on purpose, when the answer is found."
            ),
        ),
        dict(angle="shorter", text="Test, print, `break`. The loop ends at the first match."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet=(
            'if spell_name not in caster["spell_book"]:\n'
            '    print_prompt(caster["character_name"] + " doesn\'t know " + spell_name + ".")\n'
            "    return"
        ),
        why=(
            "The first `if` in `cast_spell` ends with `return`: the recipe stops right there. `break` is the "
            "loop's version: stop now, skip the rest. You'll write that kind of `return` in Unit 7."
        ),
    ),
    takeaway="`break` leaves a loop right away. Put it inside the `if`, after the line that should still run.",
    wrong_answers=[
        dict(why="the starter: nothing printed", code=FIRST_STARTER, fails_at=1, message_contains="Nothing printed"),
        dict(why="no break: every gap under 45 prints", code=_first("    if gap < 45:\n        print(gap)"), fails_at=1,
             message_contains="Add `break`"),
        dict(why="break in the wrong place: at loop level, so the loop stops on the first gap",
             code=_first("    if gap < 45:\n        print(gap)\n    break"), fails_at=1, message_contains="very first gap"),
        dict(why="break above the print: the print never runs",
             code=_first("    if gap < 45:\n        break\n        print(gap)"), fails_at=1,
             message_contains="above `break`"),
        dict(why="the answer typed by hand", code=WALL_LINE + "print(44)\n", fails_at=1, message_contains="same line"),
        dict(why="while for if inside the loop: 44 prints forever",
             code=_first("    while gap < 45:\n        print(gap)"), fails_at=0, message_contains="printed more than"),
        dict(why="while for if, with break inside it: break leaves only the while (three gaps print)",
             code=_first("    while gap < 45:\n        print(gap)\n        break"), fails_at=1,
             message_contains="sits inside the `for`"),
        dict(why="the whole wall printed", code=_first("    if gap < 45:\n        print(chalk_wall)\n        break"),
             fails_at=1, message_contains="whole wall"),
        dict(why="break outside any loop (SyntaxError)", code=_first("    pass", tail="break\n"), fails_at=0,
             message_contains="'break' outside loop"),
        dict(why="the print not indented under the if", code=_first("    if gap < 45:\n    print(gap)\n        break"),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the answer typed into the test: if gap == 44 (right here, finds nothing on another wall)",
             code=_first("    if gap == 44:\n        print(gap)\n        break"), fails_at=1,
             message_contains="Another wall printed nothing"),
        dict(why="the values typed by hand: the loop runs over a typed copy of the wall",
             code=_first(head=WALL_LINE + "for gap in [48, 48, 47, 46, 44, 41, 37]:\n"), fails_at=1,
             message_contains="by its name"),
        dict(why="the quoted list name: the loop walks the letters of the text chalk_wall (TypeError)",
             code=_first(head=WALL_LINE + 'for gap in "chalk_wall":\n'), fails_at=0, message_contains="'<' not supported"),
        dict(why="the Example's list copied: for coin in [2, 9, 4, 12]",
             code=WALL_LINE + "for coin in [2, 9, 4, 12]:\n    if coin < 45:\n        print(coin)\n        break\n",
             fails_at=1, message_contains="by its name"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="break", solo="false", dictates="", foreign_names="coin") + "\n"
        "5B-03. Intro node:Break. S2 numbered comments (with `pass`, so the starter is valid Python). CP1 [ND]. "
        "Checks (spec): exactly one line, the first gap under 45 (a label like `First: 44` passes: the line's last "
        "whole number is read); LOOP on `[50, 49, 43, 40, 38]` (43), so a typed 44 fails; and `break` is used. "
        "Catches: no `break` (three gaps), `break` at loop level (stops on 48, prints nothing: named from the "
        "code), `break` above the print, `while` for `if` (44 forever: TooMuchOutput, fails at 0), the whole "
        "wall, `break` outside a loop, and the quoted list name (`for gap in \"chalk_wall\":` walks the letters, "
        "so `gap < 45` is a TypeError, '<' not supported: a crash, so its plain words come from the explain.ts "
        "site request). WT (teacher ruling on the Unit 6 reviews): the Learn text's last line and the 'why' "
        "angle, now labeled 'Like `return`', start from what students know, Unit 3's `return`, which hands a "
        "value back and also stops the recipe; `break` stops a loop the same way. It stays a bridge to Unit "
        "7's early `return`: the campaign link is `cast_spell`'s early `return`, written in Unit 7."
    ),
)

# ---- 5B-04 forecast ----------------------------------------------------------------------------------------

FORECAST_LOOP = "while gap > 24:\n    gap = gap - shrink\n    shrink = shrink + 1\n    print(gap)\n"


def _forecast(shrink="5", gap="37", loop=FORECAST_LOOP):
    return f"gap = {gap}\nshrink = {shrink}\n" + loop


FORECAST_STARTER = _forecast()
FORECAST_SOLUTION = _forecast("3")

_FORECAST_START = r'''
_t0 = _parsed()
_start = {}
for _n in _t0.body:
    if (_tn(_n) == 'Assign' and _len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
            and _n.targets[0].id in ('gap', 'shrink') and _n.targets[0].id not in _start):
        _v = _n.value
        if _tn(_v) == 'UnaryOp' and _tn(_v.op) == 'USub' and _tn(_v.operand) == 'Constant':
            _start[_n.targets[0].id] = -_v.operand.value
        elif _tn(_v) == 'Constant':
            _start[_n.targets[0].id] = _v.value
'''

FORECAST_CHECK = chk(
    "shrink starts at another number, and Mar'tu's loop is kept",
    _FORECAST_START + r'''
assert 'gap' in _start, "Mar'tu can't find `gap = 37`. Put it back on line 1, the way it was at the start."
assert 'shrink' in _start, ('Line 2 no longer starts `shrink = ` with a number. Keep the line `shrink = ...`: change '
                            'only the number after `=`.')
_loops = [_n for _n in _t0.body if _tn(_n) == 'While']
_mine = _ast.parse(__LOOP__).body[0]
assert _loops and _ast.dump(_loops[0]) == _ast.dump(_mine), (
    "The loop changed. Keep Mar'tu's loop as it is, and change only the number in `shrink = 5`.")
assert _tn(_start['shrink']) in ('int', 'float'), '`shrink` holds text, not a number. Give it a number, with no quotes.'
assert _start['shrink'] != 5, ('`shrink` is still 5. Change the 5 in `shrink = 5` to another number, like 3. Then '
                               'press Run.')
''',
    LOOP=FORECAST_LOOP,
)

FORECAST_BONUS = chk(
    "the smallest whole shrink that runs out of nights in 3 steps",
    _FORECAST_START + r'''
_s0 = _start.get('shrink')
assert _start.get('gap') == 37, "`gap` changed. Keep `gap = 37`: the question is about tonight's wall."
assert _tn(_s0) == 'int', '`shrink` is not a whole number. Try whole numbers: 3, 4, 5 ...'
def _steps(_s):
    _g, _n = 37, 0
    while _g > 24 and _n < 1000:
        _g = _g - _s
        _s = _s + 1
        _n = _n + 1
    return _n
_n0 = _steps(_s0)
assert _n0 == 3, 'With `shrink = ' + _str(_s0) + '`, the loop takes ' + _str(_n0) + ' steps. Find a start that takes 3.'
assert _s0 == 4, '`shrink = ' + _str(_s0) + '` takes 3 steps. Is there a smaller start that still takes 3?'
''',
)

FORECAST = dict(
    id="forecast",
    title="Mar'tu wants to show you something",
    martu=(
        "This loop guesses the next gaps on my wall, like finding the next numbers in a pattern in math class. "
        "The newest gap is 37 hours, and each gap shrinks a little more than the one before.\n"
        "Each pass, the loop does three things: take `shrink` away from the gap, make `shrink` one bigger, then "
        "print the new gap. It stops when the gap is 24 hours or less. Then the bursts come every day, and there "
        "are no nights left.\n"
        "Predict it, then press Run. Then change `shrink` on line 2, and press Run again."
    ),
    names=["shrink"],
    pick="3",
    predict=dict(
        q="Before you press Run: what will Mar'tu's loop print?",
        choices=["32\n27\n22", "32\n26", "32\n26\n19", "37\n32\n26"],
        answer=2,
        explain=(
            "```text\ngap  shrink  new gap\n37   5       32\n32   6       26\n26   7       19\n```\n"
            "19 is not more than 24, so the loop stops after 3 steps."
        ),
    ),
    pair_talk="Pair talk: each of you tries a different `shrink`. Compare: how many steps until the nights run out?",
    starter=FORECAST_STARTER,
    checkpoints=[
        dict(
            id="change-the-shrink",
            text="On line 2, change only the number after `shrink =`, like 3 in place of 5. Then press Run again.",
            dictated=True,
            hints=[
                "Look at line 2, `shrink = 5`. Which part do you change, and which part stays as it is?",
                "A smaller shrink means the gaps fall more slowly. A bigger one, faster. Try one, then count the "
                "lines it prints.",
                "Write `shrink = 3` on line 2, in place of `shrink = 5`.",
            ],
            checks=[FORECAST_CHECK],
            pass_line="You changed the shrink and ran the guess again. Mar'tu, grim: If this is right, we run out of nights.",
        ),
    ],
    solution=FORECAST_SOLUTION,
    another_way=[
        dict(
            angle="step-by-step",
            label="Trace table",
            text=(
                "```text\ngap  shrink  gap > 24?  new gap\n37   5       True       32\n32   6       True       26\n"
                "26   7       True       19\n19   8       False      -\n```"
            ),
        ),
        dict(
            angle="picture",
            label="The wall, guessed",
            text=(
                "```text\nwall:   ... 44  41  37\nguess:  32  26  19\n```\n"
                "Each guess falls by one more hour than the last."
            ),
        ),
        dict(
            angle="in Tor",
            label="Thirty-two hours",
            text=(
                "Bomb Shell read the wall and said: *thirty-two hours, maybe less.* Look at the first number this "
                "loop prints."
            ),
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="Run the math",
        text=(
            "Gearshift wants numbers, not guesses. Find the smallest whole number for `shrink` that ends the loop in "
            "exactly 3 steps, which is 3 lines printed."
        ),
        hints=[
            "A bigger shrink means fewer lines. Try 3, 4 and 5, and count the lines each time.",
            "Two of those starts take 3 steps. The task wants the smaller one.",
            "3 takes 4 steps. Write `shrink = 4` on line 2.",
        ],
        checks=[FORECAST_BONUS],
        solution=_forecast("4"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "At the end of the campaign module, Bomb Shell studied the wall: *thirty-two hours, maybe less.* That's "
            "the first number this loop prints. Mar'tu closed their eyes. Now you'll get why."
        ),
    ),
    takeaway="A `while` loop can play a guess forward, one step at a time, until its question turns `False`.",
    wrong_answers=[
        dict(why="the starter: shrink still 5", code=FORECAST_STARTER, fails_at=1, message_contains="Change the 5"),
        dict(why="the loop changed instead of shrink", code=_forecast(loop=FORECAST_LOOP.replace("> 24", "> 20")),
             fails_at=1, message_contains="Keep Mar'tu's loop"),
        dict(why="shrink in quotes (TypeError)", code=_forecast('"3"'), fails_at=0, message_contains="unsupported operand"),
        dict(why="the shrink line deleted (NameError)", code="gap = 37\n" + FORECAST_LOOP, fails_at=0,
             message_contains="'shrink' is not defined"),
        dict(why="a sum in place of the number: shrink = 2 + 1", code=_forecast("2 + 1"), fails_at=1,
             message_contains="change only the number after `=`"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="while-loop", solo="false", dictates="1", foreign_names="",
             stages="P,R", story_beat="protected", minutes="2") + "\n"
        "5B-04, the protected story beat ('Mar'tu wants to show you something'). Pre-written as spec: `gap = 37`, "
        "`shrink = 5`, `while gap > 24`: subtract, add 1 to shrink, print -> 32, 26, 19 (verified: the predict "
        "runs it). Predict, then Run; CP1 [D] changes `shrink` (any number but 5; Mar'tu's pick 3 gives 34, 30, "
        "25, 19) and keeps the loop exactly (an AST compare, made inside the check so the Python version cannot "
        "differ). Every start ends: `shrink` grows by 1 each pass. Mar'tu's grim line is the pass line. Bonus "
        "(G4 R16): the smallest whole shrink that ends in 3 steps is 4 (3 takes 4 steps; 4 and 5 take 3). The "
        "campaign link is the 'thirty-two-hours' beat: 37 - 5 = 32. Teacher ruling on the Unit 6 reviews: the CP "
        "text and the keep-the-line message say 'change only the number after `shrink =`' (a whole new line, or a "
        "sum, is not a number), and the bonus ladder gets a middle rung ('Two of those starts take 3 steps. The "
        "task wants the smaller one.'); its last rung keeps the answer, opt-in like every bonus's last rung."
    ),
)

# ---- 5B-S solo-5b ------------------------------------------------------------------------------------------

SOLO_B_HEAD = 'oil = 4\nwhile oil > 0:\n    print("Lamp oil:", oil)\n'
SOLO_B_TAIL = 'print("The lamp goes out.")\n'


def _solo_b(update="    oil = oil - 1\n", head=SOLO_B_HEAD, tail=SOLO_B_TAIL):
    return head + update + tail


SOLO_B_STARTER = _solo_b("    oil = oil + 1\n")

SOLO_B_CHECK = chk(
    "the oil counts down to 1, then the lamp goes out (any start)",
    r'''
for _start in (4, 2):
    _ev = " Mar'tu tested your code with a test number, `oil = " + _str(_start) + "`."
    _ns, _rows, _err, _miss = _rerun({'oil': _start})
    assert not _miss, "The line `oil = 4` is gone, so Mar'tu can't test your code with another start."
    assert not _err.startswith('Runaway'), 'With another start, the loop never stopped.' + _ev
    assert not _err, 'With another start, your code stopped with an error, ' + _err.split(':')[0] + '.' + _ev
    _want = ['Lamp oil: ' + _str(_i) for _i in _rng(_start, 0, -1)] + ['The lamp goes out.']
    if _rows == _want:
        continue
    _oil = [_nums(_l)[-1] for _l in _rows if _l.startswith('Lamp oil') and _nums(_l)]
    _out = [_l for _l in _rows if 'goes out' in _l]
    assert _len(_out) <= 1, 'The lamp goes out on every pass: that line runs inside the loop.' + _ev
    assert not (_start == 2 and _oil == [4, 3, 2, 1]), ('Another start printed the same lines, so the lines are '
                                                        'typed in.' + _ev)
    assert _oil, 'No oil lines printed: the loop never ran.' + _ev
    assert _oil != list(_rng(_start - 1, -1, -1)), (
        'Each line shows the oil after it drops, so the count starts one low and ends at 0.' + _ev)
    assert not (_len(_oil) > 1 and _oil[1] > _oil[0]), 'The oil goes up each pass, not down.' + _ev
    assert 0 not in _oil, 'The loop ran one pass too many: it printed 0.' + _ev
    assert _len(_oil) != 1, 'Only one line of oil printed: it stopped after 1 pass.' + _ev
    assert _len(_oil) >= _start, 'The oil dropped by more than 1 each pass, so some lines are missing.' + _ev
    assert _out, 'The Console never shows `The lamp goes out.`' + _ev
    assert False, 'The lines do not count the oil down to 1, then out.' + _ev
''',
)

SOLO_5B = dict(
    id="solo-5b",
    title="Show Mar'tu",
    martu=(
        "One bug, all yours. Press Run, read the box in the Console, then read the loop. The lamp oil should run "
        "down, yes?"
    ),
    solo=True,
    explainer="lean",
    names=["oil"],
    starter=SOLO_B_STARTER,
    checkpoints=[
        dict(
            id="the-oil-runs-down",
            text="Mend the loop so the oil counts down to 1, then the lamp goes out.",
            dictated=False,
            hints=[
                "Read the box in the Console: its title, then Python's last line, `TooMuchOutput: This program "
                "printed more than 200,000 characters, so it was stopped.`",
                "Which line inside the loop changes `oil`? Which way does it move it?",
                "Each pass should take 1 away from `oil`, so that `oil > 0` can turn `False`.",
            ],
            checks=[SOLO_B_CHECK],
            pass_line="The oil runs down, and the lamp goes out. You did that on your own. Mar'tu: I saw.",
        ),
    ],
    solution=_solo_b(),
    another_way=[
        dict(
            angle="step-by-step",
            text="`oil` starts at 4. Each pass it should get closer to 0, so that `oil > 0` turns `False` and the loop ends.",
        ),
        dict(angle="shorter", text="The line that changes `oil` must move it toward the stop."),
    ],
    takeaway="On your own: the line that changes a `while` loop's value must move it toward the stop.",
    wrong_answers=[
        dict(why="the starter: the update moves the wrong way (prints forever)", code=SOLO_B_STARTER, fails_at=0,
             message_contains="printed more than"),
        dict(why="two at a time", code=_solo_b("    oil = oil - 2\n"), fails_at=1, message_contains="more than 1"),
        dict(why="oil = 0 inside: one pass", code=_solo_b("    oil = 0\n"), fails_at=1, message_contains="1 pass"),
        dict(why=">= 0: one pass too many", code=_solo_b(head=SOLO_B_HEAD.replace("> 0", ">= 0")), fails_at=1,
             message_contains="printed 0"),
        dict(why="if for while", code=_solo_b(head=SOLO_B_HEAD.replace("while", "if")), fails_at=1, message_contains="1 pass"),
        dict(why="the last line inside the loop", code=_solo_b("    oil = oil - 1\n    print(\"The lamp goes out.\")\n", tail=""),
             fails_at=1, message_contains="every pass"),
        dict(why="the lines typed", code="oil = 4\n" + "".join(f'print("Lamp oil:", {n})\n' for n in (4, 3, 2, 1)) + SOLO_B_TAIL,
             fails_at=1, message_contains="typed in"),
        dict(why="the update moved outside the loop (still forever)", code=_solo_b("oil = oil - 1\n"), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update moved above the print: 3 down to 0",
             code='oil = 4\nwhile oil > 0:\n    oil = oil - 1\n    print("Lamp oil:", oil)\n' + SOLO_B_TAIL,
             fails_at=1, message_contains="after it drops"),
        dict(why="the question flipped to stop the endless loop (oil < 0): the loop never runs",
             code=_solo_b(head=SOLO_B_HEAD.replace("oil > 0", "oil < 0")), fails_at=1, message_contains="never ran"),
        dict(why="the question changed to fit the wrong-way update (oil < 8): it counts up",
             code=_solo_b("    oil = oil + 1\n", head=SOLO_B_HEAD.replace("oil > 0", "oil < 8")), fails_at=1,
             message_contains="goes up"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="while-loop", solo="true", dictates="", foreign_names="",
             seat_b="a countdown that is off by one (`while oil >= 0:`)") + "\n"
        "SOLO, one bug (C6), explainer='lean'. Seat A (and anyone solo): a `while` update that moves the wrong way "
        "(`oil = oil + 1`). The loop prints, so the starter's Run stops in milliseconds with TooMuchOutput; that "
        "explainer is always full (explain.ts ALWAYS_FULL), and it says what happened without naming the fix. "
        "Check: reruns with `oil` 4 and 2; lean messages name the slip and keep the evidence bracket, with no "
        "fix. No Assemble rung (as Units 3-5's SOLOs): its pieces would hand over the mended update. Seat B (once "
        "pair mode ships): the off-by-one countdown. Recorded, never blocking, never shown to "
        "a partner. The pass line is Unit 2's ruled SOLO wording."
    ),
)

LESSON_5B = dict(
    kind="lesson",
    id="while-the-clock-ticks",
    title="While the Clock Ticks",
    minutes=15,
    summary=(
        "Repeat lines while a question is `True`. Count down to the burst, fix a loop that never ends, and stop a "
        "loop early with `break`."
    ),
    notes=(
        "Lesson 5B (SC). Preceded by 5b-remembers. Exactly one SOLO (solo-5b). Non-dictated checkpoints: 5B-01 "
        "CP2, 5B-02, 5B-03, 5B-S; dictated: 5B-01 CP1 and 5B-04. 5B-04 is a protected story beat. 15 minutes (14 "
        "in the spec): 5B-01's one `while` blank to fill (teacher ruling on the Unit 6 reviews). Every while loop "
        "a student can break here prints inside its body, so an endless one stops in milliseconds (file header)."
    ),
    exercises=[COUNTDOWN, LOOP_THAT_NEVER_ENDS, STOP_AT_THE_FIRST, FORECAST, SOLO_5B],
)

# =============================================================================================
# Quiz 5
# =============================================================================================

QUIZ_5 = dict(
    kind="quiz",
    id="loops-quiz",
    title="Loops Quiz",
    minutes=8,
    summary=(
        "Eight questions on `for` loops, running totals, `while` and `break`, and a recipe. Retake it as often as "
        "you like. Then try the Velocite Watch, a project that puts loops and a recipe together."
    ),
    notes=(
        "Quiz 5 (SC): 6 predict, 1 bug, 1 mc, in the spec's order. Q8 is the def/return item (every unit quiz has "
        "one from Unit 4 on). Q4 keeps the wall short as `wall` (35 characters) for the phone; Q6 keeps the night "
        "roster in setup and states it in the question. Review order: right answers first (G1 R26). The right "
        "choice sits in varied places (the site shuffles too)."
    ),
    questions=[
        dict(
            type="predict",
            id="party-total",
            q="What will this print?",
            code="total = 0\nfor mana in [18, 20, 24, 26]:\n    total = total + mana\nprint(total)\n",
            choices=["26", "88", "18\n38\n62\n88", "0"],
            answer="88",
            explain="`total` starts at 0 once, above the loop. Each pass adds one more: 18, 38, 62, 88. The print runs once, after the loop.",
            notes="Distractors: the reset-inside answer (26) and the print-inside answer (every running total).",
        ),
        dict(
            type="bug",
            id="total-restarts",
            q="This should print the party's total mana, 88, but it prints 26. Fix it.",
            code="for mana in [18, 20, 24, 26]:\n    total = 0\n    total = total + mana\nprint(total)\n",
            fix="total = 0\nfor mana in [18, 20, 24, 26]:\n    total = total + mana\nprint(total)\n",
            expected_output="88",
            explain=(
                "`total = 0` was inside the loop, so the total went back to 0 every pass, and only 26 was left. "
                "Move it above the loop."
            ),
            notes="The class's reset-inside slip (spec Q2).",
        ),
        dict(
            type="predict",
            id="three-hours",
            q="What will this print?",
            code="hours_left = 3\nwhile hours_left > 0:\n    print(hours_left)\n    hours_left = hours_left - 1\n",
            choices=["3\n2\n1\n0", "2\n1\n0", "3\n2\n1", "3"],
            answer="3\n2\n1",
            explain="The question is asked before every pass. At 0, `hours_left > 0` is `False`, so 0 never prints.",
            notes="Off-by-one distractors: with 0, and starting one low.",
        ),
        dict(
            type="predict",
            id="the-shrinks",
            q="What will this print?",
            code="wall = [48, 48, 47, 46, 44, 41, 37]\nfor i in range(1, len(wall)):\n    print(wall[i - 1] - wall[i])\n",
            choices=["0\n-1\n-1\n-2\n-3\n-4", "0\n1\n1\n2\n3\n4", "48\n48\n47\n46\n44\n41", "1\n1\n2\n3\n4"],
            answer="0\n1\n1\n2\n3\n4",
            explain=(
                "Each pass takes this gap away from the one before it: 48 − 48, 48 − 47, and so on. Each shrink is "
                "bigger: the decay is accelerating."
            ),
        ),
        dict(
            type="mc",
            id="how-many-passes",
            q="`roster` holds 4 sheets. How many times do the indented lines under `for member in roster:` run?",
            choices=["Once", "Until Python finds an error", "4 times: once for each sheet", "Forever"],
            answer=2,
            why_wrong={
                0: "The indented lines run once for each item, not once in all. Four sheets, four passes.",
                1: "A `for` loop ends by itself when the list runs out. No error is needed.",
                3: "A `for` loop over a list always ends: it stops after the last item.",
            },
            explain=(
                "A `for` loop runs its indented lines once for each item in the list. Four sheets: four passes, "
                "then it stops."
            ),
        ),
        dict(
            type="predict",
            id="who-needs-rest",
            q="`roster` holds the night's sheets: Oogrish 6 mana, Gearshift 14, Bomb Shell 3, Lucky 22. What will this print?",
            setup=setup_roster(NIGHT),
            code='for member in roster:\n    if member["mana"] < 10:\n        print(member["name"])\n',
            choices=["Oogrish\nBomb Shell", "Oogrish\nGearshift\nBomb Shell\nLucky", "Gearshift\nLucky", "Bomb Shell"],
            answer="Oogrish\nBomb Shell",
            explain="The `if` runs every pass, but only lets through sheets with less than 10 mana: Oogrish (6) and Bomb Shell (3).",
            notes="The loop-with-if item moved here from QC5 (spec 'QC5 fix').",
        ),
        dict(
            type="predict",
            id="break-at-the-first",
            q="What will this print?",
            code='for gap in [48, 46, 44, 41]:\n    if gap < 45:\n        print(gap)\n        break\nprint("done")\n',
            choices=["44\n41\ndone", "done", "44\ndone", "48\n46\n44\ndone"],
            answer="44\ndone",
            explain="44 is the first gap under 45: it prints, then `break` leaves the loop. 41 is never looked at. `done` is below the loop, so it runs.",
        ),
        dict(
            type="predict",
            id="double-the-total",
            q="What will this print?",
            code="def double(n):\n    return n * 2\n\ntotal = 0\nfor mana in [3, 4, 5]:\n    total = total + mana\nprint(double(total))\n",
            choices=["12", "24", "6\n8\n10", "10"],
            answer="24",
            explain="The loop adds up 3 + 4 + 5: 12. Then `double(12)` hands back 12 * 2, which is 24.",
            notes="The def/return item (spec Q8): a recipe called on the loop's result.",
        ),
    ],
)

ITEMS = [REMEMBERS_5A, LESSON_5A, REMEMBERS_5B, LESSON_5B, QUIZ_5]
