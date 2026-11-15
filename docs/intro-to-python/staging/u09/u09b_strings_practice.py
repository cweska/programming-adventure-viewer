"""Unit 9 "Strings" ("Runes and Ribbons"), part b: Extra practice 9X (pool: 8A-04 is-it-in-there, 8A-05
letter-by-letter, 8A-08 broken-spell-8a, and Quiz 8A), the optional Project 8P1 "The Water-Stained Log" (recommended),
the optional Project 8P2 "The Institute Cipher" (browser-only), and the optional advanced challenge "Name Tags, From
Blank" (tag-from-blank, 10 min, after 8P2; a write-from-blank task as Units 3 to 7 have, costing no one core time).

Spec: design/curriculum.md, "## Unit 9 · Strings", items 4 to 6 ("### Extra practice 9X [pool] and the projects").
Not in this file (by assignment): Lessons 8A and 8B, Quiz 8B (u09a), Quick Check 8 and the Strings cheatsheet (u09c).
Introduces nothing new (concept_map.json plans no tokens for u09b). Everything comes from earlier units or u09a:
`in` (u04b), `for` (u06a), `continue` (u06b), `.lower()` (u02a), `def`/`return` (Unit 3), `len()`, `range()`,
`sum()`, indexes and slices (Unit 4), `%` (u01d's optional Clock Math article, the named prerequisite of 8P2,
2.12 rule 2), and from u09a (planned): `.upper()`, `.split()`, `.strip()`, `.replace()`, `.join()`, `.find()`,
f-strings (the challenge names Lesson 8B as its prerequisite).
The 9X items (8A's pool) use only 8A-level tools: `in`, `.lower()`, loops over letters, indexes, slices and `len()`.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN text work there:
`dialogue_input = dialogue_input.lower()` and `.capitalize()` (program-dialogue-prompt), `option_1.lower().capitalize()`
(program-dialogue-options), the bars `"█" * caster["mana"]` and the `+ str()` return line (mana-bars), the red Ley
Clock (red-clock) and the chalk wall (chalk-wall). Campaign links are "you've seen this, now you'll get it". Every
student has their own device; pair talk is optional and every checkpoint is solo.

Help ladder as fields (FORMAT.md, the Unit 2 fix pass, as Unit 7): hints[0] Where to look, the middle hints Teach me
(a tiny example with other names, listed in foreign_names), the last hint Show me how: the step's own line in
backticks, whose start up to its first `(` or `=` is Start me off (always a start the solution uses; no hint 1 is a
"Start like this"). 3 or 4 hints per checkpoint, then another_way (3 or 4 angles), assemble (More structure) on every
exercise, and the solution (Compare). Debug steps start at "Read Python's last line". Terminology (2.9): "function",
"parameter", "returns", "variable"; "text" for a string in plain prose; the quotes sentence word for word.

Check codes (curriculum 2.5), built from the _PX helpers below. check() puts in front of each check only the helpers
it uses (as u07c does). Every call a check makes uses fresh values the task never uses (lint b), with prints kept
private; nothing a check does shows in the console:
  PAR / PAR-CONST / RET  8A-04 (`clock_warning` on four fresh reports, two with capitals), 8A-05 (`count_full` on
           seven fresh bars of different lengths, so a typed number or `len()` can't follow them), 8P2 tasks 1-3
           (`shift_letter`, `encode`, `decode` against a reference cipher, on letters, wrap-arounds past z, a space
           and a "!"), the side quests (`burst_coming`, `count_empty`, `encode_keys`), and the challenge
           (`name_tag` on `("Pell", 7)` and `("moss", 12)`, its parameter names checked letter for letter).
  CMB      `_rerun()` runs the program again in a fresh namespace with the FIRST top-level `name = ...` line given
           another value: 8A-08 (`tag` and `bar`), 8P1 (two other messy logs, every task), 8P2 (another coded note,
           another `my_note`). A value typed by hand stays the same in the rerun and gets "typed by hand".
  OUT      never alone on a computed value (lint a): every printed answer is also checked on a rerun.
Messages: the fix first, then what happened, then the evidence in brackets, "(Mar'tu's check called
`count_full("█░█░█")`, only inside the check: it gave back 1, not 3.)". Values the check made are shown; a value the
student's code handed back is shown only when it is a number, a single character, or text the student did not type
(`_said`): a student's own words never come back (2.11). Invented Tor values only (Pell, Moss, ember, frost veil).
A crash inside a student's function during the check's own calls gets `_why()` (as Units 3 and 7, and u09a's): "Inside
`fn`, Python stopped: ...", then why in plain words (a name from the example or the hints, a near-miss parameter or
variable, a name used before it is made: "Make `x` first, then use it", a method called like a function, and the
unit's TypeError / AttributeError / IndexError rows), then the evidence. Each exercise has a wrong answer proving it.

The class's slips for this unit, each proven by a wrong_answers entry (in the exercise named):
  * a method called and its result not kept (`report.lower()` on its own line, then `report` used unchanged): 8A-04
    CP2, 8A-08 CP2 (`tag.replace(...)` alone), 8P1 tasks 1, 2 and 5 (`log.split("|")`, `mark.replace(...)`,
    `clean.strip()`, `", ".join(...)` on their own lines);
  * `lower(report)` as if it were a function: 8A-04 (NameError), 8P1 task 1 (`split(log, "|")`);
  * a letter changed in place (`tag[0] = "L"`, TypeError: 'str' object does not support item assignment): 8A-08 CP2,
    Quiz 8A Q4, 8P2 task 2 (`message[i] = ...` inside `encode`);
  * an index off by one or past the end, or a slice that misses its end: 8A-08 CP1 (`tag[5]`, `tag[len(tag)]`, a
    typed `[4]` that only fits five letters), 8A-08 CP2 (`tag[2:]`, `tag[1:4]`), Quiz 8A Q1-Q3, 8P1 task 4b
    (`range(len(hours))`: the first shrink reads `hours[-1]`), 8P2 task 1 (no `% 26`: IndexError past z);
  * `\\n` and escapes are u09a's (8A-06); this part prints no quotes inside quotes;
  * `.split()` hands back a LIST, then it is treated as text (`marks.replace(...)`: AttributeError): 8P1 task 2;
    `.split()` with empty brackets (cuts at spaces): 8P1 task 1;
  * `.join` called the wrong way round (`clean_marks.join(", ")`: AttributeError) and joining numbers (TypeError:
    sequence item 0: expected str instance, int found): 8P1 task 5;
  * `int()` on text that isn't only digits (`int(" 48 hrs")`, `int("4?")`: ValueError): 8P1 task 3 and its side
    quest. NOTE: `int("7 ")` is NOT an error in Python 3 (int() ignores spaces at the ends), so the strip slip is
    caught on the text itself (8P1 task 2: clean marks with spaces, and strip-before-replace leaving `"48 "`);
  * an f-string without the `f` (prints `{total}` as it is), mismatched braces (SyntaxError: f-string: expecting
    '}'), and a `+ str()` line where the task asks for the f-string twin: 8P1 task 6, the challenge;
  * `+` between text and a number without `str()` (TypeError: can only concatenate str (not "int") to str): 8A-08 CP3,
    8P1 task 6, the challenge;
  * `.find()` returning -1 read as the last place (the space shifted into a letter): 8P2 task 1; `.find()` used
    for a yes/no question: 8A-04;
  * case-sensitive `in` (`"red" in "RED"` is False): 8A-04 CP2, Quiz 8A Q5, the 8A-04 predict;
  * the finished text typed by hand instead of built from the values: 8A-08 (each step), 8P1 (each task), 8P2 tasks
    4-5 (the decoded note typed, a coded note typed), the challenge (a typed tag, tags typed into the prints).
  Also: print for return (8A-04, 8A-05, 8P2), the parameter in quotes (8A-04 `"report"`, 8P2 `"note"`), `==` for `in`
  and the two sides of `in` swapped (8A-04), `return` inside the loop and the counter reset inside the loop (8A-05,
  8P2), `blocks + 1` thrown away (8A-05), the whole bar compared instead of the letter, a place compared instead
  of the letter at it (8A-05), the empty blocks counted (8A-05), `len(26)` and `len("bar")` (8A-08), shrinks the
  wrong way round (8P1), decode that shifts forward again (8P2), a key of 0 or 26 that hides nothing (8P2).
  From the check-breaking pass: a part of the word (`"re" in report`, caught by "green reeds"), each spelling typed
  and joined with `or` in place of `.lower()` (caught by a caps-lock `rED`), a bare text beside `or`
  (`"red" or "RED" in report`), `.lower()` on the typed text, answers typed for the check's own reports (8A-04);
  a loop added beside `.count()`, `blocks = len(bar)` in a loop, `for letter in "bar"`, `blocks =+ 1`,
  `blocks = 1` (8A-05); `tag[1]` for `tag[1:]`, a typed slice end `[1:5]` (8A-08); an f-string added beside the
  `+ str()` line that really shows the numbers, the count typed into the f-string, a loop join with a trailing
  `", "` (8P1); `place + key % 26` (precedence), `for letter in "message"`, the key or the note typed into the
  `encode(...)` call (8P2). Loosened: any loop counts in 8A-05 (`while`, a list comprehension, `.count()` on the
  loop's own letter); 8P1 task 1 accepts marks stripped while splitting; task 5 accepts the clean line printed
  inside a longer line.

Deviations from the spec, each small and noted on its item:
  * 8A-04 has two checkpoints (plain `in`, then any capitals with `.lower()`), so the capitals slip has a step of its
    own; the spec's "The clock is RED." -> True is checkpoint 2's job.
  * 8A-05 has two checkpoints: walk the bar and count every pass, then count only the full blocks.
  * 8A-08 has the spec's three loud bugs, one checkpoint each. A crash fails every checkpoint, so each loud bug left
    fails at 0 and there are no partials (as u04a's broken spell).
  * 8P1's task 2 cleans the text (replace, then strip) into `clean_marks`, and task 3 makes the numbers (int) into
    `hours`: `int()` alone would hide a missing strip, and task 5 joins the clean TEXT.
  * 8P2 adds the starter's "should show" calls, and its task 5 is the spec's "your own coded note"; the pair talk
    swaps notes, each student decoding on their own screen. The IDLE option stays off: browser-only until the
    teacher confirms IDLE [OWNER].
  * 8P1's task 4 is two checkpoints (4a the total, 4b the shrinks), and its starter gives the first loop line once
    (teacher's revision).
  * The challenge "Name Tags, From Blank" is not in the spec (teacher's revision): optional, advanced, 10 min.

Phone width: fenced pictures, examples, predict and quiz code keep to 36 characters a line. Editor code keeps
comments to 36; the exceptions are Lucky's log, the spec's own 54-character string (62 with `log = `), kept whole on
one line (as u04's chalk wall), and 8P2's `alphabet = "abc...z"` line (39). The challenge's solution, assemble
lines and pictures keep every line to 36.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u09b
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
MODULE_1 = "leylines-awaken"
MODULE_2 = "friends-in-low-places"
ABC = "abcdefghijklmnopqrstuvwxyz"


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
# check only the helpers it uses, and the helpers those use, so the unit JSON stays small (as u07c does).
# Builtins come from `_B`, so a student's `sum = 0` or `len = 5` can't break a check.
# ---------------------------------------------------------------------------------------------

_PX = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__
_ABC = 'abcdefghijklmnopqrstuvwxyz'


def _err(_e):
    return type(_e).__name__ + (': ' + _B.str(_e) if _B.str(_e) else '')


def _ev(_what, _said=''):
    return " (Mar'tu's check " + _what + ', only inside the check' + ((': ' + _said) if _said else '') + '.)'


def _sh(_v):
    # A value the check itself made (a fresh argument, the answer it expects): shown as code.
    if type(_v).__name__ == 'str':
        return '`"' + _v + '"`'
    return '`' + _B.str(_v) + '`'


def _typed(_v):
    # True when the text sits inside a string the student typed (then it may be their own words).
    return _B.bool([_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Constant'
                    and type(_n.value).__name__ == 'str' and _v in _n.value])


def _said(_v):
    # A value the student's code handed back. Never a student's own words (2.11): typed text is not repeated.
    if _v is None:
        return '`None`'
    _t = type(_v).__name__
    if _t in ('int', 'float', 'bool'):
        return '`' + _B.str(_v) + '`'
    if _t == 'str':
        if _v == '':
            return 'empty text, `""`'
        if _B.len(_v) == 1 and _v != '`':
            return '`"' + _v + '"`'
        if _B.len(_v) > 40 or '`' in _v or _typed(_v):
            return 'some other text'
        return '`"' + _v + '"`'
    return {'list': 'a list', 'dict': 'a dictionary', 'tuple': 'a tuple', 'function': 'a function'}.get(_t, 'a ' + _t)


def _edits(_a, _b):
    _prev = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _x in _B.enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in _B.enumerate(_b, 1):
            _cur.append(_B.min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b):
    # A near miss for a name: case, a plural, 1-2 edits, or one inside the other.
    if _a == _b:
        return False
    _la, _lb = _a.lower(), _b.lower()
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    if _B.min(_B.len(_la), _B.len(_lb)) >= 4 and _edits(_la, _lb) <= 2:
        return True
    return _B.len(_la) >= 5 and (_la in _lb or _lb in _la)


def _params(_f):
    _c = getattr(_f, '__code__', None)
    return _B.list(_c.co_varnames[:_c.co_argcount]) if _c is not None else []


def _defs():
    return {_n.name: _n for _n in _tree.body if type(_n).__name__ == 'FunctionDef'}


def _top():
    return [_n for _n in _tree.body if type(_n).__name__ != 'FunctionDef']


def _find(_name):
    # The student's function `_name`, or the message that says why it isn't there.
    _v = _g.get(_name)
    if callable(_v) and type(_v).__name__ == 'function':
        return _v, ''
    if _name in _g:
        return None, ('`' + _name + '` is a variable now. Keep it a function, made with `def`: a line that starts `def '
                      + _name + '(`.')
    _near = _B.sorted(_k for _k, _x in _B.list(_g.items()) if type(_x).__name__ == 'function'
                      and not _k.startswith('_') and _close(_k, _name))
    if _near:
        return None, 'Python matches names letter for letter: you wrote `' + _near[0] + '`, the task needs `' + _name + '`.'
    return None, 'Keep the function `' + _name + '` from the starter, with its `def` line.'


def _need(_name, _want):
    _f, _m = _find(_name)
    assert _f, _m
    assert _params(_f) == _want, ('Keep the parameters from the starter: `def ' + _name + '(' + ', '.join(_want)
                                  + '):`. Python matches names letter for letter.')
    return _f


def _need_def(_name, _nparams, _sig):
    # A function written from a blank page: `_name`, with the parameters of `_sig`, letter for letter.
    _f, _m = _find(_name)
    if _f is None:
        assert _name in _g or 'letter for letter' in _m, (
            'Write `' + _name + '` with `def`, at the top: a line that starts `' + _sig + '`, with its lines '
            'indented under it.')
        assert False, _m
    _want = [_p.strip() for _p in _sig[_sig.index('(') + 1:_sig.index(')')].split(',')]
    _ps = _params(_f)
    assert _B.len(_ps) == _nparams, ('Give `' + _name + '` ' + _B.str(_nparams) + ' parameters, like `' + _sig
                                     + '`. It has ' + _B.str(_B.len(_ps)) + '.')
    for _p, _w in _B.zip(_ps, _want):
        assert _p == _w or not _close(_p, _w), ('Name the parameter `' + _w + '`, letter for letter: you wrote `'
                                                + _p + '`.')
    assert _ps == _want, ('Name the parameters `' + '` and `'.join(_want) + '`, in that order, like `' + _sig
                          + '`. Python matches names letter for letter.')
    return _f


def _why(_name, _e, _what, _foreign=()):
    # Python stopped inside the student's function while Mar'tu's check called it (as Units 3 and 7, and u09a's
    # _why): where, why in plain words (a name from Mar'tu's example, a near miss, a name used before it is made, a
    # method called like a function, the unit's TypeError / AttributeError / IndexError rows), then the evidence.
    _f = _g.get(_name)
    _ps = _params(_f) if type(_f).__name__ == 'function' else []
    _d = _defs().get(_name)
    _made = [] if _d is None else [_n.id for _n in _ast.walk(_d) if type(_n).__name__ == 'Name'
                                   and type(_n.ctx).__name__ == 'Store']
    _k = type(_e).__name__
    _s = _B.str(_e)
    _lead = 'Inside `' + _name + '`, Python stopped: ' + _err(_e) + '. '
    _pl = ''
    if _B.len(_ps) == 1:
        _pl = ' The parameter of `' + _name + '` is `' + _ps[0] + '`.'
    elif _ps:
        _pl = ' The parameters of `' + _name + '` are `' + '` and `'.join(_ps) + '`.'
    _x = ''
    if _k in ('NameError', 'UnboundLocalError'):
        _x = getattr(_e, 'name', None) or ''
        if not _x:
            _m = _re.search(r"'(\w+)'", _s)
            _x = _m.group(1) if _m else ''
    if not _x:
        _say = 'Mend that line, then Run again.'
        _attr = _re.search(r"attribute '(\w+)'", _s)
        if _k == 'TypeError' and 'NoneType' in _s:
            _say = ("A function it uses hands back `None`, Python's word for nothing came back: give that function a "
                    '`return`.')
        elif _k == 'TypeError' and 'can only concatenate' in _s:
            _say = 'Glue a number to text with `str()`, or put it in an f-string. `+` glues text only to text.'
        elif _k == 'TypeError' and 'does not support item assignment' in _s:
            _say = "Text can't change one letter at a time. Build a new text instead, like `\"L\" + word[1:]`."
        elif _k == 'TypeError' and 'positional argument' in _s:
            _fn = _re.match(r'(\w+)\(\)', _s)
            _say = ('Count the values a call hands to `' + (_fn.group(1) if _fn else _name) + '`, against its `def` '
                    'line: this call hands over the wrong number.')
        elif _k == 'AttributeError' and 'builtin_function_or_method' in _s:
            _say = ('Add `()` after the method name. Without them, Python has the method itself, not the new text.')
        elif _k == 'AttributeError' and "'list' object has no attribute 'join'" in _s:
            _say = 'Ask the glue to join: `", ".join(words)`. A list has no `.join`.'
        elif _k == 'AttributeError' and "'list' object" in _s:
            _say = '`.split()` hands back a list. Text methods work on text, not on a list.'
        elif _k == 'AttributeError' and "'NoneType'" in _s:
            _say = ("A function it uses hands back `None`, Python's word for nothing came back: give that function a "
                    '`return`.')
        elif _k == 'AttributeError' and "'str' object" in _s and _attr:
            _say = 'Text has no method `.' + _attr.group(1) + '`. Check the name after the dot, letter for letter.'
        elif _k == 'IndexError':
            _say = 'A place past the end stops Python. Count the places from 0, up to one less than `len()`.'
        elif _k == 'RecursionError':
            _say = ('`' + _name + '` calls itself, again and again. Move any call to `' + _name + '` out of it: line '
                    'it up with `def`, below the function.')
        return _lead + _say + _ev(_what)
    if _k == 'UnboundLocalError' or 'local variable' in _s:
        return (_lead + 'Make `' + _x + '` first, then use it. Python runs a function from the top down, and `' + _x
                + '` was used before the line that makes it.' + _ev(_what))
    if _x in _foreign:
        return _lead + '`' + _x + "` comes from Mar'tu's example." + _pl + _ev(_what)
    if _x in ('lower', 'upper', 'title', 'capitalize', 'strip', 'split', 'join', 'replace', 'find'):
        return (_lead + '`' + _x + '` is a method: it goes after a dot, like `' + (_ps[0] if _ps else 'text') + '.'
                + _x + '()`.' + _ev(_what))
    _near = [_p for _p in _ps if _close(_x, _p)]
    if _near:
        return (_lead + 'You wrote `' + _x + '`, and the parameter is `' + _near[0] + '`. Python matches names letter '
                'for letter.' + _ev(_what))
    _near = [_v for _v in _made if _close(_x, _v)]
    if _near:
        return (_lead + 'You wrote `' + _x + '`, and the variable is `' + _near[0] + '`. Python matches names letter '
                'for letter.' + _ev(_what))
    _near = [_z for _z in _foreign if _close(_x, _z)]
    if _near:
        return _lead + '`' + _x + '` looks like `' + _near[0] + "` from Mar'tu's example." + _pl + _ev(_what)
    return _lead + 'Nothing inside `' + _name + '` makes `' + _x + '`.' + _pl + _ev(_what)


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


def _calls_in(_nodes, _name):
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
            and type(_c.func).__name__ == 'Name' and _c.func.id == _name]


def _meth(_nodes, _attr):
    # Every `x.attr(...)` call inside the nodes.
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
            and type(_c.func).__name__ == 'Attribute' and _c.func.attr == _attr]


def _bare(_nodes, _attrs):
    # A method call on a line of its own, like `line.lower()`: the new value is made and thrown away.
    return [_s for _n in _nodes if _n is not None for _s in _ast.walk(_n) if type(_s).__name__ == 'Expr'
            and type(_s.value).__name__ == 'Call' and type(_s.value.func).__name__ == 'Attribute'
            and _s.value.func.attr in _attrs]


def _inside(_node, _kind):
    # Every node of a kind (a name like 'Return') inside the loops of a function.
    return [_x for _l in _ast.walk(_node) if type(_l).__name__ == 'For' for _x in _ast.walk(_l)
            if type(_x).__name__ == _kind and _x is not _l]


def _first(_name):
    # The first top-level `name = ...` line: the line Mar'tu's check gives another value in a rerun.
    for _n in _tree.body:
        if (type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id == _name):
            return _n
    return None


def _first_text(_name):
    _n = _first(_name)
    if _n is not None and type(_n.value).__name__ == 'Constant' and type(_n.value.value).__name__ == 'str':
        return _n.value.value
    return None


def _rerun(_values):
    # The program again in a fresh namespace, the first top-level `name = ...` of each name given another value,
    # prints kept private. Returns (namespace, printed lines, error or None, names whose line was not found).
    _t = _ast.parse(_source)
    _left = _B.list(_values)
    for _n in _t.body:
        if (type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id in _left):
            _n.value = _ast.copy_location(_ast.Constant(_values[_n.targets[0].id]), _n.value)
            _left.remove(_n.targets[0].id)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__'}
    _keep_out = _sys.stdout
    _buf = _io.StringIO()
    _e = None
    _sys.stdout = _buf
    try:
        _B.exec(_B.compile(_t, 'main.py', 'exec'), _ns)
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    return _ns, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _e, _left


def _nums(_l):
    # The whole numbers on a printed line: `7 gaps, 311 hours.` gives [7, 311].
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?!\d)', _l)]


def _fprints():
    # Every print(...) that shows an f-string, right inside it or from a variable made with one.
    _made = _B.set(_t.id for _n in _ast.walk(_tree) if type(_n).__name__ == 'Assign'
                   and type(_n.value).__name__ == 'JoinedStr' for _t in _n.targets if type(_t).__name__ == 'Name')
    return [_c for _c in _calls_in([_tree], 'print') if [_a for _a in _c.args if type(_a).__name__ == 'JoinedStr'
            or (type(_a).__name__ == 'Name' and _a.id in _made)]]


def _ftexts(_ns):
    # What each print of an f-string shows, worked out again from the values in `_ns` (its prints kept private),
    # so a check can ask whether the f-string itself holds a value, not some other line.
    _out = []
    for _c in _fprints():
        _parts = []
        for _a in _c.args:
            _v, _rows, _e = _call(lambda: _B.eval(_B.compile(_ast.Expression(_a), 'main.py', 'eval'), _ns))
            if _e is None:
                _parts.append(_B.str(_v))
        _out.append(' '.join(_parts))
    return _out


def _ref_shift(_c, _k):
    _p = _ABC.find(_c)
    return _c if _p < 0 else _ABC[(_p + _k) % 26]


def _ref_encode(_m, _k):
    return ''.join([_ref_shift(_c, _k) for _c in _m])
'''


def _px_parts():
    """_PX split into its setup lines and its helper functions, each with the helper names it uses."""
    import ast

    tree = ast.parse(_PX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_PX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_PX_HEAD, _PX_DEFS = _px_parts()


def check(label, body, **values):
    """(label, code): the _PX setup lines, the helpers this check uses (and the helpers those use), then the body."""
    import re

    code = fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _PX_DEFS and name not in need:
            need.add(name)
            todo |= _PX_DEFS[name][1]
    head = "\n".join(_PX_HEAD).replace("__QUOTES__", repr(QUOTES_RULE))
    helpers = [text for name, (text, _) in _PX_DEFS.items() if name in need]
    return (label, head + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + code.strip("\n") + "\n")


def code_lines(code):
    """The lines of a solution for Assemble it: no comment lines, no blank lines, inline comments dropped."""
    out = []
    for line in code.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        out.append(line.split("  #")[0].rstrip())
    return out


# =============================================================================================
# UNIT (repeated in every part file of strings; copied verbatim from u09a, so the parts agree)
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

# Only the terms this part is first to link. Every other [[link]] here (string, index, slice, len(), in, for loop,
# return, int(), str(), remainder, list, append, TypeError, IndexError, ValueError, AttributeError, .lower(),
# continue, sum()) is defined in an earlier unit.
GLOSSARY = [
    dict(
        term="cipher",
        aliases=["ciphers", "ley shift", "secret code"],
        plain=(
            "A way to hide a message. In a shift cipher, every letter moves along the alphabet by the same number, "
            "the key. Whoever knows the key can move the letters back."
        ),
        example='"abc" shifted by 1 is "bcd"',
    ),
]


# =============================================================================================
# Extra practice 9X "Letter by Letter" (pool: 8A-04, 8A-05, 8A-08)
# =============================================================================================

# ---- 8A-04 is-it-in-there: does the report say red? `in` on text, then any capitals with .lower(). PAR, RET.

WARN_CALLS = (
    "\n\n"
    "# Should show True, False, True.\n"
    'print(clock_warning("red at dusk"))\n'
    'print(clock_warning("all calm"))\n'
    'print(clock_warning("It went RED."))\n'
)


def _warn(body="    return False\n", calls=WARN_CALLS, extra=""):
    return "def clock_warning(report):\n" + body + calls + extra


WARN_STARTER = _warn()
WARN_PLAIN = '    return "red" in report\n'
WARN_LOWER = '    return "red" in report.lower()\n'
WARN_SOLUTION = _warn(WARN_LOWER)
# The Example's own names: a NameError on one of them is explained by _why().
WARN_FOREIGN = ("says_glug", "note")
GLUG_EXAMPLE = (
    "def says_glug(note):\n"
    '    return "glug" in note\n'
    "\n\n"
    'print(says_glug("more glug, yes?"))\n'
    'print(says_glug("Shield up."))\n'
)

# Shared by both checkpoints: what the function's comparisons look like (for the messages only).
_WARN_SHAPE = r'''
_f = _need('clock_warning', ['report'])
_d = _defs().get('clock_warning')
_cmp = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Compare']
_sides = [_x for _c in _cmp for _x in [_c.left] + _B.list(_c.comparators)]
_texts = [_x.value for _x in _sides if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str']
_ops = [type(_o).__name__ for _c in _cmp for _o in _c.ops]
_swapped = [_c for _c in _cmp if type(_c.left).__name__ != 'Constant'
            and [_x for _x in _c.comparators if type(_x).__name__ == 'Constant']]
_bare_or = [_v for _b in _ast.walk(_d) if type(_b).__name__ == 'BoolOp' for _v in _b.values
            if type(_v).__name__ == 'Constant' and type(_v.value).__name__ == 'str']
_or_msg = ('Write the whole question on each side of `or`: `"red" in report`. A text on its own, like '
           + ('`"' + _bare_or[0].value + '"`' if _bare_or and _bare_or[0].value.lower() == 'red' else 'that one')
           + ', is not a question, and Python hands the text back.')
_low_typed = [_c for _c in _meth([_d], 'lower') if type(_c.func.value).__name__ == 'Constant']


def _warn_crash(_e, _what):
    _m = _B.str(_e)
    if 'not iterable' in _m and 'method' in _m:
        return ('Add `()` after `lower`: `report.lower()`. Without them, Python has the method itself, not the '
                'lower-case copy.' + _ev(_what, 'Python stopped: ' + _err(_e)))
    if type(_e).__name__ == 'NameError' and "'lower'" in _m:
        return ('Write `.lower()` after the text, with a dot: `report.lower()`. Python has no `lower()` on its own.'
                + _ev(_what, 'Python stopped: ' + _err(_e)))
    return _why('clock_warning', _e, _what, __FOREIGN__)


def _warn_typed(_cases):
    # The check's own reports typed inside the function (learned from a message): answers, not a question.
    _r = [_c[0] for _c in _cases]
    return [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Constant' and type(_n.value).__name__ == 'str'
            and [_t for _t in _r if _t in _n.value]]


_HARD = ('Ask about `report` itself, with `in`: `return "red" in report`. Answers typed by hand can\'t follow a '
         'new report.')
'''

_WARN_RED = _WARN_SHAPE + r'''
# The False report holds r, e, d, "re" and "ed", but never "red": only the whole word passes.
_cases = (('a red flash at dusk', True), ('green reeds, calm night', False))
_got = []
for _text, _want in _cases:
    _what = 'called `clock_warning("' + _text + '")`'
    _val, _rows, _e = _call(_f, (_text,))
    assert _e is None, _warn_crash(_e, _what)
    _got.append((_what, _want, _val, _rows))
_bad = [_x for _x in _got if _x[2] is not _x[1]]
if _bad:
    _what, _want, _val, _rows = _bad[0]
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want))
    assert 'report' not in _texts, ('Take the quotes off `report`. `"report"` is just those six letters, and red '
                                    'is never in them. ' + _QUOTES)
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the answer goes back to the caller.'
                                          + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, 'Hand the answer back with `return`: `return "red" in report`.' + _x
    assert not _bare_or, _or_msg + _x
    assert type(_val).__name__ != 'str', ('Hand back `True` or `False` with no quotes: the answer to `"red" in '
                                          'report`. In quotes, it is only text.')
    assert not (_meth([_d], 'find') and type(_val).__name__ == 'int'), (
        'Ask with `in`: `"red" in report` answers `True` or `False`. `.find()` hands back a place instead, or '
        '-1 when the text is not there.' + _x)
    assert 'Eq' not in _ops, ('Ask with `in`, not `==`. `==` asks if the whole report is just `"red"`. `in` asks if '
                              'red is somewhere inside it.' + _x)
    assert not _swapped, ('Turn it round: the short text goes first, `"red" in report`. `report in "red"` asks if the '
                          'whole report fits inside the word red.' + _x)
    assert not [_t for _t in _texts if _t != _t.lower()], (
        'Look for `"red"` in small letters. `report.lower()` is a lower-case copy, so capitals are never in it.' + _x)
    assert not _meth([_d], 'upper'), ('Use `.lower()`, not `.upper()`. `.upper()` makes the copy all capitals, and '
                                      '`"red"` in small letters is never in it.' + _x)
    assert not [_t for _t in _texts if _t.lower() != 'red'], (
        'Look for `"red"`. Your function looks for other letters.' + _x)
    assert _cmp, ('`clock_warning` still hands back the same answer for every report. Replace `return False` with '
                  'the question: is `"red"` in `report`?' + _x)
    if _B.len(_B.set([_B.repr(_y[2]) for _y in _got])) == 1:
        assert False, ('Ask about `report` itself, so the answer follows each report: `return "red" in report`.'
                       + _ev('called `clock_warning` with a report that says red and one that does not',
                             'both gave back ' + _said(_val)))
    assert False, 'Hand back the answer to `"red" in report`.' + _x
assert not _warn_typed(_cases), _HARD
'''

_WARN_CAPS = _WARN_SHAPE + r'''
# A caps-lock report (`rED`) beats a list of typed spellings; the False report holds r, e, d, but never red.
_cases = (('RED SKY. BRACE.', True), ('It went Red twice.', True), ('cAPS LOCK. iT WENT rED.', True),
          ('GREEN REEDS. CALM.', False))
for _text, _want in _cases:
    _what = 'called `clock_warning("' + _text + '")`'
    _val, _rows, _e = _call(_f, (_text,))
    assert _e is None, _warn_crash(_e, _what)
    if _val is _want:
        continue
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want))
    assert not _bare_or, _or_msg + _x
    assert not _low_typed, ('Put `.lower()` on `report`, the text that may have capitals: `"red" in report.lower()`. '
                            '`"red"` is small letters already.' + _x)
    assert not _bare([_d], ('lower',)), (
        'Keep the lower-case copy: `report = report.lower()`, or ask `"red" in report.lower()`. On its own line, '
        '`report.lower()` makes the copy and throws it away, so `report` kept its capitals.' + _x)
    assert not _meth([_d], 'upper'), ('Use `.lower()`, not `.upper()`. `.upper()` makes the copy all capitals, and '
                                      '`"red"` in small letters is never in it.' + _x)
    _copies = [_t.id for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and _meth([_n.value], 'lower')
               for _t in _n.targets if type(_t).__name__ == 'Name' and _t.id != 'report']
    assert not _copies, ('Ask the lower-case copy: `"red" in ' + (_copies or [''])[0] + '`. Your function made the '
                         'copy, then asked `report`, which still has its capitals.' + _x)
    _caps = [_t for _t in _texts if _t != _t.lower()]
    assert not (_caps and not _meth([_d], 'lower')), (
        'Let `.lower()` handle the capitals: `"red" in report.lower()`. Typing each spelling, like `"'
        + (_caps[0] if _caps[0].lower() == 'red' else 'Red') + '"`, misses mixes like `rED`.' + _x)
    assert _meth([_d], 'lower'), ('Ask a lower-case copy: `"red" in report.lower()`. `in` matches letter for letter, '
                                  'and capitals count, so `"red" in "RED"` is `False`.' + _x)
    assert not [_t for _t in _texts if _t.lower() != 'red'], (
        'Look for `"red"`. Your function looks for other letters.' + _x)
    assert False, 'Hand back `"red" in report.lower()`, so any capitals work.' + _x
assert not _warn_typed(_cases), _HARD
'''

_BURST_COMING = r'''
_f = _need('burst_coming', ['report'])
for _text, _want in (('A YELLOW glow.', True), ('red again', True), ('blue, calm', False), ('Yellow, then RED', True),
                     ('green reeds, mellow glow', False)):
    _what = 'called `burst_coming("' + _text + '")`'
    _val, _rows, _e = _call(_f, (_text,))
    assert _e is None, _why('burst_coming', _e, _what, __FOREIGN__)
    assert _val is _want, ('Hand back whether `"yellow"` or `"red"` is in a lower-case copy of `report`.'
                           + _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want)))
'''

IS_IT_IN_THERE = dict(
    id="is-it-in-there",
    title="Is it in there?",
    martu=(
        "The Ley Clock goes yellow for a burst. Once, it went red. Nobody in this cabin forgets that night.\n"
        "Gearshift writes a report every hour. I want one question answered: does the report say red?\n"
        "[[in]] works on text too. `\"red\" in report` asks: are those letters somewhere inside `report`? Python "
        "answers `True` or `False`.\n"
        "But `in` matches letter for letter, and capitals count. To Python, `r` and `R` are different letters. "
        "So `\"red\" in \"RED\"` is `False`. Ask a lower-case copy instead: the [[method]] `report.lower()` "
        "hands one back, and the capitals stop mattering."
    ),
    example=GLUG_EXAMPLE,
    example_output="True\nFalse",
    names=["clock_warning", "report"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code='print("glow" in "a glow at dusk")\nprint("glow" in "GLOW AT DUSK")\n',
        choices=["True\nTrue", "True\nFalse", "False\nFalse", "False\nTrue"],
        answer=1,
        explain=(
            "`in` looks for those exact letters. The first text has `glow` in small letters, so `True`. The second "
            "has `GLOW` in capitals, and to Python `g` and `G` are different letters, so `False`."
        ),
    ),
    pair_talk="Pair talk: before checkpoint 2, tell your partner why `\"red\" in \"It went RED.\"` is `False`.",
    starter=WARN_STARTER,
    checkpoints=[
        dict(
            id="ask-with-in",
            text="Make `clock_warning` return whether `\"red\"` is in `report`.",
            dictated=False,
            hints=[
                "Look at the `return` line. It hands back `False` every time, whatever the report says.",
                "`in` asks if some letters are inside a text, and Python answers `True` or `False`. Put that "
                "question right after `return`.",
                "In the Example, `return \"glug\" in note` hands back whether `glug` is inside `note`.",
                "Write `return \"red\" in report` in place of `return False`.",
            ],
            checks=[check("clock_warning returns whether red is in the report", _WARN_RED, foreign=WARN_FOREIGN)],
            pass_line="Gearshift: Visor dims. Red at dusk: True. All calm: False.",
        ),
        dict(
            id="any-capitals",
            text="The last report shouts `RED`. Make `clock_warning` find red in any capitals, with `.lower()`.",
            dictated=False,
            hints=[
                "Look at the last print. `It went RED.` says red, but in capitals, so your function says `False`.",
                "`in` matches letter for letter: `\"red\" in \"RED\"` is `False`. A lower-case copy fixes that: "
                "`\"RED\".lower()` is `\"red\"`.",
                "A method hands you a new copy. Use the copy right where you ask: `\"glug\" in note.lower()`.",
                "Write `return \"red\" in report.lower()`.",
            ],
            checks=[check("clock_warning finds red in any capitals", _WARN_CAPS, foreign=WARN_FOREIGN)],
            pass_line="Mar'tu: RED, Red, red. The clock does not care how Gearshift spells it. Neither do we.",
        ),
    ],
    solution=WARN_SOLUTION,
    partials=[_warn(WARN_PLAIN)],
    assemble=dict(
        lines=code_lines(WARN_SOLUTION),
        distractors=['    return "red" == report.lower()', '    return "red" in lower(report)',
                     '    return "RED" in report.lower()'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Sliding a window",
            text=(
                "```text\nreport: i t   w e n t   r e d\nlook:               [r e d]\n```\n"
                "`in` slides `red` along the report, one letter at a time. If all three letters match somewhere, "
                "the answer is `True`."
            ),
        ),
        dict(
            angle="everyday",
            label="Searching a page",
            text=(
                "Searching a page for a word is like `in`. A strict search says `RED` and `red` are different. "
                "So you make everything small letters first, then search."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`\"red\" in report.lower()` with `report = \"It went RED.\"`:\n"
                "1. `report.lower()` makes a copy: `\"it went red.\"`.\n"
                "2. `in` looks for `red` in the copy, and finds it.\n"
                "3. The answer, `True`, goes back with `return`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, `dialogue_input.lower()` made Mar'tu's line all small letters. Same method here. "
                "It makes the copy before the question is asked."
            ),
        ),
    ],
    bonus=dict(
        by="oogrish",
        title="Yellow counts too",
        text=(
            "Steady, now. A yellow clock means a burst as well. Write `burst_coming(report)`: it returns whether "
            "`\"yellow\"` or `\"red\"` is in the report, in any capitals."
        ),
        hints=[
            "Make the lower-case copy once: `quiet = report.lower()`. Then ask two questions, joined with `or`.",
            "`return \"yellow\" in quiet or \"red\" in quiet`.",
        ],
        checks=[check("burst_coming finds yellow or red in any capitals", _BURST_COMING, foreign=WARN_FOREIGN)],
        solution=WARN_SOLUTION + (
            "\n\ndef burst_coming(report):\n"
            "    quiet = report.lower()\n"
            '    return "yellow" in quiet or "red" in quiet\n'
        ),
    ),
    campaign_link=dict(
        module=MODULE_2,
        part="red-clock",
        why=(
            "You were in the cabin when the clock flashed red. It usually goes yellow, and the red burst nearly tore "
            "the barrier apart. `clock_warning` is the watch Gearshift wishes he had kept."
        ),
    ),
    takeaway="`\"red\" in report` asks if those letters are inside; ask a `.lower()` copy so capitals don't matter.",
    wrong_answers=[
        dict(why="the starter: False for every report", code=WARN_STARTER, fails_at=1,
             message_contains="same answer for every report"),
        dict(why="print in place of return (RET)", code=_warn('    print("red" in report)\n'), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the parameter in quotes (\"red\" in \"report\")", code=_warn('    return "red" in "report"\n'),
             fails_at=1, message_contains="Take the quotes off `report`"),
        dict(why="a typed answer for the task's own reports (hard-coded)",
             code=_warn('    if report == "red at dusk":\n        return True\n    return False\n'), fails_at=1,
             message_contains="`==`"),
        dict(why="== in place of in (the whole report must be just red)", code=_warn('    return "red" == report\n'),
             fails_at=1, message_contains="not `==`"),
        dict(why="the two sides of in swapped", code=_warn('    return report in "red"\n'), fails_at=1,
             message_contains="Turn it round"),
        dict(why="True in quotes (text, not a yes/no answer)",
             code=_warn('    if "red" in report:\n        return "True"\n    return "False"\n'), fails_at=1,
             message_contains="no quotes"),
        dict(why=".find() used for a yes/no question (a place, or -1)",
             code=_warn('    return report.lower().find("red")\n'), fails_at=1, message_contains="`.find()`"),
        dict(why="looking for capitals in a lower-case copy", code=_warn('    return "RED" in report.lower()\n'),
             fails_at=1, message_contains="small letters"),
        dict(why="the Example's letters copied (glug)", code=_warn('    return "glug" in report\n'), fails_at=1,
             message_contains="other letters"),
        dict(why="a typo that only asks for part of the word (\"re\" passes the task's own reports)",
             code=_warn('    return "re" in report.lower()\n'), fails_at=1, message_contains="other letters"),
        dict(why="the answers for the check's own reports typed in (learned from the messages)",
             code=_warn('    if report == "a red flash at dusk" or report == "RED SKY. BRACE.":\n        return True\n'
                        '    if report == "It went Red twice." or report == "cAPS LOCK. iT WENT rED.":\n'
                        '        return True\n    return False\n'),
             fails_at=1, message_contains="typed by hand can't follow"),
        dict(why=".upper() in place of .lower()", code=_warn('    return "red" in report.upper()\n'), fails_at=1,
             message_contains="not `.upper()`"),
        dict(why="or with a bare text on one side (\"red\" or \"RED\" in report hands back \"red\")",
             code=_warn('    return "red" or "RED" in report\n'), fails_at=1,
             message_contains="whole question on each side of `or`"),
        dict(why=".lower() put on the typed text, not on report", code=_warn('    return "red".lower() in report\n'),
             fails_at=2, message_contains="Put `.lower()` on `report`"),
        dict(why="lower(report) as if it were a function (NameError)", code=_warn('    return "red" in lower(report)\n'),
             fails_at=0, message_contains="name 'lower' is not defined"),
        dict(why=".lower with no () (the method itself)", code=_warn('    return "red" in report.lower\n'),
             fails_at=0, message_contains="not iterable"),
        dict(why="the starter's calls taken out: lower(report) caught by the check itself",
             code=_warn('    return "red" in lower(report)\n', calls=""), fails_at=1,
             message_contains="no `lower()` on its own"),
        dict(why="the Example's parameter (note) used, the calls taken out: _why names where it came from",
             code=_warn('    return "red" in note.lower()\n', calls=""), fails_at=1,
             message_contains="Inside `clock_warning`, Python stopped: NameError: name 'note' is not defined. "
                              "`note` comes from Mar'tu's example. The parameter of `clock_warning` is `report`."),
        dict(why="a typo in the method's name (.lowr()), the calls taken out: _why says text has no such method",
             code=_warn('    return "red" in report.lowr()\n', calls=""), fails_at=1,
             message_contains="Inside `clock_warning`, Python stopped: AttributeError: 'str' object has no attribute "
                              "'lowr'. Text has no method `.lowr`. Check the name after the dot, letter for letter."),
        dict(why="case-sensitive in: capitals count (the spec's \"The clock is RED.\" -> True)",
             code=_warn(WARN_PLAIN), fails_at=2, message_contains="capitals count"),
        dict(why="each spelling typed by hand in place of .lower() (red, Red, RED: a mix like rED is missed)",
             code=_warn('    return "red" in report or "Red" in report or "RED" in report\n'), fails_at=2,
             message_contains="misses mixes"),
        dict(why="the lower-case copy made, then the original asked", code=_warn('    low = report.lower()\n'
             '    return "red" in report\n'), fails_at=2, message_contains="Ask the lower-case copy: `\"red\" in low`"),
        dict(why="report.lower() on its own line, then report used unchanged (the result not kept)",
             code=_warn('    report.lower()\n    return "red" in report\n'), fails_at=2,
             message_contains="throws it away"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="in-text,string-methods", solo="false", dictates="",
             foreign_names="says_glug,note,quiet", par="'a red flash at dusk','green reeds, calm night' / "
             "'RED SKY. BRACE.','It went Red twice.','cAPS LOCK. iT WENT rED.','GREEN REEDS. CALM.'") + "\n"
        "8A-04 (pool). Two checkpoints, so the capitals slip has a step of its own (the spec's one CP with \"The "
        "clock is RED.\" -> True is CP2). CP1 [ND] PAR/RET on two fresh lower-case reports (one True, one False, so "
        "any constant fails; booleans make lint b's collision unavoidable, and needing both answers is the point). "
        "Each False report holds r, e, d, `re` and `ed` (green reeds) but never `red`, so a part of the word fails. "
        "CP2 [ND] four fresh reports in capitals, one in caps-lock style (`rED`), so typed spellings (`\"Red\"`, "
        "`\"RED\"`) joined with `or` fail. Both CPs fail a function that types the check's own reports (copied "
        "from a message). Messages are picked from the function's own comparisons (quoted "
        "parameter, `==`, swapped sides, capitals, `.upper()`, other letters, `.find()`). `lower(report)` and "
        "`.lower` with no `()` crash the starter's own calls (Python's lines, the explainer's rows); with the calls "
        "taken out the check names them. The bare `report.lower()` passes CP1 and is named at CP2 (the class's "
        "'method result not kept' slip). Any other crash inside the function, during the check's own calls, gets "
        "_why() (as Units 3 and 7): 'Inside `clock_warning`, Python stopped: ...', then why (a name from the "
        "Example, `says_glug` or `note`; a near-miss parameter; a name used before it is made; a method name typed "
        "wrong, `.lowr()`: 'Text has no method'). Oogrish's side quest "
        "adds yellow with `or`."
    ),
)


# ---- 8A-05 letter-by-letter: count the full blocks of a bar with a loop. PAR, RET. --------------------------------

FULL_HEAD = "def count_full(bar):\n    blocks = 0\n"
FULL_TODO = "    # Loop over bar here.\n"
FULL_ALL = "    for letter in bar:\n        blocks = blocks + 1\n"
FULL_ONLY = '    for letter in bar:\n        if letter == "█":\n            blocks = blocks + 1\n'
FULL_RETURN = "    return blocks\n"
FULL_CALLS = '\n\nprint(count_full("███░░"))  # 3\n'


def _full(loop=FULL_TODO, head=FULL_HEAD, ret=FULL_RETURN, calls=FULL_CALLS, extra=""):
    return head + loop + ret + calls + extra


FULL_STARTER = _full()
FULL_SOLUTION = _full(FULL_ONLY)
# The Example's own names: a NameError on one of them is explained by _why().
FULL_FOREIGN = ("count_bangs", "shout", "mark", "bangs")
BANGS_EXAMPLE = (
    "def count_bangs(shout):\n"
    "    bangs = 0\n"
    "    for mark in shout:\n"
    '        if mark == "!":\n'
    "            bangs = bangs + 1\n"
    "    return bangs\n"
    "\n\n"
    'print(count_bangs("Up!! Now!"))\n'
)

# What the function's loop looks like (for the messages only).
_FULL_SHAPE = r'''
_f = _need('count_full', ['bar'])
_d = _defs().get('count_full')
_fors = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'For']
_ranged = [_t.id for _l in _fors if type(_l.iter).__name__ == 'Call' and type(_l.iter.func).__name__ == 'Name'
           and _l.iter.func.id == 'range' for _t in [_l.target] if type(_t).__name__ == 'Name']
_eqs = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Compare' and type(_c.ops[0]).__name__ == 'Eq']
_names_in = lambda _c: [_x.id for _x in [_c.left] + _B.list(_c.comparators) if type(_x).__name__ == 'Name']
_whole = [_c for _c in _eqs if 'bar' in _names_in(_c)]
_pos = [_c for _c in _eqs if [_x for _x in _names_in(_c) if _x in _ranged]]
_in_bar = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Compare' and type(_c.ops[0]).__name__ == 'In'
           and [_x for _x in _c.comparators if type(_x).__name__ == 'Name' and _x.id == 'bar']]
_not_eq = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Compare' and type(_c.ops[0]).__name__ == 'NotEq']
_marks = [_x.value for _c in _eqs for _x in [_c.left] + _B.list(_c.comparators) if type(_x).__name__ == 'Constant'
          and type(_x.value).__name__ == 'str' and _x.value not in ('█', '░')]
_wrong_mark = ('Compare with the full block itself, `"█"`: copy it from the bar, or use the symbol tray. Your `if` '
               'looks for another mark, which the bar never has.')
# Any loop counts: `for`, `while`, or a list comprehension. `.count()` inside one is not counting with it.
_loops = [_n for _n in _ast.walk(_d) if type(_n).__name__ in ('For', 'While', 'ListComp')]
_steps = [_t.id for _l in _ast.walk(_d) if type(_l).__name__ == 'For' for _t in [_l.target]
          if type(_t).__name__ == 'Name']
_counted = [_c for _c in _meth([_d], 'count') if not (type(_c.func.value).__name__ == 'Name'
                                                      and _c.func.value.id in _steps)]
_quoted_bar = [_l for _l in _ast.walk(_d) if type(_l).__name__ == 'For' and type(_l.iter).__name__ == 'Constant']
_plus_eq = [_a for _a in _inside(_d, 'Assign') if type(_a.value).__name__ == 'UnaryOp'
            and type(_a.value.op).__name__ == 'UAdd']
_set_one = [_a for _a in _inside(_d, 'Assign') if type(_a.value).__name__ == 'Constant' and _a.value.value == 1]
_adds = [_s for _l in _loops if type(_l).__name__ != 'ListComp' for _s in _ast.walk(_l)
         if (type(_s).__name__ == 'AugAssign' and type(_s.op).__name__ == 'Add')
         or (type(_s).__name__ == 'Assign' and type(_s.value).__name__ == 'BinOp'
             and type(_s.value.op).__name__ == 'Add'
             and [_t for _t in _s.targets if type(_t).__name__ == 'Name'
                  and _t.id in [_y.id for _y in _ast.walk(_s.value) if type(_y).__name__ == 'Name']])]


def _full_run(_bars):
    _out = []
    for _bar in _bars:
        _what = 'called `count_full("' + _bar + '")`'
        _val, _rows, _e = _call(_f, (_bar,))
        assert _e is None, _why('count_full', _e, _what, __FOREIGN__)
        _out.append((_bar, _what, _val, _rows))
    return _out
'''

_FULL_LOOP = _FULL_SHAPE + r'''
# Three bars of different lengths: counting every letter (6, 9, 5) or only the full ones (2, 5, 0) both pass here.
_res = _full_run(('██░░░░', '█░█░█░█░█', '░░░░░'))
_fine = [_r for _r in _res if type(_r[2]).__name__ == 'int' and _r[2] in (_B.len(_r[0]), _r[0].count('█'))]
if not _loops:
    assert _B.len(_fine) < 3, ('That number is right, and `.count()` can get it too. This exercise is about the loop: '
                               'walk `bar` with `for letter in bar:`, one letter each pass.')
    assert False, 'Loop over `bar` with `for letter in bar:`, and add 1 to `blocks` inside the loop.'
assert not _counted, ('Take `.count()` out, and let the loop do the counting: `blocks = blocks + 1`, indented under '
                      '`for letter in bar:`. This exercise is about the loop, one letter each pass.')
_bad = [_r for _r in _res if _r not in _fine]
if _bad:
    _bar, _what, _val, _rows = _bad[0]
    _want = _bar.count('█')
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', and the bar has ' + _B.str(_want) + ' full blocks')
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the count goes back to the caller.'
                                          + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, ('Keep `return blocks` at the bottom of `count_full`, lined up with `for`.'
                              + _ev(_what, 'it gave back `None`'))
    assert type(_val).__name__ == 'int', 'Hand back the count, a number: `return blocks`.' + _x
    assert not _inside(_d, 'Return'), ('Move `return blocks` out of the loop: line it up with `for`. Inside the '
                                       'loop, the function hands back after the first letter.' + _x)
    assert not _quoted_bar, ('Take the quotes off `bar`: `for letter in bar:`. In quotes, it is just those letters, '
                             'the same for every bar. ' + _QUOTES + _x)
    assert not _plus_eq, ('Write `blocks = blocks + 1`, or `blocks += 1`. `blocks =+ 1` means `blocks = +1`: it sets '
                          'the count to 1 on every pass.' + _x)
    assert not _set_one, ('Add 1 to what `blocks` already holds: `blocks = blocks + 1`. `blocks = 1` sets it back to 1 '
                          'on every pass.' + _x)
    assert not [_a for _a in _inside(_d, 'Assign') if type(_a.value).__name__ == 'Constant' and _a.value.value == 0], (
        'Set `blocks = 0` once, before the loop. Inside the loop, it goes back to 0 on every pass.' + _x)
    assert not [_s for _s in _ast.walk(_d) if type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'BinOp'], (
        'Keep the new count: `blocks = blocks + 1`. On its own line, `blocks + 1` works out a number and throws it '
        'away.' + _x)
    assert not _pos, ('`' + _ranged[0] + '` is a place, a number, so it is never `"█"`. Read the letter at that '
                      'place: `bar[' + _ranged[0] + ']`.' + _x)
    assert not _whole, ('Compare the loop variable, one letter, with `"█"`. `bar` is the whole bar, and the whole bar '
                        'is never just one block.' + _x)
    assert not _marks, _wrong_mark + _x
    assert [_r for _r in _res if _r[2] != _r[0].count('░')], (
        'Count the full blocks, `"█"`. Yours counted the empty ones, `"░"`.' + _x)
    if _B.len(_B.set([_B.repr(_r[2]) for _r in _res])) == 1:
        assert False, ('Count with the loop, so the number follows each bar. A number typed by hand stays the same.'
                       + _ev('called `count_full` with three different bars', 'all three gave back ' + _said(_val)))
    assert False, 'Add 1 to `blocks` inside the loop: `blocks = blocks + 1`, indented under `for`.' + _x
assert _adds or [_l for _l in _loops if type(_l).__name__ == 'ListComp'], (
    'Count with the loop: `blocks = blocks + 1`, indented under `for letter in bar:`, adds 1 on every pass. Yours '
    'sets the count some other way.')
'''

_FULL_COUNTS = _FULL_SHAPE + r'''
for _bar, _what, _val, _rows in _full_run(('█░░█░░█░░█', '░░░░', '████████████', 'Mana [██░] 2/3')):
    _want = _bar.count('█')
    if _val == _want:
        continue
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _B.str(_want))
    assert not (_val == _B.len(_bar) and _in_bar), (
        'Ask about this letter: `if letter == "█":`. `"█" in bar` asks about the whole bar, so every letter was '
        'counted.' + _x)
    assert _val != _B.len(_bar), ('Add 1 only when the letter is `█`: put `if letter == "█":` above '
                                  '`blocks = blocks + 1`, and indent that line under the `if`.' + _x)
    assert _val != _bar.count('░'), ('Count the full blocks, `"█"`. Yours counted the empty ones, `"░"`.' + _x)
    assert not _marks, _wrong_mark + _x
    assert not _not_eq, ('Ask `if letter == "█":`. `!=` counts every letter that is not `░`, so the other marks in '
                         'the text, like `M` and `[`, were counted too.' + _x)
    assert False, 'Add 1 to `blocks` only when the letter is `"█"`.' + _x
'''

_EMPTY_COUNTS = r'''
_f = _need('count_empty', ['bar'])
assert not _meth([_defs().get('count_empty')], 'count'), (
    'Count the `"░"` letters the same way, with a loop: `.count()` skips the walk.')
for _bar in ('█░░█░', '░░░░░░░', 'Mana [█████] 5/5'):
    _what = 'called `count_empty("' + _bar + '")`'
    _val, _rows, _e = _call(_f, (_bar,))
    assert _e is None, _why('count_empty', _e, _what, __FOREIGN__)
    assert _val == _bar.count('░'), ('Count the `"░"` letters the same way, and return the count.'
                                     + _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _B.str(_bar.count('░'))))
'''

LETTER_BY_LETTER = dict(
    id="letter-by-letter",
    title="Letter by letter",
    martu=(
        "Bars, yes? A mana bar is text: a `█` for each point of mana, a `░` for each point used.\n"
        "Text is letters in a row, so a [[for loop]] can walk it. `for letter in bar:` gives you one letter each "
        "pass, from the first to the last.\n"
        "Today we go the other way from the campaign. There, you made a bar from a number. Here, you read the "
        "number back out of the bar: count the `█` letters.\n"
        "My check hands your function bars it has never seen. So count with the loop. Never type a number you can "
        "see."
    ),
    example=BANGS_EXAMPLE,
    example_output="3",
    names=["count_full", "bar", "blocks", "letter"],
    predict=dict(
        q="Before you press Run: what will this loop print?",
        code='for letter in "Tor":\n    print(letter)\n',
        choices=["Tor", "T\no\nr", "T o r", "t\no\nr"],
        answer=1,
        explain=(
            "A `for` loop over text gives one letter each pass: `T`, then `o`, then `r`. Each `print` makes its "
            "own line."
        ),
    ),
    starter=FULL_STARTER,
    checkpoints=[
        dict(
            id="walk-the-bar",
            text="Loop over `bar` with `for`, and add 1 to `blocks` on every pass.",
            dictated=False,
            hints=[
                "Look at the comment inside `count_full`. Nothing walks the bar yet, so `blocks` stays 0.",
                "`for letter in bar:` gives one letter each pass. Indent the line under it to run it every pass.",
                "With other names: `for mark in shout:` then `bangs = bangs + 1`, indented, adds 1 for every mark.",
                "Write `for letter in bar:` in place of the comment, then `blocks = blocks + 1` indented under it.",
            ],
            checks=[check("count_full walks the bar and returns a count", _FULL_LOOP, foreign=FULL_FOREIGN)],
            pass_line="Gearshift: Visor dims. It counts. Every letter, for now.",
        ),
        dict(
            id="only-full-blocks",
            text="Now add 1 only when the letter is `█`. Use an `if` inside the loop.",
            dictated=False,
            hints=[
                "Look at what it printed: 5, not 3. It counts the `░` letters too. Copy `█` from the bar, or use "
                "the symbol tray.",
                "Ask about this one letter: `if letter == \"█\":`. Then move `blocks = blocks + 1` under the `if`, "
                "four more spaces in.",
                "In the Example, `if mark == \"!\":` lets only the `!` marks add to `bangs`.",
                "Write `if letter == \"█\":` inside the loop, with `blocks = blocks + 1` indented under it.",
            ],
            checks=[check("count_full counts only the full blocks, for any bar", _FULL_COUNTS, foreign=FULL_FOREIGN)],
            pass_line="Lucky: Three. I'd have said four. I'm generous.",
        ),
    ],
    solution=FULL_SOLUTION,
    partials=[_full(FULL_ALL)],
    assemble=dict(
        lines=code_lines(FULL_SOLUTION),
        distractors=['        if bar == "█":', "        blocks + 1", "        return blocks"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One letter each pass",
            text=(
                "```text\nbar:     █  █  █  ░  ░\npass:    1  2  3  4  5\nblock?   ✓  ✓  ✓  .  .\n"
                "blocks:  1  2  3  3  3\n```\n"
                "Five passes, one per letter. Only a `█` adds 1."
            ),
        ),
        dict(
            angle="everyday",
            label="Counting coins",
            text=(
                "Tip a purse out and slide the coins past one by one. Each time you see a gold one, say the next "
                "number. The loop is the sliding. The `if` is \"is this one gold?\"."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `blocks = 0` before the loop.\n"
                "2. `for letter in bar:` takes the next letter.\n"
                "3. `if letter == \"█\":` asks about it.\n"
                "4. If yes, `blocks = blocks + 1`.\n"
                "5. After the last letter, `return blocks`, lined up with `for`."
            ),
        ),
        dict(
            angle="shorter",
            text="Walk with `for`, ask with `if`, add with `blocks = blocks + 1`, hand back after the loop.",
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="The empty half",
        text="Running the math both ways. Write `count_empty(bar)`: it counts the `░` blocks the same way.",
        hints=[
            "Copy the shape of `count_full`, with its own name and its own count.",
            "Ask `if letter == \"░\":` inside the loop.",
        ],
        checks=[check("count_empty counts the empty blocks", _EMPTY_COUNTS, foreign=FULL_FOREIGN)],
        solution=FULL_SOLUTION + (
            "\n\ndef count_empty(bar):\n"
            "    used = 0\n"
            "    for letter in bar:\n"
            '        if letter == "░":\n'
            "            used = used + 1\n"
            "    return used\n"
        ),
    ),
    campaign_link=dict(
        module=MODULE_2,
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]',
        why=(
            "In the campaign you built a bar from a number with `*`. This time you go the other way: you read the "
            "number back out of the bar, one letter at a time."
        ),
    ),
    takeaway="`for letter in bar:` walks text one letter at a time; an `if` inside picks which letters count.",
    wrong_answers=[
        dict(why="the starter: no loop, blocks stays 0", code=FULL_STARTER, fails_at=1,
             message_contains="Loop over `bar`"),
        dict(why=".count() in place of the loop (right number, skips the exercise's point)",
             code=_full('    blocks = bar.count("█")\n'), fails_at=1, message_contains="about the loop"),
        dict(why="a loop added only to please the check, .count() still doing the counting",
             code=_full('    for letter in bar:\n        blocks = bar.count("█")\n'), fails_at=1,
             message_contains="Take `.count()` out"),
        dict(why="a loop that sets the count from len() instead of adding 1 each pass",
             code=_full("    for letter in bar:\n        blocks = len(bar)\n"), fails_at=1,
             message_contains="sets the count some other way"),
        dict(why="return inside the loop (hands back after the first letter)",
             code=_full("    for letter in bar:\n        blocks = blocks + 1\n        return blocks\n"), fails_at=1,
             message_contains="out of the loop"),
        dict(why="blocks = 0 inside the loop (reset every pass)",
             code=_full("    for letter in bar:\n        blocks = 0\n        blocks = blocks + 1\n"), fails_at=1,
             message_contains="once, before the loop"),
        dict(why="the loop walks the text \"bar\" in quotes (always 3 letters)",
             code=_full('    for letter in "bar":\n        blocks = blocks + 1\n'), fails_at=1,
             message_contains="Take the quotes off `bar`"),
        dict(why="=+ for += (sets the count to 1 on every pass)",
             code=_full("    for letter in bar:\n        blocks =+ 1\n"), fails_at=1, message_contains="`blocks =+ 1`"),
        dict(why="blocks = 1 inside the loop (set, not added)",
             code=_full("    for letter in bar:\n        blocks = 1\n"), fails_at=1, message_contains="sets it back to 1"),
        dict(why="blocks + 1 on its own line (the result not kept)",
             code=_full("    for letter in bar:\n        blocks + 1\n"), fails_at=1, message_contains="throws it away"),
        dict(why="print in place of return (RET)", code=_full(FULL_ONLY, ret="    print(blocks)\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="a typed count (the task's own 3)", code=_full("    for letter in bar:\n        blocks = 3\n"),
             fails_at=1, message_contains="typed by hand"),
        dict(why="the whole bar compared with one block",
             code=_full('    for letter in bar:\n        if bar == "█":\n            blocks = blocks + 1\n'),
             fails_at=1, message_contains="whole bar"),
        dict(why="a place compared with a block (range gives numbers)",
             code=_full('    for i in range(len(bar)):\n        if i == "█":\n            blocks = blocks + 1\n'),
             fails_at=1, message_contains="`bar[i]`"),
        dict(why="the Example's names copied (shout)", code=_full('    for mark in shout:\n        blocks = blocks + 1\n'),
             fails_at=0, message_contains="name 'shout' is not defined"),
        dict(why="every letter counted (checkpoint 1's loop, no if)", code=_full(FULL_ALL), fails_at=2,
             message_contains="only when the letter is"),
        dict(why="\"█\" in bar asked about the whole bar, so every letter counts",
             code=_full('    for letter in bar:\n        if "█" in bar:\n            blocks = blocks + 1\n'),
             fails_at=2, message_contains="whole bar"),
        dict(why="another block mark compared (▓, not █)", code=_full(FULL_ONLY.replace("█", "▓")), fails_at=1,
             message_contains="full block itself"),
        dict(why="!= ░ counts every other mark too (the campaign bar's letters and brackets)",
             code=_full(FULL_ONLY.replace('== "█"', '!= "░"')), fails_at=2, message_contains="`!=`"),
        dict(why="the empty blocks counted", code=_full(FULL_ONLY.replace("█", "░")), fails_at=1,
             message_contains="empty ones"),
        dict(why="blocks = 0 taken out, the calls too: _why says make it first (UnboundLocalError in the check)",
             code=_full(FULL_ALL, head="def count_full(bar):\n", calls=""), fails_at=1,
             message_contains="Inside `count_full`, Python stopped: UnboundLocalError: cannot access local variable "
                              "'blocks' where it is not associated with a value. Make `blocks` first, then use it."),
        dict(why="a near-miss parameter (bars), the calls taken out: _why names the parameter",
             code=_full(FULL_ONLY.replace("in bar:", "in bars:"), calls=""), fails_at=1,
             message_contains="You wrote `bars`, and the parameter is `bar`."),
        dict(why="the Example's loop variable (mark) used, the calls taken out: _why says where it came from",
             code=_full(FULL_ONLY.replace('if letter ==', 'if mark =='), calls=""), fails_at=1,
             message_contains="`mark` comes from Mar'tu's example. The parameter of `count_full` is `bar`."),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="loop-letters", solo="false", dictates="",
             foreign_names="count_bangs,shout,mark,bangs,used",
             par="CP1 '██░░░░','█░█░█░█░█','░░░░░' / CP2 '█░░█░░█░░█','░░░░','████████████','Mana [██░] 2/3'") + "\n"
        "8A-05 (pool). Two checkpoints: walk the bar and count every pass (CP1 accepts every letter or only the full "
        "ones, so the final solution stays green), then count only the full blocks (CP2). CP1 bars have lengths 6, 9 "
        "and 5 and full counts 2, 5 and 0, so a typed number or `len()` alone can't follow them, and none gives the "
        "task's own 3 (lint b). A loop is required (the spec's 'with a loop'): `.count(\"█\")` gets a kind 'this is "
        "about the loop' message. Messages from the loop's shape: `return` or `blocks = 0` inside the loop, a bare "
        "`blocks + 1`, `bar == \"█\"`, a `range` place compared with a block, `\"█\" in bar`, the `░` counted, "
        "`for letter in \"bar\"`, `blocks =+ 1` and `blocks = 1`. Any loop passes (`for`, `while`, or a list "
        "comprehension), but `.count()` on the bar does not, even beside a loop, and CP1 needs the count added up "
        "inside the loop (`blocks = len(bar)` in a loop fails). A crash inside the function during the check's own "
        "calls gets _why() (as Units 3 and 7): the Example's names, a near-miss parameter (`bars`), and `blocks` "
        "used before `blocks = 0` (UnboundLocalError: 'Make `blocks` first'). Gearshift's side quest: "
        "`count_empty`, also without `.count()`."
    ),
)


# ---- 8A-08 broken-spell-8a: an index past the end, a letter changed in place, len(26). Three loud bugs. ---------


def _tag(last="last = tag[5]", fix='tag[0] = "L"', blocks='print("Blocks: " + str(len(26)))', tag='tag = "Pucky"',
         extra=""):
    return (
        f"{tag}\n"
        f"{last}\n"
        'print("Last letter: " + last)\n'
        f"{fix}\n"
        "print(tag)\n"
        'bar = "█" * 26\n'
        f"{blocks}\n"
        + extra
    )


TAG_STARTER = _tag()
TAG_LAST = "last = tag[-1]"
TAG_FIX = 'tag = "L" + tag[1:]'
TAG_BLOCKS = 'print("Blocks: " + str(len(bar)))'
TAG_SOLUTION = _tag(TAG_LAST, TAG_FIX, TAG_BLOCKS)
TAG_RERUNS = ["Pucky the Third", "Rucky!"]

_TAG_RUNS = r'''
_own_tag = _first_text('tag')
assert _own_tag, 'Keep line 1, `tag = "Pucky"`, so Mar\'tu\'s check can try another tag there.'


def _tag_runs(_name):
    # The student's own run, then the program again with two other tags in line 1.
    _out = [(None, _own_tag, _g, _lines(), None)]
    for _other in __RERUNS__:
        _ns, _rows, _e, _left = _rerun({_name: _other})
        _out.append((_other, _other, _ns, _rows, _e))
    return _out


def _tried(_other):
    return '' if _other is None else " (Mar'tu's check tried `tag = \"" + _other + "\"`, only inside the check.)"
'''

_TAG_LAST = _TAG_RUNS + r'''
_line = _first('last')
for _other, _t, _ns, _rows, _e in _tag_runs('tag'):
    assert 'last' in _ns, 'Keep `last = ` on line 2, and mend what comes after the `=`.'
    _v = _ns.get('last')
    if _v == _t[-1]:
        continue
    _x = _tried(_other)
    assert not (_line is not None and type(_line.value).__name__ == 'Constant'), (
        'Read it from the tag: `tag[-1]`. A letter typed by hand cannot follow another tag.' + _x)
    _at = _line.value.slice if _line is not None and type(_line.value).__name__ == 'Subscript' else None
    if _at is not None and type(_at).__name__ == 'Slice':
        _at = _at.lower
    assert not (_at is not None and type(_at).__name__ == 'Constant' and type(_at.value).__name__ == 'int'
                and _at.value >= 0), ('Count from the end with `[-1]`, so it fits a tag of any length. A place '
                                      'counted from the start, like ' + _B.str(_at.value) + ', only fits a tag of one '
                                      'length.' + _x)
    assert False, 'Make `last` the last letter of the tag: `tag[-1]`.' + _x
'''

_TAG_NEW = _TAG_RUNS + r'''
_replaced = _meth([_tree], 'replace')
_own_new = _g.get('tag')
for _other, _t, _ns, _rows, _e in _tag_runs('tag'):
    _v = _ns.get('tag')
    _want = 'L' + _t[1:]
    if _v == _want:
        continue
    _x = _tried(_other)
    assert type(_v).__name__ == 'str', ('Keep `tag` as text: `tag = "L" + tag[1:]`. It holds ' + _said(_v) + '.' + _x)
    assert not (_replaced and _other is not None and _v == _t), (
        'Build it by place: `"L" + tag[1:]`. `.replace()` swaps a letter you typed, so it only works when the '
        'first letter is that one.' + _x)
    if _v == _t:
        _else = [_k for _k, _y in _B.list(_ns.items()) if not _k.startswith('_') and _y == _want]
        assert not _else, ('Put the new text back in `tag`: `tag = "L" + tag[1:]`. It went into another variable, '
                           'and `tag` kept the old one.' + _x)
        assert not _bare([_tree], ('replace',)), (
            'Put the new text in `tag`: `tag = "L" + tag[1:]`. A method like `.replace()` hands back a new text, '
            'and on its own line that new text is thrown away.' + _x)
        assert False, ('Build a new text and put it in `tag`: `tag = "L" + tag[1:]`. `tag` still holds the old one.'
                       + _x)
    assert _v != 'L' + _t[2:], ('Start the slice at 1: `tag[1:]`, everything after the first letter. `[2:]` starts '
                                'at the third letter, so one letter went missing.' + _x)
    assert _v != 'L' + _t, ('Leave the old first letter out: `"L" + tag[1:]`. `"L" + tag` keeps it too.' + _x)
    _back = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Slice' and type(_n.lower).__name__ == 'UnaryOp']
    assert not (_back and _other is not None), (
        'Start the slice at 1: `tag[1:]`, everything after the first letter. A slice counted from the end only fits '
        'a tag of one length.' + _x)
    _one = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Subscript' and type(_n.value).__name__ == 'Name'
            and _n.value.id == 'tag' and type(_n.slice).__name__ == 'Constant' and _n.slice.value == 1]
    assert not (_one and _v == 'L' + _t[1]), ('Add a colon: `tag[1:]` is everything from place 1 on. `tag[1]` is '
                                              'just one letter.' + _x)
    _ends = [_n.upper.value for _n in _ast.walk(_tree) if type(_n).__name__ == 'Slice'
             and type(_n.upper).__name__ == 'Constant']
    assert not (_ends and _v.startswith('L') and _want.startswith(_v)), (
        'Leave the end of the slice empty, `tag[1:]`, so it runs to the last letter. A typed end, like `'
        + _B.str(_ends[0]) + '`, only fits a tag of one length.' + _x)
    assert not (_other is not None and _v == _own_new), (
        'Build it from the tag: `"L" + tag[1:]`. A name typed by hand cannot follow another tag.' + _x)
    assert not (_v.startswith('L') and _want.startswith(_v)), (
        'Leave the end of the slice empty, `tag[1:]`, so it runs to the last letter.' + _x)
    assert False, 'Make `tag` an L, then everything after the first letter: `tag = "L" + tag[1:]`.' + _x
'''

_TAG_BLOCKS = r'''
_n = _first('bar')
assert _n is not None, 'Keep the line `bar = "█" * 26`, so Mar\'tu\'s check can try another bar there.'
_own_bar = _g.get('bar')
_own_rows = _lines()
_cases = [(None, _own_bar, _own_rows, None)]
for _k in (9, 14):
    _ns, _rows, _e, _left = _rerun({'bar': '█' * _k})
    _cases.append(('█' * _k, '█' * _k, _rows, _e))
for _other, _b, _rows, _e in _cases:
    _want = _B.len(_b) if type(_b).__name__ == 'str' else 26
    if [_l for _l in _rows if _want in _nums(_l)]:
        continue
    _x = '' if _other is None else " (Mar'tu's check tried a bar of " + _B.str(_want) + ' blocks, only inside the check.)'
    _all = [_k for _l in _rows for _k in _nums(_l)]
    assert not (3 in _all and [_c for _c in _calls_in([_tree], 'len') if _c.args
                               and type(_c.args[0]).__name__ == 'Constant' and _c.args[0].value == 'bar']), (
        'Take the quotes off `bar`: `len("bar")` counts the three letters b, a, r. ' + _QUOTES)
    assert not [_c for _c in _calls_in([_tree], 'len') if _c.args and type(_c.args[0]).__name__ == 'Name'
                and _c.args[0].id == 'tag'], 'Measure `bar`, the variable that holds the blocks: `len(bar)`.'
    assert _other is None or 26 not in _all, ('Measure the bar: `len(bar)`. A typed 26 cannot follow another bar.'
                                              + _x)
    assert False, 'Print how many blocks are in `bar`: `print("Blocks: " + str(len(bar)))`.' + _x
'''

BROKEN_SPELL_8A = dict(
    id="broken-spell-8a",
    title="Broken spell",
    martu=(
        "Gearshift printed Lucky a name tag. The press slipped, and it says `Pucky`. Lucky is not amused.\n"
        "Gearshift's spell to fix it has three loud bugs. Python stops each time and names a line. Read the last "
        "line of Python's message first. Mend that one, run again, and see what Python finds next.\n"
        "One rule to keep close: text can't change in place. You never swap one letter. You build a new text, "
        "and put it in the variable."
    ),
    names=["tag", "last", "bar", "len"],
    predict=dict(
        q="Run Gearshift's spell. What happens first?",
        choices=[
            "Last letter: y",
            "ERROR: IndexError: string index out of range",
            "ERROR: TypeError: 'str' object does not support item assignment",
            "Last letter: k",
        ],
        answer=1,
        explain=(
            "`Pucky` has 5 letters, at places 0 to 4. Line 2 asks for place 5, past the end, so Python stops "
            "there with an IndexError. It never reaches line 4."
        ),
    ),
    pair_talk=(
        "Pair talk: you may hunt these bugs together. One of you reads Python's last line out loud; the other points "
        "at the line it names. Each of you mends it on your own screen."
    ),
    starter=TAG_STARTER,
    checkpoints=[
        dict(
            id="mend-the-index",
            text="Mend line 2 so `last` holds the tag's last letter, for a tag of any length.",
            dictated=False,
            hints=[
                "Read Python's last line: `IndexError: string index out of range`. Then look at line 2.",
                "`Pucky` has 5 letters, at places 0 to 4. There is no place 5.",
                "Count from the end: `word[-1]` is the last letter of a word of any length.",
                "Write `last = tag[-1]` on line 2.",
            ],
            checks=[check("last is the tag's last letter, for any tag", _TAG_LAST, reruns=TAG_RERUNS)],
            pass_line="Mar'tu: One loud bug down. Python got further, yes?",
        ),
        dict(
            id="build-a-new-tag",
            text="Mend line 4 so `tag` spells `Lucky`. Build a new text from `\"L\"` and the rest of the tag.",
            dictated=False,
            hints=[
                "Read Python's last line: `'str' object does not support item assignment`. Then look at line 4.",
                "Text can't change in place: you can't swap one letter. You can build a new text and put it in "
                "`tag`.",
                "`\"C\" + word[1:]` is a new text: a C, then everything from place 1 on.",
                "Write `tag = \"L\" + tag[1:]` on line 4.",
            ],
            checks=[check("tag is a new text: L, then the rest of the tag", _TAG_NEW, reruns=TAG_RERUNS)],
            pass_line="Lucky: Lucky. With an L. Finally, some respect.",
        ),
        dict(
            id="measure-the-bar",
            text="Mend the last line so it shows how many blocks are in `bar`.",
            dictated=False,
            hints=[
                "Read Python's last line: `object of type 'int' has no len()`. Then look at the last line.",
                "`len()` measures text, or a list. A number like 26 has no length. Which variable holds the blocks?",
                "`len(\"glug\")` is 4: one for each letter.",
                "Write `print(\"Blocks: \" + str(len(bar)))` as the last line.",
            ],
            checks=[check("the last line measures bar", _TAG_BLOCKS)],
            pass_line="Mar'tu: Three bugs, three mends. You read the message first. Good habit, yes?",
        ),
    ],
    solution=TAG_SOLUTION,
    assemble=dict(
        lines=code_lines(TAG_SOLUTION),
        distractors=["last = tag[5]", 'tag[0] = "L"', 'print("Blocks: " + len(bar))'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Run. Python stops at line 2: place 5 is past the end.\n"
                "2. Mend it and run again. A new message is good news: Python got further.\n"
                "3. Line 4 can't swap a letter. Build a new text.\n"
                "4. The last line measures a number. Measure `bar`."
            ),
        ),
        dict(
            angle="picture",
            label="Letters on tiles",
            text=(
                "```text\n P  u  c  k  y\n 0  1  2  3  4\n-5 -4 -3 -2 -1\n```\n"
                "Five tiles, 0 to 4. `[-1]` is always the last tile. `tag[1:]` is every tile from 1 on: `ucky`."
            ),
        ),
        dict(
            angle="everyday",
            label="Carved in stone",
            text=(
                "Text is like a word carved in stone. You can't chip out one letter and fit a new one. You carve a "
                "new stone, `\"L\" + tag[1:]`, and put it where the old one stood."
            ),
        ),
        dict(
            angle="shorter",
            text="`[-1]` for the last letter. `\"L\" + tag[1:]` for a new first letter. `len(bar)`, not `len(26)`.",
        ),
    ],
    campaign_link=dict(
        module=MODULE_1,
        part="program-dialogue-prompt",
        snippet="dialogue_input = dialogue_input.lower()",
        why=(
            "The campaign never changed a letter in place either. It built a new text and put it back in the same "
            "variable. `tag = \"L\" + tag[1:]` is the same move."
        ),
    ),
    takeaway="Places run 0 to `len - 1`; `[-1]` is the last. Text can't change in place: build `\"L\" + tag[1:]`.",
    wrong_answers=[
        dict(why="the starter: place 5 is past the end (IndexError first)", code=TAG_STARTER, fails_at=0,
             message_contains="string index out of range"),
        dict(why="len(tag) used as the place (one past the end)", code=_tag("last = tag[len(tag)]"), fails_at=0,
             message_contains="string index out of range"),
        dict(why="line 2 mended, a letter still changed in place", code=_tag(TAG_LAST), fails_at=0,
             message_contains="does not support item assignment"),
        dict(why="lines 2 and 4 mended, len(26) left", code=_tag(TAG_LAST, TAG_FIX), fails_at=0,
             message_contains="has no len()"),
        dict(why="+ between text and a number, no str()", code=_tag(TAG_LAST, TAG_FIX, 'print("Blocks: " + len(bar))'),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="mended to [4]: fits five letters only (off by one for other tags)",
             code=_tag("last = tag[4]", TAG_FIX, TAG_BLOCKS), fails_at=1, message_contains="any length"),
        dict(why="the last letter typed by hand", code=_tag('last = "y"', TAG_FIX, TAG_BLOCKS), fails_at=1,
             message_contains="typed by hand"),
        dict(why="the new tag typed by hand", code=_tag(TAG_LAST, 'tag = "Lucky"', TAG_BLOCKS), fails_at=2,
             message_contains="typed by hand"),
        dict(why="the slice starts one too late ([2:])", code=_tag(TAG_LAST, 'tag = "L" + tag[2:]', TAG_BLOCKS),
             fails_at=2, message_contains="`[2:]`"),
        dict(why="the rest sliced from the end ([-4:]): fits five letters only",
             code=_tag(TAG_LAST, 'tag = "L" + tag[-4:]', TAG_BLOCKS), fails_at=2, message_contains="counted from the end"),
        dict(why="the last letter sliced from a typed start ([4:])", code=_tag("last = tag[4:]", TAG_FIX, TAG_BLOCKS),
             fails_at=1, message_contains="any length"),
        dict(why="the old first letter kept (\"L\" + tag)", code=_tag(TAG_LAST, 'tag = "L" + tag', TAG_BLOCKS),
             fails_at=2, message_contains="Leave the old first letter out"),
        dict(why="a slice that misses its end ([1:4])", code=_tag(TAG_LAST, 'tag = "L" + tag[1:4]', TAG_BLOCKS),
             fails_at=2, message_contains="end of the slice empty"),
        dict(why="an index where a slice belongs (tag[1] is one letter)",
             code=_tag(TAG_LAST, 'tag = "L" + tag[1]', TAG_BLOCKS), fails_at=2, message_contains="Add a colon"),
        dict(why="a typed slice end that fits five letters only ([1:5])",
             code=_tag(TAG_LAST, 'tag = "L" + tag[1:5]', TAG_BLOCKS), fails_at=2, message_contains="A typed end"),
        dict(why="the new text put in another variable (tag kept the old one)",
             code=_tag(TAG_LAST, 'new_tag = "L" + tag[1:]', TAG_BLOCKS), fails_at=2,
             message_contains="another variable"),
        dict(why="tag.replace() on its own line (the new text thrown away)",
             code=_tag(TAG_LAST, 'tag.replace("P", "L")', TAG_BLOCKS), fails_at=2, message_contains="thrown away"),
        dict(why=".replace(\"P\", \"L\") only fits a tag that starts with P",
             code=_tag(TAG_LAST, 'tag = tag.replace("P", "L")', TAG_BLOCKS), fails_at=2,
             message_contains="Build it by place"),
        dict(why="the block count typed by hand (26)", code=_tag(TAG_LAST, TAG_FIX, 'print("Blocks: " + str(26))'),
             fails_at=3, message_contains="typed 26"),
        dict(why="bar in quotes (len(\"bar\") is 3)", code=_tag(TAG_LAST, TAG_FIX, 'print("Blocks: " + str(len("bar")))'),
             fails_at=3, message_contains="Take the quotes off `bar`"),
        dict(why="the wrong variable measured (tag)", code=_tag(TAG_LAST, TAG_FIX, 'print("Blocks: " + str(len(tag)))'),
             fails_at=3, message_contains="Measure `bar`"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="string-index-slice,immutable-text,read-traceback", solo="false",
             dictates="", foreign_names="word,glug", reruns="tag='Pucky the Third','Rucky!'; bar of 9 and 14") + "\n"
        "8A-08 (pool). The spec's three bugs, one checkpoint each, in the order Python's messages arrive (verified, "
        "Python 3.13): `tag[5]` (IndexError: string index out of range), `tag[0] = \"L\"` (TypeError: 'str' object "
        "does not support item assignment), `len(26)` (TypeError: object of type 'int' has no len()). A crash fails "
        "every checkpoint, so each loud bug left fails at 0 and there are no partials (as u04a's broken spell). "
        "CP1 and CP2 rerun with two other tags in line 1, so a typed `\"y\"`, a mend to `[4]`, a typed "
        "`\"Lucky\"` and `.replace(\"P\", \"L\")` fail; `[2:]`, `\"L\" + tag`, `[1:4]`, a new variable and a bare "
        "`.replace()` each get a message. CP3 reruns with bars of 9 and 14 blocks (a typed 26 fails). "
        "`\"Blocks: \" + len(bar)` is Python's own concatenate error. Rung 0 is 'Read Python's last line'."
    ),
)

EXTRA_9X = dict(
    kind="lesson",
    id="extra-letter-by-letter",
    title="Extra practice: Letter by Letter",
    optional=True,
    minutes=12,
    summary="Ask if red is in the clock's report, count a bar's full blocks with a loop, and mend Lucky's name tag.",
    notes=(
        "9X pool (8A-04 is-it-in-there, 8A-05 letter-by-letter, 8A-08 broken-spell-8a); Quiz 8A follows as its own "
        "quiz item (6 more minutes, 18 in all, as the spec's row 4). Optional; feeds twins, the spaced queue and "
        "early finishers. 8A-level tools only: `in` on text, `.lower()`, loops over letters, indexes, slices, `len()`."
    ),
    exercises=[IS_IT_IN_THERE, LETTER_BY_LETTER, BROKEN_SPELL_8A],
)


# =============================================================================================
# Quiz 8A (pool, 6 questions)
# =============================================================================================

QUIZ_8A = dict(
    kind="quiz",
    id="rows-of-letters-quiz",
    title="Quiz: Rows of Letters",
    optional=True,
    minutes=6,
    summary="Six questions on places, slices, `len()`, `in`, and why text can't change in place.",
    notes=(
        "Quiz 8A (pool, 6 questions): 3 predict, 1 fill, 1 mc, 1 bug. The v1 samples, moved off the two that "
        "8b-remembers already asks (`\"Telegun\"[-1]`, `\"Greenroom\"[:5]`): a slice of the greenroom sign, the "
        "rest of the sign by a slice, the last letter for any length, `word[0] = ...`, case-sensitive `in`, and "
        "`len()` counting a space. Question 6 is the def/return item (2.4: every unit quiz has one from Unit 4 on)."
    ),
    questions=[
        dict(
            type="predict",
            id="slice-the-sign",
            q="The door in the greenroom has a small label. What will this print?",
            code='sign = "Greenroom, Interior"\nprint(sign[:9])\n',
            choices=["Greenroom", "Greenroom,", "Greenroo", "reenroom,"],
            answer="Greenroom",
            explain=(
                "`[:9]` starts at place 0 and stops *before* place 9, the comma. That is the 9 letters of "
                "`Greenroom`."
            ),
            notes="Distractors: the end included (the comma), one short, starting at 1.",
        ),
        dict(
            type="fill",
            id="the-rest-of-the-sign",
            q="Fill the blank so the program prints `Interior`.",
            code='sign = "Greenroom, Interior"\nprint(sign[___])\n',
            answer="11:",
            accept=["-8:", "11:19", "-8:19", "11:len(sign)", "-8:len(sign)"],
            expected_output="Interior",
            explain=(
                "`I` sits at place 11: count the comma and the space too. Leave the end empty and the slice runs "
                "to the end. `[-8:]` works as well: the last 8 letters."
            ),
        ),
        dict(
            type="mc",
            id="last-letter-any-length",
            q="Which one reads the last letter of `word`, for a word of any length?",
            choices=["word[len(word)]", "word[-1]", "word[1]", "word[0]"],
            answer=1,
            why_wrong={
                0: "Places stop at `len(word) - 1`, so `word[len(word)]` is one past the end: an IndexError.",
                2: "`word[1]` is the second letter. Places start at 0.",
                3: "`word[0]` is the first letter, not the last.",
            },
            explain="`[-1]` counts from the end, so it is the last letter of a word of any length.",
        ),
        dict(
            type="bug",
            id="build-a-new-word",
            q="This should print `Telegun`, with a capital T. Mend it.",
            code='word = "telegun"\nword[0] = "T"\nprint(word)\n',
            fix='word = "telegun"\nword = "T" + word[1:]\nprint(word)\n',
            expected_output="Telegun",
            explain=(
                "Text can't change in place, so `word[0] = \"T\"` stops with a TypeError. Build a new text, a T and "
                "then everything from place 1 on, and put it back in `word`."
            ),
        ),
        dict(
            type="predict",
            id="capitals-count",
            q="What will this print?",
            code='spell = "Glow"\nprint("glow" in spell)\nprint("glow" in spell.lower())\n',
            choices=["True\nTrue", "False\nTrue", "False\nFalse", "True\nFalse"],
            answer="False\nTrue",
            explain=(
                "`in` matches letter for letter, and `G` is not `g`, so the first line is `False`. The lower-case "
                "copy, `\"glow\"`, does hold it: `True`."
            ),
        ),
        dict(
            type="predict",
            id="a-space-is-a-letter",
            q="What will this print?",
            code='def size(name):\n    return len(name)\n\n\nprint(size("Bomb Shell"))\n',
            choices=["9", "10", "2", "BombShell"],
            answer="10",
            explain=(
                "`len()` counts every character, and the space is one: 4 + 1 + 5 = 10. The function hands that back, "
                "and `print` shows it."
            ),
            notes="The def/return item.",
        ),
    ],
)


# =============================================================================================
# Project 8P1 "The Water-Stained Log" (optional, recommended, 40 min)
# =============================================================================================

LOG_TEXT = " 48 hrs| 48 hrs |47 hrs|46hrs | 44 hrs|41 hrs | 37hrs "
LOG_LINE = 'log = "' + LOG_TEXT + '"'
# The other messy logs Mar'tu's check tries: other lengths, other spacing, numbers chosen so the count and the total
# never show up in the clean line (A: 4 gaps, 196 hours; B: 3 gaps, 86 hours; the real log: 7 gaps, 311 hours).
LOG_OTHERS = ["52hrs |50 hrs| 49 hrs |45hrs", " 30 hrs|29hrs | 27 hrs "]
LOG_SMUDGED = " 48 hrs|4?hrs | 47hrs |46 hrs"

LOG_SPLIT = 'marks = log.split("|")'
# The starter gives the project's first loop line once (teacher's revision); task 2 fills it in, in place of `pass`.
# Task 3's loop stays the student's own.
LOG_LOOP = "for mark in marks:\n    pass\n"
LOG_CLEAN = (
    "for mark in marks:\n"
    '    clean = mark.replace("hrs", "")\n'
    "    clean = clean.strip()\n"
    "    clean_marks.append(clean)\n"
)
LOG_HOURS = "for clean in clean_marks:\n    hours.append(int(clean))\n"
LOG_TOTAL = "total = sum(hours)"
LOG_SHRINKS = "for i in range(1, len(hours)):\n    shrinks.append(hours[i - 1] - hours[i])\n"
LOG_JOIN = 'clean_line = ", ".join(clean_marks)'
LOG_SUMMARY = 'print(f"{len(hours)} gaps, {total} hours in all.")\n'


def _wlog(split="marks = []", clean=LOG_LOOP, hours="", total="total = 0", shrinks="", join='clean_line = ""',
          summary="", log=LOG_LINE):
    """The project program with any of its parts filled in (defaults: the starter's placeholders)."""
    return (
        "# Lucky copied the chalk wall in\n"
        "# the rain. Mar'tu needs numbers.\n"
        f"{log}\n"
        "\n"
        '# 1. Split log at each "|".\n'
        f"{split}\n"
        "\n"
        "# 2. In the loop, clean each mark:\n"
        '#    take out "hrs" and the spaces.\n'
        "#    Append it to clean_marks.\n"
        "clean_marks = []\n"
        f"{clean}"
        "\n"
        "# 3. Turn each clean mark into a\n"
        "#    number. Append it to hours.\n"
        "hours = []\n"
        f"{hours}"
        "\n"
        "# 4a. Add up hours into total.\n"
        f"{total}\n"
        "print(total)\n"
        "\n"
        "# 4b. Append each shrink to\n"
        "#     shrinks: the gap before,\n"
        "#     minus this gap.\n"
        "shrinks = []\n"
        f"{shrinks}"
        "print(shrinks)\n"
        "\n"
        '# 5. Join clean_marks, with ", "\n'
        "#    between them.\n"
        f"{join}\n"
        "print(clean_line)\n"
        "\n"
        "# 6. Print a summary with an\n"
        "#    f-string: how many gaps, and\n"
        "#    the total.\n"
        f"{summary}"
    )


LOG_STARTER = _wlog()
LOG_PARTS = [("split", LOG_SPLIT), ("clean", LOG_CLEAN), ("hours", LOG_HOURS), ("total", LOG_TOTAL),
             ("shrinks", LOG_SHRINKS), ("join", LOG_JOIN), ("summary", LOG_SUMMARY)]


def _wlog_upto(k, **changes):
    """The solution's parts for checkpoints 1..k (checkpoint 4 is task 4a, the total; 5 is task 4b, the shrinks;
    6 the join; 7 the summary), with any part changed."""
    tasks = {1: ["split"], 2: ["clean"], 3: ["hours"], 4: ["total"], 5: ["shrinks"], 6: ["join"], 7: ["summary"]}
    parts = dict(LOG_PARTS)
    use = {name: parts[name] for t in range(1, k + 1) for name in tasks[t]}
    use.update(changes)
    return _wlog(**use)


LOG_SOLUTION = _wlog_upto(7)
LOG_SMUDGE_CLEAN = (
    "for mark in marks:\n"
    '    clean = mark.replace("hrs", "")\n'
    "    clean = clean.strip()\n"
    '    if "?" in clean:\n'
    "        continue\n"
    "    clean_marks.append(clean)\n"
)

# Shared by every task's check: the student's own run, then the program again with two other messy logs.
_LOG_RUNS = r'''
_own_log = _first_text('log')
assert _own_log is not None, ('Keep the line `log = "..."` from the starter, so Mar\'tu\'s check can try another '
                              'log there.')


def _want_of(_log):
    _m = _log.split('|')
    _c = [_x.replace('hrs', '').strip() for _x in _m]
    assert [_x for _x in _c if _x.isdigit()] == _c, (
        "Keep the log line as Lucky wrote it. Mar'tu's check tries its own smudged log for the side quest.")
    _h = [_B.int(_x) for _x in _c]
    return {'log': _log, 'marks': _m, 'clean_marks': _c, 'hours': _h, 'total': _B.sum(_h),
            'shrinks': [_h[_i - 1] - _h[_i] for _i in _B.range(1, _B.len(_h))], 'clean_line': ', '.join(_c)}


def _log_runs():
    _out = [(None, _g, _lines(), None, _want_of(_own_log))]
    for _other in __OTHERS__:
        _ns, _rows, _e, _left = _rerun({'log': _other})
        _out.append((_other, _ns, _rows, _e, _want_of(_other)))
    return _out


def _tried(_other, _e=None):
    if _other is None:
        return ''
    _t = " (Mar'tu's check tried `log = \"" + _other + "\"`, only inside the check"
    return _t + ('. Python stopped: ' + _err(_e) + '.)' if _e is not None else '.)')


def _typed_here(_other, _v, _name):
    # A rerun that kept the value of the student's own run: it was typed, not built from `log`.
    return _other is not None and _v == _g.get(_name)
'''

_LOG_MARKS = _LOG_RUNS + r'''
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('marks')
    if _v == _w['marks']:
        continue
    if (type(_v).__name__ == 'list' and [type(_y).__name__ for _y in _v] == ['str'] * _B.len(_v)
            and [_y.strip() for _y in _v] == [_y.strip() for _y in _w['marks']] and not _typed_here(_other, _v, 'marks')):
        continue
    _x = _tried(_other, _e)
    assert 'marks' in _ns, 'Keep `marks = ` under task 1, and put `log.split("|")` after the `=`.' + _x
    assert not (_v == [] and _bare([_tree], ('split',))), (
        'Keep what `.split()` hands back: `marks = log.split("|")`. On its own line, the list is made and thrown '
        'away, so `marks` stayed empty.')
    assert _v != [], "`marks` is still the starter's `[]`. Replace the `[]` with `log.split(\"|\")`." + _x
    assert not _typed_here(_other, _v, 'marks'), (
        'Let `.split()` cut the log: `marks = log.split("|")`. A list typed by hand cannot follow another log.' + _x)
    assert type(_v).__name__ == 'list', ('Make `marks` a list with `.split()`: `marks = log.split("|")`. It holds '
                                         + _said(_v) + '.' + _x)
    assert _v != _w['log'].split(), ('Split at the bar: `log.split("|")`. With nothing in the brackets, `.split()` '
                                     'cuts at the spaces.' + _x)
    assert _B.len(_v) != 1, ('Split at the bar, `"|"`: the bars keep the marks apart. `marks` holds just one item, '
                             'the whole log.' + _x)
    assert False, 'Make `marks` with `log.split("|")`.' + _x
'''

_LOG_CLEAN_CHECK = _LOG_RUNS + r'''
_loops = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'For']
# The starter's own loop, still holding only `pass`.
_idle = [_l for _l in _loops if [type(_b).__name__ for _b in _l.body] == ['Pass']]
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('clean_marks')
    _want = _w['clean_marks']
    if _v == _want:
        continue
    _x = _tried(_other, _e)
    assert 'clean_marks' in _ns, 'Keep `clean_marks = []` under task 2, and append each clean mark to it.' + _x
    assert type(_v).__name__ == 'list', (
        'Keep `clean_marks` a list: write `clean_marks.append(clean)` on its own line, with no `clean_marks = ` in '
        'front. It holds ' + _said(_v) + '.' + _x)
    if not _v:
        assert not _idle, ('Fill in the loop under task 2: in place of `pass`, make `clean` from `mark`, then '
                           '`clean_marks.append(clean)`. `pass` does nothing, so `clean_marks` stayed empty.' + _x)
        assert not _loops, 'Append each clean mark to `clean_marks`, inside the loop: `clean_marks.append(clean)`.' + _x
        assert False, 'Loop over the marks, `for mark in marks:`, and append each clean mark to `clean_marks`.' + _x
    assert not _typed_here(_other, _v, 'clean_marks'), (
        'Clean the marks in a loop, so it works for any log. A list typed by hand cannot follow another log.' + _x)
    assert not [_y for _y in _v if type(_y).__name__ == 'int'], (
        'Append the clean text, like `"48"`, to `clean_marks`. Task 3 makes the numbers, in `hours`.' + _x)
    assert _B.len(_v) == _B.len(_want), (
        'Append inside the loop, once for every mark: indent each line under `for mark in marks:`. `clean_marks` '
        'has ' + _B.str(_B.len(_v)) + (' item' if _B.len(_v) == 1 else ' items') + ', and the log has '
        + _B.str(_B.len(_want)) + ' marks.' + _x)
    _strs = [_y for _y in _v if type(_y).__name__ == 'str']
    if [_y for _y in _strs if 'hrs' in _y]:
        assert not _bare([_tree], ('replace',)), (
            'Keep what `.replace()` hands back: `clean = mark.replace("hrs", "")`. On its own line, the new text is '
            'thrown away, and the mark keeps its hrs.' + _x)
        assert False, 'Take `hrs` out of each mark with `.replace("hrs", "")`. Some clean marks still say hrs.' + _x
    if [_y for _y in _strs if _y != _y.strip()]:
        assert _v != [_m.strip().replace('hrs', '') for _m in _w['marks']], (
            'Replace first, then strip. Stripping first leaves the space that sat before hrs: `" 48 hrs"` becomes '
            '`"48 "`.' + _x)
        assert not _bare([_tree], ('strip',)), ('Keep what `.strip()` hands back: `clean = clean.strip()`. On its '
                                                'own line, the new text is thrown away.' + _x)
        assert False, ('Strip the spaces off each mark with `.strip()`, after the replace. Some clean marks still have '
                       'spaces at the ends.' + _x)
    assert False, 'Make each clean mark with `.replace("hrs", "")`, then `.strip()`, and append it.' + _x
'''

_LOG_HOURS_CHECK = _LOG_RUNS + r'''
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('hours')
    _want = _w['hours']
    if _v == _want and [type(_y).__name__ for _y in _v] == ['int'] * _B.len(_want):
        continue
    _x = _tried(_other, _e)
    assert 'hours' in _ns, 'Keep `hours = []` under task 3, and append each number to it.' + _x
    assert type(_v).__name__ == 'list', (
        'Keep `hours` a list: write `hours.append(int(clean))` on its own line, with no `hours = ` in front. It holds '
        + _said(_v) + '.' + _x)
    assert _v, ('Turn each clean mark into a number and append it to `hours`: loop over `clean_marks`, and append '
                '`int(clean)`.' + _x)
    assert not _typed_here(_other, _v, 'hours'), (
        'Build `hours` in a loop, so it works for any log. A list typed by hand cannot follow another log.' + _x)
    assert not [_y for _y in _v if type(_y).__name__ == 'str'], (
        'Wrap each clean mark in `int()` before you append it: `hours.append(int(clean))`. `hours` holds text, like '
        '`"48"`, and text does not add up.' + _x)
    assert _B.len(_v) == _B.len(_want), (
        'Append inside the loop, once for every clean mark. `hours` has ' + _B.str(_B.len(_v))
        + (' item' if _B.len(_v) == 1 else ' items') + ', and there are ' + _B.str(_B.len(_want)) + ' clean marks.'
        + _x)
    assert False, 'Append `int(clean)` to `hours` for every clean mark.' + _x
'''

_LOG_TOTAL_CHECK = _LOG_RUNS + r'''
_t0 = _first('total')
_set = [_n for _n in _ast.walk(_tree) if type(_n).__name__ in ('Assign', 'AugAssign')
        and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
             if type(_t).__name__ == 'Name' and _t.id == 'total']]
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('total')
    if _v == _w['total'] and type(_v).__name__ == 'int':
        continue
    _x = _tried(_other, _e)
    assert 'total' in _ns, 'Keep `total = ` under task 4a, and add up `hours` after the `=`.' + _x
    assert not (_v == 0 and _B.len(_set) == 1 and _t0 is not None and type(_t0.value).__name__ == 'Constant'), (
        "`total` still holds the starter's 0. Replace the 0 with `sum(hours)`." + _x)
    assert not _typed_here(_other, _v, 'total'), (
        'Add it up from the list: `total = sum(hours)`. A total typed by hand cannot follow another log.' + _x)
    assert _v != _B.len(_w['hours']), ('Add up the numbers with `sum(hours)`. `len()` counts how many there are.'
                                       + _x)
    assert False, ('Make `total` the sum of `hours`: `total = sum(hours)`. It holds ' + _said(_v) + ', not '
                   + _B.str(_w['total']) + '.' + _x)
'''

_LOG_SHRINKS_CHECK = _LOG_RUNS + r'''
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('shrinks')
    _want = _w['shrinks']
    if _v == _want:
        continue
    _x = _tried(_other, _e)
    assert 'shrinks' in _ns, 'Keep `shrinks = []` under task 4b, and append each shrink to it.' + _x
    assert type(_v).__name__ == 'list', (
        'Keep `shrinks` a list: write `shrinks.append(...)` on its own line, with no `shrinks = ` in front.' + _x)
    assert _v, ('Under `shrinks = []`, loop over the places from 1: `for i in range(1, len(hours)):`. Then append '
                'each shrink, `hours[i - 1] - hours[i]`.' + _x)
    assert not _typed_here(_other, _v, 'shrinks'), (
        'Work each shrink out from `hours`, so it works for any log. A list typed by hand cannot follow another log.'
        + _x)
    assert _v != [-_y for _y in _want], ('Take this gap away from the gap before: `hours[i - 1] - hours[i]`. Your '
                                         'shrinks came out below 0.' + _x)
    assert _B.len(_v) != _B.len(_w['hours']), (
        'Start the loop at 1: `range(1, len(hours))`. The first gap has no gap before it, so `hours[i - 1]` read the '
        'last gap.' + _x)
    assert False, 'Append `hours[i - 1] - hours[i]` for each place `i` from 1.' + _x
'''

_LOG_JOIN_CHECK = _LOG_RUNS + r'''
for _other, _ns, _rows, _e, _w in _log_runs():
    _v = _ns.get('clean_line')
    _want = _w['clean_line']
    if _v == _want and [_l for _l in _rows if _want in _l]:
        continue
    _x = _tried(_other, _e)
    assert 'clean_line' in _ns, 'Keep `clean_line = ` under task 5, and join `clean_marks` after the `=`.' + _x
    assert _v != _want, 'Keep `print(clean_line)` under task 5, so the clean line shows.' + _x
    assert not (_v == '' and _bare([_tree], ('join',))), (
        'Keep what `.join()` hands back: `clean_line = ", ".join(clean_marks)`. On its own line, the joined text is '
        'thrown away.')
    assert _v != '', "`clean_line` is still the starter's empty text. Replace the `\"\"` with `\", \".join(clean_marks)`." + _x
    assert type(_v).__name__ == 'str', ('Make `clean_line` text with `.join()`: `", ".join(clean_marks)`. It holds '
                                        + _said(_v) + '.' + _x)
    assert not _typed_here(_other, _v, 'clean_line'), (
        'Join it from the list: `", ".join(clean_marks)`. A line typed by hand cannot follow another log.' + _x)
    _c = _w['clean_marks']
    assert _v not in (' '.join(_c), ''.join(_c), ','.join(_c), ' ,'.join(_c)), (
        'Put a comma and a space between them: `", ".join(clean_marks)`. The text before `.join` goes between every '
        'two marks.' + _x)
    assert _v != ', '.join(_w['marks']), 'Join the clean marks, `clean_marks`, not `marks`.' + _x
    assert not (_v.endswith(', ') and _v[:-2] == _want), (
        'Let `.join()` place the commas: `", ".join(clean_marks)` puts `", "` only between two marks. Yours ends with '
        'one more, after the last mark.' + _x)
    assert False, 'Make `clean_line` with `", ".join(clean_marks)`.' + _x
'''

_LOG_SUMMARY_CHECK = _LOG_RUNS + r'''
_fp = _fprints()
_mine = _want_of(_own_log)
for _other, _ns, _rows, _e, _w in _log_runs():
    _n, _t = _B.len(_w['hours']), _w['total']
    _cands = [_l for _l in _rows if _l != _w['clean_line']]
    _hit = [_l for _l in _cands if _n in _nums(_l) and _t in _nums(_l)]
    _fhit = [_s for _s in _ftexts(_ns) if _n in _nums(_s) and _t in _nums(_s)]
    if _hit and _fhit:
        continue
    _x = _tried(_other, _e)
    if not _fp:
        assert not [_l for _l in _cands if '{' in _l and '}' in _l], (
            'Put an `f` right in front of the opening quote: `f"..."`. Without it, Python prints the braces and the '
            'names inside them, letter for letter.')
        assert not _hit, ('Write this line as an f-string: `print(f"{len(hours)} gaps, {total} hours in all.")`. Your '
                          '`+ str()` line works, and the campaign reads like that. This task asks for its f-string '
                          'twin.')
        assert not _uses('node:FString'), ('Print the summary: put the f-string right inside `print(...)`, or print '
                                           'the variable that holds it.')
        assert False, 'Print a summary with an f-string: `print(f"{len(hours)} gaps, {total} hours in all.")`.'
    assert not (_hit and not _fhit), (
        'Put both numbers in the f-string itself: `print(f"{len(hours)} gaps, {total} hours in all.")`. The line '
        'that shows them now is not that f-string.' + _x)
    _n0, _t0 = _B.len(_mine['hours']), _mine['total']
    assert not (_other is not None and [_l for _l in _cands if (_n0 != _n and _n0 in _nums(_l))
                                        or (_t0 != _t and _t0 in _nums(_l))]), (
        'Put the values in braces, `{len(hours)}` and `{total}`, so the summary follows any log. Numbers typed into '
        'the text cannot.' + _x)
    # Which value is missing is read from the f-string itself: `print(total)` shows the total on a line of its own.
    _ft = _ftexts(_ns)
    _has_t = [_s for _s in _ft if _t in _nums(_s)]
    _has_n = [_s for _s in _ft if _n in _nums(_s)]
    assert not (_has_t and not _has_n), 'Show how many gaps too: `{len(hours)}` inside the f-string.' + _x
    assert not (_has_n and not _has_t), 'Show the total too: `{total}` inside the f-string.' + _x
    assert False, ('Show how many gaps and the total in the same f-string, on one line: `{len(hours)}` and '
                   '`{total}`.' + _x)
'''

_LOG_SMUDGE_CHECK = r'''
_smudged = __SMUDGED__
_ns, _rows, _e, _left = _rerun({'log': _smudged})
assert not _left, 'Keep the line `log = "..."` from the starter, so Mar\'tu\'s check can try a smudged log there.'
_x = " (Mar'tu's check tried `log = \"" + _smudged + "\"`, only inside the check.)"
assert _e is None, ('Skip the smudged mark before `int()` meets it: `if "?" in clean:`, then `continue`, above the '
                    'append. With this log, Python stopped: ' + _err(_e) + '.' + _x)
assert _ns.get('hours') == [48, 47, 46], 'Leave the smudged mark out of `hours`, and keep every other mark.' + _x
'''


def _log_check(label, body):
    return check(label, body, others=LOG_OTHERS, smudged=LOG_SMUDGED)


PROJECT_8P1 = dict(
    kind="project",
    id="the-water-stained-log",
    title="The Water-Stained Log",
    optional=True,
    minutes=40,
    summary="Lucky copied the chalk wall in the rain. Split, clean and count his messy log until the numbers come out.",
    intro=(
        "Lucky copied the chalk wall onto paper, in the rain. He is very proud of it. This is what he handed Mar'tu:\n"
        "`\" 48 hrs| 48 hrs |47 hrs|46hrs | 44 hrs|41 hrs | 37hrs \"`\n"
        "The numbers are in there, under bars, spaces and `hrs`. Lucky: \"You're welcome.\"\n"
        "Six tasks, in order. Task 4 comes in two parts, 4a and 4b. The comments in the editor mark each one.\n"
        "Before this: Lesson 8B, Words That Change Shape (`.split()`, `.strip()`, `.replace()`, `.join()` and "
        "[[f-string|f-strings]]), and Biggest and smallest in More List Tools (`sum()`). A loop that adds works too."
    ),
    martu=(
        "Text in, numbers out. That is the whole job, yes?\n"
        "1. `.split(\"|\")` cuts the log at every bar, and hands back a [[list]] of marks.\n"
        "2. Each mark is still messy text. `.replace(\"hrs\", \"\")` takes out the hrs. `.strip()` takes the spaces "
        "off the ends. Each one hands back a new text, so keep it: `clean = ...`.\n"
        "3. `int(\"48\")` turns clean digits into the number 48. Text like `\"48 hrs\"` it refuses.\n"
        "My check tries other messy logs. So build everything from `log`, and never type a number you can see."
    ),
    names=["log", "marks", "clean_marks", "hours", "total", "shrinks", "clean_line"],
    pair_talk=(
        "Pair talk: before task 2, read the log together. Find a mark with a space before the number, and one with no "
        "space before `hrs`. Then each of you cleans them on your own screen."
    ),
    starter=LOG_STARTER,
    checkpoints=[
        dict(
            id="split-the-log",
            text="1. Make `marks` by splitting `log` at each `\"|\"`.",
            dictated=False,
            hints=[
                "Look at task 1. `marks = []` is a placeholder. The list should come from `log`.",
                "`.split()` cuts text wherever it finds what is in its brackets, and hands back a list. Here the "
                "marks are kept apart by `|`.",
                "With other names: `\"a,b,c\".split(\",\")` is `['a', 'b', 'c']`.",
                "Write `marks = log.split(\"|\")` in place of `marks = []`.",
            ],
            checks=[_log_check("marks is the log split at each bar", _LOG_MARKS)],
            pass_line="Lucky: Seven marks. See? You're welcome.",
        ),
        dict(
            id="clean-each-mark",
            text="2. In the loop, in place of `pass`, clean each mark: take out `hrs` and the spaces. Append each "
                 "clean mark to `clean_marks`.",
            dictated=False,
            hints=[
                "Look at task 2. The loop `for mark in marks:` is there, but `pass` does nothing, so `clean_marks` "
                "stays empty. Each mark still has `hrs` and spaces.",
                "In the loop, make `clean` from `mark` with `.replace(\"hrs\", \"\")`, then `.strip()` it. Each "
                "method hands back a new text, so catch it: `clean = ...`.",
                "With other names: `word = note.replace(\"!\", \"\")`, then `word = word.strip()`.",
                "Write `clean = mark.replace(\"hrs\", \"\")` in place of `pass`. Then `clean = clean.strip()` and "
                "`clean_marks.append(clean)` under it, each indented under the loop.",
            ],
            checks=[_log_check("clean_marks holds each mark, clean", _LOG_CLEAN_CHECK)],
            pass_line="Mar'tu: No hrs. No spaces. Lucky, look. This is what clean means.",
        ),
        dict(
            id="make-numbers",
            text="3. Turn each clean mark into a number, and append it to `hours`.",
            dictated=False,
            hints=[
                "Look at task 3. `hours` is still empty, and each clean mark is still text, like `\"48\"`.",
                "`int(\"48\")` is the number 48. Loop over `clean_marks`, and append `int(clean)` to `hours`.",
                "With other names: `nums.append(int(word))` adds the number inside `word`.",
                "Write `for clean in clean_marks:` under `hours = []`, then `hours.append(int(clean))` indented.",
            ],
            checks=[_log_check("hours holds each clean mark as a number", _LOG_HOURS_CHECK)],
            pass_line="Gearshift: Visor dims. Seven numbers. Now they can do math.",
        ),
        dict(
            id="add-the-total",
            text="4a. Make `total` the sum of `hours`.",
            dictated=False,
            hints=[
                "Look at task 4a. `total = 0` is a placeholder, so `print(total)` shows 0.",
                "`sum()` adds up a whole list of numbers. With other names: `rain = sum(days)` adds every number in "
                "`days`.",
                "Write `total = sum(hours)` in place of `total = 0`.",
            ],
            checks=[_log_check("total adds up the hours", _LOG_TOTAL_CHECK)],
            pass_line="Oogrish: Three hundred and eleven hours.",
        ),
        dict(
            id="find-the-shrinks",
            text="4b. Append each shrink to `shrinks`: the gap before, minus this gap.",
            dictated=False,
            hints=[
                "Look at task 4b. `shrinks` is still the empty list, so `print(shrinks)` shows `[]`.",
                "The first shrink is 48 minus 48, then 48 minus 47. A shrink compares neighbours: the gap before "
                "place `i` is at place `i - 1`, so start the loop at place 1.",
                "With other names: `for i in range(1, len(days)):`, then `drops.append(days[i - 1] - days[i])`.",
                "Write `for i in range(1, len(hours)):` under `shrinks = []`, above `print(shrinks)`. Under it, "
                "indented: `shrinks.append(hours[i - 1] - hours[i])`.",
            ],
            checks=[_log_check("shrinks holds each shrink", _LOG_SHRINKS_CHECK)],
            pass_line="Oogrish: The shrinks keep growing. Steady, now.",
        ),
        dict(
            id="join-a-clean-line",
            text="5. Make `clean_line` from `clean_marks`, with `\", \"` between them.",
            dictated=False,
            hints=[
                "Look at task 5. `clean_line = \"\"` is a placeholder, so the print shows nothing.",
                "`.join()` is called on the text that goes between the items. The list goes in the brackets.",
                "With other names: `\" + \".join(parts)` puts ` + ` between every two parts.",
                "Write `clean_line = \", \".join(clean_marks)` in place of `clean_line = \"\"`.",
            ],
            checks=[_log_check("clean_line joins the clean marks", _LOG_JOIN_CHECK)],
            pass_line="Bomb Shell: Clean line. Copied.",
        ),
        dict(
            id="f-string-summary",
            text="6. Print a summary with an f-string. Show how many gaps there are, and the total.",
            dictated=False,
            hints=[
                "Look at task 6. One `print` goes at the bottom, with an f-string inside it.",
                "An f-string has an `f` right before the quote. Inside it, `{...}` shows a value, like `{total}` or "
                "`{len(hours)}`.",
                "With other names: `print(f\"{len(days)} days, {rain} mm of rain.\")`.",
                "Write `print(f\"{len(hours)} gaps, {total} hours in all.\")` at the bottom.",
            ],
            checks=[_log_check("an f-string shows the count and the total", _LOG_SUMMARY_CHECK)],
            pass_line="Mar'tu: Text in, numbers out. Lucky, this is how a note should look.",
        ),
    ],
    solution=LOG_SOLUTION,
    partials=[_wlog_upto(k) for k in range(1, 7)],
    assemble=dict(
        lines=code_lines(LOG_SOLUTION),
        distractors=["marks = log.split()", 'clean_line = clean_marks.join(", ")', "    hours.append(clean)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One mark, step by step",
            text=(
                "```text\n\" 48 hrs\"  -> replace -> \" 48 \"\n\" 48 \"     -> strip   -> \"48\"\n"
                "\"48\"       -> int     -> 48\n```\n"
                "Every mark takes the same three steps. The loop does them for each one."
            ),
        ),
        dict(
            angle="everyday",
            label="Washing carrots",
            text=(
                "A muddy carrot: rinse off the mud, cut off the ends, then cook it. A mark: take out `hrs`, strip "
                "the ends, then `int()` it. Same order every time, one carrot at a time."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `.split(\"|\")`: one messy log becomes a list of messy marks.\n"
                "2. The loop: replace, then strip, then append the clean text.\n"
                "3. A loop: `int()` each clean mark, and append the number.\n"
                "4. `sum()` for the total, then a loop from place 1 for the shrinks.\n"
                "5. `\", \".join(...)` the clean text back into one line.\n"
                "6. An f-string with `{len(hours)}` and `{total}`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, `dialogue_input = dialogue_input.lower()` kept the new text in the same variable. "
                "`clean = clean.strip()` is the same move: a method hands back a new text, and you keep it."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="It was raining",
        text=(
            "My pen ran dry on one mark. It just says `4?`. Make your program skip any mark with a `?` in it, so a log "
            "like `\" 48 hrs|4?hrs | 47hrs |46 hrs\"` still works."
        ),
        hints=[
            "In the task 2 loop, after the strip: `if \"?\" in clean:`, then `continue` indented under it.",
            "`continue` skips the rest of this pass, so the smudged mark is never appended, and `int()` never sees it. "
            "(You met `continue` in Skip the empty, in Loops in One Line.)",
        ],
        checks=[check("a smudged mark is skipped", _LOG_SMUDGE_CHECK, smudged=LOG_SMUDGED)],
        solution=_wlog_upto(7, clean=LOG_SMUDGE_CLEAN),
    ),
    campaign_link=dict(
        module=MODULE_2,
        part="chalk-wall",
        why=(
            "You read this wall in the campaign: 48, 48, 47, 46, 44, 41, 37. Lucky's copy has the same numbers, "
            "buried in rain. Getting clean numbers out of messy text is half of real programming."
        ),
    ),
    takeaway="Messy text to numbers: `.split()`, then `.replace()` and `.strip()` (keep each new text), then `int()`.",
    wrong_answers=[
        dict(why="the starter: marks is still []", code=LOG_STARTER, fails_at=1, message_contains="starter's `[]`"),
        dict(why="log.split() on its own line (the list not kept)", code=_wlog(split='marks = []\nlog.split("|")'),
             fails_at=1, message_contains="thrown away"),
        dict(why="split() with empty brackets (cuts at spaces)", code=_wlog_upto(1, split="marks = log.split()"),
             fails_at=1, message_contains="cuts at the spaces"),
        dict(why="split at a comma (no commas in the log)", code=_wlog_upto(1, split='marks = log.split(",")'),
             fails_at=1, message_contains="just one item"),
        dict(why="split(log, \"|\") as if it were a function", code=_wlog_upto(1, split='marks = split(log, "|")'),
             fails_at=0, message_contains="name 'split' is not defined"),
        dict(why="the marks typed by hand",
             code=_wlog_upto(7, split='marks = [" 48 hrs", " 48 hrs ", "47 hrs", "46hrs ", " 44 hrs", "41 hrs ",'
                                     ' " 37hrs "]'),
             fails_at=1, message_contains="typed by hand"),
        dict(why=".split() hands back a list, then treated as text (marks.replace inside the loop)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = marks.replace("hrs", "")\n'
                                      "    clean_marks.append(clean)\n"), fails_at=0,
             message_contains="'list' object has no attribute 'replace'"),
        dict(why="mark.replace() on its own line (the new text not kept)",
             code=_wlog_upto(1, clean='for mark in marks:\n    mark.replace("hrs", "")\n    clean = mark.strip()\n'
                                      "    clean_marks.append(clean)\n"),
             fails_at=2, message_contains="Keep what `.replace()` hands back"),
        dict(why="no strip: the spaces stay (int() would not notice them)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = mark.replace("hrs", "")\n'
                                      "    clean_marks.append(clean)\n"),
             fails_at=2, message_contains="Strip the spaces"),
        dict(why="strip before replace (leaves the space before hrs)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = mark.strip().replace("hrs", "")\n'
                                      "    clean_marks.append(clean)\n"),
             fails_at=2, message_contains="Replace first, then strip"),
        dict(why="clean.strip() on its own line (the new text not kept)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = mark.replace("hrs", "")\n    clean.strip()\n'
                                      "    clean_marks.append(clean)\n"),
             fails_at=2, message_contains="Keep what `.strip()` hands back"),
        dict(why="numbers appended in task 2 (the join needs text)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = mark.replace("hrs", "").strip()\n'
                                      "    clean_marks.append(int(clean))\n"),
             fails_at=2, message_contains="Task 3 makes the numbers"),
        dict(why="the append outside the loop (only the last mark)",
             code=_wlog_upto(1, clean='for mark in marks:\n    clean = mark.replace("hrs", "").strip()\n'
                                      "clean_marks.append(clean)\n"),
             fails_at=2, message_contains="once for every mark"),
        dict(why="the starter's loop left as pass (clean_marks stays empty)", code=_wlog_upto(1), fails_at=2,
             message_contains="in place of `pass`"),
        dict(why="the lines written under the loop, not indented (pass left in): only the last mark",
             code=_wlog_upto(1, clean=LOG_LOOP + 'clean = mark.replace("hrs", "")\nclean = clean.strip()\n'
                                      "clean_marks.append(clean)\n"),
             fails_at=2, message_contains="has 1 item, and the log has 7 marks"),
        dict(why="the clean marks typed by hand",
             code=_wlog_upto(1, clean='clean_marks = ["48", "48", "47", "46", "44", "41", "37"]\n'), fails_at=2,
             message_contains="typed by hand"),
        dict(why="hours left as text (no int)", code=_wlog_upto(2, hours="for clean in clean_marks:\n"
                                                                         "    hours.append(clean)\n"),
             fails_at=3, message_contains="Wrap each clean mark in `int()`"),
        dict(why="int() on the raw mark (ValueError)", code=_wlog_upto(2, hours="for mark in marks:\n"
                                                                                "    hours.append(int(mark))\n"),
             fails_at=0, message_contains="invalid literal for int()"),
        dict(why="int() on the whole list", code=_wlog_upto(2, hours="hours = int(clean_marks)\n"), fails_at=0,
             message_contains="int() argument must be"),
        dict(why="the hours typed by hand", code=_wlog_upto(2, hours="hours = [48, 48, 47, 46, 44, 41, 37]\n"),
             fails_at=3, message_contains="typed by hand"),
        dict(why="total still the starter's 0", code=_wlog_upto(3, shrinks=LOG_SHRINKS), fails_at=4,
             message_contains="starter's 0"),
        dict(why="the total typed by hand", code=_wlog_upto(4, total="total = 311"), fails_at=4,
             message_contains="typed by hand"),
        dict(why="len() for sum()", code=_wlog_upto(4, total="total = len(hours)"), fails_at=4,
             message_contains="`len()` counts"),
        dict(why="the text added up (sum of clean_marks: TypeError)", code=_wlog_upto(4, total="total = sum(clean_marks)"),
             fails_at=0, message_contains="unsupported operand"),
        dict(why="4b left empty (shrinks still [])", code=_wlog_upto(4), fails_at=5,
             message_contains="Under `shrinks = []`, loop over the places from 1"),
        dict(why="shrinks the wrong way round", code=_wlog_upto(5, shrinks="for i in range(1, len(hours)):\n"
                                                                           "    shrinks.append(hours[i] - hours[i - 1])\n"),
             fails_at=5, message_contains="below 0"),
        dict(why="the shrink loop starts at 0 (hours[-1] read first: off by one)",
             code=_wlog_upto(5, shrinks="for i in range(len(hours)):\n    shrinks.append(hours[i - 1] - hours[i])\n"),
             fails_at=5, message_contains="Start the loop at 1"),
        dict(why="the shrinks typed by hand", code=_wlog_upto(5, shrinks="shrinks = [0, 1, 1, 2, 3, 4]\n"), fails_at=5,
             message_contains="typed by hand"),
        dict(why="join called the wrong way round (AttributeError)",
             code=_wlog_upto(6, join='clean_line = clean_marks.join(", ")'), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
        dict(why="the numbers joined (join needs text)", code=_wlog_upto(6, join='clean_line = ", ".join(hours)'),
             fails_at=0, message_contains="expected str instance, int found"),
        dict(why="a space between, not a comma and a space", code=_wlog_upto(6, join='clean_line = " ".join(clean_marks)'),
             fails_at=6, message_contains="comma and a space"),
        dict(why="the messy marks joined", code=_wlog_upto(6, join='clean_line = ", ".join(marks)'), fails_at=6,
             message_contains="not `marks`"),
        dict(why="the clean line typed by hand", code=_wlog_upto(6, join='clean_line = "48, 48, 47, 46, 44, 41, 37"'),
             fails_at=6, message_contains="typed by hand"),
        dict(why="joined by a loop, with one \", \" too many at the end",
             code=_wlog_upto(6, join='clean_line = ""\nfor clean in clean_marks:\n'
                                     '    clean_line = clean_line + clean + ", "'),
             fails_at=6, message_contains="after the last mark"),
        dict(why="\", \".join() on its own line (the joined text not kept)",
             code=_wlog_upto(5, join='clean_line = ""\n", ".join(clean_marks)'), fails_at=6,
             message_contains="Keep what `.join()` hands back"),
        dict(why="a + str() line where the task asks for the f-string twin",
             code=_wlog_upto(7, summary='print(str(len(hours)) + " gaps, " + str(total) + " hours in all.")\n'),
             fails_at=7, message_contains="f-string twin"),
        dict(why="an f-string added beside the + str() line, which still shows the numbers",
             code=_wlog_upto(7, summary='print(f"Total: {total}")\n'
                                        'print(str(len(hours)) + " gaps, " + str(total) + " hours in all.")\n'),
             fails_at=7, message_contains="in the f-string itself"),
        dict(why="the count typed into the f-string (7), the total in braces",
             code=_wlog_upto(7, summary='print(f"7 gaps, {total} hours in all.")\n'), fails_at=7,
             message_contains="typed into the text"),
        dict(why="the f is missing (prints the braces as they are)",
             code=_wlog_upto(7, summary='print("{len(hours)} gaps, {total} hours in all.")\n'), fails_at=7,
             message_contains="`f` right in front"),
        dict(why="a brace left open (SyntaxError)", code=_wlog_upto(7, summary='print(f"{len(hours)} gaps, {total hours.")\n'),
             fails_at=0, message_contains="f-string: expecting '}'"),
        dict(why="a brace never opened (SyntaxError)", code=_wlog_upto(7, summary='print(f"{len(hours)} gaps, total} hours.")\n'),
             fails_at=0, message_contains="single '}' is not allowed"),
        dict(why="+ between text and a number, no str()", code=_wlog_upto(7, summary='print("Total: " + total)\n'),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="the summary's numbers typed into the f-string",
             code=_wlog_upto(7, summary='print(f"7 gaps, 311 hours in all.")\n'), fails_at=7,
             message_contains="typed into the text"),
        dict(why="only the total shown", code=_wlog_upto(7, summary='print(f"{total} hours in all.")\n'), fails_at=7,
             message_contains="how many gaps too"),
        dict(why="the f-string made but never printed",
             code=_wlog_upto(7, summary='summary = f"{len(hours)} gaps, {total} hours in all."\n'), fails_at=7,
             message_contains="Print the summary"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="split-join,string-methods,fstring-read", solo="false",
             dictates="", foreign_names="note,word,nums,days,drops,parts,rain",
             reruns="'52hrs |50 hrs| 49 hrs |45hrs' (4 gaps, 196), ' 30 hrs|29hrs | 27 hrs ' (3 gaps, 86)") + "\n"
        "Project 8P1 (O, recommended, 40 min; prerequisites Lesson 8B and, for `sum()` (optional only, 3C-03), Biggest "
        "and smallest in More List Tools, both named in the intro, 2.12 rule 2; a loop total passes too). The spec's six tasks, one "
        "checkpoint each, except task 4, split into 4a `add-the-total` and 4b `find-the-shrinks` (teacher's "
        "revision: seven checkpoints; the texts and the editor comments say 4a and 4b, which the exporter keeps, as "
        "it strips only a plain leading number). The starter gives the project's first loop line once, "
        "`for mark in marks:` with `pass` under it, under `clean_marks = []`: task 2 fills it in (an idle `pass` "
        "gets its own message; lines written under the loop but not indented append only the last mark). Task 3's "
        "loop stays the student's. `print(total)` and `print(shrinks)` under their lines put the numbers Oogrish "
        "talks about on screen; the summary check reads which value is missing from the f-string itself, since "
        "`print(total)` shows the total on its own line. 4b's middle rung says why the loop starts at place 1 (a "
        "shrink compares neighbours). Task 2 cleans the TEXT (replace, then strip) "
        "into `clean_marks` and task 3 makes the numbers into `hours`: `int(\" 48 \")` is fine in Python 3 (int() "
        "ignores spaces at the ends), so a missing strip only shows on the text, and task 5 joins the clean text. "
        "Every task is CMB: the program reruns with two other messy logs (other lengths, other spacing) in the "
        "first `log = ...` line, so anything typed by hand fails, with its own message. Each task reads the "
        "program's state at the end of the run (or where a rerun stopped, whose error the evidence shows). Task 6 "
        "needs a `print` of an f-string (or of a variable made from one) and a printed line, not the clean line, "
        "that holds the count and the total; a `+ str()` line gets 'its f-string twin' (objective 6: read both, "
        "write either; this task asks for the f-string). The side quest (Lucky) reruns with a smudged `4?` mark: "
        "the plain solution stops with Python's ValueError, the class's `int(\"seven\")` slip."
    ),
)


