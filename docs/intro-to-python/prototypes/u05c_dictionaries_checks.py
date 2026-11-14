"""Unit 5 "Dictionaries" ("Stat Sheets and Spell Books"), part c: Quick Check 5 (the curriculum's Quick Check 4; forms A
and B: five code tasks each as testout items, three questions each that the form also needs, 2 of 3) and the cheatsheet
"Mar'tu's Chalk Notes: Dictionaries".

Spec: design/curriculum.md, "## Unit 5 · Dictionaries", items 7 and 8 (u05c): Quick Check 4 (C1 make a sheet, C2 read
`["abilities"]["wisdom"]`, C3 `book[spell_name] = spell` built from variables, Q1 `in` / `not in` on keys and on a
value, C4 mend a KeyError from a skipped level, C5 `roster[1]["name"]` then spend that hero's mana by a cost variable,
2 CPs; form B with Oogrish's sheet, a `wards` book and `roster[3]`) and the Dictionaries cheatsheet.
Introduces nothing new (concept_map.json: u05c introduces []). Dictionaries, `in` / `not in` (u05a) and lists as
Unit 4 plans them (list literals, a read by position, a list of dicts read by index; u04a) are all it uses. No loops,
no f-strings, no `None` written in code. `.get()` (u05a's optional article) shows up once, as a cheatsheet extra.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN the spell book
(`spell_book[spell_name] = spell`), the mana bars (`"█" * caster["mana"]`) and the barrier spell
(`if spell_name not in caster["spell_book"]:`, `caster["abilities"]["magical_affinity"]`,
`caster["mana"] = caster["mana"] - spell["mana_cost"]`). Campaign links are "you've seen this, now you'll get it",
and the Quick Check is framed as "it only shows Mar'tu where to start", never as a test of what they should know.
Every student has their own device; every task here is solo.

Deviations from the spec, each small and noted on its exercise:
  * The Unit 5 ruling ("an honest fast path"): every Quick Check task the site gates on now covers a skill the
    lessons teach, so a student who tests out has done each kind of step once:
      - C2 has two checkpoints: CP1 reads `["abilities"]["wisdom"]` (the spec), CP2 (`train-inside`, goal only)
        adds 2 to that value inside the card, below the print (dict-nested write). CP1 stays true after CP2.
      - C4 is the campaign's chain (`skill = caster["magical_affinity"]`, the campaign's exact slip, kept;
        `if skill < needed:` / `elif False:` / `else:`). CP1 mends the read (the spec); CP2 (`mana-test`, goal
        only) replaces `False` with the mana test, exactly enough still casting: objective 9, get it, compare,
        act, now gated.
      - C1 opens with a three-line story recap ("Mar'tu's notes so far"), for a student who skips the lessons.
      - The forms take 14 minutes (was 12), as Unit 4's.
  * C3 has two checkpoints (build the spell, then store it) and its store step asks first, the campaign's way:
    "If `spell_name` is not in `book` yet, store `spell` ...". Reason: the site gates a Quick Check on its code tasks
    only (the Unit 2 and Unit 3 teacher rulings: the code tasks alone must cover the unit), so `dict-in` needs a
    gated task that can fail on the class's slip. The guard is exactly `if spell_name not in caster["spell_book"]:`
    (Obj 4's campaign line), and u05b's 4B-04 CP3 (`store-if-new`) now teaches it first, so the step is fair. Q1
    stays the predict the spec names.
  * The question quizzes hold three questions: the spec's Q1 plus two self-check questions, the way Units 1-3 carry
    3-4 (quotes on keys, an mc for Obj 1's reconciliation card; a key read from a variable, a predict for Obj 5).
    Since the Unit 5 ship they count, as Unit 3's do: the form needs 2 of the 3. Their right answers sit at varied
    positions.
  * C4 names its sheet `caster`, the campaign's word, so the mended chain reads like `hold-the-barrier`'s body.
  * Form B's C1 is Bomb Shell's sheet and its C2 is Oogrish's (the spec's "Oogrish's sheet"): Oogrish's
    intelligence and wisdom are both 17, so his inner card here holds dexterity, wisdom and magical affinity only.

Help ladder as fields (FORMAT.md, as u05a/u05b): hints[0] Where to look, the middle hints Teach me (a tiny example
with other names, listed in foreign_names), the last hint the step's shape. Quick Checks show no hints
(support="none"), so no hint holds the finished line. Then another_way (2 angles each) and assemble.

Check codes (curriculum 2.5), built by the helpers below. Every rerun happens inside the check only: the student's
program is parsed, a line is slipped in right after the top-level statement that makes a named variable, and the
program runs again in a fresh namespace with its prints kept private (as u05b's _rerun):
  KEY      sheet_keys() / the spell and page checks: exact keys, near misses named letter for letter
           (`"Max_Mana"`, `"max mana"`, a plural), a set (commas, no colons), a list, keys kept as variables;
           values with no keys at all, a set or a list, get u05a's "Each value needs its key in front".
  NUM/TEXT/SWAP  sheet_values() and the spell check: a quoted number, a name that is not text, swapped values, a
           value that is a quoted variable name (`"cost"`, with the quotes sentence).
  CMB      follow checks: C2 changes the wisdom inside the sheet (CP1 must print it, CP2 must end 2 higher), C3
           changes the cost, the needed affinity and the spell's name, C4 changes the affinity (CP1) and the mana
           and `cost` (CP2), C5 changes the cost, the hero's mana and the roster's order. A
           typed value (the class's "numbers in ink": A-06, A-07 test values) always fails. C3 and C5 compare
           against the student's own `cost` / `needed` when they are whole numbers, so a changed starter number is
           accepted (the reruns still prove the build follows the variables); C5 refuses `cost = 0` (nothing spent).
  KEEP     the starter's sheets stay as they are (a key moved to the outside to dodge the nested read fails); C4
           also keeps `needed`, because its rerun expects the `if` line. C2 CP1 judges the sheet's own lines, so
           CP2's write (and its slips: a flat key, another value changed) are CP2's to name.
  chain    C4 CP2: the student's own run, then reruns with the mana below `cost`, `cost` above the mana, exactly
           enough (`<=` fails) and the affinity too low (a second `if` fails: two lines print). Diagnoses from the
           test itself: `False` left, typed numbers, a typed mana or cost; the sign; an extra level is a crash.
  OUT      reads are matched as whole numbers or the name, never inside a printed dictionary or list, even after a
           label: `print("Wisdom:", card)` or `print("Roster:", roster)` gets "one value" / "only the name". C5 CP1
           also fails when another hero's name is printed (every name printed at once, the position skipped).
  guard    C3: the program runs with a name already in the book, then with a second page added (named in the
           message), then with a third page whose name no message shows, and each page must stay as it was. So a
           guard that types the names it has seen (`!= "Glow" and != "Spark"`, `not in ["Glow", "Spark"]`) fails.
           Diagnoses: no `in` / `not in` at all, `in` asked about a value (`cost`, the "in looks at values"
           belief), `"spell_name"` in quotes, `in` for `not in`, names typed in the `if`, a typed list, the store
           line left unindented under the `if` (it runs every time). The store rerun reads only the two keys, so
           a spell with an extra key (`"name": spell_name`) passes.
  roster   C5: the read goes through `roster`, position first (the reorder rerun; an AST look at the print names
           a typed name or the hero's own sheet); the spend goes through `roster` too (the reorder rerun: a
           `gearshift[...]` write pays from the wrong sheet). NEWBOX, BARE, the sign the wrong way, a near-miss
           key (`"Mana"`), another hero's mana changed.
Messages are lean, as Unit 2's QC2 and every Quick Check since (the teacher's ruling): the slip and the evidence in
brackets, never the fix or the finished line: "The spend does not follow `cost`. (Mar'tu's check tried `cost = 4`, only
inside the check: the mana went to 14, not 16.)". The helpers copied from u05b's lesson checks (`_gone`, `_stop`) go
through _leaned(), whose every rewrite must match the lesson message, and the Quick-Check-only templates are lean as
written. _lean_guard() proves both at import: no message opens with a fix ("Put a colon ...", "Read it from the sheet
..."), and no text a student reads shows a line of Mar'tu's version the starter does not (a rerun's evidence names the
value it tried, "another wisdom inside the card, 11", never the read). They use the party table's values and invented
ones only, never a student's own text (2.11).

The forms gate on their questions too (questions_to_pass=2: 2 of the 3, all but one, as QC2 gates on 3 of its 4), and
the site calls them Quick Check 5 (the unit's order on the map; the curriculum's numbering is Quick Check 4, kept in
the ids `qc4-a` and `qc4-b`).

Python's messages were checked in CPython 3.13 (the site runs 3.13): `{name: "Lucky"}` -> "name 'name' is not
defined"; `{"name" = "Lucky"}` -> "cannot assign to literal here"; a missing comma after a number -> "invalid syntax.
Perhaps you forgot a comma?" on that line, after text -> "invalid syntax" on the next line; a missing colon on a
later key -> "':' expected after dictionary key"; `hero.mana` -> "'dict' object has no attribute 'mana'";
`hero("mana")` -> "'dict' object is not callable"; `hero[0]` -> "KeyError: 0"; `roster["Gearshift"]` -> "list
indices must be integers or slices, not str"; `roster[4]` -> "list index out of range"; `spell in book` ->
"unhashable type: 'dict'"; a whole card compared with `<` -> "'<' not supported between instances of 'dict' and
'int'"; `caster["abilities"]["mana"]` -> "KeyError: 'mana'".

Phone width: fenced pictures, question code, cheatsheet code and starter lines keep to 36 characters or fewer
(checked by script). Some solution lines are longer, because the nested read or the roster spend is long
(`roster[1]["mana"] = roster[1]["mana"] - cost`); those are the campaign's own shapes.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u05c
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
LESSON_A = "Stat Sheets"
LESSON_B = "Sheets Inside Sheets"
MODULE = "friends-in-low-places"


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

_QX = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
_QUOTES = __QUOTES__
_tree = _ast.parse(_source)
_g = globals()
def _lit(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
def _did(_tried, _end=''):
    return "(Mar'tu's check tried " + _tried + ', only inside the check' + _end + '.)'
def _whole(_v):
    return r'(?<![\d.])' + _re.escape(str(_v)) + r'(?!\d)(?!\.\d)'
def _display(_l):
    return _l[:1] in '{[(' or '{' in _l or "['" in _l
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
def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]
def _squash(_s):
    return str(_s).lower().replace('_', '').replace(' ', '').replace('-', '')
def _near(_a, _b):
    if type(_a).__name__ != 'str' or _a == _b:
        return False
    _x, _y = _a.lower().strip(), _b.lower()
    return (_x == _y or _squash(_a) == _squash(_b) or _x.rstrip('s') == _y.rstrip('s')
            or (min(len(_x), len(_y)) >= 5 and _edits(_x, _y) <= 2))
def _near_key(_d, _k, _skip=()):
    if type(_d).__name__ != 'dict':
        return None
    for _x in _d:
        if _x not in _skip and _near(_x, _k):
            return _x
    return None
def _targets(_n):
    _kind = type(_n).__name__
    _ts = list(_n.targets) if _kind == 'Assign' else ([_n.target] if _kind == 'AugAssign' else [])
    return [_t.id for _t in _ts if type(_t).__name__ == 'Name']
def _made():
    _out = []
    for _n in _ast.walk(_tree):
        for _m in _targets(_n):
            if _m not in _out:
                _out.append(_m)
    return _out
def _gone(_k, _skip=(), _new=False):
    _close = [_m for _m in _made() if _m != _k and _m not in _skip and _near(_m, _k)]
    if _close:
        return ('Python matches names letter for letter: you wrote `' + _close[0] + '`, and the task needs `'
                + _k + '`.')
    if _new:
        return 'Make the variable `' + _k + '`: nothing in your program is called that yet.'
    return 'Keep the variable `' + _k + '` from the starter, on a line that starts `' + _k + ' = `.'
def _keep(_name):
    return ('Keep `' + _name + '` from the starter, made on its own line, so Mar' + chr(39) + 'tu' + chr(39)
            + 's check can try other values there.')
def _stop(_err, _tried):
    return 'Make it work for other values too. ' + _did(_tried, ', and your program stopped with ' + _err)
def _rerun(_changes):
    _body, _found = [], []
    for _n in _tree.body:
        _body.append(_n)
        _here = _targets(_n)
        for _anchor, _line in _changes:
            if _anchor in _here:
                if _anchor not in _found:
                    _found.append(_anchor)
                _body.extend(_ast.parse(_line).body)
    _mod = _ast.Module(body=_body, type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _ns = {'__name__': '__main__'}
    _out, _old, _err = _io.StringIO(), _sys.stdout, ''
    _sys.stdout = _out
    try:
        exec(compile(_mod, 'main.py', 'exec'), _ns)
    except BaseException as _e:
        _err = type(_e).__name__ + (': ' + str(_e) if str(_e) else '')
    finally:
        _sys.stdout = _old
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _err, [_a for _a, _l in _changes if _a not in _found]
def _print_calls():
    return [_c for _c in _ast.walk(_tree) if type(_c).__name__ == 'Call' and type(_c.func).__name__ == 'Name'
            and _c.func.id == 'print']
def _prints_name(_name):
    for _c in _print_calls():
        if [_x for _x in _ast.walk(_c) if type(_x).__name__ == 'Name' and _x.id == _name]:
            return True
    return False
def _prints_text(_text):
    for _c in _print_calls():
        if [_x for _x in _ast.walk(_c) if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str'
                and _text in _x.value]:
            return True
    return False
'''


def _leaned(code, pairs):
    """A Quick Check's check (a test-out, no hints): the lesson's helper messages, rewritten to name the slip and the
    evidence, never the fix (the teacher's lean ruling, as Unit 2's QC2 does). Each pair must match, so a reworded lesson
    message cannot silently leave a fix in the Quick Check."""
    for old, new in pairs:
        assert old in code, f"lean rewrite does not match: {old[:70]!r}"
        code = code.replace(old, new)
    return code


# The helpers u05c shares with u05b's lesson checks (`_gone`, `_stop`): their lesson messages name the fix ("Make the
# variable", "Make it work for other values too"), so the Quick Check says the slip and the evidence instead.
_QX_LEAN = [
    ("return 'Make the variable `' + _k + '`: nothing in your program is called that yet.'",
     "return 'Nothing in your program is called `' + _k + '` yet.'"),
    ("return 'Make it work for other values too. ' + _did(_tried, ', and your program stopped with ' + _err)",
     "return 'Other values stop your program. ' + _did(_tried, ', and your program stopped with ' + _err)"),
]


def qx():
    return _leaned(_QX.replace("__QUOTES__", repr(QUOTES_RULE)), _QX_LEAN)


def check(label, template, **values):
    """A check: the helpers, then a template filled with repr() values."""
    return (label, qx() + fill(template, **values))


# ---------------------------------------------------------------------------------------------
# The unit (the same UNIT dict in every Unit 5 part file)
# ---------------------------------------------------------------------------------------------

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

# Every term this file links ([[dictionary]], [[key]], [[KeyError]], [[TypeError]]) is defined in u05a or earlier.
GLOSSARY = []


# =============================================================================================
# Quick Check 5 (forms A and B; the curriculum's Quick Check 4)
# =============================================================================================

def _stuck(lesson):
    return f"Stuck? Skip it, or try the lesson {lesson}. Tasks you pass here stay ticked."


def _qc_meta(skills, foreign="", form="A", level="S3", dictates=""):
    return meta(starter_level=level, path="QC4", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


def _sheet_lines(var, pairs, inner=None, indent=""):
    """A sheet written one key a line (phone width). pairs: (key, code); inner: (key, [(key, code)])."""
    out = f"{indent}{var} = {{\n"
    for key, code in pairs:
        out += f"{indent}    \"{key}\": {code},\n"
    if inner:
        key, rows = inner
        out += f"{indent}    \"{key}\": {{\n"
        for k, code in rows:
            out += f"{indent}        \"{k}\": {code},\n"
        out += f"{indent}    }},\n"
    out += f"{indent}}}\n"
    return out


# ---- C1: make a sheet (dict-make) ----

# The story so far, for a student who tests out of Unit 5 (the Unit 5 ruling): C1 opens with it in both forms.
_NOTES_SO_FAR = ("Mar'tu's notes so far: Gearshift's tank holds starlode. Lantern Ward is in the spell book. The "
                 "barrier holds again.")

SHEET_KEYS = ["name", "magical_affinity", "max_mana", "armor_bonus"]

_SHEET_KEYS = r'''
_name = __NAME__
_want = __KEYS__
_v = _g.get(_name)
_msg = ''
# Values only, no keys at all (as u05a): `{"Lucky", 13, 26, 3}` (a set) or `["Lucky", 13, 26, 3]` (a list).
_no_keys = type(_v).__name__ in ('set', 'list', 'tuple') and not [_k for _k in _want if _k in _v]
if _name not in _g:
    _msg = _gone(_name)
elif _no_keys:
    _msg = 'Your sheet has values but no keys.'
elif type(_v).__name__ == 'set':
    _msg = '`' + _name + '` has commas but no colons, so it is not a dictionary.'
elif type(_v).__name__ in ('list', 'tuple'):
    _msg = '`' + _name + '` has square brackets, so it is a list, not a dictionary.'
elif type(_v).__name__ != 'dict':
    _msg = '`' + _name + '` does not hold a dictionary.'
elif not _v:
    _msg = 'The sheet is still empty.'
else:
    for _k in _want:
        if _k in _v:
            continue
        _x = _near_key(_v, _k, _want)
        if _x is not None:
            _msg = '`' + _name + '` has a key `' + _lit(_x) + '`, and the card spells it `"' + _k + '"`.'
        elif _k in _g and not _k.startswith('_'):
            _msg = '`' + _k + '` is a variable of its own, outside the sheet.'
        else:
            _msg = '`' + _name + '` has no key `"' + _k + '"` yet.'
        break
assert not _msg, _msg
'''

_SHEET_VALUES = r'''
_name = __NAME__
_wants = __WANTS__
_v = _g.get(_name)
_nums = dict((_k, _w) for _k, _w in _wants if _w != 'text')
_msg = ''
for _k, _w in _wants:
    _at = '`' + _name + '["' + _k + '"]`'
    _x = _v[_k]
    _t = type(_x).__name__
    if _w == 'text':
        if _t in ('int', 'float'):
            _msg = _at + ' holds a number, and a name is text.'
        elif _t != 'str':
            _msg = _at + ' does not hold text.'
        elif not _x.strip():
            _msg = _at + ' is empty text.'
    elif _t == 'str':
        if _x.strip().lstrip('+-').isdigit():
            _msg = _at + ' holds the text `"' + _x + '"`, not a number.'
        else:
            _msg = _at + ' holds text, and the card has a number.'
    elif _t != 'int':
        _msg = _at + ' holds ' + _lit(_x) + ', not a whole number.'
    elif _x != _w:
        _swap = [_o for _o, _ow in _nums.items() if _o != _k and _ow == _x]
        if _swap:
            _msg = ('Two values may be swapped: ' + _at + ' holds ' + str(_x)
                    + ', the card' + chr(39) + 's `"' + _swap[0] + '"` value.')
        else:
            _msg = _at + ' holds ' + str(_x) + ', and the card says ' + str(_w) + '.'
    if _msg:
        break
assert not _msg, _msg
'''


def _qc_sheet(form, var, who, values, foreign_var, pass_line):
    affinity, max_mana, armor = values

    def program(lines=None, name=f"\"{who}\"", aff=str(affinity), mx=str(max_mana), arm=str(armor), head=None,
                body=None):
        if body is None:
            if lines is None:
                lines = [f"    \"name\": {name},", f"    \"magical_affinity\": {aff},", f"    \"max_mana\": {mx},",
                         f"    \"armor_bonus\": {arm},"]
            body = f"{var} = {{\n" + "".join(line + "\n" for line in lines) + "}\n"
        return (head if head is not None else HEAD) + body

    HEAD = f"# {who}'s sheet. Copy each key\n# from the card, letter for letter.\n"
    starter = program(body=f"{var} = {{\n}}\n")
    solution = program()
    good = [f"    \"name\": \"{who}\",", f"    \"magical_affinity\": {affinity},", f"    \"max_mana\": {max_mana},",
            f"    \"armor_bonus\": {armor},"]
    card = (
        "```text\n"
        f"{who.upper()}\n"
        f"name              {who}\n"
        f"magical_affinity  {affinity}\n"
        f"max_mana          {max_mana}\n"
        f"armor_bonus       {armor}\n"
        "```"
    )
    return dict(
        id="make-the-sheet",
        title="Make a sheet",
        # The recap opens the task (the Unit 5 ruling), and the same first line ends with a colon, so "Keep it
        # short" shows the card under it too (the player keeps a code block a first line introduces).
        martu=(
            _NOTES_SO_FAR + f" Make {who}'s sheet, a [[dictionary]], from this card:\n" + card + "\n"
            "Use the four keys on the card, with the values beside them. Copy each key exactly.\n" + _stuck(LESSON_A)
        ),
        names=[var],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="the-sheet",
                text=f"Make `{var}` with the card's four keys and {who}'s values.",
                dictated=False,
                hints=[
                    "Look at the card: four keys, each with its value. Text goes in quotes, numbers don't.",
                    f"Each line inside the curly brackets is a key in quotes, a colon, a value and a comma: "
                    f"`\"{foreign_var}\": 6,`.",
                    "The keys are text, so each one has quotes. A box's name never does. " + QUOTES_RULE,
                ],
                checks=[
                    check(f"{var} has the four keys", _SHEET_KEYS, name=var, keys=SHEET_KEYS),
                    check("the values match the card", _SHEET_VALUES, name=var,
                          wants=[["name", "text"], ["magical_affinity", affinity], ["max_mana", max_mana],
                                 ["armor_bonus", armor]]),
                ],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[f"{var} = {{", *good, "}"],
            distractors=[f"    name: \"{who}\",", f"    \"max_mana\" = {max_mana},", f"    \"Max_Mana\": {max_mana},"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `{var} = {{` opens the sheet.\n2. One line for each key on the card: the key in quotes, `:`, "
                "the value, `,`.\n3. `}` closes it.")),
            dict(angle="why", label="Wait, quotes on names?", text=(
                "A box's name (a variable) never has quotes: `mana = 26`. A key is text inside the sheet, so it "
                "does: `{\"mana\": 26}`. " + QUOTES_RULE)),
        ],
        campaign_link=dict(
            module=MODULE,
            part="spell-book",
            snippet='spell = {\n    "mana_cost": 0,\n    "required_affinity": 0,\n}',
            why=(
                "You have seen this. The spell book part had a dictionary like yours: a key in quotes, a colon and "
                "a value on every line. Now you write one from nothing."
            ),
        ),
        takeaway="A sheet is `{ }` holding `\"key\": value` lines with commas. Keys are text, so they have quotes.",
        wrong_answers=[
            dict(why="the starter (the empty sheet)", code=starter, fails_at=1, message_contains="still empty"),
            dict(why="a key with no quotes (box names have no quotes, keys do; A-02 names in quotes, the other way)",
                 code=program(lines=[f"    name: \"{who}\","] + good[1:]), fails_at=0,
                 message_contains="name 'name' is not defined"),
            dict(why="every key unquoted", code=program(lines=[line.replace('"', "", 2) for line in good]), fails_at=0,
                 message_contains="is not defined"),
            dict(why="= for : inside the sheet (the box habit)",
                 code=program(lines=[f"    \"name\" = \"{who}\","] + good[1:]), fails_at=0,
                 message_contains="cannot assign to literal"),
            dict(why="a missing comma after a text value: Python names the NEXT line",
                 code=program(lines=[f"    \"name\": \"{who}\""] + good[1:]), fails_at=0,
                 message_contains="invalid syntax"),
            dict(why="a missing comma after a number: Python names that line ('forgot a comma')",
                 code=program(lines=good[:2] + [f"    \"max_mana\": {max_mana}"] + good[3:]), fails_at=0,
                 message_contains="forgot a comma"),
            dict(why="a missing colon on a later key",
                 code=program(lines=good[:2] + [f"    \"max_mana\" {max_mana},"] + good[3:]), fails_at=0,
                 message_contains="':' expected after dictionary key"),
            dict(why="= for : on a later key (there 3.13 says ':' expected, not 'cannot assign')",
                 code=program(lines=good[:2] + [f"    \"max_mana\" = {max_mana},"] + good[3:]), fails_at=0,
                 message_contains="':' expected after dictionary key"),
            dict(why="key capitals: Max_Mana (KEY)", code=solution.replace('"max_mana"', '"Max_Mana"'), fails_at=1,
                 message_contains='"Max_Mana"'),
            dict(why="a space for _ in a key (KEY)", code=solution.replace('"armor_bonus"', '"armor bonus"'),
                 fails_at=1, message_contains='the card spells it `"armor_bonus"`'),
            dict(why="a key with a typo (KEY)", code=solution.replace('"magical_affinity"', '"magic_affinity"'),
                 fails_at=1, message_contains='"magic_affinity"'),
            dict(why="commas but no colons: a set, not a dictionary (the keys are in it)",
                 code=program(body=f"{var} = {{\"name\", \"{who}\", \"max_mana\", {max_mana}}}\n"), fails_at=1,
                 message_contains="no colons"),
            dict(why="values only, in curly brackets: a set with no keys (as u05a)",
                 code=program(body=f"{var} = {{\"{who}\", {affinity}, {max_mana}, {armor}}}\n"), fails_at=1,
                 message_contains="values but no keys"),
            dict(why="a list of the four values, no keys (the list habit, Unit 4; as u05a)",
                 code=program(body=f"{var} = [\"{who}\", {affinity}, {max_mana}, {armor}]\n"), fails_at=1,
                 message_contains="values but no keys"),
            dict(why="a list that holds the keys and values (square brackets, the list habit)",
                 code=program(body=f"{var} = [\"name\", \"{who}\", \"max_mana\", {max_mana}]\n"), fails_at=1,
                 message_contains="it is a list"),
            dict(why="separate boxes instead of keys (box versus key)",
                 code=program(body=f"name = \"{who}\"\nmax_mana = {max_mana}\n{var} = {{\n    \"armor_bonus\": {armor},\n}}\n"),
                 fails_at=1, message_contains="variable of its own"),
            dict(why="a capital in the sheet's name (NAME)", code=solution.replace(f"{var} = {{", f"{var.capitalize()} = {{"),
                 fails_at=1, message_contains="letter for letter"),
            dict(why="a number in quotes (NUM)", code=program(mx=f"\"{max_mana}\""), fails_at=1,
                 message_contains="not a number"),
            dict(why="affinity and max mana swapped (SWAP)", code=program(aff=str(max_mana), mx=str(affinity)),
                 fails_at=1, message_contains="swapped"),
            dict(why="a wrong number", code=program(arm=str(armor + 1)), fails_at=1, message_contains="the card says"),
            dict(why="the name with no quotes (A-05/A-08 unquoted text)", code=program(name=who.replace(" ", "_")),
                 fails_at=0, message_contains="is not defined"),
            # Two words with no quotes: Python reads them side by side (the explainer's bare-words row, Unit 5 words).
            *([dict(why="the two-word name with no quotes (a space, so 'forgot a comma')", code=program(name=who),
                    fails_at=0, message_contains="Perhaps you forgot a comma")] if " " in who else []),
            dict(why="the name as a number", code=program(name="7"), fails_at=1, message_contains="A name is text"),
            dict(why="empty text for the name", code=program(name='""'), fails_at=1, message_contains="empty text"),
            dict(why="a key missing", code=program(lines=good[:3]), fails_at=1, message_contains='"armor_bonus"'),
        ],
        notes=_qc_meta("dict-make", foreign_var, form, level="S3") + "\n"
        f"QC4 C1, form {form}: {who}'s sheet from the party table ({affinity}, {max_mana}, {armor}). One checkpoint, "
        "goal only: KEY first (near misses named letter for letter; a set, a list, keys kept as variables, the empty "
        "starter; values with no keys at all, a set or a list, get 'Each value needs its key in front', as u05a), "
        "then NUM / TEXT / SWAP against the card. The Learn pane opens with Mar'tu's three-line story recap (the "
        "Unit 5 ruling: a student who tests out still meets the starlode, Lantern Ward and the barrier). Any "
        "non-empty text passes for the name (lint e: \"Captain Glug\" passes); the three numbers are the card's. "
        "Fails on (spec): `\"Max_Mana\"` -> KEY; `{name: ...}` -> NameError (crash). Also the class's other "
        "dict-literal slips: `=` for `:`, a missing comma (after a number: that line, 'forgot a comma'; after "
        "text: the next line), a missing colon, a quoted number (NUM), swapped values. support='none', "
        "explainer='lean'.",
    )


# ---- C2: read inside a sheet (dict-nested, dict-read) ----

_KEEP_SHEET = r'''
_name = __NAME__
_want = __SHEET__
_ik, _train = __INNER__, __TRAIN__
if _name not in _g:
    assert False, _gone(_name)
_v = _g.get(_name)
# With a write step after this one (C2 CP2), this step judges the sheet's own lines: what a write line does to
# the sheet later is that step's to judge, and so is the value it changes.
if _train:
    for _n in _tree.body:
        if type(_n).__name__ == 'Assign' and _name in _targets(_n):
            try:
                _v = _ast.literal_eval(_n.value)
            except Exception:
                pass
            break
assert type(_v).__name__ == 'dict', '`' + _name + '` should still hold the sheet from the starter.'
_out = [_k for _k in _v if _k in _want[_ik]]
assert not _out, ('Keep the sheet as the starter has it: the sheet now has `"' + _out[0] + '"` on the outside.')
_cmp = dict(_v)
if _train and type(_cmp.get(_ik)).__name__ == 'dict' and _train in _cmp[_ik]:
    _cmp[_ik] = dict(_cmp[_ik])
    _cmp[_ik][_train] = _want[_ik][_train]
assert _cmp == _want, 'Keep the sheet as the starter has it: its lines changed.'
'''

# C2's value inside the card, in the student's run or a rerun's namespace (None when it is not a whole number).
_CARD_VALUE = r'''
def _card_value(_ns):
    _s = _ns.get(__NAME__)
    _c = _s.get(__INNER__) if type(_s).__name__ == 'dict' else None
    _x = _c.get(__KEY__) if type(_c).__name__ == 'dict' else None
    return _x if type(_x).__name__ == 'int' else None
'''

# CP1 accepts the value before or after CP2's +2: the value the card holds when the line prints is the read.
_READ = _CARD_VALUE + r'''
_ls = _lines()
_msg = ''
_ok = [__WANT__] + [_x for _x in [_card_value(_g)] if _x is not None]
if not [_x for _x in _ok if _shows(_ls, _x)]:
    if [_l for _l in _ls if _display(_l)]:
        _msg = __WHOLE__
    for _v, _m in __NEAR__:
        if not _msg and _shows(_ls, _v):
            _msg = _m
    _msg = _msg or __FIX__
assert not _msg, _msg
'''

_FOLLOW = _CARD_VALUE + r'''
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, __TRIED__)
_ok = [__NEW__] + [_x for _x in [_card_value(_ns)] if _x is not None]
if not [_x for _x in _ok if _shows(_ls, _x)]:
    assert not _shows(_ls, __OLD__), __TYPED__ + ' ' + _did(__TRIED__, ': your program still printed ' + _lit(__OLD__))
    assert False, __FIX__ + ' ' + _did(__TRIED__)
'''

_TRAIN = r'''
_name, _ik, _k, _start, _label = __NAME__, __INNER__, __KEY__, __START__, __WHAT__
_want = __SHEET__
_v = _g.get(_name)
if _name not in _g:
    assert False, _gone(_name)
assert type(_v).__name__ == 'dict', '`' + _name + '` should still hold the sheet from the starter.'
_c = _v.get(_ik)
assert type(_c).__name__ == 'dict', 'Keep `"' + _ik + '"` inside the sheet, as the starter has it.'
assert _k not in _v, 'Your line made a new `"' + _k + '"` key on the outside of the sheet.'
_x = _near_key(_c, _k, list(_want[_ik]))
assert _x is None, ('The card now has a key `' + _lit(_x) + '` too, and its `"' + _k + '"` is still '
                    + _lit(_c.get(_k)) + '.')
assert _k in _c, 'Keep `"' + _k + '"` inside `"' + _ik + '"`, as the starter has it.'
_others = ([_o for _o in _want if _o != _ik and _v.get(_o) != _want[_o]]
           + [_o for _o in _want[_ik] if _o != _k and _c.get(_o) != _want[_ik][_o]])
_x = _c[_k]
if _x == _start:
    _box = [_m for _m in _made() if _m != _name and _g.get(_m) == _start + 2]
    _bare = [_n for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
    if _others:
        _msg = ('Your line changed `"' + _others[0] + '"`, and the ' + _label + ' is still ' + str(_start) + '.')
    elif _box:
        _msg = ('Your variable `' + _box[0] + '` holds ' + str(_start + 2) + ', and the card still says '
                + str(_start) + '.')
    elif _bare:
        _msg = ('Your line works out the new ' + _label + ', then forgets it. The card still says ' + str(_start)
                + '.')
    else:
        _msg = 'The ' + _label + ' inside the card is still ' + str(_start) + '.'
    assert False, _msg
assert not _others, '`"' + _others[0] + '"` changed too, as well as the ' + _label + '.'
assert type(_x).__name__ == 'int', 'The ' + _label + ' holds ' + _lit(_x) + ', not a whole number.'
assert _x != _start - 2, 'The ' + _label + ' went down to ' + str(_x) + '.'
assert _x == _start + 2, 'The ' + _label + ' is ' + str(_x) + ' now, and it started at ' + str(_start) + '.'
'''

_TRAIN_FOLLOW = _CARD_VALUE + r'''
_tried, _new, _start, _label = __TRIED__, __NEW__, __START__, __WHAT__
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
_x = _card_value(_ns)
if _x != _new + 2:
    _end = ': the ' + _label + ' became ' + _lit(_x) + ', not ' + str(_new + 2)
    assert _x != _new, ('The ' + str(_start) + ' in the sheet was edited, so the card does not follow. '
                        + _did(_tried, _end))
    assert _x != _start + 2, ('The new ' + _label + ' is a typed number. ' + _did(_tried, _end))
    assert False, 'The new ' + _label + ' does not follow the old one. ' + _did(_tried, _end)
'''


def _qc_inside(form, var, who, mana, abilities, key, other, pass_line, train_line):
    """abilities: [(key, value)] in the inner card; key: the one to print, then train (+2) in CP2; other: the
    reruns' new value (CP1: it is printed; CP2: it must become other + 2)."""
    sheet = {"name": who, "mana": mana, "abilities": dict(abilities)}
    want = dict(abilities)[key]
    sheet_code = _sheet_lines(var, [("name", f"\"{who}\""), ("mana", str(mana))],
                              ("abilities", [(k, str(v)) for k, v in abilities]))
    labels = {"dexterity": "dexterity", "wisdom": "wisdom", "magical_affinity": "magical affinity",
              "strength": "strength"}
    label = labels[key]
    step1 = f"# 1. Print {who}'s {label}.\n"
    step2 = f"# 2. {who} trains: add 2 to\n#    his {label}, inside the card.\n"
    starter = sheet_code + "\n" + step1 + "\n" + step2
    read = f"{var}[\"abilities\"][\"{key}\"]"
    get_line = f"wis = {read}\n"
    put_line = f"{read} = wis + 2\n"

    def program(line, write=""):
        return sheet_code + "\n" + step1 + line + "\n\n" + step2 + write

    solution = program(f"print({read})", get_line + put_line)
    near = [(v, f"Your line printed {v}, {who}'s {labels[k]}, not the {label}.") for k, v in abilities
            if k != key]
    near.append((mana, f"Your line printed {mana}, {who}'s mana, not the {label}."))
    # The evidence names the value tried, never the read itself (that is CP1's fix).
    tried = f"another {label} inside the card, {other}"
    printed = program(f"print({read})")
    moved = sheet_code.replace(f"    \"mana\": {mana},\n", f"    \"mana\": {mana},\n    \"{key}\": {want},\n")
    return dict(
        id="read-inside",
        title="A value inside a card",
        martu=(
            f"{who}'s sheet has a card inside it, `\"abilities\"`. Print {who}'s {label}, read from the sheet. "
            f"Then {who} trains: change the {label} inside the card. Mar'tu's check also tries another {label}, "
            "so read it from the sheet. Don't type it.\n" + _stuck(LESSON_B)
        ),
        names=[var],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id=f"print-the-{key.replace('_', '-')}",
                text=f"Print {who}'s {label}, read from `{var}`.",
                dictated=False,
                hints=[
                    f"Find `\"{key}\"` in the starter. Which card is it inside?",
                    "Read left to right: the outer key gives the inner card, and the inner key gives one value. "
                    "`shelf[\"books\"][\"maps\"]` reads `\"maps\"` inside `\"books\"`.",
                    f"Start with the sheet's name, then two keys in square brackets: `print({var}[`",
                ],
                checks=[
                    check(f"the {var} sheet is kept", _KEEP_SHEET, name=var, sheet=sheet, inner="abilities",
                          train=key),
                    check(f"{who}'s {label} is printed", _READ, name=var, inner="abilities", key=key, want=want,
                          whole="Your line printed a whole dictionary, not one value from inside the card.",
                          near=near,
                          fix=f"No line printed {who}'s {label}."),
                    check(f"the {label} follows the sheet", _FOLLOW, name=var, inner="abilities", key=key,
                          changes=[(var, f"{read} = {other}")], tried=tried, new=other, old=want,
                          typed="The line prints a typed number.",
                          fix=f"The printed {label} does not follow the sheet."),
                ],
                pass_line=pass_line,
            ),
            dict(
                id="train-inside",
                text=f"{who} trains: below your print, add 2 to his {label}, inside the card.",
                dictated=False,
                hints=[
                    f"Below your `print`. The {label} to change is the one you just read: same sheet, same two "
                    "keys.",
                    "Get it, change it, put it back: `old = jar[\"lid\"][\"turns\"]`, then "
                    "`jar[\"lid\"][\"turns\"] = old + 1`. The left side walks the same keys as the read.",
                    "A value inside a card changes like any value: the new value goes on the right of `=`, and the "
                    "spot it goes back to, both keys, on the left.",
                    f"Get the old {label} into a variable first: `wis = {var}[`, then put it back plus 2, with the "
                    "same two keys on the left.",
                ],
                checks=[
                    check(f"the {label} inside the card is up by 2", _TRAIN, name=var, inner="abilities", key=key,
                          start=want, what=label, sheet=sheet),
                    check(f"the new {label} follows the old one", _TRAIN_FOLLOW, name=var, inner="abilities",
                          key=key, tried=tried, changes=[(var, f"{read} = {other}")], new=other, start=want,
                          what=label),
                ],
                pass_line=train_line,
            ),
        ],
        solution=solution,
        partials=[printed],
        assemble=dict(
            lines=[line for line in solution.splitlines() if line.strip() and not line.startswith("#")],
            distractors=[f"print({var}[\"{key}\"])", f"print({var}[\"abilities\"])", f"{var}[\"{key}\"] = wis + 2",
                         f"wis = {want}"],
        ),
        another_way=[
            dict(angle="picture", label="A card inside a sheet", text=(
                "```text\n" f"{var}\n" "  \"name\"\n" "  \"mana\"\n" "  \"abilities\"\n" f"      \"{key}\"\n" "```\n"
                "The outer key opens the card. The inner key reads one line of it. Writing to it walks the same "
                "two keys.")),
            dict(angle="step-by-step", text=(
                f"1. `{var}[\"abilities\"]` is the whole inner card.\n"
                f"2. One more key in square brackets reads one line of that card.\n"
                "3. Put the read inside `print(...)`.\n"
                "4. To change it: get the old value into a variable, then put the new one back with the same two "
                "keys on the left of `=`.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="hold-the-barrier",
            why=(
                "You have seen this read. Holding the barrier started with "
                "`caster[\"abilities\"][\"magical_affinity\"]`: the outer key `\"abilities\"`, then the inner key."
            ),
        ),
        takeaway="Outer key, then inner key: `hero[\"abilities\"][\"wisdom\"]`, to read it or to change it.",
        wrong_answers=[
            dict(why="the starter (nothing printed)", code=starter, fails_at=1, message_contains="No line printed"),
            dict(why=f"a skipped level: {var}[\"{key}\"] (KeyError)", code=program(f"print({var}[\"{key}\"])"),
                 fails_at=0, message_contains=f"KeyError: '{key}'"),
            dict(why="only the outer key: the whole card printed", code=program(f"print({var}[\"abilities\"])"),
                 fails_at=1, message_contains="whole dictionary"),
            dict(why="the whole sheet printed", code=program(f"print({var})"), fails_at=1,
                 message_contains="whole dictionary"),
            dict(why="a label, then the whole inner card (the inner key skipped)",
                 code=program(f"print(\"{label.capitalize()}:\", {var}[\"abilities\"])"), fails_at=1,
                 message_contains="whole dictionary"),
            dict(why="a label, then the whole sheet", code=program(f"print(\"{who}:\", {var})"), fails_at=1,
                 message_contains="whole dictionary"),
            dict(why=f"the {label} typed (CMB; A-06/A-07 typed values)", code=program(f"print({want})"),
                 fails_at=1, message_contains=f"still printed {want}"),
            dict(why="the value typed with a label", code=program(f"print(\"{label.capitalize()}: {want}\")"),
                 fails_at=1, message_contains="prints a typed number"),
            dict(why="the trained value typed in CP1's print (the card is still the starter's)",
                 code=program(f"print({want + 2})"), fails_at=1, message_contains=f"No line printed {who}'s {label}"),
            dict(why="dot access", code=program(f"print({var}.{key})"), fails_at=0,
                 message_contains=f"has no attribute '{key}'"),
            dict(why="dot access on the card", code=program(f"print({var}[\"abilities\"].{key})"), fails_at=0,
                 message_contains="has no attribute"),
            dict(why="round brackets", code=program(f"print({var}(\"abilities\"))"), fails_at=0,
                 message_contains="not callable"),
            dict(why="a dict read by position", code=program(f"print({var}[0])"), fails_at=0,
                 message_contains="KeyError: 0"),
            dict(why="the inner key with a capital", code=program(f"print({var}[\"abilities\"][\"{key.capitalize()}\"])"),
                 fails_at=0, message_contains=f"KeyError: '{key.capitalize()}'"),
            dict(why="the keys the other way round", code=program(f"print({var}[\"{key}\"][\"abilities\"])"),
                 fails_at=0, message_contains=f"KeyError: '{key}'"),
            dict(why="keys with no quotes", code=program(f"print({var}[abilities][{key}])"), fails_at=0,
                 message_contains="name 'abilities' is not defined"),
            dict(why=f"another inner key ({abilities[0][0]})", code=program(f"print({var}[\"abilities\"][\"{abilities[0][0]}\"])"),
                 fails_at=1, message_contains=f"printed {abilities[0][1]}"),
            dict(why="the mana", code=program(f"print({var}[\"mana\"])"), fails_at=1, message_contains=f"printed {mana}"),
            dict(why=f"the key moved to the outside of the sheet to make {var}[\"{key}\"] work (KEEP)",
                 code=moved + "\n" + step1 + f"print({var}[\"{key}\"])\n\n" + step2,
                 fails_at=1, message_contains="on the outside"),
            dict(why="the key in quotes as text: print(\"wisdom\")", code=program(f"print(\"{key}\")"), fails_at=1,
                 message_contains="No line printed"),
            # CP2: the write inside the card (dict-nested write).
            dict(why="CP2 nothing written yet (the partial)", code=printed, fails_at=2,
                 message_contains=f"The {label} inside the card is still"),
            dict(why="CP2 a flat key: the write skips the card (the skipped level, on the left)",
                 code=program(f"print({read})", f"{var}[\"{key}\"] = {read} + 2\n"), fails_at=2,
                 message_contains="on the outside of the sheet"),
            dict(why=f"CP2 the new {label} typed (CMB: {var}[...] = {want + 2})",
                 code=program(f"print({read})", f"{read} = {want + 2}\n"), fails_at=2,
                 message_contains="is a typed number"),
            dict(why=f"CP2 the sum typed ({want} + 2)", code=program(f"print({read})", f"{read} = {want} + 2\n"),
                 fails_at=2, message_contains="is a typed number"),
            dict(why=f"CP2 the {want} in the sheet edited, no write line",
                 code=program(f"print({read})").replace(f"\"{key}\": {want},", f"\"{key}\": {want + 2},"),
                 fails_at=2, message_contains="was edited"),
            dict(why="CP2 worked out into a new variable, never put back (NEWBOX)",
                 code=program(f"print({read})", f"wis = {read} + 2\n"), fails_at=2,
                 message_contains="your variable `wis`"),
            dict(why="CP2 worked out, kept nowhere (BARE)", code=program(f"print({read})", f"{read} + 2\n"),
                 fails_at=2, message_contains="forgets it"),
            dict(why="CP2 the sign the wrong way (minus 2)",
                 code=program(f"print({read})", get_line + f"{read} = wis - 2\n"), fails_at=2,
                 message_contains="went down to"),
            dict(why="CP2 the wrong amount (plus 3)",
                 code=program(f"print({read})", get_line + f"{read} = wis + 3\n"), fails_at=2,
                 message_contains="and it started at"),
            dict(why="CP2 the inner key with a capital on the left (a second key)",
                 code=program(f"print({read})", get_line + f"{var}[\"abilities\"][\"{key.capitalize()}\"] = wis + 2\n"),
                 fails_at=2, message_contains=f"\"{key.capitalize()}\""),
            dict(why=f"CP2 another value trained ({abilities[0][0]})",
                 code=program(f"print({read})", f"{var}[\"abilities\"][\"{abilities[0][0]}\"] = "
                              f"{var}[\"abilities\"][\"{abilities[0][0]}\"] + 2\n"),
                 fails_at=2, message_contains=f"your line changed `\"{abilities[0][0]}\"`"),
            dict(why="CP2 the new value in quotes", code=program(f"print({read})", f"{read} = \"{want + 2}\"\n"),
                 fails_at=2, message_contains="whole number"),
            dict(why="CP2 the right side skips the card (KeyError)",
                 code=program(f"print({read})", f"{read} = {var}[\"{key}\"] + 2\n"), fails_at=0,
                 message_contains=f"KeyError: '{key}'"),
            dict(why="CP2 dot access to write", code=program(f"print({read})", f"{var}[\"abilities\"].{key} = 17\n"),
                 fails_at=0, message_contains="has no attribute"),
        ],
        notes=_qc_meta("dict-nested,dict-read,dict-write", "shelf,books,maps,jar,lid,turns,old", form,
                       level="S3") + "\n"
        f"QC4 C2, form {form}: {who}'s sheet with an inner card ({', '.join(f'{k} {v}' for k, v in abilities)}). "
        f"CP1 prints the {label} ({want}); CP2 (the Unit 5 ruling: a gated write inside a card, dict-nested write) "
        f"adds 2 to it below the print ({want} -> {want + 2}), goal only. CP1: KEEP first (the sheet as given; a key "
        "moved outside in the sheet's own lines to dodge the nested read is named; a key put outside by a write "
        "line, and the trained value itself, are CP2's to judge), then the value (a printed card or sheet gets "
        "'one value', with or without a label in front; neighbouring values are named; the value the card holds "
        f"when it prints is accepted too, so a write put above the print still passes CP1), then CMB: the rerun "
        f"sets `{read} = {other}` inside the check, so a typed {want} fails. CP2: the state (the flat key on the "
        "outside, a near-miss key, another value changed, NEWBOX, BARE, the sign, the amount, a quoted number), "
        f"then CMB: the same rerun must end at {other + 2}, so a typed {want + 2} fails, and so does editing the "
        f"{want} in the sheet. Fails on (spec): `{var}[\"{key}\"]` -> KeyError (crash). Also dot access, round "
        "brackets and a read by position, each a crash with Python's own line (lean explainer). The solution "
        "uses the two-step form of 4B-02 change-inside (`wis = ...`, then the put-back). support='none', "
        "explainer='lean'.",
    )


# ---- C3: build a spell from variables, then store it by name, if it is new (dict-write, dict-key-from-variable,
# dict-in) ----

_SPELL = r'''
_name = __SPELL__
_cv, _nv = __COST__, __NEEDED__
if type(_g.get('cost')).__name__ == 'int':
    _cv = _g['cost']
if type(_g.get('needed')).__name__ == 'int':
    _nv = _g['needed']
if _name not in _g:
    assert False, _gone(_name, __STARTER_NAMES__, True)
_sp = _g[_name]
assert type(_sp).__name__ == 'dict', '`' + _name + '` is not a dictionary.'
_msg = ''
for _k in ('mana_cost', 'required_affinity'):
    if _k in _sp:
        continue
    _x = _near_key(_sp, _k, ('mana_cost', 'required_affinity'))
    if _x is not None:
        _msg = '`' + _name + '` has a key `' + _lit(_x) + '`, and the task spells it `"' + _k + '"`.'
    else:
        _msg = '`' + _name + '` has no key `"' + _k + '"` yet.'
    break
assert not _msg, _msg
_mc, _ra = _sp['mana_cost'], _sp['required_affinity']
for _k, _x in (('mana_cost', _mc), ('required_affinity', _ra)):
    if type(_x).__name__ == 'str':
        _msg = '`' + _name + '["' + _k + '"]` holds the text `"' + _x + '"`. ' + _QUOTES
        break
assert not _msg, _msg
assert not (_cv != _nv and _mc == _nv and _ra == _cv), ('Two values are swapped: `"mana_cost"` holds ' + str(_mc)
                                                        + ', which is `needed`.')
assert _mc == _cv, '`' + _name + '["mana_cost"]` holds ' + _lit(_mc) + ', and `cost` holds ' + str(_cv) + '.'
assert _ra == _nv, '`' + _name + '["required_affinity"]` holds ' + _lit(_ra) + ', and `needed` holds ' + str(_nv) + '.'
'''

_SPELL_FOLLOW = r'''
_tried = __TRIED__
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
_sp = _ns.get(__SPELL__)
_got = (_sp.get('mana_cost'), _sp.get('required_affinity')) if type(_sp).__name__ == 'dict' else ('?', '?')
assert _got == __WANT__, ('`' + __SPELL__ + '` does not follow `cost` and `needed`. '
                          + _did(_tried, ': `' + __SPELL__ + '` still held ' + _lit(_got[0]) + ' and ' + _lit(_got[1])))
'''

_STORE = r'''
_bn, _nn, _sn = __BOOK__, __NAMEVAR__, __SPELL__
_old, _page = __OLD__, __OLD_PAGE__
if _bn not in _g:
    assert False, _gone(_bn)
_b = _g[_bn]
assert type(_b).__name__ == 'dict', '`' + _bn + '` should still be a dictionary.'
_new = _g.get(_nn)
assert _nn not in _b, ('`' + _bn + '` got a page called `"' + _nn + '"`. ' + _QUOTES)
assert _old in _b, 'Keep ' + _old + chr(39) + 's page: `' + _bn + '` lost it.'
assert _b[_old] == _page, 'Leave ' + _old + chr(39) + 's page as the starter has it: it changed.'
if _new not in _b:
    _asks = [_c for _c in _ast.walk(_tree) if type(_c).__name__ == 'Compare' and type(_c.ops[0]).__name__ == 'In'
             and type(_c.left).__name__ == 'Name' and _c.left.id == _nn]
    assert not _asks, 'Your `if` stores only when the name is already in `' + _bn + '`.'
    _extra = [_k for _k in _b if _k != _old]
    assert not _extra, '`' + _bn + '` got a page called `' + _lit(_extra[0]) + '`.'
    assert False, 'The book has no page for ' + _lit(_new) + ' yet.'
_pg = _b[_new]
assert type(_pg).__name__ != 'str', ('The page holds the text `"' + _pg + '"`. ' + _QUOTES)
assert _pg == _g.get(_sn), 'The page holds ' + _lit(_pg) + ', not the whole `' + _sn + '` dictionary.'
'''

_STORE_FOLLOW = r'''
_tried = __TRIED__
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
_b = _ns.get(__BOOK__)
_b = _b if type(_b).__name__ == 'dict' else {}
assert __NEWNAME__ in _b, ('The page name does not follow `' + __NAMEVAR__ + '`. '
                           + _did(_tried, ': the book got no ' + __NEWNAME__ + ' page'))
_pg = _b[__NEWNAME__]
_got = (_pg.get('mana_cost'), _pg.get('required_affinity')) if type(_pg).__name__ == 'dict' else None
assert _got == __WANT__, ('The new page does not follow `' + __SPELL__ + '`. '
                          + _did(_tried, ': the new page held ' + _lit(_pg)))
'''

_GUARD = r'''
_bn, _nn = __BOOK__, __NAMEVAR__
_cmp = [_c for _c in _ast.walk(_tree) if type(_c).__name__ == 'Compare'
        and type(_c.ops[0]).__name__ in ('In', 'NotIn')]
_quoted = [_c for _c in _cmp if type(_c.left).__name__ == 'Constant' and _c.left.value == _nn]
_values = [_c.left.id for _c in _cmp if type(_c.left).__name__ == 'Name' and _c.left.id in __VALUES__]
_typed_list = [_c for _c in _cmp if type(_c.comparators[0]).__name__ in ('List', 'Tuple', 'Set')]
_typed = [_c for _c in _ast.walk(_tree) if type(_c).__name__ == 'Compare'
          and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Name' and _x.id == _nn]
          and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
               and type(_x.value).__name__ == 'str']]
_top_store = [_n for _n in _tree.body if type(_n).__name__ in ('Assign', 'AugAssign')
              and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
                   if type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name' and _t.value.id == _bn]]
if _quoted:
    _why = ('`"' + _nn + '"` in quotes is just those letters, and no page is called that. ' + _QUOTES)
elif _values:
    _why = ('Your `if` asks about `' + _values[0] + '`, and `in` looks at the keys only, never the values.')
elif _typed_list:
    _why = 'Your `if` asks a list of names you typed, not `' + _bn + '`.'
elif _cmp and _top_store:
    _why = 'Line ' + str(_top_store[0].lineno) + ' stores every time, even when the name is not new.'
elif _typed and not _cmp:
    _why = 'Your `if` checks names you typed, not `' + _bn + '`.'
elif not _cmp:
    _why = 'No line asks `' + _bn + '` about the name before the store.'
else:
    _why = 'The store also runs when the name is already in `' + _bn + '`.'
for _tried, _changes, _who, _page, _what in __CASES__:
    _ns, _ls, _err, _miss = _rerun(_changes)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_err, _tried)
    _b = _ns.get(_bn)
    _got = _b.get(_who) if type(_b).__name__ == 'dict' else None
    assert _got == _page, _why + ' ' + _did(_tried, ': ' + _what + ' was written over')
'''


def _qc_store(form, book, name_var, spell_var, old, old_page, new, cost, needed, follow, guard2, guard3, pass_line):
    """follow = (new name, cost, needed) for the CMB rerun; guard2 = (name, page) added to the book in a rerun, and
    named in its message; guard3 = (name, page) the same, never named in any message (so typed names cannot pass)."""
    old_cost, old_needed = old_page
    book_code = (
        f"{book} = {{\n"
        f"    \"{old}\": {{\n"
        f"        \"mana_cost\": {old_cost},\n"
        f"        \"required_affinity\": {old_needed},\n"
        "    },\n"
        "}\n"
    )
    vars_code = f"{name_var} = \"{new}\"\ncost = {cost}\nneeded = {needed}\n"
    step1 = (
        f"# 1. Make {spell_var} from cost and\n"
        "#    needed, with the keys\n"
        "#    \"mana_cost\" and\n"
        "#    \"required_affinity\".\n"
    )
    step2 = (
        f"# 2. If {name_var} is not in {book}\n"
        f"#    yet, store {spell_var} in {book},\n"
        f"#    with {name_var} as the key.\n"
    )
    spell_ok = f"{spell_var} = {{\n    \"mana_cost\": cost,\n    \"required_affinity\": needed,\n}}\n"
    store_ok = f"if {name_var} not in {book}:\n    {book}[{name_var}] = {spell_var}\n"

    def program(spell=spell_ok, store=store_ok):
        return (book_code + vars_code + "\n" + step1 + spell + "\n" + step2 + store + "\n" + f"print({book})\n")

    def literal_spell(mc, ra):
        return f"{spell_var} = {{\n    \"mana_cost\": {mc},\n    \"required_affinity\": {ra},\n}}\n"

    starter = program(spell="", store="")
    solution = program()
    f_name, f_cost, f_needed = follow
    g_name, g_page = guard2
    h_name, h_page = guard3
    page = {"mana_cost": old_cost, "required_affinity": old_needed}
    cases = [
        (f"`{name_var} = \"{old}\"`, `cost = 9` and `needed = 9`",
         [(name_var, f"{name_var} = \"{old}\""), ("cost", "cost = 9"), ("needed", "needed = 9")], old, page,
         f"{old}'s page"),
        (f"`{name_var} = \"{g_name}\"`, with a page for {g_name} already in `{book}`",
         [(book, f"{book}[\"{g_name}\"] = {{\"mana_cost\": {g_page[0]}, \"required_affinity\": {g_page[1]}}}"),
          (name_var, f"{name_var} = \"{g_name}\"")],
         g_name, {"mana_cost": g_page[0], "required_affinity": g_page[1]}, f"{g_name}'s page"),
        (f"another name that already has a page in `{book}`",
         [(book, f"{book}[\"{h_name}\"] = {{\"mana_cost\": {h_page[0]}, \"required_affinity\": {h_page[1]}}}"),
          (name_var, f"{name_var} = \"{h_name}\"")],
         h_name, {"mana_cost": h_page[0], "required_affinity": h_page[1]}, "that page"),
    ]
    return dict(
        id="store-the-spell",
        title="Store a spell by name",
        martu=(
            f"`{book}` holds one page per spell, by name. Build a new spell from the variables, then store it in "
            f"`{book}` under the name in `{name_var}`. Store it only if that name is not in the book yet, so a page "
            "that is already there stays as it is. Mar'tu's check also tries other names and numbers.\n"
            + _stuck(LESSON_B)
        ),
        names=[spell_var, "cost", "needed", book, name_var],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="build-the-spell",
                text=(f"Make `{spell_var}` with the keys `\"mana_cost\"` and `\"required_affinity\"`, built from "
                      "`cost` and `needed`."),
                dictated=False,
                hints=[
                    "Look at the variables above the comments. Which one is the price in mana, and which is the "
                    "affinity a caster needs?",
                    "A value in a dictionary can be a variable, with no quotes: `{\"fuel\": tank}` holds whatever "
                    "`tank` holds.",
                    f"Start with `{spell_var} = {{`, then one line for each key, with a variable as its value.",
                ],
                checks=[
                    check(f"{spell_var} holds the cost and the needed affinity", _SPELL, spell=spell_var, cost=cost,
                          needed=needed, starter_names=[book, name_var, "cost", "needed"]),
                    check(f"{spell_var} follows cost and needed", _SPELL_FOLLOW,
                          tried=f"`cost = {f_cost}` and `needed = {f_needed}`",
                          changes=[("cost", f"cost = {f_cost}"), ("needed", f"needed = {f_needed}")], spell=spell_var,
                          want=(f_cost, f_needed)),
                ],
                pass_line="Gearshift: Math checks out. Cost and affinity, from the variables.",
            ),
            dict(
                id="store-if-new",
                text=(f"If `{name_var}` is not in `{book}` yet, store `{spell_var}` in `{book}`, with `{name_var}` as "
                      "the key."),
                dictated=False,
                hints=[
                    f"Two lines: an `if` that asks the book about `{name_var}`, then an indented line that stores the "
                    "spell.",
                    "`if food not in pantry:` asks about a key. Under it, `pantry[food] = amount` stores a value under "
                    "the key `food` holds.",
                    f"Start with `if {name_var} not in`, then store under `{book}[`",
                ],
                checks=[
                    check(f"the spell is stored under {name_var}", _STORE, book=book, namevar=name_var, spell=spell_var,
                          old=old, old_page=page),
                    check("the page follows the name and the numbers", _STORE_FOLLOW,
                          tried=f"`{name_var} = \"{f_name}\"`, `cost = {f_cost}` and `needed = {f_needed}`",
                          changes=[(name_var, f"{name_var} = \"{f_name}\""), ("cost", f"cost = {f_cost}"),
                                   ("needed", f"needed = {f_needed}")],
                          book=book, namevar=name_var, spell=spell_var, newname=f_name,
                          want=(f_cost, f_needed)),
                    check("a page that is there stays as it is", _GUARD, book=book, namevar=name_var,
                          values=["cost", "needed", spell_var], cases=cases),
                ],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        partials=[program(store="")],
        assemble=dict(
            lines=[line for line in solution.splitlines() if line.strip() and not line.startswith("#")],
            distractors=[f"    {book}[\"{name_var}\"] = {spell_var}", f"if {spell_var} not in {book}:",
                         f"    \"mana_cost\": {cost},"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. Build `{spell_var}`: two keys in quotes, each with a variable as its value, no quotes.\n"
                f"2. Ask the book: is the name in `{name_var}` missing from `{book}`?\n"
                f"3. If so, store the spell under that name, with no quotes around `{name_var}`.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "The spell book part stored each spell with `spell_book[spell_name] = spell`. The barrier part "
                "began by asking `if spell_name not in caster[\"spell_book\"]:`. This task puts the two together.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="spell-book",
            snippet="spell_book[spell_name] = spell",
            why=(
                "You have seen this line in `add_spell()`. The key came from a variable, with no quotes, so each "
                "page was called by the spell's own name. And `cast_spell` opened by asking `not in` first."
            ),
        ),
        takeaway="Build a dict from variables, ask `if name not in book:`, then store it with `book[name] = spell`.",
        wrong_answers=[
            dict(why="the starter (no spell yet)", code=starter, fails_at=1, message_contains=f"Nothing in your program is called `{spell_var}`"),
            dict(why=f"CP1 the numbers typed in (literals; A-06/A-07 test values)", code=program(spell=literal_spell(cost, needed)),
                 fails_at=1, message_contains=f"`{spell_var}` still held {cost} and {needed}"),
            dict(why="CP1 the two variables swapped (SWAP)", code=program(spell=literal_spell("needed", "cost")),
                 fails_at=1, message_contains="swapped"),
            dict(why="CP1 a variable in quotes (\"cost\")", code=program(spell=literal_spell("\"cost\"", "needed")),
                 fails_at=1, message_contains=QUOTES_RULE),
            dict(why="CP1 a key with a capital (KEY)", code=program(spell=spell_ok.replace('"mana_cost"', '"Mana_Cost"')),
                 fails_at=1, message_contains='"Mana_Cost"'),
            dict(why="CP1 keys with no quotes", code=program(spell=spell_ok.replace('"mana_cost"', "mana_cost")),
                 fails_at=0, message_contains="name 'mana_cost' is not defined"),
            dict(why="CP1 = for : inside the dictionary", code=program(spell=spell_ok.replace('"mana_cost":', '"mana_cost" =')),
                 fails_at=0, message_contains="cannot assign to literal"),
            dict(why="CP1 a missing comma after a variable", code=program(spell=spell_ok.replace("cost,", "cost", 1)),
                 fails_at=0, message_contains="invalid syntax"),
            dict(why="CP2 the variable's name in quotes: book[\"spell_name\"] (KEY)",
                 code=program(store=f"if {name_var} not in {book}:\n    {book}[\"{name_var}\"] = {spell_var}\n"),
                 fails_at=2, message_contains=f"page called `\"{name_var}\"`"),
            dict(why="CP2 stored with no guard (a page that is there is written over)",
                 code=program(store=f"{book}[{name_var}] = {spell_var}\n"), fails_at=2, message_contains="No line asks"),
            dict(why="CP2 the guard asks about a value: `in` checks keys, not values",
                 code=program(store=f"if cost not in {book}:\n    {book}[{name_var}] = {spell_var}\n"), fails_at=2,
                 message_contains="never the values"),
            dict(why="CP2 the guard asks about the spell itself (a value: unhashable dict)",
                 code=program(store=f"if {spell_var} not in {book}:\n    {book}[{name_var}] = {spell_var}\n"),
                 fails_at=0, message_contains="unhashable type: 'dict'"),
            dict(why="CP2 the guard asks about the quoted name",
                 code=program(store=f"if \"{name_var}\" not in {book}:\n    {book}[{name_var}] = {spell_var}\n"),
                 fails_at=2, message_contains="just those letters"),
            dict(why="CP2 `in` for `not in` (nothing new is ever stored)",
                 code=program(store=f"if {name_var} in {book}:\n    {book}[{name_var}] = {spell_var}\n"), fails_at=2,
                 message_contains="already in"),
            dict(why="CP2 the guard typed for one page only (!= the old name)",
                 code=program(store=f"if {name_var} != \"{old}\":\n    {book}[{name_var}] = {spell_var}\n"), fails_at=2,
                 message_contains=f"{g_name}'s page was written over"),
            dict(why="CP2 the guard types both names it has seen (the hidden third page catches it)",
                 code=program(store=f"if {name_var} != \"{old}\" and {name_var} != \"{g_name}\":\n"
                                    f"    {book}[{name_var}] = {spell_var}\n"),
                 fails_at=2, message_contains="checks names you typed"),
            dict(why="CP2 the store line not indented under the if (it runs every time)",
                 code=program(store=f"if {name_var} not in {book}:\n    print(\"A new spell.\")\n"
                                    f"{book}[{name_var}] = {spell_var}\n"),
                 fails_at=2, message_contains="stores every time"),
            dict(why="CP2 the guard asks a typed list, not the book",
                 code=program(store=f"if {name_var} not in [\"{old}\", \"{g_name}\"]:\n"
                                    f"    {book}[{name_var}] = {spell_var}\n"),
                 fails_at=2, message_contains="list of names you typed"),
            dict(why="CP2 the spell's name typed as the key (CMB)",
                 code=program(store=f"if \"{new}\" not in {book}:\n    {book}[\"{new}\"] = {spell_var}\n"), fails_at=2,
                 message_contains=f"no {f_name} page"),
            dict(why="CP2 the book replaced (the old page lost)", code=program(store=f"{book} = {{{name_var}: {spell_var}}}\n"),
                 fails_at=2, message_contains="lost it"),
            dict(why="CP2 the spell's name stored as text", code=program(store=f"if {name_var} not in {book}:\n    {book}[{name_var}] = \"{spell_var}\"\n"),
                 fails_at=2, message_contains="holds the text"),
            dict(why="CP2 something else stored (the cost)", code=program(store=f"if {name_var} not in {book}:\n    {book}[{name_var}] = cost\n"),
                 fails_at=2, message_contains="whole"),
            dict(why="CP2 dot access to store", code=program(store=f"{book}.{name_var} = {spell_var}\n"), fails_at=0,
                 message_contains="has no attribute"),
            dict(why="CP2 round brackets to store", code=program(store=f"{book}({name_var}) = {spell_var}\n"), fails_at=0,
                 message_contains="cannot assign to function call"),
            dict(why="CP2 the lesson's book name (NameError)",
                 code=program(store=f"if {name_var} not in spell_books:\n    spell_books[{name_var}] = {spell_var}\n"),
                 fails_at=0, message_contains="name 'spell_books' is not defined"),
        ],
        notes=_qc_meta("dict-make,dict-write,dict-key-from-variable,dict-in", "fuel,tank,pantry,food,amount", form,
                       level="S2") + "\n"
        f"QC4 C3, form {form}: `{book}` holds {old} ({old_cost}, {old_needed}); the new spell {new} costs {cost} and "
        f"needs {needed}. Deviation (module docstring): two checkpoints, and CP2 asks `not in` first, the campaign's "
        "`if spell_name not in caster[\"spell_book\"]:`, so dict-in has a gated task. CP1: KEY, the quoted variable "
        f"(`\"cost\"`, with the quotes sentence), SWAP, then CMB (`cost = {f_cost}`, `needed = {f_needed}`): typed "
        f"numbers fail (spec: literals -> CMB). CP2: `{book}[\"{name_var}\"]` -> KEY (spec), {old} kept, the page is "
        f"the spell, CMB (`{name_var} = \"{f_name}\"`), then the guard: three reruns where the name is already a page "
        f"({old}, a {g_name} page added inside the check, and a {guard3[0]} page that no message names), so `!= "
        f"\"{old}\"` fails, and so does typing every name the messages show (`!=` chains, a typed list). Guard "
        "diagnoses: names typed in the `if`, a typed list, the store line not indented under the `if`, no ask, "
        "a value asked about (`cost`: the in-checks-values belief, Q1's slip in code form), the quoted name, `in` "
        "for `not in`. `if spell not in book:` crashes (unhashable dict). The guard is now taught first in u05b's "
        "4B-04 CP3 (`store-if-new`, `if spell_name not in spell_book:` above the store line), so this goal-only "
        "store-then-guard step is fair on the fast path. support='none', explainer='lean'.",
    )


# ---- C4: mend a KeyError from a skipped level, then get it, compare, act (dict-nested, Obj 9) ----

_MEND_READ = r'''
assert _g.get('needed') == __NEEDED__, ('Keep `needed = ' + str(__NEEDED__) + '` as the starter has it: `needed` now '
                                        'holds ' + _lit(_g.get('needed')) + '.')
assert 'skill' in _g, 'Keep the line that makes `skill`: it is gone.'
_s = _g['skill']
_msg = ''
if _s != __WANT__:
    for _v, _m in __NEAR__:
        if _s == _v:
            _msg = _m
    _msg = _msg or ('`skill` holds ' + _lit(_s) + ', not the magical affinity.')
assert not _msg, _msg
'''

# CP1 judges the read and the `if`, never the `elif` (CP2's step): the starter's caster can cast, so the run
# prints the cast line, or the mana warning while CP2's test is still wrong.
_MEND_FOLLOW = r'''
_tried = __TRIED__
_yes, _no, _more = __YES__, __NO__, __MORE__
_now = _lines()
assert _shows(_now, _yes) or _shows(_now, _more), ('Keep the `if`, `elif` and `else` lines as they are: `'
                                                   + _yes + '` no longer prints.')
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
assert _ns.get('skill') == __NEW__, ('`skill` holds a typed number. '
                                     + _did(_tried, ': `skill` still held ' + _lit(_ns.get('skill'))))
# Only one line printing is CP2's to judge (its last rerun), so a broken chain is named there.
assert _shows(_ls, _no), ('Keep the `if` line as the starter has it. ' + _did(_tried, ': `' + _no + '` should have '
                                                                             'printed'))
'''

# CP2: the mana test in place of `elif False:` (get it, compare, act). The student's own run first, then reruns
# with the mana below `cost`, `cost` above the mana, exactly enough, and the affinity too low as well.
_MANA_TEST = r'''
_yes, _no, _more = __YES__, __NO__, __MORE__
def _holds(_body, _text):
    for _s in _body:
        for _c in _ast.walk(_s):
            if type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'str' and _text in _c.value:
                return True
    return False
_t = [_n.test for _n in _ast.walk(_tree) if type(_n).__name__ == 'If' and _holds(_n.body, _more)]
_t = _t[0] if _t else None
_parts = [_t.left] + list(_t.comparators) if type(_t).__name__ == 'Compare' else []
_nums = [_p for _p in _parts if type(_p).__name__ == 'Constant' and type(_p.value).__name__ in ('int', 'float')]
_cost = [_p for _p in _parts if type(_p).__name__ == 'Name' and _p.id == 'cost']
_why = ''
if type(_t).__name__ == 'Constant':
    _why = '`' + str(_t.value) + '` is still there, so every caster gets the same answer.'
elif _parts and len(_nums) == len(_parts):
    _why = 'Your test compares typed numbers, so every caster gets the same answer.'
elif _nums and _cost:
    _why = 'Your test uses a typed number for the mana.'
elif _nums:
    _why = 'Your test uses a typed number for the cost.'
def _seen(_ls):
    return [_x for _x in (_no, _more, _yes) if _shows(_ls, _x)]
def _said(_got):
    return ('your program printed ' + ' and '.join('`' + _x + '`' for _x in _got)) if _got else 'nothing printed'
_c = _g.get('caster')
_m = _c.get('mana') if type(_c).__name__ == 'dict' else None
_cv, _sk, _nd = _g.get('cost'), _g.get('skill'), _g.get('needed')
if not [_x for _x in (_m, _cv, _sk, _nd) if type(_x).__name__ != 'int']:
    _exp = _no if _sk < _nd else (_more if _m < _cv else _yes)
    _got = _seen(_lines())
    if _got != [_exp]:
        if _why:
            _msg = _why
        elif _exp == _yes and _got == [_more]:
            _msg = ('The caster has ' + str(_m) + ' mana and `cost` is ' + str(_cv) + ', and your test warned.')
        else:
            _msg = 'One run should print one line: ' + _said(_got) + '.'
        assert False, _msg
for _tried, _changes, _expect, _m in __CASES__:
    _ns, _ls, _err, _miss = _rerun(_changes)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_err, _tried)
    _got = _seen(_ls)
    if _got != [_expect]:
        assert False, (_why or _m) + ' ' + _did(_tried, ': ' + _said(_got))
'''


def _qc_mend(form, who, mana, abilities, needed, cost, other, pass_line, mana_line):
    affinity = dict(abilities)["magical_affinity"]
    sheet = {"name": who, "mana": mana, "abilities": dict(abilities)}
    sheet_code = _sheet_lines("caster", [("name", f"\"{who}\""), ("mana", str(mana))],
                              ("abilities", [(k, str(v)) for k, v in abilities]))
    yes, no, more = f"{who} can cast it.", "Not skilled enough yet.", "Needs more mana."
    slip = "caster[\"magical_affinity\"]"
    mended = "caster[\"abilities\"][\"magical_affinity\"]"
    mana_ok = "caster[\"mana\"] < cost"

    def program(read=slip, test="False", sheet=sheet_code, extra=""):
        return (
            sheet + f"needed = {needed}\ncost = {cost}\n\n"
            f"skill = {read}\n"
            "if skill < needed:\n"
            f"    print(\"{no}\")\n"
            f"elif {test}:\n"
            f"    print(\"{more}\")\n"
            "else:\n"
            f"    print(\"{yes}\")\n"
            + extra
        )

    starter = program()
    solution = program(mended, mana_ok)
    other_key, other_value = [(k, v) for k, v in abilities if k != "magical_affinity"][0]
    near = [(other_value, f"`skill` holds {other_value}, the {other_key}, not the magical affinity."),
            (mana, f"`skill` holds {mana}, the mana, not the magical affinity.")]
    # The evidence names the value tried, never the mended read (CP1's fix).
    tried = f"another magical affinity inside the card, {other}"
    moved = sheet_code.replace(f"    \"mana\": {mana},\n", f"    \"mana\": {mana},\n    \"magical_affinity\": {affinity},\n")
    low_aff = 4
    cases = [
        (f"a caster with 3 mana against `cost = {cost}`",
         [("caster", "caster[\"mana\"] = 3"), ("cost", f"cost = {cost}")], more,
         "This caster is short of mana, and your test let them cast."),
        (f"`cost = 30` against {mana} mana",
         [("caster", f"caster[\"mana\"] = {mana}"), ("cost", "cost = 30")], more,
         "This spell costs more than the caster has, and your test let them cast."),
        (f"a caster with exactly {cost} mana against `cost = {cost}`",
         [("caster", f"caster[\"mana\"] = {cost}"), ("cost", f"cost = {cost}")], yes,
         "Your test also warns when the mana equals `cost`."),
        (f"an affinity of {low_aff} and 3 mana against `cost = {cost}`",
         [("caster", f"caster[\"abilities\"][\"magical_affinity\"] = {low_aff}"),
          ("caster", "caster[\"mana\"] = 3"), ("cost", f"cost = {cost}")], no,
         f"With the affinity too low, only `{no}` should print."),
    ]
    return dict(
        id="mend-the-read",
        title="Mend it, then test the mana",
        martu=(
            f"This program stops with a [[KeyError]]. Read Python's last line, find the line it names, and mend "
            "the read so the program runs. Leave the sheet as it is.\n"
            "Then finish the chain: replace `False` with a test of the caster's mana against `cost`. Mar'tu's "
            "check also tries other casters and costs.\n" + _stuck(LESSON_B)
        ),
        names=["caster", "skill", "cost"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="mend-the-read",
                text="Mend the line Python stops on, so `skill` holds the caster's magical affinity.",
                dictated=False,
                hints=[
                    "Read Python's last line: which key could it not find? Then find that key in the sheet.",
                    "A [[KeyError]] means no key spelled exactly like that, at that level. A key inside a card "
                    "needs the card's key first: `shelf[\"books\"][\"maps\"]`.",
                    "Keep `skill = caster[` and add the outer key before the one that is there.",
                ],
                checks=[
                    check("the caster sheet is kept", _KEEP_SHEET, name="caster", sheet=sheet, inner="abilities",
                          train=None),
                    check("skill holds the magical affinity", _MEND_READ, want=affinity, near=near, needed=needed),
                    check("skill follows the sheet", _MEND_FOLLOW, tried=tried,
                          changes=[("caster", f"caster[\"abilities\"][\"magical_affinity\"] = {other}")], new=other,
                          yes=yes, no=no, more=more),
                ],
                pass_line=pass_line,
            ),
            dict(
                id="mana-test",
                text=("Replace `False` with a test: the warning prints when the caster's mana is lower than `cost`. "
                      "Exactly enough mana still casts."),
                dictated=False,
                hints=[
                    "The mana is on the big sheet, beside `\"name\"`, not inside the card. The price is in `cost`.",
                    "`elif` asks only when the `if` above was false. `fuel < trip` asks *lower than*: exactly "
                    "enough is not lower, so it still goes. That is `<`, not `<=`.",
                    "Read the mana with one key, then compare it with `cost`, the way `skill < needed` compares "
                    "two values.",
                    "Start with `elif caster[`, in place of `elif False:`.",
                ],
                checks=[
                    check("the warning follows the mana and cost", _MANA_TEST, yes=yes, no=no, more=more,
                          cases=cases),
                ],
                pass_line=mana_line,
            ),
        ],
        solution=solution,
        partials=[program(mended)],
        assemble=dict(
            lines=[line for line in solution.splitlines() if line.strip()],
            distractors=["skill = caster[\"magical_affinity\"][\"abilities\"]", f"skill = {affinity}",
                         "elif caster[\"mana\"] <= cost:", "elif caster[\"abilities\"][\"mana\"] < cost:"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                "1. Python's last line names the key it could not find.\n"
                "2. Find that key in the sheet: which card is it inside?\n"
                "3. Read the card's key first, then the inner key.\n"
                "4. In the `elif`, compare the caster's mana with `cost`. *Lower than* is `<`.")),
            dict(angle="picture", label="Where the keys live", text=(
                "```text\ncaster\n  \"name\"\n  \"mana\"\n  \"abilities\"\n      \"magical_affinity\"\n```\n"
                "The affinity is one level down, inside the card. The mana is on the big sheet.")),
            dict(angle="from the campaign", label="Get it, compare, act", text=(
                "Holding the barrier was this chain. Get the affinity and compare it with what the spell needs. "
                "Else, if the mana is lower than the cost, warn. Else, cast. Exactly enough still casts, so the "
                "tests use `<`.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="hold-the-barrier",
            why=(
                "You have seen this chain. Holding the barrier asked about "
                "`caster[\"abilities\"][\"magical_affinity\"]` first, then `elif caster[\"mana\"] < "
                "spell[\"mana_cost\"]:`. `caster[\"magical_affinity\"]` would stop there with the same KeyError."
            ),
        ),
        takeaway="Get it, compare, act: read the outer key first, then test with `<`, so exactly enough still casts.",
        wrong_answers=[
            dict(why="the starter, left unmended (the skipped level; the campaign's own slip)", code=starter,
                 fails_at=0, message_contains="KeyError: 'magical_affinity'"),
            dict(why="the affinity typed (CMB)", code=program(str(affinity)), fails_at=1,
                 message_contains=f"still held {affinity}"),
            dict(why="the key moved to the outside of the sheet (KEEP)", code=program(sheet=moved), fails_at=1,
                 message_contains="on the outside"),
            dict(why="only the outer key: a whole card compared with <", code=program("caster[\"abilities\"]"),
                 fails_at=0, message_contains="not supported between instances of 'dict' and 'int'"),
            dict(why="the keys the other way round", code=program("caster[\"magical_affinity\"][\"abilities\"]"),
                 fails_at=0, message_contains="KeyError: 'magical_affinity'"),
            dict(why="the inner key with capitals", code=program("caster[\"abilities\"][\"Magical_Affinity\"]"),
                 fails_at=0, message_contains="KeyError: 'Magical_Affinity'"),
            dict(why="the inner key with a space", code=program("caster[\"abilities\"][\"magical affinity\"]"),
                 fails_at=0, message_contains="KeyError: 'magical affinity'"),
            dict(why="dot access on the card", code=program("caster[\"abilities\"].magical_affinity"), fails_at=0,
                 message_contains="has no attribute 'magical_affinity'"),
            dict(why="round brackets", code=program("caster(\"abilities\")[\"magical_affinity\"]"), fails_at=0,
                 message_contains="not callable"),
            dict(why="a dict read by position", code=program("caster[2][\"magical_affinity\"]"), fails_at=0,
                 message_contains="KeyError: 2"),
            dict(why="keys with no quotes", code=program("caster[abilities][magical_affinity]"), fails_at=0,
                 message_contains="name 'abilities' is not defined"),
            dict(why=f"another inner key ({other_key})", code=program(f"caster[\"abilities\"][\"{other_key}\"]"),
                 fails_at=1, message_contains=f"the {other_key}"),
            dict(why="the read line deleted and the number typed in the if",
                 code=program().replace(f"skill = {slip}\n", "").replace("if skill <", f"if {affinity} <"),
                 fails_at=1, message_contains="Keep the line that makes `skill`"),
            dict(why="needed changed instead of the read mended (skill typed, needed lowered to match)",
                 code=program(str(affinity)).replace(f"needed = {needed}\n", "needed = 0\n"), fails_at=1,
                 message_contains="Keep `needed"),
            dict(why="the reply lines changed (KEEP)", code=solution.replace(f"\"{yes}\"", "\"Yes.\""), fails_at=1,
                 message_contains="Keep the `if`, `elif` and `else`"),
            # CP2: get it, compare, act (Obj 9).
            dict(why="CP2 `False` left as it is (the partial)", code=program(mended), fails_at=2,
                 message_contains="is still there"),
            dict(why=f"CP2 typed numbers ({mana} < {cost}; the class's numbers in ink)",
                 code=program(mended, f"{mana} < {cost}"), fails_at=2, message_contains="typed numbers"),
            dict(why="CP2 <= for < (exactly enough would not cast)", code=program(mended, "caster[\"mana\"] <= cost"),
                 fails_at=2, message_contains="equals `cost`"),
            dict(why="CP2 the sides swapped: cost < caster[\"mana\"]", code=program(mended, "cost < caster[\"mana\"]"),
                 fails_at=2, message_contains="and your test warned"),
            dict(why="CP2 > for <", code=program(mended, "caster[\"mana\"] > cost"), fails_at=2,
                 message_contains="and your test warned"),
            dict(why="CP2 the mana read inside the card: an extra level (KeyError)",
                 code=program(mended, "caster[\"abilities\"][\"mana\"] < cost"), fails_at=0,
                 message_contains="KeyError: 'mana'"),
            dict(why=f"CP2 the cost typed: caster[\"mana\"] < {cost} (CMB on cost)",
                 code=program(mended, f"caster[\"mana\"] < {cost}"), fails_at=2,
                 message_contains="a typed number for the cost"),
            dict(why=f"CP2 the mana typed: {mana} < cost (CMB on the mana)", code=program(mended, f"{mana} < cost"),
                 fails_at=2, message_contains="a typed number for the mana"),
            dict(why="CP2 needed for cost", code=program(mended, "caster[\"mana\"] < needed"), fails_at=2,
                 message_contains="costs more than the caster has"),
            dict(why="CP2 the affinity compared with the cost", code=program(mended, "skill < cost"), fails_at=2,
                 message_contains="this caster is short"),
            dict(why="CP2 the chain broken: the mana test as a second `if` (both lines print)",
                 code=program(mended, mana_ok).replace("elif caster", "if caster"), fails_at=2,
                 message_contains="should print"),
            dict(why="CP2 a capital in the key (KeyError)", code=program(mended, "caster[\"Mana\"] < cost"),
                 fails_at=0, message_contains="KeyError: 'Mana'"),
            dict(why="CP2 dot access", code=program(mended, "caster.mana < cost"), fails_at=0,
                 message_contains="has no attribute 'mana'"),
        ],
        notes=_qc_meta("dict-nested,dict-read,read-traceback,boundary,elif-chain", "shelf,books,maps,fuel,trip", form,
                     level="S4")
        + "\n"
        f"QC4 C4, form {form}: `caster` is {who}'s sheet (magical affinity {affinity} inside `\"abilities\"`, mana "
        f"{mana} on the outside), `needed = {needed}`, `cost = {cost}`, then the campaign's chain: `skill = "
        "caster[\"magical_affinity\"]` (the campaign's exact slip, kept), `if skill < needed:` / `elif False:` / "
        "`else:`. The starter's caster can cast once the read is mended. CP1 (spec: 'left unmended' fails): KEEP "
        f"first (a key moved to the outside fails; `needed` stays {needed}), then the value (other inner values "
        f"named), then CMB (`... = {other}` inside the check: `skill` follows and the `if` line prints), so a "
        f"typed {affinity} fails. CP1 never judges the `elif`, so a CP2 slip never turns it red. CP2 (the Unit 5 "
        "ruling: objective 9, get it, compare, act, gated on the fast path): the student writes the mana test in "
        "place of `False`, goal only. The student's own run, then four reruns: the mana below `cost` (only the "
        "warning), `cost = 30` above the mana (only the warning), exactly enough (the cast line: `<=` fails), and "
        "the affinity too low with too little mana (only 'Not skilled': a second `if` fails). The reruns set the "
        "mana and `cost`, so a typed number on either side fails (CMB); diagnoses from the test itself: `False` "
        "left, typed numbers on both sides, a typed mana, a typed cost; the sign; `caster[\"abilities\"][\"mana\"]` "
        "is a crash (KeyError: 'mana'). Each other slip (round brackets, a dot, a position, unquoted keys, "
        "capitals) is a crash with Python's own line. support='none', explainer='lean'.",
    )


# ---- C5: a list of sheets, then spend by key (list-of-dicts, dict-write); 2 CPs ----

HEROES = [("oogrish", "Oogrish", 18), ("gearshift", "Gearshift", 20), ("bomb_shell", "Bomb Shell", 24),
          ("lucky", "Lucky", 26)]

_ROSTER_KEEP = r'''
_r = _g.get('roster')
assert type(_r).__name__ == 'list' and len(_r) == 4, 'Keep `roster` as the starter has it: four sheets.'
assert not [_s for _s in _r if type(_s).__name__ != 'dict' or 'name' not in _s or 'mana' not in _s], (
    'Keep the four sheets as the starter has them, each with `"name"` and `"mana"`.')
'''

_ROSTER_READ = r'''
_ls = _lines()
_msg = ''
if not _shows(_ls, __WANT__):
    _whole = [_l for _l in _ls if _display(_l) and __WANT__ in _l]
    if _whole:
        _msg = 'Your line printed ' + ('the whole roster' if '[{' in _whole[0] else 'a whole sheet') + ', not only the name.'
    for _v, _m in __NEAR__:
        if not _msg and _shows(_ls, _v):
            _msg = _m
    _msg = _msg or 'No line printed the name at position ' + str(__POS__) + ' in `roster`.'
else:
    _also = [(_i, _n) for _i, _n in __OTHERS__ if _shows(_ls, _n)]
    if _also:
        _msg = ('Your program printed ' + _also[0][1] + ' too, at position ' + str(_also[0][0]) + '.')
assert not _msg, _msg
'''

_ROSTER_FOLLOW = r'''
_tried = __TRIED__
_ns, _ls, _err, _miss = _rerun(__CHANGES__)
assert not _miss, _keep(_miss[0])
assert not _err, _stop(_err, _tried)
if not _shows(_ls, __NEW__):
    _end = ': position ' + str(__POS__) + ' was ' + __NEW__ + ', and your line did not print that name'
    if _prints_name(__VAR__):
        _msg = 'Your line reads the name from `' + __VAR__ + '`, not through `roster`.'
    elif _prints_text(__WHO__):
        _msg = 'Your line types the name.'
    else:
        _msg = 'The printed name does not follow `roster`.'
    assert False, _msg + ' ' + _did(_tried, _end)
'''

_SPEND = _ROSTER_KEEP + r'''
_pos, _start, _cost = __POS__, __START__, __COST__
if type(_g.get('cost')).__name__ == 'int':
    assert _g['cost'] != 0, ('Keep `cost = ' + str(_cost) + '` as the starter has it: `cost` now holds 0, so '
                             'nothing is spent.')
    _cost = _g['cost']
_starts = __STARTS__
_want = _start - _cost
_r = _g['roster']
_h = _r[_pos]
_m = _h['mana']
_others = [_i for _i in range(4) if _i != _pos and _r[_i].get('mana') != _starts[_i]]
assert not _others, ('Your line changed the mana at position ' + str(_others[0]) + ', not ' + str(_pos) + '.')
_x = _near_key(_h, 'mana', ('name', 'mana'))
assert _x is None, ('The sheet now has a key `' + _lit(_x) + '` too, and its `"mana"` is still ' + str(_m) + '.')
if _m == _start:
    _box = [_n for _n in _made() if _n not in ('roster', 'cost') and _n not in __SHEETS__ and _g.get(_n) == _want]
    _bare = [_n for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
    if _box:
        _msg = ('Your variable `' + _box[0] + '` holds ' + str(_want) + ', and the sheet still says ' + str(_start)
                + '.')
    elif _bare:
        _msg = ('Your line works out the new mana, then forgets it. The sheet still says ' + str(_start) + '.')
    else:
        _msg = 'The hero' + chr(39) + 's mana is still ' + str(_start) + '.'
    assert False, _msg
assert type(_m).__name__ == 'int', 'The mana holds ' + _lit(_m) + ', not a whole number.'
assert _m != _start + _cost, 'The mana went up to ' + str(_m) + '.'
assert _m != _cost - _start, 'The mana is ' + str(_m) + ': the cost minus the mana.'
assert _m == _want, 'The mana should go down by `cost`: it is ' + str(_m) + ', and it started at ' + str(_start) + '.'
'''

_SPEND_FOLLOW = r'''
_pos = __POS__
_c = _g['cost'] if type(_g.get('cost')).__name__ == 'int' else __COST__
for _tried, _changes, _base, _spent, _what, _keepname, _keepmana in __CASES__:
    _want = _base - (_c if _spent is None else _spent)
    _ns, _ls, _err, _miss = _rerun(_changes)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_err, _tried)
    _r = _ns.get('roster')
    _got = _r[_pos].get('mana') if type(_r).__name__ == 'list' and len(_r) > _pos and type(_r[_pos]).__name__ == 'dict' else '?'
    if _keepname:
        _paid = [_s for _s in _r if type(_s).__name__ == 'dict' and _s.get('name') == _keepname]
        assert not (_paid and _paid[0].get('mana') != _keepmana), (
            'The spend does not go through `roster`. ' + _did(_tried, ': ' + _keepname + chr(39) + 's own sheet paid, '
            'not the hero at position ' + str(_pos)))
    assert _got == _want, _what + ' ' + _did(_tried, ': the mana went to ' + _lit(_got) + ', not ' + str(_want))
'''


def _qc_roster(form, pos, cost, follow_cost, follow_mana, pass_line):
    var, who, start = HEROES[pos]
    sheets = "".join(_sheet_lines(v, [("name", f"\"{n}\""), ("mana", str(m))]) for v, n, m in HEROES)
    roster_code = "roster = [\n" + "".join(f"    {v},\n" for v, _, _ in HEROES) + "]\n"
    head = sheets + roster_code + f"cost = {cost}\n\n"
    step1 = f"# 1. Print the name of the hero\n#    at position {pos} in roster.\n"
    step2 = "# 2. That hero casts a spell.\n#    Take cost from their mana,\n#    through roster.\n"
    read_ok = f"print(roster[{pos}][\"name\"])\n"
    spend_ok = f"roster[{pos}][\"mana\"] = roster[{pos}][\"mana\"] - cost\n"

    def program(read=read_ok, spend=spend_ok):
        return head + step1 + read + "\n" + step2 + spend

    starter = program(read="", spend="")
    solution = program()
    order = [3, 2, 1, 0]
    moved_var, moved_who, moved_start = HEROES[order[pos]]
    reorder = "roster = [roster[3], roster[2], roster[1], roster[0]]"
    reorder_tried = "the heroes in another order, Lucky first"
    near = []
    for i, (_, n, _) in enumerate(HEROES):
        if i == pos:
            continue
        lead = "Positions count from 0: " if i == pos + 1 else ""
        near.append((n, f"{lead}your line printed {n}, at position {i}."))
    want = start - cost
    starts = [m for _, _, m in HEROES]
    cases = [
        (f"`cost = {follow_cost}`", [("cost", f"cost = {follow_cost}")], start, follow_cost,
         "The spend does not follow `cost`.", "", 0),
        (f"{who} with {follow_mana} mana", [(var, f"{var}[\"mana\"] = {follow_mana}")], follow_mana, None,
         "The new mana does not follow the old mana.", "", 0),
        (reorder_tried, [("roster", reorder)], moved_start, None,
         "The spend does not follow `roster`.", who, start),
    ]
    return dict(
        id="spend-through-the-roster",
        title="A roster of sheets",
        martu=(
            f"Four sheets, one list. Print the name of the hero at position {pos} in `roster`. Then that hero casts "
            "a spell: take `cost` from their mana, through `roster`. Mar'tu's check also tries other numbers and "
            "another order.\n" + _stuck(LESSON_B)
        ),
        names=["roster", "cost"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="name-at-position",
                text=f"Print the name of the hero at position {pos} in `roster`.",
                dictated=False,
                hints=[
                    "A list counts from 0. Which sheet sits at that position?",
                    "Position first, then the key: `shelf[0][\"title\"]` is the title of the first book on the "
                    "shelf.",
                    "Start with `print(roster[`, then the position, then the key.",
                ],
                checks=[
                    check("the roster is kept", _ROSTER_KEEP),
                    check(f"the name at position {pos} is printed", _ROSTER_READ, want=who, near=near, pos=pos,
                          others=[[i, n] for i, (_, n, _) in enumerate(HEROES) if i != pos]),
                    check("the name follows the roster", _ROSTER_FOLLOW, tried=reorder_tried,
                          changes=[("roster", reorder)], new=moved_who, pos=pos, var=var, who=who),
                ],
                pass_line=f"{who}: That's me. Position {pos}.",
            ),
            dict(
                id="spend-the-cost",
                text="That hero casts a spell. Take `cost` from their mana, through `roster`.",
                dictated=False,
                hints=[
                    "One line: the left side is where the new mana goes, and the right side works it out from the "
                    "old mana.",
                    "`shelf[0][\"pages\"] = shelf[0][\"pages\"] - torn` reads the old pages, takes `torn` away, and "
                    "stores the answer under the same key.",
                    f"Start with `roster[{pos}][\"mana\"] =`, then read the old mana the same way.",
                ],
                checks=[
                    check("the hero's mana went down by cost", _SPEND, pos=pos, start=start, cost=cost, starts=starts,
                          sheets=[v for v, _, _ in HEROES]),
                    check("the mana follows cost, the sheet and the roster", _SPEND_FOLLOW, pos=pos, cases=cases,
                          cost=cost),
                ],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        partials=[program(spend="")],
        assemble=dict(
            lines=[line for line in solution.splitlines() if line.strip() and not line.startswith("#")],
            distractors=[f"print(roster[\"{who}\"])", f"roster[{pos}][\"mana\"] = {want}",
                         f"{var}[\"mana\"] = {var}[\"mana\"] - cost"],
        ),
        another_way=[
            dict(angle="picture", label="A row of sheets", text=(
                "```text\nroster\n" + "".join(f"  [{i}]  {v}\n" for i, (v, _, _) in enumerate(HEROES)) + "```\n"
                "The list is numbered from 0. Each sheet inside it has a key on every value.")),
            dict(angle="step-by-step", text=(
                f"1. `roster[{pos}]` is one whole sheet.\n"
                "2. Then a key reads one line of it.\n"
                "3. To spend, read the old mana on the right, take `cost` away, and store it back under the same "
                "key on the left.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="spell-book",
            snippet="for member in party.members:",
            why=(
                "You have seen this list. Every caster came from `party.members`, a list of sheets like `roster`. "
                "And the barrier spell paid with `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]`."
            ),
        ),
        takeaway="Position first, then the key: `roster[1][\"name\"]`. Spend with `x[\"mana\"] = x[\"mana\"] - cost`.",
        wrong_answers=[
            dict(why="the starter (nothing printed)", code=starter, fails_at=1, message_contains=f"position {pos}"),
            dict(why=f"a name as the position: roster[\"{who}\"] (TypeError)",
                 code=program(read=f"print(roster[\"{who}\"])\n"), fails_at=0,
                 message_contains="list indices must be integers or slices, not str"),
            dict(why=f"a name as the position, then the key", code=program(read=f"print(roster[\"{who}\"][\"name\"])\n"),
                 fails_at=0, message_contains="list indices must be integers"),
            dict(why="counting from 1", code=program(read=f"print(roster[{pos + 1}][\"name\"])\n"),
                 fails_at=1 if pos + 1 < 4 else 0,
                 message_contains="Positions count from 0" if pos + 1 < 4 else "list index out of range"),
            dict(why="the whole sheet printed", code=program(read=f"print(roster[{pos}])\n"), fails_at=1,
                 message_contains="whole sheet"),
            dict(why="a label, then the whole sheet", code=program(read=f"print(\"Hero:\", roster[{pos}])\n"),
                 fails_at=1, message_contains="whole sheet"),
            dict(why="a label, then the whole roster (every name is in it)",
                 code=program(read="print(\"Roster:\", roster)\n"), fails_at=1, message_contains="whole roster"),
            dict(why="every name printed, so the right one is in there somewhere (position skipped)",
                 code=program(read="".join(f"print(roster[{i}][\"name\"])\n" for i in range(4))), fails_at=1,
                 message_contains="too, at position"),
            dict(why="the name typed (CMB)", code=program(read=f"print(\"{who}\")\n"), fails_at=1,
                 message_contains="types the name"),
            dict(why="read from the sheet's own variable, not through roster", code=program(read=f"print({var}[\"name\"])\n"),
                 fails_at=1, message_contains="not through `roster`"),
            dict(why="roster in the line, the name typed", code=program(read=f"print(\"{who}\", len(roster))\n"), fails_at=1,
                 message_contains="types the name"),
            dict(why="a dict read by position: roster[pos][0] (KeyError: 0)",
                 code=program(read=f"print(roster[{pos}][0])\n"), fails_at=0, message_contains="KeyError: 0"),
            dict(why="dot access on a sheet", code=program(read=f"print(roster[{pos}].name)\n"), fails_at=0,
                 message_contains="has no attribute 'name'"),
            dict(why="round brackets on the list", code=program(read=f"print(roster({pos})[\"name\"])\n"), fails_at=0,
                 message_contains="not callable"),
            dict(why="the key with no quotes", code=program(read=f"print(roster[{pos}][name])\n"), fails_at=0,
                 message_contains="name 'name' is not defined"),
            dict(why="CP2 the new mana typed (CMB; hero[\"mana\"] = 7-type)", code=program(spend=f"roster[{pos}][\"mana\"] = {want}\n"),
                 fails_at=2, message_contains=f"`cost = {follow_cost}`"),
            dict(why="CP2 the old mana typed", code=program(spend=f"roster[{pos}][\"mana\"] = {start} - cost\n"),
                 fails_at=2, message_contains="does not follow the old mana"),
            dict(why="CP2 the cost typed", code=program(spend=f"roster[{pos}][\"mana\"] = roster[{pos}][\"mana\"] - {cost}\n"),
                 fails_at=2, message_contains="does not follow `cost`"),
            dict(why="CP2 worked out, kept nowhere (BARE)", code=program(spend=f"roster[{pos}][\"mana\"] - cost\n"),
                 fails_at=2, message_contains="forgets it"),
            dict(why="CP2 a new variable (NEWBOX)", code=program(spend=f"mana = roster[{pos}][\"mana\"] - cost\n"),
                 fails_at=2, message_contains="your variable `mana`"),
            dict(why="CP2 a capital in the key (KEY)", code=program(spend=f"roster[{pos}][\"Mana\"] = roster[{pos}][\"mana\"] - cost\n"),
                 fails_at=2, message_contains='"Mana"'),
            dict(why="CP2 the cost added", code=program(spend=f"roster[{pos}][\"mana\"] = roster[{pos}][\"mana\"] + cost\n"),
                 fails_at=2, message_contains="went up"),
            dict(why="CP2 the subtraction the wrong way round", code=program(spend=f"roster[{pos}][\"mana\"] = cost - roster[{pos}][\"mana\"]\n"),
                 fails_at=2, message_contains="the cost minus the mana"),
            dict(why="CP2 another hero pays (the next position)",
                 code=program(spend=f"roster[{(pos + 1) % 4}][\"mana\"] = roster[{(pos + 1) % 4}][\"mana\"] - cost\n"),
                 fails_at=2, message_contains="Your line changed the mana at position"),
            dict(why="CP2 spent from the sheet's own variable, not through roster",
                 code=program(spend=f"{var}[\"mana\"] = {var}[\"mana\"] - cost\n"), fails_at=2,
                 message_contains="does not go through `roster`"),
            dict(why="CP2 a name as the position (TypeError)",
                 code=program(spend=f"roster[\"{who}\"][\"mana\"] = roster[\"{who}\"][\"mana\"] - cost\n"), fails_at=0,
                 message_contains="list indices must be integers"),
            dict(why="CP2 dot access", code=program(spend=f"roster[{pos}].mana = roster[{pos}].mana - cost\n"), fails_at=0,
                 message_contains="has no attribute 'mana'"),
        ],
        notes=_qc_meta("list-of-dicts,dict-write", "shelf,title,pages,torn", form, level="S2") + "\n"
        f"QC4 C5, form {form} (G4 R1): four sheets (name and mana from the party table) and `roster`; CP1 prints "
        f"the name at position {pos} ({who}), CP2 spends `cost = {cost}` from that hero's mana ({start} -> {want}). "
        "CP1: the roster kept, the name (a whole sheet or the whole roster named, label or not; other positions "
        "named, counting from 1 named; every name printed at once fails: 'too, at position'), then "
        "CMB (the roster reversed inside the check, so a typed name or "
        f"`{var}[\"name\"]` fails; each gets its own message from an AST look at the print, and an alias such as "
        f"`hero = roster[{pos}]` passes). CP2: the state (another hero changed, a near-miss key, NEWBOX, BARE, the sign), "
        f"then three reruns: `cost = {follow_cost}`, `{var}[\"mana\"] = {follow_mana}`, and the reversed roster "
        f"(through roster: `{var}[...]` pays from the wrong sheet). Fails on (spec): a typed number -> CMB; "
        f"`roster[\"{who}\"]` -> crash. support='none', explainer='lean'.",
    )


_QC_SUMMARY = (
    "Optional. Five short tasks and three questions, no hints. Pass all five tasks and get 2 of the 3 questions right "
    "to test out of Unit 5. A task you miss just shows Mar'tu where to start. Tasks you pass here stay ticked."
)
_STRETCH = "Want more? Lucky's side quest in Mar'tu's Ledger of Heroes."
_RECAP = ("A sheet, a value read and changed inside a card, a spell stored by name, a mended read with a mana "
          "test, and a spend through the roster.")


QC4_A = dict(
    kind="testout",
    id="qc4-a",
    title="Quick Check 5 · Form A",
    optional=True,
    minutes=14,
    summary=_QC_SUMMARY,
    questions_to_pass=2,
    exercises=[
        _qc_sheet("A", "lucky", "Lucky", (13, 26, 3), "luck", "Lucky: A key on every value. Even the armor."),
        _qc_inside("A", "gearshift", "Gearshift", 20,
                   [("dexterity", 13), ("wisdom", 15), ("magical_affinity", 10)], "wisdom", 11,
                   "Gearshift: Fifteen. Math checks out.", "Gearshift: Seventeen. Upgrade logged."),
        _qc_store("A", "book", "spell_name", "spell", "Glow", (2, 3), "Ember Shield", 5, 8, ("Frost Veil", 4, 11),
                  ("Spark", (1, 1)), ("Quiet Step", (3, 4)),
                  "Mar'tu: A new page, and Glow's page kept. That is a spell book, yes?"),
        _qc_mend("A", "Bomb Shell", 24, [("dexterity", 6), ("magical_affinity", 12)], 10, 7, 7,
                 "Bomb Shell: Read mended. Next.", "Bomb Shell: Works. Shield up."),
        _qc_roster("A", 1, 6, 4, 11, "Mar'tu: " + _RECAP + " That is Unit 5, yes? " + _STRETCH),
    ],
    notes=(
        "Quick Check 5 (the curriculum's Quick Check 4), form A (code tasks, in the spec's order C1-C5; Q1 lives in "
        "qc4-a-questions). Pass = every code task plus 2 of the 3 questions; a retake draws form B. The site gates on "
        "both (questions_to_pass=2, as Unit 2's QC2 gates on 3 of its 4: all but one), and the code tasks alone still "
        "cover the unit, `dict-in` included (C3 CP2's guard). Framing (G4 R25): it only shows Mar'tu where to start. "
        "Messages are lean (Unit 2 ruling): the slip and the evidence in brackets, never the fix or the finished line, "
        "every one a whole sentence (_lean_guard proves it at import). C1 opens with Mar'tu's three-line story recap for a student who tests out. "
        "Coverage (lint d): dict-make -> C1 (WA `\"Max_Mana\"` KEY, `{name: ...}` NameError, `=` for `:`, the missing "
        "comma and colon, a quoted number, values with no keys) and C3 CP1 (WA a key with a capital, unquoted keys); "
        "dict-read, dict-nested -> C2 CP1 (WA `gearshift[\"wisdom\"]` KeyError, a typed 15, dot, round brackets, a "
        "position) and C4 CP1 (WA left unmended, a typed 12, the key moved outside); dict-nested write -> C2 CP2 "
        "(the Unit 5 ruling: a gated write inside a card; WA a flat `gearshift[\"wisdom\"] = ...`, a typed 17, the "
        "15 in the sheet edited, NEWBOX, BARE, the sign); get-compare-act (objective 9) -> C4 CP2 (the campaign's "
        "chain, the student writes the mana test; WA typed `24 < 7`, `<=` on the edge, `cost < caster[\"mana\"]`, "
        "`caster[\"abilities\"][\"mana\"]`, a typed cost or mana, a second `if`); dict-key-from-variable -> C3 "
        "CP1 (WA `\"cost\"` in quotes) and CP2 (WA `book[\"spell_name\"]`, the typed name); dict-write -> C3 CP2 and C5 CP2 (WA a typed 14, "
        "the typed old mana or cost, NEWBOX, BARE, `\"Mana\"`, the sign); dict-in -> C3 CP2 (WA no ask, `cost` asked "
        "about, the quoted name, `in` for `not in`) and Q1 (`4 in book` -> True); list-of-dicts -> C5 CP1 (WA "
        "`roster[\"Gearshift\"]` TypeError, counting from 1, the typed name, `gearshift[\"name\"]`). The last task's "
        "pass line recaps the form and offers the stretch. support='none' and explainer='lean' everywhere: no hints, "
        "tracer or compare; glossary and read-aloud stay on. 14 minutes (the Unit 5 ruling, as Unit 4's): C2 and C4 "
        "each gained a goal-only step."
    ),
)

QC4_B = dict(
    kind="testout",
    id="qc4-b",
    title="Quick Check 5 · Form B",
    optional=True,
    minutes=14,
    summary=_QC_SUMMARY,
    questions_to_pass=2,
    exercises=[
        _qc_sheet("B", "bomb_shell", "Bomb Shell", (12, 24, 3), "fuse", "Bomb Shell: Logged. Works."),
        _qc_inside("B", "oogrish", "Oogrish", 18,
                   [("dexterity", 14), ("wisdom", 17), ("magical_affinity", 9)], "wisdom", 11,
                   "Oogrish: Seventeen. Steady, now.", "Oogrish: Nineteen. An old shell still learns."),
        _qc_store("B", "wards", "ward_name", "ward", "Stone Skin", (4, 6), "Thorn Ring", 7, 11, ("Mist Veil", 3, 5),
                  ("Iron Bark", (2, 2)), ("Moss Cloak", (5, 9)),
                  "Mar'tu: A new ward, and Stone Skin kept. That is a ward book, yes?"),
        _qc_mend("B", "Gearshift", 20, [("strength", 17), ("magical_affinity", 10)], 9, 8, 6,
                 "Gearshift: Read corrected. Math checks out.", "Gearshift: Mana test online. Barrier's holding."),
        _qc_roster("B", 3, 8, 5, 11, "Mar'tu: " + _RECAP + " That is Unit 5, yes? " + _STRETCH),
    ],
    notes=(
        "Quick Check 5 (the curriculum's Quick Check 4), form B (spec: Oogrish's sheet, a `wards` book and "
        "`roster[3]`): C1 Bomb Shell's sheet (12, "
        "24, 3); C2 Oogrish's wisdom, 17 (his inner card holds dexterity 14, wisdom 17 and magical affinity 9: his "
        "intelligence is also 17, so it is left out); C3 `wards` with Stone Skin (4, 6) and the new ward Thorn Ring "
        "(7, 11) built into `ward` and stored under `ward_name`; C4 `caster` is Gearshift's sheet (affinity 10, needed "
        "9, `cost = 8`); C5 `roster[3]` is Lucky (26 - 8 = 18; counting from 1 gives `roster[4]`, an IndexError). "
        "C2 CP2 trains Oogrish's wisdom (17 -> 19). Same coverage, order and rules as form A, 14 minutes. Q1 lives "
        "in qc4-b-questions; the site gates on 2 of its 3 questions too (questions_to_pass=2)."
    ),
)


# Lean, proved (as Unit 2's _leaned asserts its rewrites and Unit 4's _lean_guard its forms): no check names the fix.
_FIX_WORDS = {"Put", "Make", "Add", "Use", "Copy", "Read", "Store", "Take", "Print", "Change", "Replace", "Spend",
              "Fill", "Check", "Write", "Ask", "Indent", "Give", "Build", "Warn", "Swap", "Compare", "Set", "Spell",
              "Move", "Delete", "Remove", "Type", "Try", "Mend"}


def _lean_guard(form):
    """Quick Check messages are lean (Unit 2 ruling): the slip and the evidence, never the fix. Proved at import, two
    ways. (1) As Unit 4's guard: no check of a form's tasks holds a line of Mar'tu's version that the starter does not
    show, or that line's working part (the read, the store, the test). (2) No message in a check starts with a fix
    ("Put a colon ...", "Read it from the sheet ...", "Indent the store line ..."): every text in a check that opens a
    sentence is the slip or the evidence. "Keep ..." and "Leave ..." stay: they name the starter's own lines, never
    the task's fix."""
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
            for head in ("print(", "if", "elif"):
                if right.startswith(head):
                    right = right[len(head):].rstrip(":)")
            if right.strip("[]0123456789,-+") and len(right) >= 6:
                pieces.add(right)
        for cp in ex["checkpoints"]:
            for name, check_code in cp["checks"]:
                for node in _ast_guard.walk(_ast_guard.parse(check_code)):
                    if isinstance(node, _ast_guard.Constant) and isinstance(node.value, str):
                        # Text a student reads (it has `code` marks or ends a sentence) never shows a line of the fix.
                        shown_text = "`" in node.value or node.value.rstrip().endswith(".")
                        named = [piece for piece in pieces if shown_text and len(piece) >= 6 and piece in squash(node.value)]
                        assert not named, f"{form['id']}/{ex['id']}: the check {name!r} shows the fix {named[0]!r}"
                        first = node.value.strip().split(" ")[0] if " " in node.value.strip() else ""
                        assert first not in _FIX_WORDS, (f"{form['id']}/{ex['id']}: the check {name!r} opens a message "
                                                         f"with the fix: {node.value[:60]!r}")
    return form


_lean_guard(QC4_A)
_lean_guard(QC4_B)


def _qc_questions(form, keys_q, sheet_q, box_q):
    """keys_q / box_q = (code, answer, choices, explain, notes); sheet_q = (choices, answer, why_wrong, notes)."""
    def predict(qid, parts):
        code, answer, choices, explain, notes = parts
        return dict(type="predict", id=qid, q="What will this print?", code=code, answer=answer, choices=choices,
                    explain=explain, notes=notes)

    s_choices, s_answer, s_why, s_notes = sheet_q
    return dict(
        kind="quiz",
        id=f"qc4-{form.lower()}-questions",
        title=f"Quick Check 5 · Form {form} questions",
        optional=True,
        minutes=2,
        summary="Three questions that go with Quick Check 5. To pass the Quick Check, get 2 of the 3 right.",
        questions=[
            predict("in-looks-at-keys", keys_q),
            dict(
                type="mc",
                id="quotes-on-keys",
                q="Which sheet does Python accept?",
                choices=s_choices,
                answer=s_answer,
                why_wrong=s_why,
                explain=(
                    "Keys are text, so each one has quotes. A colon goes between a key and its value, and a comma "
                    "between the pairs. " + QUOTES_RULE
                ),
                notes=s_notes,
            ),
            predict("key-from-a-box", box_q),
        ],
        notes=(
            f"Quick Check 5, form {form} questions (scored with qc4-{form.lower()}: every code task plus 2 of these 3, "
            "questions_to_pass=2 on the form, as Unit 2's QC2 gates on 3 of its 4). The best score counts, so a retake "
            "can lift it. Q1 is the spec's; the quotes mc (Obj 1, the reconciliation card) and the key-from-a-box "
            "predict (Obj 5) are additions. No hints; read-aloud and glossary stay on. The right "
            "answers sit at varied positions (the Unit 5 ruling, as Unit 4's: form A second, third, third; form B "
            "fourth, first, second), and the site shuffles the rest."
        ),
    )


QC4_A_QUESTIONS = _qc_questions(
    "A",
    (
        "book = {\n"
        '    "Spark": 1,\n'
        '    "Frost Veil": 4,\n'
        "}\n"
        'print("Spark" in book)\n'
        'print("Glow" not in book)\n'
        "print(4 in book)\n",
        "True\nTrue\nFalse",
        ["True\nTrue\nTrue", "True\nTrue\nFalse", "True\nFalse\nFalse", "False\nTrue\nTrue"],
        (
            "`in` looks at the keys only. `\"Spark\"` is a key: `True`. `\"Glow\"` is not a key, so `not in` gives "
            "`True`. 4 is a value, not a key, so `4 in book` is `False`."
        ),
        "Skill dict-in (spec Q1: `in` / `not in` on keys and on a value). Distractors: True/True/True (the "
        "in-checks-values belief: `4 in book` -> True), not in read as in, and Spark missed.",
    ),
    (
        ['{name: "Pell", mana: 7}', '{"name" = "Pell", "mana" = 7}', '{"name": "Pell", "mana": 7}',
         '{"name": "Pell" "mana": 7}'],
        2,
        {
            0: "`name` with no quotes is a box name, so Python looks for a box called `name` and stops: "
               "NameError. Keys are text, so they need quotes.",
            1: "`=` puts a value in a box. Inside a sheet, a colon goes between each key and its value.",
            3: "A comma is missing after `\"Pell\"`, so Python stops: invalid syntax.",
        },
        "Skill dict-make (Obj 1). Distractors: an unquoted key (box names have no quotes, keys do), `=` for `:`, a "
        "missing comma.",
    ),
    (
        "book = {\n"
        '    "Glow": 2,\n'
        '    "Spark": 5,\n'
        "}\n"
        'spell_name = "Spark"\n'
        "print(book[spell_name])\n",
        "5",
        ["2", "Spark", "5", "an error"],
        (
            "No quotes means look inside the box: `spell_name` holds `\"Spark\"`, so Python reads Spark's page, 5. "
            "`book[\"spell_name\"]`, with quotes, would stop with a KeyError."
        ),
        "Skill dict-key-from-variable (Obj 5). Distractors: Glow's 2, the name itself, an error (the belief that "
        "`spell_name` is looked up as a key).",
    ),
)

QC4_B_QUESTIONS = _qc_questions(
    "B",
    (
        "wards = {\n"
        '    "Stone Skin": 4,\n'
        '    "Iron Bark": 6,\n'
        "}\n"
        'print("Iron Bark" in wards)\n'
        'print("Stone Skin" not in wards)\n'
        "print(6 in wards)\n",
        "True\nFalse\nFalse",
        ["True\nFalse\nTrue", "True\nTrue\nFalse", "False\nFalse\nFalse", "True\nFalse\nFalse"],
        (
            "`in` looks at the keys only. `\"Iron Bark\"` is a key: `True`. `\"Stone Skin\"` is a key too, so "
            "`not in` gives `False`. 6 is a value, not a key, so `6 in wards` is `False`."
        ),
        "Form B of in-looks-at-keys. Distractors: True/False/True (the in-checks-values belief), not in read as "
        "in, Iron Bark missed.",
    ),
    (
        ['{"name": "Orrin", "armor": 4}', '{name: "Orrin", armor: 4}', '{"name" = "Orrin", "armor" = 4}',
         '{"name" "Orrin", "armor": 4}'],
        0,
        {
            1: "`name` with no quotes is a box name, so Python looks for a box called `name` and stops: "
               "NameError. Keys are text, so they need quotes.",
            2: "`=` puts a value in a box. Inside a sheet, a colon goes between each key and its value.",
            3: "A colon is missing after `\"name\"`, so Python stops: invalid syntax.",
        },
        "Form B of quotes-on-keys. Distractors: an unquoted key, `=` for `:`, a missing colon. The names in the "
        "two forms' sheets (Pell, Orrin) are invented Tor names, never a student's own value (2.11).",
    ),
    (
        "wards = {\n"
        '    "Stone Skin": 4,\n'
        '    "Iron Bark": 6,\n'
        "}\n"
        'ward_name = "Stone Skin"\n'
        "print(wards[ward_name])\n",
        "4",
        ["6", "4", "Stone Skin", "an error"],
        (
            "No quotes means look inside the box: `ward_name` holds `\"Stone Skin\"`, so Python reads Stone Skin's "
            "page, 4. `wards[\"ward_name\"]`, with quotes, would stop with a KeyError."
        ),
        "Form B of key-from-a-box.",
    ),
)


# =============================================================================================
# Cheatsheet "Mar'tu's Chalk Notes: Dictionaries"
# =============================================================================================

CHALK_NOTES_4 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Dictionaries",
    summary="Everything from Unit 5 on one page. Printable.",
    entries=[
        dict(concept="A sheet: keys and values",
             code='hero = {\n    "name": "Lucky",\n    "mana": 26,\n}\nprint(hero)\n',
             output="{'name': 'Lucky', 'mana': 26}",
             note="Curly brackets hold the sheet (a dictionary). Each line is a key in quotes, a colon, its value and "
                  "a comma. (Lesson: Stat Sheets)"),
        dict(concept="Box names have no quotes. Keys do.",
             code='mana = 26\nhero = {"mana": 26}\nprint(mana)\nprint(hero["mana"])\n',
             output="26\n26",
             note="A box's name (a variable) never has quotes. A key is text inside the sheet, so it does. "
                  + QUOTES_RULE),
        dict(concept="Read by key",
             code='hero = {"name": "Lucky", "mana": 26}\nprint(hero["name"])\nprint(hero["mana"])\n',
             output="Lucky\n26",
             note="Square brackets, with the key in quotes, read one value."),
        dict(concept="Change a value by key",
             code='hero = {"name": "Lucky", "mana": 26}\nhero["mana"] = hero["mana"] - 3\nprint(hero["mana"])\n',
             output="23",
             note="The right side reads the old mana and takes 3 away. The left side stores the answer under the same "
                  "key. You've seen this: `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]`."),
        dict(concept="Add a new key",
             code='hero = {"name": "Lucky", "mana": 26}\nhero["glug"] = 2\nprint(hero)\n',
             output="{'name': 'Lucky', 'mana': 26, 'glug': 2}",
             note="A key the sheet doesn't have yet is added. A key it has is changed: a key is never there twice."),
        dict(concept="`in` and `not in` look at keys",
             code='book = {"Glow": 2, "Warm Hands": 3}\nprint("Glow" in book)\nprint("Fire Bolt" not in book)\n'
                  "print(2 in book)\n",
             output="True\nTrue\nFalse",
             note="2 is a value, not a key, so `2 in book` is `False`. You've seen this: "
                  "`if spell_name not in caster[\"spell_book\"]:`."),
        dict(concept="A key from a variable",
             code='book = {"Glow": 2, "Warm Hands": 3}\nspell_name = "Warm Hands"\nprint(book[spell_name])\n',
             output="3",
             note="No quotes: Python looks inside `spell_name` and finds `\"Warm Hands\"`. `book[\"spell_name\"]`, "
                  "with quotes, looks for a key spelled s-p-e-l-l-_-n-a-m-e, and stops with a KeyError."),
        dict(concept="A card inside a sheet",
             code='hero = {\n    "name": "Bomb Shell",\n    "abilities": {\n        "wisdom": 8,\n    },\n}\n'
                  'print(hero["abilities"]["wisdom"])\n',
             output="8",
             note="Outer key, then inner key. One key alone gives the whole inner card. You've seen this: "
                  "`caster[\"abilities\"][\"magical_affinity\"]`. (Lesson: Sheets Inside Sheets)"),
        dict(concept="Change a value inside a card",
             code='hero = {\n    "abilities": {\n        "wisdom": 8,\n    },\n}\n'
                  'w = hero["abilities"]["wisdom"]\nhero["abilities"]["wisdom"] = w + 3\n'
                  'print(hero["abilities"]["wisdom"])\n',
             output="11",
             note="Get it, change it, put it back. `w` gets the old wisdom, 8. The next line puts the new one, 11, "
                  "back in the same spot, with the same two keys on the left of `=`."),
        dict(concept="A list of sheets",
             code='roster = [\n    {"name": "Oogrish"},\n    {"name": "Gearshift"},\n    {"name": "Bomb Shell"},\n]\n'
                  'print(roster[2]["name"])\n',
             output="Bomb Shell",
             note="Position first, counting from 0, then the key. A list remembers order; each sheet remembers "
                  "meaning. In the campaign, a list like this was `party.members`."),
        dict(concept="Store by name",
             code='book = {}\nname = "Warm Hands"\nspell = {"mana_cost": 3}\nbook[name] = spell\nprint(book)\n',
             output="{'Warm Hands': {'mana_cost': 3}}",
             note="The key comes from the variable `name`, so the page is called Warm Hands. You've seen this: "
                  "`spell_book[spell_name] = spell`."),
        dict(concept="Store only when it is new",
             code='book = {"Glow": 2}\nname = "Warm Hands"\nif name not in book:\n    book[name] = 3\nprint(book)\n',
             output="{'Glow': 2, 'Warm Hands': 3}",
             note="`not in` asks first, so a page that is already there stays as it is. The store line is indented "
                  "under the `if`, so it runs only when the name is new."),
        dict(concept="Get it, compare, act",
             code='hero = {\n    "mana": 5,\n    "abilities": {"wisdom": 8},\n}\ncost = 4\n'
                  'skill = hero["abilities"]["wisdom"]\nif skill < 6:\n    print("Not wise enough.")\n'
                  'elif hero["mana"] < cost:\n    print("Needs more mana.")\nelse:\n    print("Cast!")\n',
             output="Cast!",
             note="Get it: read the value through every key. Compare: `<` asks *lower than*, so exactly enough "
                  "still casts. Act: only one branch of the chain runs. You've seen this: holding the barrier."),
        dict(concept="(extra) `.get()`: a default, not an error",
             code='hero = {"name": "Lucky"}\nprint(hero.get("glug", 0))\n',
             output="0",
             note="`.get` gives the second value when the key is missing, in place of a KeyError. (Article: Why "
                  "Does This Work? Keys and .get())"),
        dict(concept="Error: a key with no quotes", code='hero = {name: "Lucky"}\n',
             note="NameError: name 'name' is not defined. With no quotes, `name` is a box name. Keys are text: "
                  "`\"name\"`."),
        dict(concept="Error: `=` inside a sheet", code='hero = {"name" = "Lucky"}\n',
             note="SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='? Python's guess "
                  "is wrong here: inside a sheet, a colon goes between a key and its value."),
        dict(concept="Error: a missing comma", code='hero = {\n    "mana": 26\n    "glug": 2,\n}\n',
             note="SyntaxError: invalid syntax. Perhaps you forgot a comma? After a number, Python names that line. "
                  "After text, it names the next line."),
        dict(concept="Error: a missing colon", code='hero = {\n    "name": "Lucky",\n    "mana" 26,\n}\n',
             note="SyntaxError: ':' expected after dictionary key. Every key needs a colon before its value."),
        dict(concept="Error: a KeyError", code='hero = {"mana": 26}\nprint(hero["Mana"])\n',
             note="KeyError: 'Mana'. No key is spelled exactly like that. Check the spelling, the capitals and the "
                  "spaces."),
        dict(concept="Error: a skipped level",
             code='hero = {\n    "abilities": {\n        "wisdom": 8,\n    },\n}\nprint(hero["wisdom"])\n',
             note="KeyError: 'wisdom'. Wisdom lives inside `\"abilities\"`. Read the outer key first."),
        dict(concept="Error: a dot, not brackets", code='hero = {"mana": 26}\nprint(hero.mana)\n',
             note="AttributeError: 'dict' object has no attribute 'mana'. Read a sheet with square brackets and "
                  "the key in quotes."),
        dict(concept="Error: round brackets", code='hero = {"mana": 26}\nprint(hero("mana"))\n',
             note="TypeError: 'dict' object is not callable. Round brackets call a recipe. A sheet takes square "
                  "brackets."),
        dict(concept="Error: a position on a sheet", code='hero = {"mana": 26}\nprint(hero[0])\n',
             note="KeyError: 0. A sheet has no positions, only keys."),
        dict(concept="Error: a name as a list position", code='roster = [{"name": "Lucky"}]\nprint(roster["Lucky"])\n',
             note="TypeError: list indices must be integers or slices, not str. A list takes a position number."),
        dict(concept="Error: a variable's name in quotes",
             code='book = {"Glow": 2}\nspell_name = "Glow"\nprint(book["spell_name"])\n',
             note="KeyError: 'spell_name'. With quotes, Python looks for those exact letters. Without them, it "
                  "looks inside the variable."),
    ],
    notes="Cheatsheet: Dictionaries (the spec's entries in order, plus the three the Unit 5 ruling adds: a change "
          "inside a card in the two-step form of 4B-02, store only when it is new (4B-04 CP3) and get-compare-act "
          "(4B-05, objective 9); then `.get()` as an extra from the optional article, then the errors this unit "
          "catches). Entries with `output` are run and checked by the harness; the errors have none. The entries "
          "show the shapes the Quick Check asks for, with other names and values: `hero`, `book` and `roster`, "
          "wisdom 8 (plus 3), Warm Hands 3, `roster[2]`, a spend of 3, a cost of 4. Every code line is 36 "
          "characters or fewer (phone width).",
)


ITEMS = [QC4_A, QC4_A_QUESTIONS, QC4_B, QC4_B_QUESTIONS, CHALK_NOTES_4]
