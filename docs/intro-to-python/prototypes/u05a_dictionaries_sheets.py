"""Unit 5 "Dictionaries" ("Stat Sheets and Spell Books"), part a: Mar'tu remembers (4a-remembers), Lesson 4A
"Stat Sheets" and the optional Article 4-A1 "Why Does This Work? Keys and .get()".

Spec: design/curriculum.md, "## Unit 5 · Dictionaries", items 1 and 2 (u05a): 4a-remembers; 4A-01 to 4A-08 and 4A-S;
Article 4-A1. Introduces node:Dict (4A-02), op:In and op:NotIn (4A-06; `in` on lists is only in Unit 4's optional
3C, so the core path meets it here) and attr:get (Article 4-A1, optional). Lists are used only as Unit 4 plans them
(a list literal and a read by position in 4A-01 and in the warm-up). No loops, no nested dicts (Lesson 4B, u05b),
no `None` written in code.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN the spell book
(`spell = {"mana_cost": ..., ...}` and `spell_book[spell_name] = spell`), the mana bars (`"█" * caster["mana"]`,
`caster["max_mana"] - caster["mana"]`) and the barrier spell (`if spell_name not in caster["spell_book"]:`,
`caster["mana"] = caster["mana"] - spell["mana_cost"]`). Campaign links are "you've seen this, now you'll get it".
Every student has their own device; pair talk is optional and every checkpoint is solo.

Mar'tu's framing line: "A list remembers order. It does not remember meaning." (the unit intro and 4A-01).
UNIT is shared by u05a-u05c and the exporter rejects a field that differs between parts: martu_intro and goals were
copied verbatim from u05b's UNIT (written at the same time), so the parts agree.

Help ladder as fields (FORMAT.md, the order the site shows them, as the Unit 2 fix pass set it): hints[0] Where to
look (point; in a debug step "Read Python's last line first"), the middle hints Teach me (a tiny example with other
names, listed in foreign_names), the last hint Show me how: the step's own line in backticks ("Write `x = 1`."),
whose start up to its first `(` or `=` becomes Start me off. Then another_way, assemble (More structure), and
Compare with Mar'tu's version (the solution).
Terminology (2.9, with the teacher's Unit 5 ruling, which overrides 2.9's "label (key)"): "variable" from Unit 4 on
(Mar'tu may still say "box"); student-facing text never calls a dictionary key a "label". Mar'tu says "A dictionary
keeps a tag on every value. Python calls the tag a key." (the unit intro says "tag" too), then "key" from then on.
The quotes sentence stays word for word, because its "box with this label" means a variable: "Quotes mean these
exact letters. No quotes means look inside the box with this label." Its first use (4A-02's Learn pane and 'why'
angle) is followed by "*Box* here means a variable, like `mana = 26`. A key is never a box." "recipe (function)"
for `def` (4A-02's side quest, where the student writes the recipe).

Check codes (curriculum 2.5), built by the helpers below. Every check that re-runs the program does it inside the
check only, with its prints kept private, and puts stdout back:
  sheet_keys()    KEY: the variable holds a dictionary with exactly-spelled keys. Near misses (`"Max_Mana"`,
                  `"max mana"`, a plural, 1-2 edits) get "`gearshift` has a key `"Max_Mana"`. The task spells it
                  `"max_mana"`"; values with no keys at all (a set or a list of values only: "Each value needs its
                  key in front"), commas with no colons (a set that holds the keys), square brackets (a list that
                  holds the keys), a key kept in a variable of its own instead of the sheet (NEWBOX), the empty
                  starter sheet. A renamed variable gets NAME; the Example's sheet name (`bomb_shell`) gets LEFT;
                  part of a key (`"armor"`) counts as a near miss.
  sheet_values()  NUM / TEXT / SWAP for a sheet's values: a quoted number, a name that is not text or is empty,
                  the starter's 0 left in, two values swapped, a wrong number.
  out_line()      OUT with the first difference ("A space is missing right after `Gearshift:`."), Mar'tu's
                  wanted text only. Never the only check on a computed value (lint a): a follows() always comes next.
                  With `comma_line`, a print with commas between its pieces (or that printed line) is led by Unit
                  3's line: "A comma inside `print(...)` adds a space. Glue the pieces with `+` instead."
  follows()       CMB: `_rerun(changes)` swaps other values into the starter's `name = <literal>` lines (a whole
                  sheet, a list, a cost, a spell name) and the printed line or the sheet must follow. Each failure
                  is diagnosed (the max mana read for the mana, a typed number, half the line typed, a key added
                  to fit a slip, ...). A crash in the rerun gets "Use keys the sheet really has" for a KeyError.
  now_check()     the student's own run, with per-exercise diagnoses (`26 is at position 2: Lucky's max mana`).
  _ends_in()      a printed line whose last whole number is n; a printed list or sheet never counts, so
                  `print(lucky)` does not pass for one item.
  4A-05 SPENT     the new mana is the old mana minus the cost (both read from the student's own code), with
                  BARE (worked out, kept nowhere), NEWBOX (`mana = ...`), a near-miss key (`gearshift["Mana"] =`),
                  the sign the wrong way round, the cost added; then CMB on the cost and on the sheet.
  4A-06 IN_CHECK  CMB on `in`: the program runs with and without "Fire Bolt" in the book; a message must show
                  only when it is missing. Diagnoses the starter's `if False:` left as it is ("Replace `False`
                  with a question"), `in` for `not in`, an unconditional print, a value (a cost) asked about with
                  `in` ("`in` checks keys, never values"), a near-miss spell name (STREXACT).
  4A-S SOLO_SPENT the solo's undictated write: write-by-key's SPENT pattern on `oogrish` and `glow_cost` (BARE,
                  NEWBOX, a near-miss key, the sign, the cost added), then CMB with another sheet and
                  `glow_cost = 3` (a typed number, a typed 18, the max mana read, a second sheet). The last line
                  shows the mana left because CP1's checks compare it with the sheet as it is now, before and
                  after the spend. Lean messages: the kind of slip and the line ("Line 8 takes away a typed 4"),
                  never the fix (`follows(..., lead="_wl + ' '")` puts the line in front).
Messages: the fix first, then what happened, then the evidence in brackets, "(Mar'tu's check tried another sheet,
name "Pell" and mana 7, only inside the check: the line should show `Pell: 7 mana`.)", as in Units 2-4.
Invented values only ("Pell", an invented Tor name, as in the Unit 4 ruling; "Moth"); a student's own text is never
repeated back (2.11). No lesson codes in student-facing text.

Deviations from the spec, each small and noted on its exercise:
  * 4A-01's starter names the four positions in a comment (name, magical affinity, max mana, armor bonus), so the
    hook is a certain, early win (teacher decision 2: confidence first); the story beat is the pass line.
  * 4A-02's "predict hero["mana"] versus hero[mana]" is one predict on `hero[mana]` (a NameError); the question
    gives `hero["mana"]` -> 26 as the contrast. The reconciliation card is in the Learn pane (short form) and in
    full as the first another_way angle.
  * 4A-03's starter carries the hand-typed line `print("Gearshift: 20 mana")` as the placeholder to replace (S4),
    so the CMB lesson ("build it from the sheet") is visible from the start.
  * 4A-04 reads the max mana twice: line 6 prints it, line 7 works out the mana used (the mana-bar subtraction).
  * 4A-02's starter has no `def` (teacher ruling): Lucky's side quest has the student write Unit 3's recipe
    `max_mana_for(affinity)` above the sheet, then use it for the max mana.
  * 4A-07's 6-card quotes sort (G2 R11) is a one-click card sort on its 'picture' angle (another_way `sort`, the
    site request shipped with this unit): one click a card, then *Check my sort* marks each card and shows the
    answers, plus the pair-talk prompt.
  * Point-at-it (4A-05, G2 R9) is CP1's pass line, as in Units 1-2. 4A-05 CP2 (add `"fuel"`) is goal-only.
  * 4A-06's starter carries can-they-cast's scaffold, `if False:` with the message under it, so the fade runs:
    replace `False` (4A-06) -> replace `False` with nested reads (4B-05) -> write the whole `if` (Quick Check).
  * 4A-08 uses Lucky's sheet with three of the spec slips (`=` for `:`, an unquoted key, a dot); the capital-letter
    KeyError was cut (teacher ruling: it is practised in 4A-04 and checked alone in 4A-S). The `lucky.mana` slip
    sits on the right side of a mana subtraction (a second write-by-key rep).
  * 4A-S: seat A is the exercise (`oogrish["Mana"]`); seat B (`oogrish.mana`) is in its notes (meta), as in Units 2-3.
    A second, undictated step writes by key (`glow_cost`), so a write is checked solo.
  * Article 4-A1's try-it ("Lucky's canteen") has one checkpoint: `.get("glug", 0)`.
  * Nested reads (`hero["abilities"]["wisdom"]`) and the roster of sheets (`roster["Gearshift"]` versus
    `roster[1]["name"]`) are Lesson 4B (u05b); here the TypeError row for a text index is proven on a list
    (`lucky["armor_bonus"]` in 4A-01).

Phone width: every fenced picture or code block in prose, every Example, predict, quiz and article code keep lines
to 36 characters or fewer (checked by script). Editor code (starters, solutions) keeps sheets one key a line; a
glued `print(...)` line that cannot be split runs longer, as in Units 3-4.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u05a
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates, filled in per exercise)
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# Shared by every check: near-miss tests, the first-difference note, and `_rerun`, which runs the student's program
# again with other values swapped into its top-level `name = <literal>` lines (prints kept private).
_PRE = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
_g = globals()
_tree = _ast.parse(_source)
_Q = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def _try(_f):
    try:
        return bool(_f())
    except Exception:
        return False


def _show(_v):
    if type(_v).__name__ == 'str':
        return '"' + _v + '"'
    return str(_v)


def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _squash(_s):
    return _s.lower().replace('_', '').replace(' ', '').replace('-', '')


def _near(_a, _b):
    # KEY / NAME near miss: capitals, `_` or spaces, a plural, or 1-2 edits.
    if type(_a).__name__ != 'str' or _a == _b:
        return False
    _x, _y = _a.lower().strip(), _b.lower()
    return (_x == _y or _squash(_a) == _squash(_b) or _x.rstrip('s') == _y.rstrip('s')
            or (min(len(_x), len(_y)) >= 3 and _edits(_x, _y) <= 2))


def _made():
    _out = []
    for _n in _ast.walk(_tree):
        if type(_n).__name__ == 'Assign':
            for _t in _n.targets:
                if type(_t).__name__ == 'Name' and _t.id not in _out:
                    _out.append(_t.id)
    return _out


def _gone(_k):
    _close = [_m for _m in _made() if _m != _k and _near(_m, _k)]
    if _close:
        return 'Python matches names letter for letter: you wrote `' + _close[0] + '`, the task needs `' + _k + '`.'
    return 'Keep the variable `' + _k + '` from the starter: a line that starts `' + _k + ' = `.'


def _nums(_l):
    return _re.findall(r'-?\d+', _l)


def _ends_in(_ls, _n):
    # A printed line whose last whole number is _n. A printed list or sheet never counts.
    return any(_nums(_l) and _nums(_l)[-1] == str(_n) for _l in _ls if not _l.startswith(('[', '{', '(')))


def _gap(_got, _want):
    # The first difference between a printed line and the wanted line, in Mar'tu's words and values only.
    _i = 0
    while _i < len(_got) and _i < len(_want) and _got[_i] == _want[_i]:
        _i += 1
    _seen = _want[:_i].strip()
    _at = ('right after `' + _seen + '`') if _seen else 'at the start'
    if _i < len(_want) and _got[_i:] == _want[_i + 1:]:
        _c = _want[_i]
        return ('A space is missing ' + _at + '.') if _c == ' ' else ('The `' + _c + '` is missing ' + _at + '.')
    if _i < len(_got) and _got[_i + 1:] == _want[_i:]:
        return ('There is an extra space ' + _at + '.') if _got[_i] == ' ' else ('There is an extra mark ' + _at + '.')
    if _got.lower() == _want.lower():
        return 'Every capital counts: the line should read `' + _want + '`.'
    return 'Nearly. The line should read `' + _want + '`.'


def _lit_key(_var, _key):
    # The value the starter-style sheet `_var = {...}` gives `_key`, read from the code (None if not a literal).
    for _n in _tree.body:
        if (type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and getattr(_n.targets[0], 'id', '') == _var
                and type(_n.value).__name__ == 'Dict'):
            for _k, _x in zip(_n.value.keys, _n.value.values):
                if type(_k).__name__ == 'Constant' and _k.value == _key:
                    try:
                        return _ast.literal_eval(_x)
                    except Exception:
                        return None
    return None


def _rerun(_changes):
    _t = _ast.parse(_source)
    _found = []
    _sets = {}
    for _n in _t.body:
        if (type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id in _changes):
            _sets.setdefault(_n.targets[0].id, []).append(_n)
    for _k, _ns_ in _sets.items():
        _lits = [_n for _n in _ns_ if type(_n.value).__name__ in ('Constant', 'Dict', 'List')]
        for _n in (_lits or _ns_[:1]):
            _n.value = _ast.parse(repr(_changes[_k]), mode='eval').body
        _found.append(_k)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__', 'input': lambda *_a: ''}
    _keep = _sys.stdout
    _sys.stdout = _io.StringIO()
    _err = ''
    try:
        exec(compile(_t, 'main.py', 'exec'), _ns)
    except Exception as _x:
        _err = type(_x).__name__ + ': ' + str(_x)
    finally:
        _out = _sys.stdout.getvalue()
        _sys.stdout = _keep
    return _ns, [_l.strip() for _l in _out.splitlines() if _l.strip()], _found, _err


def _crash(_e, _ev, _what):
    if _e.startswith('KeyError') and _what == 'sheet':
        _lead = 'Use keys the sheet really has, spelled the same way, so your code works for any sheet.'
    elif _e.startswith('KeyError'):
        _lead = 'Read only keys that are really there, spelled the same way, so your code works for any ' + _what + '.'
    else:
        _lead = 'Make your code work for any ' + _what + '.'
    return _lead + ' With another ' + _what + ', Python stopped: ' + _e + ' ' + _ev + '.)'
'''


def _sub(body, **subs):
    for key, value in subs.items():
        body = body.replace("@" + key + "@", repr(value))
    return _PRE + body


def _chain(rules, indent="    "):
    """An if/elif chain over (condition, message) rules; each condition is guarded, so a check never crashes."""
    out = ""
    for i, (cond, message) in enumerate(rules):
        out += indent + ("if" if i == 0 else "elif") + " _try(lambda: (" + cond + ")):\n"
        out += indent + "    _msg = " + repr(message) + "\n"
    return out


def follows(label, changes, ev, ok, fix, said, rules=(), pre="", what="sheet", lead="''"):
    """CMB: re-run the program with `changes` (name -> value) swapped into its `name = <literal>` lines, inside the
    check only. `ok` is an expression over `_p` (the rerun's printed lines) and `_R` (`.get` on its names).
    The first matching rule's message (or `fix`) leads; the evidence follows in brackets: "(Mar'tu's check tried
    <ev>, only inside the check: <said>.)". `said` is an expression (it may use names `pre` computes); so is
    `lead`, put in front of the message (solo-4a: `_wl + ' '`, the line the slip is on)."""
    ev_txt = "(Mar'tu's check tried " + ev + ", only inside the check"
    code = (
        "_ch = " + repr(changes) + "\n"
        + pre
        + "_r, _p, _f, _e = _rerun(_ch)\n"
        "_ev = " + repr(ev_txt) + "\n"
        "_miss = [_k for _k in _ch if _k not in _f]\n"
        "assert not _miss, _gone(_miss[0] if _miss else '')\n"
        "assert not _e, _crash(_e, _ev, " + repr(what) + ")\n"
        "_R = _r.get\n"
        "_ok = _try(lambda: (" + ok + "))\n"
        "_msg = " + repr(fix) + "\n"
        "if not _ok:\n"
        + (_chain(rules) or "    pass\n")
        + "assert _ok, (" + lead + ") + _msg + ' ' + _ev + ': ' + (" + said + ") + '.)'\n"
    )
    return (label, _PRE + code)


def now_check(label, ok, fix, rules=(), pre=""):
    """The student's own run: `ok` over `_ls` (printed lines) and the student's names; rules diagnose a miss."""
    code = (
        pre
        + "_ls = _lines()\n"
        "_ok = _try(lambda: (" + ok + "))\n"
        "_msg = " + repr(fix) + "\n"
        "if not _ok:\n"
        + (_chain(rules) or "    pass\n")
        + "assert _ok, _msg\n"
    )
    return (label, _PRE + code)


_SHEET_KEYS = r'''
_name = @NAME@
_want = @KEYS@
_foreign = @FOREIGN@
_first = @FIRST@
_v = _g.get(_name)
_msg = ''
_left = [_m for _m in _made() if _m in _foreign]
# Values only, no keys at all: `{"Gearshift", 10, 20, 3}` (a set) or `["Gearshift", 10, 20, 3]` (a list).
_no_keys = type(_v).__name__ in ('set', 'list', 'tuple') and not _try(lambda: any(_k in _v for _k in _want))
if _name not in _g and _left and not [_m for _m in _made() if _near(_m, _name)]:
    # LEFT: the Example's sheet name copied.
    _msg = ('`' + _left[0] + '` comes from the Example. This task' + "'" + 's sheet is `' + _name + '`: keep `'
            + _name + ' = {` from the starter.')
elif _name not in _g:
    _msg = _gone(_name)
elif _no_keys:
    _msg = 'Each value needs its key in front: `' + _first + '`. Your sheet has values but no keys.'
elif type(_v).__name__ == 'set':
    _msg = ('`' + _name + '` has commas but no colons, so it is not a dictionary. Put `:` between each key and its '
            'value, like `"name": "Bomb Shell"`.')
elif type(_v).__name__ in ('list', 'tuple'):
    _msg = ('`' + _name + '` has square brackets, so it is a list. A sheet is a dictionary: curly brackets, with a '
            'key and a colon before each value.')
elif type(_v).__name__ != 'dict':
    _msg = '`' + _name + '` should hold a dictionary: curly brackets, with `"key": value` inside.'
else:
    for _k in _want:
        if _k in _v:
            continue
        # A near miss, or part of the key (`"armor"` for `"armor_bonus"`, `"affinity"` for `"magical_affinity"`).
        _close = [_x for _x in _v if _near(_x, _k) or (type(_x).__name__ == 'str' and len(_x) >= 4
                                                        and _x not in _want and (_x in _k or _k in _x))]
        if _close:
            _msg = ('`' + _name + '` has a key `' + _show(_close[0]) + '`. The task spells it `"' + _k + '"`: Python '
                    'matches keys letter for letter.')
        elif _k in _g and not _k.startswith('_'):
            _msg = ('`' + _k + '` is a variable of its own. Put it inside the sheet as a key instead: `"' + _k
                    + '": ...`.')
        elif not _v:
            _msg = ('The sheet is still empty. Inside the curly brackets, write each key in quotes, a colon, a value '
                    'and a comma.')
        else:
            _msg = 'Add the key `"' + _k + '"` to `' + _name + '`, with a colon and a value.'
        break
assert not _msg, _msg
'''


def sheet_keys(label, name, keys, foreign=(), first='"name": "Gearshift",'):
    """KEY: `name` holds a dictionary with every key in `keys`, spelled exactly (see the module docstring).
    `foreign`: the Example's sheet names (LEFT: "`bomb_shell` comes from the Example"). `first`: the sheet's first
    line, shown when the sheet has values but no keys."""
    return (label, _sub(_SHEET_KEYS, NAME=name, KEYS=list(keys), FOREIGN=list(foreign), FIRST=first))


_SHEET_VALUES = r'''
_name = @NAME@
_wants = @WANTS@
_owner = @OWNER@
_v = _g.get(_name)
_msg = ''
_numbers = dict((_k, _w) for _k, _w in _wants if _w != 'text')
for _k, _w in _wants:
    _at = '`' + _name + '["' + _k + '"]`'
    if type(_v).__name__ != 'dict' or _k not in _v:
        _msg = 'Keep the key `"' + _k + '"` in `' + _name + '`.'
        break
    _x = _v[_k]
    _t = type(_x).__name__
    if _w == 'text':
        if _t in ('int', 'float'):
            _msg = _at + ' holds a number. A name is text: put it in quotes.'
        elif _t != 'str':
            _msg = _at + ' should hold text, in quotes.'
        elif not _x.strip():
            _msg = _at + ' is empty text. Put the name between the quotes.'
    elif _t == 'str':
        if _x.strip().lstrip('+-').isdigit():
            _msg = _at + ' holds the text `"' + _x + '"`. Numbers don' + "'" + 't need quotes.'
        else:
            _msg = _at + ' holds text. It should hold the number ' + str(_w) + ', with no quotes.'
    elif _t != 'int':
        _msg = _at + ' should hold the whole number ' + str(_w) + '.'
    elif _x != _w:
        _swap = [_o for _o, _ow in _numbers.items() if _o != _k and _ow == _x]
        if _x == 0:
            _msg = _at + ' still holds 0. Fill in ' + _owner + ' value from the sheet.'
        elif _swap:
            _msg = (_at + ' holds ' + str(_x) + ', which is the `"' + _swap[0] + '"` value. Two lines may be '
                    'swapped: check each key against the sheet.')
        else:
            _msg = _at + ' holds ' + str(_x) + '. ' + _owner + ' sheet says ' + str(_w) + '.'
    if _msg:
        break
assert not _msg, _msg
'''


def sheet_values(label, name, wants, owner):
    """NUM / TEXT / SWAP: each (key, want) of `wants` holds text ('text', any non-empty text) or the number want."""
    return (label, _sub(_SHEET_VALUES, NAME=name, WANTS=[list(w) for w in wants], OWNER=owner))


_OUT_LINE = r'''
_want = @WANT@
_comma_line = @COMMA_LINE@
_ls = _lines()
_best = sorted(_ls, key=lambda _l: _edits(_l, _want))[:1]
_close = _best[0] if _best and _edits(_best[0], _want) <= 4 else ''
# Unit 3's line: a print with commas between its pieces (or the line it prints) adds a space.
_spread = bool(_comma_line) and (_comma_line in _ls or any(
    type(_c).__name__ == 'Call' and getattr(_c.func, 'id', '') == 'print' and len(_c.args) > 1
    for _c in _ast.walk(_tree)))
if _want not in _ls and _spread:
    assert False, 'A comma inside `print(...)` adds a space. Glue the pieces with `+` instead.'
assert _want in _ls, (_gap(_close, _want) if _close else @FIX@)
'''


def out_line(label, want, fix, comma_line=""):
    """OUT: a printed line reads exactly `want`; a near miss gets its first difference (Mar'tu's text only).
    `comma_line`: the line a print with commas would show (`Gearshift : 20 mana`); such a print is led by Unit 3's
    'A comma inside `print(...)` adds a space.'"""
    return (label, _sub(_OUT_LINE, WANT=want, FIX=fix, COMMA_LINE=comma_line))


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of dictionaries)
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
        'Write a dictionary with keys in quotes, `:` and commas, and say why keys have quotes when box names '
        "don't",
        'Read a value by its key, and mend a KeyError caused by spelling, capitals or a skipped level',
        'Change a value and add a key, including `hero["mana"] = hero["mana"] - cost`',
        'Ask whether a key is in a dictionary with `in` and `not in`',
        'Use a key kept in a variable: `book[spell_name]`, not `book["spell_name"]`',
        'Read and change values inside values: `hero["abilities"]["magical_affinity"]`',
        'Read from a list of sheets, like `roster[2]["name"]`',
        'Build a spell from variables and store it by name: `spell_book[spell_name] = spell`',
        'Get a value, compare it, and act on it with `if` / `elif` / `else`, like holding the barrier',
    ],
    campaign_links=["friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="dictionary",
        aliases=["dictionaries", "dict", "dicts"],
        plain=(
            "Values kept under keys, in curly brackets. Each key, then a colon, then its value. Commas go between."
        ),
        example='{"name": "Lucky", "mana": 26}',
    ),
    dict(
        term="key",
        aliases=["keys", "tag"],
        plain=(
            "The tag on one value in a dictionary. A key is text, so it has quotes: `\"mana\"`. Read its value "
            "with the key in square brackets."
        ),
        example='lucky["mana"]',
    ),
    dict(
        term="KeyError",
        aliases=["key error", "key errors"],
        plain=(
            "Python's message when a dictionary has no key spelled exactly like that. Check the spelling, the "
            "capitals and the spaces."
        ),
        example="KeyError: 'Max_Mana'",
    ),
    dict(
        term="not in",
        aliases=["in (a dictionary)"],
        plain=(
            "`in` asks whether a key is in a dictionary, and gives `True` or `False`. `not in` asks whether it is "
            "missing. Both look at the keys only, never the values."
        ),
        example='"Glow" not in spell_book',
    ),
    dict(
        term="AttributeError",
        aliases=["attribute error"],
        plain=(
            "Python's message when a dot asks for something that is not there. Read a dictionary with square "
            "brackets, not a dot: `lucky[\"mana\"]`, not `lucky.mana`."
        ),
        example="AttributeError: 'dict' object has no attribute 'mana'",
    ),
    dict(
        term=".get()",
        aliases=["get()"],
        plain=(
            "Reads a key gently. `hero.get(\"glug\", 0)` gives the value, or 0 when the key is missing, with no "
            "KeyError."
        ),
        example='hero.get("glug", 0)',
    ),
]

# =============================================================================================
# Mar'tu remembers... (4a-remembers)
# =============================================================================================

ROSTER_CODE = (
    "roster = [\n"
    '    ["Oogrish", 18],\n'
    '    ["Gearshift", 20],\n'
    '    ["Bomb Shell", 24],\n'
    '    ["Lucky", 26],\n'
    "]\n"
)

REMEMBERS_4A = dict(
    kind="quiz",
    id="4a-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from Units 3 and 4. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 4A. Q1 is the nested-list read from Unit 4's "
        "lists-inside-lists exercise (`roster[1][1]`, the stepping stone to sheets; distractor 18 is row 0, the "
        "count-from-1 slip). Q2 is the def/return item (from Unit 4 on one warm-up item is always def/return, 2.1): "
        "`max_mana_for(9)`, Unit 3's recipe; its explain names `None` as 'nothing came back' (the Unit 4 ruling's "
        "wording). A miss shows the answer and a one-line why, with no red X. The right answers sit at positions 4 "
        "and 2 (the site shuffles too)."
    ),
    questions=[
        dict(
            type="predict",
            id="row-then-item",
            q="What will this print?",
            code=ROSTER_CODE + "print(roster[1][1])\n",
            choices=["Gearshift", "18", "['Gearshift', 20]", "20"],
            answer="20",
            explain=(
                "`roster[1]` is row 1, counting from 0: `[\"Gearshift\", 20]`. Then `[1]` is item 1 of that row: "
                "20. Outer number first, then inner."
            ),
        ),
        dict(
            type="predict",
            id="max-mana-for-nine",
            q="What will this print?",
            code="def max_mana_for(affinity):\n    total = affinity * 2\n    return total\n\nprint(max_mana_for(9))\n",
            choices=["9", "18", "total", "None"],
            answer="18",
            explain=(
                "The call hands over 9, so `affinity` is 9 inside the recipe. `total` is 18, and `return` hands "
                "18 back to the `print`. If the recipe had no `return`, nothing would come back, and `print` would "
                "show `None`."
            ),
        ),
    ],
)

# =============================================================================================
# Lesson 4A "Stat Sheets"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 4A-01 which-number-is-which (protected story beat)
# ---------------------------------------------------------------------------------------------

WHICH_HEAD = "# name, magical affinity,\n# max mana, armor bonus\n" + 'lucky = ["Lucky", 13, 26, 3]\n'
WHICH_STARTER = WHICH_HEAD + "print(lucky[2])\n"


def _which(line="print(lucky[3])"):
    return WHICH_HEAD + line + "\n"


WHICH_NUMBER = dict(
    id="which-number-is-which",
    title="Which number is which?",
    martu=(
        "A list remembers order. It does not remember *meaning*.\n"
        "Here is Lucky as a [[list]]: his name, his magical affinity, his max mana and his armor bonus, in that "
        "order.\n"
        "Print his armor bonus. Which position is it? Count from 0, yes?"
    ),
    example='drill = ["Run", 12, 9]\nprint(drill[2])\n',
    example_output="9",
    names=["lucky"],
    predict=dict(
        q="Before you press Run: what will `print(lucky[2])` show?",
        choices=["13", "3", "26", "Lucky"],
        answer=2,
        explain=(
            "Positions start at 0. The name is 0, 13 is 1, and 26 is 2: his max mana. Did you have to count? "
            "That is the trouble with a list of numbers."
        ),
    ),
    pair_talk=(
        "Pair talk: each of you guesses the armor bonus's position before you run. Compare guesses, then each of "
        "you checks on your own screen."
    ),
    starter=WHICH_STARTER,
    checkpoints=[
        dict(
            id="print-the-armor",
            text="Change the `print` so it shows Lucky's armor bonus, read from `lucky`.",
            dictated=False,
            hints=[
                "Count the positions in the list from 0: the name is 0. Which position is the armor bonus?",
                "Positions start at 0. In `drill = [\"Run\", 12, 9]`, `drill[0]` is `\"Run\"` and `drill[2]` is 9.",
                "Write `print(lucky[3])` in place of `print(lucky[2])`.",
            ],
            checks=[
                now_check(
                    "the armor bonus shows",
                    ok="_ends_in(_ls, 3)",
                    fix="Print the armor bonus, read from `lucky` with its position. Count from 0.",
                    rules=[
                        ("any(_l.startswith('[') for _l in _ls)",
                         "That prints the whole list. Print one item: its position goes in square brackets after "
                         "`lucky`."),
                        ("_ends_in(_ls, 26)",
                         "26 is at position 2: Lucky's max mana. The armor bonus is the next item along."),
                        ("_ends_in(_ls, 13)",
                         "13 is at position 1: his magical affinity. The armor bonus is the last item."),
                        ("'Lucky' in _ls",
                         "`Lucky` is at position 0: his name. The armor bonus is the last item. Count from 0."),
                    ],
                ),
                follows(
                    "the armor bonus follows the list",
                    {"lucky": ["Pell", 11, 22, 5]},
                    ev='another list, `["Pell", 11, 22, 5]`',
                    ok="_ends_in(_p, 5)",
                    fix="Read the armor bonus from `lucky` with its position, so it follows the list.",
                    said="'no line ended in its armor bonus, 5'",
                    rules=[("lucky != ['Lucky', 13, 26, 3]",
                            "Keep the list as the starter has it, `[\"Lucky\", 13, 26, 3]`, and change only the "
                            "`print`: read the armor bonus by its position.")],
                    what="list",
                ),
            ],
            pass_line="Mar'tu: You had to remember that position 3 means armor. Python can remember for you.",
        ),
    ],
    solution=_which(),
    assemble=dict(
        lines=["lucky = [\"Lucky\", 13, 26, 3]", "print(lucky[3])"],
        distractors=["print(lucky[4])", "print(3)", "print(lucky[2])"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Positions under the list",
            text=(
                "Each item has a position, counting from 0:\n"
                "```text\n[\"Lucky\", 13, 26, 3]\n    0     1   2  3\n```\n"
                "Nothing in the list says which number is armor. Only the order does."
            ),
        ),
        dict(
            angle="everyday",
            label="Lockers with no tags",
            text=(
                "A row of lockers with no tags. You must remember that locker 3 holds the armor. Forget once, and "
                "you grab the wrong thing."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "My chalk wall is a good list: its order IS its meaning, oldest gap first. A hero's numbers have no "
                "order like that. They have meanings."
            ),
        ),
        dict(angle="shorter", text="Count from 0: name 0, affinity 1, max mana 2, armor 3."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]',
        why=(
            "In the mana bars you never wrote `caster[2]`. You wrote `caster[\"mana\"]`: a tag, not a position. "
            "That is a dictionary. You make one next."
        ),
    ),
    takeaway="A list keeps order, so you must remember what each position means: `lucky[3]` is the armor only because you counted.",
    wrong_answers=[
        dict(why="starter unchanged: position 2 is the max mana", code=WHICH_STARTER, fails_at=1,
             message_contains="max mana"),
        dict(why="counting from 1: position 4 does not exist", code=_which("print(lucky[4])"), fails_at=0,
             message_contains="list index out of range"),
        dict(why="the armor bonus typed by hand (CMB)", code=_which("print(3)"), fails_at=1,
             message_contains="follows the list"),
        dict(why="position 1 (the affinity)", code=_which("print(lucky[1])"), fails_at=1, message_contains="affinity"),
        dict(why="position 0 (the name)", code=_which("print(lucky[0])"), fails_at=1, message_contains="position 0"),
        dict(why="the whole list printed (its last number is 3, but it is not one item)", code=_which("print(lucky)"),
             fails_at=1, message_contains="whole list"),
        dict(why="a key used on a list (the TypeError row: a list wants a position, not text)",
             code=_which('print(lucky["armor_bonus"])'), fails_at=0,
             message_contains="list indices must be integers"),
        dict(why="round brackets for a read", code=_which("print(lucky(3))"), fails_at=0,
             message_contains="not callable"),
        dict(why="the list reordered so position 2 holds the 3 (the list changed to fit the read)",
             code=WHICH_HEAD.replace("13, 26, 3]", "13, 3, 26]") + "print(lucky[2])\n", fails_at=1,
             message_contains="Keep the list as the starter has it"),
        dict(why="worked out from the list's length, not read (len(lucky) - 1 is 3 too)",
             code=_which("print(len(lucky) - 1)"), fails_at=1, message_contains="follows the list"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-index", solo="false", dictates="", foreign_names="drill")
        + "\n"
        "Protected story beat (2P1, 4A-01, 5A-05, 5B-04): a student who tests out gets it as a 'Mar'tu's notes' "
        "line. Hook (P): the predict asks for `lucky[2]` (26, his max mana; written third of four), then CP1 [ND] "
        "prints the armor bonus (position 3 or -1). Checks: the student's run ends a line in 3 (a printed list "
        "never counts), then CMB with another list `[\"Pell\", 11, 22, 5]`, so a typed `print(3)` fails. The "
        "starter's comment labels the four positions so the win is certain (teacher decision 2). Mar'tu's spec "
        "line is the pass line. The TypeError row for a text index on a list (`lucky[\"armor_bonus\"]`) is proven "
        "here; Lesson 4B proves `roster[\"Gearshift\"]`."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-02 make-a-sheet (intro node:Dict)
# ---------------------------------------------------------------------------------------------

# Lucky's side quest only: the student writes Unit 3's recipe above the sheet (the starter has no `def`).
SHEET_RECIPE = "def max_mana_for(affinity):\n    return affinity * 2\n\n"
# "*Box* here means a variable": said right after the quotes sentence's first use (teacher ruling).
BOX_NOTE = "*Box* here means a variable, like `mana = 26`. A key is never a box."
SHEET_STARTER = (
    "gearshift = {\n"
    '    # "name", "magical_affinity",\n'
    '    # "max_mana", "armor_bonus"\n'
    "}\n"
)
SHEET_KEYS = ["name", "magical_affinity", "max_mana", "armor_bonus"]


def _sheet(name='"Gearshift"', affinity="10", max_mana="20", armor="3", lines=None):
    body = lines or [
        f'    "name": {name},',
        f'    "magical_affinity": {affinity},',
        f'    "max_mana": {max_mana},',
        f'    "armor_bonus": {armor},',
    ]
    return "gearshift = {\n" + "\n".join(body) + "\n}\n"


SHEET_SOLUTION = _sheet()

MAKE_A_SHEET = dict(
    id="make-a-sheet",
    title="Make a sheet",
    martu=(
        "A [[dictionary]] keeps a tag on every value. Python calls the tag a [[key]]. Run the Example: Bomb "
        "Shell's sheet.\n"
        "Curly brackets hold the sheet. Each line inside is a key, a colon, its value, then a comma.\n"
        "Wait: quotes on a name? A box's name never has quotes: `mana = 26`. A key is text inside the sheet, so it "
        "does: `{\"mana\": 26}`. " + QUOTES_RULE + " " + BOX_NOTE + "\n"
        "Gearshift's sheet. Copy the keys exactly:\n"
        "```text\nGEARSHIFT\nname               Gearshift\nmagical_affinity   10\nmax_mana           20\n"
        "armor_bonus        3\n```"
    ),
    introduces=["node:Dict"],
    example='bomb_shell = {\n    "name": "Bomb Shell",\n    "dexterity": 6,\n}\nprint(bomb_shell["dexterity"])\n',
    example_output="6",
    names=["gearshift"],
    pick="Gearshift",
    predict=dict(
        q="`hero = {\"mana\": 26}`, so `print(hero[\"mana\"])` shows 26. What does `print(hero[mana])` show?",
        code='hero = {"mana": 26}\nprint(hero[mana])\n',
        choices=["26", "mana", "ERROR: name 'mana' is not defined"],
        answer=2,
        explain=(
            "No quotes means look inside the box with this label. There is no box called `mana`, only a key "
            "inside `hero`, so Python stops: *not defined*. With quotes, `hero[\"mana\"]` reads the key: 26."
        ),
    ),
    pair_talk=(
        "Pair talk: read your sheet to your partner, one line at a time: the key, then *colon*, then the value. "
        "Each of you types your own sheet."
    ),
    starter=SHEET_STARTER,
    checkpoints=[
        dict(
            id="four-keys",
            text=(
                "Make `gearshift` with the keys `\"name\"`, `\"magical_affinity\"`, `\"max_mana\"` and "
                "`\"armor_bonus\"`. Any value is fine for now, like 0."
            ),
            dictated=False,
            hints=[
                "Each line inside the curly brackets is a key in quotes, a colon, a value, then a comma. Copy each "
                "key from the comment, letter for letter.",
                "In the Example, `\"dexterity\": 6,` is one line: the key in quotes, `:`, the value, a comma.",
                "Write one line for each key, like `\"max_mana\": 0,`, under `gearshift = {`.",
            ],
            checks=[sheet_keys("gearshift has the four keys", "gearshift", SHEET_KEYS, foreign=["bomb_shell"])],
        ),
        dict(
            id="fill-the-values",
            text="Fill in Gearshift's values from his sheet: his name as text, then three numbers.",
            dictated=False,
            hints=[
                "Look at Gearshift's sheet in the Learn pane. Text goes in quotes. Numbers have no quotes.",
                "`\"dexterity\": 6,` holds a number, with no quotes. `\"name\": \"Bomb Shell\",` holds text, in quotes.",
                "Write `\"name\": \"Gearshift\",` first, then `\"magical_affinity\": 10,`, `\"max_mana\": 20,` and "
                "`\"armor_bonus\": 3,`.",
            ],
            checks=[
                sheet_values(
                    "the values match the sheet", "gearshift",
                    [("name", "text"), ("magical_affinity", 10), ("max_mana", 20), ("armor_bonus", 3)],
                    "Gearshift's",
                ),
            ],
            pass_line="Gearshift: Visor dims. Sheet logged.",
        ),
    ],
    solution=SHEET_SOLUTION,
    partials=[_sheet(name='""', affinity="0", max_mana="0", armor="0")],
    assemble=dict(
        lines=["gearshift = {", '    "name": "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20,',
               '    "armor_bonus": 3,', "}"],
        distractors=['    name: "Gearshift",', '    "max_mana" = 20,', '    "Max_Mana": 20,'],
    ),
    another_way=[
        dict(
            angle="why",
            label="Wait, quotes on names?",
            text=(
                "A box's name (a variable) never has quotes: `mana = 26`. A key inside a dictionary is a piece of "
                "text, so it does: `{\"mana\": 26}`.\n" + QUOTES_RULE + " " + BOX_NOTE
            ),
        ),
        dict(
            angle="picture",
            label="Keys and values in one big box",
            text=(
                "The sheet is one big box. Inside, every value has its key:\n"
                "```text\ngearshift\n+------------------------+\n| \"name\"     \"Gearshift\" |\n"
                "| \"max_mana\"          20 |\n+------------------------+\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A stat sheet",
            text=(
                "A stat sheet names every line: *armor bonus: 3*. You find a line by its name, not its number. A "
                "dictionary works the same way."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `gearshift = {` opens the sheet.\n"
                "2. Each line: a key in quotes, `:`, the value, `,`.\n"
                "3. `}` closes the sheet."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "At the Institute, each student had a record card: a tag and a value on every line. Mine said "
                "*talks too little*. Python keeps the same kind of card."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "In the spell book part, `spell = {...}` held three keys: `\"mana_cost\"`, `\"required_affinity\"` "
                "and `\"spell_function\"`. Each key had quotes, a colon and a value. That was a dictionary."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Let the recipe do it",
        text=(
            "What's in it for me? Less math. Above the sheet, write Unit 3's recipe `max_mana_for(affinity)`: it "
            "hands back twice the affinity. Then put `max_mana_for(10)` in the sheet in place of the 20."
        ),
        hints=[
            "A recipe call can sit where a value goes. Python works it out first, then stores what it hands back.",
            "`def double(n):` with `return n * 2` indented under it hands back twice whatever comes in.",
            "Write `def max_mana_for(affinity):` with `return affinity * 2` under it, above the sheet. Then change "
            "the max mana line to `\"max_mana\": max_mana_for(10),`.",
        ],
        checks=[
            (
                "max_mana comes from the recipe",
                _PRE + r'''
# The recipe first: written above the sheet, handing back twice the affinity (its prints kept private).
_defs = [_n.name for _n in _ast.walk(_tree) if type(_n).__name__ == 'FunctionDef']
_f = _g.get('max_mana_for')
_close = [_d for _d in _defs if _d != 'max_mana_for' and _near(_d, 'max_mana_for')]
assert callable(_f) or not _close, ('Python matches names letter for letter: you wrote `' + (_close[0] if _close
                                    else '') + '`, the task needs `max_mana_for`.')
assert callable(_f), ('Write the recipe above the sheet first: `def max_mana_for(affinity):`, with '
                      '`return affinity * 2` indented under it.')
_keep = _sys.stdout
_sys.stdout = _io.StringIO()
try:
    _twice = _try(lambda: _f(7) == 14)
finally:
    _sys.stdout = _keep
assert _twice, 'The recipe should hand back twice the affinity: end it with `return affinity * 2`.'
_calls = []
for _n in _tree.body:
    if (type(_n).__name__ == 'Assign' and getattr(_n.targets[0], 'id', '') == 'gearshift'
            and type(_n.value).__name__ == 'Dict'):
        for _k, _x in zip(_n.value.keys, _n.value.values):
            if (type(_k).__name__ == 'Constant' and _k.value == 'max_mana' and type(_x).__name__ == 'Call'
                    and getattr(_x.func, 'id', '') == 'max_mana_for'):
                _calls.append(_x)
assert _calls, 'Set `"max_mana"` with the recipe: write `max_mana_for(10)` where the 20 is.'
assert gearshift.get('max_mana') == 20, "Hand the recipe Gearshift's magical affinity, 10."
''',
            ),
        ],
        solution=SHEET_RECIPE + _sheet(max_mana="max_mana_for(10)"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet='spell = {\n    "mana_cost": 0,\n    "required_affinity": 0,\n}',
        why=(
            "You filled in a dictionary like this in the spell book part. Every key had quotes, a colon and a "
            "value. Now you know why the keys had quotes."
        ),
    ),
    takeaway="A dictionary is `{ }` holding `\"key\": value` lines with commas. Keys are text, so they have quotes.",
    wrong_answers=[
        dict(why="starter unchanged (the empty sheet)", code=SHEET_STARTER, fails_at=1, message_contains="empty"),
        dict(why="a key with no quotes (G1 R6: box names have no quotes, keys do)",
             code=_sheet(lines=['    name: "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="name 'name' is not defined"),
        dict(why="= for : inside the sheet (the box habit)",
             code=_sheet(lines=['    "name" = "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="cannot assign to literal"),
        dict(why="a missing comma after a text value: Python reports the NEXT line",
             code=_sheet(lines=['    "name": "Gearshift"', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="a missing comma after a number: Python reports that line ('forgot a comma')",
             code=_sheet(lines=['    "name": "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="forgot a comma"),
        dict(why="a missing colon",
             code=_sheet(lines=['    "name" "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="= for : on a later line of the sheet (there 3.13 says ':' expected, not 'cannot assign')",
             code=_sheet(lines=['    "name": "Gearshift",', '    "magical_affinity" = 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="':' expected after dictionary key"),
        dict(why="the key's closing quote left off (an unclosed quote, the class's common slip)",
             code=_sheet(lines=['    "name: "Gearshift",', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="unterminated string literal"),
        dict(why="the value's closing quote left off (an unclosed quote, the class's common slip)",
             code=_sheet(lines=['    "name": "Gearshift,', '    "magical_affinity": 10,', '    "max_mana": 20,',
                                '    "armor_bonus": 3,']),
             fails_at=0, message_contains="unterminated string literal"),
        dict(why="key capitals: Max_Mana (KEY)", code=_sheet().replace('"max_mana"', '"Max_Mana"'), fails_at=1,
             message_contains='"Max_Mana"'),
        dict(why="key with a space for _ (KEY)", code=_sheet().replace('"max_mana"', '"max mana"'), fails_at=1,
             message_contains="letter for letter"),
        dict(why="commas but no colons: a set, not a dictionary",
             code='gearshift = {"name", "Gearshift", "max_mana", 20}\n', fails_at=1,
             message_contains="no colons"),
        dict(why="values with no keys, in curly brackets (a set of values only)",
             code='gearshift = {"Gearshift", 10, 20, 3}\n', fails_at=1, message_contains="values but no keys"),
        dict(why="a list of the four values (the 4A-01 habit): values with no keys",
             code='gearshift = ["Gearshift", 10, 20, 3]\n', fails_at=1, message_contains="values but no keys"),
        dict(why="a list that holds the keys too: square brackets, not curly",
             code='gearshift = ["name", "Gearshift", "max_mana", 20]\n', fails_at=1,
             message_contains="square brackets"),
        dict(why="separate boxes instead of keys (box versus key)",
             code='name = "Gearshift"\nmax_mana = 20\ngearshift = {}\n', fails_at=1,
             message_contains="variable of its own"),
        dict(why="a renamed sheet (NAME)", code=_sheet().replace("gearshift = {", "Gearshift = {"), fails_at=1,
             message_contains="letter for letter"),
        dict(why="the Example's sheet name copied (LEFT, A-05/A-07/A-08 player_name habit)",
             code=_sheet().replace("gearshift = {", "bomb_shell = {"), fails_at=1,
             message_contains="`bomb_shell` comes from the Example"),
        dict(why="part of a key: armor for armor_bonus (KEY)", code=_sheet().replace('"armor_bonus"', '"armor"'),
             fails_at=1, message_contains='has a key `"armor"`'),
        dict(why="placeholders left (CP1 only)", code=_sheet(name='"Gearshift"', affinity="0", max_mana="0", armor="0"),
             fails_at=2, message_contains="still holds 0"),
        dict(why="numbers in quotes (NUM)", code=_sheet(max_mana='"20"'), fails_at=2,
             message_contains="don't need quotes"),
        dict(why="affinity and max mana swapped (SWAP)", code=_sheet(affinity="20", max_mana="10"), fails_at=2,
             message_contains="swapped"),
        dict(why="the name with no quotes (A-05/A-08 unquoted text)", code=_sheet(name="Gearshift"), fails_at=0,
             message_contains="name 'Gearshift' is not defined"),
        dict(why="the name as a number", code=_sheet(name="10"), fails_at=2, message_contains="A name is text"),
        dict(why="a wrong number", code=_sheet(armor="2"), fails_at=2, message_contains="sheet says 3"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="dict-make", solo="false", dictates="",
             foreign_names="bomb_shell,dexterity,hero,double,n") + "\n"
        "CP1 [ND] KEY: the four keys, any values (partial 1 has 0s and empty text). CP2 [ND] NUM/TEXT/SWAP: any "
        "non-empty text for the name (personal values pass, lint e), 10, 20, 3 from the party table. Catches (spec): "
        "an unquoted key -> NameError (explainer rule 9, 'keys are text, so they need quotes'); `=` for `:` -> "
        "Python's 'cannot assign to literal here' (site request: inside `{ }` the explainer row should say 'Use `:` "
        "between a key and its value', not the box-name row); a missing comma after a text value is reported on the "
        "NEXT line ('invalid syntax'), after a number on that line ('forgot a comma'), both verified in 3.13 (the "
        "dict-comma row); `\"Max_Mana\"` -> KEY. Also: values with no keys (a set or a list of values only: 'Each "
        "value needs its key in front'), a set that holds the keys (commas, no colons), a list that holds the "
        "keys, boxes made instead of keys. The reconciliation card (G1 R6) is in the Learn pane and in full as the "
        "first angle; both end with the box note ('*Box* here means a variable'). Teacher ruling: a key is called "
        "a tag once ('Python calls the tag a key'), then 'key'; never 'label'. BQ (dict + recipe): the starter has "
        "no `def` (teacher ruling), so the student writes Unit 3's `max_mana_for(affinity)` above the sheet, then "
        "`\"max_mana\": max_mana_for(10)`; the check asks for the recipe first ('Write the recipe above the sheet "
        "first'; a near-miss name is named), then that it hands back twice the affinity, then the call in the "
        "sheet. Any other name passes (lint e)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-03 read-by-key
# ---------------------------------------------------------------------------------------------

READ_HEAD = (
    "gearshift = {\n"
    '    "name": "Gearshift",\n'
    '    "mana": 20,\n'
    '    "max_mana": 20,\n'
    "}\n"
    'print(gearshift["mana"])\n'
)
READ_STARTER = READ_HEAD + "# This line is typed by hand.\n# Build it from gearshift:\n" + 'print("Gearshift: 20 mana")\n'
READ_LINE = 'print(gearshift["name"] + ": " + str(gearshift["mana"]) + " mana")'


def _read(line=READ_LINE):
    return READ_HEAD + line + "\n"


OTHER_SHEET = {"name": "Pell", "mana": 7, "max_mana": 31}
OTHER_EV = 'another sheet, name `"Pell"`, mana 7 and max mana 31'

READ_BY_KEY = dict(
    id="read-by-key",
    title="Read by key",
    martu=(
        "To read a value, write the sheet's name, then the key in square brackets: `gearshift[\"mana\"]`. Python "
        "finds the key and hands you its value.\n"
        "The brackets look like a list's. Inside, a list wants a position. A dictionary wants a key.\n"
        "Then let the code build the line, the way you did in Unit 1."
    ),
    example='bomb_shell = {"mana": 24}\nmana_now = bomb_shell["mana"]\nprint("Mana: " + str(mana_now))\n',
    example_output="Mana: 24",
    names=["gearshift"],
    predict=dict(
        q="What will these two lines print?",
        code='gearshift = {\n    "name": "Gearshift",\n    "mana": 20,\n}\nprint(gearshift["name"])\nprint(gearshift["mana"])\n',
        choices=["name\nmana", "Gearshift\n20", "\"Gearshift\"\n20"],
        answer=1,
        explain=(
            "Python finds each key and prints its value. Text prints without its quotes, the same as always."
        ),
    ),
    starter=READ_STARTER,
    checkpoints=[
        dict(
            id="build-the-line",
            text="Change the last line so `Gearshift: 20 mana` is built from `gearshift`, with `+` and `str()`.",
            dictated=False,
            hints=[
                "Read two keys: `\"name\"` and `\"mana\"`. The mana is a number, so it needs `str()` before it is "
                "glued to text.",
                "`shell[\"name\"] + \" has \" + str(shell[\"ore\"])` glues text, text, and a number turned into text.",
                "Glue four pieces with `+`: `gearshift[\"name\"]`, `\": \"`, `str(gearshift[\"mana\"])` and "
                "`\" mana\"`. Or work in two steps, like the Example: `now = gearshift[\"mana\"]` first, then glue "
                "`str(now)`.",
                "Write `print(gearshift[\"name\"] + \": \" + str(gearshift[\"mana\"]) + \" mana\")` in place of "
                "`print(\"Gearshift: 20 mana\")`.",
            ],
            checks=[
                now_check(
                    "the keys are read, not printed",
                    ok="'Gearshift: 20 mana' in _ls or not any(_l.split(':')[0].strip() == 'name' "
                       "or _l.endswith('mana mana') for _l in _ls)",
                    fix="`\"name\"` on its own is only the text *name*. To read what the sheet holds, put the key "
                        "after the sheet: `gearshift[\"name\"]`.",
                    rules=[("any(_l.endswith('mana mana') for _l in _ls)",
                            "`\"mana\"` on its own is only the text *mana*. To read his mana, put the key after the "
                            "sheet: `gearshift[\"mana\"]`.")],
                ),
                out_line("the line reads Gearshift: 20 mana", "Gearshift: 20 mana",
                         "Print the line `Gearshift: 20 mana`: the name, a colon and a space, the mana, a space, then "
                         "`mana`.", comma_line="Gearshift : 20 mana"),
                follows(
                    "the line follows the sheet",
                    {"gearshift": OTHER_SHEET},
                    ev=OTHER_EV,
                    ok="'Pell: 7 mana' in _p",
                    fix="Build the line from `gearshift`, so it follows the sheet.",
                    said="'the line should show `Pell: 7 mana`'",
                    rules=[
                        ("'Pell: 31 mana' in _p",
                         "That reads `\"max_mana\"`. This line wants `\"mana\"`: what he has now."),
                        ("'Gearshift: 7 mana' in _p", "Read the name from the sheet too: `gearshift[\"name\"]`."),
                        ("'Pell: 20 mana' in _p", "Read the mana from the sheet too: `gearshift[\"mana\"]`."),
                    ],
                ),
            ],
            pass_line="Gearshift: Math checks out. Sheet reads true.",
        ),
    ],
    solution=_read(),
    assemble=dict(
        lines=[line for line in _read().splitlines() if line.strip()],
        distractors=['print("Gearshift: 20 mana")', 'print(gearshift["name"] + ": " + gearshift["mana"] + " mana")',
                     'print(gearshift.name + ": " + str(gearshift.mana) + " mana")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Sheet, then key",
            text=(
                "```text\ngearshift[\"mana\"]\n    |        |\n  sheet     key -> 20\n```\n"
                "First the sheet's name, then the key in square brackets."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `gearshift[\"name\"]` gives `\"Gearshift\"`.\n"
                "2. `+ \": \"` glues on a colon and a space.\n"
                "3. `str(gearshift[\"mana\"])` gives `\"20\"`.\n"
                "4. `+ \" mana\"` glues on the last word."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Reading a key is like finding *armor bonus* on a stat sheet and reading across. You look for the "
                "key, not the line number."
            ),
        ),
        dict(angle="shorter", text="The sheet's name, then the key in square brackets: `gearshift[\"name\"]`."),
    ],
    bonus=dict(
        by="gearshift",
        title="The full gauge",
        text=(
            "Gearshift wants the full gauge. On a new line, print `Gearshift: 20/20 mana`, built from `\"mana\"` and "
            "`\"max_mana\"`."
        ),
        hints=[
            "Two numbers, so two `str()` calls, with `\"/\"` glued between them.",
            "`str(have) + \"/\" + str(most)` glues two numbers with a `/` between them.",
            "Write `print(gearshift[\"name\"] + \": \" + str(gearshift[\"mana\"]) + \"/\" + "
            "str(gearshift[\"max_mana\"]) + \" mana\")`.",
        ],
        checks=[
            out_line("the gauge line reads Gearshift: 20/20 mana", "Gearshift: 20/20 mana",
                     "Print `Gearshift: 20/20 mana`: the mana, then `/`, then the max mana."),
            follows(
                "the gauge follows the sheet",
                {"gearshift": OTHER_SHEET},
                ev=OTHER_EV,
                ok="'Pell: 7/31 mana' in _p",
                fix="Build the gauge from the sheet's keys, so it follows the sheet.",
                said="'the gauge should show `Pell: 7/31 mana`'",
            ),
        ],
        solution=_read() + 'print(gearshift["name"] + ": " + str(gearshift["mana"]) + "/" + str(gearshift["max_mana"]) + " mana")\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='str(caster["mana"]) + "/" + str(caster["max_mana"])',
        why=(
            "The mana bar's last part read two keys and glued them with `str()`, the same as your line. `caster` "
            "was a sheet like `gearshift`."
        ),
    ),
    takeaway="Read a value with its key: `gearshift[\"mana\"]`. Glue a number to text with `str()`.",
    wrong_answers=[
        dict(why="starter unchanged: the line typed by hand (CMB)", code=READ_STARTER, fails_at=1,
             message_contains="Pell: 7 mana"),
        dict(why="commas between the pieces, as in Unit 3: print adds a space before the colon",
             code=_read('print(gearshift["name"], ":", gearshift["mana"], "mana")'), fails_at=1,
             message_contains="A comma inside"),
        dict(why="no str(): a number glued to text", code=_read('print(gearshift["name"] + ": " + gearshift["mana"] + " mana")'),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="the space after the colon left out (OUT first difference)",
             code=_read('print(gearshift["name"] + ":" + str(gearshift["mana"]) + " mana")'), fails_at=1,
             message_contains="A space is missing right after `Gearshift:`"),
        dict(why="the max mana read for the mana (same number now, not on another sheet)",
             code=_read('print(gearshift["name"] + ": " + str(gearshift["max_mana"]) + " mana")'), fails_at=1,
             message_contains="max_mana"),
        dict(why="half typed: the name typed by hand",
             code=_read('print("Gearshift: " + str(gearshift["mana"]) + " mana")'), fails_at=1,
             message_contains="name from the sheet"),
        dict(why="half typed: the mana typed by hand", code=_read('print(gearshift["name"] + ": 20 mana")'), fails_at=1,
             message_contains="mana from the sheet"),
        dict(why="dot access", code=_read('print(gearshift.name + ": " + str(gearshift.mana) + " mana")'), fails_at=0,
             message_contains="has no attribute 'name'"),
        dict(why="round brackets", code=_read('print(gearshift("name") + ": " + str(gearshift("mana")) + " mana")'),
             fails_at=0, message_contains="'dict' object is not callable"),
        dict(why="a position, as in a list", code=_read('print(gearshift[0] + ": " + str(gearshift[1]) + " mana")'),
             fails_at=0, message_contains="KeyError: 0"),
        dict(why="the key with no quotes (a box name)", code=_read('print(gearshift[name] + ": " + str(gearshift[mana]) + " mana")'),
             fails_at=0, message_contains="name 'name' is not defined"),
        dict(why="the key's text printed, not read: \"name\" for gearshift[\"name\"] (a variable is just its value)",
             code=_read('print("name" + ": " + str(gearshift["mana"]) + " mana")'), fails_at=1,
             message_contains="only the text *name*"),
        dict(why="the key's text printed, not read: \"mana\" for gearshift[\"mana\"]",
             code=_read('print(gearshift["name"] + ": " + "mana" + " mana")'), fails_at=1,
             message_contains="only the text *mana*"),
        dict(why="a key added to fit a typed read (the sheet's own key is kept): the rerun has no such key",
             code=READ_HEAD.replace('"mana": 20,\n', '"mana": 20,\n    "Mana": 20,\n')
             + 'print(gearshift["name"] + ": " + str(gearshift["Mana"]) + " mana")\n', fails_at=1,
             message_contains="Use keys the sheet really has"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-read,concat-str", solo="false", dictates="",
             foreign_names="bomb_shell,mana_now,shell,ore,now") + "\n"
        "P->R->M. The predict reads two keys (the right answer written second); the starter runs one read and "
        "carries the hand-typed line as its placeholder (S4). Hint ladder: Where to look, Teach (other names: "
        "`shell[\"name\"] + \" has \" + str(shell[\"ore\"])`), a middle rung that lists the four pieces (or the "
        "Example's two steps, `now = gearshift[\"mana\"]`), then Show me how. CP1 [ND]: OUT, led by Unit 3's 'A "
        "comma inside `print(...)` adds a space' when the print has commas between its pieces (or shows "
        "`Gearshift : 20 mana`), else the first difference; then CMB with another sheet (name \"Pell\", "
        "mana 7, max mana 31): the typed line, half-typed lines and the max mana read for the mana each get their "
        "own message (spaced practice of `+ str()`, 1C). WA (spec): the line typed -> CP1, CMB. Also proves dot "
        "access (AttributeError), round brackets (TypeError 'dict' object is not callable), a position "
        "(`KeyError: 0`) and an unquoted key (NameError), the class's dictionary slips. Site requests: explainer "
        "rows for `'dict' object is not callable` ('Read a dictionary with square brackets') and `KeyError: 0` "
        "('A dictionary has keys, not positions'). BQ (two reads + concat): the full gauge, with a Teach rung "
        "(`str(have) + \"/\" + str(most)`) between its two hints."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-04 key-errors (debug)
# ---------------------------------------------------------------------------------------------

KEYS_HEAD = (
    "gearshift = {\n"
    '    "name": "Gearshift",\n'
    '    "mana": 14,\n'
    '    "max_mana": 20,\n'
    "}\n"
)


def _keys(first='print(gearshift["max_mana"])', second='used = gearshift["max_mana"] - gearshift["mana"]',
          head=KEYS_HEAD):
    return head + first + "\n" + second + "\n" + 'print("Used: " + str(used))\n'


KEYS_STARTER = _keys('print(gearshift["Max_Mana"])', 'used = gearshift["max mana"] - gearshift["mana"]')
KEYS_OTHER = {"name": "Pell", "mana": 7, "max_mana": 31}
KEYS_EV = "another sheet, mana 7 and max mana 31"

KEYS_KEPT = (
    "_v = _g.get('gearshift')\n"
    "assert type(_v).__name__ == 'dict', _gone('gearshift')\n"
    "_odd = [_k for _k in _v if _k not in ('name', 'mana', 'max_mana')]\n"
    "assert 'max_mana' in _v and not _odd, ('Mend the lines that read the sheet, not the sheet. The sheet spells "
    "the key `\"max_mana\"`: keep it as it is.')\n"
    "assert _lit_key('gearshift', 'mana') == 14 and _lit_key('gearshift', 'max_mana') == 20, ('Keep the sheet as it "
    "is, with `\"mana\": 14` and `\"max_mana\": 20`. Mend only the lines that read it.')\n"
)

KEY_ERRORS = dict(
    id="key-errors",
    title="Key errors",
    martu=(
        "A [[KeyError]] means the sheet has no key spelled exactly like that. Capitals count. Spaces count. "
        "`\"Max_Mana\"` and `\"max_mana\"` are two different keys to Python.\n"
        "Read the last line of the message. It names the key Python could not find. Then look at how the sheet "
        "spells it. Python shows keys in `'` marks, like `KeyError: 'Max_Mana'`. Same text."
    ),
    names=["gearshift", "used"],
    pair_talk="Pair talk: tell your partner which key each message names, and how the sheet spells it.",
    starter=KEYS_STARTER,
    checkpoints=[
        dict(
            id="mend-max-mana",
            text="Mend line 6 so it prints Gearshift's max mana, read with the key the sheet really has.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which key does it name?",
                "Python says `KeyError: 'Max_Mana'`. Now look at the sheet: how does it spell that key?",
                "A key must match letter for letter. With `{\"dexterity\": 6}`, `[\"Dexterity\"]` is a KeyError and "
                "`[\"dexterity\"]` works.",
                "Write `print(gearshift[\"max_mana\"])` in place of `print(gearshift[\"Max_Mana\"])`.",
            ],
            checks=[
                ("the sheet keeps its keys", _PRE + KEYS_KEPT),
                now_check(
                    "the max mana shows",
                    ok="_ends_in(_ls, 20)",
                    fix="Keep line 6 printing the max mana, and mend only its key.",
                    rules=[("_ends_in(_ls, 14)",
                            "14 is his `\"mana\"`, what he has now. Line 6 wants his max mana.")],
                ),
                follows(
                    "the max mana follows the sheet",
                    {"gearshift": KEYS_OTHER},
                    ev=KEYS_EV,
                    ok="_ends_in(_p, 31)",
                    fix="Read the max mana from the sheet with its key, so line 6 follows the sheet.",
                    said="'no line showed its max mana, 31'",
                ),
            ],
        ),
        dict(
            id="mend-mana-used",
            text="Mend the next `KeyError`, on line 7.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which key does it name now?",
                "`'max mana'` has a space in it. What does the sheet's key have between the two words?",
                "In `{\"armor_bonus\": 3}`, the key has `_`, so `[\"armor bonus\"]` is a KeyError.",
                "Write `used = gearshift[\"max_mana\"] - gearshift[\"mana\"]` in place of "
                "`used = gearshift[\"max mana\"] - gearshift[\"mana\"]`.",
            ],
            checks=[
                now_check(
                    "the mana used shows",
                    ok="'Used: 6' in _ls",
                    fix="Keep the last two lines, and mend the key on line 7 so `used` is worked out from the sheet.",
                    rules=[
                        ("'Used: -6' in _ls", "That is the wrong way round: the max mana comes first, then `-`, then the mana."),
                        ("'Used: 0' in _ls", "That reads `\"mana\"` twice. The first key should be the max mana."),
                    ],
                ),
                follows(
                    "the mana used follows the sheet",
                    {"gearshift": KEYS_OTHER},
                    ev=KEYS_EV,
                    ok="'Used: 24' in _p",
                    fix="Work out `used` from the sheet's two keys, so it follows the sheet.",
                    said="'the line should show `Used: 24`'",
                    rules=[
                        ("'Used: 6' in _p and 'str(used)' not in _source.replace(' ', '')",
                         "Keep the last line as it was, `print(\"Used: \" + str(used))`, so it shows whatever `used` "
                         "holds. That line is typed by hand now."),
                        ("'Used: 6' in _p", "Work out `used` from the sheet's two keys, not a number you typed."),
                        ("'Used: 13' in _p", "Read the max mana from the sheet too, not a number you typed."),
                        # 31 - 14: the mana typed by hand.
                        ("'Used: 17' in _p", "Read the mana from the sheet too, not a number you typed."),
                    ],
                ),
            ],
            pass_line="Mar'tu: Two keys, spelled exactly. That is all a KeyError ever asks.",
        ),
    ],
    solution=_keys(),
    assemble=dict(
        lines=[line for line in _keys().splitlines() if line.strip()],
        distractors=['print(gearshift["Max_Mana"])', 'used = gearshift["max mana"] - gearshift["mana"]',
                     'print(20)'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="How Python finds a key",
            text=(
                "1. Python takes the key you wrote, letter by letter.\n"
                "2. It looks for a key in the sheet spelled exactly the same.\n"
                "3. None? It stops with `KeyError` and the key you wrote."
            ),
        ),
        dict(
            angle="picture",
            label="Two different keys",
            text=(
                "```text\nthe sheet has:   \"max_mana\"\nyou wrote:       \"Max_Mana\"\n"
                "                  ^   ^\n          two capitals differ\n```"
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "A locker tagged *Max_Mana* and a locker tagged *max_mana* are two lockers. Ask for the wrong "
                "one and nobody is home."
            ),
        ),
        dict(angle="shorter", text="KeyError: no key spelled exactly like that. Copy the key from the sheet."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='caster["max_mana"] - caster["mana"]',
        why=(
            "This line from the mana bars worked out the mana used. It spelled both keys exactly as the sheet did. "
            "One capital off, and it was a KeyError."
        ),
    ),
    takeaway="A KeyError means no key spelled exactly like that: copy the key from the sheet, capitals and `_` too.",
    wrong_answers=[
        dict(why="starter: capitals in the key", code=KEYS_STARTER, fails_at=0, message_contains="KeyError: 'Max_Mana'"),
        dict(why="line 6 mended, line 7 still has a space for _",
             code=_keys(second='used = gearshift["max mana"] - gearshift["mana"]'), fails_at=0,
             message_contains="KeyError: 'max mana'"),
        dict(why="half mended: one capital left", code=_keys(first='print(gearshift["max_Mana"])'), fails_at=0,
             message_contains="'max_Mana'"),
        dict(why="mended by typing the number (CMB)", code=_keys(first="print(20)"), fails_at=1,
             message_contains="31"),
        dict(why="the wrong key that exists (mana for max mana)", code=_keys(first='print(gearshift["mana"])'),
             fails_at=1, message_contains="what he has now"),
        dict(why="the sheet changed to fit the slips instead",
             code=_keys('print(gearshift["Max_Mana"])', 'used = gearshift["max mana"] - gearshift["mana"]',
                        head=KEYS_HEAD.replace('"max_mana": 20,', '"Max_Mana": 20,\n    "max mana": 20,')),
             fails_at=1, message_contains="not the sheet"),
        dict(why="line 6 deleted", code=KEYS_HEAD + 'used = gearshift["max_mana"] - gearshift["mana"]\n'
             'print("Used: " + str(used))\n', fails_at=1, message_contains="Keep line 6"),
        dict(why="the key with no quotes", code=_keys(second="used = gearshift[max_mana] - gearshift[\"mana\"]"),
             fails_at=0, message_contains="name 'max_mana' is not defined"),
        dict(why="the space just deleted (maxmana)", code=_keys(second='used = gearshift["maxmana"] - gearshift["mana"]'),
             fails_at=0, message_contains="'maxmana'"),
        dict(why="used typed by hand (CMB)", code=_keys(second="used = 6"), fails_at=2, message_contains="Used: 24"),
        dict(why="half typed: 20 - mana", code=_keys(second='used = 20 - gearshift["mana"]'), fails_at=2,
             message_contains="max mana from the sheet"),
        dict(why="half typed: max mana - 14 (the mana typed by hand)",
             code=_keys(second='used = gearshift["max_mana"] - 14'), fails_at=2, message_contains="mana from the sheet"),
        dict(why="the Used line typed by hand (used is worked out, but the print is not built from it)",
             code=_keys().replace('print("Used: " + str(used))', 'print("Used: 6")'), fails_at=2,
             message_contains="typed by hand"),
        dict(why="the sheet's mana changed to fit (mana 20), then the reads work but the answer is 0",
             code=_keys(head=KEYS_HEAD.replace('"mana": 14,', '"mana": 20,')), fails_at=1,
             message_contains="Keep the sheet as it is"),
        dict(why="the subtraction the wrong way round", code=_keys(second='used = gearshift["mana"] - gearshift["max_mana"]'),
             fails_at=2, message_contains="wrong way round"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-read,read-traceback", solo="false", dictates="",
             foreign_names="dexterity,armor_bonus") + "\n"
        "Debug (D), one checkpoint per KeyError, in the order Python reports them (the Learn pane notes that "
        "Python shows keys in `'` marks): `\"Max_Mana\"` (capitals), then "
        "`\"max mana\"` (a space for `_`). The KeyError row: 'The dictionary has no key spelled exactly ...' "
        "(site request: the spec's row, which also says 'or whether it lives one level deeper', for 4B). Each "
        "check is CMB with another sheet, so typing 20 or 6 fails, and a sheet changed to fit the slip fails "
        "('Mend the lines that read the sheet, not the sheet'; its values must stay 14 and 20 too). A typed "
        "`Used:` line and the mana typed into line 7 (31 - 14 = 17 in the rerun) get their own messages. Line 7 is "
        "the mana-bars subtraction (mana used). "
        "No partials: a crash fails every checkpoint on the site."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-05 write-by-key (point-at-it)
# ---------------------------------------------------------------------------------------------

WRITE_HEAD = (
    "gearshift = {\n"
    '    "name": "Gearshift",\n'
    '    "mana": 20,\n'
    '    "max_mana": 20,\n'
    "}\n"
    "fire_bolt_cost = 6\n"
)
WRITE_LINE = 'gearshift["mana"] = gearshift["mana"] - fire_bolt_cost'
FUEL_LINE = 'gearshift["fuel"] = "starlode"'


def _write(cast=WRITE_LINE, fuel=FUEL_LINE, head=WRITE_HEAD):
    return (head + "# 1. Gearshift casts Fire Bolt:\n" + (cast + "\n" if cast else "\n")
            + 'print(gearshift["mana"])\n' + '# 2. Add the key "fuel":\n' + (fuel + "\n" if fuel else "\n")
            + "print(gearshift)\n")


WRITE_STARTER = _write(cast="", fuel="")

_SPENT = r'''
_v = _g.get('gearshift')
assert type(_v).__name__ == 'dict', _gone('gearshift')
assert 'mana' in _v, ('`gearshift` has no key `"mana"` now. Keep the starter' + "'" + 's sheet, and change one key at '
                      'a time: `gearshift["mana"] = ...`.')
_start = _lit_key('gearshift', 'mana')
_cost = _g.get('fire_bolt_cost')
assert type(_start).__name__ == 'int', 'Keep the sheet' + "'" + 's `"mana": 20` line as a number.'
assert type(_cost).__name__ == 'int', 'Keep `fire_bolt_cost = 6` from the starter, as a number.'
_want = _start - _cost
_m = _v['mana']
_close = [_k for _k in _v if _k != 'mana' and _near(_k, 'mana')]
_bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
_boxes = [_t.id for _n in _tree.body if type(_n).__name__ == 'Assign' for _t in _n.targets
          if type(_t).__name__ == 'Name' and _t.id not in ('gearshift', 'fire_bolt_cost') and _g.get(_t.id) == _want]
_msg = ''
if _m == _start:
    if _close:
        _msg = ('`gearshift` has a new key `' + _show(_close[0]) + '`. The sheet' + "'" + 's key is `"mana"`: Python '
                'matches keys letter for letter.')
    elif _bare:
        _msg = ('Line ' + str(_bare[0]) + ' works out the new mana but keeps it nowhere. Put `gearshift["mana"] = ` '
                'in front of it.')
    elif _boxes:
        _msg = ('Your new variable `' + _boxes[0] + '` holds the new mana, but `gearshift["mana"]` still holds '
                + str(_start) + '. Put it in the sheet: `gearshift["mana"] = ...`.')
    else:
        _msg = ('`gearshift["mana"]` still holds ' + str(_start) + '. Under comment 1, spend the cost: '
                '`gearshift["mana"] = gearshift["mana"] - fire_bolt_cost`.')
elif _m == -_want:
    _msg = 'That takes the mana away from the cost. Start from the old mana: `gearshift["mana"] - fire_bolt_cost`.'
elif _m in (_cost, -_cost):
    _msg = ('`gearshift["mana"]` holds just the cost now. Start the right side from the old mana: '
            '`gearshift["mana"] - fire_bolt_cost`.')
elif _m == _start + _cost:
    _msg = 'That adds the cost. Casting spends mana: use `-`.'
elif _m != _want:
    _msg = ('`gearshift["mana"]` holds ' + str(_m) + '. After one Fire Bolt it should hold ' + str(_want)
            + ': the old mana minus `fire_bolt_cost`, once.')
assert not _msg, _msg
'''

_FUEL = r'''
_v = _g.get('gearshift')
assert type(_v).__name__ == 'dict', _gone('gearshift')
_close = [_k for _k in _v if _near(_k, 'fuel')]
_msg = ''
if 'fuel' not in _v:
    if _close:
        _msg = '`gearshift` has a key `' + _show(_close[0]) + '`. The task spells it `"fuel"`: Python matches keys letter for letter.'
    elif 'fuel' in _g:
        _msg = ('Your new variable `fuel` holds the fuel, but `gearshift` has no key `"fuel"`. Put it in the sheet: '
                '`gearshift["fuel"] = ...`.')
    else:
        _msg = ('Under comment 2, add the key `"fuel"` to `gearshift`: the key in square brackets on the left of '
                '`=`, its text on the right.')
elif type(_v['fuel']).__name__ != 'str' or not _v['fuel'].strip():
    _msg = '`gearshift["fuel"]` should hold text, in quotes: the name of his fuel.'
elif not all(_k in _v for _k in ('name', 'mana', 'max_mana')):
    _msg = ('Keep the rest of the sheet. One new line, `gearshift["fuel"] = ...`, adds a key and keeps every '
            'other key.')
assert not _msg, _msg
'''

WRITE_START = (
    "_start = _lit_key('gearshift', 'mana')\n"
    # Does the line that changes the mana read the cost, and the old mana? (a typed answer reads neither)
    "_rights = [_n.value for _n in _tree.body if type(_n).__name__ in ('Assign', 'AugAssign')\n"
    "           and any(type(_t).__name__ == 'Subscript' and getattr(_t.value, 'id', '') == 'gearshift'\n"
    "                   for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target]))]\n"
    "_names_used = [_x.id for _v in _rights for _x in _ast.walk(_v) if type(_x).__name__ == 'Name']\n"
    "_typed = bool(_rights) and not _names_used\n"
    "_sheets = [_n for _n in _tree.body if type(_n).__name__ == 'Assign' and getattr(_n.targets[0], 'id', '') == "
    "'gearshift']\n"
)

WRITE_BY_KEY = dict(
    id="write-by-key",
    title="Write by key",
    martu=(
        "A sheet can change. Put the key on the left of `=`, and that key gets a new value.\n"
        "`gearshift[\"mana\"] = gearshift[\"mana\"] - fire_bolt_cost`\n"
        "Python works out the right side first: it reads the old mana and takes the cost away. Then the key gets "
        "the answer.\n"
        "A key that is not there yet? The same kind of line adds it."
    ),
    example='shell = {"mana": 24}\nshell["mana"] = shell["mana"] - 5\nshell["ore"] = "Velocite"\nprint(shell)\n',
    example_output="{'mana': 19, 'ore': 'Velocite'}",
    names=["gearshift", "fire_bolt_cost"],
    pick="starlode",
    predict=dict(
        q="What will this print?",
        code='sheet = {"mana": 12}\nsheet["mana"] = sheet["mana"] - 5\nprint(sheet["mana"])\n',
        choices=["12", "-5", "5", "7"],
        answer="7",
        explain=(
            "Python works out the right side first: it reads the old mana, 12, and takes away 5. Then the key "
            "`\"mana\"` gets 7, in place of the 12."
        ),
    ),
    starter=WRITE_STARTER,
    checkpoints=[
        dict(
            id="cast-fire-bolt",
            text=(
                "Gearshift casts Fire Bolt. Under comment 1, write "
                "`gearshift[\"mana\"] = gearshift[\"mana\"] - fire_bolt_cost`."
            ),
            dictated=True,
            hints=[
                "The right side reads the old mana, then takes away the cost. Use the variable `fire_bolt_cost`, not "
                "a number.",
                "`shell[\"mana\"] = shell[\"mana\"] - 5` reads 24, takes 5 away, and puts 19 back under the key.",
                "Write `gearshift[\"mana\"] = gearshift[\"mana\"] - fire_bolt_cost` under `# 1.`",
            ],
            checks=[
                ("the mana is spent", _PRE + _SPENT),
                follows(
                    "the mana follows the cost",
                    {"fire_bolt_cost": 4},
                    ev="`fire_bolt_cost = 4`",
                    ok="_R('gearshift')['mana'] == _start - 4",
                    fix="Use the variable `fire_bolt_cost` on the right side, not a number, so the cost can change.",
                    said="'the mana should become ' + str(_start - 4)",
                    rules=[("len(_sheets) > 1",
                            "Keep one `gearshift = {...}`, the starter's. Change the mana with a "
                            "`gearshift[\"mana\"] = ...` line, not a new sheet."),
                           ("_typed", "Work the new mana out on the right side, from `gearshift[\"mana\"]` and "
                                      "`fire_bolt_cost`, not a number you typed.")],
                    pre=WRITE_START,
                    what="cost",
                ),
                follows(
                    "the mana follows the sheet",
                    # mana and max mana differ here, so reading "max_mana" for "mana" shows.
                    {"gearshift": {"name": "Pell", "mana": 31, "max_mana": 40}, "fire_bolt_cost": 4},
                    ev="another sheet with mana 31 and max mana 40, and `fire_bolt_cost = 4`",
                    ok="_R('gearshift')['mana'] == 27",
                    fix="Read the old mana from the sheet, `gearshift[\"mana\"]`, not a number you typed.",
                    said="'the mana should become 27'",
                    rules=[("_R('gearshift')['mana'] == 36",
                            "That reads `\"max_mana\"`. Spend from `\"mana\"`, what he has now: "
                            "`gearshift[\"mana\"] - fire_bolt_cost`.")],
                ),
            ],
            pass_line=(
                "Mar'tu: Which part reads the old mana? Point at it. Yes: the `gearshift[\"mana\"]` on the right "
                "side."
            ),
        ),
        dict(
            id="add-fuel",
            text="Under comment 2, give Gearshift a new key `\"fuel\"` that holds `\"starlode\"`.",
            dictated=False,
            hints=[
                "A new key is made the same way a value is changed: the key on the left of `=`. Text goes in quotes.",
                "`shell[\"ore\"] = \"Velocite\"` adds the key `\"ore\"` to `shell`.",
                "Write `gearshift[\"fuel\"] = \"starlode\"` under `# 2.`",
            ],
            checks=[("gearshift has a fuel key", _PRE + _FUEL)],
            pass_line="Gearshift: Starlode logged. Tank's full.",
        ),
    ],
    solution=_write(),
    partials=[_write(fuel="")],
    assemble=dict(
        lines=[line for line in _write().splitlines() if line.strip() and not line.startswith("#")],
        distractors=['gearshift["mana"] = gearshift["mana"] - 6', 'gearshift["mana"] = 14', 'gearshift.fuel = "starlode"'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "1. Python reads `gearshift[\"mana\"]` on the right: 20.\n"
                "2. It takes away `fire_bolt_cost`: 20 - 6 is 14.\n"
                "3. The key `\"mana\"` on the left gets 14."
            ),
        ),
        dict(
            angle="picture",
            label="Before and after",
            text=(
                "```text\nbefore:  \"mana\": 20\nafter:   \"mana\": 14\n"
                "         \"fuel\": \"starlode\"\n```\nThe same key, a new value. Then a new key."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Like a scoreboard: read the old score, work out the new one, and write it over the old one. The "
                "key stays; the number changes."
            ),
        ),
        dict(
            angle="from Unit 1",
            text="In Unit 1 you wrote `mana = mana - 3`. This is the same move, with a key in place of the box.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Show me the bar",
        text=(
            "What's in it for me? A picture. At the bottom, print Gearshift's mana bar: a `\"█\"` for each point of "
            "mana he has, then a `\"░\"` for each point he used."
        ),
        hints=[
            "The points used are `gearshift[\"max_mana\"] - gearshift[\"mana\"]`. Put that in brackets after "
            "`\"░\" * `.",
            "`\"█\" * 3 + \"░\" * (5 - 3)` makes 3 full blocks and 2 light ones. The brackets are worked out first.",
            "Write `print(\"█\" * gearshift[\"mana\"] + \"░\" * (gearshift[\"max_mana\"] - gearshift[\"mana\"]))`.",
        ],
        checks=[
            now_check(
                "the bar shows",
                ok="'█' * gearshift['mana'] + '░' * (gearshift['max_mana'] - gearshift['mana']) in _ls",
                fix="Print the bar: `\"█\"` times the mana, then `\"░\"` times the max mana minus the mana.",
            ),
            follows(
                "the bar follows the sheet",
                {"gearshift": {"name": "Pell", "mana": 9, "max_mana": 12}, "fire_bolt_cost": 4},
                ev="another sheet, mana 9 of 12, and `fire_bolt_cost = 4`",
                ok="'█' * 5 + '░' * 7 in _p",
                fix="Build the bar from the sheet's keys, so it follows the sheet.",
                said="'the bar should be 5 full blocks and 7 light ones'",
            ),
        ],
        solution=_write() + 'print("█" * gearshift["mana"] + "░" * (gearshift["max_mana"] - gearshift["mana"]))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "This line paid for holding the barrier. The right side read the caster's old mana and took the "
            "spell's cost away. Same shape as your line."
        ),
    ),
    takeaway="Change a value by its key: `gearshift[\"mana\"] = gearshift[\"mana\"] - cost`. A new key is added the same way.",
    wrong_answers=[
        dict(why="starter unchanged", code=WRITE_STARTER, fails_at=1, message_contains="still holds 20"),
        dict(why="subtracting a typed 6 (CMB, spec)", code=_write(cast='gearshift["mana"] = gearshift["mana"] - 6'),
             fails_at=1, message_contains="fire_bolt_cost = 4"),
        dict(why="the new mana typed by hand: hero[\"mana\"] = 7 style (CMB)", code=_write(cast='gearshift["mana"] = 14'),
             fails_at=1, message_contains="not a number you typed"),
        dict(why="the old mana typed by hand: 20 - cost (CMB on the sheet)",
             code=_write(cast='gearshift["mana"] = 20 - fire_bolt_cost'), fails_at=1, message_contains="mana 31"),
        dict(why="the max mana read for the mana (both are 20 in the starter, so only another sheet shows it)",
             code=_write(cast='gearshift["mana"] = gearshift["max_mana"] - fire_bolt_cost'), fails_at=1,
             message_contains='That reads `"max_mana"`'),
        dict(why="a new sheet typed with the new mana, instead of writing by key",
             code=_write(fuel='gearshift = {"name": "Gearshift", "mana": 14, "max_mana": 20, "fuel": "starlode"}'),
             fails_at=1, message_contains="Keep one `gearshift = {...}`"),
        dict(why="worked out, kept nowhere (BARE)", code=_write(cast='gearshift["mana"] - fire_bolt_cost'), fails_at=1,
             message_contains="keeps it nowhere"),
        dict(why="a new variable instead of the key (NEWBOX)", code=_write(cast='mana = gearshift["mana"] - fire_bolt_cost'),
             fails_at=1, message_contains="new variable"),
        dict(why="a near-miss key on the left: a new key Mana (KEY)",
             code=_write(cast='gearshift["Mana"] = gearshift["mana"] - fire_bolt_cost'), fails_at=1,
             message_contains='"Mana"'),
        dict(why="the subtraction the wrong way round", code=_write(cast='gearshift["mana"] = fire_bolt_cost - gearshift["mana"]'),
             fails_at=1, message_contains="away from the cost"),
        dict(why="the cost added", code=_write(cast='gearshift["mana"] = gearshift["mana"] + fire_bolt_cost'), fails_at=1,
             message_contains="adds the cost"),
        dict(why="only the cost stored", code=_write(cast='gearshift["mana"] = fire_bolt_cost'), fails_at=1,
             message_contains="just the cost"),
        dict(why="dot access on the right", code=_write(cast='gearshift["mana"] = gearshift.mana - fire_bolt_cost'),
             fails_at=0, message_contains="has no attribute 'mana'"),
        dict(why="round brackets", code=_write(cast='gearshift["mana"] = gearshift("mana") - fire_bolt_cost'),
             fails_at=0, message_contains="not callable"),
        dict(why="the fuel key with a dot", code=_write(fuel='gearshift.fuel = "starlode"'), fails_at=0,
             message_contains="has no attribute 'fuel'"),
        dict(why="the fuel key with no quotes", code=_write(fuel='gearshift[fuel] = "starlode"'), fails_at=0,
             message_contains="name 'fuel' is not defined"),
        dict(why="the fuel with no quotes", code=_write(fuel='gearshift["fuel"] = starlode'), fails_at=0,
             message_contains="name 'starlode' is not defined"),
        dict(why="the key kept, the sheet left off: \"fuel\" = \"starlode\"", code=_write(fuel='"fuel" = "starlode"'),
             fails_at=0, message_contains="cannot assign to literal"),
        dict(why="the mana key kept, the sheet left off on the left",
             code=_write(cast='"mana" = gearshift["mana"] - fire_bolt_cost'), fails_at=0,
             message_contains="cannot assign to literal"),
        dict(why="the cost read from the sheet: gearshift[\"fire_bolt_cost\"] (KeyError)",
             code=_write(cast='gearshift["mana"] = gearshift["mana"] - gearshift["fire_bolt_cost"]'), fails_at=0,
             message_contains="KeyError: 'fire_bolt_cost'"),
        dict(why="round brackets on both sides of the store",
             code=_write(cast='gearshift("mana") = gearshift("mana") - fire_bolt_cost'), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="== for = (reads a key that is not there yet)", code=_write(fuel='gearshift["fuel"] == "starlode"'),
             fails_at=0, message_contains="KeyError: 'fuel'"),
        dict(why="a new variable instead of a key (NEWBOX)", code=_write(fuel='fuel = "starlode"'), fails_at=2,
             message_contains="new variable `fuel`"),
        dict(why="a near-miss key (KEY)", code=_write(fuel='gearshift["Fuel"] = "starlode"'), fails_at=2,
             message_contains='"Fuel"'),
        dict(why="the whole sheet replaced by the fuel", code=_write(fuel='gearshift = {"fuel": "starlode"}'),
             fails_at=1, message_contains="no key `\"mana\"` now"),
        dict(why="no fuel line", code=_write(fuel=""), fails_at=2, message_contains="add the key"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-write", solo="false", dictates="1",
             foreign_names="shell,sheet,ore") + "\n"
        "P->R->M. The predict's right answer is written last of four. CP1 [D] (spec; the unit's first write, so "
        "it stays dictated and carries the Point-at-it pass line): the mana check reads the start mana and the "
        "cost from the student's own code, "
        "then CMB with `fire_bolt_cost = 4` (spec) and with another sheet (mana 31, max mana 40, so "
        "`20 - fire_bolt_cost` and a `\"max_mana\"` read for the mana both fail; in the starter both are 20). "
        "A second typed `gearshift = {...}` is named. Catches (spec): subtracting a typed 6 -> CMB; the class's 'literal number instead of reading by "
        "key' (`gearshift[\"mana\"] = 14`) -> CMB; BARE, NEWBOX, a near-miss key, the sign reversed. CP2 [ND] "
        "(teacher ruling: goal-only, the spec's [D] relaxed; the text names the key and the value, not the line): "
        "KEY `\"fuel\"`, any text (pick: starlode), with NEWBOX, a near-miss key and the whole sheet replaced. "
        "Point-at-it (G2 R9) is CP1's pass line. TR from the campaign is the campaign_link (hold-the-barrier's mana "
        "line). BQ (write + bar, 1C stamps): the mana bar, blocks given in the text and the symbol tray; a Teach "
        "rung (`\"█\" * 3 + \"░\" * (5 - 3)`) sits between its two hints."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-06 is-it-in (intro op:In, op:NotIn)
# ---------------------------------------------------------------------------------------------

BOOK_HEAD = 'spell_book = {\n    "Glow": 2,\n    "Warm Hands": 3,\n}\n'
IN_TOP = (
    BOOK_HEAD
    + 'print("Glow" in spell_book)\n'
    + "print(2 in spell_book)\n"
    + '# If "Fire Bolt" is not in the\n# book, print a message.\n'
)
# can-they-cast's scaffold (4B-05): an `if` that never fires, its message already under it. The fade runs: replace
# `False` here -> replace `False` with nested reads (4B-05) -> write the whole `if` (Quick Check).
IN_SCAFFOLD = 'if False:\n    print("Learn Fire Bolt first.")\n'
IN_STARTER = IN_TOP + IN_SCAFFOLD
IN_IF = 'if "Fire Bolt" not in spell_book:\n    print("Learn Fire Bolt first.")\n'


def _in(block=IN_IF):
    return IN_TOP + block


_IN_CHECK = r'''
_A = {'Glow': 2, 'Warm Hands': 3}
_B = {'Glow': 2, 'Warm Hands': 3, 'Fire Bolt': 6}
_ev = "(Mar'tu's check ran your code with and without \"Fire Bolt\" in the book, only inside the check"
_ra, _pa, _fa, _ea = _rerun({'spell_book': _A})
_rb, _pb, _fb, _eb = _rerun({'spell_book': _B})
assert _fa, _gone('spell_book')
assert not _ea, _crash(_ea, _ev, 'book')
assert not _eb, _crash(_eb, _ev, 'book')


def _minus(_x, _y):
    _y = list(_y)
    _out = []
    for _l in _x:
        if _l in _y:
            _y.remove(_l)
        elif _l not in ('True', 'False'):
            _out.append(_l)
    return _out


_only_a = _minus(_pa, _pb)
_only_b = _minus(_pb, _pa)
_ifs = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'If']
_asks = [_c for _n in _ifs for _c in _ast.walk(_n.test) if type(_c).__name__ == 'Compare'
         and any(type(_o).__name__ in ('In', 'NotIn') for _o in _c.ops)]
_words = [_c.left.value for _c in _asks if type(_c.left).__name__ == 'Constant']
_odd = [_x for _x in _words if type(_x).__name__ == 'str' and _x != 'Fire Bolt' and _squash(_x) == _squash('Fire Bolt')]
_numbers = [_x for _x in _words if type(_x).__name__ in ('int', 'float')]
_others = [_x for _x in _words if type(_x).__name__ == 'str' and _x != 'Fire Bolt']
# A variable's name asked about in quotes (`"spell"` for the variable `spell`): these exact letters, not the box.
_quoted = [_x for _x in _others if _x in _made()]
_both = [_l for _l in _pb if _l not in ('True', 'False')]
# The starter's scaffold left as it is: an `if` whose test is a plain `False` (it never fires), or `True`.
_stuck = [_n for _n in _ifs if type(_n.test).__name__ == 'Constant']
_msg = ''
if _odd:
    _msg = '`"' + _odd[0] + '"` and `"Fire Bolt"` are different text to Python: every letter, space and capital counts.'
elif not _only_a:
    if _numbers:
        _msg = ('`in` checks keys, never values. A cost is a value. Ask about the spell' + "'" + 's name, '
                '`"Fire Bolt"`, which would be a key.')
    elif _quoted and not any(_x == 'Fire Bolt' for _x in _words):
        _msg = ('`"' + _quoted[0] + '"` has quotes, so Python asks about those exact letters, not what the variable `'
                + _quoted[0] + '` holds. Take the quotes off.')
    elif _others and not any(_x == 'Fire Bolt' for _x in _words):
        _msg = 'Your `if` asks about another key. This step asks about `"Fire Bolt"`, letter for letter.'
    elif _stuck and not _asks:
        _msg = ('Replace `' + str(_stuck[0].test.value) + '` with a question: `not in` asks whether a key is '
                'missing.')
    elif _only_b:
        _msg = ('Your message shows only when "Fire Bolt" IS in the book. Ask the other question, with `not in`. '
                + _ev + '.)')
    elif _both:
        _msg = ('Your message also shows when "Fire Bolt" is in the book. Put the `print` under an `if` that asks '
                '`not in`, indented. ' + _ev + '.)')
    elif _ifs and len(_pa) > len(_pb):
        _msg = ('Your `if` prints `True` or `False`, the answer to the question. Print a message of your own '
                'instead, in quotes, like `print("Learn Fire Bolt first.")`.')
    elif _ifs:
        _msg = ('Nothing new printed when "Fire Bolt" was missing. Ask `"Fire Bolt" not in spell_book`, and indent '
                'a `print` under the `if`. ' + _ev + '.)')
    else:
        _msg = 'Add an `if` that asks whether "Fire Bolt" is not in `spell_book`, and print a message under it.'
assert not _msg, _msg
'''

_GLOW_CHECK = r'''
_ev = "(Mar'tu's check tried a book where Glow costs 5, and a book with no Glow, only inside the check"
_ra, _pa, _fa, _ea = _rerun({'spell_book': {'Glow': 5, 'Warm Hands': 3}})
_rb, _pb, _fb, _eb = _rerun({'spell_book': {'Warm Hands': 3}})
assert 'Glow costs 2' in _lines(), 'Print `Glow costs 2`, built from the book: `str(spell_book["Glow"])`.'
assert not _ea, _crash(_ea, _ev, 'book')
assert not _eb, ('Put the read under an `if` that asks `"Glow" in spell_book`, so a book with no Glow does not stop. '
                 + _ev + '.)')
assert 'Glow costs 5' in _pa, 'Read the cost from the book, so it follows the book. ' + _ev + '.)'
assert not any(_l.startswith('Glow costs') for _l in _pb), ('Print the cost only when `"Glow" in spell_book`. '
                                                             + _ev + ': the line still showed.)')
'''

IS_IT_IN = dict(
    id="is-it-in",
    title="Is it in the book?",
    martu=(
        "`in` asks a yes/no question: is this key in the dictionary? `\"Glow\" in spell_book` gives `True` or "
        "`False`.\n"
        "`in` looks at the keys only, never the values.\n"
        "[[not in|`not in`]] asks the opposite: is it missing? Put it in an `if`, and Python acts only when the key is "
        "missing.\n"
        "After you run, try it: change the `2` to `3`. Still `False`, yes? 3 is a value too."
    ),
    introduces=["op:In", "op:NotIn"],
    example='pack = {"rope": 1, "lamp": 2}\nprint("rope" in pack)\nif "map" not in pack:\n    print("No map.")\n',
    example_output="True\nNo map.",
    names=["spell_book"],
    predict=dict(
        q="Before you press Run: what will the two `print` lines show?",
        choices=["True\nTrue", "False\nFalse", "False\nTrue", "True\nFalse"],
        answer=3,
        explain=(
            "`in` looks at keys only. `\"Glow\"` is a key: `True`. 2 is a value, Glow's cost, not a key: `False`."
        ),
    ),
    starter=IN_STARTER,
    checkpoints=[
        dict(
            id="if-not-in",
            text=(
                "Replace `False` with a `not in` test, so the message shows only when `\"Fire Bolt\"` is missing. "
                "Change the message to your own if you like."
            ),
            dictated=False,
            hints=[
                "Look at `if False:`. Its test should ask whether `\"Fire Bolt\"` is missing from `spell_book`.",
                "`if \"map\" not in pack:` with `print(\"No map.\")` indented under it prints only when the key is "
                "missing.",
                "Replace `False` with `\"Fire Bolt\" not in spell_book`.",
            ],
            checks=[("the message shows only when Fire Bolt is missing", _PRE + _IN_CHECK)],
            pass_line="Bomb Shell: Not in the book. Noted.",
        ),
    ],
    solution=_in(),
    assemble=dict(
        lines=[line for line in _in().splitlines() if line.strip() and not line.startswith("#")],
        distractors=['if "Fire Bolt" in spell_book:', "if 6 not in spell_book:", 'print("Fire Bolt" not in spell_book)'],
    ),
    another_way=[
        dict(
            angle="why",
            label="Why does this work? `in` checks keys",
            text=(
                "A dictionary is built to find keys fast. The values are what you get *after* you find a key. So "
                "`in` asks about keys and never looks at values: `2 in spell_book` is `False` even though 2 is "
                "Glow's cost."
            ),
        ),
        dict(
            angle="picture",
            label="Keys on the left",
            text=(
                "`in` only reads the left side:\n"
                "```text\n  key            value\n\"Glow\"       ->  2\n\"Warm Hands\" ->  3\n"
                "  ^ in looks here\n```"
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Is *Fire Bolt* in the book's contents page? You read the titles, not the page numbers. Titles are "
                "the keys."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `\"Fire Bolt\" not in spell_book` asks: is it missing?\n"
                "2. It is missing, so the answer is `True`.\n"
                "3. `if True:` runs the indented `print`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Only if I know it",
        text=(
            "What's in it for me? Under your `if`, add a second `if`: when `\"Glow\"` is in `spell_book`, print "
            "`Glow costs 2`, built from the book."
        ),
        hints=[
            "A second `if`, asking with `in`. The cost is a number, so wrap it in `str()`.",
            "Write `if \"Glow\" in spell_book:`, then indent `print(\"Glow costs \" + str(spell_book[\"Glow\"]))` "
            "under it.",
        ],
        checks=[("Glow's cost shows only when Glow is known", _PRE + _GLOW_CHECK)],
        solution=_in() + 'if "Glow" in spell_book:\n    print("Glow costs " + str(spell_book["Glow"]))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='if spell_name not in caster["spell_book"]:',
        why=(
            "The barrier spell started with this line. It asked: is this spell's name a key in the caster's spell "
            "book? If not, the caster didn't know it. Now you can read it."
        ),
    ),
    takeaway="`in` and `not in` ask about keys, never values: `if \"Fire Bolt\" not in spell_book:`.",
    wrong_answers=[
        dict(why="starter unchanged: the scaffold's `if False:` never fires", code=IN_STARTER, fails_at=1,
             message_contains="Replace `False` with a question"),
        dict(why="the scaffold kept, only its message changed", code=_in('if False:\n    print("No Fire Bolt.")\n'),
             fails_at=1, message_contains="Replace `False` with a question"),
        dict(why="False replaced with True: the message always shows",
             code=_in('if True:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="Replace `True` with a question"),
        dict(why="the scaffold deleted, nothing in its place (no if)", code=IN_TOP, fails_at=1,
             message_contains="Add an `if`"),
        dict(why="in for not in: the message shows only when Fire Bolt is known",
             code=_in('if "Fire Bolt" in spell_book:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="IS in the book"),
        dict(why="no if: the message always shows", code=_in('print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="also shows"),
        dict(why="`in` used on a value (a cost): `in` checks keys, not values",
             code=_in('if 6 not in spell_book:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="checks keys, never values"),
        dict(why="`in` used on a value that IS in the book (Glow's cost, 2): still never a key (spec: 2 in book)",
             code=_in('if 2 not in spell_book:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="checks keys, never values"),
        dict(why="a variable's name in quotes: \"spell\" for the variable spell (quoting a variable key)",
             code=_in('spell = "Fire Bolt"\nif "spell" not in spell_book:\n    print("Learn it.")\n'), fails_at=1,
             message_contains='`"spell"` has quotes'),
        dict(why="the answer True printed under the if, not a message",
             code=_in('if "Fire Bolt" not in spell_book:\n    print("Fire Bolt" not in spell_book)\n'), fails_at=1,
             message_contains="prints `True` or `False`"),
        dict(why="capitals in the spell name (STREXACT)",
             code=_in('if "Fire bolt" not in spell_book:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="every letter, space and capital counts"),
        dict(why="the answer printed, not a message", code=_in('print("Fire Bolt" not in spell_book)\n'), fails_at=1,
             message_contains="Add an `if`"),
        dict(why="!= used to ask (always True)",
             code=_in('if "Fire Bolt" != spell_book:\n    print("Learn Fire Bolt first.")\n'), fails_at=1,
             message_contains="also shows"),
        dict(why="reading the missing key to test it", code=_in('if spell_book["Fire Bolt"]:\n    print("Learn it.")\n'),
             fails_at=0, message_contains="KeyError: 'Fire Bolt'"),
        dict(why="the print not indented", code=_in('if "Fire Bolt" not in spell_book:\nprint("Learn it.")\n'),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the colon left off", code=_in('if "Fire Bolt" not in spell_book\n    print("Learn it.")\n'),
             fails_at=0, message_contains="expected ':'"),
        dict(why="another spell asked about", code=_in('if "Glow" not in spell_book:\n    print("Learn it.")\n'),
             fails_at=1, message_contains="another key"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-in,if-else", solo="false", dictates="",
             foreign_names="pack,map,rope,lamp") + "\n"
        "P->I->M. The predict is the spec's (`\"Glow\" in spell_book` True, `2 in spell_book` False; the right "
        "answer written last of four; the scaffold's `if False:` prints nothing, so the starter still shows only "
        "True and False); the Investigate prompt (change 2 to 3) is the Learn pane's last line. The starter carries "
        "can-they-cast's scaffold (teacher ruling): `if False:` with the message under it, so the fade runs "
        "replace `False` (here) -> replace `False` with nested reads (4B-05) -> write the whole `if` (Quick Check). "
        "CP1 [ND]: CMB, the program runs with and without Fire Bolt in the book, and a new line must show only when "
        "it is missing (an else branch is fine; a printed True/False never counts as the message). The scaffold "
        "left as it is gets 'Replace `False` with a question'. WT ('`in` checks keys') is the 'why' angle. The "
        "class's slip 'in checks values' is proven by `if 6 not in spell_book:` and `if 2 not in spell_book:`. Any "
        "message passes (the starter's message is kept or changed; no pick needed). About 0.5 minutes saved for "
        "students who would stall on a blank `if`. BQ (in + read + str): Glow's cost, only when Glow is known."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-07 key-from-a-box
# ---------------------------------------------------------------------------------------------

NAME_HEAD = BOOK_HEAD + 'spell_name = "Warm Hands"\n'
NAME_STARTER = NAME_HEAD + "# Print the cost of the spell\n# that spell_name names.\n"


def _named(line="print(spell_book[spell_name])"):
    return NAME_HEAD + line + "\n"


KEY_FROM_A_BOX = dict(
    id="key-from-a-box",
    title="A key from a box",
    martu=(
        "A key can come from a variable. `spell_book[spell_name]` has no quotes, so Python opens the box "
        "`spell_name` first. It finds `\"Warm Hands\"`, then reads that key.\n"
        "`spell_book[\"spell_name\"]` has quotes, so Python looks for a key spelled s-p-e-l-l-_-n-a-m-e. There is "
        "none: a KeyError.\n" + QUOTES_RULE
    ),
    example='pack = {"rope": 1, "lamp": 2}\nitem = "lamp"\nprint(pack[item])\n',
    example_output="2",
    names=["spell_book", "spell_name"],
    predict=dict(
        q="`print(spell_book[spell_name])` shows 3. What does `print(spell_book[\"spell_name\"])` show?",
        code=NAME_HEAD + 'print(spell_book["spell_name"])\n',
        choices=["3", "Warm Hands", "ERROR: KeyError: 'spell_name'"],
        answer=2,
        explain=(
            "With quotes, Python looks for a key spelled exactly `spell_name`. The book has no such key, so it "
            "stops with a KeyError. With no quotes, it opens the box first and finds `\"Warm Hands\"`."
        ),
    ),
    pair_talk=(
        "Pair talk: sort the six cards in *Another way* together. For each one, say *these exact letters* or *look "
        "inside the box*, and why. Then each of you does the step on your own."
    ),
    starter=NAME_STARTER,
    checkpoints=[
        dict(
            id="cost-of-the-named-spell",
            text="Print the cost of whichever spell `spell_name` names, read from `spell_book`.",
            dictated=False,
            hints=[
                "Which goes in the square brackets: the box `spell_name`, or the letters `\"spell_name\"`? Only one "
                "finds the cost.",
                "`pack[item]` opens the box `item`, finds `\"lamp\"`, then reads the key `\"lamp\"`: 2.",
                "Write `print(spell_book[spell_name])`.",
            ],
            checks=[
                now_check(
                    "the cost shows",
                    ok="_ends_in(_ls, 3)",
                    fix="Print the spell's cost: read `spell_book` with the variable `spell_name` as the key.",
                    rules=[
                        ("spell_name != 'Warm Hands'",
                         "Keep `spell_name = \"Warm Hands\"` from the starter. Mar'tu's check changes it for you, to "
                         "see your line follow."),
                        ("'Warm Hands' in _ls",
                         "That prints the spell's name. Put `spell_name` inside `spell_book[...]` to read its cost."),
                        ("_ends_in(_ls, 2)", "2 is Glow's cost. Read the spell that `spell_name` names."),
                    ],
                ),
                follows(
                    "the cost follows spell_name",
                    {"spell_name": "Glow"},
                    ev='`spell_name = "Glow"`',
                    ok="_ends_in(_p, 2)",
                    fix="Use the variable `spell_name` as the key, so the line follows it.",
                    said="'the line should end in 2, the cost of Glow'",
                    what="spell name",
                ),
            ],
            pass_line="Mar'tu: No quotes, so Python looked inside the box first. Good.",
        ),
    ],
    solution=_named(),
    assemble=dict(
        lines=[line for line in _named().splitlines() if line.strip()],
        distractors=['print(spell_book["spell_name"])', "print(spell_name)", 'print(spell_book["Warm Hands"])'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="What Python looks up",
            text=(
                "`spell_book[spell_name]`:\n"
                "1. No quotes: open the box `spell_name`. It holds `\"Warm Hands\"`.\n"
                "2. Read the key `\"Warm Hands\"`: 3.\n"
                "`spell_book[\"spell_name\"]`:\n"
                "1. Quotes: look for the key spelled `spell_name`.\n"
                "2. There is none: KeyError."
            ),
        ),
        dict(
            angle="picture",
            label="The quotes sort",
            text=(
                "Sort the six cards: does `mana` mean *these exact letters*, or *look inside the box*? One click "
                "for each card, with your partner, then press *Check my sort*."
            ),
            # The one-click card sort (the teacher's Unit 5 site request): its answers show only after the check.
            sort=dict(
                groups=["these exact letters", "look inside the box"],
                cards=[("mana = 26", 1), ('{"mana": 26}', 0), ('hero["mana"]', 0), ("hero[mana]", 1),
                       ('print("mana")', 0), ("print(mana)", 1)],
                explain=(
                    "Cards 2, 3 and 5 have quotes, so they mean these exact letters. Cards 1, 4 and 6 have none, so "
                    "`mana` is a box (card 1 makes it)."
                ),
            ),
        ),
        dict(angle="shorter", text=QUOTES_RULE),
        dict(
            angle="everyday",
            text=(
                "A note says *look in the drawer marked TODAY*. You open TODAY and find *Warm Hands*. Then you look "
                "that up. The note's word was a box, not the answer."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "The barrier spell read `caster[\"spell_book\"][spell_name]`: no quotes on `spell_name`, so the key "
                "came from the variable. Any spell name worked."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Say it properly",
        text=(
            "What's in it for me? A proper line. On a new line, print `Warm Hands costs 3`, built from `spell_name` "
            "and the book."
        ),
        hints=[
            "The cost is a number: wrap `spell_book[spell_name]` in `str()`.",
            "Write `print(spell_name + \" costs \" + str(spell_book[spell_name]))`.",
        ],
        checks=[
            out_line("the line reads Warm Hands costs 3", "Warm Hands costs 3",
                     "Print `Warm Hands costs 3`: the spell's name, ` costs `, then its cost."),
            follows(
                "the line follows spell_name",
                {"spell_name": "Glow"},
                ev='`spell_name = "Glow"`',
                ok="'Glow costs 2' in _p",
                fix="Build the line from `spell_name` and the book, so it follows `spell_name`.",
                said="'the line should show `Glow costs 2`'",
                what="spell name",
            ),
        ],
        solution=_named() + 'print(spell_name + " costs " + str(spell_book[spell_name]))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='spell = caster["spell_book"][spell_name]',
        why=(
            "The barrier spell read the spell with `[spell_name]`, no quotes: the key came from the variable. Next "
            "lesson you read those two brackets one at a time."
        ),
    ),
    takeaway="`book[spell_name]` opens the variable first; `book[\"spell_name\"]` looks for those exact letters.",
    wrong_answers=[
        dict(why="starter unchanged (nothing printed)", code=NAME_STARTER, fails_at=1, message_contains="Print the spell's cost"),
        dict(why="the variable's name in quotes (spec)", code=_named('print(spell_book["spell_name"])'), fails_at=0,
             message_contains="KeyError: 'spell_name'"),
        dict(why="the spell's name printed, not its cost", code=_named("print(spell_name)"), fails_at=1,
             message_contains="spell's name"),
        dict(why="the spell typed in as text (CMB)", code=_named('print(spell_book["Warm Hands"])'), fails_at=1,
             message_contains='spell_name = "Glow"'),
        dict(why="the cost typed by hand (CMB)", code=_named("print(3)"), fails_at=1, message_contains="follows it"),
        dict(why="the spell's name with no quotes and a space", code=_named("print(spell_book[Warm Hands])"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the other spell's cost", code=_named('print(spell_book["Glow"])'), fails_at=1,
             message_contains="Glow's cost"),
        dict(why="dot access with the variable", code=_named("print(spell_book.spell_name)"), fails_at=0,
             message_contains="has no attribute 'spell_name'"),
        dict(why="spell_name changed in the starter, then read (the step wants Warm Hands, the check changes it)",
             code=NAME_HEAD.replace('"Warm Hands"\n', '"Glow"\n') + "print(spell_book[spell_name])\n", fails_at=1,
             message_contains='Keep `spell_name = "Warm Hands"`'),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-key-from-variable,dict-read", solo="false", dictates="",
             foreign_names="pack,item,rope,lamp,hero") + "\n"
        "P->I->M. The predict is the spec's contrast, `spell_book[\"spell_name\"]` (KeyError: 'spell_name'), with "
        "`spell_book[spell_name]` -> 3 in the question. Investigate: the 6-card quotes sort (G2 R11) is the "
        "'picture' angle, a one-click card sort (another_way `sort`): its answers show only after *Check my sort*, "
        "so a student sorts before seeing them; plus the pair-talk prompt. CP1 [ND]: the cost ends a printed line (words before it are fine), then CMB with "
        "`spell_name = \"Glow\"` (spec). Catches: 4A-02's name-in-quotes habit in a new form (KeyError), the "
        "spell's name typed in, the cost typed. BQ (key from a variable + concat)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-08 broken-spell-4a (debug, three slips)
# ---------------------------------------------------------------------------------------------


def _broken(colon='"name": "Lucky",', name_line='print(lucky["name"])',
            mana_line='print("Mana: " + str(lucky["mana"]))', spend='lucky["mana"] = lucky["mana"] - 2'):
    return (
        "lucky = {\n"
        f"    {colon}\n"
        '    "mana": 26,\n'
        "}\n"
        f"{name_line}\n"
        f"{mana_line}\n"
        f"{spend}\n"
        'print("After Glow: " + str(lucky["mana"]))\n'
    )


# The mana line (line 6) is already right: the capital-letter KeyError is cut here (teacher ruling), since it is
# practised in 4A-04 and checked alone in 4A-S. The other slips keep their line numbers.
BROKEN_STARTER = _broken('"name" = "Lucky",', "print(lucky[name])", 'print("Mana: " + str(lucky["mana"]))',
                         'lucky["mana"] = lucky.mana - 2')
BROKEN_SOLUTION = _broken()
LUCKY_OTHER = {"name": "Pell", "mana": 31}
LUCKY_EV = 'another sheet, name `"Pell"` and mana 31'

_LUCKY_SHEET = r'''
_v = _g.get('lucky')
assert type(_v).__name__ == 'dict', _gone('lucky')
assert type(_v.get('name')).__name__ == 'str' and _v['name'].strip(), ('Keep the key `"name"` in the sheet, holding '
                                                                       "Lucky's name as text: a colon, then the name in quotes.")
assert 'mana' in _v, 'Keep the key `"mana"` in the sheet as it is.'
'''

# A key added to fit a read (`"Name": "Lucky"` beside `"name"`, for `lucky["Name"]`): the read works, but the
# sheet was changed to fit it.
_LUCKY_EXTRA = r'''
_v = _g.get('lucky')
assert type(_v).__name__ == 'dict', _gone('lucky')
_odd = [_k for _k in _v if _k not in ('name', 'mana') and (_near(_k, 'mana') or _near(_k, 'name'))]
assert not _odd, ('Mend the read, not the sheet: `lucky` now has an extra key, `' + (_show(_odd[0]) if _odd else '')
                  + '`. Read with the key the sheet already had, spelled the same way.')
'''

BROKEN_SPELL_4A = dict(
    id="broken-spell-4a",
    title="Broken spell",
    martu=(
        "Lucky's sheet has three slips. Python reports them one at a time. Read the last line of each message first, "
        "then go to the line it names.\n"
        "Mend one, run again, and Python shows you the next. Normal. That is how everyone debugs, yes?"
    ),
    names=["lucky"],
    pair_talk="Pair talk: compare which line each message names, and why. Each of you mends your own screen.",
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="colon-not-equals",
            text="Mend the sheet line Python names first.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Python points at line 2, inside the sheet. What goes between a key and its value?",
                "`{\"dexterity\": 6}`: a key in quotes, a colon, then the value. Inside a sheet the key keeps its "
                "quotes; `=` is for variables.",
                "Change line 2 to `\"name\": \"Lucky\",`.",
            ],
            checks=[("the sheet has a name and a mana", _PRE + _LUCKY_SHEET),
                    ("the reads are mended, not the sheet", _PRE + _LUCKY_EXTRA)],
        ),
        dict(
            id="quote-the-key",
            text="Mend the line that prints Lucky's name.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which name is not defined?",
                "`name` has no quotes, so Python looks for a box called `name`. The sheet has a key `\"name\"`.",
                QUOTES_RULE + " `hero[\"glug\"]` reads the key `\"glug\"`.",
                "Write `print(lucky[\"name\"])` in place of `print(lucky[name])`.",
            ],
            checks=[
                now_check("the name shows", ok="any(_l.endswith(str(lucky['name'])) for _l in _ls)",
                          fix="Keep the line that prints Lucky's name, and read it from the sheet with its key."),
                follows("the name follows the sheet", {"lucky": LUCKY_OTHER}, ev=LUCKY_EV,
                        ok="any(_l.endswith('Pell') for _l in _p)",
                        fix="Read the name from the sheet with its key, so the line follows the sheet.",
                        said="'no line showed `Pell`'"),
            ],
        ),
        dict(
            id="brackets-not-a-dot",
            text="Mend the line that spends 2 mana on Glow.",
            dictated=False,
            hints=[
                "Read Python's last line first. What does it say has no attribute?",
                "A dot is for things like `.lower()`. A dictionary is read another way.",
                "Read a dictionary with square brackets: `hero[\"glug\"]`, never `hero.glug`.",
                "Write `lucky[\"mana\"] = lucky[\"mana\"] - 2` in place of `lucky[\"mana\"] = lucky.mana - 2`.",
            ],
            checks=[
                now_check("the after-Glow line shows", ok="any(_l.startswith('After Glow: ') for _l in _ls)",
                          fix="Keep the last line, which prints `After Glow: ` and his mana."),
                follows("the mana is spent from the sheet", {"lucky": LUCKY_OTHER}, ev=LUCKY_EV,
                        ok="'After Glow: 29' in _p and _R('lucky')['mana'] == 29",
                        fix="Read the old mana from the sheet with square brackets, so the cost comes off whatever he "
                            "has.",
                        said="'the last line should show `After Glow: 29`, and the sheet should hold 29'",
                        rules=[("'After Glow: 29' in _p",
                                "Keep line 7 as a write: `lucky[\"mana\"] = ...` stores the new mana in the sheet, "
                                "then the last line shows it."),
                               ("'After Glow: 24' in _p and _R('lucky')['mana'] == 29",
                                "The last line is typed by hand. Keep `print(\"After Glow: \" + "
                                "str(lucky[\"mana\"]))`, so it shows what the sheet holds."),
                               ("'After Glow: 31' in _p",
                                "Keep the cost: the line takes 2 away from the old mana."),
                               ("lucky['mana'] not in (24, 26) and _R('lucky')['mana'] == 31 - (26 - lucky['mana'])",
                                "Glow costs 2. Keep `- 2` on line 7, so the line takes 2 away from the old "
                                "mana.")]),
            ],
            pass_line="Bomb Shell: Three slips. Three mends. Works.",
        ),
    ],
    solution=BROKEN_SOLUTION,
    assemble=dict(
        lines=[line for line in BROKEN_SOLUTION.splitlines() if line.strip()],
        distractors=['    "name" = "Lucky",', "print(lucky[name])", 'lucky["mana"] = lucky.mana - 2'],
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
                "```text\nline 2  \"name\" = \"Lucky\"\n  a key needs :\nline 5  lucky[name]\n"
                "  a key needs quotes\nline 7  lucky.mana\n  square brackets\n```\nThe line numbers are the "
                "starter's."
            ),
        ),
        dict(
            angle="shorter",
            text="Colon between key and value. Quotes on keys. Square brackets, no dots.",
        ),
    ],
    takeaway="Read the last line, go to the line it names, mend one slip, run again.",
    wrong_answers=[
        dict(why="the starter: = for : inside the sheet first (a SyntaxError beats the runtime slips)",
             code=BROKEN_STARTER, fails_at=0, message_contains="cannot assign to literal"),
        dict(why="colon mended; the key with no quotes",
             code=_broken(name_line="print(lucky[name])", spend='lucky["mana"] = lucky.mana - 2'),
             fails_at=0, message_contains="name 'name' is not defined"),
        dict(why="two mended; dot access (the AttributeError row)", code=_broken(spend='lucky["mana"] = lucky.mana - 2'),
             fails_at=0, message_contains="'dict' object has no attribute 'mana'"),
        dict(why="the colon slip 'mended' by taking the key's quotes off (the explainer's box-name advice): still a SyntaxError",
             code=_broken(colon='name = "Lucky",'), fails_at=0, message_contains="invalid syntax"),
        dict(why="the colon mended, but the name left unquoted",
             code=_broken(colon='"name": Lucky,'), fails_at=0, message_contains="name 'Lucky' is not defined"),
        dict(why="the name line 'mended' by typing the name (CMB)", code=_broken(name_line='print("Lucky")'),
             fails_at=2, message_contains="Pell"),
        dict(why="the name read by position", code=_broken(name_line="print(lucky[0])"), fails_at=0,
             message_contains="KeyError: 0"),
        dict(why="the name line deleted", code=_broken(name_line=""), fails_at=2, message_contains="Keep the line"),
        dict(why="the spend typed by hand: lucky[\"mana\"] = 24 (CMB)", code=_broken(spend='lucky["mana"] = 24'),
             fails_at=3, message_contains="After Glow: 29"),
        dict(why="the spend line deleted (the cost is gone)", code=_broken(spend=""), fails_at=3,
             message_contains="Keep the cost"),
        dict(why="round brackets for the read", code=_broken(spend='lucky["mana"] = lucky("mana") - 2'), fails_at=0,
             message_contains="not callable"),
        dict(why="the name slip 'mended' by a second key in the sheet, `\"Name\"`, read with a capital",
             code=_broken(colon='"name": "Lucky",\n    "Name": "Lucky",', name_line='print(lucky["Name"])'),
             fails_at=1, message_contains="extra key"),
        dict(why="the name slip 'mended' by writing a key to fit the read: lucky[\"Name\"] = lucky[\"name\"]",
             code=_broken(name_line='lucky["Name"] = lucky["name"]\nprint(lucky["Name"])'),
             fails_at=1, message_contains="Mend the read, not the sheet"),
        dict(why="the spend line dropped, the cost taken off inside the print: nothing is stored in the sheet",
             code=_broken(spend="").replace('print("After Glow: " + str(lucky["mana"]))',
                                            'print("After Glow: " + str(lucky["mana"] - 2))'),
             fails_at=3, message_contains="Keep line 7 as a write"),
        dict(why="the last line typed by hand", code=_broken().replace('"After Glow: " + str(lucky["mana"])',
                                                                        '"After Glow: 24"'),
             fails_at=3, message_contains="typed by hand"),
        dict(why="the cost changed (3 for Glow's 2)", code=_broken(spend='lucky["mana"] = lucky["mana"] - 3'),
             fails_at=3, message_contains="Glow costs 2"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="dict-make,dict-read,dict-write,read-traceback", solo="false",
             dictates="", foreign_names="dexterity,hero,glug") + "\n"
        "Broken spell, three of the spec's four slips in the order Python reports them (teacher ruling: the "
        "capital-letter KeyError `lucky[\"Mana\"]` is cut, its third copy in 4A; 4A-04 practises it and 4A-S checks "
        "it alone, which pays for 4A-S's new write; line 6 is now right and the other line numbers are unchanged). "
        "The SyntaxError first (`\"name\" = \"Lucky\"` -> 'cannot assign to literal here'; site request: inside "
        "`{ }` the explainer should say 'Use `:` between a key and its value', not the box-name row, which says "
        "'Take the quotes off'; until that fix lands, CP1's Teach rung says the key keeps its quotes and `=` is for "
        "variables, and WA proves that taking the quotes off is still a crash), then the runtime slips in line "
        "order: `lucky[name]` (NameError, rule 9), `lucky.mana` (AttributeError; site request: the spec's row 'Read "
        "a dictionary with square brackets: `hero[\"mana\"]`'). Each slip left fails at 0 with its own message "
        "(WA). Each mend is CMB with another sheet (name \"Pell\", mana 31), so typed values fail. A key added to "
        "fit a read (`\"Name\": \"Lucky\"` in the sheet, or `lucky[\"Name\"] = lucky[\"name\"]`) fails CP1, 'Mend "
        "the read, not the sheet'. CP3 also reads the sheet after the rerun, so the cost taken off inside the last "
        "`print` (nothing stored) fails, and a changed cost or a typed last line get their own messages. No "
        "partials: a crash fails every checkpoint on the site. About 2 minutes (one slip fewer: -1)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 4A-S solo-4a (SOLO, one bug and one undictated write, done alone)
# ---------------------------------------------------------------------------------------------

SOLO_HEAD = (
    "oogrish = {\n"
    '    "name": "Oogrish",\n'
    '    "mana": 18,\n'
    '    "max_mana": 18,\n'
    "}\n"
)
SOLO_SPEND = 'oogrish["mana"] = oogrish["mana"] - glow_cost'
SOLO_LINE = 'print(oogrish["name"] + ": " + str(oogrish["mana"]))'


def _solo(line=SOLO_LINE, spend=SOLO_SPEND, head=SOLO_HEAD):
    # Line 8 is the spend (empty in the starter), line 9 the print.
    return head + "glow_cost = 4\n" + "# Oogrish casts Glow:\n" + (spend + "\n" if spend else "\n") + line + "\n"


SOLO_STARTER = _solo('print(oogrish["name"] + ": " + str(oogrish["Mana"]))', spend="")
# mana and max mana differ, so "reads the max mana" and "the spell is not spent" show as different lines.
SOLO_OTHER = {"name": "Pell", "mana": 30, "max_mana": 35}

# Mend the read, not the sheet: the sheet keeps "mana", and no key the code READS was added to fit the slip. (A write
# to a near-miss key, `oogrish["Mana"] = ...`, is CP2's slip, so a key that is only written does not count here.)
_SOLO_SHEET = r'''
_v = _g.get('oogrish')
assert type(_v).__name__ == 'dict', _gone('oogrish')
_read = [_n.slice.value for _n in _ast.walk(_tree) if type(_n).__name__ == 'Subscript'
         and type(_n.ctx).__name__ == 'Load' and type(_n.slice).__name__ == 'Constant']
_odd = [_k for _k in _v if _k not in ('name', 'mana', 'max_mana') and (_near(_k, 'mana') or _near(_k, 'name'))
        and _k in _read]
assert 'mana' in _v and not _odd, 'Mend the read, not the sheet: keep the sheet' + "'" + 's keys as they are.'
'''

# The keys the code's prints read, and the sheet's own mana (from the code), for CP1's diagnoses.
SOLO_PRINTS = (
    "_prints = [_c for _c in _ast.walk(_tree) if type(_c).__name__ == 'Call' and getattr(_c.func, 'id', '') == "
    "'print']\n"
    "_printed_keys = [_x.slice.value for _c in _prints for _x in _ast.walk(_c) if type(_x).__name__ == 'Subscript'\n"
    "                 and type(_x.slice).__name__ == 'Constant']\n"
    "_start = _lit_key('oogrish', 'mana')\n"
)

# The lines that write into the sheet (for "Line 8 ..."), whether their right side reads any variable (a typed
# answer reads none), and how many sheets the code types.
SOLO_WRITES = (
    "_writes = [_n for _n in _tree.body if type(_n).__name__ in ('Assign', 'AugAssign')\n"
    "           and any(type(_t).__name__ == 'Subscript' and getattr(_t.value, 'id', '') == 'oogrish'\n"
    "                   for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target]))]\n"
    "_sheets = [_n for _n in _tree.body if type(_n).__name__ == 'Assign' and getattr(_n.targets[0], 'id', '') == "
    "'oogrish']\n"
    "_wl = 'Line ' + str(_writes[0].lineno if _writes else (_sheets[1].lineno if len(_sheets) > 1 else 8))\n"
    "_names_used = [_x.id for _n in _writes for _x in _ast.walk(_n.value) if type(_x).__name__ == 'Name']\n"
    "_typed = bool(_writes) and not _names_used\n"
)

# CP2 SPENT, lean (the kind of slip and the line, never the fix): write-by-key's _SPENT on `oogrish`/`glow_cost`.
_SOLO_SPENT = r'''
_v = _g.get('oogrish')
assert type(_v).__name__ == 'dict', _gone('oogrish')
_start = _lit_key('oogrish', 'mana')
_cost = _g.get('glow_cost')
assert type(_start).__name__ == 'int', 'The sheet' + "'" + 's `"mana"` line no longer holds a number.'
assert type(_cost).__name__ == 'int', '`glow_cost = 4` from the starter is gone or no longer a number.'
_want = _start - _cost
_m = _v.get('mana')
_close = [_k for _k in _v if _k != 'mana' and _near(_k, 'mana')]
_bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
_boxes = [(_t.id, _n.lineno) for _n in _tree.body if type(_n).__name__ == 'Assign' for _t in _n.targets
          if type(_t).__name__ == 'Name' and _t.id not in ('oogrish', 'glow_cost') and _g.get(_t.id) == _want]
_msg = ''
if _m == _start:
    if _close:
        _msg = (_wl + ' writes a new key, `' + _show(_close[0]) + '`. The sheet' + "'" + 's key is `"mana"`, '
                'and it still holds ' + str(_start) + '.')
    elif _bare:
        _msg = 'Line ' + str(_bare[0]) + ' works out the new mana but keeps it nowhere.'
    elif _boxes:
        _msg = ('Line ' + str(_boxes[0][1]) + ' keeps the new mana in a new variable, `' + _boxes[0][0] + '`. '
                '`oogrish["mana"]` still holds ' + str(_start) + '.')
    else:
        _msg = '`oogrish["mana"]` still holds ' + str(_start) + ': Glow is not spent yet.'
elif _m == -_want:
    _msg = _wl + ' takes the mana away from the cost: the wrong way round.'
elif _m in (_cost, -_cost):
    _msg = _wl + ' stores just the cost in `oogrish["mana"]`.'
elif _m == _start + _cost:
    _msg = _wl + ' adds the cost. Casting spends mana.'
elif _m != _want:
    _msg = ('`oogrish["mana"]` holds ' + str(_m) + '. After Glow it should hold ' + str(_want) + ': the old mana '
            'minus `glow_cost`, once.')
assert not _msg, _msg
'''

SOLO_4A = dict(
    id="solo-4a",
    title="Show Mar'tu",
    martu=(
        "A short one, just for you. Oogrish's last line should show his name and his mana, but one slip stops "
        "it. Mend it. Then Oogrish casts Glow: spend `glow_cost` from his sheet, by key."
    ),
    solo=True,
    # Teacher ruling (FORMAT.md, from Unit 2 on): every SOLO item is lean. The crash explainer names the kind of
    # slip and the line, never the fix; Python's own last line stays on screen.
    explainer="lean",
    names=["oogrish", "glow_cost"],
    starter=SOLO_STARTER,
    checkpoints=[
        dict(
            id="oogrish-mana-left",
            text="Mend the last line so it shows Oogrish's name and his mana.",
            dictated=False,
            hints=[
                "Read Python's last line first.",
                "The message names a key. Compare it with the keys in the sheet, letter for letter.",
                "Keys match letter for letter: `[\"Glug\"]` and `[\"glug\"]` are two different keys.",
                "Copy each key from the sheet, as the sheet spells it: when a sheet says `\"gold\": 5`, the read "
                "is `pouch[\"gold\"]`, never `pouch[\"Gold\"]`.",
            ],
            # These hold before and after CP2: the line must show whatever the sheet holds now.
            checks=[
                ("the read is mended, not the sheet", _PRE + _SOLO_SHEET),
                now_check(
                    "the line shows",
                    ok="str(oogrish['name']) + ': ' + str(oogrish['mana']) in _ls",
                    fix="Keep the last line: his name, `: `, then his mana, read from the sheet.",
                    rules=[("'max_mana' in _printed_keys",
                            "That reads the max mana. The line wants his mana."),
                           ("_start != oogrish['mana'] and str(oogrish['name']) + ': ' + str(_start) in _ls",
                            "The last line shows the mana from before Glow: it runs before the spend line.")],
                    pre=SOLO_PRINTS,
                ),
                follows(
                    "the line follows the sheet",
                    {"oogrish": SOLO_OTHER},
                    ev='another sheet, name `"Pell"`, mana 30 and max mana 35',
                    ok="'Pell: ' + str(_R('oogrish')['mana']) in _p",
                    fix="Read the name and the mana from the sheet, so the line follows it.",
                    said="'the line should show `Pell: ' + str(_R('oogrish')['mana']) + '`'",
                    rules=[("'Pell: 35' in _p", "That reads the max mana. The line wants his mana.")],
                ),
            ],
        ),
        dict(
            id="spend-glow-cost",
            text="Oogrish casts Glow: under the comment, take `glow_cost` from his mana, by key.",
            dictated=False,
            hints=[
                "Read the old mana on the right, take away `glow_cost`, store it on the left.",
                "`hero[\"mana\"] = hero[\"mana\"] - cost` reads the old value and stores the new one.",
                "The same shape spends from any sheet: `pouch[\"gold\"] = pouch[\"gold\"] - price` takes `price` "
                "from the gold and keeps the new gold on the sheet.",
            ],
            checks=[
                ("the mana is spent", _PRE + SOLO_WRITES + _SOLO_SPENT),
                follows(
                    "the mana follows the sheet and the cost",
                    {"oogrish": SOLO_OTHER, "glow_cost": 3},
                    ev='another sheet, name `"Pell"`, mana 30 and max mana 35, and `glow_cost = 3`',
                    ok="_R('oogrish')['mana'] == 27",
                    fix="does not follow the sheet and the cost.",
                    said="'the mana should become 27'",
                    rules=[("len(_sheets) > 1", "types a second `oogrish = {...}` sheet."),
                           ("_typed", "has the new mana typed in."),
                           ("_R('oogrish')['mana'] == 30 - 4", "takes away a typed 4, not `glow_cost`."),
                           ("_R('oogrish')['mana'] == 18 - 3", "starts from a typed 18, not the sheet's mana."),
                           ("_R('oogrish')['mana'] == 35 - 3", "reads the max mana, not the mana.")],
                    pre=SOLO_WRITES,
                    lead="_wl + ' '",
                ),
            ],
            pass_line=(
                "Mar'tu: You did that alone. I saw. On your map: ✓ read a value by its key, ✓ change a value by its "
                "key."
            ),
        ),
    ],
    solution=_solo(),
    partials=[_solo(spend="")],
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line of the message. 2. Find that key in the sheet. "
                                        "3. Spell it the same way."),
        dict(angle="shorter", text="A KeyError names the key Python could not find. Copy the key from the sheet."),
        dict(
            angle="from earlier",
            label="Spending, by key",
            text=(
                "Spending is one line: the key on the left of `=` gets the old mana minus the cost, read on the "
                "right. Same move as Gearshift's Fire Bolt."
            ),
        ),
    ],
    takeaway=(
        "On your own: a KeyError names the key, so spell it as the sheet does; spend by key with "
        "`oogrish[\"mana\"] = oogrish[\"mana\"] - glow_cost`."
    ),
    wrong_answers=[
        dict(why="the starter: capital M (seat A's slip)", code=SOLO_STARTER, fails_at=0, message_contains="KeyError: 'Mana'"),
        dict(why="seat B's slip, dot access", code=_solo('print(oogrish["name"] + ": " + str(oogrish.mana))'), fails_at=0,
             message_contains="has no attribute 'mana'"),
        dict(why="the line typed by hand (CMB)", code=_solo('print("Oogrish: 14")'), fails_at=1, message_contains="Pell: 26"),
        dict(why="the line typed by hand before the spend (CMB): it shows 18 now, not the sheet's 30",
             code=_solo('print("Oogrish: 18")', spend=""), fails_at=1, message_contains="Pell: 30"),
        dict(why="the max mana read instead", code=_solo('print(oogrish["name"] + ": " + str(oogrish["max_mana"]))'),
             fails_at=1, message_contains="max mana"),
        dict(why="the max mana read before the spend (18 = 18 now; only another sheet shows it)",
             code=_solo('print(oogrish["name"] + ": " + str(oogrish["max_mana"]))', spend=""), fails_at=1,
             message_contains="That reads the max mana"),
        dict(why="a key added to fit the slip: the rerun's sheet has no Mana",
             code=_solo('print(oogrish["name"] + ": " + str(oogrish["Mana"]))',
                        head='oogrish = {\n    "name": "Oogrish",\n    "mana": 18,\n    "Mana": 14,\n    "max_mana": 18,\n}\n'),
             fails_at=1, message_contains="Mend the read, not the sheet"),
        dict(why="no str()", code=_solo('print(oogrish["name"] + ": " + oogrish["mana"])'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="a key written to fit the slip: oogrish[\"Mana\"] = oogrish[\"mana\"] above the line",
             code=_solo('oogrish["Mana"] = oogrish["mana"]\nprint(oogrish["name"] + ": " + str(oogrish["Mana"]))'),
             fails_at=1, message_contains="Mend the read, not the sheet"),
        dict(why="the sheet's key renamed to Mana everywhere, so the read matches a changed sheet",
             code=_solo('print(oogrish["name"] + ": " + str(oogrish["Mana"]))',
                        spend='oogrish["Mana"] = oogrish["Mana"] - glow_cost',
                        head='oogrish = {\n    "name": "Oogrish",\n    "Mana": 18,\n    "max_mana": 18,\n}\n'),
             fails_at=1, message_contains="Mend the read, not the sheet"),
        dict(why="the spend written below the print: the line shows the mana from before Glow",
             code=_solo(SOLO_LINE + "\n" + SOLO_SPEND, spend=""), fails_at=1, message_contains="before Glow"),
        dict(why="CP2 not done: Glow not spent yet", code=_solo(spend=""), fails_at=2, message_contains="not spent yet"),
        dict(why="the cost typed: - 4 for - glow_cost (CMB with glow_cost = 3)",
             code=_solo(spend='oogrish["mana"] = oogrish["mana"] - 4'), fails_at=2,
             message_contains="Line 8 takes away a typed 4"),
        dict(why="the new mana typed by hand: hero[\"mana\"] = 7 style (CMB)", code=_solo(spend='oogrish["mana"] = 14'),
             fails_at=2, message_contains="Line 8 has the new mana typed in"),
        dict(why="the old mana typed: 18 - glow_cost (CMB on the sheet)",
             code=_solo(spend='oogrish["mana"] = 18 - glow_cost'), fails_at=2, message_contains="typed 18"),
        dict(why="the spend typed in above the comment, with a typed 4: the line named is the spend's own",
             code=_solo(spend="").replace("glow_cost = 4\n", 'glow_cost = 4\noogrish["mana"] = oogrish["mana"] - 4\n'),
             fails_at=2, message_contains="Line 7 takes away a typed 4"),
        dict(why="the max mana read for the mana (both are 18 in the starter, so only another sheet shows it)",
             code=_solo(spend='oogrish["mana"] = oogrish["max_mana"] - glow_cost'), fails_at=2,
             message_contains="Line 8 reads the max mana"),
        dict(why="a second sheet typed with the new mana, instead of writing by key",
             code=_solo(spend='oogrish = {"name": "Oogrish", "mana": 14, "max_mana": 18}'), fails_at=2,
             message_contains="Line 8 types a second `oogrish = {...}`"),
        dict(why="worked out, kept nowhere (BARE)", code=_solo(spend='oogrish["mana"] - glow_cost'), fails_at=2,
             message_contains="keeps it nowhere"),
        dict(why="a new variable instead of the key (NEWBOX)", code=_solo(spend='mana = oogrish["mana"] - glow_cost'),
             fails_at=2, message_contains="new variable, `mana`"),
        dict(why="a near-miss key on the left: a new key Mana (KEY)",
             code=_solo(spend='oogrish["Mana"] = oogrish["mana"] - glow_cost'), fails_at=2,
             message_contains='new key, `"Mana"`'),
        dict(why="the subtraction the wrong way round", code=_solo(spend='oogrish["mana"] = glow_cost - oogrish["mana"]'),
             fails_at=2, message_contains="wrong way round"),
        dict(why="the cost added", code=_solo(spend='oogrish["mana"] = oogrish["mana"] + glow_cost'), fails_at=2,
             message_contains="adds the cost"),
        dict(why="only the cost stored", code=_solo(spend='oogrish["mana"] = glow_cost'), fails_at=2,
             message_contains="just the cost"),
        dict(why="dot access on the right of the spend", code=_solo(spend='oogrish["mana"] = oogrish.mana - glow_cost'),
             fails_at=0, message_contains="has no attribute 'mana'"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-read,dict-write", solo="true", dictates="",
             foreign_names="glug,hero,cost,gold,pouch,price",
             seat_b='oogrish.mana for oogrish["mana"] in the last line (AttributeError); glow_cost = 5') + "\n"
        "SOLO, one bug and one undictated write (C6), about 3 minutes. CP1 [ND]: seat A (and anyone solo) gets "
        "`oogrish[\"Mana\"]`; seat B would get `oogrish.mana` (WA proves it) once pair mode ships. Values differ "
        "per seat (seat B: Oogrish casts for 5, so seat B's spend uses its own cost, `glow_cost = 5`). CP1's "
        "checks hold before and after CP2: the line must show whatever the sheet holds now (own run, then CMB with "
        "another sheet, \"Pell\", mana 30, max mana 35). The sheet must keep its keys: a key the code reads, added "
        "or renamed to fit the slip, fails 'Mend the read, not the sheet' (a write to a near-miss key is CP2's "
        "slip). A typed line, the max mana read and the line run before the spend each get their own message. "
        "CP2 [ND] (teacher ruling: a write by key checked solo, which the cut of 4A-08's KeyError pays for): "
        "write-by-key's SPENT pattern on `oogrish` and `glow_cost` (BARE, NEWBOX, a near-miss key, the sign, the "
        "cost added, the cost alone), then CMB with another sheet and `glow_cost = 3` (a typed number, a typed "
        "`- 4`, a typed 18, the max mana read, a second sheet). CP2's messages are lean: the kind of slip and the "
        "line, never the fix. The pass line (the map ticks) is CP2's. Recorded, never blocking, never shown to a "
        "partner. explainer='lean' (teacher's ruling, every SOLO from Unit 2 on)."
    ),
)

LESSON_4A = dict(
    kind="lesson",
    id="stat-sheets",
    title="Stat Sheets",
    minutes=32,
    summary=(
        "Make hero stat sheets with dictionaries, read and change values by key, mend KeyErrors, ask `in` and "
        "`not in`, and use a key kept in a variable."
    ),
    notes=(
        "Lesson 4A (CC; 4A-01 and 4A-08 SC). Preceded by 4a-remembers. Exactly one SOLO (solo-4a). Non-dictated "
        "checkpoints: 4A-01, 4A-02 CP1-2, 4A-03, 4A-04 (mends), 4A-05 CP2, 4A-06, 4A-07, 4A-08 (three mends), 4A-S "
        "CP1-2. Dictated: 4A-05 CP1 only (the unit's first write; it carries the Point-at-it pass line). Story beat: "
        "4A-01 (protected). Minutes: 32, unchanged by the teacher's Unit 5 ruling: 4A-S's undictated write +1.5, "
        "the capital-letter KeyError cut from 4A-08 -1, 4A-06's `if False:` scaffold about -0.5 for students who "
        "would stall. Per exercise, about 2 + 6 + 4 + 3 + 5 + 3.5 + 4 + 2 + 3.5 (4A-01 to 4A-S; the estimates run "
        "a little over the 32, as before)."
    ),
    exercises=[WHICH_NUMBER, MAKE_A_SHEET, READ_BY_KEY, KEY_ERRORS, WRITE_BY_KEY, IS_IT_IN, KEY_FROM_A_BOX,
               BROKEN_SPELL_4A, SOLO_4A],
)

# =============================================================================================
# Article 4-A1 "Why Does This Work? Keys and .get()" (optional)
# =============================================================================================

CANTEEN_HEAD = 'lucky = {"name": "Lucky", "mana": 26}\n'
CANTEEN_STARTER = CANTEEN_HEAD + 'print(lucky["glug"])\n'


def _canteen(line='print(lucky.get("glug", 0))'):
    return CANTEEN_HEAD + line + "\n"


CANTEEN = dict(
    id="lucky-canteen",
    title="Lucky's canteen",
    martu=(
        "Lucky's sheet has no `\"glug\"` key yet, so `lucky[\"glug\"]` stops with a KeyError. Run it and see.\n"
        "[[.get()|`.get()`]] can give 0 instead."
    ),
    example='hero = {"mana": 7}\nprint(hero.get("mana", 0))\nprint(hero.get("ore", 0))\n',
    example_output="7\n0",
    names=["lucky"],
    starter=CANTEEN_STARTER,
    checkpoints=[
        dict(
            id="get-with-a-default",
            text="Change the last line so it shows 0 when there is no `\"glug\"` key, using `.get()`.",
            dictated=False,
            hints=[
                "`.get()` takes two things, with a comma between: the key in quotes, then what to give back when "
                "the key is missing.",
                "`hero.get(\"ore\", 0)` gives the ore, or 0 if there is no `\"ore\"` key.",
                "Write `print(lucky.get(\"glug\", 0))` in place of `print(lucky[\"glug\"])`.",
            ],
            checks=[
                now_check(
                    "0 shows with no glug",
                    ok="_ends_in(_ls, 0) and _uses('attr:get')",
                    fix="Use `.get()` with the key and a default of 0, so the line shows 0 when there is no glug.",
                    rules=[
                        ("any(_l.endswith('None') for _l in _ls)",
                         "`.get(\"glug\")` with only the key gives back `None` when the key is missing. Add the "
                         "default after a comma: `, 0`."),
                        ("not _uses('attr:get')", "Use `.get()`: it gives a default instead of a KeyError."),
                    ],
                ),
                follows(
                    "the glug shows when there is some",
                    {"lucky": {"name": "Lucky", "mana": 26, "glug": 2}},
                    ev='a sheet with `"glug": 2`',
                    ok="_ends_in(_p, 2)",
                    fix="Read the key with `.get()`, so the line shows the glug when Lucky has some.",
                    said="'the line should show 2'",
                    # the keys handed to .get(), read from the code: a near miss ("Glug") always gives the default.
                    pre=("_gk = [_c.args[0].value for _c in _ast.walk(_tree) if type(_c).__name__ == 'Call'\n"
                         "       and getattr(_c.func, 'attr', '') == 'get' and _c.args\n"
                         "       and type(_c.args[0]).__name__ == 'Constant']\n"),
                    rules=[("any(_near(_k, 'glug') for _k in _gk) and 'glug' not in _gk",
                            "Spell the key exactly like the sheet's: `\"glug\"`, all small letters. Python matches "
                            "keys letter for letter, so a near miss always gives the 0.")],
                ),
            ],
            pass_line="Lucky: Zero glug. Typical.",
        ),
    ],
    solution=_canteen(),
    another_way=[
        dict(
            angle="everyday",
            text=(
                "Asking a friend *how much glug is left?* A kind friend says *none* instead of shouting. `.get()` is "
                "the kind friend; `lucky[\"glug\"]` shouts."
            ),
        ),
        dict(angle="shorter", text="`sheet.get(\"key\", 0)`: the value, or 0 if the key is missing."),
    ],
    takeaway="`lucky.get(\"glug\", 0)` gives the value, or the default when the key is missing.",
    assemble=dict(
        lines=['lucky = {"name": "Lucky", "mana": 26}', 'print(lucky.get("glug", 0))'],
        distractors=['print(lucky["glug"])', 'print(lucky.get("glug"))', 'print(0)'],
    ),
    wrong_answers=[
        dict(why="starter unchanged", code=CANTEEN_STARTER, fails_at=0, message_contains="KeyError: 'glug'"),
        dict(why="0 typed by hand", code=_canteen("print(0)"), fails_at=1, message_contains="Use `.get()`"),
        dict(why="0 typed by hand next to a .get() that prints nothing useful (CMB)",
             code=_canteen('x = lucky.get("glug", 0)\nprint(0)'), fails_at=1, message_contains="should show 2"),
        dict(why="no default: None", code=_canteen('print(lucky.get("glug"))'), fails_at=1, message_contains="None"),
        dict(why="a near-miss key in .get(): Glug always gives the default (KEY)",
             code=_canteen('print(lucky.get("Glug", 0))'), fails_at=1, message_contains="letter for letter"),
        dict(why="the key with no quotes", code=_canteen("print(lucky.get(glug, 0))"), fails_at=0,
             message_contains="name 'glug' is not defined"),
        dict(why="square brackets on get", code=_canteen('print(lucky.get["glug", 0])'), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="the default typed into the read", code=_canteen('print(lucky["glug", 0])'), fails_at=0,
             message_contains="KeyError"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="dict-read", solo="false", dictates="",
             foreign_names="hero,ore,moth") + "\n"
        "The article's try-it. The example builds its own `hero` (2.12 rule 3: a setup-made sheet would hide "
        "attr:get). CMB with a sheet that has glug 2, so `print(0)` fails."
    ),
)

ARTICLE_4A1 = dict(
    kind="article",
    id="keys-and-get",
    title="Why Does This Work? Keys and .get()",
    optional=True,
    minutes=8,
    summary="Why a key can only appear once, how `.get()` avoids a KeyError, and why `in` is fast.",
    introduces=["attr:get"],
    body=(
        "Three things that make dictionaries work. Read them when you like. Nothing here is scored.\n"
        "*Keys are unique.* A sheet has only one of each key. Give a key a value again, and the new value takes "
        "the old one's place:\n"
        "```python\nhero = {\"name\": \"Moth\", \"glug\": 1}\nhero[\"glug\"] = 3\nprint(hero)\n```\n"
        "It prints `{'name': 'Moth', 'glug': 3}`. There is still only one `\"glug\"`. When Python prints a whole "
        "sheet it uses `'` marks. Same text.\n"
        "*A default instead of an error.* Reading a key that is not there stops the program with a [[KeyError]]. "
        "[[.get()|`.get()`]] asks more gently. `hero.get(\"glug\", 0)` gives the value when the key is there, and 0 when "
        "it is not:\n"
        "```python\nhero = {\"name\": \"Moth\", \"mana\": 7}\nprint(hero.get(\"mana\", 0))\n"
        "print(hero.get(\"glug\", 0))\n```\n"
        "It prints 7, then 0. No KeyError.\n"
        "*Fast questions.* To find a value in a list, Python checks the items one by one, like opening a row of "
        "lockers. A dictionary works like the index at the back of a book: Python jumps straight to the key. So "
        "`\"Glow\" in spell_book` takes about the same time for 3 spells or 3,000."
    ),
    examples=[
        dict(code='hero = {"name": "Moth", "glug": 1}\nhero["glug"] = 3\nprint(hero)\n',
             output="{'name': 'Moth', 'glug': 3}"),
        dict(code='hero = {"name": "Moth", "mana": 7}\nprint(hero.get("mana", 0))\nprint(hero.get("glug", 0))\n',
             output="7\n0"),
    ],
    exercises=[CANTEEN],
    notes=(
        "Article 4-A1 (O). The spec's three points: unique keys (a second assignment overwrites), `.get(\"glug\", "
        "0)` (intro attr:get; the examples build their own `hero`, 2.12 rule 3), and why `in` is fast (the book "
        "index picture). One try-it, Lucky's canteen. Optional: core items never rely on attr:get."
    ),
)

ITEMS = [REMEMBERS_4A, LESSON_4A, ARTICLE_4A1]