# =============================================================================================
# Project 8P2 "The Institute Cipher" (optional, 60 min, browser-only until IDLE is confirmed [OWNER])
# =============================================================================================

NOTE_PLAIN = "lucky, it is not a compass."
NOTE_CODED = "qzhpd, ny nx sty f htrufxx."  # NOTE_PLAIN shifted by 5 (checked below)
OTHER_PLAIN = "shield up. latch stuck."
OTHER_CODED = "xmnjqi zu. qfyhm xyzhp."  # OTHER_PLAIN shifted by 5

SHIFT_BODY = (
    "    place = alphabet.find(letter)\n"
    "    if place == -1:\n"
    "        return letter\n"
    "    return alphabet[(place + key) % 26]\n"
)
ENCODE_BODY = (
    '    coded = ""\n'
    "    for letter in message:\n"
    "        coded = coded + shift_letter(letter, key)\n"
    "    return coded\n"
)
DECODE_BODY = "    return encode(message, -key)\n"
NOTE_PRINT = "print(decode(note, 5))\n"
MINE = 'my_note = "meet me by the chalk wall"\nmy_key = 7\nprint(encode(my_note, my_key))\n'


def _cipher(shift="    return letter\n", enc="    return message\n", dec="    return message\n", note_print="",
            mine="", note=NOTE_CODED, extra=""):
    """The project program with any of its parts filled in (defaults: the starter's placeholders)."""
    return (
        f'alphabet = "{ABC}"\n'
        "\n\n"
        "# 1. Shift letter forward by key.\n"
        "#    Wrap past z with % 26. Hand\n"
        "#    back anything not in alphabet\n"
        "#    as it is.\n"
        "def shift_letter(letter, key):\n"
        f"{shift}"
        "\n\n"
        'print(shift_letter("a", 2))  # c\n'
        "\n\n"
        "# 2. Shift every letter in message.\n"
        "def encode(message, key):\n"
        f"{enc}"
        "\n\n"
        'print(encode("abc", 1))  # bcd\n'
        "\n\n"
        "# 3. Shift every letter back.\n"
        "def decode(message, key):\n"
        f"{dec}"
        "\n\n"
        'print(decode("bcd", 1))  # abc\n'
        "\n\n"
        "# 4. Mar'tu's note. The key is 5.\n"
        "#    Print it, decoded.\n"
        f'note = "{note}"\n'
        f"{note_print}"
        "\n"
        "# 5. Make my_note and my_key. Print\n"
        "#    my_note, encoded.\n"
        f"{mine}"
        f"{extra}"
    )


