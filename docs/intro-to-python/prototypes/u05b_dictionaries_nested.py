"""Unit 5 "Dictionaries" ("Stat Sheets and Spell Books"), part b: Mar'tu remembers (4b-remembers), Lesson 4B
"Sheets Inside Sheets", Quiz 4, Project 4P "Mar'tu's Ledger of Heroes" (with Lucky's side quest), the optional
advanced challenge "The Barrier, From Blank", and Extra practice 5X (4A-T, 4B-T).

Spec: design/curriculum.md, "## Unit 5 · Dictionaries", items 3 to 6 (u05b): 4b-remembers; 4B-01 to 4B-06 and 4B-S;
Quiz 4 (8 questions: 4 predict, 1 mc, 1 parsons, 1 fill, 1 bug, as listed); Project 4P with the old groups D-E side
quest; the 5X pool (4A-T write-by-key-again, 4B-T store-by-name-again). The teacher's Unit 5 ruling adds an optional
advanced challenge after the project, "The Barrier, From Blank" (barrier-from-blank, 10 min, no core time), and a
third checkpoint on 4B-04 (store-if-new: `if spell_name not in spell_book:` before the store, so Quick Check C3's
guard-then-store is practised first).
Introduces nothing new (concept_map.json: u05b introduces []). Dictionaries (`node:Dict`), `in` / `not in` and
`.get()` come from u05a (4A, written at the same time); lists come from Unit 4 (u04a/u04b, in staging): only list
literals, indexing and a list of dicts read by position are used here. No loops (Unit 6), no f-strings (Unit 9),
and `None` is never written in code (u07b): it only shows up as printed output.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN the spell book
(`spell_book[spell_name] = spell` in `add_spell`), the mana bars (`caster["max_mana"] - caster["mana"]`), the body
of `cast_spell` in hold-the-barrier (`caster["abilities"]["magical_affinity"] < spell["required_affinity"]`, then
`caster["mana"] = caster["mana"] - spell["mana_cost"]`) and `for member in party.members:`. So every campaign link
here is "you've seen this, now you'll get it". Every student has their own device; pair talk is optional and every
checkpoint is solo. Mar'tu's framing line, kept from the spec: "A list remembers order. It does not remember
meaning."

Help ladder (curriculum 2.2) as fields, the same as Units 1-3: hints[0] Start me off (the line's first tokens; in a
debug step "Read Python's last line first"), hints[1] Point (where to look), another_way, hints[2+] Teach (a tiny
example with other names, listed in foreign_names), assemble (More structure), solution (Show).
Terminology (2.9): from Unit 4 on "variable" (Mar'tu may still say "box"), "key" for the tag a dictionary keeps on
each value (u05a: "keeps a tag on every value. Python calls the tag a key"; a key is never called a "label" in
student text, because the quotes sentence uses "label" for a variable's name), "recipe" for `def` (Functions II
changes that), the quotes sentence word for word (u05a gives its first use the "*Box* here means a variable" line).

Check codes (curriculum 2.5). Each part file is self-contained, so the dictionary helpers live here (_DX). Every
rerun happens inside the check only: the student's program (and the exercise's setup) is parsed, a line is slipped
in right after the statement that makes a named sheet or box, and the program runs again in a fresh namespace with
its prints captured. So a check can change a value deep inside a sheet without editing what the student typed:
  read_check()    the printed lines show the value (a whole number, or the text), and not as a printed dict: a
                  printed inner card gets "Add the inner key"; neighbouring values from the same sheet get their
                  own message ("Your line printed 6, the dexterity").
  follow_check()  CMB: the rerun changes the sheet (`bomb_shell["abilities"]["wisdom"] = 11`) or reorders the
                  roster, and the printed line must follow. A line that still shows the old value is "typed".
  roster_check()  "through the list", by behavior: the rerun gives `roster` its own deep copies of the sheets and
                  changes a value in a copy. A read through `roster` (or through a box taken from it, such as
                  `first = roster[0]` or `hero = roster[1]`) follows; `oogrish[...]`, a typed value, or a box
                  named next to `roster` in the same print does not. 4B-03 CP2, 4B-06 CP2 and the project's
                  task 5 use it.
  _said()         True / False said as a word, so a labelled print such as `print("Found:", x in book)` passes.
  bespoke state checks for writes: KEY (near-miss keys such as `"Max_Mana"` named letter for letter), a flat key
                  made on the outside of the sheet (a skipped level), NUM, SWAP for the spell's two blanks, "Glow
                  is kept", `spell_book["spell_name"]`, and CMB reruns for every write (a typed 8, 14 or 13 fails).
  cast_cases()    BND for 4B-05: affinity, mana, cost and needed are all changed in the rerun (four caster setups
                  per step, exactly enough affinity and exactly enough mana included). The printed line is matched
                  by its words ("skilled" with a no-word such as "not" or "isn't", and "more mana"), so Lucky's side
                  quest wording passes, and so does an `else` line that cheers "skilled enough!". Before any case
                  message, CP1 and CP2 diagnose the test they replace: still `False`, typed numbers only
                  (`if 12 < 9:`), or the sign backwards.
  _GUARD          4B-04 CP3, ported from u05c's C3 check: reruns with a name that already has a page (Glow, other
                  numbers), a new name (stored), and a page no message names; diagnoses an unindented store line,
                  `"spell_name"` in quotes, a value asked, a typed list or name, and no `if`.
  barrier_check() the challenge: calls `cast_spell` inside the check with fresh sheets (Pell, Moon Step, Ash Ward),
                  never the game's own caster, so the values never collide with the student's call.
  the project's recipe check: PAR (7 and 15, never a hero's affinity), PAR-CONST, RET (print instead of return);
                  its CMB swaps in another `max_mana_for` inside the check, so a hand-worked `* 2` fails "let the
                  recipe do the math".
Messages follow the Unit 2/3 ruling: the fix first, then what happened, then the evidence in brackets,
"(Mar'tu's check tried `bomb_shell["abilities"]["wisdom"] = 11`, only inside the check.)". They use the party
table's values and invented ones only, never a student's own text (2.11).

Python's messages were checked in CPython 3.13 (the site runs 3.13): `{name: "Lucky"}` -> "name 'name' is not
defined"; `{"name" = "Lucky"}` -> "cannot assign to literal here. Maybe you meant '==' instead of '='?"; a missing
comma after an int value -> "invalid syntax. Perhaps you forgot a comma?" on that line, after a text value ->
"invalid syntax" on the next line; a missing colon -> "':' expected after dictionary key"; `roster["Lucky"]` ->
"list indices must be integers or slices, not str"; `hero.mana` -> "'dict' object has no attribute 'mana'";
`hero("mana")` -> "'dict' object is not callable"; `hero[0]` -> "KeyError: 0"; `spell in book` with a dict value
-> "unhashable type: 'dict'".

Phone width: fenced pictures, examples, predict code and quiz code keep lines to 36 characters or fewer, and so do
starter lines. Some solution lines are longer, because the nested read itself is long
(`bomb_shell["abilities"]["dexterity"]` is 35 characters); those lines are the campaign's own shapes.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u05b
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


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
# Check helpers, put in front of every check (plain Python, run in the student's namespace)
# ---------------------------------------------------------------------------------------------

_DX = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
_QUOTES = __QUOTES__
_SETUP = __SETUP__
def _lit(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
def _did(_tried, _end=''):
    return "(Mar'tu's check tried " + _tried + ', only inside the check' + _end + '.)'
def _whole(_v):
    return r'(?<![\d.])' + _re.escape(str(_v)) + r'(?!\d)(?!\.\d)'
def _display(_l):
    return _l[:1] in '{['
def _shows(_ls, _v):
    for _l in _ls:
        if _display(_l):
            continue
        if type(_v).__name__ == 'str':
            if _v in _l:
                return True
        elif _re.search(_whole(_v), _l):
            return True
    return False
def _said(_ls, _w):
    return [_l for _l in _ls if _re.search(r'(?<![A-Za-z])' + _w + r'(?![A-Za-z])', _l)]
def _sq(_s):
    return str(_s).lower().replace('_', '').replace(' ', '')
def _near(_d, _k):
    if type(_d).__name__ != 'dict':
        return None
    for _x in _d:
        if _x != _k and _sq(_x) == _sq(_k):
            return _x
    return None
def _targets(_n):
    _kind = type(_n).__name__
    if _kind == 'FunctionDef':
        return [_n.name]
    _ts = list(_n.targets) if _kind == 'Assign' else ([_n.target] if _kind == 'AugAssign' else [])
    _out = []
    for _t in _ts:
        if type(_t).__name__ == 'Name':
            _out.append(_t.id)
        elif type(_t).__name__ == 'Subscript':
            _out.append(_ast.unparse(_t).replace(chr(39), '"'))
    return _out
def _rerun(_changes):
    _body, _found = [], []
    for _code in (_SETUP, _source):
        for _n in (_ast.parse(_code).body if _code.strip() else []):
            _body.append(_n)
            _made = _targets(_n)
            for _anchor, _line in _changes:
                _first = _anchor.startswith('1:')
                _alts = (_anchor[2:] if _first else _anchor).split('|')
                if any(_a in _made for _a in _alts) and not (_first and _anchor in _found):
                    _found.append(_anchor)
                    _body.extend(_ast.parse(_line).body)
    _tree = _ast.Module(body=_body, type_ignores=[])
    _ast.fix_missing_locations(_tree)
    _ns = {'__name__': '__main__'}
    _out, _old, _err = _io.StringIO(), _sys.stdout, ''
    _sys.stdout = _out
    try:
        exec(compile(_tree, 'main.py', 'exec'), _ns)
    except BaseException as _e:
        _err = type(_e).__name__ + (': ' + str(_e) if str(_e) else '')
    finally:
        _sys.stdout = _old
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _err, [_a for _a, _l in _changes if _a not in _found]
def _keep(_name):
    return ('Keep `' + _name + '` from the starter, made on its own line, so Mar' + chr(39) + 'tu' + chr(39)
            + 's check can try other values there.')
def _stop(_err, _tried):
    return 'Mend this slip, then Run again: ' + _err + ' ' + _did(_tried, ', and your program stopped there')
def _calls(_f):
    return [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call'
            and type(_n.func).__name__ == 'Name' and _n.func.id == _f]
_COPY = 'import copy as _cp\nroster = _cp.deepcopy(roster)\n'
def _get(_d, *_path):
    for _k in _path:
        if type(_d).__name__ == 'dict' and _k in _d:
            _d = _d[_k]
        elif type(_d).__name__ == 'list' and type(_k).__name__ == 'int' and -len(_d) <= _k < len(_d):
            _d = _d[_k]
        else:
            return '(missing)'
    return _d
'''


def dx(setup=""):
    """The helpers, with the exercise's hidden setup (reruns run it first, like the site does)."""
    return _DX.replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))


_READ = r'''
_ls = _lines()
if not _shows(_ls, __WANT__):
    assert not [_l for _l in _ls if _display(_l) and __INSIDE__ in _l], __WHOLE__
    for _v, _m in __NEAR__:
        assert not _shows(_ls, _v), _m
    assert False, __FIX__
'''


def read_check(label, want, fix, *, inside, whole, near=(), pre="", setup=""):
    """The printed lines show `want` (not as a printed dict). `near`: (value, message) pairs for other values."""
    return (label, dx(setup) + pre + fill(_READ, want=want, fix=fix, inside=inside, whole=whole, near=list(near)))


_FOLLOW = r'''
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, __KEEP__ or _keep(_miss[0])
assert not _err, _stop(_err, __TRIED__)
if not _shows(_ls, __WANT__):
    assert not _shows(_ls, __OLD__), __TYPED__ + ' ' + _did(__TRIED__, ': your program still printed ' + _lit(__OLD__))
    assert False, __FIX__ + ' ' + _did(__TRIED__)
'''


def follow_check(label, changes, tried, want, old, *, typed, fix, keep="", setup=""):
    """CMB: rerun with `changes` ([(anchor, line)]); the printed lines must show `want`, not the old value."""
    return (label, dx(setup) + fill(_FOLLOW, changes=list(changes), tried=tried, want=want, old=old, typed=typed,
                                    fix=fix, keep=keep))


_ROSTER = r'''
_ns, _ls, _err, _miss = _rerun([('roster', _COPY + __EDIT__)])
assert not _miss, _keep('roster')
assert not _err, _stop(_err, __TRIED__)
if not _shows(_ls, __WANT__):
    _end = ': your program still printed ' + _lit(__OLD__) if _shows(_ls, __OLD__) else ''
    assert False, __FIX__ + ' ' + _did(__TRIED__, _end)
'''


def roster_check(label, edit, tried, want, old, fix):
    """Through the list, by behavior: the rerun gives `roster` its own copies of the sheets, then `edit` changes a
    copy. A read through `roster` (or a box taken from it) follows; a read of the sheet's own box or a typed value
    does not."""
    return (label, dx() + fill(_ROSTER, edit=edit, tried=tried, want=want, old=old, fix=fix))


def flat_check(var, key, fix):
    """Code for a pre-check: the sheet `var` exists and has no `key` on the outside (a skipped level)."""
    return fill(
        "assert type(globals().get(__VAR__)).__name__ == 'dict', _keep(__VAR__)\n"
        "assert __KEY__ not in globals()[__VAR__], __FIX__\n",
        var=var, key=key, fix=fix,
    )


# =============================================================================================
# The unit (the same UNIT dict in every Unit 5 part file)
# =============================================================================================

UNIT = dict(
    id="dictionaries",
    order=5,
    title="Dictionaries",
    subtitle="Stat Sheets and Spell Books",
    published=True,
    martu_intro=(
        "A list remembers order. It does not remember *meaning*. Which number is Lucky's armor? Which is his "
        'mana? A dictionary keeps a tag on every value. At the Institute, every student had a record like '
        "this. Mine said 'talks too little'.\nYou have seen dictionaries already: the spell book, the mana "
        'bars, and `caster["abilities"]["magical_affinity"]` when you held the barrier. A lot of that code '
        'felt like a wall, yes? Tonight we read it one key at a time.'
    ),
    goals=[
        "Write a dictionary with keys in quotes, `:` and commas, and say why keys have quotes when box names don't",
        "Read a value by its key, and mend a KeyError caused by spelling, capitals or a skipped level",
        "Change a value and add a key, including `hero[\"mana\"] = hero[\"mana\"] - cost`",
        "Ask whether a key is in a dictionary with `in` and `not in`",
        "Use a key kept in a variable: `book[spell_name]`, not `book[\"spell_name\"]`",
        "Read and change values inside values: `hero[\"abilities\"][\"magical_affinity\"]`",
        "Read from a list of sheets, like `roster[2][\"name\"]`",
        "Build a spell from variables and store it by name: `spell_book[spell_name] = spell`",
        "Get a value, compare it, and act on it with `if` / `elif` / `else`, like holding the barrier",
    ],
    campaign_links=["friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="nested dictionary",
        aliases=["nested dictionaries", "dictionary inside a dictionary", "inner dictionary", "inner card"],
        plain=(
            "A dictionary kept as a value inside another dictionary. Read it with two keys in a row: the outer key "
            "first, then the inner key."
        ),
        example='bomb_shell["abilities"]["wisdom"]',
    ),
    dict(
        term="list of dictionaries",
        aliases=["lists of dictionaries", "list of sheets"],
        plain="A list whose items are dictionaries. Pick a sheet by its position first, then read it by key.",
        example='roster[2]["name"]',
    ),
]

# The party table (curriculum 1.2): the real values every sheet uses.
TABLE = {
    "oogrish": ("Oogrish", {"intelligence": 17, "wisdom": 17, "dexterity": 14, "strength": 13, "magical_affinity": 9}),
    "gearshift": ("Gearshift", {"intelligence": 14, "wisdom": 15, "dexterity": 13, "strength": 17,
                                "magical_affinity": 10}),
    "bomb_shell": ("Bomb Shell", {"intelligence": 14, "wisdom": 8, "dexterity": 6, "strength": 15,
                                  "magical_affinity": 12}),
    "lucky": ("Lucky", {"intelligence": 13, "wisdom": 12, "dexterity": 15, "strength": 17, "magical_affinity": 13}),
}
HEROES = [(var, TABLE[var][0], TABLE[var][1]) for var in ("oogrish", "gearshift", "bomb_shell", "lucky")]

# =============================================================================================
# Mar'tu remembers... (4b-remembers): a Unit 4 nested-list read and a Unit 3 def/return item
# =============================================================================================

REMEMBERS_4B = dict(
    kind="quiz",
    id="4b-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from earlier units. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 4B; recall from Unit 4 (a list inside a list, "
        "3A-09) and Unit 3 (`return roll >= 11`, 6A-09; the def/return item every warm-up carries from Unit 4 on). "
        "A miss shows the answer and a one-line why, with no red X. The roster is Unit 4's `[name, max_mana]` "
        "roster, so the lesson can open with 'a list remembers order, not meaning'."
    ),
    questions=[
        dict(
            type="predict",
            id="list-inside-a-list",
            q="What will this print?",
            code=(
                "roster = [\n"
                '    ["Oogrish", 18],\n'
                '    ["Gearshift", 20],\n'
                '    ["Bomb Shell", 24],\n'
                '    ["Lucky", 26],\n'
                "]\n"
                "print(roster[3][0])\n"
            ),
            choices=["26", "Lucky", "Bomb Shell", "an error"],
            answer="Lucky",
            explain=(
                "`roster[3]` is the fourth inner list, `[\"Lucky\", 26]`, because positions count from 0. Then `[0]` "
                "is its first item: `Lucky`. Two brackets, read left to right."
            ),
            notes="26 reads [0] as the second item; Bomb Shell counts from 1 (Unit 4's off-by-one).",
        ),
        dict(
            type="predict",
            id="latch-at-exactly",
            q="What will this print?",
            code="def latch_check(roll):\n    return roll >= 11\n\nprint(latch_check(11))\n",
            choices=["11", "False", "True", "an error"],
            answer="True",
            explain=(
                "`>=` means *at least*. A roll of exactly 11 is at least 11, so the recipe hands back `True`. The "
                "recipe hands back the answer, not the roll."
            ),
            notes="BND recall (6A-09): False is the exactly-enough slip; 11 is 'the recipe hands back the roll'.",
        ),
    ],
)

# =============================================================================================
# Lesson 4B "Sheets Inside Sheets"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 4B-01 abilities-inside (moment: boxes in boxes, teacher-led)
# ---------------------------------------------------------------------------------------------

BOMB_SHEET = (
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "mana": 24,\n'
    '    "abilities": {\n'
    '        "dexterity": 6,\n'
    '        "wisdom": 8,\n'
    '        "magical_affinity": 12,\n'
    "    },\n"
    "}\n"
)
ABIL_STARTER = BOMB_SHEET + "\n# Print Bomb Shell's wisdom.\n"
ABIL_LINE = 'print(bomb_shell["abilities"]["wisdom"])\n'
ABIL_SOLUTION = BOMB_SHEET + "\n" + ABIL_LINE
LANTERN_EXAMPLE = (
    "lantern = {\n"
    '    "name": "Brass lantern",\n'
    '    "parts": {\n'
    '        "wick": 2,\n'
    '        "oil": 5,\n'
    "    },\n"
    "}\n"
    'print(lantern["parts"]["oil"])\n'
)
WISE_LINE = 'print(bomb_shell["abilities"]["wisdom"] >= 10)\n'

_KEEP_BOMB = "Keep the sheet `bomb_shell` from the starter."
_WISDOM_PRE = (
    flat_check("bomb_shell", "wisdom", "Keep the sheet as the starter has it: `\"wisdom\"` lives inside "
               "`\"abilities\"`, not on the outside.")
    + "assert _get(bomb_shell, 'abilities', 'wisdom') == 8, "
    + repr("Keep the sheet as the starter has it: `\"wisdom\": 8`, inside `\"abilities\"`.") + "\n"
)

_WISE_ENOUGH = r'''
assert _said(_lines(), 'False'), __NOT_YET__
for _w, _want in ((10, 'True'), (9, 'False'), (14, 'True')):
    _tried = '`bomb_shell["abilities"]["wisdom"] = ' + str(_w) + '`'
    _ns, _ls, _err, _miss = _rerun([('bomb_shell', 'bomb_shell["abilities"]["wisdom"] = ' + str(_w))])
    assert not _err, _stop(_err, _tried)
    if _w == 10:
        assert _said(_ls, 'True'), __EXACTLY__ + ' ' + _did(_tried)
    assert _said(_ls, _want), __FOLLOW__ + ' ' + _did(_tried)
'''