def _cipher_upto(k, **changes):
    parts = dict(shift=SHIFT_BODY, enc=ENCODE_BODY, dec=DECODE_BODY, note_print=NOTE_PRINT, mine=MINE)
    order = ["shift", "enc", "dec", "note_print", "mine"]
    use = {name: parts[name] for name in order[:k]}
    use.update(changes)
    return _cipher(**use)


CIPHER_STARTER = _cipher()
CIPHER_SOLUTION = _cipher_upto(5)
RING_EXAMPLE = (
    'ring = "abcde"\n'
    'place = ring.find("d")\n'
    "print(place)\n"
    "print(ring[(place + 3) % 5])\n"
    'print(ring.find("!"))\n'
)
KEYS_SOLUTION = (
    "\n\ndef encode_keys(message, keys):\n"
    '    coded = ""\n'
    "    for i in range(len(message)):\n"
    "        key = keys[i % len(keys)]\n"
    "        coded = coded + shift_letter(message[i], key)\n"
    "    return coded\n"
)


def _ref_encode_py(message, key):
    return "".join(c if ABC.find(c) < 0 else ABC[(ABC.find(c) + key) % 26] for c in message)


assert _ref_encode_py(NOTE_PLAIN, 5) == NOTE_CODED and _ref_encode_py(OTHER_PLAIN, 5) == OTHER_CODED


def _typed_ints(skip):
    """Check code: the whole numbers typed inside a function, other than the ones in `skip`."""
    return ("[_n.value for _n in _ast.walk(_d) if type(_n).__name__ == 'Constant' and type(_n.value).__name__ == 'int' "
            "and _n.value not in " + repr(tuple(skip)) + "]")


_CIPHER_SHIFT = r'''
assert _g.get('alphabet') == _ABC, 'Keep line 1 as it is: `alphabet` holds the 26 small letters, a to z, in order.'
_f = _need('shift_letter', ['letter', 'key'])
_d = _defs().get('shift_letter')
_quoted = [_c for _c in _meth([_d], 'find') if _c.args and type(_c.args[0]).__name__ == 'Constant']
_keys = __TYPED__
for _c, _k in (('m', 7), ('y', 3), ('z', 1), (' ', 4), ('!', 9)):
    _what = 'called `shift_letter("' + _c + '", ' + _B.str(_k) + ')`'
    _want = _ref_shift(_c, _k)
    _val, _rows, _e = _call(_f, (_c, _k))
    if _e is not None:
        _m = _B.str(_e)
        _y = _ev(_what, 'Python stopped: ' + _err(_e))
        _mods = [_b for _b in _ast.walk(_d) if type(_b).__name__ == 'BinOp' and type(_b.op).__name__ == 'Mod']
        assert not (type(_e).__name__ == 'IndexError' and _mods), (
            'Put brackets round the sum: `alphabet[(place + key) % 26]`. Python works out `%` before `+`, so '
            '`place + key % 26` only wraps the key, and the place ran off the end past z.' + _y)
        assert type(_e).__name__ != 'IndexError', ('Wrap past z with `% 26`: `alphabet[(place + key) % 26]`. Past z, '
                                                   'the place ran off the end of the alphabet.' + _y)
        assert 'can only concatenate' not in _m, ("Find the letter's place first, `alphabet.find(letter)`: a number "
                                                  'you can add `key` to. A letter is text, and text and a number do not '
                                                  'add.' + _y)
        assert 'substring not found' not in _m, ('Use `.find()`: it hands back -1 for a letter that is not there. '
                                                 '`.index()` stops the program instead.' + _y)
        assert not (type(_e).__name__ == 'NameError' and "'find'" in _m), (
            'Write `.find()` after the text, with a dot: `alphabet.find(letter)`.' + _y)
        assert False, _why('shift_letter', _e, _what, __FOREIGN__)
    if _val == _want:
        continue
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want))
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the letter goes back to the caller.'
                                          + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, 'Hand the new letter back with `return`.' + _x
    assert type(_val).__name__ != 'int', ('Hand back the letter at the new place, `alphabet[...]`, not the place '
                                          'itself.' + _x)
    assert not _quoted, ('Take the quotes off `letter`: `alphabet.find(letter)`. `"letter"` is just those six '
                         'letters, and they are not in the alphabet in that order. ' + _QUOTES)
    assert _c in _ABC, ('Check for -1 first, and hand back `letter` as it is. `alphabet.find("' + _c + '")` is -1, '
                        'which means *not there*. It does not mean the last letter.' + _x)
    assert _val != _c, ('Find the letter\'s place, add `key`, and hand back the letter at the new place. '
                        '`shift_letter` still hands back the letter as it came in.' + _x)
    for _t in _keys:
        assert _val != _ref_shift(_c, _t), ('Use the parameter `key`, not a typed ' + _B.str(_t) + ', so every key '
                                            'works.' + _x)
    assert False, 'Hand back `alphabet[(place + key) % 26]`, where `place` is `alphabet.find(letter)`.' + _x
'''