ABILITIES_INSIDE = dict(
    id="abilities-inside",
    title="Abilities inside",
    martu=(
        "Some values are dictionaries too. Bomb Shell's `\"abilities\"` is a whole little sheet, kept inside the "
        "big one. Boxes in boxes, yes?\n"
        "*Get it out of the dictionary: outer key, then inner key.* `bomb_shell[\"abilities\"]` opens the inner "
        "card. Then `[\"wisdom\"]` reads one line of it."
    ),
    example=LANTERN_EXAMPLE,
    example_output="5",
    names=["bomb_shell"],
    predict=dict(
        q="Before you press Run: what does this line print?",
        code=BOMB_SHEET + 'print(bomb_shell["abilities"])\n',
        choices=[
            "6",
            "abilities",
            "{'dexterity': 6, 'wisdom': 8, 'magical_affinity': 12}",
            "an error",
        ],
        answer=2,
        explain=(
            "One key opens the inner card, so Python prints the whole card, curly brackets and all. To read one "
            "line of it, add a second key: `bomb_shell[\"abilities\"][\"wisdom\"]`."
        ),
    ),
    starter=ABIL_STARTER,
    checkpoints=[
        dict(
            id="print-the-wisdom",
            text="Print Bomb Shell's wisdom.",
            dictated=False,
            hints=[
                "Wisdom is not on the big sheet. Open the inner card with the outer key, then read `\"wisdom\"` "
                "from it.",
                "Two keys in a row, outer key first: `lantern[\"parts\"][\"oil\"]` reads the oil from the lantern's "
                "parts.",
                "Write `print(bomb_shell[\"abilities\"][\"wisdom\"])` under `# Print Bomb Shell's wisdom.`",
            ],
            checks=[
                read_check(
                    "the wisdom is printed", 8,
                    "Print Bomb Shell's wisdom: the outer key `\"abilities\"`, then the inner key `\"wisdom\"`.",
                    pre=_WISDOM_PRE, inside="wisdom",
                    whole="Add the inner key, `[\"wisdom\"]`, after `bomb_shell[\"abilities\"]`. Your line printed "
                          "the whole abilities card.",
                    near=[(6, "Use the inner key `\"wisdom\"`. Your line printed 6, the dexterity."),
                          (12, "Use the inner key `\"wisdom\"`. Your line printed 12, the magical affinity."),
                          (24, "Read inside `\"abilities\"`: your line printed 24, the mana on the big sheet.")],
                ),
                follow_check(
                    "the wisdom follows the sheet",
                    [("bomb_shell", 'bomb_shell["abilities"]["wisdom"] = 11')],
                    '`bomb_shell["abilities"]["wisdom"] = 11`', 11, 8,
                    typed="Read it from the sheet, so it follows: `bomb_shell[\"abilities\"][\"wisdom\"]`, not a "
                          "typed 8.",
                    fix="Print the wisdom from the sheet: outer key, then inner key.",
                    keep=_KEEP_BOMB,
                ),
            ],
            pass_line="Bomb Shell: Eight. Acts before he thinks. Noted.",
        ),
    ],
    solution=ABIL_SOLUTION,
    assemble=dict(
        lines=[line for line in ABIL_SOLUTION.splitlines() if line.strip()],
        distractors=['print(bomb_shell["wisdom"])', 'print(bomb_shell["abilities"])'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Boxes in boxes",
            text=(
                "```text\nbomb_shell\n+---------------------------+\n| \"name\" -> \"Bomb Shell\"    |\n"
                "| \"mana\" -> 24              |\n| \"abilities\" ->            |\n"
                "|  +---------------------+  |\n|  | \"dexterity\" -> 6    |  |\n"
                "|  | \"wisdom\"    -> 8    |  |\n|  | \"magical_affinity\"  |  |\n"
                "|  |             -> 12   |  |\n|  +---------------------+  |\n"
                "+---------------------------+\n```\n"
                "The first key opens the big box's `\"abilities\"` drawer. The second key reads one line inside it."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Left to right",
            text=(
                "1. `bomb_shell` is the whole sheet.\n"
                "2. `bomb_shell[\"abilities\"]` is the inner card: `{'dexterity': 6, 'wisdom': 8, ...}`.\n"
                "3. `bomb_shell[\"abilities\"][\"wisdom\"]` is one line of that card: 8.\n"
                "Each pair of brackets goes one level in."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Holding the barrier, the campaign read `caster[\"abilities\"][\"magical_affinity\"]`. The caster's "
                "sheet, then its abilities card, then one line. Same two keys in a row."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Institute records had a pocket on the back for the student's ability card. To read a score, you "
                "opened the record, then the pocket. Nobody found it on the front page."
            ),
        ),
        dict(
            angle="try it",
            label="Skip a level on purpose",
            text=(
                "After your tick, try `print(bomb_shell[\"wisdom\"])`. Read Python's last line: wisdom is not on the "
                "big sheet. Then change it back."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants to know if Bomb Shell can read the old scrolls. They need wisdom 10. Print whether Bomb "
            "Shell's wisdom is at least 10: Python should show `True` or `False`."
        ),
        hints=[
            "A comparison inside `print()` shows `True` or `False`. *At least* is `>=`.",
            "Write `print(bomb_shell[\"abilities\"][\"wisdom\"] >= 10)` at the bottom.",
        ],
        checks=[
            (
                "a True or False line that follows the wisdom",
                dx() + fill(
                    _WISE_ENOUGH,
                    not_yet="Print the comparison itself, like `print(... >= 10)`. It shows `True` or `False`.",
                    exactly="Exactly 10 is wise enough: use *at least*, `>=`.",
                    follow="Compare the wisdom from the sheet, `bomb_shell[\"abilities\"][\"wisdom\"]`, with 10.",
                ),
            ),
        ],
        solution=ABIL_SOLUTION + WISE_LINE,
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["abilities"]["magical_affinity"]',
        why=(
            "You have seen this line in `hold-the-barrier`. The caster's sheet, then its abilities card, then one "
            "line of it: the same two keys in a row as Bomb Shell's wisdom."
        ),
    ),
    takeaway="Two keys in a row read inside a sheet: `bomb_shell[\"abilities\"][\"wisdom\"]`, outer key first.",
    wrong_answers=[
        dict(why="the starter (nothing printed yet)", code=ABIL_STARTER, fails_at=1, message_contains="outer key"),
        dict(why="a skipped level: bomb_shell[\"wisdom\"] (KeyError)",
             code=BOMB_SHEET + 'print(bomb_shell["wisdom"])\n', fails_at=0, message_contains="KeyError: 'wisdom'"),
        dict(why="only the outer key: the whole inner card printed",
             code=BOMB_SHEET + 'print(bomb_shell["abilities"])\n', fails_at=1, message_contains="whole abilities card"),
        dict(why="the number typed (CMB)", code=BOMB_SHEET + "print(8)\n", fails_at=1, message_contains="typed 8"),
        dict(why="the number typed in quotes (CMB)", code=BOMB_SHEET + 'print("8")\n', fails_at=1,
             message_contains="typed 8"),
        dict(why="the wrong inner key (dexterity)", code=BOMB_SHEET + 'print(bomb_shell["abilities"]["dexterity"])\n',
             fails_at=1, message_contains="the dexterity"),
        dict(why="dot access (bomb_shell.abilities)", code=BOMB_SHEET + "print(bomb_shell.abilities.wisdom)\n",
             fails_at=0, message_contains="has no attribute 'abilities'"),
        dict(why="round brackets (bomb_shell(\"abilities\"))",
             code=BOMB_SHEET + 'print(bomb_shell("abilities")("wisdom"))\n', fails_at=0,
             message_contains="'dict' object is not callable"),
        dict(why="both keys in one bracket", code=BOMB_SHEET + 'print(bomb_shell["abilities", "wisdom"])\n',
             fails_at=0, message_contains="KeyError: ('abilities', 'wisdom')"),
        dict(why="a capital letter in the key", code=BOMB_SHEET + 'print(bomb_shell["abilities"]["Wisdom"])\n',
             fails_at=0, message_contains="KeyError: 'Wisdom'"),
        dict(why="the keys without quotes (box names, not text)",
             code=BOMB_SHEET + "print(bomb_shell[abilities][wisdom])\n", fails_at=0,
             message_contains="name 'abilities' is not defined"),
        dict(why="the inner card read by position (a dict has no positions)",
             code=BOMB_SHEET + 'print(bomb_shell["abilities"][1])\n', fails_at=0, message_contains="KeyError: 1"),
        dict(why="the sheet flattened so the skipped level works",
             code=BOMB_SHEET.replace('    "mana": 24,\n', '    "mana": 24,\n    "wisdom": 8,\n')
             + 'print(bomb_shell["wisdom"])\n', fails_at=1, message_contains="not on the outside"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-nested", solo="false", dictates="",
             foreign_names="lantern,parts,wick,oil", stages="P,R,I", gate="pattern:NestedSubscript",
             moment="boxes in boxes (teacher-led, 5 min)") + "\n"
        "Predict: one key prints the whole inner card (the spec's 'bomb_shell[\"abilities\"] alone prints the whole "
        "inner dict'). Investigate: the optional 'Skip a level on purpose' angle (bomb_shell[\"wisdom\"] after the "
        "tick, then change it back; moved out of the Learn text by the teacher's ruling). TR: "
        "the boxes-in-boxes picture is the first angle (static until the live tracer). CP1 is goal-only: the "
        "message names the keys, the hint ladder ends on the Example's names. CMB reruns with wisdom 11, so "
        "`print(8)` fails. A flattened sheet (wisdom copied to the outside) gets its own message. Side quest (BQ, "
        "combining nested read + comparison): wisdom at least 10, checked at 10 (exactly enough), 9 and 14. Rest of "
        "the KeyError family is proven in WA: a skipped level, a capital, both keys in one bracket, position 1."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4B-02 change-inside
# ---------------------------------------------------------------------------------------------

BOMB_HANDS = (
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "abilities": {\n'
    '        "dexterity": 6,\n'
    '        "wisdom": 8,\n'
    "    },\n"
    "}\n"
)
HANDS_PRINT = 'print(bomb_shell["abilities"])\n'
HANDS_STARTER = (
    BOMB_HANDS + "\n"
    "# Gearshift tunes Bomb Shell's\n"
    "# hands: dexterity goes up by 2.\n"
    "# Get it, change it, put it back.\n"
    "\n" + HANDS_PRINT
)
HANDS_LINE = 'dex = bomb_shell["abilities"]["dexterity"]\nbomb_shell["abilities"]["dexterity"] = dex + 2\n'
HANDS_ONE_LINE = 'bomb_shell["abilities"]["dexterity"] = bomb_shell["abilities"]["dexterity"] + 2\n'


def _hands(line=HANDS_LINE, sheet=BOMB_HANDS):
    return sheet + "\n" + line + "\n" + HANDS_PRINT


JAR_EXAMPLE = (
    'jar = {"lid": {"turns": 4}}\n'
    'old = jar["lid"]["turns"]\n'
    'jar["lid"]["turns"] = old + 1\n'
    "print(jar)\n"
)

_DEX_STATE = r'''
assert type(globals().get('bomb_shell')).__name__ == 'dict', _keep('bomb_shell')
_ab = bomb_shell.get('abilities')
assert type(_ab).__name__ == 'dict', __NO_ABIL__
assert 'dexterity' not in bomb_shell, __FLAT__
assert _ab.get('wisdom') == 8, __WISDOM__
_dx = _ab.get('dexterity')
assert type(_dx).__name__ == 'int', __NUM__
assert _dx != 6, __STILL__
assert _dx == 8, __ADD_TWO__ + ' It is ' + str(_dx) + ' now, not 8.'
'''

_DEX_FOLLOW = r'''
for _old in (3, 11):
    _tried = '`bomb_shell["abilities"]["dexterity"] = ' + str(_old) + '`'
    _ns, _ls, _err, _miss = _rerun([('bomb_shell', 'bomb_shell["abilities"]["dexterity"] = ' + str(_old))])
    assert not _miss, _keep('bomb_shell')
    assert not _err, _stop(_err, _tried)
    _new = _get(_ns.get('bomb_shell'), 'abilities', 'dexterity')
    if _new != _old + 2:
        _end = ': the dexterity became ' + _lit(_new) + ', not ' + str(_old + 2)
        assert _new != _old, __LITERAL__ + ' ' + _did(_tried, _end)
        assert _new != 8, __TYPED__ + ' ' + _did(_tried, _end)
        assert False, __FIX__ + ' ' + _did(_tried, _end)
'''

CHANGE_INSIDE = dict(
    id="change-inside",
    title="Change inside",
    martu=(
        "Reading inside is half the job. Writing inside uses the same path, on the left of `=`.\n"
        "*Get it, change it, put it back.* The right side reads the old value, and Python works it out first. "
        "Then the left side puts the new value back in the same spot.\n"
        "Get it into a variable, change it, then put it back with the same two keys on the left, as in the Example."
    ),
    example=JAR_EXAMPLE,
    example_output="{'lid': {'turns': 5}}",
    names=["bomb_shell"],
    starter=HANDS_STARTER,
    checkpoints=[
        dict(
            id="tune-the-hands",
            text="Gearshift tunes Bomb Shell's hands: add 2 to the dexterity inside `\"abilities\"`.",
            dictated=False,
            hints=[
                "Below the sheet, above the `print`. The right side reads the old dexterity and adds 2. The left "
                "side is the same path.",
                "Get it, change it, put it back: `old = jar[\"lid\"][\"turns\"]`, then "
                "`jar[\"lid\"][\"turns\"] = old + 1`.",
                "Write `dex = bomb_shell[\"abilities\"][\"dexterity\"]`, then "
                "`bomb_shell[\"abilities\"][\"dexterity\"] = dex + 2`, above `print(bomb_shell[\"abilities\"])`.",
            ],
            checks=[
                (
                    "the dexterity is up by 2",
                    dx() + fill(
                        _DEX_STATE,
                        no_abil="Keep `\"abilities\"` inside the sheet, as the starter has it.",
                        flat="Dexterity lives inside `\"abilities\"`: write to "
                             "`bomb_shell[\"abilities\"][\"dexterity\"]`. Your line made a new `\"dexterity\"` key on "
                             "the outside of the sheet.",
                        wisdom="Leave the wisdom as it is. Only the dexterity goes up.",
                        num="Keep the dexterity a number, with no quotes.",
                        still="Store the new value back: `bomb_shell[\"abilities\"][\"dexterity\"] = ...`. The "
                              "dexterity is still 6.",
                        add_two="Add 2 to the old dexterity, 6.",
                    ),
                ),
                (
                    "the new dexterity follows the old one",
                    dx() + fill(
                        _DEX_FOLLOW,
                        literal="Change it with code below the sheet, not by editing the 6 in the sheet: get the "
                                "old dexterity, then add 2.",
                        typed="Build it from the old value: read `bomb_shell[\"abilities\"][\"dexterity\"]` "
                              "first, then add 2. A typed 8 stays 8.",
                        fix="Get the old dexterity, add 2, and put it back with the same two keys on the left.",
                    ),
                ),
            ],
            pass_line="Lucky: That latch might stop hating you.",
        ),
    ],
    solution=_hands(),
    assemble=dict(
        lines=[line for line in _hands().splitlines() if line.strip()],
        distractors=[
            'bomb_shell["dexterity"] = dex + 2',
            'dex = 6',
        ],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Get it, change it, put it back",
            text=(
                "1. Get it: `dex = bomb_shell[\"abilities\"][\"dexterity\"]` puts 6 in `dex`.\n"
                "2. Change it: `dex + 2` is 8.\n"
                "3. Put it back: `bomb_shell[\"abilities\"][\"dexterity\"] = dex + 2` stores 8 in the same spot, "
                "inside `\"abilities\"`.\n"
                "The wisdom next to it does not change."
            ),
        ),
        dict(
            angle="picture",
            label="Same path, both lines",
            text=(
                "```text\nget it:       6 -> dex\nchange it:    dex + 2 is 8\n"
                "put it back:  8 -> [\"abilities\"]\n                   [\"dexterity\"]\n```\n"
                "The first line and the last line walk the same two keys. One reads, one writes."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "A score sheet in a binder: find the page, find the line, read the number, rub it out, write the "
                "new one in the same line. You don't start a new sheet."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Holding the barrier, the campaign wrote `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]`. "
                "Read the old value, change it, put it back. Here the spot is one level deeper."
            ),
        ),
        dict(
            angle="shorter",
            label="In one line",
            text=(
                "The campaign did it in one line: `caster[\"mana\"] = caster[\"mana\"] - cost`. The same path on both "
                "sides. Both ways pass."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "You have seen this shape: the right side reads the old mana, the left side stores the new one. Bomb "
            "Shell's dexterity works the same way, with one more key on each side."
        ),
    ),
    takeaway="Change a value inside: get it, change it, put it back with the same two keys: "
             "`dex = sheet[\"a\"][\"b\"]`, then `sheet[\"a\"][\"b\"] = dex + 2`.",
    wrong_answers=[
        dict(why="the starter (no line yet)", code=HANDS_STARTER, fails_at=1, message_contains="still 6"),
        dict(why="a typed 8 (CMB: typing literal numbers instead of reading by key)",
             code=_hands('bomb_shell["abilities"]["dexterity"] = 8\n'), fails_at=1, message_contains="typed 8"),
        dict(why="6 + 2 worked out by hand (CMB)", code=_hands('bomb_shell["abilities"]["dexterity"] = 6 + 2\n'),
             fails_at=1, message_contains="typed 8"),
        dict(why="the 6 in the sheet edited to 8 instead of a line of code",
             code=_hands("", BOMB_HANDS.replace('"dexterity": 6', '"dexterity": 8')), fails_at=1,
             message_contains="not by editing"),
        dict(why="a skipped level on the right side (KeyError)",
             code=_hands('bomb_shell["dexterity"] = bomb_shell["dexterity"] + 2\n'), fails_at=0,
             message_contains="KeyError: 'dexterity'"),
        dict(why="a skipped level on the left side: a new flat key",
             code=_hands('bomb_shell["dexterity"] = bomb_shell["abilities"]["dexterity"] + 2\n'), fails_at=1,
             message_contains="on the outside"),
        dict(why="worked out but never stored", code=_hands('bomb_shell["abilities"]["dexterity"] + 2\n'),
             fails_at=1, message_contains="Store the new value back"),
        dict(why="stored in a new box instead of the sheet",
             code=_hands('dexterity = bomb_shell["abilities"]["dexterity"] + 2\n'), fails_at=1,
             message_contains="Store the new value back"),
        dict(why="dot access (bomb_shell.abilities)", code=_hands("bomb_shell.abilities.dexterity += 2\n"),
             fails_at=0, message_contains="has no attribute 'abilities'"),
        dict(why="the new value in quotes (text)", code=_hands('bomb_shell["abilities"]["dexterity"] = "8"\n'),
             fails_at=1, message_contains="no quotes"),
        dict(why="two steps, never put back (dex changed, the sheet not)",
             code=_hands('dex = bomb_shell["abilities"]["dexterity"]\ndex = dex + 2\n'), fails_at=1,
             message_contains="Store the new value back"),
        dict(why="two steps, put back on a flat key (a skipped level on the left)",
             code=_hands('dex = bomb_shell["abilities"]["dexterity"]\nbomb_shell["dexterity"] = dex + 2\n'),
             fails_at=1, message_contains="on the outside"),
        dict(why="the old value typed into dex (CMB: a literal instead of reading by key)",
             code=_hands('dex = 6\nbomb_shell["abilities"]["dexterity"] = dex + 2\n'), fails_at=1,
             message_contains="Build it from the old value"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="dict-nested,dict-write", solo="false", dictates="",
             foreign_names="jar,lid,turns,old,cost", stages="M") + "\n"
        "The nested read-modify-write, in the Example's two-step form (teacher's ruling: the Example cannot fit a "
        "one-line nested write in 36 characters, so the Learn text, the starter comment, the hints, the solution "
        "and Assemble all use `dex = ...` then `... = dex + 2`). The one-line campaign shape "
        "(HANDS_ONE_LINE) and `+= 2` pass too; the 'In one line' angle says so. CMB: the dexterity is reset to 3 "
        "and to 11 right after "
        "the sheet, inside the check, and must end 2 higher: a typed 8 (or 6 + 2) stays 8, and an edited sheet "
        "with no line stays 3 ('not by editing the 6'). A flat `bomb_shell[\"dexterity\"]` on the left is the "
        "skipped-level slip written instead of read. The starter's last line prints the inner card, so each Run "
        "shows the change. The put-back line is 45 characters, longer than a phone line, because the nested path "
        "itself is 35."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4B-03 the-roster
# ---------------------------------------------------------------------------------------------


def _sheet(var, name, mana, abilities):
    out = f"{var} = {{\n" f'    "name": "{name}",\n' f'    "mana": {mana},\n' '    "abilities": {\n'
    for key, value in abilities:
        out += f'        "{key}": {value},\n'
    return out + "    },\n}\n"


ROSTER_SHEETS = (
    _sheet("oogrish", "Oogrish", 18, [("intelligence", 17), ("magical_affinity", 9)]) + "\n"
    + _sheet("gearshift", "Gearshift", 20, [("intelligence", 14), ("magical_affinity", 10)]) + "\n"
    + _sheet("bomb_shell", "Bomb Shell", 24, [("intelligence", 14), ("magical_affinity", 12)]) + "\n"
    + _sheet("lucky", "Lucky", 26, [("intelligence", 13), ("magical_affinity", 13)]) + "\n"
    + "roster = [\n    oogrish,\n    gearshift,\n    bomb_shell,\n    lucky,\n]\n"
)
ROSTER_STARTER = (
    ROSTER_SHEETS + "\n"
    "# 1. Print Lucky's name, through\n"
    "#    roster.\n"
    "\n"
    "# 2. Print Oogrish's intelligence,\n"
    "#    through roster.\n"
)
ROSTER_NAME = 'print(roster[3]["name"])\n'
ROSTER_INT = 'print(roster[0]["abilities"]["intelligence"])\n'


def _roster(name=ROSTER_NAME, smart=ROSTER_INT):
    return ROSTER_SHEETS + "\n" + name + smart


SHELF_EXAMPLE = (
    "shelf = [\n"
    '    {"title": "Maps", "pages": 40},\n'
    '    {"title": "Runes", "pages": 12},\n'
    "]\n"
    'print(shelf[1]["title"])\n'
)
_REORDER = ("roster", "roster = [bomb_shell, lucky, gearshift, oogrish]")
_REORDER_TRIED = "the sheets in another order, `roster = [bomb_shell, lucky, gearshift, oogrish]`"

THE_ROSTER = dict(
    id="the-roster",
    title="The roster",
    martu=(
        "Four heroes, four sheets. A list holds them all, in order. The list remembers order. Each sheet "
        "remembers meaning.\n"
        "To read one line, give the position first, then the key. `roster[2]` is the third sheet, since "
        "positions count from 0. `roster[2][\"name\"]` is its name.\n"
        "A hero's name is not a position. `roster[\"Lucky\"]` stops Python: a list only takes numbers in its "
        "brackets."
    ),
    example=SHELF_EXAMPLE,
    example_output="Runes",
    names=["roster"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=(
            "roster = [\n"
            '    {"name": "Oogrish"},\n'
            '    {"name": "Gearshift"},\n'
            '    {"name": "Bomb Shell"},\n'
            '    {"name": "Lucky"},\n'
            "]\n"
            'print(roster[2]["name"])\n'
        ),
        choices=["Bomb Shell", "Gearshift", "Lucky", "an error"],
        answer=0,
        explain=(
            "`roster[2]` is the third sheet (0, 1, 2), Bomb Shell's. Then `[\"name\"]` reads its name. Gearshift "
            "counts from 1. Lucky is position 3."
        ),
    ),
    starter=ROSTER_STARTER,
    checkpoints=[
        dict(
            id="third-sheet-name",
            text="Print Lucky's name, read through `roster`.",
            dictated=False,
            hints=[
                "Lucky is the fourth sheet, and positions count from 0.",
                "`shelf[1][\"title\"]` picks the second book on the shelf, then reads its title.",
                "Write `print(roster[3][\"name\"])` under `# 1.`",
            ],
            checks=[
                read_check(
                    "Lucky's name is printed", "Lucky",
                    "Print Lucky's name through `roster`: his position in the list, then the key `\"name\"`.",
                    inside="Lucky",
                    whole="Add the key, `[\"name\"]`, after Lucky's position. Your line printed the whole sheet.",
                    near=[("Bomb Shell", "Positions count from 0: `roster[2]` is the third sheet, Bomb Shell. Lucky "
                                         "is one further."),
                          ("Gearshift", "Lucky is further along: your line printed Gearshift, at position 1. "
                                        "Positions count from 0."),
                          ("Oogrish", "Lucky is the fourth sheet: your line printed Oogrish, at position 0. "
                                      "Positions count from 0.")],
                ),
                follow_check(
                    "the name comes through the roster", [_REORDER], _REORDER_TRIED, "Oogrish", "Lucky",
                    typed="Read it through the list, `roster[3][\"name\"]`, so it follows the roster.",
                    fix="Print Lucky's name through `roster`, so the line follows the roster.",
                ),
            ],
            pass_line="Lucky: Position three. Saved the best for last.",
        ),
        dict(
            id="oogrish-intelligence",
            text="Print Oogrish's intelligence. Read it through `roster`.",
            dictated=False,
            hints=[
                "Oogrish is the first sheet in the list. His intelligence lives inside `\"abilities\"`: so one "
                "position, then two keys.",
                "Three brackets, read left to right: `drawer[1][\"card\"][\"score\"]` is position 1, then the outer "
                "key, then the inner key.",
                "Write `print(roster[0][\"abilities\"][\"intelligence\"])` under `# 2.`",
            ],
            checks=[
                read_check(
                    "Oogrish's intelligence is printed", 17,
                    "Print Oogrish's intelligence: `roster[0]`, then `[\"abilities\"]`, then `[\"intelligence\"]`.",
                    inside="intelligence",
                    whole="Add the inner key, `[\"intelligence\"]`. Your line printed a whole card.",
                    near=[(14, "Oogrish is the first sheet: position 0. Your line printed 14, another hero's "
                               "intelligence."),
                          (13, "Oogrish is the first sheet: position 0. Your line printed 13, Lucky's "
                               "intelligence.")],
                ),
                roster_check(
                    "the read goes through roster", 'roster[0]["abilities"]["intelligence"] = 11',
                    "a roster copy where Oogrish's intelligence is 11", 11, 17,
                    "Read it through `roster`: Oogrish is at position 0, so start with `roster[0]`.",
                ),
                follow_check(
                    "the intelligence follows Oogrish's sheet",
                    [("oogrish", 'oogrish["abilities"]["intelligence"] = 11')],
                    '`oogrish["abilities"]["intelligence"] = 11`', 11, 17,
                    typed="Read it from the sheet, so it follows: through `roster`, not a typed 17.",
                    fix="Print Oogrish's intelligence through `roster`: a position, then two keys.",
                ),
            ],
            pass_line="Oogrish: Steady, now. Seventeen, and still learning.",
        ),
    ],
    solution=_roster(),
    partials=[_roster(smart="")],
    assemble=dict(
        lines=[line for line in _roster().splitlines() if line.strip()],
        distractors=['print(roster["Bomb Shell"]["name"])', 'print(roster[0]["intelligence"])'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A row of sheets",
            text=(
                "```text\nroster\n  [0]  oogrish\n  [1]  gearshift\n  [2]  bomb_shell\n  [3]  lucky\n\n"
                "roster[2][\"name\"]\n  [2]      -> the bomb_shell sheet\n  [\"name\"] -> \"Bomb Shell\"\n```\n"
                "The list is numbered. Each sheet inside it has its own keys."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `roster[0]`: the first sheet, Oogrish's.\n"
                "2. `[\"abilities\"]`: his ability card.\n"
                "3. `[\"intelligence\"]`: one line of the card, 17.\n"
                "Numbers for the list, keys in quotes for the sheets."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Every Module 2 part ended with `for member in party.members:`. That list was the roster: four "
                "sheets, in order. Each `member` was one whole sheet, read by key."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "The Institute kept its records in a drawer, in order. To find one, you counted to the right "
                "folder. To read it, you used the keys inside."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="for member in party.members:",
        why=(
            "In the campaign, this list is called `party.members`. Each member was a sheet like these, so "
            "`member[\"spell_book\"]` read one sheet's book, by key."
        ),
    ),
    takeaway="A list of sheets: position first, then keys. `roster[2][\"name\"]`; never `roster[\"Lucky\"]`.",
    wrong_answers=[
        dict(why="the starter (nothing printed)", code=ROSTER_STARTER, fails_at=1, message_contains="his position"),
        dict(why="a name as the position: roster[\"Lucky\"] (TypeError)",
             code=_roster(name='print(roster["Lucky"]["name"])\n'), fails_at=0,
             message_contains="list indices must be integers or slices, not str"),
        dict(why="the predict's line copied: roster[2] (Bomb Shell)", code=_roster(name='print(roster[2]["name"])\n'),
             fails_at=1, message_contains="Lucky is one further"),
        dict(why="a position and a key in one [ ]: roster[3, \"name\"] (TypeError)",
             code=_roster(name='print(roster[3, "name"])\n'), fails_at=0, message_contains="not tuple"),
        dict(why="the sheet's variable as the position: roster[lucky] (TypeError)",
             code=_roster(name='print(roster[lucky]["name"])\n'), fails_at=0, message_contains="not dict"),
        dict(why="counting from 1: roster[4] (IndexError)", code=_roster(name='print(roster[4]["name"])\n'),
             fails_at=0, message_contains="list index out of range"),
        dict(why="counting from 1 the other way: roster[1] (Gearshift)",
             code=_roster(name='print(roster[1]["name"])\n'), fails_at=1, message_contains="Gearshift, at position 1"),
        dict(why="the whole sheet printed (no key)", code=_roster(name="print(roster[3])\n"), fails_at=1,
             message_contains="whole sheet"),
        dict(why="the name typed (CMB)", code=_roster(name='print("Lucky")\n'), fails_at=1,
             message_contains="through the list"),
        dict(why="read from the sheet's own box, not through roster",
             code=_roster(name='print(lucky["name"])\n'), fails_at=1, message_contains="through the list"),
        dict(why="a dict read by position: roster[3][0] (KeyError: 0)", code=_roster(name="print(roster[3][0])\n"),
             fails_at=0, message_contains="KeyError: 0"),
        dict(why="dot access on a sheet", code=_roster(name="print(roster[3].name)\n"), fails_at=0,
             message_contains="has no attribute 'name'"),
        dict(why="CP2 a skipped level: roster[0][\"intelligence\"] (KeyError)",
             code=_roster(smart='print(roster[0]["intelligence"])\n'), fails_at=0,
             message_contains="KeyError: 'intelligence'"),
        dict(why="CP2 the wrong position (Gearshift's 14)",
             code=_roster(smart='print(roster[1]["abilities"]["intelligence"])\n'), fails_at=2,
             message_contains="position 0"),
        dict(why="CP2 read from the box, not through roster",
             code=_roster(smart='print(oogrish["abilities"]["intelligence"])\n'), fails_at=2,
             message_contains="through `roster`"),
        dict(why="CP2 roster[\"Oogrish\"] (TypeError)",
             code=_roster(smart='print(roster["Oogrish"]["abilities"]["intelligence"])\n'), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="CP2 typed 17 with roster in the line",
             code=_roster(smart='print(roster[0]["name"], 17)\n'), fails_at=2, message_contains="through `roster`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="list-of-dicts,dict-nested", solo="false", dictates="",
             foreign_names="shelf,title,pages,drawer,card,score", stages="P,M") + "\n"
        "The four sheets use the real party table (mana is the max: 18, 20, 24, 26; intelligence 17, 14, 14, 13; "
        "affinity 9, 10, 12, 13), built in the starter, with `roster` over several lines (phone width). CP1 is "
        "goal-only (teacher's ruling): Lucky's name, at position 3, so it is not a copy of the predict's "
        "`roster[2]` (that copy gets 'Lucky is one further'; `roster[-1]` passes too). Its CMB reorders the roster "
        "inside the check (`roster[3]` becomes Oogrish), so a typed name or `lucky[\"name\"]` fails 'through the "
        "list'. CP2 is goal-only: the value first (near misses named), its Teach rung a three-bracket read, "
        "then roster_check (a roster of copies with Oogrish's intelligence at 11, so a read of `oogrish` or a "
        "typed 17 fails, while `first = roster[0]` passes), then CMB on the sheet's own box. Lucky's box is "
        "the campaign link ('In the campaign, this list is called `party.members`')."
    ),
)


# ---------------------------------------------------------------------------------------------
# 4B-04 spell-book-of-spells (point-at-it)
# ---------------------------------------------------------------------------------------------

GLOW_BOOK = (
    "spell_book = {\n"
    '    "Glow": {\n'
    '        "mana_cost": 2,\n'
    '        "required_affinity": 3,\n'
    "    },\n"
    "}\n"
)
WARD_VARS = 'spell_name = "Lantern Ward"\ncost = 6\nneeded = 9\n'


def _ward_spell(cost="0", needed="0"):
    return f'spell = {{\n    "mana_cost": {cost},\n    "required_affinity": {needed},\n}}\n'


WARD_STARTER = (
    GLOW_BOOK + "\n" + WARD_VARS + "\n"
    "# 1. Replace each 0 with the\n"
    "#    variable that holds that value.\n"
    + _ward_spell() + "\n"
    "# 2. Store the spell in spell_book,\n"
    "#    with spell_name as the key.\n"
    "# 3. Only store it if spell_name\n"
    "#    is not in spell_book yet.\n"
    "\n"
    "print(spell_book)\n"
)
WARD_STORE_PLAIN = "spell_book[spell_name] = spell\n"
WARD_STORE = "if spell_name not in spell_book:\n    spell_book[spell_name] = spell\n"


def _ward(spell=None, store=WARD_STORE, head=GLOW_BOOK + "\n" + WARD_VARS + "\n"):
    spell = _ward_spell("cost", "needed") if spell is None else spell
    return head + spell + "\n" + store + "\n" + "print(spell_book)\n"


PANTRY_EXAMPLE = 'pantry = {"bread": 2}\nfood = "apples"\namount = 5\npantry[food] = amount\nprint(pantry)\n'

_SPELL_STATE = r'''
assert type(globals().get('spell')).__name__ == 'dict', _keep('spell')
for _k in ('mana_cost', 'required_affinity'):
    _x = _near(spell, _k)
    assert _x is None, ('`spell` has a key ' + _lit(_x) + '. The starter' + chr(39) + 's key is `"' + _k
                        + '"`, letter for letter.')
    assert _k in spell, ('Keep the key `"' + _k + '"` in `spell`, as the starter has it. Change only the value '
                         'after the colon.')
_mc, _ra = spell['mana_cost'], spell['required_affinity']
assert not [_v for _v in (_mc, _ra) if type(_v).__name__ == 'str'], __QUOTED__ + ' ' + _QUOTES
assert _mc != 0 and _ra != 0, __ZERO__
assert not (_mc == 9 and _ra == 6), __SWAP__
assert _mc == 6, __COST__
assert _ra == 9, __NEEDED__
'''

_SPELL_FOLLOW = r'''
_tried = '`cost = 5` and `needed = 7`'
_ns, _ls, _err, _miss = _rerun([('cost', 'cost = 5'), ('needed', 'needed = 7')])
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
_sp = _ns.get('spell')
_got = (_get(_sp, 'mana_cost'), _get(_sp, 'required_affinity'))
assert _got == (5, 7), __TYPED__ + ' ' + _did(_tried, ': the spell still held ' + _lit(_got[0]) + ' and ' + _lit(_got[1]))
'''

_STORE_STATE = r'''
assert type(globals().get('spell_book')).__name__ == 'dict', _keep('spell_book')
assert 'spell_name' not in spell_book, __QUOTED_KEY__ + ' ' + _QUOTES
assert 'Glow' in spell_book, __GLOW__
if 'Lantern Ward' not in spell_book:
    _asks = [_c for _c in _ast.walk(_ast.parse(_source)) if type(_c).__name__ == 'Compare'
             and type(_c.ops[0]).__name__ == 'In' and type(_c.left).__name__ == 'Name' and _c.left.id == 'spell_name']
    assert not _asks, __ALREADY__
    assert False, __STORE__
_pg = spell_book['Lantern Ward']
assert type(_pg).__name__ != 'str', __TEXT__
assert _pg == spell, __SPELL__
'''

_STORE_FOLLOW = r'''
_tried = '`spell_name = "Frost Veil"`, `cost = 5` and `needed = 7`'
_ns, _ls, _err, _miss = _rerun([('spell_name', 'spell_name = "Frost Veil"'), ('cost', 'cost = 5'),
                                ('needed', 'needed = 7')])
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
_bk = _ns.get('spell_book')
assert _get(_bk, 'Frost Veil') != '(missing)', __TYPED_KEY__ + ' ' + _did(_tried, ': the book got no Frost Veil page')
_pg = _get(_bk, 'Frost Veil')
assert _pg == _ns.get('spell') and _get(_pg, 'mana_cost') == 5, __TYPED_SPELL__ + ' ' + _did(_tried)
assert _get(_bk, 'Glow') != '(missing)', __GLOW__ + ' ' + _did(_tried)
'''

_GUARD = r'''
_tr = _ast.parse(_source)
_ifs = [_n for _n in _ast.walk(_tr) if type(_n).__name__ == 'If']
_in_ifs = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Compare']
_cmp = [_c for _c in _in_ifs if type(_c.ops[0]).__name__ in ('In', 'NotIn')]
_quoted = [_c for _c in _cmp if type(_c.left).__name__ == 'Constant' and _c.left.value == 'spell_name']
_values = [_c.left.id for _c in _cmp if type(_c.left).__name__ == 'Name' and _c.left.id in ('cost', 'needed')]
_typed_list = [_c for _c in _cmp if type(_c.comparators[0]).__name__ in ('List', 'Tuple', 'Set')]
_wrong_way = [_c for _c in _cmp if type(_c.ops[0]).__name__ == 'In' and type(_c.left).__name__ == 'Name'
              and _c.left.id == 'spell_name']
_typed = [_c for _c in _in_ifs
          if [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Name' and _x.id == 'spell_name']
          and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
               and type(_x.value).__name__ == 'str']]
_top_store = [_n for _n in _tr.body if type(_n).__name__ in ('Assign', 'AugAssign')
              and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
                   if type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name'
                   and _t.value.id == 'spell_book']]
if _quoted:
    _why = __QUOTED_IF__ + ' ' + _QUOTES
elif _values:
    _why = __VALUE__ + ' Your `if` asks about `' + _values[0] + '`.'
elif _typed_list:
    _why = __TYPED_LIST__
elif _wrong_way:
    _why = __WRONG_WAY__
elif _cmp and _top_store:
    _why = __INDENT__ + ' Line ' + str(_top_store[0].lineno) + ' stores every time.'
elif _typed and not _cmp:
    _why = __TYPED__
elif not _cmp:
    _why = __NO_IF__
else:
    _why = __FIX__
for _tried, _changes, _who, _page, _what in __CASES__:
    _ns, _ls, _err, _miss = _rerun(_changes)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_err, _tried)
    _got = _get(_ns.get('spell_book'), _who)
    if _page is None:
        assert _got != '(missing)' and _got == _ns.get('spell'), (
            __STORE_NEW__ + ' ' + _did(_tried, ': the book got no ' + _who + ' page'))
    else:
        assert _got == _page, _why + ' ' + _did(_tried, ': ' + _what + ' was written over')
'''

GUARD_CASES = [
    ('`spell_name = "Glow"`, `cost = 9` and `needed = 9`',
     [("spell_name", 'spell_name = "Glow"'), ("cost", "cost = 9"), ("needed", "needed = 9")],
     "Glow", {"mana_cost": 2, "required_affinity": 3}, "Glow's page"),
    ('`spell_name = "Moon Step"`, a name with no page yet', [("spell_name", 'spell_name = "Moon Step"')],
     "Moon Step", None, ""),
    ("another name that already has a page in `spell_book`",
     [("spell_book", 'spell_book["Ash Ward"] = {"mana_cost": 7, "required_affinity": 8}'),
      ("spell_name", 'spell_name = "Ash Ward"')],
     "Ash Ward", {"mana_cost": 7, "required_affinity": 8}, "that page"),
]

_IN_THE_BOOK = r'''
_tr = _ast.parse(_source)
# The store's own guard (`if spell_name not in spell_book:` over the store line) is not the side quest's question.
_guards = [id(_c) for _i in _ast.walk(_tr) if type(_i).__name__ == 'If'
           and [_s for _s in _ast.walk(_i) if type(_s).__name__ == 'Assign'
                and [_t for _t in _s.targets if type(_t).__name__ == 'Subscript']]
           for _c in _ast.walk(_i.test)]
_tests = [_n for _n in _ast.walk(_tr) if type(_n).__name__ == 'Compare'
          and type(_n.ops[0]).__name__ in ('In', 'NotIn') and id(_n) not in _guards]
assert _tests, __USE_IN__
_ward = [_t for _t in _tests if (type(_t.left).__name__ == 'Constant' and _t.left.value == 'Lantern Ward')
         or (type(_t.left).__name__ == 'Name' and _t.left.id == 'spell_name')]
assert _ward, __OTHER__
if not _said(_lines(), 'True'):
    assert type(_ward[-1].ops[0]).__name__ != 'NotIn', __NOT_IN__
    assert False, __AFTER__
'''

SPELL_BOOK_OF_SPELLS = dict(
    id="spell-book-of-spells",
    title="A spell book of spells",
    martu=(
        "A spell book is a dictionary of spells. Each key is a spell's name. Each value is a little sheet of its "
        "own: what the spell costs, and the affinity it needs.\n"
        "To add a page, build the spell from your variables. Then store it under its name: "
        "`spell_book[spell_name] = spell`.\n"
        "No quotes around `spell_name`. " + QUOTES_RULE + " The box holds `\"Lantern Ward\"`, so that is the page "
        "you get.\n"
        "Then ask first, as the campaign did: `if spell_name not in spell_book:`, with the store line indented "
        "under it. A page that is already there stays as it is."
    ),
    example=PANTRY_EXAMPLE,
    example_output="{'bread': 2, 'apples': 5}",
    names=["spell", "cost", "needed", "spell_book", "spell_name"],
    predict=dict(
        q="Before you press Run: what does this print?",
        code=(
            "book = {\n"
            '    "Glow": {\n'
            '        "mana_cost": 2,\n'
            '        "required_affinity": 3,\n'
            "    },\n"
            "}\n"
            'print(book["Glow"]["mana_cost"])\n'
        ),
        choices=["3", "2", "{'mana_cost': 2, 'required_affinity': 3}", "an error"],
        answer=1,
        explain=(
            "`book[\"Glow\"]` is Glow's page, a small dictionary. Then `[\"mana_cost\"]` reads one line of that "
            "page: 2. A spell book is sheets inside a sheet, like Bomb Shell's abilities."
        ),
    ),
    pair_talk=(
        "Tell your partner what `spell_book[\"spell_name\"] = spell` would store, and why. Then each of you stores "
        "the spell on your own screen."
    ),
    starter=WARD_STARTER,
    checkpoints=[
        dict(
            id="fill-the-spell",
            text="Replace each 0 in `spell` with the variable that holds that value.",
            dictated=True,
            hints=[
                "Look at the three variables above `spell`. Which holds the cost? Which holds the affinity the "
                "spell needs? Their names differ from the keys on purpose.",
                "A value can be a variable: `{\"bread\": amount}` puts whatever is in `amount` there. No quotes, so "
                "Python looks inside the box.",
                "Write `\"mana_cost\": cost,` and `\"required_affinity\": needed,` in place of the two 0 lines.",
            ],
            checks=[
                (
                    "the spell holds the cost and the affinity",
                    dx() + fill(
                        _SPELL_STATE,
                        quoted="Take the quotes off the variable names.",
                        zero="Replace each 0 with the variable that holds that value: `spell` still holds the "
                             "starter's 0.",
                        swap="You swapped them: `\"mana_cost\"` holds 9, which is `needed`. The cost is in `cost`.",
                        cost="`\"mana_cost\"` should hold the variable `cost`.",
                        needed="`\"required_affinity\"` should hold the variable `needed`.",
                    ),
                ),
                (
                    "the spell follows the variables",
                    dx() + fill(
                        _SPELL_FOLLOW,
                        typed="Use the variables, not typed numbers: `\"mana_cost\": cost`, so the spell follows "
                              "them.",
                    ),
                ),
            ],
            pass_line="Gearshift: Cost and need, both read from the variables. Math checks out.",
        ),
        dict(
            id="store-by-name",
            text="Store `spell` in `spell_book`, under the name that `spell_name` holds.",
            dictated=False,
            hints=[
                "Below `spell`, above the `print`. The key is the variable `spell_name`, with no quotes.",
                "`pantry[food] = amount` stores under whatever name `food` holds: `\"apples\"`.",
                "Write `spell_book[spell_name] = spell` above `print(spell_book)`.",
            ],
            checks=[
                (
                    "the spell is stored under its name",
                    dx() + fill(
                        _STORE_STATE,
                        quoted_key="`spell_book` has a key `\"spell_name\"`: those exact letters. Take the quotes "
                                   "off: `spell_book[spell_name]`.",
                        glow="Keep Glow in the book: add the new page with `spell_book[spell_name] = spell`, not a "
                             "new book.",
                        already="Store it when the name is new: `not in`, not `in`. Your `if` stores only when the "
                                "name is already in `spell_book`.",
                        store="Store the spell: `spell_book[spell_name] = spell`, below `spell`.",
                        text="Store the spell itself, `spell`, with no quotes. `\"spell\"` is just the word.",
                        spell="Store the spell itself: `= spell` on the right side.",
                    ),
                ),
                (
                    "the page follows spell_name",
                    dx() + fill(
                        _STORE_FOLLOW,
                        typed_key="Use the variable as the key, `spell_book[spell_name]`, so a new name gets a new "
                                  "page.",
                        typed_spell="Store the spell itself, `= spell`, not a typed copy.",
                        glow="Keep Glow in the book: add a page, don't make a new book.",
                    ),
                ),
            ],
            pass_line="Gearshift: Page stored. Math checks out.",
        ),
        dict(
            id="store-if-new",
            text=(
                "Store it only when the name is new: put your store line under `if spell_name not in spell_book:`, "
                "indented."
            ),
            dictated=True,
            hints=[
                "The `if` asks first. The store line goes under it, indented.",
                "`if \"map\" not in pack:` with `pack[\"map\"] = 1` indented under it adds a map only when there is "
                "none.",
                "Write `if spell_name not in spell_book:` above the store line, and indent the store line under it.",
            ],
            checks=[
                (
                    "a page that is already there stays as it is",
                    dx() + fill(
                        _GUARD,
                        cases=GUARD_CASES,
                        quoted_if="Ask about the name inside `spell_name`: `\"spell_name\"` in quotes is just those "
                                  "letters, and no page is called that.",
                        value="Ask about the name: `in` looks at the keys only, never the values.",
                        typed_list="Ask `spell_book` itself whether the name is in it: your `if` asks a list of "
                                   "names you typed.",
                        wrong_way="Use `not in`: your `if` stores only when the name is already in `spell_book`.",
                        indent="Indent the store line under the `if`, so it runs only when the name is new.",
                        typed="Ask `spell_book` itself whether the name is in it: your `if` checks names you typed.",
                        no_if="Ask the book first: put the store line under `if spell_name not in spell_book:`, "
                              "indented. No `if` asks the book yet.",
                        fix="Store the spell only when its name is not in `spell_book` yet: "
                            "`if spell_name not in spell_book:`.",
                        store_new="Store it when the name is new: the store line goes under the `if`, so a new name "
                                  "gets its page.",
                    ),
                ),
            ],
            pass_line="Oogrish: A new page, and the old one kept. Steady, now.",
        ),
    ],
    solution=_ward(),
    partials=[_ward(store=""), _ward(store=WARD_STORE_PLAIN)],
    assemble=dict(
        lines=[line for line in _ward().splitlines() if line.strip()],
        distractors=['spell_book["spell_name"] = spell', '    "mana_cost": 6,', "if spell_name in spell_book:"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A book of pages",
            text=(
                "```text\nspell_book\n  \"Glow\"         -> {cost 2,\n                     need 3}\n"
                "  \"Lantern Ward\" -> {cost 6,\n                     need 9}\n```\n"
                "`spell_name` holds the page's title. `spell` holds the page."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `spell_name` holds `\"Lantern Ward\"`.\n"
                "2. `spell_book[spell_name]`: Python looks inside the box and finds `\"Lantern Ward\"`.\n"
                "3. `= spell` stores the whole spell sheet on that page.\n"
                "4. Glow's page is still there.\n"
                "5. `if spell_name not in spell_book:` asks first, so a name that already has a page keeps it."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "In `add_spell()`, you replaced each placeholder in the `spell` dictionary, then wrote "
                "`spell_book[spell_name] = spell`. That is this exercise. The campaign's names were the recipe's "
                "ingredients; here they are plain variables."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "My spell book has a tab for each spell, with its name in ink. Behind each tab: the cost and what it "
                "needs. A new spell gets a new tab. The old tabs stay."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky wants proof. After storing the spell, print whether `\"Lantern Ward\"` is in `spell_book`.",
        hints=[
            "`in` asks a dictionary about its keys, and shows `True` or `False`.",
            "Write `print(\"Lantern Ward\" in spell_book)` at the bottom.",
        ],
        checks=[
            (
                "True is printed from an in test",
                dx() + fill(
                    _IN_THE_BOOK,
                    use_in="Ask with `in`: `print(\"Lantern Ward\" in spell_book)` shows `True` or `False`.",
                    other="Ask about the new page, `\"Lantern Ward\" in spell_book`: it is the page your store "
                          "added, so its answer proves the store worked.",
                    not_in="Ask whether it *is* in the book: `in`, not `not in`.",
                    after="Ask after the store: put the `print` below `spell_book[spell_name] = spell`, so the page "
                          "is there to find.",
                ),
            ),
        ],
        solution=_ward() + 'print("Lantern Ward" in spell_book)\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="spell_book[spell_name] = spell",
        why=(
            "You have seen this exact line in `add_spell()`. You replaced each placeholder in `spell`, then stored "
            "it with `spell_name` as the key. Now you know why that key has no quotes."
        ),
    ),
    takeaway="Build the spell from variables, then store it by name: `spell_book[spell_name] = spell`.",
    wrong_answers=[
        dict(why="the starter (0 placeholders)", code=WARD_STARTER, fails_at=1, message_contains="starter's 0"),
        dict(why="numbers typed in the blanks (CMB; the campaign's replace-each-placeholder step, A-08 25 * 2)",
             code=_ward(spell=_ward_spell("6", "9")), fails_at=1, message_contains="not typed numbers"),
        dict(why="swapped (SWAP)", code=_ward(spell=_ward_spell("needed", "cost")), fails_at=1,
             message_contains="swapped"),
        dict(why="the variable names in quotes", code=_ward(spell=_ward_spell('"cost"', '"needed"')), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="a key renamed with a capital (KEY)",
             code=_ward(spell='spell = {\n    "Mana_Cost": cost,\n    "required_affinity": needed,\n}\n'), fails_at=1,
             message_contains='"mana_cost"`, letter for letter'),
        dict(why="a key without quotes (a box name, not text: NameError)",
             code=_ward(spell="spell = {\n    mana_cost: cost,\n    required_affinity: needed,\n}\n"), fails_at=0,
             message_contains="name 'mana_cost' is not defined"),
        dict(why="= in place of : inside the dictionary",
             code=_ward(spell='spell = {\n    "mana_cost" = cost,\n    "required_affinity": needed,\n}\n'), fails_at=0,
             message_contains="cannot assign to literal"),
        dict(why="= in place of : on the second key (there 3.13 says ':' expected)",
             code=_ward(spell='spell = {\n    "mana_cost": cost,\n    "required_affinity" = needed,\n}\n'), fails_at=0,
             message_contains="':' expected after dictionary key"),
        dict(why="a missing comma after a value (reported on the next line)",
             code=_ward(spell='spell = {\n    "mana_cost": cost\n    "required_affinity": needed,\n}\n'), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="CP2 the variable key in quotes: spell_book[\"spell_name\"] (KEY)",
             code=_ward(store='spell_book["spell_name"] = spell\n'), fails_at=2, message_contains='"spell_name"'),
        dict(why="CP2 the name typed as the key (CMB)", code=_ward(store='spell_book["Lantern Ward"] = spell\n'),
             fails_at=2, message_contains="new name gets a new page"),
        dict(why="CP2 a new book: Glow is lost", code=_ward(store="spell_book = {spell_name: spell}\n"), fails_at=2,
             message_contains="Keep Glow"),
        dict(why="CP2 the word spell in quotes", code=_ward(store='spell_book[spell_name] = "spell"\n'), fails_at=2,
             message_contains="just the word"),
        dict(why="CP2 a typed copy of the spell (CMB)",
             code=_ward(store='spell_book[spell_name] = {"mana_cost": 6, "required_affinity": 9}\n'), fails_at=2,
             message_contains="not a typed copy"),
        dict(why="CP2 key and value swapped: spell_book[spell] = spell_name (a sheet can't be a key)",
             code=_ward(store="spell_book[spell] = spell_name\n"), fails_at=0,
             message_contains="unhashable type: 'dict'"),
        dict(why="CP2 the Example's names copied (pantry's food and amount)",
             code=_ward(store="spell_book[food] = amount\n"), fails_at=0,
             message_contains="name 'amount' is not defined"),
        dict(why="CP2 dot access", code=_ward(store="spell_book.spell_name = spell\n"), fails_at=0,
             message_contains="has no attribute 'spell_name'"),
        dict(why="CP2 round brackets", code=_ward(store="spell_book(spell_name) = spell\n"), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="CP2 `in` for `not in` (the guard never lets a new name in)",
             code=_ward(store="if spell_name in spell_book:\n    spell_book[spell_name] = spell\n"), fails_at=2,
             message_contains="already in `spell_book`"),
        dict(why="CP3 the store with no guard (a page that is there is written over)",
             code=_ward(store=WARD_STORE_PLAIN), fails_at=3, message_contains="No `if` asks the book yet"),
        dict(why="CP3 the store line not indented under the if (it runs every time)",
             code=_ward(store='if spell_name not in spell_book:\n    print("A new page.")\n'
                              'spell_book[spell_name] = spell\n'),
             fails_at=3, message_contains="Indent the store line"),
        dict(why="CP3 the guard asks about the quoted name, \"spell_name\" (always not in)",
             code=_ward(store='if "spell_name" not in spell_book:\n    spell_book[spell_name] = spell\n'), fails_at=3,
             message_contains="just those letters"),
        dict(why="CP3 a typed name in the if (!= the one page it has seen; the unnamed page catches it)",
             code=_ward(store='if spell_name != "Glow":\n    spell_book[spell_name] = spell\n'), fails_at=3,
             message_contains="names you typed"),
        dict(why="CP3 the guard asks a typed list, not the book",
             code=_ward(store='if spell_name not in ["Glow"]:\n    spell_book[spell_name] = spell\n'), fails_at=3,
             message_contains="list of names you typed"),
        dict(why="CP3 the guard asks about a value (`in` checks keys, not values)",
             code=_ward(store="if cost not in spell_book:\n    spell_book[spell_name] = spell\n"), fails_at=3,
             message_contains="never the values"),
        dict(why="CP3 the guard asks about the spell itself (a dict value: unhashable)",
             code=_ward(store="if spell not in spell_book:\n    spell_book[spell_name] = spell\n"), fails_at=0,
             message_contains="unhashable type: 'dict'"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-make,dict-write,dict-key-from-variable,dict-in", solo="false",
             dictates="1,3", foreign_names="pantry,bread,food,amount,apples,book,pack,map", stages="P,I,M",
             point_at_it="Which variable holds the spell's name?") + "\n"
        "C2: the variables' names differ from the keys on purpose (`cost` for `\"mana_cost\"`, `needed` for "
        "`\"required_affinity\"`); 'matching' waits for 6B-03, so the starter comment says 'the variable that "
        "holds that value'. CP1 CMB reruns with cost 5 and needed 7; SWAP names `needed`. CP2: KEY "
        "(`\"spell_name\"`), Glow kept, then CMB with spell_name Frost Veil (and cost 5, needed 7), so a typed "
        "`\"Lantern Ward\"` key or a typed copy of the spell fails. CP2 is goal-only (teacher's ruling). CP3 "
        "(dictated, added by the teacher's ruling so Quick Check C3's guard-then-store is practised first) puts the store "
        "under `if spell_name not in spell_book:`, u05c's guard check ported: the program reruns with "
        "`spell_name = \"Glow\"` and other numbers (Glow's page must stay 2 and 3), with a new name (Moon Step, "
        "stored), and with a page no message names (Ash Ward), so a typed `!= \"Glow\"` or a typed list fails. "
        "Diagnoses: no `if`, the store line unindented under the `if`, `\"spell_name\"` in quotes, a value "
        "(`cost`) asked, a typed list or name; `in` for `not in` already fails CP2 ('already in'). The side "
        "quest's `in` check skips the store's own guard. The predict uses `book` so its print line fits "
        "a phone (spell_book's would be 38 characters). Side quest (BQ, combining store + in): `\"Lantern Ward\" in "
        "spell_book` prints True. Its `in` test must ask about `\"Lantern Ward\"` or `spell_name` (anywhere, so "
        "`found = ...` then `print(found)` passes): `\"Glow\" in spell_book` was always True and gets 'ask about "
        "the new page'; the right test before the store gets 'ask after the store'."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4B-05 can-they-cast (A-stage: Assemble-first under Show me more)
# ---------------------------------------------------------------------------------------------

CAST_SETUP = (
    "caster = {\n"
    '    "name": "Bomb Shell",\n'
    '    "mana": 24,\n'
    '    "abilities": {\n'
    '        "magical_affinity": 12,\n'
    "    },\n"
    "}\n"
    "spell_book = {\n"
    '    "Lantern Ward": {\n'
    '        "mana_cost": 6,\n'
    '        "required_affinity": 9,\n'
    "    },\n"
    "}\n"
)
CAST_HEAD = (
    "# The game hands you caster, as\n"
    "# in the campaign. Try\n"
    "# print(caster) to see it.\n"
    'spell = spell_book["Lantern Ward"]\n'
    "\n"
    "# Get it, compare, act.\n"
    "# Replace each False with a test:\n"
    "# 1. Is the caster's affinity too\n"
    "#    low for this spell?\n"
    "# 2. Too little mana for it?\n"
)
AFF_TEST = 'caster["abilities"]["magical_affinity"] < spell["required_affinity"]'
MANA_TEST = 'caster["mana"] < spell["mana_cost"]'
SPEND = '    caster["mana"] = caster["mana"] - spell["mana_cost"]\n'


def _cast(first="False", second="False", spend=SPEND, comment=True, head=CAST_HEAD):
    return (
        head
        + f"if {first}:\n"
        + '    print("Not skilled enough.")\n'
        + f"elif {second}:\n"
        + '    print("Needs more mana.")\n'
        + "else:\n"
        + ("    # 3. Subtract the cost first.\n" if comment else "")
        + spend
        + '    print(caster["mana"])\n'
    )


CAST_STARTER = _cast(spend="")
CAST_SOLUTION = _cast(AFF_TEST, MANA_TEST)

DOOR_EXAMPLE = (
    'door = {"lock": {"level": 3}}\n'
    "skill = 2\n"
    'if skill < door["lock"]["level"]:\n'
    '    print("Too hard.")\n'
    "else:\n"
    '    print("It opens.")\n'
)

_CAST = r'''
# Diagnose the test this step replaces (1: the `if`, 2: the `elif`) before any case message.
_dg = ''
_top = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'If']
_t = None
if _top and __WHICH__ == 1:
    _t = _top[0].test
elif _top and __WHICH__ == 2 and len(_top[0].orelse) == 1 and type(_top[0].orelse[0]).__name__ == 'If':
    _t = _top[0].orelse[0].test
if _t is not None:
    _names = [_x.id for _x in _ast.walk(_t) if type(_x).__name__ == 'Name']
    if type(_t).__name__ == 'Constant' and type(_t.value).__name__ == 'bool' and not _t.value:
        _dg = __STILL_FALSE__
    elif type(_t).__name__ == 'Compare' and not _names:
        _dg = __TYPED_TEST__
    elif type(_t).__name__ == 'Compare' and len(_t.ops) == 1:
        _ln = [_x.id for _x in _ast.walk(_t.left) if type(_x).__name__ == 'Name']
        _rn = [_x.id for _x in _ast.walk(_t.comparators[0]) if type(_x).__name__ == 'Name']
        _op = type(_t.ops[0]).__name__
        _sp = [_x for _x in _ln + _rn if _x in ('spell', 'spell_book')]
        if _sp and (('caster' in _ln and _op in ('Gt', 'GtE')) or ('caster' in _rn and _op in ('Lt', 'LtE'))):
            _dg = 'Check the sign: `<` asks *lower than*.'
for _aff, _mana, _cost, _need, _want, _msg in __CASES__:
    _ch = [('caster', 'caster["abilities"]["magical_affinity"] = ' + str(_aff) + '\ncaster["mana"] = ' + str(_mana)),
           ('spell_book', 'spell_book["Lantern Ward"]["mana_cost"] = ' + str(_cost)
            + '\nspell_book["Lantern Ward"]["required_affinity"] = ' + str(_need))]
    _tried = ('affinity ' + str(_aff) + ' and mana ' + str(_mana) + ' against a spell needing ' + str(_need)
              + ' and costing ' + str(_cost))
    _ns, _ls, _err, _miss = _rerun(_ch)
    assert not _miss, ('Keep `spell = spell_book["Lantern Ward"]` and use `caster` as the game hands it to you, so '
                       'Mar' + chr(39) + 'tu' + chr(39) + 's check can try other casters.')
    assert not _err, _stop(_err, _tried)
    _sk = [_l for _l in _ls
           if 'skilled' in _l.lower() and _re.search(r"\bnot\b|n't|\bno\b|\bun|lack|never", _l.lower())]
    _nm = [_l for _l in _ls if 'more mana' in _l.lower()]
    _left = _get(_ns.get('caster'), 'mana')
    if _want == 'skilled':
        assert _sk, (_dg or _msg) + ' ' + _did(_tried)
        assert not _nm, __ONE_LINE__ + ' ' + _did(_tried)
        assert _left == _mana, __NO_CAST__ + ' ' + _did(_tried)
    elif _want == 'needs':
        assert not _sk, __CAST_AFF__ + ' ' + _did(_tried)
        assert _nm, (_dg or _msg) + ' ' + _did(_tried)
        assert _left == _mana, __NO_CAST__ + ' ' + _did(_tried)
    elif _want == 'not-skilled':
        assert not _sk, (_dg or _msg) + ' ' + _did(_tried)
    elif _want == 'not-needs':
        assert not _nm, (_dg or _msg) + ' ' + _did(_tried)
    else:
        assert not _sk, (_msg if _aff == _need else __CAST_AFF__) + ' ' + _did(_tried)
        assert not _nm, (_msg if _mana == _cost else __CAST_MANA__) + ' ' + _did(_tried)
        _end = ': the mana ended at ' + _lit(_left) + ', not ' + str(_mana - _cost)
        if _left == _mana:
            assert not _shows(_ls, _mana - _cost), __STORE_BACK__ + ' ' + _did(_tried)
            assert False, __SUBTRACT__ + ' ' + _did(_tried, _end)
        _plain = _aff != _need and _mana != _cost
        assert _left == _mana - _cost, (_msg if _plain else __SUBTRACT__) + ' ' + _did(_tried, _end)
        assert _shows(_ls, _mana - _cost), __PRINT_AFTER__ + ' ' + _did(_tried)
'''

CAST_MSGS = dict(
    one_line="Keep the `elif`: only one message should print. When the affinity is too low, Python skips the rest.",
    no_cast="When the caster can't cast, nothing is spent. Keep one chain, `if`, `elif`, `else`, so only one "
            "branch runs.",
    cast_aff="This caster is skilled enough, so the first test should be false. Check its sign.",
    cast_mana="This caster has enough mana, so the second test should be false. Check its sign.",
    store_back="Store it back in the sheet, `caster[\"mana\"] = ...`, so the sheet remembers the cast.",
    subtract="In the `else`, subtract the cost from the sheet: take `spell[\"mana_cost\"]` from `caster[\"mana\"]`.",
    print_after="Subtract first, then print `caster[\"mana\"]`, so the line shows the mana left.",
)


CAST_DIAG = {
    1: dict(
        still_false="Replace the first `False` with a test that reads the sheets: is the caster's affinity lower "
                    "than `spell[\"required_affinity\"]`? The affinity lives inside `\"abilities\"`.",
        typed_test="Your test compares typed numbers, so every caster gets the same answer. Read both sides from "
                   "the sheets: `" + 'caster["abilities"]["magical_affinity"] < spell["required_affinity"]' + "`.",
    ),
    2: dict(
        still_false="Replace the second `False` with a test: is `caster[\"mana\"]` lower than "
                    "`spell[\"mana_cost\"]`?",
        typed_test="Your test compares typed numbers, so every caster gets the same answer. Read both sides from "
                   "the sheets: `" + 'caster["mana"] < spell["mana_cost"]' + "`.",
    ),
    0: dict(still_false="", typed_test=""),
}


def cast_cases(label, cases, which=0):
    """BND reruns. `which` is the test this step replaces (1 the `if`, 2 the `elif`, 0 none): a test still `False`,
    one that compares typed numbers, or one whose sign is backwards is named before the case's own message."""
    return (label, dx(CAST_SETUP) + fill(_CAST, cases=cases, which=which, **CAST_DIAG[which], **CAST_MSGS))


CP1_CASES = [
    (8, 24, 6, 9, "skilled", "Turn away a caster whose affinity is lower than `spell[\"required_affinity\"]`: this "
                             "one's is, and your first test let them through. The affinity lives inside "
                             "`\"abilities\"`."),
    (12, 24, 6, 14, "skilled", "Compare with `spell[\"required_affinity\"]`, not a typed 9, so a harder spell is "
                               "caught too."),
    (3, 2, 6, 9, "skilled", "Test the affinity in the first `if`. This caster is short of both, and the affinity "
                            "comes first."),
    (12, 24, 6, 9, "not-skilled", "Check the sign in the first test: 12 is not lower than 9, so this caster is "
                                  "skilled enough."),
    (9, 24, 6, 9, "not-skilled", "Exactly enough affinity still casts: 9 is not lower than 9. Use `<` in the "
                                 "affinity test, not `<=`."),
]
CP2_CASES = [
    (12, 5, 6, 9, "needs", "Tell a caster with too little mana: this one has less than `spell[\"mana_cost\"]`, and "
                           "your second test let them through. Compare `caster[\"mana\"]` with the cost."),
    (12, 9, 11, 9, "needs", "Compare with `spell[\"mana_cost\"]`, not a typed 6, so a spell that costs more is "
                            "caught too."),
    (12, 24, 6, 9, "not-needs", "Check the sign in the mana test: 24 mana is not lower than a cost of 6."),
    (3, 2, 6, 9, "skilled", "Keep the chain in order: the affinity test first, then the mana test in the `elif`."),
    (12, 6, 6, 9, "not-needs", "Exactly enough mana still casts: 6 mana pays for a 6-mana spell. Use `<` in the "
                               "mana test, not `<=`."),
]
# The edges (exactly enough affinity, exactly enough mana) sit in the step whose own test they check (CP1, CP2), so
# `<=` in either test stops on that step, and Help aims at the step whose Teach rung says `<`, not `<=`.
CP3_CASES = [
    (12, 24, 6, 9, "cast", "Take `spell[\"mana_cost\"]` from the old `caster[\"mana\"]`."),
    (12, 20, 6, 9, "cast", "Take `spell[\"mana_cost\"]` from the old `caster[\"mana\"]`."),
    (12, 10, 4, 9, "cast", "Subtract `spell[\"mana_cost\"]`, not a typed 6, so a cheaper spell costs less."),
]

_HOW_SHORT = r'''
for _mana, _gap in ((3, 3), (1, 5)):
    _tried = 'mana ' + str(_mana) + ' against a spell costing 6'
    _ns, _ls, _err, _miss = _rerun([('caster', 'caster["mana"] = ' + str(_mana))])
    assert not _err, _stop(_err, _tried)
    assert [_l for _l in _ls if 'more mana' in _l.lower() and _re.search(_whole(_gap), _l)], (
        __FIX__ + ' ' + _did(_tried, ': that is ' + str(_gap) + ' short'))
'''

CAN_THEY_CAST = dict(
    id="can-they-cast",
    title="Can they cast?",
    martu=(
        "Holding the barrier was three moves: get it, compare, act.\n"
        "*Get it:* read the value out of the sheet, through every key on the way. *Compare:* is it lower than "
        "what the spell needs? *Act:* print a warning, or cast.\n"
        "The game hands you `caster`, as it did in the campaign:\n"
        "```text\ncaster (from the game)\n  \"name\"      -> \"Bomb Shell\"\n  \"mana\"      -> 24\n"
        "  \"abilities\" ->\n    \"magical_affinity\" -> 12\n```\n"
        "One rule from the campaign: exactly enough still casts."
    ),
    example=DOOR_EXAMPLE,
    example_output="Too hard.",
    setup=CAST_SETUP,
    names=["caster", "spell"],
    pair_talk=(
        "Read each test aloud to your partner in plain English: 'if the caster's affinity is lower than what the "
        "spell needs...'. Then each of you writes it on your own screen."
    ),
    starter=CAST_STARTER,
    checkpoints=[
        dict(
            id="not-skilled-enough",
            text=(
                "Replace the first `False`: when the caster's affinity is lower than `spell[\"required_affinity\"]`, "
                "the chain prints `Not skilled enough.`"
            ),
            dictated=False,
            hints=[
                "Run `print(caster)` first. The affinity is `\"magical_affinity\"`, inside `\"abilities\"`.",
                "Read inside, then compare: `skill < door[\"lock\"][\"level\"]` in the Example asks whether the "
                "skill is too low. `<` asks *lower than*. Exactly enough is not lower, so it still casts. Use `<`, "
                "not `<=`.",
                "Write `if " + AFF_TEST + ":` in place of `if False:`.",
            ],
            checks=[cast_cases("a caster with too little affinity is turned away", CP1_CASES, which=1)],
        ),
        dict(
            id="needs-more-mana",
            text="Replace the second `False`: when `caster[\"mana\"]` is lower than the spell's cost, it prints "
                 "`Needs more mana.` Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "The mana is on the big sheet, `caster[\"mana\"]`. The cost is on the spell's page, "
                "`spell[\"mana_cost\"]`.",
                "`elif` only asks when the `if` above was false: a caster who is not skilled never gets here. `<` "
                "asks *lower than*: exactly enough mana is not lower, so it still casts. Use `<`, not `<=`.",
                "Write `elif " + MANA_TEST + ":` in place of `elif False:`.",
            ],
            checks=[cast_cases("a caster with too little mana is told", CP2_CASES, which=2)],
        ),
        dict(
            id="cast-it",
            text="In the `else`, subtract the spell's cost from `caster[\"mana\"]` before the print.",
            dictated=False,
            hints=[
                "Read the old mana, take away `spell[\"mana_cost\"]`, and store it back in the sheet, above "
                "`print(caster[\"mana\"])`.",
                "Change a value by its key: `hero[\"mana\"] = hero[\"mana\"] - cost` reads the old mana on the right "
                "and stores the new one on the left.",
                "Write `" + SPEND.strip() + "` in the `else`, above `print(caster[\"mana\"])`.",
            ],
            checks=[cast_cases("the cast spends the mana", CP3_CASES)],
            pass_line="Gearshift: Barrier's holding. Visor dims.",
        ),
    ],
    solution=CAST_SOLUTION,
    partials=[_cast(AFF_TEST, spend=""), _cast(AFF_TEST, MANA_TEST, spend="")],
    assemble=dict(
        lines=[
            'spell = spell_book["Lantern Ward"]',
            "if " + AFF_TEST + ":",
            '    print("Not skilled enough.")',
            "elif " + MANA_TEST + ":",
            '    print("Needs more mana.")',
            "else:",
            SPEND.rstrip("\n"),
            '    print(caster["mana"])',
        ],
        distractors=[
            'if caster["abilities"]["magical_affinity"] <= spell["required_affinity"]:',
            'if caster["magical_affinity"] < spell["required_affinity"]:',
        ],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Get it, compare, act",
            text=(
                "1. Get it: `caster[\"abilities\"][\"magical_affinity\"]` is 12. `spell[\"required_affinity\"]` is 9.\n"
                "2. Compare: is 12 lower than 9? No. Skip that branch.\n"
                "3. Get it: `caster[\"mana\"]` is 24. `spell[\"mana_cost\"]` is 6. Is 24 lower than 6? No.\n"
                "4. Act: the `else`. 24 - 6 is 18. Print 18."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "The `hold-the-barrier` comments said: if the affinity is lower than the spell's required affinity, "
                "say they aren't skilled enough. Otherwise, if the mana is lower than the cost, say so. Otherwise, "
                "cast and subtract. This is that chain, with `print` for `print_prompt`."
            ),
        ),
        dict(
            angle="picture",
            label="Three doors",
            text=(
                "```text\naffinity too low? -yes-> Not skilled\n      | no\nmana too low? ---yes---> Needs mana\n"
                "      | no\nelse: spend, print the mana\n```\n"
                "Python takes the first door that opens, and only that one."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants details. In the mana branch, say how much mana is missing, like `Needs 3 more mana.` Work "
            "it out from the sheet and the spell."
        ),
        hints=[
            "Missing mana is the cost take away the mana the caster has. Glue a number into text with `str()`.",
            "`\"Short by \" + str(need - have)` works out the gap, then glues it into the text.",
            "Write `print(\"Needs \" + str(spell[\"mana_cost\"] - caster[\"mana\"]) + \" more mana.\")` in the "
            "`elif`.",
        ],
        checks=[
            (
                "the missing mana is said",
                dx(CAST_SETUP) + fill(_HOW_SHORT, fix="Say how much is missing: the cost take away the caster's "
                                                      "mana, glued in with `str()`."),
            ),
        ],
        solution=CAST_SOLUTION.replace(
            '    print("Needs more mana.")\n',
            '    print("Needs " + str(spell["mana_cost"] - caster["mana"]) + " more mana.")\n',
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "You have seen this chain: it is the body of `cast_spell` in `hold-the-barrier`. Get the affinity, "
            "compare, act; then the mana. Now you can read every key on the way."
        ),
    ),
    takeaway="Get it, compare, act: read through the keys, compare with `<`, then print or cast in an `else`.",
    wrong_answers=[
        dict(why="the starter (both tests still False)", code=CAST_STARTER, fails_at=1,
             message_contains="Replace the first `False`"),
        dict(why="a skipped level: caster[\"magical_affinity\"] (KeyError)",
             code=_cast('caster["magical_affinity"] < spell["required_affinity"]', MANA_TEST), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="<= in the affinity test (exactly enough affinity turned away: step 1 stops on it)",
             code=_cast(AFF_TEST.replace(" < ", " <= "), MANA_TEST), fails_at=1,
             message_contains="Exactly enough affinity still casts"),
        dict(why="<= in the mana test (exactly enough mana turned away: step 2 stops on it)",
             code=_cast(AFF_TEST, MANA_TEST.replace(" < ", " <= ")), fails_at=2,
             message_contains="Exactly enough mana still casts"),
        dict(why="dot access in the mana test: caster.mana (AttributeError)",
             code=_cast(AFF_TEST, 'caster.mana < spell["mana_cost"]'), fails_at=0,
             message_contains="has no attribute 'mana'"),
        dict(why="dot access on the spell: spell.mana_cost (AttributeError)",
             code=_cast(AFF_TEST, 'caster["mana"] < spell.mana_cost'), fails_at=0,
             message_contains="has no attribute 'mana_cost'"),
        dict(why="the cost read from the caster's sheet: caster[\"mana_cost\"] (KeyError)",
             code=_cast(AFF_TEST, 'caster["mana"] < caster["mana_cost"]'), fails_at=0,
             message_contains="KeyError: 'mana_cost'"),
        dict(why="the whole caster compared: caster < spell[\"mana_cost\"] (TypeError)",
             code=_cast(AFF_TEST, 'caster < spell["mana_cost"]'), fails_at=0,
             message_contains="not supported between instances of 'dict' and 'int'"),
        dict(why="the numbers from the sheets typed into both tests (12 < 9, 24 < 6)",
             code=_cast("12 < 9", "24 < 6"), fails_at=1, message_contains="compares typed numbers"),
        dict(why="typed numbers in the first test only: if 12 < 9 (every caster gets the same answer)",
             code=_cast("12 < 9", MANA_TEST), fails_at=1, message_contains="compares typed numbers"),
        dict(why="typed numbers in the mana test: elif 24 < 6",
             code=_cast(AFF_TEST, "24 < 6"), fails_at=2, message_contains="compares typed numbers"),
        dict(why="the first False left, the mana test written (CP1 still names the False)",
             code=_cast("False", MANA_TEST), fails_at=1, message_contains="Replace the first `False`"),
        dict(why="the second False left (CP2 names it)",
             code=_cast(AFF_TEST, "False"), fails_at=2, message_contains="Replace the second `False`"),
        dict(why="the sign backwards in the mana test (>)",
             code=_cast(AFF_TEST, MANA_TEST.replace(" < ", " > ")), fails_at=2, message_contains="Check the sign"),
        dict(why="the sides swapped with < (spell's need lower than the affinity: backwards)",
             code=_cast('spell["required_affinity"] < caster["abilities"]["magical_affinity"]', MANA_TEST),
             fails_at=1, message_contains="Check the sign"),
        dict(why="a typed 9 for the needed affinity",
             code=_cast('caster["abilities"]["magical_affinity"] < 9', MANA_TEST), fails_at=1,
             message_contains="not a typed 9"),
        dict(why="the sign backwards in the first test (>)",
             code=_cast(AFF_TEST.replace(" < ", " > "), MANA_TEST), fails_at=1, message_contains="Check the sign"),
        dict(why="a typed 6 for the cost in the mana test",
             code=_cast(AFF_TEST, 'caster["mana"] < 6'), fails_at=2, message_contains="not a typed 6"),
        dict(why="a typed 6 subtracted (CMB)",
             code=_cast(AFF_TEST, MANA_TEST, spend='    caster["mana"] = caster["mana"] - 6\n'), fails_at=3,
             message_contains="not a typed 6"),
        dict(why="the mana typed: caster[\"mana\"] = 18",
             code=_cast(AFF_TEST, MANA_TEST, spend='    caster["mana"] = 18\n'), fails_at=3,
             message_contains="Take `spell[\"mana_cost\"]`"),
        dict(why="worked out into a new box, never stored back",
             code=_cast(AFF_TEST, MANA_TEST, spend='    caster["mana"] - spell["mana_cost"]\n'), fails_at=3,
             message_contains="subtract the cost"),
        dict(why="subtracted after the print (the print shows the old mana)",
             code=_cast(AFF_TEST, MANA_TEST, spend="").replace(
                 '    print(caster["mana"])\n', '    print(caster["mana"])\n' + SPEND), fails_at=3,
             message_contains="Subtract first"),
        dict(why="two ifs instead of if / elif (the second if's else casts after the warning)",
             code=_cast(AFF_TEST, MANA_TEST).replace("elif " + MANA_TEST, "if " + MANA_TEST), fails_at=1,
             message_contains="Keep one chain"),
        dict(why="the tests in the wrong order (mana first, then affinity)",
             code=_cast(MANA_TEST, AFF_TEST).replace('"Not skilled enough."', '"X"').replace(
                 '"Needs more mana."', '"Not skilled enough."').replace('"X"', '"Needs more mana."'), fails_at=1,
             message_contains="affinity comes first"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="dict-nested,boundary,elif-chain", solo="false", dictates="",
             foreign_names="door,lock,level,skill,hero,cost,need,have", stages="A,M",
             assemble_first="Show me more") + "\n"
        "Given `caster` and `spell = spell_book[\"Lantern Ward\"]`: caster and the book live in setup, like the "
        "game handing `caster` to `cast_spell` (prebuilt data, rule 3; no methods are taught on them), so the "
        "Assemble view is the eight lines of the chain, not thirteen brace lines. The starter's skeleton keeps "
        "`False` placeholders (not `___`), so each step runs on its own and the partials hold. Subgoal labels "
        "(Get it, Compare, Act) are in the Learn text and the starter's comments; the starter's numbered comments use "
        "plain words, not keys (the CP texts keep the spell's keys), and the Learn pane pictures what the game "
        "hands over. Before any case message, CP1 and CP2 diagnose the test they replace: still `False` ('Replace "
        "the first `False`', only then), typed numbers only (`if 12 < 9:`: every caster gets the same answer), or "
        "a sign backwards (`>` with the caster on the left, `<` with it on the right). BND: four caster setups per "
        "step, rerun inside the check with affinity, mana, cost and needed all changed (typed 9 and 6 fail; "
        "exactly enough affinity and exactly enough mana must cast). Lines are matched by words ('skilled' with a "
        "no-word such as not, n't or un-, and 'more mana'), so an `else` line that cheers 'skilled enough!' still "
        "casts, and Lucky's side quest (BQ, G4 R16: 'Needs 3 more mana.', checked at mana 3 and 1) keeps CP2 "
        "green. PA distractors: `<=` and the flat key. PR: the navigator's plain-English read is the pair talk."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4B-06 broken-spell-4b (three slips, in the order Python reports them)
# ---------------------------------------------------------------------------------------------

BROKEN_DATA = (
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "mana": 24,\n'
    '    "abilities": {\n'
    '        "dexterity": 6,\n'
    "    },\n"
    "}\n"
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    "}\n"
    "roster = [bomb_shell, lucky]\n"
    'spell_book = {"Glow": 2}\n'
    "\n"
)
DEX_GOOD = 'print(bomb_shell["abilities"]["dexterity"])\n'
LUCKY_GOOD = 'print(roster[1]["mana"])\n'
GLOW_GOOD = 'print(spell_book["Glow"])\n'


def _broken(dex='print(bomb_shell["dexterity"])\n', mana='print(roster["Lucky"]["mana"])\n',
            glow="print(spell_book[Glow])\n", data=BROKEN_DATA):
    return data + dex + mana + glow


BROKEN_STARTER = _broken()
_NO_GLOW_BOX = r'''
_made = [_t.id for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ in ('Assign', 'AugAssign')
         for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
         if type(_t).__name__ == 'Name' and _t.id == 'Glow']
assert not _made, __FIX__
'''
BROKEN_SOLUTION = _broken(DEX_GOOD, LUCKY_GOOD, GLOW_GOOD)

BROKEN_SPELL_4B = dict(
    id="broken-spell-4b",
    title="Broken spell",
    martu=(
        "Three slips, one per line, and Python reports them one at a time. Read the last line of each message "
        "first.\n"
        "A KeyError names the key it could not find. A TypeError about list indices means a list was asked for a "
        "name. A NameError means a word with no quotes.\n"
        "Mend one, run again, and Python shows you the next. Normal, yes?"
    ),
    names=["bomb_shell", "roster", "spell_book"],
    pair_talk="Compare which key or name each message points at, and why. Each of you mends your own screen.",
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="dexterity-inside",
            text="Mend the line that prints Bomb Shell's dexterity.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which key could it not find?",
                "Look at the sheet. Is `\"dexterity\"` on the big sheet, or inside another card?",
                "Write `print(bomb_shell[\"abilities\"][\"dexterity\"])` in place of `print(bomb_shell[\"dexterity\"])`.",
            ],
            checks=[
                read_check(
                    "Bomb Shell's dexterity is printed", 6,
                    "Print Bomb Shell's dexterity: `[\"abilities\"]`, then `[\"dexterity\"]`.",
                    pre=flat_check("bomb_shell", "dexterity", "Mend the line, not the sheet: dexterity lives "
                                                               "inside `\"abilities\"`, so read through it."),
                    inside="dexterity",
                    whole="Add the inner key, `[\"dexterity\"]`. Your line printed the whole card.",
                ),
                follow_check(
                    "the dexterity follows the sheet",
                    [("bomb_shell", 'bomb_shell["abilities"]["dexterity"] = 9')],
                    '`bomb_shell["abilities"]["dexterity"] = 9`', 9, 6,
                    typed="Read it from the sheet, not a typed 6: outer key, then inner key.",
                    fix="Print the dexterity from the sheet: outer key, then inner key.",
                ),
            ],
        ),
        dict(
            id="lucky-by-position",
            text="Mend the line that prints Lucky's mana through `roster`.",
            dictated=False,
            hints=[
                "Read Python's last line first. A list was given text in its brackets.",
                "A list takes a position, not a name. Which position is Lucky in `roster`?",
                "Write `print(roster[1][\"mana\"])` in place of `print(roster[\"Lucky\"][\"mana\"])`.",
            ],
            checks=[
                read_check(
                    "Lucky's mana is printed", 26,
                    "Print Lucky's mana: his position in `roster`, then the key `\"mana\"`.",
                    inside="Lucky",
                    whole="Add the key, `[\"mana\"]`, after the position. Your line printed a whole sheet.",
                    near=[(24, "Lucky is at position 1. Your line printed 24, Bomb Shell's mana at position 0.")],
                ),
                roster_check(
                    "Lucky's mana is read through roster", 'roster[1]["mana"] = 11',
                    "a roster copy where Lucky's mana is 11", 11, 26,
                    "Read it through `roster`, not from the `lucky` box or a typed 26: Lucky is at position 1, so "
                    "`roster[1][\"mana\"]`.",
                ),
            ],
        ),
        dict(
            id="glow-in-quotes",
            text="Mend the line that prints Glow's cost.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which name does it not know?",
                "`Glow` is the name of a page in the book, not a box. " + QUOTES_RULE,
                "Write `print(spell_book[\"Glow\"])` in place of `print(spell_book[Glow])`.",
            ],
            checks=[
                ("the key gets quotes, not a box", dx() + fill(_NO_GLOW_BOX, fix=(
                    "Put quotes around the key, `spell_book[\"Glow\"]`, and take out the box `Glow`. A new box "
                    "stops the NameError, but Glow is a page's name: text, so it needs quotes. " + QUOTES_RULE))),
                read_check(
                    "Glow's cost is printed", 2,
                    "Print Glow's cost: `spell_book` with the key `\"Glow\"`, in quotes.",
                    inside="Glow",
                    whole="Print one page: `spell_book[\"Glow\"]`, not the whole book.",
                ),
                follow_check(
                    "the cost follows the book", [("spell_book", 'spell_book["Glow"] = 5')],
                    '`spell_book["Glow"] = 5`', 5, 2,
                    typed="Read it from the book, `spell_book[\"Glow\"]`, not a typed 2.",
                    fix="Print Glow's cost from the book: `spell_book[\"Glow\"]`.",
                ),
            ],
            pass_line="Bomb Shell: That latch hates me. These lines don't. Works.",
        ),
    ],
    solution=BROKEN_SOLUTION,
    assemble=dict(
        lines=[line for line in BROKEN_SOLUTION.splitlines() if line.strip()],
        distractors=['print(bomb_shell["dexterity"])', 'print(roster["Lucky"]["mana"])'],
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
            label="What each message means",
            text=(
                "```text\nKeyError: 'dexterity'\n  no key spelled like that\n  here: look one level in\n"
                "TypeError: list indices...\n  a list got a name\n  use a position number\n"
                "NameError: name 'Glow'\n  a word with no quotes\n  add the quotes\n```"
            ),
        ),
        dict(
            angle="shorter",
            text="Inner keys need the outer key first. Lists take numbers. Keys take quotes.",
        ),
    ],
    takeaway="Read the last line: KeyError (the key's spelling or level), TypeError (a list got a name), NameError "
             "(quotes missing).",
    wrong_answers=[
        dict(why="the starter (the skipped level first: KeyError)", code=BROKEN_STARTER, fails_at=0,
             message_contains="KeyError: 'dexterity'"),
        dict(why="one mended, roster[\"Lucky\"] left (the TypeError row)", code=_broken(dex=DEX_GOOD), fails_at=0,
             message_contains="list indices must be integers or slices, not str"),
        dict(why="two mended, spell_book[Glow] left (NameError)", code=_broken(dex=DEX_GOOD, mana=LUCKY_GOOD),
             fails_at=0, message_contains="name 'Glow' is not defined"),
        dict(why="counting from 1: roster[2] (IndexError)",
             code=_broken(dex=DEX_GOOD, mana='print(roster[2]["mana"])\n', glow=GLOW_GOOD), fails_at=0,
             message_contains="list index out of range"),
        dict(why="position 0 (Bomb Shell's 24)",
             code=_broken(dex=DEX_GOOD, mana='print(roster[0]["mana"])\n', glow=GLOW_GOOD), fails_at=2,
             message_contains="position 1"),
        dict(why="a small letter in the key (KeyError)",
             code=_broken(dex=DEX_GOOD, mana=LUCKY_GOOD, glow='print(spell_book["glow"])\n'), fails_at=0,
             message_contains="KeyError: 'glow'"),
        dict(why="the sheet changed instead of the line (dexterity copied to the outside)",
             code=_broken(dex='print(bomb_shell["dexterity"])\n', mana=LUCKY_GOOD, glow=GLOW_GOOD,
                          data=BROKEN_DATA.replace('    "mana": 24,\n', '    "mana": 24,\n    "dexterity": 6,\n', 1)),
             fails_at=1, message_contains="not the sheet"),
        dict(why="the numbers typed (CMB)", code=_broken("print(6)\n", "print(26)\n", "print(2)\n"), fails_at=1,
             message_contains="typed 6"),
        dict(why="Lucky's mana read from his own box (not through roster)",
             code=_broken(DEX_GOOD, 'print(lucky["mana"])\n', GLOW_GOOD), fails_at=2,
             message_contains="through `roster`"),
        dict(why="dot access on the list", code=_broken(DEX_GOOD, "print(roster.lucky.mana)\n", GLOW_GOOD),
             fails_at=0, message_contains="'list' object has no attribute 'lucky'"),
        dict(why="Lucky's box printed, with roster named in the same print (not a read through roster)",
             code=_broken(DEX_GOOD, 'print(lucky["mana"], roster[0]["mana"])\n', GLOW_GOOD), fails_at=2,
             message_contains="not from the `lucky` box"),
        dict(why="Bomb Shell's mana plus 2 (26 worked out by hand, through roster)",
             code=_broken(DEX_GOOD, 'print(roster[0]["mana"] + 2)\n', GLOW_GOOD), fails_at=2,
             message_contains="still printed 26"),
        dict(why="the NameError hidden with a new box, Glow = \"Glow\", instead of quotes on the key",
             code=_broken(DEX_GOOD, LUCKY_GOOD, 'Glow = "Glow"\nprint(spell_book[Glow])\n'), fails_at=3,
             message_contains="take out the box `Glow`"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="dict-nested,list-of-dicts,dict-read,read-traceback",
             solo="false", dictates="", foreign_names="") + "\n"
        "Broken spell, three runtime slips in run order: `bomb_shell[\"dexterity\"]` (KeyError, a skipped level), "
        "`roster[\"Lucky\"]` (TypeError: list indices must be integers or slices, not str) and `spell_book[Glow]` "
        "(NameError: quotes missing). Each slip left fails at 0 with Python's own words (WA). No partials: on the "
        "site a crash fails every checkpoint. Every mend has CMB (the dexterity 9, Lucky's mana 11, Glow's cost "
        "5). Lucky's line must read through `roster`, checked by behavior: a roster of copies with Lucky's mana "
        "at 11, so `hero = roster[1]` then `print(hero[\"mana\"])` passes, while `lucky[\"mana\"]` (even printed "
        "next to a `roster` read) fails. CP3 also refuses a new box `Glow = \"Glow\"`: it hides the NameError "
        "instead of quoting the key. Bomb Shell has mana 24, so `roster[0]` gets its own "
        "message; `roster[2]` (counting from 1) is an IndexError with two sheets. Lucky is position 1 here; "
        "4B-S seat B uses the same TypeError shape (`roster[\"Lucky\"][\"mana\"]`) on another roster."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4B-S solo-4b (SOLO, one bug, done alone)
# ---------------------------------------------------------------------------------------------

SOLO_SHEET = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    '    "abilities": {\n'
    '        "magical_affinity": 13,\n'
    "    },\n"
    "}\n"
)
SOLO_STARTER = SOLO_SHEET + 'print(lucky["magical_affinity"])\n'
SOLO_SOLUTION = SOLO_SHEET + 'print(lucky["abilities"]["magical_affinity"])\n'

SOLO_4B = dict(
    id="solo-4b",
    title="Show Mar'tu",
    martu="A short one, just for you. One slip. Read the message, then mend it.",
    solo=True,
    explainer="lean",
    names=["lucky"],
    starter=SOLO_STARTER,
    checkpoints=[
        dict(
            id="lucky-affinity",
            text="Make it print Lucky's `magical_affinity`.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which key could it not find?",
                "Look at the sheet. Where does `\"magical_affinity\"` live?",
                "A value inside an inner card needs both keys, outer first: `jar[\"lid\"][\"turns\"]`.",
            ],
            checks=[
                read_check(
                    "Lucky's affinity is printed", 13,
                    "Print Lucky's magical affinity: the outer key, then the inner key.",
                    pre=flat_check("lucky", "magical_affinity", "Mend the line, not the sheet: the affinity lives "
                                                                "inside `\"abilities\"`, so read through it."),
                    inside="magical_affinity",
                    whole="Add the inner key after `[\"abilities\"]`. Your line printed the whole card.",
                    near=[(26, "Read the affinity, inside `\"abilities\"`. Your line printed 26, the mana.")],
                ),
                follow_check(
                    "the affinity follows the sheet",
                    [("lucky", 'lucky["abilities"]["magical_affinity"] = 7')],
                    '`lucky["abilities"]["magical_affinity"] = 7`', 7, 13,
                    typed="Read it from the sheet, not a typed 13.",
                    fix="Print the affinity from the sheet: outer key, then inner key.",
                ),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ read a value inside a sheet.",
        ),
    ],
    solution=SOLO_SOLUTION,
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line. 2. Find that key in the sheet. 3. Count the levels."),
        dict(angle="shorter", text="Outer key, then inner key."),
    ],
    takeaway="On your own: read the KeyError, find the key's level, read through every key on the way.",
    wrong_answers=[
        dict(why="the starter (a skipped level: KeyError)", code=SOLO_STARTER, fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the number typed", code=SOLO_SHEET + "print(13)\n", fails_at=1, message_contains="typed 13"),
        dict(why="only the outer key (the whole card)", code=SOLO_SHEET + 'print(lucky["abilities"])\n',
             fails_at=1, message_contains="whole card"),
        dict(why="the sheet flattened instead of the line mended",
             code=SOLO_SHEET.replace('    "mana": 26,\n', '    "mana": 26,\n    "magical_affinity": 13,\n')
             + 'print(lucky["magical_affinity"])\n', fails_at=1, message_contains="not the sheet"),
        dict(why="both keys, inner first (KeyError)", code=SOLO_SHEET + 'print(lucky["magical_affinity"]["abilities"])\n',
             fails_at=0, message_contains="KeyError: 'magical_affinity'"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-nested,read-traceback", solo="true", dictates="",
             foreign_names="jar,lid,turns",
             seat_b="`roster = [lucky]` with `print(roster[\"Lucky\"][\"mana\"])` (TypeError: list indices must be "
                    "integers or slices, not str), mended to `roster[0][\"mana\"]`") + "\n"
        "SOLO, one bug. Seat A (and anyone solo) gets the skipped level, `lucky[\"magical_affinity\"]`; seat B "
        "would get `roster[\"Lucky\"][\"mana\"]` once pair mode ships. Recorded, never blocking, never shown to a "
        "partner. CMB with the affinity at 7. explainer='lean' (teacher's ruling: from Unit 2 on, SOLO items and "
        "Quick Checks): the explainer names the kind of slip and the line, not the fix."
    ),
)

LESSON_4B = dict(
    kind="lesson",
    id="sheets-inside-sheets",
    title="Sheets Inside Sheets",
    minutes=31,
    summary=(
        "Read and change values inside values, read a roster of sheets, store a spell by its name, and rebuild the "
        "campaign's can-they-cast chain."
    ),
    notes=(
        "Lesson 4B (CC; 4B-02 and 4B-06 SC). Preceded by 4b-remembers. Exactly one SOLO (solo-4b, "
        "explainer='lean'). Non-dictated checkpoints: 4B-01, 4B-02, 4B-03 CP1 and CP2, 4B-04 CP2, 4B-05 CP1-3, "
        "4B-06, 4B-S. Dictated: 4B-04 CP1 and CP3. 31 minutes (teacher's ruling, from 30): 4B-04's guard "
        "checkpoint adds about 2, the abilities-inside try-it moved to an optional angle (-0.5), and "
        "change-inside's Example/text mismatch is gone (-0.5). Point-at-it: 4B-04 ('Which variable holds the "
        "spell's name?'). Moment: 4B-01 "
        "boxes in boxes (teacher-led). Rest marker: 4B-04's pass lines come about halfway. 4B-05 is the A-stage "
        "exercise (Assemble-first under Show me more) that rebuilds the body of hold-the-barrier."
    ),
    exercises=[ABILITIES_INSIDE, CHANGE_INSIDE, THE_ROSTER, SPELL_BOOK_OF_SPELLS, CAN_THEY_CAST, BROKEN_SPELL_4B,
               SOLO_4B],
)

# =============================================================================================
# Quiz 4
# =============================================================================================

QUIZ_4 = dict(
    kind="quiz",
    id="dictionaries-quiz",
    title="Dictionaries Quiz",
    minutes=8,
    summary="Eight questions on keys, sheets inside sheets, rosters and spell books. Retake as often as you like.",
    notes=(
        "Quiz 4 (SC), the spec's eight in order: 4 predict, 1 mc, 1 parsons, 1 fill, 1 bug, with the def/return "
        "item (#8) every unit quiz carries from Unit 4 on. Review order: right answers first, then 'worth another "
        "look', then the score. Distractors come from this unit's slips (values tested with `in`, a quoted "
        "variable key, a skipped level, counting from 1)."
    ),
    questions=[
        dict(
            type="predict",
            id="in-looks-at-keys",
            q="What will this print?",
            code=(
                "pack = {\n"
                '    "Glow": 2,\n'
                '    "Spark": 1,\n'
                "}\n"
                'print("glow" in pack)\n'
                "print(2 in pack)\n"
            ),
            choices=["True\nTrue", "True\nFalse", "False\nTrue", "False\nFalse"],
            answer="False\nFalse",
            explain=(
                "`in` looks at the keys only, letter for letter. The key is `\"Glow\"` with a capital G, so "
                "`\"glow\"` is not a key: `False`. 2 is a value, not a key, so `2 in pack` is `False` too."
            ),
            notes=(
                "dict-in (Obj 4), with fresh values (teacher's ruling) so the answer does not come from 4A-06's "
                "predict: 'True, True' is the in-checks-values belief plus 'capitals don't matter'; 'True, False' is "
                "4A-06's answer, remembered; 'False, True' is the in-checks-values belief alone."
            ),
        ),
        dict(
            type="mc",
            id="key-from-a-variable",
            q="`spell_name` holds `\"Glow\"`. Which line prints Glow's cost?",
            code='spell_book = {"Glow": 2}\nspell_name = "Glow"\n',
            choices=['print(spell_book["spell_name"])', "print(spell_book[spell_name])", "print(spell_book.spell_name)"],
            answer=1,
            why_wrong={
                0: "With quotes, Python looks for a key spelled s-p-e-l-l-_-n-a-m-e. The book has no such key, so "
                   "it stops with a KeyError.",
                2: "Dictionaries are read with square brackets, not a dot. Python stops: `'dict' object has no "
                   "attribute 'spell_name'`.",
            },
            explain=(
                "No quotes means look inside the box: `spell_name` holds `\"Glow\"`, so `spell_book[spell_name]` "
                "reads Glow's page, 2."
            ),
            notes="dict-key-from-variable (Obj 5): the quoted variable key and dot access.",
        ),
        dict(
            type="parsons",
            id="build-and-store",
            q=(
                "Put the lines in order (with their indents). Build the spell from `cost` and `needed`, then store "
                "it under `spell_name`."
            ),
            lines=[
                "spell_book = {}",
                'spell_name = "Frost Veil"',
                "cost = 5",
                "needed = 7",
                "spell = {",
                '    "mana_cost": cost,',
                '    "required_affinity": needed,',
                "}",
                "spell_book[spell_name] = spell",
                "print(spell_book[spell_name])",
            ],
            distractors=['spell_book["spell_name"] = spell'],
            expected_output="{'mana_cost': 5, 'required_affinity': 7}",
            explain=(
                "Make the variables first, then the spell that uses them, then store it. `spell_book[spell_name]` "
                "has no quotes, so the page is called Frost Veil. With quotes it would be called spell_name."
            ),
            notes="dict-make + dict-write + dict-key-from-variable (Obj 8). Distractor: the quoted variable key.",
        ),
        dict(
            type="predict",
            id="two-keys-in-a-row",
            q="What will this print?",
            code=(
                "hero = {\n"
                '    "name": "Lucky",\n'
                '    "abilities": {\n'
                '        "dexterity": 15,\n'
                '        "strength": 17,\n'
                "    },\n"
                "}\n"
                'print(hero["abilities"]["strength"])\n'
            ),
            choices=["15", "{'dexterity': 15, 'strength': 17}", "17", "an error"],
            answer="17",
            explain=(
                "Outer key, then inner key. `hero[\"abilities\"]` is Lucky's inner card. `[\"strength\"]` reads one "
                "line of it: 17. One key alone would print the whole card."
            ),
            notes=(
                "dict-nested (Obj 6), with fresh values (teacher's ruling): Lucky's card and the inner key "
                "`\"strength\"`, so the answer does not come from 4B-01's Bomb Shell wisdom (8). The print line is "
                "exactly 36 characters; `[\"dexterity\"]` would be 37, so strength is the inner key asked. 15 is the "
                "neighbour on the card; the whole card is one key alone."
            ),
        ),
        dict(
            type="fill",
            id="spend-by-key",
            q="Fill the blank so the hero pays `cost` from their mana. The program should print 18.",
            code='hero = {"mana": 24}\ncost = 6\nhero["mana"] = hero["mana"] ___ cost\nprint(hero["mana"])\n',
            answer="-",
            expected_output="18",
            explain=(
                "The right side reads the old mana, 24, and takes away `cost`. The left side stores 18 back in the "
                "same key. This is the campaign's mana line."
            ),
            notes="dict-write (Obj 3), the hold-the-barrier subtraction.",
        ),
        dict(
            type="bug",
            id="skipped-a-level",
            q="This program stops with `KeyError: 'wisdom'`. Mend it so it prints Lucky's wisdom.",
            code=(
                "hero = {\n"
                '    "name": "Lucky",\n'
                '    "abilities": {\n'
                '        "wisdom": 12,\n'
                "    },\n"
                "}\n"
                'print(hero["wisdom"])\n'
            ),
            fix=(
                "hero = {\n"
                '    "name": "Lucky",\n'
                '    "abilities": {\n'
                '        "wisdom": 12,\n'
                "    },\n"
                "}\n"
                'print(hero["abilities"]["wisdom"])\n'
            ),
            expected_output="12",
            explain=(
                "Wisdom is not on the big sheet. It lives inside `\"abilities\"`, so the read needs the outer key "
                "first: `hero[\"abilities\"][\"wisdom\"]`."
            ),
            notes="A KeyError from the wrong nesting level (Obj 2).",
        ),
        dict(
            type="predict",
            id="a-roster-of-sheets",
            q="What will this print?",
            code=(
                "roster = [\n"
                '    {"name": "Oogrish", "mana": 18},\n'
                '    {"name": "Lucky", "mana": 26},\n'
                "]\n"
                'print(roster[1]["mana"])\n'
            ),
            choices=["26", "18", "Lucky", "an error"],
            answer="26",
            explain=(
                "`roster[1]` is the second sheet, Lucky's, because positions count from 0. Then `[\"mana\"]` reads "
                "his mana: 26."
            ),
            notes="list-of-dicts (Obj 7): 18 counts from 1.",
        ),
        dict(
            type="predict",
            id="a-recipe-reads-the-book",
            q="What will this print?",
            code=(
                "spell_book = {\n"
                '    "Glow": 2,\n'
                '    "Warm Hands": 3,\n'
                "}\n"
                "\n"
                "def cost_of(book, name):\n"
                "    return book[name]\n"
                "\n"
                'print(cost_of(spell_book, "Glow"))\n'
            ),
            choices=["3", "Glow", "2", "an error"],
            answer="2",
            explain=(
                "During the call, `book` holds the spell book and `name` holds `\"Glow\"`. `book[name]` looks "
                "inside `name`, so it reads Glow's page and hands back 2."
            ),
            notes="def/return item (Unit 3) with a key from an ingredient: `book[\"name\"]` would be a KeyError.",
        ),
    ],
)

# =============================================================================================
# Project 4P "Mar'tu's Ledger of Heroes" (with Lucky's side quest, old groups D-E)
# =============================================================================================

LEDGER_A = (
    "# Mar'tu's Ledger of Heroes\n"
    "\n"
    "# A. Sheets\n"
    '# 1. Each sheet: "name", an\n'
    '#    "abilities" dict and an\n'
    '#    empty "spell_book". Two are\n'
    "#    done. Make gearshift and\n"
    "#    lucky the same way.\n"
)


def _ledger_sheet(var, name, abilities):
    out = f'{var} = {{\n    "name": "{name}",\n    "abilities": {{\n'
    for key, value in abilities:
        out += f'        "{key}": {value},\n'
    return out + '    },\n    "spell_book": {},\n}\n'


OOGRISH_LEDGER = _ledger_sheet("oogrish", "Oogrish", [("magical_affinity", 9), ("intelligence", 17), ("wisdom", 17)])
BOMB_LEDGER = _ledger_sheet("bomb_shell", "Bomb Shell", [("magical_affinity", 12), ("dexterity", 6), ("strength", 15)])
GEAR_LEDGER = _ledger_sheet("gearshift", "Gearshift", [("magical_affinity", 10), ("intelligence", 14), ("strength", 17)])
LUCKY_LEDGER = _ledger_sheet("lucky", "Lucky", [("magical_affinity", 13), ("dexterity", 15), ("strength", 17)])
LEDGER_B2 = "\n# B. Let the code combine it\n# 2. Write max_mana_for(affinity).\n"
LEDGER_B3 = '\n# 3. Set each sheet\'s "max_mana"\n#    with it, and "mana" to the max.\n#    Oogrish, done for you:\n'
LEDGER_C4 = "\n# C. Roster\n# 4. roster = [...]\n"
LEDGER_C5 = "\n# 5. Print Bomb Shell's dexterity\n#    and Oogrish's intelligence,\n#    through roster.\n"
LEDGER_C6 = "\n# 6. Gearshift casts Fire Bolt (6).\n"

LEDGER_RECIPE = "def max_mana_for(affinity):\n    return affinity * 2\n"


def _maxes(var):
    return (f'{var}["max_mana"] = max_mana_for({var}["abilities"]["magical_affinity"])\n'
            f'{var}["mana"] = {var}["max_mana"]\n')


LEDGER_MAXES = "".join(_maxes(var) for var in ("oogrish", "gearshift", "bomb_shell", "lucky"))
# The worked example: Oogrish's two lines, commented out in the starter so it runs before task 2 makes the recipe.
OOGRISH_DONE = "".join("# " + line + "\n" for line in _maxes("oogrish").splitlines())
LEDGER_ROSTER = "roster = [oogrish, gearshift, bomb_shell, lucky]\n"
LEDGER_PRINTS = 'print(roster[2]["abilities"]["dexterity"])\nprint(roster[0]["abilities"]["intelligence"])\n'
LEDGER_CAST = 'roster[1]["mana"] = roster[1]["mana"] - 6\n'


def _ledger(gear=GEAR_LEDGER, lucky=LUCKY_LEDGER, recipe=LEDGER_RECIPE, maxes=LEDGER_MAXES, roster=LEDGER_ROSTER,
            prints=LEDGER_PRINTS, cast=LEDGER_CAST, extra="", oogrish=OOGRISH_LEDGER, bomb=BOMB_LEDGER):
    sheets = oogrish + "\n" + bomb + ("\n" + gear if gear else "") + ("\n" + lucky if lucky else "")
    return (LEDGER_A + sheets + LEDGER_B2 + recipe + LEDGER_B3 + maxes + LEDGER_C4 + roster + LEDGER_C5 + prints
            + LEDGER_C6 + cast + extra)


LEDGER_STARTER = _ledger(gear="", lucky="", recipe="", maxes=OOGRISH_DONE, roster="", prints="", cast="")
LEDGER_SOLUTION = _ledger()
LEDGER_PICK = (
    "# Mar'tu's picks:\n"
    '# gearshift: "intelligence": 14\n'
    '#   and "strength": 17\n'
    '# lucky: "dexterity": 15\n'
    '#   and "strength": 17'
)
SIDE_QUEST = (
    "\n# Lucky's side quest\n"
    'lucky["mana"] = lucky["mana"] + 2\n'
    'if lucky["mana"] > lucky["max_mana"]:\n'
    '    lucky["mana"] = lucky["max_mana"]\n'
    'spell_name = "Glow"\n'
    "spell = {\n"
    '    "mana_cost": 2,\n'
    '    "required_affinity": 3,\n'
    "}\n"
    'oogrish["spell_book"][spell_name] = spell\n'
    'print("Glow" in roster[0]["spell_book"])\n'
    'print("Glow" in roster[1]["spell_book"])\n'
    'print("Glow" in roster[2]["spell_book"])\n'
    'print("Glow" in roster[3]["spell_book"])\n'
    'print("█" * lucky["mana"])\n'
    "my_hero = {\n"
    '    "name": "Pell",\n'
    '    "abilities": {\n'
    '        "wisdom": 11,\n'
    "    },\n"
    '    "spell_book": {},\n'
    "}\n"
)

_HEROES_CODE = "_HEROES = " + repr(HEROES) + "\n"

_SHEETS = _HEROES_CODE + r'''
_g = globals()
for _var, _hero, _row in _HEROES:
    assert _var in _g, ('Make the sheet `' + _var + '`, like the sheets above it, with `"name"`, `"abilities"` and '
                        '`"spell_book"` inside.')
    _s = _g[_var]
    assert type(_s).__name__ == 'dict', ('`' + _var + '` should be a dictionary: curly brackets, each key in quotes, '
                                         'a colon, and a comma between pairs.')
    for _k in ('name', 'abilities', 'spell_book'):
        _x = _near(_s, _k)
        assert _x is None, ('`' + _var + '` has a key ' + _lit(_x) + '. The ledger' + chr(39) + 's key is `"' + _k
                            + '"`, letter for letter.')
        assert _k in _s, '`' + _var + '` needs a `"' + _k + '"` key, like the sheets above it.'
    assert type(_s['name']).__name__ == 'str' and _sq(_hero) in _sq(_s['name']), (
        '`' + _var + '["name"]` should be the text `"' + _hero + '"`.')
    _ab = _s['abilities']
    assert type(_ab).__name__ == 'dict', ('`' + _var + '["abilities"]` should be a dictionary inside the sheet: '
                                          '`"abilities": {...}`.')
    for _k in _ab:
        if _k not in _row:
            _x = [_r for _r in _row if _sq(_r) == _sq(_k)]
            assert not _x, ('`' + _var + '["abilities"]` has a key ' + _lit(_k) + '. The table' + chr(39) + 's key '
                            'is `"' + (_x[0] if _x else '') + '"`, letter for letter.')
            assert False, ('`' + _var + '["abilities"]` has a key ' + _lit(_k) + ', which is not on the table. Use '
                           '`"magical_affinity"`, `"intelligence"`, `"wisdom"`, `"dexterity"` or `"strength"`.')
        _v = _ab[_k]
        assert type(_v).__name__ == 'int', ('`' + _var + '["abilities"]["' + _k + '"]` holds text. Numbers need no '
                                            'quotes.')
        assert _v == _row[_k], (_hero + chr(39) + 's ' + _k.replace('_', ' ') + ' is ' + str(_row[_k]) + ' on the '
                                'table, not ' + str(_v) + '.')
    assert 'magical_affinity' in _ab, ('Give `' + _var + '["abilities"]` its `"magical_affinity"`: task 3 reads it.')
    assert len(_ab) >= 3, ('Give `' + _var + '["abilities"]` two more abilities from the table, as well as '
                           '`"magical_affinity"`.')
    assert type(_s['spell_book']).__name__ == 'dict', ('`' + _var + '["spell_book"]` should be an empty dictionary: '
                                                       '`{}`.')
assert 'intelligence' in oogrish['abilities'], 'Give Oogrish' + chr(39) + 's abilities `"intelligence"`: task 5 reads it.'
assert 'dexterity' in bomb_shell['abilities'], 'Give Bomb Shell' + chr(39) + 's abilities `"dexterity"`: task 5 reads it.'
'''

_RECIPE = r'''
_f = globals().get('max_mana_for')
assert _f is not None, 'Write the recipe again: `def max_mana_for(affinity):`, with a `return` line inside.'
assert type(_f).__name__ == 'function', '`max_mana_for` is a box. Make a recipe: `def max_mana_for(affinity):`.'
_seen = []
for _a in (7, 15):
    _out, _old = _io.StringIO(), _sys.stdout
    _sys.stdout = _out
    _e = ''
    try:
        _v = _f(_a)
    except BaseException as _x:
        _v, _e = None, type(_x).__name__ + ': ' + str(_x)
    finally:
        _sys.stdout = _old
    _ev = "(Mar'tu's check called `max_mana_for(" + str(_a) + ")`, only inside the check"
    assert not _e, 'Mend this slip in the recipe: ' + _e + ' ' + _ev + '.)'
    _pr = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    assert not (_v is None and _pr), ('Hand the answer back with `return`, not `print`. ' + _ev + ': it printed '
                                      + _pr[0] + ' but handed back `None`: nothing came back.)')
    assert _v is not None, ('Add a `return` line: it hands back twice the affinity. ' + _ev
                            + ': it handed back `None`, so nothing came back.)')
    assert type(_v).__name__ == 'int', 'Hand back a number, not text: no quotes. ' + _ev + '.)'
    _seen.append(_v)
assert _seen[0] != _seen[1], ("A recipe gets its numbers when it is called: work it out from `affinity`. (Mar'tu's "
                              "check called `max_mana_for(7)` and `max_mana_for(15)`: both gave back "
                              + str(_seen[0]) + '.)')
for _a, _v in ((7, _seen[0]), (15, _seen[1])):
    assert _v == 2 * _a, ("It hands back twice the affinity. (Mar'tu's check called `max_mana_for(" + str(_a)
                          + ")`, only inside the check: it gave back " + str(_v) + ', not ' + str(2 * _a) + '.)')
'''

_MAX = _HEROES_CODE + r'''
_g = globals()
for _var, _hero, _row in _HEROES:
    _s = _g[_var]
    for _k in ('max_mana', 'mana'):
        _x = _near(_s, _k)
        assert _x is None, ('`' + _var + '` has a key ' + _lit(_x) + '. The ledger' + chr(39) + 's key is `"' + _k
                            + '"`, letter for letter.')
    assert not (_var == 'oogrish' and 'max_mana' not in _s and '# oogrish["max_mana"]' in _source), (
        'Take the `#` off Oogrish' + chr(39) + 's two lines under comment 3: they set his `"max_mana"` and `"mana"`.')
    assert 'max_mana' in _s, 'Set `' + _var + '["max_mana"]` with `max_mana_for(...)`, handing over its affinity.'
    _aff = _s['abilities']['magical_affinity']
    # A copied line that still hands over another sheet's affinity (Oogrish's worked example, say).
    for _v2, _h2, _r2 in _HEROES:
        _a2 = _get(_g.get(_v2), 'abilities', 'magical_affinity')
        assert not (_v2 != _var and _s['max_mana'] != 2 * _aff and type(_a2).__name__ == 'int'
                    and _s['max_mana'] == 2 * _a2), (
            'Hand over ' + _hero + chr(39) + 's own affinity: `' + _var + '["abilities"]["magical_affinity"]`. ('
            + str(_s['max_mana']) + ' is twice ' + _h2 + chr(39) + 's ' + str(_a2) + '.)')
    assert _s['max_mana'] == 2 * _aff, ('`' + _var + '["max_mana"]` should be twice its affinity, ' + str(2 * _aff)
                                        + ', not ' + _lit(_s['max_mana']) + '.')
    assert 'mana' in _s, 'Then set `' + _var + '["mana"]` to its max: `' + _var + '["mana"] = ' + _var + '["max_mana"]`.'
# Each hero's mana is read right after the line that first sets it (task 3), so task 6's cast and the glug in
# Lucky's side quest (even half written) never turn this red.
_snaps = [('1:' + _v + '["mana"]|roster[' + str(_i) + ']["mana"]', '_task3_' + _v + ' = ' + _v + '["mana"]')
          for _i, (_v, _h, _r) in enumerate(_HEROES)]
_anchors = [_a for _a, _l in _snaps]
def _mana_of(_ns, _var):
    if '_task3_' + _var in _ns:
        return _ns['_task3_' + _var]
    return _get(_ns.get(_var), 'mana')
def _typed_in(_var):
    for _n in _ast.parse(_source).body:
        if (type(_n).__name__ == 'Assign' and [getattr(_t, 'id', '') for _t in _n.targets] == [_var]
                and type(_n.value).__name__ == 'Dict'):
            return [_k.value for _k in _n.value.keys if getattr(_k, 'value', '') in ('max_mana', 'mana')]
    return []
_ns0, _ls0, _err0, _miss0 = _rerun(_snaps)
assert not _err0, _stop(_err0, 'your program again')
for _var, _hero, _row in _HEROES:
    _mn = _mana_of(_ns0, _var)
    if _mn != _g[_var]['max_mana']:
        _t = _typed_in(_var)
        assert not _t, ('Take `"' + _t[0] + '"` out of the `' + _var + '` sheet. Task 3 sets `"max_mana"` and '
                        '`"mana"` with lines of code under the recipe, so they follow the affinity.')
        assert False, ('Set `' + _var + '["mana"]` to its max, `' + _var + '["max_mana"]`. It holds ' + _lit(_mn)
                       + '.')
_new = {'oogrish': 5, 'gearshift': 4, 'bomb_shell': 7, 'lucky': 3}
_ch = [(_v, _v + '["abilities"]["magical_affinity"] = ' + str(_a)) for _v, _a in _new.items()] + _snaps
_tried = 'other affinities (Oogrish 5, Gearshift 4, Bomb Shell 7, Lucky 3)'
_ns, _ls, _err, _miss = _rerun(_ch)
assert not [_m for _m in _miss if _m not in _anchors], _keep(_miss[0])
assert not _err, _stop(_err, _tried)
for _var, _hero, _row in _HEROES:
    _mx, _mn = _get(_ns.get(_var), 'max_mana'), _mana_of(_ns, _var)
    _want = 2 * _new[_var]
    assert _mx == _want, ('Hand over the sheet' + chr(39) + 's own affinity, `max_mana_for(' + _var
                          + '["abilities"]["magical_affinity"])`, not a typed number. ' + _did(_tried, ': ' + _hero
                          + chr(39) + 's max stayed ' + _lit(_mx) + ', not ' + str(_want)))
    assert _mn == _want, ('Set `"mana"` from the sheet, `' + _var + '["mana"] = ' + _var + '["max_mana"]`, not a typed '
                          'number. ' + _did(_tried, ': ' + _hero + chr(39) + 's mana stayed ' + _lit(_mn)))
_ns2, _ls2, _err2, _miss2 = _rerun([('max_mana_for', 'def max_mana_for(affinity):\n    return affinity * 2 + 1')])
assert not _err2, _stop(_err2, 'another `max_mana_for`')
for _var, _hero, _row in _HEROES:
    assert _get(_ns2.get(_var), 'max_mana') == 2 * _row['magical_affinity'] + 1, (
        'Let the recipe do the math: set `' + _var + '["max_mana"]` with `max_mana_for(...)`. (Mar' + chr(39) + 'tu'
        + chr(39) + 's check swapped in another `max_mana_for`, only inside the check: ' + _hero + chr(39)
        + 's max did not change.)')
'''

_LEDGER_ROSTER = _HEROES_CODE + r'''
assert 'roster' in globals(), 'Make `roster`: a list of the four sheets, in the table' + chr(39) + 's order.'
assert type(roster).__name__ == 'list', '`roster` should be a list: square brackets, with commas between the sheets.'
assert not [_x for _x in roster if type(_x).__name__ == 'str'], (
    'Put the sheets themselves in the list, with no quotes: `oogrish`, not `"oogrish"`. ' + _QUOTES)
assert len(roster) == 4, '`roster` should hold the four sheets. It holds ' + str(len(roster)) + '.'
for _i, _h in enumerate(_HEROES):
    assert roster[_i] is globals()[_h[0]], ('Put the sheets in the table' + chr(39) + 's order: Oogrish, Gearshift, '
                                            'Bomb Shell, Lucky. Position ' + str(_i) + ' should be `' + _h[0] + '`.')
'''

_LEDGER_PRINTS = r'''
_ls = _lines()
assert _shows(_ls, 6), ('Print Bomb Shell' + chr(39) + 's dexterity: `roster[2]`, then `["abilities"]`, then '
                        '`["dexterity"]`. Bomb Shell is at position 2, counting from 0.')
assert _shows(_ls, 17), ('Print Oogrish' + chr(39) + 's intelligence: `roster[0]`, then `["abilities"]`, then '
                         '`["intelligence"]`.')
_tried = ('a roster copy where Bomb Shell' + chr(39) + 's dexterity is 3 and Oogrish' + chr(39) + 's intelligence '
          'is 11')
_ns, _ls2, _err, _miss = _rerun([('roster', _COPY + 'roster[2]["abilities"]["dexterity"] = 3\n'
                                            'roster[0]["abilities"]["intelligence"] = 11')])
assert not _miss, _keep('roster')
assert not _err, _stop(_err, _tried)
assert _shows(_ls2, 3), ('Print Bomb Shell' + chr(39) + 's dexterity through `roster`, not from his box or a typed '
                         'number: Bomb Shell is at position 2, counting from 0. ' + _did(_tried))
if not _shows(_ls2, 11) and 'wisdom' in _get(oogrish, 'abilities'):
    _tw = 'a roster copy where Oogrish' + chr(39) + 's wisdom is 12'
    _nw, _lw, _ew, _mw = _rerun([('roster', _COPY + 'roster[0]["abilities"]["wisdom"] = 12')])
    assert _ew or not _shows(_lw, 12), ('Read `["intelligence"]`, not `["wisdom"]`. Oogrish has 17 of both, so the '
                                        'number looked right. ' + _did(_tw, ': your program printed 12'))
assert _shows(_ls2, 11), ('Print Oogrish' + chr(39) + 's intelligence through `roster`, not from his box or a typed '
                          'number: Oogrish is at position 0. ' + _did(_tried))
'''

_FIRE_BOLT = r'''
_mx, _mn = _get(gearshift, 'max_mana'), _get(gearshift, 'mana')
assert _mn != _mx, ('Gearshift casts Fire Bolt: take 6 from his mana, by key. His mana is still full, ' + _lit(_mx)
                    + '.')
assert _mn != 6, ('Take 6 away from his mana; don' + chr(39) + 't set his mana to 6. Read the old mana on the right '
                  'side of `=`.')
assert _mn == _mx - 6, 'Take 6 from his old mana, once: it should be ' + str(_mx - 6) + ' now, not ' + _lit(_mn) + '.'
_tried = 'an affinity of 8 for Gearshift'
_ns, _ls, _err, _miss = _rerun([('gearshift', 'gearshift["abilities"]["magical_affinity"] = 8')])
assert not _err, _stop(_err, _tried)
_left = _get(_ns.get('gearshift'), 'mana')
assert _left == 10, ('Read the old mana and take 6 from it, so it follows the sheet: `roster[1]["mana"] - 6`, not a '
                     'typed number. ' + _did(_tried, ': his mana ended at ' + _lit(_left) + ', not 10'))
_tried = 'Gearshift at 11 mana just before the cast'
_ns, _ls, _err, _miss = _rerun([('1:gearshift["mana"]|roster[1]["mana"]', 'gearshift["mana"] = 11')])
assert not _err, _stop(_err, _tried)
_left = _get(_ns.get('gearshift'), 'mana')
if not _miss and _left != 5:
    _end = ': his mana ended at ' + _lit(_left) + ', not 5'
    assert _left != _get(_ns.get('gearshift'), 'max_mana') - 6, (
        'Take 6 from the mana he has now, `roster[1]["mana"]`, not from his max. ' + _did(_tried, _end))
    assert False, 'Read the mana he has now and take 6 from it: `roster[1]["mana"] - 6`. ' + _did(_tried, _end)
'''

_GLUG = r'''
for _start, _want in ((20, 22), (25, 26), (26, 26)):
    _tried = 'Lucky at ' + str(_start) + ' mana before the glug'
    _ns, _ls, _err, _miss = _rerun([('1:lucky["mana"]|roster[3]["mana"]', 'lucky["mana"] = ' + str(_start))])
    assert not _miss, ('Set Lucky' + chr(39) + 's mana on a line of its own first (task 3), so Mar' + chr(39) + 'tu'
                       + chr(39) + 's check can try other numbers there.')
    assert not _err, _stop(_err, _tried)
    _got = _get(_ns.get('lucky'), 'mana')
    if _got != _want:
        _end = ': he ended at ' + _lit(_got) + ', not ' + str(_want)
        assert _got != _start, 'Lucky drinks glug: add 2 to his mana, by key. ' + _did(_tried, _end)
        assert not (type(_got).__name__ == 'int' and _got > _want), (
            'Never over his max: if his mana goes over `lucky["max_mana"]`, set it back to the max. ' + _did(_tried, _end))
        assert False, 'Add 2 to what he has, then stop at his max. ' + _did(_tried, _end)
'''

_GLOW_PAGE = r'''
_bk = _get(oogrish, 'spell_book')
assert type(_bk).__name__ == 'dict' and 'Glow' in _bk, (
    'Give Oogrish a page: `spell_name = "Glow"`, a `spell` dictionary, then `oogrish["spell_book"][spell_name] = spell`.')
assert type(_bk['Glow']).__name__ == 'dict', 'Store a spell dictionary under `"Glow"`, like `{"mana_cost": 2}`.'
_tried = '`spell_name = "Frost Veil"`'
_ns, _ls, _err, _miss = _rerun([('spell_name', 'spell_name = "Frost Veil"')])
assert not _miss, ('Make `spell_name = "Glow"` on a line of its own, then store with '
                   '`oogrish["spell_book"][spell_name] = spell`.')
assert not _err, _stop(_err, _tried)
assert _get(_ns.get('oogrish'), 'spell_book', 'Frost Veil') != '(missing)', (
    'Store it with the key from the variable, `oogrish["spell_book"][spell_name] = spell`, so a new name gets a new '
    'page. ' + _did(_tried, ': Oogrish' + chr(39) + 's book got no Frost Veil page'))
'''

_GLOW_LINES = r'''
def _tf(_ls):
    return [_l for _l in _ls if _said([_l], 'True') or _said([_l], 'False')]
_base = _tf(_lines())
assert len(_base) >= 4, __FOUR__
# By behavior, so a loop passes too: give a hero with no Glow page one, only inside the check, and their line
# must change.
for _var, _hero in (('gearshift', 'Gearshift'), ('bomb_shell', 'Bomb Shell'), ('lucky', 'Lucky')):
    _tried = 'a Glow page for ' + _hero
    _ns, _ls, _err, _miss = _rerun([(_var, _var + '["spell_book"]["Glow"] = {"mana_cost": 2}')])
    assert not _miss, _keep(_var)
    assert not _err, _stop(_err, _tried)
    assert _tf(_ls) != _base, __ASK__ + ' ' + _did(_tried, ': no True or False line changed')
'''

_OWN_HERO = r'''
_four = ('oogrish', 'gearshift', 'bomb_shell', 'lucky')
_mine = [_v for _k, _v in list(globals().items()) if not _k.startswith('_') and _k not in _four
         and type(_v).__name__ == 'dict' and ('name' in _v or 'abilities' in _v or 'spell_book' in _v)]
assert _mine, __MAKE__
_ok = [_v for _v in _mine if type(_v.get('name')).__name__ == 'str' and _v['name'].strip()
       and type(_v.get('abilities')).__name__ == 'dict'
       and [_x for _x in _v['abilities'].values() if type(_x).__name__ == 'int']
       and type(_v.get('spell_book')).__name__ == 'dict']
if not _ok:
    _h = _mine[0]
    assert type(_h.get('name')).__name__ == 'str' and _h['name'].strip(), __NAME__
    assert type(_h.get('abilities')).__name__ == 'dict', __ABIL__
    assert [_x for _x in _h['abilities'].values() if type(_x).__name__ == 'int'], __ABIL_NUM__
    assert False, __BOOK__
'''

_BAR = r'''
assert [_l for _l in _lines() if _l.count('█') == lucky['mana']], 'Print Lucky' + chr(39) + 's mana as a bar of `█`.'
_ns, _ls, _err, _miss = _rerun([('1:lucky["mana"]|roster[3]["mana"]', 'lucky["mana"] = 20')])
assert not _err, _stop(_err, 'Lucky at 20 mana before the glug')
assert [_l for _l in _ls if _l.count('█') == 22], (
    'Build the bar from his mana after the glug: `"█" * lucky["mana"]`. ' + _did('Lucky at 20 mana before the glug'))
'''

PROJECT_4P = dict(
    kind="project",
    id="martus-ledger-of-heroes",
    title="Mar'tu's Ledger of Heroes",
    minutes=20,
    summary="Copy every hero's record into the cabin ledger: four sheets, their mana worked out by a recipe, and a roster.",
    intro=(
        "Mar'tu copies each hero's record into the cabin ledger, Institute-style: the same keys on every sheet.\n"
        "Three parts, in order: A. the sheets, B. let the code combine it, C. the roster.\n"
        "Use the party table:\n"
        "```text\nhero        INT WIS DEX STR AFF\nOogrish      17  17  14  13   9\nGearshift    14  15  13  17  10\n"
        "Bomb Shell   14   8   6  15  12\nLucky        13  12  15  17  13\n```\n"
        "The keys are `\"intelligence\"`, `\"wisdom\"`, `\"dexterity\"`, `\"strength\"` and `\"magical_affinity\"`. "
        "Oogrish and Bomb Shell are done. Pick two abilities each for Gearshift and Lucky."
    ),
    martu=(
        "At the Institute, every record had the same keys in the same places. That is what made them useful. A "
        "record nobody can read is a diary, yes?\n"
        "My check tries other numbers, only inside the check: other affinities, another recipe. Your sheets stay "
        "yours."
    ),
    names=["gearshift", "lucky", "max_mana_for", "affinity", "roster"],
    pick=LEDGER_PICK,
    starter=LEDGER_STARTER,
    checkpoints=[
        dict(
            id="four-sheets",
            text=(
                "A. Make `gearshift` and `lucky` like the sheets above. Each needs `\"name\"`, `\"abilities\"` "
                "(`\"magical_affinity\"` and two more from the table) and an empty `\"spell_book\"`."
            ),
            dictated=False,
            hints=[
                "Copy the shape of `oogrish`: the same three keys, with each hero's own numbers from the table.",
                "A dictionary can hold another as a value, `\"parts\": {\"wick\": 2}`. An empty one is `{}`.",
                "Write `gearshift = {` with `\"name\": \"Gearshift\",`, an `\"abilities\"` card holding "
                "`\"magical_affinity\": 10` and two more, then `\"spell_book\": {},` and `}`, above `# B.` Then the same for Lucky.",
            ],
            checks=[("four sheets with the table's values", dx() + _SHEETS)],
            pass_line="Mar'tu: Four records, the same keys. Institute-style.",
        ),
        dict(
            id="max-mana-recipe",
            text="B. Write `max_mana_for(affinity)` again. It hands back twice the affinity.",
            dictated=False,
            hints=[
                "You wrote this recipe in Unit 3. One ingredient, `affinity`. It hands back twice that.",
                "`def double(n):` with `return n * 2` inside hands back twice whatever comes in.",
                "Write `def max_mana_for(affinity):` under `# 2.`, with `return affinity * 2` under it, indented.",
            ],
            checks=[("max_mana_for hands back twice the affinity", dx() + _RECIPE)],
            pass_line="Gearshift: Math checks out.",
        ),
        dict(
            id="set-the-mana",
            text=(
                "B. Take the `#` off Oogrish's two lines. Then set `\"max_mana\"` and `\"mana\"` the same way for the "
                "other three sheets, each with its own affinity."
            ),
            dictated=False,
            hints=[
                "Copy Oogrish's shape, and change every `oogrish` to the sheet you are setting.",
                "A call can hand over a value read from a sheet: `double(jar[\"lid\"][\"turns\"])`.",
                "Two steps work too: `aff = gearshift[\"abilities\"][\"magical_affinity\"]`, then "
                "`gearshift[\"max_mana\"] = max_mana_for(aff)`.",
                "Write `gearshift[\"max_mana\"] = max_mana_for(gearshift[\"abilities\"][\"magical_affinity\"])`, "
                "then `gearshift[\"mana\"] = gearshift[\"max_mana\"]`, then the same for Bomb Shell and Lucky, above `# C.`",
            ],
            checks=[("max_mana follows the affinity, and mana is the max", dx() + _MAX)],
            pass_line="Mar'tu: Eight lines that look alike, yes? In Unit 6, a loop does every hero in two.",
        ),
        dict(
            id="make-the-roster",
            text="C. Make `roster`, a list of the four sheets: Oogrish, Gearshift, Bomb Shell, Lucky.",
            dictated=False,
            hints=[
                "The four sheets go in by their variable names, with no quotes, in the table's order.",
                "`shelf = [maps, runes]` makes a list of two things that already exist.",
                "Write `roster = [oogrish, gearshift, bomb_shell, lucky]` under `# 4.`",
            ],
            checks=[("roster holds the four sheets in order", dx() + _LEDGER_ROSTER)],
            pass_line="Oogrish: Steady, now. All four, in order.",
        ),
        dict(
            id="read-through-the-roster",
            text="C. Print Bomb Shell's dexterity and Oogrish's intelligence, reading through `roster`.",
            dictated=False,
            hints=[
                "Bomb Shell is at position 2, Oogrish at 0. Each read is a position, then `\"abilities\"`, then the "
                "ability.",
                "`drawer[1][\"card\"][\"score\"]`: position, then the outer key, then the inner key.",
                "Write `print(roster[2][\"abilities\"][\"dexterity\"])` under `# 5.`, then the same for Oogrish's "
                "intelligence at position 0.",
            ],
            checks=[("both reads go through roster", dx() + _LEDGER_PRINTS)],
            pass_line="Bomb Shell: Six. Clumsy hands. Working on it.",
        ),
        dict(
            id="fire-bolt",
            text="C. Gearshift casts Fire Bolt, which costs 6 mana. Take it from his mana, by key.",
            dictated=False,
            hints=[
                "Gearshift is at position 1. Read his old mana, take away 6, and store it back.",
                "`hero[\"mana\"] = hero[\"mana\"] - cost` reads the old value on the right and stores the new one on "
                "the left.",
                "Write `roster[1][\"mana\"] = roster[1][\"mana\"] - 6` under `# 6.`",
            ],
            checks=[("Fire Bolt spends 6 of Gearshift's mana", dx() + _FIRE_BOLT)],
            pass_line="Gearshift: Fire Bolt away. Fourteen left.",
        ),
    ],
    solution=LEDGER_SOLUTION,
    partials=[
        _ledger(recipe="", maxes=OOGRISH_DONE, roster="", prints="", cast=""),
        _ledger(maxes=OOGRISH_DONE, roster="", prints="", cast=""),
        _ledger(roster="", prints="", cast=""),
        _ledger(prints="", cast=""),
        _ledger(cast=""),
    ],
    assemble=dict(
        lines=[line for line in LEDGER_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=[
            'roster = ["oogrish", "gearshift", "bomb_shell", "lucky"]',
            'oogrish["max_mana"] = max_mana_for(oogrish["magical_affinity"])',
            'roster[1]["mana"] = 14',
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One sheet, all its keys",
            text=(
                "```text\ngearshift\n  \"name\"       -> \"Gearshift\"\n  \"abilities\"  -> {affinity 10,\n"
                "                   + two more}\n  \"spell_book\" -> {}\n  \"max_mana\"   -> 20  (task 3)\n"
                "  \"mana\"       -> 20  (task 3)\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            label="Task 3 for one sheet",
            text=(
                "1. Get it: `oogrish[\"abilities\"][\"magical_affinity\"]` is 9.\n"
                "2. Hand it over: `max_mana_for(9)` hands back 18.\n"
                "3. Store it: `oogrish[\"max_mana\"]` gets 18, a new key.\n"
                "4. Copy it: `oogrish[\"mana\"]` gets 18 too."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Every campaign sheet had `\"mana\"` and `\"max_mana\"`, and the mana bars read them. The roster you "
                "build here is the shape of `party.members`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's side quest",
        text=(
            "Lucky has a list, of course.\n"
            "1. Glug: add 2 to his mana, but never over his max. Use an `if`.\n"
            "2. Give Oogrish a spell: make `spell_name = \"Glow\"` and a `spell` dictionary, then store it in "
            "`oogrish[\"spell_book\"]` with `spell_name` as the key.\n"
            "3. One line per hero, through `roster`: print whether `\"Glow\"` is in that hero's book. (A loop works "
            "too. Loops come in Unit 6.)\n"
            "4. Print Lucky's mana as a bar of `█` blocks.\n"
            "5. Make a sheet for your own hero: any name in quotes, with `\"abilities\"` and an empty "
            "`\"spell_book\"`, like the others."
        ),
        hints=[
            "`if lucky[\"mana\"] > lucky[\"max_mana\"]:` catches too much glug. Under it, set the mana back to the max.",
            "`oogrish[\"spell_book\"][spell_name] = spell` stores a page in his book. `\"█\" * 3` makes three blocks.",
            "`\"Glow\" in roster[0][\"spell_book\"]` asks Oogrish's book. Do the same for positions 1, 2 and 3.",
            "For your own hero, copy the shape of `oogrish` under a new variable name, with your hero's own name and "
            "at least one ability.",
            "Write `print(\"█\" * lucky[\"mana\"])` for the bar, after the glug.",
        ],
        checks=[
            ("glug adds 2, never over the max", dx() + _GLUG),
            ("Glow is stored in Oogrish's book by a variable key", dx() + _GLOW_PAGE),
            ("a True or False line per hero, by behavior", dx() + fill(
                _GLOW_LINES,
                four="For each hero, print whether `\"Glow\"` is in their book: four lines of `True` or `False`, one "
                     "per hero.",
                ask="Ask each hero's own book, one line each, like `\"Glow\" in roster[1][\"spell_book\"]`.",
            )),
            ("Lucky's mana bar follows his mana", dx() + _BAR),
            ("a sheet for your own hero", dx() + fill(
                _OWN_HERO,
                make="Make a sheet for your own hero, like `oogrish`: a new variable holding `\"name\"`, "
                     "`\"abilities\"` and `\"spell_book\"`.",
                name="Give your hero's sheet a `\"name\"`: any name, as text in quotes.",
                abil="Give your hero's sheet `\"abilities\"`: a dictionary inside the sheet, like "
                     "`{\"strength\": 11}`.",
                abil_num="Put at least one ability in `\"abilities\"`, with a whole number as its value, like "
                         "`\"strength\": 11`.",
                book="Give your hero's sheet an empty `\"spell_book\"`: `{}`.",
            )),
        ],
        solution=LEDGER_SOLUTION + SIDE_QUEST,
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]',
        why=(
            "Every sheet in the campaign had `\"mana\"` and `\"max_mana\"`, and the mana bars read them by key. Your "
            "ledger builds those same keys, from the affinity, with a recipe."
        ),
    ),
    takeaway="Sheets with the same keys, a recipe to fill them, a roster to hold them: read and write by position, then key.",
    wrong_answers=[
        dict(why="the starter (Gearshift and Lucky not made)", code=LEDGER_STARTER, fails_at=1,
             message_contains="Make the sheet `gearshift`"),
        dict(why="a key with no quotes: {name: ...} (NameError; keys are text, box names are not)",
             code=_ledger(gear=GEAR_LEDGER.replace('"name":', "name:")), fails_at=0,
             message_contains="name 'name' is not defined"),
        dict(why="= in place of : inside the dictionary",
             code=_ledger(gear=GEAR_LEDGER.replace('"name":', '"name" =')), fails_at=0,
             message_contains="cannot assign to literal"),
        # The explainer's Unit 5 rows (explain.test.ts reads these by their `why`).
        dict(why="the name as a value with no quotes: \"name\": Gearshift (NameError; text needs quotes)",
             code=_ledger(gear=GEAR_LEDGER.replace('"name": "Gearshift"', '"name": Gearshift')), fails_at=0,
             message_contains="name 'Gearshift' is not defined"),
        dict(why="the recipe with no return, the rest written (the spend does math with None)",
             code=_ledger(recipe="def max_mana_for(affinity):\n    total = affinity * 2\n"), fails_at=0,
             message_contains="'NoneType' and 'int'"),
        dict(why="a missing comma after a text value (reported on the next line)",
             code=_ledger(gear=GEAR_LEDGER.replace('"Gearshift",', '"Gearshift"')), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="a missing comma after a number (reported on that line)",
             code=_ledger(gear=GEAR_LEDGER.replace('"magical_affinity": 10,', '"magical_affinity": 10')), fails_at=0,
             message_contains="Perhaps you forgot a comma"),
        dict(why="a missing colon (on a later line of the card; on its first line 3.13 says 'forgot a comma')",
             code=_ledger(gear=GEAR_LEDGER.replace('"strength": 17', '"strength" 17')),
             fails_at=0, message_contains="':' expected after dictionary key"),
        dict(why="a value off the table (Gearshift's strength 15)",
             code=_ledger(gear=GEAR_LEDGER.replace('"strength": 17', '"strength": 15')), fails_at=1,
             message_contains="17 on the table"),
        dict(why="a key with a capital (KEY)", code=_ledger(lucky=LUCKY_LEDGER.replace('"strength"', '"Strength"')),
             fails_at=1, message_contains='"strength"`, letter for letter'),
        dict(why="an ability that is not on the table",
             code=_ledger(lucky=LUCKY_LEDGER.replace('"strength": 17', '"charm": 17')), fails_at=1,
             message_contains="not on the table"),
        dict(why="only the affinity in abilities", code=_ledger(lucky=_ledger_sheet("lucky", "Lucky", [("magical_affinity", 13)])),
             fails_at=1, message_contains="two more abilities"),
        dict(why="a number in quotes", code=_ledger(gear=GEAR_LEDGER.replace('"intelligence": 14', '"intelligence": "14"')),
             fails_at=1, message_contains="Numbers need no quotes"),
        dict(why="the spell book as a list", code=_ledger(gear=GEAR_LEDGER.replace('"spell_book": {}', '"spell_book": []')),
             fails_at=1, message_contains="empty dictionary"),
        dict(why="no spell book", code=_ledger(gear=GEAR_LEDGER.replace('    "spell_book": {},\n', '')), fails_at=1,
             message_contains='needs a `"spell_book"` key'),
        dict(why="the recipe prints instead of returning (RET)",
             code=_ledger(recipe="def max_mana_for(affinity):\n    print(affinity * 2)\n", maxes="", roster="",
                          prints="", cast=""), fails_at=2, message_contains="handed back `None`"),
        dict(why="the recipe hands back one fixed number (PAR-CONST)",
             code=_ledger(recipe="def max_mana_for(affinity):\n    return 20\n"), fails_at=2,
             message_contains="both gave back 20"),
        dict(why="the recipe adds instead of doubling", code=_ledger(recipe="def max_mana_for(affinity):\n    return affinity + 2\n"),
             fails_at=2, message_contains="twice the affinity"),
        dict(why="max_mana typed (CMB)",
             code=_ledger(maxes=LEDGER_MAXES.replace('max_mana_for(oogrish["abilities"]["magical_affinity"])', "18")),
             fails_at=3, message_contains="not a typed number"),
        dict(why="the affinity typed into the call (CMB)",
             code=_ledger(maxes=LEDGER_MAXES.replace('max_mana_for(lucky["abilities"]["magical_affinity"])',
                                                     "max_mana_for(13)")), fails_at=3,
             message_contains="sheet's own affinity"),
        dict(why="worked out by hand, not with the recipe",
             code=_ledger(maxes=LEDGER_MAXES.replace('max_mana_for(bomb_shell["abilities"]["magical_affinity"])',
                                                     'bomb_shell["abilities"]["magical_affinity"] * 2')), fails_at=3,
             message_contains="Let the recipe do the math"),
        dict(why="mana typed (CMB: a literal instead of reading by key)",
             code=_ledger(maxes=LEDGER_MAXES.replace('oogrish["mana"] = oogrish["max_mana"]', 'oogrish["mana"] = 18')),
             fails_at=3, message_contains='Set `"mana"` from the sheet'),
        dict(why="max_mana and mana typed into Gearshift's sheet, with no task 3 lines for him (CMB)",
             code=_ledger(gear=GEAR_LEDGER.replace('    "spell_book": {},\n',
                                                   '    "spell_book": {},\n    "max_mana": 20,\n    "mana": 20,\n'),
                          maxes=LEDGER_MAXES.replace(_maxes("gearshift"), "")), fails_at=3,
             message_contains="out of the `gearshift` sheet"),
        dict(why="a key spelled Max_Mana (KEY)", code=_ledger(maxes=LEDGER_MAXES.replace(
            'gearshift["max_mana"]', 'gearshift["Max_Mana"]')), fails_at=3, message_contains='"max_mana"`, letter for letter'),
        dict(why="a read with Max_Mana when the key is max_mana (KeyError)", code=_ledger(maxes=LEDGER_MAXES.replace(
            'gearshift["mana"] = gearshift["max_mana"]', 'gearshift["mana"] = gearshift["Max_Mana"]')), fails_at=0,
             message_contains="KeyError: 'Max_Mana'"),
        dict(why="Oogrish's worked example copied for Gearshift, still reading oogrish[...] in the call",
             code=_ledger(maxes=LEDGER_MAXES.replace('max_mana_for(gearshift["abilities"]["magical_affinity"])',
                                                     'max_mana_for(oogrish["abilities"]["magical_affinity"])')),
             fails_at=3, message_contains="Hand over Gearshift's own affinity"),
        dict(why="Bomb Shell's line copied from Lucky's (twice another sheet's affinity, worded for each sheet)",
             code=_ledger(maxes=LEDGER_MAXES.replace('max_mana_for(bomb_shell["abilities"]["magical_affinity"])',
                                                     'max_mana_for(lucky["abilities"]["magical_affinity"])')),
             fails_at=3, message_contains="(26 is twice Lucky's 13.)"),
        dict(why="the # left on Oogrish's worked example (his sheet never set)",
             code=_ledger(maxes=OOGRISH_DONE + LEDGER_MAXES.replace(_maxes("oogrish"), "")), fails_at=3,
             message_contains="Take the `#` off Oogrish's two lines"),
        dict(why="Oogrish's sheet never set and no worked example left (the plain message)",
             code=_ledger(maxes=LEDGER_MAXES.replace(_maxes("oogrish"), "")), fails_at=3,
             message_contains='Set `oogrish["max_mana"]`'),
        dict(why="a skipped level in the call (KeyError)", code=_ledger(maxes=LEDGER_MAXES.replace(
            'oogrish["abilities"]["magical_affinity"]', 'oogrish["magical_affinity"]')), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the roster made of names in quotes", code=_ledger(roster='roster = ["oogrish", "gearshift", '
                                                                        '"bomb_shell", "lucky"]\n', prints="", cast=""),
             fails_at=4, message_contains="no quotes"),
        dict(why="the roster out of order", code=_ledger(roster="roster = [gearshift, oogrish, bomb_shell, lucky]\n",
                                                         prints="", cast=""), fails_at=4,
             message_contains="Position 0 should be `oogrish`"),
        dict(why="the roster missing a hero", code=_ledger(roster="roster = [oogrish, gearshift, bomb_shell]\n",
                                                           prints="", cast=""), fails_at=4, message_contains="It holds 3"),
        dict(why="roster[\"Bomb Shell\"] (TypeError)",
             code=_ledger(prints='print(roster["Bomb Shell"]["abilities"]["dexterity"])\n', cast=""), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="read from the boxes, not through roster",
             code=_ledger(prints='print(bomb_shell["abilities"]["dexterity"])\nprint(oogrish["abilities"]["intelligence"])\n'),
             fails_at=5, message_contains="through `roster`"),
        dict(why="the numbers typed", code=_ledger(prints="print(6)\nprint(17)\n"), fails_at=5,
             message_contains="through `roster`"),
        dict(why="Oogrish's wisdom read for his intelligence (17 and 17: the number looks right)",
             code=_ledger(prints=LEDGER_PRINTS.replace('["intelligence"]', '["wisdom"]')), fails_at=5,
             message_contains="not `[\"wisdom\"]`"),
        dict(why="counting from 1: roster[3] for Bomb Shell (Lucky's dexterity)",
             code=_ledger(prints=LEDGER_PRINTS.replace("roster[2]", "roster[3]")), fails_at=5,
             message_contains="position 2"),
        dict(why="Gearshift's mana typed after the cast (CMB)", code=_ledger(cast='roster[1]["mana"] = 14\n'),
             fails_at=6, message_contains="not a typed number"),
        dict(why="the mana set to the cost (hero[\"mana\"] = 6, not - 6)", code=_ledger(cast='roster[1]["mana"] = 6\n'),
             fails_at=6, message_contains="set his mana to 6"),
        dict(why="the cost taken from his max, not from the mana he has now",
             code=_ledger(cast='roster[1]["mana"] = roster[1]["max_mana"] - 6\n'), fails_at=6,
             message_contains="not from his max"),
        dict(why="roster[\"Gearshift\"] (TypeError)",
             code=_ledger(cast='roster["Gearshift"]["mana"] = roster["Gearshift"]["mana"] - 6\n'), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="worked out but never stored", code=_ledger(cast='roster[1]["mana"] - 6\n'), fails_at=6,
             message_contains="still full"),
        dict(why="dot access", code=_ledger(cast="roster[1].mana -= 6\n"), fails_at=0,
             message_contains="has no attribute 'mana'"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="dict-make,dict-nested,dict-write,list-of-dicts,return-value",
             solo="false", dictates="",
             foreign_names="parts,wick,double,n,jar,lid,turns,shelf,maps,runes,title,hero,cost,pages,aff,drawer,card,score",
             par="(7,),(15,)") + "\n"
        "Task 3's worked example (teacher's ruling): Oogrish's two lines sit in the starter under comment 3, "
        "commented out so the program still runs before task 2 makes the recipe; the task says to take the `#` "
        "off, then set the other three the same way (about 1 minute saved for G1). Those two lines run long (78 "
        "and 39 characters with their `# `), like the campaign's own shapes, so they are the one exception to the "
        "starter's phone-width rule. The earlier partials keep them commented. A copied line that still hands over another "
        "sheet's affinity gets 'Hand over Gearshift's own affinity ... (18 is twice Oogrish's 9.)', worded for "
        "each sheet. The hint ladder gains a two-step rung (`aff = ...`, then `max_mana_for(aff)`). Site request: "
        "a per-task More structure (Assemble for the current task only), since the project's Assemble is the "
        "whole ledger.\n"
        "Starter: the task-group headers (A, B, C) and, because 'Show me more' is the default preset and the "
        "prototype has one starter, two of the four sheets pre-built (Oogrish with intelligence, Bomb Shell with "
        "dexterity: task 5 reads them; G1 R17). Under 'Keep it short' the site would drop the two sheets (a site "
        "request: a per-preset starter). Checks: the values match the party table (any two real abilities pass, "
        "lint e; 'Use Mar'tu's picks' is a note), PAR on max_mana_for with 7 and 15 (never a hero's affinity: 9, "
        "10, 12, 13), CMB on max_mana (every affinity changed inside the check) plus a swapped-in recipe (so `* 2` "
        "by hand fails 'let the recipe do the math'), the nested reads through roster (the values, then a roster of copies with dexterity 3 and "
        "intelligence 11, so a read of the boxes or a typed number fails and a box taken from `roster` passes), KEY on "
        "`\"max_mana\"`/`\"mana\"`, and the Fire Bolt rerun (Gearshift at affinity 8 must end at 10). Task 3 "
        "reads each hero's mana right after the line that first sets it, so task 6's cast and the side quest's glug "
        "(even half written, before its `if`) keep task 3 green; `\"max_mana\"`/`\"mana\"` typed into a sheet "
        "literal gets 'take it out of the sheet'. Task 5 names Oogrish's wisdom (17, like his intelligence). Task "
        "6 also reruns with Gearshift at 11 mana just before the cast, so `roster[1][\"max_mana\"] - 6` fails 'not "
        "from his max'. Lucky's side quest (old groups D-E): glug +2 capped at the max (rerun at 20, 25, 26, after "
        "the line that sets his mana), Glow stored in Oogrish's book by a variable key (rerun with spell_name Frost "
        "Veil), a True or False line per hero, by behavior (at least four such lines, and a rerun that gives "
        "Gearshift, Bomb Shell and then Lucky a Glow page must change a line each time; no `in` is counted, so a "
        "`for` loop over `roster` passes, while typed `True`/`False` or four lines about Oogrish fail), Lucky's "
        "bar of █ (22 blocks at 20 + 2), and task 5, a sheet for the student's own hero (a personal value: any "
        "dict variable other than the four, with a non-empty text name, an abilities dict holding a whole number "
        "and a spell_book dict; the name is never echoed back). Every task's check is behavior-based; the "
        "assemble lines are the solution without comments."
    ),
)

# =============================================================================================
# Optional advanced challenge "The Barrier, From Blank" (after the project; costs no one core time)
# =============================================================================================

BARRIER_SETUP = (
    "caster = {\n"
    '    "name": "Gearshift",\n'
    '    "mana": 20,\n'
    '    "abilities": {\n'
    '        "magical_affinity": 10,\n'
    "    },\n"
    '    "spell_book": {\n'
    '        "Glow": {\n'
    '            "mana_cost": 2,\n'
    '            "required_affinity": 3,\n'
    "        },\n"
    '        "Lantern Ward": {\n'
    '            "mana_cost": 6,\n'
    '            "required_affinity": 9,\n'
    "        },\n"
    "    },\n"
    "}\n"
)
BARRIER_STARTER = (
    "# The game hands you caster. Write\n"
    "# cast_spell(caster, spell_name),\n"
    "# then call it once.\n"
)
BARRIER_DEF = "def cast_spell(caster, spell_name):\n"
BARRIER_GUARD = (
    '    if spell_name not in caster["spell_book"]:\n'
    '        print("No such spell.")\n'
)
BARRIER_READ = (
    "    else:\n"
    '        spell = caster["spell_book"][spell_name]\n'
)
BARRIER_AFF = (
    '        if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:\n'
    '            print("Not skilled enough.")\n'
)
BARRIER_MANA = (
    '        elif caster["mana"] < spell["mana_cost"]:\n'
    '            print("Needs more mana.")\n'
)
BARRIER_SPEND = (
    "        else:\n"
    '            caster["mana"] = caster["mana"] - spell["mana_cost"]\n'
)
BARRIER_CALL = '\ncast_spell(caster, "Lantern Ward")\nprint(caster["mana"])\n'


def _barrier(guard=BARRIER_GUARD, read=BARRIER_READ, aff=BARRIER_AFF, mana=BARRIER_MANA, spend=BARRIER_SPEND,
             call=BARRIER_CALL, head=BARRIER_DEF):
    return head + guard + read + aff + mana + spend + call


BARRIER_SOLUTION = _barrier()

# The helpers every checkpoint shares: fresh sheets for a caster called Pell, and two spells the game's own
# caster never has (Moon Step and Ash Ward), so no value collides with the student's own call.
_BARRIER = r'''
_f = globals().get('cast_spell')
assert _f is not None, __NO_DEF__
assert type(_f).__name__ == 'function', __NOT_DEF__
assert _f.__code__.co_argcount == 2, __TWO__
_SP = {'Moon Step': (5, 7), 'Ash Ward': (8, 11)}
def _cast_once(_aff, _mana, _name):
    _c = {'name': 'Pell', 'mana': _mana, 'abilities': {'magical_affinity': _aff},
          'spell_book': {_k: {'mana_cost': _v[0], 'required_affinity': _v[1]} for _k, _v in _SP.items()}}
    _out, _old = _io.StringIO(), _sys.stdout
    _sys.stdout = _out
    _e, _back = '', None
    try:
        _back = _f(_c, _name)
    except BaseException as _x:
        _e = type(_x).__name__ + (': ' + str(_x) if str(_x) else '')
    finally:
        _sys.stdout = _old
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ls, _e, _c.get('mana'), _back
def _skilled(_ls):
    return [_l for _l in _ls if 'skilled' in _l.lower() and _re.search(r"\bnot\b|n't|\bno\b|\bun|lack|never",
                                                                         _l.lower())]
def _needs(_ls):
    return [_l for _l in _ls if 'more mana' in _l.lower()]
def _ev(_aff, _mana, _name, _end=''):
    _what = ('a spell that is not in its book' if _name not in _SP else
             'a spell needing ' + str(_SP[_name][1]) + ' and costing ' + str(_SP[_name][0]))
    return ("(Mar'tu's check called `cast_spell` with a caster at affinity " + str(_aff) + ' and mana '
            + str(_mana) + ', and ' + _what + ', only inside the check' + _end + '.)')
def _ran(_aff, _mana, _name):
    _ls, _e, _left, _back = _cast_once(_aff, _mana, _name)
    assert not _e, 'Mend this slip in the recipe: ' + _e + ' ' + _ev(_aff, _mana, _name)
    return _ls, _left, _back
'''

_BARRIER_MISSING = r'''
_ls, _e, _left, _back = _cast_once(11, 15, 'Star Fall')
if _e:
    assert 'Star Fall' not in _e, __ASK_FIRST__ + ' ' + _ev(11, 15, 'Star Fall', ': ' + _e)
    assert False, 'Mend this slip in the recipe: ' + _e + ' ' + _ev(11, 15, 'Star Fall')
assert _ls, __SAY_MISSING__ + ' ' + _ev(11, 15, 'Star Fall', ': nothing was printed')
assert _left == 15, __SPEND_NOTHING__ + ' ' + _ev(11, 15, 'Star Fall', ': the mana went to ' + _lit(_left))
'''

_BARRIER_AFF = r'''
_missing = _cast_once(11, 15, 'Star Fall')[0]
for _aff, _mana, _name, _kind in ((6, 15, 'Moon Step', 'low'), (6, 2, 'Moon Step', 'both'),
                                  (8, 15, 'Moon Step', 'ok'), (10, 15, 'Ash Ward', 'low'),
                                  (7, 15, 'Moon Step', 'exact'), (11, 15, 'Ash Ward', 'exact')):
    _ls, _left, _back = _ran(_aff, _mana, _name)
    if _kind in ('low', 'both'):
        if not _skilled(_ls):
            assert not (_ls and _ls == _missing), __OWN_BOOK__ + ' ' + _ev(_aff, _mana, _name)
            assert not (_kind == 'both' and _needs(_ls)), __AFF_FIRST__ + ' ' + _ev(_aff, _mana, _name)
            assert False, __TURN_AWAY__ + ' ' + _ev(_aff, _mana, _name)
        assert not _needs(_ls), __ONE_MSG__ + ' ' + _ev(_aff, _mana, _name)
    elif _kind == 'ok':
        assert not _skilled(_ls), __TYPED_AFF__ + ' ' + _ev(_aff, _mana, _name)
    else:
        assert not _skilled(_ls), __EXACT_AFF__ + ' ' + _ev(_aff, _mana, _name)
'''

_BARRIER_MANA = r'''
for _aff, _mana, _name, _kind in ((12, 4, 'Moon Step', 'low'), (12, 6, 'Moon Step', 'ok'),
                                  (12, 7, 'Ash Ward', 'low'), (12, 5, 'Moon Step', 'exact'),
                                  (12, 8, 'Ash Ward', 'exact')):
    _ls, _left, _back = _ran(_aff, _mana, _name)
    if _kind == 'low':
        assert not _skilled(_ls), __CAST_AFF__ + ' ' + _ev(_aff, _mana, _name)
        assert _needs(_ls), __TELL__ + ' ' + _ev(_aff, _mana, _name)
    elif _kind == 'ok':
        assert not _needs(_ls), __TYPED_COST__ + ' ' + _ev(_aff, _mana, _name)
    else:
        assert not _needs(_ls), __EXACT_MANA__ + ' ' + _ev(_aff, _mana, _name)
'''

_BARRIER_SPEND = r'''
for _aff, _mana, _name, _want in ((12, 15, 'Moon Step', 10), (12, 5, 'Moon Step', 0), (7, 15, 'Moon Step', 10),
                                  (12, 20, 'Ash Ward', 12), (11, 8, 'Ash Ward', 0), (6, 15, 'Moon Step', 15),
                                  (12, 4, 'Moon Step', 4), (11, 15, 'Star Fall', 15)):
    _ls, _left, _back = _ran(_aff, _mana, _name)
    if _left == _want:
        continue
    _end = ': the mana ended at ' + _lit(_left) + ', not ' + str(_want)
    assert _want != _mana, __SPEND_NOTHING__ + ' ' + _ev(_aff, _mana, _name, _end)
    if _left == _mana:
        assert _back != _want, __STORE_BACK__ + ' ' + _ev(_aff, _mana, _name, _end)
        assert False, __SUBTRACT__ + ' ' + _ev(_aff, _mana, _name, _end)
    assert False, __OWN_COST__ + ' ' + _ev(_aff, _mana, _name, _end)
'''

_BARRIER_CALL_CHECK = r'''
_calls_here = [_c for _n in _ast.parse(_source).body if type(_n).__name__ != 'FunctionDef'
               for _c in _ast.walk(_n) if type(_c).__name__ == 'Call' and type(_c.func).__name__ == 'Name'
               and _c.func.id == 'cast_spell']
assert _calls_here, __CALL__
'''

BARRIER_MSGS = dict(
    no_def="Write the recipe: `def cast_spell(caster, spell_name):`, with its lines indented under it.",
    not_def="`cast_spell` should be a recipe: `def cast_spell(caster, spell_name):`.",
    two="Give `cast_spell` two ingredients, `caster` and `spell_name`, in that order.",
)


def barrier_check(label, template, **messages):
    return (label, dx(BARRIER_SETUP) + fill(_BARRIER, **BARRIER_MSGS) + fill(template, **messages))


_SPEND_NOTHING_MSG = "Spend nothing when the caster can't cast: keep the subtraction in the last `else`."

BARRIER_FROM_BLANK = dict(
    kind="challenge",
    id="barrier-from-blank",
    title="The Barrier, From Blank",
    level="advanced",
    optional=True,
    minutes=10,
    support="light",
    summary="Write the whole `cast_spell` recipe from a blank page, the way the campaign's barrier worked.",
    martu=(
        "The barrier, from a blank page. You have every piece now: `not in`, two keys in a row, `if` / `elif` / "
        "`else`, and a change by key. Write `cast_spell(caster, spell_name)`:\n"
        "1. If the name is not in the caster's `\"spell_book\"`, print a message.\n"
        "2. Otherwise, read the spell from the book.\n"
        "3. If the affinity is lower than the spell's `\"required_affinity\"`, say they are not skilled enough.\n"
        "4. Else, if the mana is lower than its `\"mana_cost\"`, say it needs more mana.\n"
        "5. Else, subtract the cost from `caster[\"mana\"]`.\n"
        "Your recipe changes the sheet it is handed, as the campaign's did. My check calls it with other casters "
        "and other spells, only inside the check."
    ),
    setup=BARRIER_SETUP,
    names=["cast_spell", "caster", "spell_name", "spell"],
    starter=BARRIER_STARTER,
    checkpoints=[
        dict(
            id="missing-spell",
            text=(
                "Write `def cast_spell(caster, spell_name):`. If the name is not in the caster's `\"spell_book\"`, "
                "print a message."
            ),
            dictated=True,
            hints=[
                "The recipe gets a caster's sheet and a name. Ask the sheet's `\"spell_book\"` about the name "
                "first, the campaign's way.",
                "`if item not in pack:` asks a dictionary about a key before anything reads it, so a missing key "
                "never stops Python.",
                "Start with `def cast_spell(caster, spell_name):`, then the `not in` question, indented under it.",
            ],
            checks=[
                barrier_check(
                    "a name that is not in the book gets a message", _BARRIER_MISSING,
                    ask_first="Ask first, `if spell_name not in caster[\"spell_book\"]:`, so a name that is not in "
                              "the book stops there.",
                    say_missing="Print a message, such as `No such spell.`, when the name is not in the book.",
                    spend_nothing=_SPEND_NOTHING_MSG,
                ),
            ],
        ),
        dict(
            id="not-skilled",
            text=(
                "Otherwise, read the spell from the book. If the caster's affinity is lower than the spell's "
                "`\"required_affinity\"`, print that they are not skilled enough."
            ),
            dictated=False,
            hints=[
                "Read the spell from the caster's own book, by the name. The affinity is inside `\"abilities\"`; "
                "what the spell needs is on its page.",
                "`thing = pack[item]` reads one page by a key kept in a variable. Then `if thing[\"weight\"] > "
                "strength:` compares a value from that page.",
                "Write `else:` lined up with the `if`, then `spell = caster[\"spell_book\"][spell_name]` under it, then "
                "an `if` that asks whether the affinity is lower than `spell[\"required_affinity\"]`.",
            ],
            checks=[
                barrier_check(
                    "too little affinity is turned away, exactly enough is not", _BARRIER_AFF,
                    own_book="Ask the caster's own book, `caster[\"spell_book\"]`, about the name: this spell is "
                             "in it, and your recipe answered as if it were not.",
                    aff_first="Test the affinity first: this caster is short of both, and the affinity comes "
                              "first.",
                    turn_away="When the caster's affinity is lower than the spell's `\"required_affinity\"`, print "
                              "that they are not skilled enough. Read both from the sheets, not a typed number.",
                    one_msg="Keep one chain, `if` / `elif` / `else`, so only one message prints.",
                    typed_aff="Compare with the spell's own `\"required_affinity\"`, not a typed number: this "
                              "caster is skilled enough.",
                    exact_aff="Exactly enough affinity still casts: it is not lower. Use `<`, not `<=`.",
                ),
            ],
        ),
        dict(
            id="needs-mana",
            text=(
                "Else, if the caster's mana is lower than the spell's `\"mana_cost\"`, print that they need more "
                "mana."
            ),
            dictated=False,
            hints=[
                "One more question before the cast: is the mana on the big sheet lower than the spell's cost?",
                "`elif` only asks when the `if` above was false: `elif coins < price:` after a first test.",
                "Write an `elif` under the affinity branch that compares `caster[\"mana\"]` with "
                "`spell[\"mana_cost\"]`, with its message under it.",
            ],
            checks=[
                barrier_check(
                    "too little mana is told, exactly enough is not", _BARRIER_MANA,
                    cast_aff="This caster is skilled enough, so only the mana message should print.",
                    tell="When the caster's mana is lower than the spell's `\"mana_cost\"`, print that they need "
                         "more mana. Read both from the sheets, not a typed number.",
                    typed_cost="Compare with the spell's own `\"mana_cost\"`, not a typed number: this caster has "
                               "enough mana.",
                    exact_mana="Exactly enough mana still casts: it pays the whole cost. Use `<`, not `<=`.",
                ),
            ],
        ),
        dict(
            id="cast-it",
            text="Else, subtract the spell's `\"mana_cost\"` from `caster[\"mana\"]`. Exactly enough still casts.",
            dictated=False,
            hints=[
                "The last `else` is the cast: read the old mana, take the spell's cost away, and store it back.",
                "`hero[\"mana\"] = hero[\"mana\"] - cost` reads the old mana on the right and stores the new one on "
                "the left.",
                "Write `else:` lined up with the `elif`, then `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]` "
                "under it.",
            ],
            checks=[
                barrier_check(
                    "a cast spends the spell's own cost, and only a cast", _BARRIER_SPEND,
                    spend_nothing=_SPEND_NOTHING_MSG,
                    store_back="Store it back in the sheet, `caster[\"mana\"] = ...`: the recipe handed the new mana "
                               "back, and the sheet kept the old one.",
                    subtract="In the last `else`, subtract the spell's cost from `caster[\"mana\"]`, by key.",
                    own_cost="Take the spell's own `\"mana_cost\"` from `caster[\"mana\"]`, once, not a typed number.",
                ),
            ],
            pass_line="Gearshift: Barrier's holding. Every line yours.",
        ),
        dict(
            id="call-it",
            text="Below the recipe, call `cast_spell` once, with `caster` and a spell from its book.",
            dictated=False,
            hints=[
                "Below the recipe and not indented: one call, with the game's `caster` and a name from its book.",
                "`latch_check(11)` runs a recipe once. A recipe that changes a sheet does its work when it is "
                "called.",
                "Write `cast_spell(caster, \"Lantern Ward\")` below the recipe, then `print(caster[\"mana\"])` to "
                "see the change.",
            ],
            checks=[
                ("cast_spell is called below the recipe", dx(BARRIER_SETUP) + fill(
                    _BARRIER_CALL_CHECK,
                    call="Call your recipe once, below it and not indented: `cast_spell(caster, ...)`, with a "
                         "spell name from the book.",
                )),
            ],
            pass_line="Mar'tu: From a blank page. That is the whole spell, yes?",
        ),
    ],
    solution=BARRIER_SOLUTION,
    partials=[
        _barrier(read="", aff="", mana="", spend="", call=""),
        _barrier(mana="", spend="", call=""),
        _barrier(spend="", call=""),
        _barrier(call=""),
    ],
    assemble=dict(
        lines=[line for line in BARRIER_SOLUTION.splitlines() if line.strip()],
        distractors=[
            '    if spell_name in caster["spell_book"]:',
            '        if caster["magical_affinity"] < spell["required_affinity"]:',
            '            caster["mana"] = caster["mana"] - 6',
        ],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The campaign's order",
            text=(
                "1. Ask the book: `not in` first.\n"
                "2. Read the spell: the book, by the name.\n"
                "3. Compare the affinity: `<`.\n"
                "4. `elif`: compare the mana.\n"
                "5. `else`: take the cost from the mana, by key."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "`hold-the-barrier` handed you this recipe with its `not in` question already written, and you "
                "filled in the chain. The campaign stopped after the message with `return`; an `else` does the "
                "same job here. Can they cast? was the chain on its own."
            ),
        ),
        dict(
            angle="picture",
            label="Doors in doors",
            text=(
                "```text\nname not in book? --> message\n  else: read the spell\n    affinity low? --> not skilled\n"
                "    mana low? -----> more mana\n    else: spend the cost\n```\n"
                "Python takes the first door that opens, and only that one."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet="def cast_spell(caster, spell_name):",
        why=(
            "You have seen this recipe in `hold-the-barrier`: the game handed it a caster and a spell's name, and it "
            "changed the caster's mana. Now every line of it is yours."
        ),
    ),
    takeaway="A recipe can change the sheet it is handed: ask `not in`, read the spell, then `if` / `elif` / `else`.",
    wrong_answers=[
        dict(why="the starter (only the comment)", code=BARRIER_STARTER, fails_at=1,
             message_contains="Write the recipe"),
        dict(why="no `not in` question: the spell read first (KeyError on a name that is not in the book)",
             code=_barrier(guard='    if False:\n        print("No such spell.")\n'), fails_at=1,
             message_contains="Ask first"),
        dict(why="nothing printed for a missing name",
             code=_barrier(guard='    if spell_name not in caster["spell_book"]:\n'
                                 '        caster["mana"] = caster["mana"]\n'),
             fails_at=1, message_contains="Print a message"),
        dict(why="one ingredient only", code='def cast_spell(spell_name):\n    print("No such spell.")\n',
             fails_at=1, message_contains="two ingredients"),
        dict(why="the guard asks a typed list of the game's names, not the caster's book",
             code=_barrier(guard='    if spell_name not in ["Glow", "Lantern Ward"]:\n'
                                 '        print("No such spell.")\n'),
             fails_at=2, message_contains="caster's own book"),
        dict(why="the game's caster read inside the recipe (the ingredient is called hero)",
             code=_barrier(head="def cast_spell(hero, spell_name):\n"), fails_at=2,
             message_contains="caster's own book"),
        dict(why="a skipped level: caster[\"magical_affinity\"] (the student's own call stops with a KeyError)",
             code=_barrier(aff=BARRIER_AFF.replace('caster["abilities"]["magical_affinity"]',
                                                   'caster["magical_affinity"]')), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the same skipped level before any call (the check's own call names the slip)",
             code=_barrier(aff=BARRIER_AFF.replace('caster["abilities"]["magical_affinity"]',
                                                   'caster["magical_affinity"]'), call=""), fails_at=2,
             message_contains="Mend this slip in the recipe: KeyError: 'magical_affinity'"),
        dict(why="a typed affinity (Lantern Ward's 9)",
             code=_barrier(aff=BARRIER_AFF.replace('spell["required_affinity"]', "9")), fails_at=2,
             message_contains="not a typed number"),
        dict(why="<= in the affinity test (exactly enough turned away)",
             code=_barrier(aff=BARRIER_AFF.replace(" < ", " <= ")), fails_at=2,
             message_contains="Exactly enough affinity"),
        dict(why="the mana asked before the affinity",
             code=_barrier(aff=BARRIER_MANA.replace("elif", "if"), mana=BARRIER_AFF.replace("if", "elif", 1)),
             fails_at=2, message_contains="affinity first"),
        dict(why="two ifs instead of if / elif (both messages print)",
             code=_barrier(mana=BARRIER_MANA.replace("elif", "if")), fails_at=2, message_contains="Keep one chain"),
        dict(why="a typed cost in the mana test (Lantern Ward's 6)",
             code=_barrier(mana=BARRIER_MANA.replace('spell["mana_cost"]', "6")), fails_at=3,
             message_contains="not a typed number"),
        dict(why="<= in the mana test (exactly enough told it needs more)",
             code=_barrier(mana=BARRIER_MANA.replace(" < ", " <= ")), fails_at=3,
             message_contains="Exactly enough mana"),
        dict(why="a typed cost subtracted (CMB)",
             code=_barrier(spend=BARRIER_SPEND.replace('spell["mana_cost"]', "6")), fails_at=4,
             message_contains="not a typed number"),
        dict(why="the new mana handed back with return, never stored",
             code=_barrier(spend='        else:\n            return caster["mana"] - spell["mana_cost"]\n'),
             fails_at=4, message_contains="handed the new mana back"),
        dict(why="the subtraction outside the chain (a warning still spends)",
             code=_barrier(spend='        caster["mana"] = caster["mana"] - spell["mana_cost"]\n'), fails_at=4,
             message_contains="Spend nothing"),
        dict(why="never called", code=_barrier(call=""), fails_at=5, message_contains="Call your recipe"),
    ],
    notes=(
        meta(starter_level="S0", path="pool", skills="dict-in,dict-nested,dict-write,boundary,elif-chain,def",
             solo="false", dictates="1",
             foreign_names="item,pack,thing,weight,strength,coins,price,hero,cost,latch_check",
             campaign_link="hold-the-barrier", par="fresh sheets: Pell at affinity 6-12, Moon Step (5, 7), "
                                                   "Ash Ward (8, 11), Star Fall (not in the book)") + "\n"
        "Optional advanced challenge (teacher's ruling, for ready-to-stretch students; 10 min, costs no one core "
        "time), after the project. The editor starts with only a comment; setup gives the campaign-shaped "
        "`caster` (Gearshift, mana 20, affinity 10, a book of Glow and Lantern Ward). One Learn sentence says the "
        "recipe changes the sheet it is handed, as hold-the-barrier's `cast_spell` did. Every check calls "
        "`cast_spell` inside the check with fresh sheets for an invented caster, Pell, and two spells the game's "
        "caster never has (Moon Step and Ash Ward), so the values never collide with the student's own call: a "
        "name that is not in the book (no crash, a message, nothing spent), exactly enough affinity and exactly "
        "enough mana (still casts), too little of each (nothing spent), a caster short of both (the affinity "
        "comes first), and a typed affinity or cost (fails: two spells with different numbers). Lines are matched "
        "by their words, as cast_cases does ('skilled' with a no-word, 'more mana'). A guard that asks a typed "
        "list or the game's own `caster` answers Moon Step as missing and gets 'ask the caster's own book'. The "
        "ladder: Where to look, Teach with other names, then a Show that gives only the `def` line for step 1. "
        "The solution's nested `else` stands in for the campaign's early `return`."
    ),
)

# =============================================================================================
# Extra practice 5X (pool): 4A-T write-by-key-again, 4B-T store-by-name-again
# =============================================================================================

SPEND_STARTER = (
    "oogrish = {\n"
    '    "name": "Oogrish",\n'
    '    "mana": 18,\n'
    "}\n"
    "ward_cost = 5\n"
    "\n"
    "# Oogrish casts a ward. Take\n"
    "# ward_cost from his mana, by key.\n"
    "\n"
    'print(oogrish["mana"])\n'
)
SPEND_LINE = 'oogrish["mana"] = oogrish["mana"] - ward_cost\n'


def _spend(line=SPEND_LINE):
    return SPEND_STARTER.replace("by key.\n\n", "by key.\n" + line + "\n")


_SPEND_STATE = r'''
assert type(globals().get('oogrish')).__name__ == 'dict', _keep('oogrish')
_x = _near(oogrish, 'mana')
assert _x is None, '`oogrish` has a key ' + _lit(_x) + '. The sheet' + chr(39) + 's key is `"mana"`, letter for letter.'
_m = oogrish.get('mana')
assert type(_m).__name__ == 'int', 'Keep the mana a number, with no quotes.'
assert _m != 18, __STILL__
assert _m != 5, __SET_TO_COST__
assert _m == 13, __WRONG__ + ' It is ' + str(_m) + ' now, not 13.'
'''

_SPEND_FOLLOW = r'''
for _anchor, _line, _want in (('ward_cost', 'ward_cost = 3', 15), ('oogrish', 'oogrish["mana"] = 11', 6)):
    _tried = '`' + _line + '`'
    _ns, _ls, _err, _miss = _rerun([(_anchor, _line)])
    assert not _miss, _keep(_anchor)
    assert not _err, _stop(_err, _tried)
    _got = _get(_ns.get('oogrish'), 'mana')
    assert _got == _want, __TYPED__ + ' ' + _did(_tried, ': his mana ended at ' + _lit(_got) + ', not ' + str(_want))
'''

WRITE_BY_KEY_AGAIN = dict(
    id="write-by-key-again",
    title="Twin: spend by key",
    martu=(
        "The same move as Gearshift's Fire Bolt, on another sheet. Read the old mana, take away the cost, and put "
        "the new mana back under the same key."
    ),
    example='jar = {"oil": 9}\nspill = 2\njar["oil"] = jar["oil"] - spill\nprint(jar["oil"])\n',
    example_output="7",
    names=["oogrish", "ward_cost"],
    starter=SPEND_STARTER,
    checkpoints=[
        dict(
            id="spend-by-key",
            text="Oogrish casts a ward. Take `ward_cost` from his mana, by key.",
            dictated=False,
            hints=[
                "Under the comment, above the `print`. The right side reads the old mana and takes away the cost.",
                "Read, change, put back: `jar[\"oil\"] = jar[\"oil\"] - spill`.",
                "Write `oogrish[\"mana\"] = oogrish[\"mana\"] - ward_cost` above `print(oogrish[\"mana\"])`.",
            ],
            checks=[
                (
                    "the ward's cost comes off his mana",
                    dx() + fill(
                        _SPEND_STATE,
                        still="Store the new mana back in the sheet: `oogrish[\"mana\"] = ...`. His mana is still 18.",
                        set_to_cost="Take the cost away from the old mana; don't set the mana to the cost.",
                        wrong="Take `ward_cost` away from the old mana, once.",
                    ),
                ),
                (
                    "the mana follows the cost and the sheet",
                    dx() + fill(
                        _SPEND_FOLLOW,
                        typed="Build it from the sheet and the variable: `oogrish[\"mana\"] - ward_cost`, not typed "
                              "numbers.",
                    ),
                ),
            ],
            pass_line="Oogrish: Thirteen left. Steady, now.",
        ),
    ],
    solution=_spend(),
    assemble=dict(
        lines=[line for line in _spend().splitlines() if line.strip() and not line.startswith("#")],
        distractors=['oogrish["mana"] = 13', 'oogrish["mana"] = ward_cost'],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Right side: `oogrish[\"mana\"]` is 18, `ward_cost` is 5, so 13.\n"
            "2. Left side: 13 goes back under `\"mana\"`.\n"
            "3. `print(oogrish[\"mana\"])` shows 13.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]` in hold-the-barrier. Same move, with the "
            "cost in a variable.")),
    ],
    takeaway="Spend by key: `oogrish[\"mana\"] = oogrish[\"mana\"] - ward_cost`.",
    wrong_answers=[
        dict(why="the starter", code=SPEND_STARTER, fails_at=1, message_contains="still 18"),
        dict(why="the answer typed (CMB)", code=_spend('oogrish["mana"] = 13\n'), fails_at=1,
             message_contains="not typed numbers"),
        dict(why="a typed cost (CMB)", code=_spend('oogrish["mana"] = oogrish["mana"] - 5\n'), fails_at=1,
             message_contains="not typed numbers"),
        dict(why="the mana set to the cost (hero[\"mana\"] = cost, not - cost)",
             code=_spend('oogrish["mana"] = ward_cost\n'), fails_at=1, message_contains="don't set the mana"),
        dict(why="dot access", code=_spend("oogrish.mana = oogrish.mana - ward_cost\n"), fails_at=0,
             message_contains="has no attribute 'mana'"),
        dict(why="round brackets", code=_spend('oogrish["mana"] = oogrish("mana") - ward_cost\n'), fails_at=0,
             message_contains="'dict' object is not callable"),
        dict(why="a capital in the key (KeyError)", code=_spend('oogrish["Mana"] = oogrish["Mana"] - ward_cost\n'),
             fails_at=0, message_contains="KeyError: 'Mana'"),
        dict(why="the sheet read by position (KeyError: 0)", code=_spend('oogrish["mana"] = oogrish[0] - ward_cost\n'),
             fails_at=0, message_contains="KeyError: 0"),
        dict(why="a new box, the sheet unchanged", code=_spend('mana = oogrish["mana"] - ward_cost\n'), fails_at=1,
             message_contains="still 18"),
        dict(why="the variable in quotes (text)", code=_spend('oogrish["mana"] = oogrish["mana"] - "ward_cost"\n'),
             fails_at=0, message_contains="unsupported operand"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="dict-write", solo="false", dictates="",
             foreign_names="jar,oil,spill", twin_of="4A-05 write-by-key (u05a)") + "\n"
        "4A-T twin, goal-only. CMB reruns with `ward_cost = 3` and with Oogrish's mana at 11, so a typed 13 or a "
        "typed 5 fails. Proves the slips: dot access, round brackets, a capital key, a position, a quoted variable."
    ),
)

BOOK_DATA = (
    "book = {\n"
    '    "Glow": {\n'
    '        "mana_cost": 2,\n'
    '        "required_affinity": 3,\n'
    "    },\n"
    "}\n"
    'spell_name = "Moss Shield"\n'
    "spell = {\n"
    '    "mana_cost": 4,\n'
    '    "required_affinity": 6,\n'
    "}\n"
)
BOOK_STARTER = (
    BOOK_DATA + "\n"
    "# 1. Store spell in book, with\n"
    "#    spell_name as the key.\n"
    "\n"
    "# 2. Print whether spell_name is\n"
    "#    a key in book.\n"
)
BOOK_STORE = "book[spell_name] = spell\n"
BOOK_ASK = "print(spell_name in book)\n"


def _book(store=BOOK_STORE, ask=BOOK_ASK):
    return (BOOK_DATA + "\n# 1. Store spell in book, with\n#    spell_name as the key.\n" + store
            + "\n# 2. Print whether spell_name is\n#    a key in book.\n" + ask)


_BOOK_STATE = r'''
assert type(globals().get('book')).__name__ == 'dict', _keep('book')
assert 'spell_name' not in book, __QUOTED_KEY__ + ' ' + _QUOTES
assert 'Glow' in book, __GLOW__
assert 'Moss Shield' in book, __STORE__
assert type(book['Moss Shield']).__name__ != 'str', __TEXT__
assert book['Moss Shield'] == spell, __SPELL__
_tried = '`spell_name = "Ember Coat"`'
_ns, _ls, _err, _miss = _rerun([('spell_name', 'spell_name = "Ember Coat"')])
assert not _miss, _keep('spell_name')
assert not _err, _stop(_err, _tried)
assert _get(_ns.get('book'), 'Ember Coat') != '(missing)', __TYPED_KEY__ + ' ' + _did(_tried, ': no Ember Coat page')
'''

_BOOK_ASK = r'''
_tests = [_n for _n in _ast.walk(_ast.parse(_source))
          if type(_n).__name__ == 'Compare' and type(_n.ops[0]).__name__ in ('In', 'NotIn')]
assert _tests, __USE_IN__
_left = _tests[-1].left
if not _said(_lines(), 'True'):
    assert not (type(_left).__name__ == 'Constant' and _left.value == 'spell_name'), __QUOTED__ + ' ' + _QUOTES
    assert not (type(_left).__name__ == 'Constant' and type(_left.value).__name__ == 'int'), __VALUE__
    assert type(_tests[-1].ops[0]).__name__ != 'NotIn', __NOT_IN__
    assert not (type(_left).__name__ == 'Name' and _left.id == 'spell_name'), __AFTER__
    assert False, __FIX__
_tried = '`spell_name = "Ember Coat"`, and a book without Glow'
_ns, _ls, _err, _miss = _rerun([('spell_name', 'spell_name = "Ember Coat"'), ('book', 'del book["Glow"]')])
assert not _err, _stop(_err, _tried)
assert _said(_ls, 'True'), __TYPED__ + ' ' + _did(_tried, ': your program printed no True')
'''

STORE_BY_NAME_AGAIN = dict(
    id="store-by-name-again",
    title="Twin: store by name",
    martu=(
        "Another page for another book. Store the spell under the name the variable holds, then ask the book "
        "whether it has that key. `in` looks only at the keys."
    ),
    example='shelf = {"Maps": 40}\ntitle = "Runes"\nshelf[title] = 12\nprint(title in shelf)\n',
    example_output="True",
    names=["book", "spell_name", "spell"],
    starter=BOOK_STARTER,
    checkpoints=[
        dict(
            id="store-the-page",
            text="Store `spell` in `book`, with `spell_name` as the key.",
            dictated=False,
            hints=[
                "Under the first comment. The key is the variable `spell_name`, with no quotes.",
                "`shelf[title] = 12` stores under whatever name `title` holds.",
                "Write `book[spell_name] = spell` under `# 1.`",
            ],
            checks=[
                (
                    "the spell is stored under the name in spell_name",
                    dx() + fill(
                        _BOOK_STATE,
                        quoted_key="`book` has a key `\"spell_name\"`: those exact letters. Take the quotes off: "
                                   "`book[spell_name]`.",
                        glow="Keep Glow in the book: add a page, don't make a new book.",
                        store="Store the spell: `book[spell_name] = spell`.",
                        text="Store the spell itself, `spell`, with no quotes.",
                        spell="Store the spell itself: `= spell` on the right side.",
                        typed_key="Use the variable as the key, `book[spell_name]`, so a new name gets a new page.",
                    ),
                ),
            ],
        ),
        dict(
            id="ask-the-book",
            text="Print whether `spell_name` is a key in `book`.",
            dictated=False,
            hints=[
                "Under the second comment. `in` asks a dictionary about its keys and shows `True` or `False`.",
                "`print(title in shelf)` asks the shelf whether it has a page called whatever `title` holds.",
                "Write `print(spell_name in book)` under `# 2.`",
            ],
            checks=[
                (
                    "True from an in test on spell_name",
                    dx() + fill(
                        _BOOK_ASK,
                        use_in="Ask with `in`: `spell_name in book` shows `True` or `False`.",
                        quoted="Take the quotes off `spell_name`: with quotes, Python asks about the text s-p-e-l-l-_-n-a-m-e.",
                        value="`in` looks only at the keys, the spell names. Ask about the name: `spell_name in book`.",
                        not_in="Ask whether it *is* in the book: `in`, not `not in`.",
                        after="Ask after the store: put the `print` below `book[spell_name] = spell`, so the page "
                              "is there to find.",
                        fix="Print whether `spell_name` is a key in `book`: `spell_name in book`.",
                        typed="Ask about the variable, `spell_name in book`, so the question follows the name.",
                    ),
                ),
            ],
            pass_line="Lucky: True. Fine. But I'm keeping track.",
        ),
    ],
    solution=_book(),
    partials=[_book(ask="")],
    assemble=dict(
        lines=[line for line in _book().splitlines() if line.strip() and not line.startswith("#")],
        distractors=['book["spell_name"] = spell', "print(spell in book)"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. `book[spell_name]`: Python looks inside `spell_name` and finds `\"Moss Shield\"`.\n"
            "2. `= spell` stores the spell on that page.\n"
            "3. `spell_name in book` asks: is `\"Moss Shield\"` a key? `True`.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`if spell_name not in caster[\"spell_book\"]:` opened `cast_spell`. It asked the book about a key, "
            "the name, never about a spell's numbers.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='if spell_name not in caster["spell_book"]:',
        why=(
            "You have seen this line open `cast_spell`. `not in` asked the caster's book whether it had a key "
            "spelled like the spell's name. Now you know it only ever looks at keys."
        ),
    ),
    takeaway="`book[spell_name] = spell` stores by name; `spell_name in book` asks about keys, never values.",
    wrong_answers=[
        dict(why="the starter", code=BOOK_STARTER, fails_at=1, message_contains="Store the spell"),
        dict(why="the variable key in quotes (KEY)", code=_book(store='book["spell_name"] = spell\n', ask=""),
             fails_at=1, message_contains='"spell_name"'),
        dict(why="the name typed as the key (CMB)", code=_book(store='book["Moss Shield"] = spell\n', ask=""),
             fails_at=1, message_contains="new name gets a new page"),
        dict(why="a new book: Glow is lost", code=_book(store="book = {spell_name: spell}\n", ask=""), fails_at=1,
             message_contains="Keep Glow"),
        dict(why="CP1 key and value swapped: book[spell] = spell_name (a sheet can't be a key)",
             code=_book(store="book[spell] = spell_name\n", ask=""), fails_at=0,
             message_contains="unhashable type: 'dict'"),
        dict(why="CP2 a value tested with in (the spell itself: in checks keys, a dict can't be one)",
             code=_book(ask="print(spell in book)\n"), fails_at=0, message_contains="unhashable type: 'dict'"),
        dict(why="CP2 a value tested with in (a cost: in checks keys, not values)",
             code=_book(ask="print(4 in book)\n"), fails_at=2, message_contains="only at the keys"),
        dict(why="CP2 the variable in quotes", code=_book(ask='print("spell_name" in book)\n'), fails_at=2,
             message_contains="Take the quotes off"),
        dict(why="CP2 the name typed (CMB)", code=_book(ask='print("Moss Shield" in book)\n'), fails_at=2,
             message_contains="follows the name"),
        dict(why="CP2 not in", code=_book(ask="print(spell_name not in book)\n"), fails_at=2,
             message_contains="not `not in`"),
        dict(why="CP2 True typed", code=_book(ask="print(True)\n"), fails_at=2, message_contains="Ask with `in`"),
        dict(why="CP2 the example's Glow asked about instead (always True, so it proves nothing)",
             code=_book(ask='print("Glow" in book)\n'), fails_at=2, message_contains="follows the name"),
        dict(why="CP2 the right question asked before the store (False)",
             code=_book(store="", ask="") + "print(spell_name in book)\nbook[spell_name] = spell\n", fails_at=2,
             message_contains="Ask after the store"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="dict-write,dict-key-from-variable,dict-in", solo="false",
             dictates="", foreign_names="shelf,title,Maps,Runes", twin_of="4B-04 CP2 + its side quest") + "\n"
        "4B-T twin, goal-only. CP1: KEY (`\"spell_name\"`), Glow kept, CMB with spell_name Ember Coat. CP2: an "
        "`in` test (in the print or in a box printed after), then True, then CMB (Ember Coat, and the book's Glow "
        "page taken out, must still give True, so a typed `\"Moss Shield\" in book` or the always-true "
        "`\"Glow\" in book` fails); the right test asked before the store gets 'ask after the store'. The "
        "in-checks-keys slip is proven twice: `spell in book` (a dict value "
        "cannot be a key: unhashable) and `4 in book` (a cost is a value, not a key)."
    ),
)

EXTRA_5X = dict(
    kind="lesson",
    id="extra-sheets-and-books",
    title="Extra practice: Sheets and Books",
    optional=True,
    minutes=7,
    summary="Two short twins: spend mana by key, then store a spell by its name and ask the book about it.",
    notes="5X pool (4A-T write-by-key-again, 4B-T store-by-name-again). Optional; both twins are goal-only (ND). "
          "Feeds twins, the spaced queue and early finishers.",
    exercises=[WRITE_BY_KEY_AGAIN, STORE_BY_NAME_AGAIN],
)

ITEMS = [REMEMBERS_4B, LESSON_4B, QUIZ_4, PROJECT_4P, BARRIER_FROM_BLANK, EXTRA_5X]