_CIPHER_ENCODE = r'''
_f = _need('encode', ['message', 'key'])
_d = _defs().get('encode')
_keys = __TYPED__
for _m, _k in (('burst at dusk', 3), ('moss, glow!', 25)):
    _what = 'called `encode("' + _m + '", ' + _B.str(_k) + ')`'
    _want = _ref_encode(_m, _k)
    _val, _rows, _e = _call(_f, (_m, _k))
    if _e is not None:
        _y = _ev(_what, 'Python stopped: ' + _err(_e))
        assert 'item assignment' not in _B.str(_e), (
            'Build a new text: start with `coded = ""`, then add each shifted letter on, `coded = coded + '
            'shift_letter(letter, key)`. Text cannot change in place.' + _y)
        assert False, _why('encode', _e, _what, __FOREIGN__)
    if _val == _want:
        continue
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want))
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the coded text goes back to the '
                                          'caller.' + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, 'Hand back the coded text with `return coded`, under the loop.' + _x
    assert _val != _m, ('Shift each letter: loop over `message`, and add `shift_letter(letter, key)` onto a new text. '
                        '`encode` still hands back the message as it came in.' + _x)
    assert not [_l for _l in _ast.walk(_d) if type(_l).__name__ == 'For' and type(_l.iter).__name__ == 'Constant'], (
        'Take the quotes off `message`: `for letter in message:`. In quotes, it is just those letters, the same for '
        'every message. ' + _QUOTES + _x)
    assert type(_val).__name__ != 'list', ('Build text, not a list: `coded = coded + shift_letter(letter, key)`.'
                                           + _x)
    assert type(_val).__name__ == 'str', 'Hand back the coded text.' + _x
    if _B.len(_val) <= 1:
        assert not _inside(_d, 'Return'), ('Move `return coded` out of the loop: line it up with `for`. Inside the '
                                           'loop, the function hands back after the first letter.' + _x)
        assert False, ('Add each letter on: `coded = coded + shift_letter(letter, key)`. Your text kept only one '
                       'letter.' + _x)
    for _t in _keys:
        assert _val != _ref_encode(_m, _t), ('Hand `key` on to `shift_letter`, not a typed ' + _B.str(_t) + ', so '
                                             'every key works.' + _x)
    assert False, 'Hand back every character of `message`, each one passed through `shift_letter(letter, key)`.' + _x
'''

_CIPHER_DECODE = r'''
_f = _need('decode', ['message', 'key'])
for _plain, _k in (('ember wall', 4), ('frost veil, moon step.', 11)):
    _m = _ref_encode(_plain, _k)
    _what = 'called `decode("' + _m + '", ' + _B.str(_k) + ')`'
    _val, _rows, _e = _call(_f, (_m, _k))
    if _e is not None:
        _y = _ev(_what, 'Python stopped: ' + _err(_e))
        assert type(_e).__name__ != 'RecursionError', (
            'Call `encode` inside `decode`, not `decode` itself: `return encode(message, -key)`. A function that '
            'calls itself never stops.' + _y)
        assert False, _why('decode', _e, _what, __FOREIGN__)
    if _val == _plain:
        continue
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_plain))
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the plain text goes back to the '
                                          'caller.' + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, 'Hand back the plain text with `return`: `return encode(message, -key)`.' + _x
    assert _val != _m, ('Shift every letter back: `return encode(message, -key)`. `decode` still hands back the '
                        'message as it came in.' + _x)
    assert _val != _ref_encode(_m, _k), ('Shift back, not forward: hand `encode` the key the other way round, '
                                         '`-key`. Your `decode` moved the letters on again.' + _x)
    assert False, 'Shift every letter back by `key`: `return encode(message, -key)`.' + _x
'''

_CIPHER_NOTE = r'''
_own = _first_text('note')
assert _own is not None, 'Keep the line `note = "..."` from the starter, so Mar\'tu\'s check can try another note there.'
_plain = _ref_encode(_own, -5)
_rows = _lines()
_shows = lambda _t, _rs: _B.bool([_l for _l in _rs if _t.strip() and _t.strip() in _l])
if not _shows(_plain, _rows):
    _calls = [_c for _c in _calls_in(_top(), 'encode') + _calls_in(_top(), 'decode') if _c.args]
    assert not [_c for _c in _calls_in(_top(), 'encode') if _c.args and type(_c.args[0]).__name__ == 'Name'
                and _c.args[0].id == 'note'], ('Decode it, do not encode it: `print(decode(note, 5))`. `encode` '
                                               'shifts the letters further on.')
    assert not [_c for _c in _calls if type(_c.args[0]).__name__ == 'Constant' and _c.args[0].value == 'note'], (
        'Take the quotes off `note`: `decode(note, 5)`. `"note"` is just those four letters. ' + _QUOTES)
    assert not [_k for _k in _B.range(1, 26) if _k != 5 and _shows(_ref_encode(_own, -_k), _rows)], (
        'Use the key 5, the hour on the note: `decode(note, 5)`. Another key moves the letters to the wrong places.')
    assert not [_s for _s in _top() if type(_s).__name__ == 'Expr' and _calls_in([_s], 'decode')
                and not _calls_in([_s], 'print')], ('Print it: `print(decode(note, 5))`. On its own line, the '
                                                   'decoded note is made and thrown away.')
    assert False, 'Print the note, decoded: `print(decode(note, 5))`.'
_ns, _rows2, _e, _left = _rerun({'note': __OTHER__})
_x = " (Mar'tu's check tried another note, `\"" + __OTHER__ + "\"`, only inside the check.)"
if not _shows(__OTHER_PLAIN__, _rows2):
    assert _e is None, 'Make it work for another note too. Python stopped: ' + _err(_e) + '.' + _x
    assert not _shows(_plain, _rows2), ('Let `decode` read the note: `print(decode(note, 5))`. A line typed by hand cannot '
                                  'follow another note.' + _x)
    assert False, 'Print `decode(note, 5)`, so any note in `note` is decoded.' + _x
'''

_CIPHER_MINE = r'''
assert 'my_note' in _g, 'Make `my_note` under task 5: any message you like, in quotes.'
_n = _g.get('my_note')
assert type(_n).__name__ == 'str', 'Put your message in quotes: `my_note = "..."`. ' + _QUOTES
assert [_c for _c in _n if _c in _ABC], 'Put some small letters in `my_note`. Only a to z get shifted.'
assert 'my_key' in _g, 'Make `my_key` under task 5: a whole number from 1 to 25.'
_k = _g.get('my_key')
assert type(_k).__name__ == 'int', 'Make `my_key` a whole number, like `7`, with no quotes.'
assert _k % 26 != 0, ('Pick a key from 1 to 25. A key of 0, or 26, moves every letter all the way round, back where '
                      'it started, so nothing is hidden.')
_secret = _ref_encode(_n, _k)
_rows = _lines()
_shows = lambda _t, _rs: _B.bool([_l for _l in _rs if _t.strip() and _t.strip() in _l])
if not _shows(_secret, _rows):
    assert not _shows(_n, _rows), 'Print `my_note` coded, not as it is: `print(encode(my_note, my_key))`.'
    assert False, 'Print your note, coded: `print(encode(my_note, my_key))`.'
assert _first('my_note') is not None, ("Make `my_note` on a line of its own, with `=`, so Mar'tu's check can try "
                                        'another note there.')
_other = 'moss and ember, at dusk'
_k2 = 12 if _k % 26 == 11 else 11
_ns, _rows2, _e, _left = _rerun({'my_note': _other, 'my_key': _k2})
if not _shows(_ref_encode(_other, _k2), _rows2):
    _y = _ev('tried another note in `my_note`' + ('' if 'my_key' in _left else ' and another key in `my_key`'))
    assert not _shows(_ref_encode(_other, _k), _rows2), (
        'Hand `my_key` to `encode`: `encode(my_note, my_key)`. A key typed into the call cannot follow another key.'
        + _y)
    _typed_in = [_c for _c in _calls_in(_top(), 'encode') if _c.args and type(_c.args[0]).__name__ == 'Constant'
                 and _c.args[0].value == _n]
    assert not _typed_in, ('Hand `my_note` to `encode`: `encode(my_note, my_key)`. A note typed into the call '
                           'cannot follow another note.' + _y)
    assert False, ('Let `encode` do the shifting: `print(encode(my_note, my_key))`. A coded note typed by hand cannot '
                   'follow another note.' + _y)
'''

_CIPHER_KEYS = r'''
_f = _need('encode_keys', ['message', 'keys'])
for _m, _ks in (('abc abc', [1, 2]), ('glow', [3]), ('moon step', [2, 0, 5])):
    _want = ''.join([_ref_shift(_m[_i], _ks[_i % _B.len(_ks)]) for _i in _B.range(_B.len(_m))])
    _what = 'called `encode_keys("' + _m + '", ' + _B.str(_ks) + ')`'
    _val, _rows, _e = _call(_f, (_m, _ks))
    assert _e is None, _why('encode_keys', _e, _what, __FOREIGN__)
    assert _val == _want, ('Shift the character at place `i` by `keys[i % len(keys)]`, and add it on.'
                           + _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want)))
'''

# The hints' example names (`place` is left out: the solution makes it too). A NameError on one gets _why().
CIPHER_FOREIGN = ("ring", "out", "ch", "word", "secret")
_SHIFT_BODY_CHECK = _CIPHER_SHIFT.replace("__TYPED__", _typed_ints((0, 1, 26)))
_ENCODE_BODY_CHECK = _CIPHER_ENCODE.replace("__TYPED__", _typed_ints((0,)))

PROJECT_8P2 = dict(
    kind="project",
    id="the-institute-cipher",
    title="The Institute Cipher",
    optional=True,
    minutes=60,
    summary="Ley shift, the Institute's secret code: move every letter along the alphabet, then read Mar'tu's note.",
    intro=(
        "Mar'tu still writes notes in the Institute's old code, ley shift: a [[cipher]]. Every letter moves along "
        "the alphabet by the hour on the Ley Clock. A note was pinned to the mantle this morning. The clock said 5.\n"
        "Five tasks, in order. The comments in the editor mark each one. It all runs here, in the browser.\n"
        "Before this: the Clock Math article in Unit 1 (`%`, the [[remainder]]), and Lesson 8B (`.find()`)."
    ),
    martu=(
        "Each letter has a place in `alphabet`: `a` is 0, `b` is 1, `z` is 25. `alphabet.find(letter)` hands you "
        "that place. For anything not in the alphabet, like a space or a comma, it hands back -1. That means *not "
        "there*. It does not mean the last letter.\n"
        "Add `key` to the place. Past `z`, wrap back round to `a` with `% 26`, the clock math from Unit 1. A clock "
        "wraps at 12. The alphabet wraps at 26.\n"
        "Then read the letter at the new place. Text can't change in place, so `encode` builds a new text, one "
        "letter at a time."
    ),
    example=RING_EXAMPLE,
    example_output="3\nb\n-1",
    names=["alphabet", "shift_letter", "letter", "key", "encode", "message", "decode", "note", "my_note", "my_key"],
    pick='"meet me by the chalk wall"',
    predict=dict(
        q="Before you start: what will these two lines print?",
        code='abc = "abcdefghijklmnopqrstuvwxyz"\nprint(abc.find("c"))\nprint(abc.find("?"))\n',
        choices=["3\n0", "2\n-1", "2\n25", "3\n-1"],
        answer=1,
        explain=(
            "Places start at 0, so `c` is at 2. `?` is not in the text, so `.find()` hands back -1: not there. "
            "It is a signal, not the last letter."
        ),
    ),
    pair_talk=(
        "Pair talk: when you finish task 5, tell your partner your key, but not your note. Each of you copies the "
        "other's coded note into `decode(...)` on your own screen, and reads it."
    ),
    starter=CIPHER_STARTER,
    checkpoints=[
        dict(
            id="shift-a-letter",
            text="1. Make `shift_letter` hand back `letter` moved forward by `key`, wrapping past z. Anything not in "
                 "`alphabet` comes back as it is.",
            dictated=False,
            hints=[
                "Look at task 1. `shift_letter` hands back `letter` as it came in, so nothing moves.",
                "Three steps: find the place with `alphabet.find(letter)`. If the place is -1, hand back `letter`. "
                "Else hand back the letter at `(place + key) % 26`.",
                "With other names: in `ring = \"abcde\"`, `ring[(ring.find(\"d\") + 3) % 5]` is `\"b\"`. It wraps "
                "past the end.",
                "Write `place = alphabet.find(letter)`, then `if place == -1:` with `return letter` under it, then "
                "`return alphabet[(place + key) % 26]`.",
            ],
            checks=[check("shift_letter moves letters and leaves the rest as they are", _SHIFT_BODY_CHECK,
                          foreign=CIPHER_FOREIGN)],
            pass_line="Gearshift: Visor dims. y plus 3 wraps to b. The math holds.",
        ),
        dict(
            id="encode-a-message",
            text="2. Make `encode` hand back `message` with every letter shifted by `key`.",
            dictated=False,
            hints=[
                "Look at task 2. `encode` hands back `message` as it came in.",
                "Text can't change in place. Start a new text, `coded = \"\"`, and loop over `message`. Add each "
                "shifted letter on, then hand back `coded` after the loop.",
                "With other names: `out = \"\"`, then `for ch in word:` and `out = out + ch.upper()`.",
                "Write `coded = \"\"`, then `for letter in message:` with `coded = coded + shift_letter(letter, key)` "
                "under it, then `return coded`.",
            ],
            checks=[check("encode shifts every letter of the message", _ENCODE_BODY_CHECK, foreign=CIPHER_FOREIGN)],
            pass_line="Mar'tu: Letter by letter, into a new text. That is how the Institute did it, yes?",
        ),
        dict(
            id="decode-a-message",
            text="3. Make `decode` hand back `message` with every letter shifted back by `key`.",
            dictated=False,
            hints=[
                "Look at task 3. `decode` hands back `message` as it came in.",
                "Shifting back by `key` is shifting forward by `-key`. `encode` can do that for you.",
                "With numbers: 7 steps on, then 7 steps back, lands where you started. `(2 + 7 - 7) % 26` is 2. "
                "Going back past `a` wraps too: `(2 - 5) % 26` is 23, which is `x`.",
                "Write `return encode(message, -key)` in place of `return message`.",
            ],
            checks=[check("decode shifts every letter back", _CIPHER_DECODE, foreign=CIPHER_FOREIGN)],
            pass_line="Mar'tu: Forward to hide, back to read. Good.",
        ),
        dict(
            id="read-the-note",
            text="4. Print Mar'tu's note, decoded with the key 5.",
            dictated=False,
            hints=[
                "Look at task 4. The note is in `note`, and nothing prints it yet.",
                "Your `decode` takes the coded text and the key, and hands back plain text. Print what it hands back.",
                "With other names: `print(decode(\"bcd\", 1))` shows `abc`.",
                "Write `print(decode(note, 5))` under the note.",
            ],
            checks=[check("the note prints, decoded by decode", _CIPHER_NOTE, other=OTHER_CODED,
                          other_plain=OTHER_PLAIN)],
            pass_line="Lucky: It is not a compass. Even in code. Unbelievable.",
        ),
        dict(
            id="your-own-note",
            text="5. Make `my_note`, any message, and `my_key`, a whole number from 1 to 25. Print `my_note`, encoded.",
            dictated=False,
            hints=[
                "Look at task 5. Make two variables: your note, and your key.",
                "Any message in quotes, in small letters, and a key from 1 to 25. Then print what `encode` hands back.",
                "With other names: `secret = encode(\"see you at dusk\", 3)`, then `print(secret)`.",
                "Put your own words in `my_note = \"...\"` (or Mar'tu's pick, `\"meet me by the chalk wall\"`), "
                "make `my_key` any number from 1 to 25, then `print(encode(my_note, my_key))`.",
            ],
            checks=[check("my_note prints, encoded with my_key", _CIPHER_MINE)],
            pass_line="Mar'tu: A secret. Keep the key in your head, not on the wall.",
        ),
    ],
    solution=CIPHER_SOLUTION,
    partials=[_cipher_upto(k) for k in range(1, 5)],
    assemble=dict(
        lines=code_lines(CIPHER_SOLUTION),
        distractors=["    return alphabet[place + key]", "    return encode(message, key)",
                     "        coded = shift_letter(letter, key)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The alphabet on a ring",
            text=(
                "```text\n a  b  c ...  x  y  z\n 0  1  2 ... 23 24 25\n\ny + 3: 24 + 3 = 27\n27 % 26 = 1  ->  b\n```\n"
                "Past `z`, the count goes round to the start again, like a clock hand past 12."
            ),
        ),
        dict(
            angle="everyday",
            label="A clock with 26 hours",
            text=(
                "Picture a clock with a letter on every hour, 26 of them. A key of 3 turns the hand 3 hours on. From "
                "`y`, three hours on is `b`. `% 26` is the hand going round."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`shift_letter(\"y\", 3)`:\n"
                "1. `alphabet.find(\"y\")` is 24. It is not -1, so keep going.\n"
                "2. `24 + 3` is 27, past the end.\n"
                "3. `27 % 26` is 1.\n"
                "4. `alphabet[1]` is `\"b\"`. Hand it back."
            ),
        ),
        dict(
            angle="shorter",
            text="Place with `.find()`; -1 means leave it. New place `(place + key) % 26`. Build the text letter by letter.",
        ),
    ],
    bonus=dict(
        by="mar-tu",
        title="The hard notes",
        text=(
            "At the Institute, the hard notes changed key on every letter. Write `encode_keys(message, keys)`, where "
            "`keys` is a list of numbers. The character at place `i` shifts by `keys[i % len(keys)]`."
        ),
        hints=[
            "Loop over places: `for i in range(len(message)):`. The key for this one is `keys[i % len(keys)]`.",
            "Add `shift_letter(message[i], key)` onto a new text, and hand it back after the loop.",
        ],
        checks=[check("encode_keys changes key on every letter", _CIPHER_KEYS, foreign=CIPHER_FOREIGN)],
        solution=CIPHER_SOLUTION + KEYS_SOLUTION,
    ),
    campaign_link=dict(
        module=MODULE_2,
        part="ley-clock",
        why=(
            "Lucky kept calling the Ley Clock a compass, and Mar'tu's note says so again, in code. The key is an hour "
            "on that clock, and `% 26` wraps the alphabet the way the clock's hand wraps past 12."
        ),
    ),
    takeaway="`.find()` gives a place, or -1 for not there. `(place + key) % 26` wraps past z. Build new text letter "
             "by letter.",
    wrong_answers=[
        dict(why="the starter: every letter comes back as it is", code=CIPHER_STARTER, fails_at=1,
             message_contains="as it came in"),
        dict(why=".find() -1 read as the last place (a space shifted into a letter)",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    return alphabet[(place + key) % 26]\n"),
             fails_at=1, message_contains="It does not mean the last letter"),
        dict(why="no % 26: the place runs past z (IndexError)",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        return letter\n"
                                        "    return alphabet[place + key]\n"),
             fails_at=1, message_contains="`% 26`"),
        dict(why="no brackets round the sum: place + key % 26 wraps only the key (IndexError past z)",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        return letter\n"
                                        "    return alphabet[place + key % 26]\n"),
             fails_at=1, message_contains="Put brackets round the sum"),
        dict(why="a typo in the -1 branch (leter), which only the check's space reaches: _why names the parameter",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        return leter\n"
                                        "    return alphabet[(place + key) % 26]\n"),
             fails_at=1, message_contains="Inside `shift_letter`, Python stopped: NameError: name 'leter' is not "
                                          "defined. You wrote `leter`, and the parameter is `letter`."),
        dict(why="a near-miss variable in encode (return code, not coded), the starter's call taken out",
             code=_cipher_upto(2, enc=ENCODE_BODY.replace("return coded", "return code"))
             .replace('print(encode("abc", 1))  # bcd\n', ""),
             fails_at=2, message_contains="Inside `encode`, Python stopped: NameError: name 'code' is not defined. "
                                          "You wrote `code`, and the variable is `coded`."),
        dict(why="shift_letter handed one value inside encode, the starter's call taken out: _why counts the values",
             code=_cipher_upto(2, enc=ENCODE_BODY.replace("shift_letter(letter, key)", "shift_letter(letter)"))
             .replace('print(encode("abc", 1))  # bcd\n', ""),
             fails_at=2, message_contains="Inside `encode`, Python stopped: TypeError: shift_letter() missing 1 "
                                          "required positional argument: 'key'. Count the values a call hands to "
                                          "`shift_letter`, against its `def` line"),
        dict(why="a letter and a number added (text + int)", code=_cipher_upto(1, shift="    return letter + key\n"),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="the place handed back, not the letter",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        return letter\n"
                                        "    return (place + key) % 26\n"),
             fails_at=1, message_contains="not the place itself"),
        dict(why="a typed key (the task's own 2)",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        return letter\n"
                                        "    return alphabet[(place + 2) % 26]\n"),
             fails_at=1, message_contains="not a typed 2"),
        dict(why="the parameter in quotes (find(\"letter\") is always -1)",
             code=_cipher_upto(1, shift='    place = alphabet.find("letter")\n    if place == -1:\n'
                                        "        return letter\n    return alphabet[(place + key) % 26]\n"),
             fails_at=1, message_contains="Take the quotes off `letter`"),
        dict(why="print in place of return",
             code=_cipher_upto(1, shift="    place = alphabet.find(letter)\n    if place == -1:\n        print(letter)\n"
                                        "    print(alphabet[(place + key) % 26])\n"),
             fails_at=1, message_contains="in place of `print`"),
        dict(why=".index() stops at a space (find hands back -1 instead)",
             code=_cipher_upto(1, shift="    place = alphabet.index(letter)\n    return alphabet[(place + key) % 26]\n"),
             fails_at=1, message_contains="`.index()` stops"),
        dict(why="a letter changed in place inside encode (TypeError)",
             code=_cipher_upto(2, enc="    for i in range(len(message)):\n"
                                      "        message[i] = shift_letter(message[i], key)\n    return message\n"),
             fails_at=0, message_contains="does not support item assignment"),
        dict(why="the loop walks the text \"message\" in quotes",
             code=_cipher_upto(2, enc='    coded = ""\n    for letter in "message":\n'
                                      "        coded = coded + shift_letter(letter, key)\n    return coded\n"),
             fails_at=2, message_contains="Take the quotes off `message`"),
        dict(why="return inside the loop (one letter back)",
             code=_cipher_upto(2, enc='    coded = ""\n    for letter in message:\n'
                                      "        coded = coded + shift_letter(letter, key)\n        return coded\n"),
             fails_at=2, message_contains="out of the loop"),
        dict(why="each letter replaces the last (coded = shift_letter(...))",
             code=_cipher_upto(2, enc='    coded = ""\n    for letter in message:\n'
                                      "        coded = shift_letter(letter, key)\n    return coded\n"),
             fails_at=2, message_contains="Add each letter on"),
        dict(why="a typed key inside encode (the task's own 1)",
             code=_cipher_upto(2, enc='    coded = ""\n    for letter in message:\n'
                                      "        coded = coded + shift_letter(letter, 1)\n    return coded\n"),
             fails_at=2, message_contains="not a typed 1"),
        dict(why="the whole message handed to shift_letter (find gives -1: nothing moves)",
             code=_cipher_upto(2, enc="    return shift_letter(message, key)\n"), fails_at=2,
             message_contains="as it came in"),
        dict(why="a list built, not text",
             code=_cipher_upto(2, enc="    coded = []\n    for letter in message:\n"
                                      "        coded.append(shift_letter(letter, key))\n    return coded\n"),
             fails_at=2, message_contains="not a list"),
        dict(why="decode shifts forward again", code=_cipher_upto(3, dec="    return encode(message, key)\n"),
             fails_at=3, message_contains="Shift back, not forward"),
        dict(why="decode calls itself forever (RecursionError)", code=_cipher_upto(3, dec="    return decode(message, -key)\n"),
             fails_at=0, message_contains="recursion"),
        dict(why="the decoded note typed by hand", code=_cipher_upto(3, note_print=f'print("{NOTE_PLAIN}")\n'),
             fails_at=4, message_contains="typed by hand"),
        dict(why="the note encoded, not decoded", code=_cipher_upto(3, note_print="print(encode(note, 5))\n"),
             fails_at=4, message_contains="do not encode it"),
        dict(why="note in quotes", code=_cipher_upto(3, note_print='print(decode("note", 5))\n'), fails_at=4,
             message_contains="Take the quotes off `note`"),
        dict(why="the wrong key", code=_cipher_upto(3, note_print="print(decode(note, 4))\n"), fails_at=4,
             message_contains="key 5"),
        dict(why="decoded but not printed (the result not kept)", code=_cipher_upto(3, note_print="decode(note, 5)\n"),
             fails_at=4, message_contains="Print it"),
        dict(why="the key left out (missing argument)", code=_cipher_upto(3, note_print="print(decode(note))\n"),
             fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="no note of your own yet", code=_cipher_upto(4), fails_at=5, message_contains="Make `my_note`"),
        dict(why="a key of 0 hides nothing",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = 0\n'
                                       "print(encode(my_note, my_key))\n"),
             fails_at=5, message_contains="1 to 25"),
        dict(why="the key in quotes (text + number inside shift_letter)",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = "7"\n'
                                       "print(encode(my_note, my_key))\n"),
             fails_at=0, message_contains="unsupported operand"),
        dict(why="the coded note typed by hand",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = 7\n'
                                       f'print("{_ref_encode_py("meet me by the chalk wall", 7)}")\n'),
             fails_at=5, message_contains="typed by hand"),
        dict(why="the key typed into the call (encode(my_note, 7)), not my_key",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = 7\n'
                                       "print(encode(my_note, 7))\n"),
             fails_at=5, message_contains="A key typed into the call"),
        dict(why="the note typed into the call, not my_note",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = 7\n'
                                       'print(encode("meet me by the chalk wall", my_key))\n'),
             fails_at=5, message_contains="A note typed into the call"),
        dict(why="my_note printed as it is, not encoded",
             code=_cipher_upto(4, mine='my_note = "meet me by the chalk wall"\nmy_key = 7\nprint(my_note)\n'),
             fails_at=5, message_contains="not as it is"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="string-index-slice,string-methods,loop-letters",
             solo="false", dictates="", foreign_names="ring,place,out,ch,word,secret",
             par="shift_letter ('m',7),('y',3),('z',1),(' ',4),('!',9); encode ('burst at dusk',3),('moss, glow!',25); "
                 "decode ('ember wall',4),('frost veil, moon step.',11)",
             prereq="1-A2 Clock Math (op:Mod, optional) and Lesson 8B (attr:find), named in the intro",
             browser_only="yes, until the teacher confirms IDLE [OWNER]") + "\n"
        "Project 8P2 (O, 60 min). Browser-only: the intro says it all runs in the browser, and nothing offers IDLE "
        "until the teacher confirms it (curriculum Q14, open question 7 [OWNER]). Prerequisites (2.12 rule 2): `%` "
        "comes from the optional Clock Math article (u01d), named in the intro as the recap card; `.find()` from "
        "Lesson 8B. Tasks 1-3 are PAR/RET against a reference cipher in the check (letters, wrap-arounds past z, a "
        "space and a \"!\"; no fresh call gives the task's own `c`, `bcd` or `abc`, lint b). Task 1 catches the "
        "class's `.find()` -1 slip by name (a space comes back as `d`). Task 2 catches text changed in place "
        "(Python's TypeError at the starter's own call). Task 3 accepts any working decode (`-key`, `26 - key`, "
        "`key - 26`, its own loop). Task 4 reruns with another note shifted by 5, so a typed answer fails. Task 5 is "
        "creative (any note, any key from 1 to 25; lint e): the check encodes the student's own note with a reference "
        "cipher and reruns with another note in `my_note`, so a coded note typed by hand fails. A student's note "
        "is never repeated in a message (2.11). Any other crash inside `shift_letter`, `encode`, `decode` or "
        "`encode_keys` during the check's own calls gets _why() (as Units 3 and 7, and u09a): the hints' example "
        "names, a near-miss parameter (`leter`) or variable (`code`), and the unit's rows (a call that hands over "
        "the wrong number of values, a place past the end). Mar'tu's side quest: a key list that changes on every "
        "letter."
    ),
)


# =============================================================================================
# Optional advanced challenge "Name Tags, From Blank" (after 8P2; costs no one core time)
# =============================================================================================

TAGB_STARTER = "# Write name_tag(name, hours) here.\n"
TAGB_SIG = "def name_tag(name, hours):\n"
TAGB_BODY = "    caps = name.upper()\n" '    return f"{caps}: {hours} hrs"\n'
TAGB_PRINTS = 'print(name_tag("Lucky", 48))\nprint(name_tag("Oogrish", 311))\n'
# The hints' example names: a NameError on one of them is explained by _why().
TAGB_FOREIGN = ("label", "item", "cost")


def _tagb(body=TAGB_BODY, prints=TAGB_PRINTS, sig=TAGB_SIG, head=TAGB_STARTER):
    """The challenge program: the starter's comment, then `name_tag` (when `body` is not None), then the prints."""
    out = head
    if body is not None:
        out += sig + body
    if prints:
        out += "\n\n" + prints
    return out


TAGB_SOLUTION = _tagb()

_TAGB_TAG = r'''
_f = _need_def('name_tag', 2, 'def name_tag(name, hours):')
_d = _defs().get('name_tag')
_got = []
for _n, _h, _want in (('Pell', 7, 'PELL: 7 hrs'), ('moss', 12, 'MOSS: 12 hrs')):
    _what = 'called `name_tag("' + _n + '", ' + _B.str(_h) + ')`'
    _val, _rows, _e = _call(_f, (_n, _h))
    if _e is not None:
        _y = _ev(_what, 'Python stopped: ' + _err(_e))
        assert 'can only concatenate' not in _B.str(_e), (
            'Put the hours in the f-string, `{hours}`: an f-string turns a number into text for you. `+` glues text '
            'only to text.' + _y)
        assert not (type(_e).__name__ == 'NameError' and "'upper'" in _B.str(_e)), (
            'Write `.upper()` after the text, with a dot: `name.upper()`. Python has no `upper()` on its own.' + _y)
        assert False, _why('name_tag', _e, _what, __FOREIGN__)
    _got.append((_n, _h, _want, _what, _val, _rows))
_bad = [_r for _r in _got if _r[4] != _r[2]]
if _bad:
    _n, _h, _want, _what, _val, _rows = _bad[0]
    _x = _ev(_what, 'it gave back ' + _said(_val) + ', not ' + _sh(_want))
    assert not (_val is None and _rows), ('Use `return` in place of `print`, so the tag goes back to the caller.'
                                          + _ev(_what, 'it printed, then gave back `None`'))
    assert _val is not None, 'Hand the tag back with `return`, at the end of `name_tag`.' + _x
    assert type(_val).__name__ == 'str', 'Hand back the tag as text, built with an f-string.' + _x
    assert not ('{' in _val and '}' in _val), (
        'Put an `f` right in front of the opening quote: `f"..."`. Without it, Python hands back the braces and the '
        'names inside them, letter for letter.' + _x)
    _up = [_a for _a in _ast.walk(_d) if type(_a).__name__ == 'Attribute' and _a.attr == 'upper']
    assert not ('built-in method' in _val or _B.len(_up) > _B.len(_meth([_d], 'upper'))), (
        'Add `()` after `upper`: `name.upper()`. Without them, Python shows the method itself, not the capitals.'
        + _x)
    if _B.len(_B.set([_r[4] for _r in _got])) == 1:
        assert False, ('Build the tag from `name` and `hours`, so it follows any name. A tag typed by hand stays the '
                       'same.' + _ev('called `name_tag` with two names and two numbers',
                                     'both gave back ' + _said(_val)))
    assert _val != _want.upper(), ('Put `.upper()` on the name only: `name.upper()`. On the whole tag, it turns `hrs` '
                                   'into `HRS` too.' + _x)
    assert _val != _n + ': ' + _B.str(_h) + ' hrs', ('Put the name in capitals with `.upper()`: `caps = name.upper()`, '
                                                     'then `{caps}` in the f-string.' + _x)
    assert _B.str(_h) in _val, 'Put the hours in the tag too: `{hours}`, inside the f-string.' + _x
    assert _val.endswith(' hrs'), 'End the tag with a space and `hrs`, after the hours: `{hours} hrs`.' + _x
    assert False, ('Hand back the name in capitals, then a colon and a space, then the hours and ` hrs`, like '
                   '`LUCKY: 48 hrs`.' + _x)
'''

_TAGB_TOOLS = r'''
_f = _need_def('name_tag', 2, 'def name_tag(name, hours):')
_d = _defs().get('name_tag')
if not [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'JoinedStr']:
    _glue = ([_n for _n in _ast.walk(_d) if type(_n).__name__ == 'BinOp' and type(_n.op).__name__ == 'Add']
             or _calls_in([_d], 'str'))
    assert not _glue, ('This challenge practices the f-string. Your `+ str()` line works, and the campaign reads like '
                       'that. Now write its twin: `return f"{name.upper()}: {hours} hrs"`.')
    assert False, ('This challenge practices the f-string: an `f` right before the quote, and `{...}` round each '
                   'value, like `f"{caps}: {hours} hrs"`.')
assert _meth([_d], 'upper'), ('This challenge practices `.upper()`: make the capitals with `caps = name.upper()`, '
                              'then put `{caps}` in the f-string.')
'''

_TAGB_SHOWN = r'''
_f = _need_def('name_tag', 2, 'def name_tag(name, hours):')
_d = _defs().get('name_tag')
_made = _B.set(_t.id for _s in _top() if type(_s).__name__ == 'Assign' and _calls_in([_s.value], 'name_tag')
               for _t in _s.targets if type(_t).__name__ == 'Name')
_is_tag = lambda _c: _B.bool(_calls_in(_c.args, 'name_tag') or [_a for _a in _c.args if type(_a).__name__ == 'Name'
                                                                 and _a.id in _made])
_shown = [_c for _c in _calls_in(_top(), 'print') if _is_tag(_c)]
_looped = [_c for _s in _top() if type(_s).__name__ in ('For', 'While') for _c in _calls_in([_s], 'print')
           if _is_tag(_c)]
if not (_B.len(_shown) >= 2 or (_looped and _B.len(_lines()) >= 2)):
    assert not [_c for _c in _calls_in([_d], 'print') if _calls_in(_c.args, 'name_tag')], (
        'Move the `print(name_tag(...))` lines out of the function: line them up with `def`, below it. Inside '
        '`name_tag`, under `return`, they never run.')
    assert not [_s for _s in _top() if type(_s).__name__ == 'Expr' and _calls_in([_s], 'name_tag')
                and not _calls_in([_s], 'print')], (
        'Print what `name_tag` hands back: `print(name_tag("Lucky", 48))`. On its own line, the tag is made and '
        'thrown away.')
    assert not [_c for _c in _calls_in(_top(), 'print') if [_a for _a in _c.args if type(_a).__name__ == 'Name'
                                                            and _a.id == 'name_tag']], (
        'Add brackets with a name and the hours: `print(name_tag("Lucky", 48))`. Without them, Python prints the '
        'function itself.')
    assert _shown or not [_c for _c in _calls_in(_top(), 'print') if [_a for _a in _c.args
                                                                       if type(_a).__name__ in ('Constant', 'JoinedStr')]], (
        'Let `name_tag` build each tag: `print(name_tag("Lucky", 48))`. A tag typed by hand skips the function.')
    assert _shown, 'Print two tags below the function: `print(name_tag("Lucky", 48))`, then one more like it.'
    assert False, 'Print a second tag: one more `print(name_tag(...))` line, with another name and number.'
'''

TAG_FROM_BLANK = dict(
    kind="challenge",
    id="tag-from-blank",
    title="Name Tags, From Blank",
    level="advanced",
    optional=True,
    minutes=10,
    support="light",
    summary="Write name_tag from a blank page: the name in capitals with .upper(), the tag with an f-string.",
    martu=(
        "A blank page, and one small job. Write `name_tag(name, hours)` that hands back a tag like `LUCKY: 48 hrs`, "
        "using `.upper()` and an f-string. Then print two tags.\n"
        "`.upper()` makes the capitals. The f-string puts the name, the hours and `hrs` into one text, with no `+` "
        "and no `str()`.\n"
        "My check tries other names and other hours, only inside the check. So build the tag from `name` and "
        "`hours`. Never type it.\n"
        "Before this: Lesson 8B."
    ),
    names=["name_tag", "name", "hours"],
    starter=TAGB_STARTER,
    checkpoints=[
        dict(
            id="write-name-tag",
            text="Write `name_tag(name, hours)`. It returns a tag like `LUCKY: 48 hrs`, built with `.upper()` and an "
                 "f-string.",
            dictated=False,
            hints=[
                "Look at the top of the page. The `def` line comes first: `name_tag`, then `name` and `hours` in "
                "brackets. Inside it, make the tag and hand it back with `return`.",
                "`.upper()` hands back a copy in capitals: `\"glow\".upper()` is `\"GLOW\"`. In an f-string, each "
                "`{...}` shows a value, so one text can hold the name and the number.",
                "With other names: `def label(item, cost):`, then `return f\"{item.upper()} - {cost} gold\"`. "
                "`label(\"rope\", 5)` hands back `ROPE - 5 gold`.",
                "Write `def name_tag(name, hours):`. Under it, indented: `caps = name.upper()`, then "
                "`return f\"{caps}: {hours} hrs\"`.",
            ],
            checks=[
                check("name_tag hands back the tag for any name and hours", _TAGB_TAG, foreign=TAGB_FOREIGN),
                check("name_tag builds the tag with .upper() and an f-string", _TAGB_TOOLS),
            ],
            pass_line="Lucky: LUCKY. In capitals. Finally, a tag that knows who I am.",
        ),
        dict(
            id="print-two-tags",
            text="Below the function, print two tags: call `name_tag` inside `print(...)`, two times, with any names "
                 "and hours.",
            dictated=False,
            hints=[
                "Below the function, lined up with `def`. Nothing prints yet: `name_tag` only hands the tag back.",
                "A call inside `print(...)` runs first, and `print` shows what it hands back: "
                "`print(label(\"rope\", 5))` shows `ROPE - 5 gold`.",
                "Write `print(name_tag(\"Lucky\", 48))` below the function. Then one more line like it, with another "
                "name and number.",
            ],
            checks=[check("two tags are printed, each made by name_tag", _TAGB_SHOWN)],
            pass_line="Mar'tu: From a blank page. Every tag built, not one typed.",
        ),
    ],
    solution=TAGB_SOLUTION,
    partials=[_tagb(prints="")],
    assemble=dict(
        lines=code_lines(TAGB_SOLUTION),
        distractors=["    caps = name.upper", '    return "{caps}: {hours} hrs"', '    print(f"{caps}: {hours} hrs")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One tag, piece by piece",
            text=(
                "```text\nname_tag(\"Lucky\", 48)\n\ncaps = \"LUCKY\"\nhours = 48\n\n"
                "f\"{caps}: {hours} hrs\"\n -> \"LUCKY: 48 hrs\"\n```\n"
                "Each `{...}` is a gap that the value fills. Everything else in the quotes stays as you typed it."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The `def` line: `name_tag`, then `name` and `hours`.\n"
                "2. `caps = name.upper()` keeps the capitals copy.\n"
                "3. One f-string: `{caps}`, a colon and a space, `{hours}`, then ` hrs`.\n"
                "4. `return` hands the tag back.\n"
                "5. Below, lined up with `def`: two `print(name_tag(...))` lines."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The mana bars glued their line with `+` and `str()`. An f-string does the same job in one piece: "
                "`f\"{caps}: {hours} hrs\"` is `caps + \": \" + str(hours) + \" hrs\"`, with no `str()` to forget."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE_2,
        part="mana-bars",
        why=(
            "Every mana bar in the campaign started with the hero's name and glued a number on with `+ str()`. Your "
            "tag is the same idea, written as an f-string, and built for any name."
        ),
    ),
    takeaway="`.upper()` for the capitals, an f-string for the glue: build the tag from the values, never type it.",
    wrong_answers=[
        dict(why="the starter (only the comment)", code=TAGB_STARTER, fails_at=1,
             message_contains="Write `name_tag` with `def`"),
        dict(why="the prints written before the function (NameError)", code=_tagb(body=None), fails_at=0,
             message_contains="name 'name_tag' is not defined"),
        dict(why="print in place of return (RET)",
             code=_tagb(TAGB_BODY.replace('return f"', 'print(f"').replace('hrs"\n', 'hrs")\n')), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the parameters renamed (who, hrs)",
             code=_tagb('    return f"{who.upper()}: {hrs} hrs"\n', sig="def name_tag(who, hrs):\n"), fails_at=1,
             message_contains="Name the parameters `name` and `hours`"),
        dict(why="a near-miss parameter (names): named, letter for letter",
             code=_tagb(TAGB_BODY.replace("name.upper", "names.upper"), sig="def name_tag(names, hours):\n"),
             fails_at=1, message_contains="you wrote `names`"),
        dict(why="no f before the quote (the braces come back as they are)",
             code=_tagb(TAGB_BODY.replace('return f"', 'return "')), fails_at=1,
             message_contains="`f` right in front"),
        dict(why=".upper with no () (the method itself goes in the tag)",
             code=_tagb(TAGB_BODY.replace("name.upper()", "name.upper")), fails_at=1,
             message_contains="Add `()` after `upper`"),
        dict(why="the tag typed by hand (the same for every name)",
             code=_tagb('    return "LUCKY: 48 hrs"\n'), fails_at=1, message_contains="typed by hand"),
        dict(why="the + str() way: it works, and this challenge practices the f-string",
             code=_tagb('    caps = name.upper()\n    return caps + ": " + str(hours) + " hrs"\n'), fails_at=1,
             message_contains="This challenge practices the f-string"),
        dict(why="no .upper(): the name keeps its own capitals",
             code=_tagb('    return f"{name}: {hours} hrs"\n'), fails_at=1, message_contains="capitals with `.upper()`"),
        dict(why=".upper() on the whole tag (HRS in capitals too)",
             code=_tagb('    return f"{name}: {hours} hrs".upper()\n'), fails_at=1, message_contains="name only"),
        dict(why="the hrs left off", code=_tagb('    caps = name.upper()\n    return f"{caps}: {hours}"\n'), fails_at=1,
             message_contains="End the tag with a space and `hrs`"),
        dict(why="+ between text and a number, no str(), the prints taken out (the check's call meets it)",
             code=_tagb('    return name.upper() + ": " + hours + " hrs"\n', prints=""), fails_at=1,
             message_contains="Put the hours in the f-string"),
        dict(why="a near-miss parameter in the f-string (hour), the prints taken out: _why names the parameter",
             code=_tagb(TAGB_BODY.replace("{hours}", "{hour}"), prints=""), fails_at=1,
             message_contains="Inside `name_tag`, Python stopped: NameError: name 'hour' is not defined. You wrote "
                              "`hour`, and the parameter is `hours`."),
        dict(why="the hints' example name (item) used, the prints taken out: _why says where it came from",
             code=_tagb(TAGB_BODY.replace("name.upper()", "item.upper()"), prints=""), fails_at=1,
             message_contains="`item` comes from Mar'tu's example. The parameters of `name_tag` are `name` and "
                              "`hours`."),
        dict(why="a brace left open (SyntaxError)", code=_tagb(TAGB_BODY.replace("{caps}", "{caps")), fails_at=0,
             message_contains="f-string: expecting '}'"),
        dict(why="the function only, nothing printed", code=_tagb(prints=""), fails_at=2,
             message_contains="Print two tags below the function"),
        dict(why="one tag printed", code=_tagb(prints='print(name_tag("Lucky", 48))\n'), fails_at=2,
             message_contains="Print a second tag"),
        dict(why="the tags typed into the prints by hand",
             code=_tagb(prints='print("LUCKY: 48 hrs")\nprint("OOGRISH: 311 hrs")\n'), fails_at=2,
             message_contains="typed by hand"),
        dict(why="the calls made, not printed (the tags thrown away)",
             code=_tagb(prints='name_tag("Lucky", 48)\nname_tag("Oogrish", 311)\n'), fails_at=2,
             message_contains="thrown away"),
        dict(why="print(name_tag) with no brackets (the function itself)",
             code=_tagb(prints="print(name_tag)\nprint(name_tag)\n"), fails_at=2, message_contains="function itself"),
        dict(why="the prints indented into the function, under return (they never run)",
             code=_tagb(TAGB_BODY + '    print(name_tag("Lucky", 48))\n    print(name_tag("Oogrish", 311))\n',
                        prints=""), fails_at=2, message_contains="out of the function"),
        dict(why="the values handed over the wrong way round (a number has no .upper())",
             code=_tagb(prints='print(name_tag(48, "Lucky"))\nprint(name_tag(311, "Oogrish"))\n'), fails_at=0,
             message_contains="'int' object has no attribute 'upper'"),
    ],
    notes=(
        meta(starter_level="S0", path="optional", skills="string-methods,fstring-read,func-make", solo="false",
             dictates="", foreign_names=",".join(TAGB_FOREIGN),
             par="name_tag ('Pell', 7) -> 'PELL: 7 hrs', ('moss', 12) -> 'MOSS: 12 hrs'") + "\n"
        "Optional advanced challenge for the ready-to-stretch group (teacher's revision: a write-from-blank task as "
        "Units 3 to 7 have; 10 min, costs no one core time), after 8P2, modelled on u07b's spell-book-from-blank. "
        "The starter is one comment line. CP1 [ND] has two checks: PAR/RET on two fresh calls (`Pell`, 7 and "
        "`moss`, 12: a capital already there, and one to make; never the hints' Lucky or 48, lint b), with the "
        "parameter names checked exactly (`_need_def`: a near miss like `names` is named), then the tools: an "
        "f-string (JoinedStr) and a `.upper()` call inside `name_tag`. A working `+ str()` line gets the kind "
        "'this challenge practices the f-string' message (objective 6: students read `+ str()` lines; this task "
        "asks for the f-string). Slips named: print for return, no `f` (the braces come back), `.upper` with no "
        "`()`, a typed tag (both calls give the same), `.upper()` on the whole tag (`HRS`), no capitals, no hours, "
        "no `hrs`, and `+` with a number (TypeError) caught by name. Other crashes inside the function during the "
        "check's calls get _why() (the hints' names `label`, `item`, `cost`; a near-miss parameter, `hour`). CP2 "
        "[ND] needs two `print(...)` calls at the top level that hold a `name_tag` call (or a variable made from "
        "one), or one inside a loop that prints two lines; any names and hours pass. Named: prints indented into "
        "the function, a call not printed, `print(name_tag)`, tags typed into the prints. No Show me line holds "
        "more than two lines; every solution line is 36 characters or fewer."
    ),
)


ITEMS = [EXTRA_9X, QUIZ_8A, PROJECT_8P1, PROJECT_8P2, TAG_FROM_BLANK]
