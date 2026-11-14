"""Prototype verifier for the Intro to Python units.

Every unit lives in a file named ``uNN_<slug>.py`` beside this one. A big unit may be split into parts
``uNNa_<slug>.py``, ``uNNb_<slug>.py`` ... (each part repeats the UNIT dict); files run in prefix order. Run:

    python3 docs/intro-to-python/prototypes/harness.py            # all units
    python3 docs/intro-to-python/prototypes/harness.py u03         # units whose file name starts with u03
    python3 docs/intro-to-python/prototypes/harness.py --json out.json

It checks, for every exercise / project / challenge / test-out item:
  * the solution passes every checkpoint,
  * the starter code fails at least one checkpoint (unless ``starter_passes=True``),
  * each staged partial solution passes checkpoints 1..k and fails k+1,
  * each known wrong answer fails at the checkpoint it names (and with the message it names),
  * the worked example prints exactly ``example_output``,
  * the bonus side quest passes with its own solution,
  * the "Assemble it" lines (``assemble=dict(lines=[...], distractors=[...])``), put in the editor on their
    own exactly as the player does, pass every checkpoint (and a WARNING when a line like ``row = 60`` is the
    only number a goal-only step accepts, as in a trace ledger: More structure would hand the answer over),
  * no code a student SEES (starter, solution, example, partials, quiz code) uses a concept that has not been
    introduced yet, in course order (see CONCEPT TOKENS below),
  * every checkpoint has a hint ladder of at least two hints,
  * an exercise ``predict`` has 2+ choices, an explanation, and an answer that IS what its code prints,
  * the exercise fields ``names`` (every name is used by the solution), ``pick``, ``pair_talk``, ``solo`` and
    ``explainer`` ("full" or "lean"), and the checkpoint field ``dictated``, have the right types,
and for quizzes, it EXECUTES predict / fill / parsons / bug questions to prove the keyed answer is right.

It also reports reading load (word count and a Flesch-Kincaid grade estimate) for Mar'tu's text and the
checkpoint instructions, so the novice-facing text can be kept short and plain.

Unit file format (plain Python data, no imports needed):

    UNIT = dict(id="lists", order=3, title="Lists", martu_intro="...", goals=[...], campaign_links=[...])
    ITEMS = [
        dict(kind="lesson", id="...", title="...", exercises=[EXERCISE, ...]),
        dict(kind="quiz", id="...", title="...", questions=[QUESTION, ...]),
        dict(kind="project", id="...", title="...", **EXERCISE_FIELDS),         # checkpoints = project tasks
        dict(kind="challenge", id="...", title="...", level="core"|"advanced", **EXERCISE_FIELDS),
        dict(kind="testout", id="...", title="...", exercises=[EXERCISE, ...]),  # pass all => unit complete
             # optional questions_to_pass=3: the quiz "<id>-questions" must have 3 right too
        dict(kind="article", id="...", title="...", body="...", examples=[dict(code=..., output=..., stdin=[...])],
             exercises=[...optional try-it EXERCISEs...]),
        dict(kind="cheatsheet", id="...", title="...", entries=[dict(concept=..., code=..., output=..., note=...)]),
    ]

    (The site cannot run article examples with ``setup``, or cheatsheet entries with ``setup``/``stdin``:
    this verifier would accept them, but scripts/course/export_prototypes.py rejects them.)

    EXERCISE = dict(
        id="lists-create", title="Make a list",
        martu="Mar'tu's explanation (the Learn pane).",
        example="code shown to the student", example_output="what it prints",
        another_way=[dict(angle="analogy", text="..."), dict(angle="step by step", text="...")],
        introduces=["node:List"],          # concept tokens this exercise teaches (see below)
        preview=[],                         # tokens deliberately shown before they are taught (justify in notes)
        setup="",                           # hidden code run before the student's code
        stdin=["Oogrish"],                  # answers fed to input(), in order
        starter="...",
        checkpoints=[dict(text="1. ...", hints=["nudge", "more specific", "nearly the answer"],
                          checks=[("check name", "assert ..., 'student-facing message'")],
                          dictated=True)],     # True: the text spells out the code; False: goal and names only
        solution="...",
        partials=["code after checkpoint 1", ...],     # optional, len < len(checkpoints)
        wrong_answers=[dict(why="hard-codes 68", code="...", fails_at=1, message_contains="variable")],
        starter_passes=False,
        engine=False,                        # True: also load the campaign objects (party, print_prompt, ...)
        tracer=True,                         # offer the step-through tracer on this exercise
        bonus=dict(text="Lucky's side quest ...", checks=[...], solution="..."),
        assemble=dict(lines=["first line", "second line"], distractors=["a wrong line"]),
        predict=dict(q="What will this print?", code="...optional, defaults to the starter...",
                     choices=["right output", "a likely wrong one"], answer=0, explain="..."),   # Predict before Run
        names=["caster", "mana"],          # "Names to use" chips: the exact names the steps ask for
        pick='"Gearshift"',                 # Mar'tu's pick: a value to use when the student can't decide
        pair_talk="Tell your partner ...",  # an optional Pair talk prompt (every step is still done solo)
        solo=False,                         # True for the lesson's SOLO item, done alone
        explainer="full",                   # "lean": the crash explainer names the slip and the line, not the fix
        notes="designer notes (not shown to students)",
    )

    QUESTION kinds:
        dict(type="mc", q="...", code=None, choices=[...], answer=1, explain="...", why_wrong={0: "..."})
        dict(type="predict", q="What prints?", code="...", answer="exact output", choices=[...optional...], explain="...")
        dict(type="fill", q="...", code="... ___ ...", answer="len", accept=["len"], expected_output="...", explain="...")
        dict(type="parsons", q="...", lines=["correct", "order"], distractors=["..."], expected_output="...", explain="...")
        dict(type="bug", q="...", code="buggy", fix="fixed", expected_output="...", explain="...")

Code runs exactly like a course run on the site, because every host executes the same file,
public/workers/course_helpers.py: a fresh namespace, the import guard, the check helpers and the input() shim,
the campaign objects (party, user, stage, print_prompt, ...) only when the exercise sets engine=True, then
setup, then the student's code. Checks run after the student's code in the same namespace. Besides everything
the student defined, a check can use:
    _captured_stdout     everything printed
    _lines()             printed lines, stripped, blanks removed
    _source              the student's code as text
    _uses(token)         True if the student's code contains a concept token, e.g. _uses("node:For")
    _count(token)        how many times a concept token appears
    _assigned_from_expression(name)  True if `name` is assigned from something other than a plain literal
    _inputs_used()       how many input() answers were consumed

CONCEPT TOKENS (produced by ``concept_tokens``):
    node:Assign node:AugAssign node:If node:For node:While node:Break node:Continue node:FunctionDef node:Return
    node:Lambda node:List node:Tuple node:Dict node:Set node:Subscript node:Slice node:ListComp node:DictComp
    node:FString node:Import node:Match node:Try node:Pass node:KeywordArg node:DefaultArg node:IfExp node:Global
    node:Starred node:Assert node:With node:Class
    op:Add op:Sub op:Mult op:Div op:FloorDiv op:Mod op:Pow op:Eq op:NotEq op:Lt op:LtE op:Gt op:GtE op:In op:NotIn
    op:Is op:IsNot op:And op:Or op:Not op:USub
    const:str const:int const:float const:bool const:None const:multiline_str const:escape (\\n, \\t, \\" ...)
    call:<builtin>   e.g. call:print call:len call:range call:input call:str call:int call:sorted call:zip call:map
    attr:<name>      e.g. attr:append attr:lower attr:randint (attributes on engine objects like party.move are exempt)
    import:<module>  e.g. import:random
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
WORKER = REPO / "public" / "workers" / "python-worker.js"
HELPERS = REPO / "public" / "workers" / "course_helpers.py"
TIMEOUT_SECONDS = 6

BASE_TOKENS = {"node:Module", "node:Expr", "node:Name", "node:Call"}


def worker_prelude() -> str:
    """The campaign GUARD from python-worker.js (loaded only for engine=True exercises)."""
    text = WORKER.read_text(encoding="utf8")
    match = re.search(r"const GUARD = `([\s\S]*?)`;", text)
    if not match:
        raise SystemExit("python-worker.js has no GUARD prelude")
    return match.group(1)


PRELUDE = worker_prelude()
PRELUDE_NAMES = {
    node.name if isinstance(node, (ast.FunctionDef, ast.ClassDef)) else getattr(node.targets[0], "id", "")
    for node in ast.parse(PRELUDE).body
    if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    or (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name))
}

# ---------------------------------------------------------------------------------------------
# Concept tokens: the tokenizer lives in course_helpers.py, so the concept gate, the checks' _uses(),
# and the browser all share one copy. Loading it as "course_helpers" skips its import guard.
# ---------------------------------------------------------------------------------------------

HELPERS_SOURCE = HELPERS.read_text(encoding="utf8")
_HELPERS: dict = {"__name__": "course_helpers"}
exec(compile(HELPERS_SOURCE, str(HELPERS), "exec"), _HELPERS)


def concept_tokens(code: str, exempt_names: set[str] | None = None) -> list[str]:
    """Every concept token in ``code``, with repeats (so callers can count)."""
    return _HELPERS["_concept_tokens"](code, exempt_names)


def _check_helpers_match_guard() -> None:
    # The tokenizer exempts attributes on the campaign objects; its list must match GUARD.
    if set(_HELPERS["_COURSE_CAMPAIGN_NAMES"]) != PRELUDE_NAMES:
        raise SystemExit(
            "_COURSE_CAMPAIGN_NAMES in course_helpers.py is out of date with GUARD in python-worker.js; "
            f"set it to {sorted(PRELUDE_NAMES)}"
        )


_check_helpers_match_guard()

# ---------------------------------------------------------------------------------------------
# Running code exactly like the site does (course_helpers.py, GUARD when engine=True, setup, code, checks)
# ---------------------------------------------------------------------------------------------

RESULT_MARKER = "\n@@course-run-result@@\n"

RUNNER = r"""
import json, sys
payload = json.loads(sys.stdin.read())
ns = {"__name__": "__main__"}
events = []
if payload["engine"]:
    for name in ["_stage_say", "_stage_flare", "_stage_focus", "_stage_move", "_stage_prompt", "_stage_options",
                 "_stage_speak", "_stage_highlight", "_stage_cast", "_stage_mana", "_stage_roll"]:
        ns[name] = (lambda n: (lambda *a: events.append([n] + [str(x) for x in a])))(name)
    ns["_stage_option"] = lambda *a: None
exec(compile(payload["helpers"], "course_helpers.py", "exec"), ns)
if payload["engine"]:
    exec(compile(payload["prelude"], "<guard>", "exec"), ns)
flat = [{"name": name, "code": code} for group in payload["checkpoints"] for name, code in group]
result = ns["_course_run"](payload["code"], payload["setup"], flat, payload["stdin"])
rows, at = [], 0
if result["ok"]:
    for group in payload["checkpoints"]:
        row = []
        for _ in group:
            check = result["checks"][at]
            at += 1
            row.append([check["name"], check["passed"], check["message"]])
        rows.append(row)
sys.__stdout__.write(payload["marker"] + json.dumps({
    "ok": result["ok"], "error": result["error"], "traceback": result["traceback"],
    "stdout": result["stdout"], "checkpoints": rows,
}))
"""


def normalize_checks(checks) -> list[list[str]]:
    out = []
    for check in checks or []:
        if isinstance(check, dict):
            out.append([check["name"], check["code"]])
        else:
            name, code = check
            out.append([name, code])
    return out


def run(code: str, checkpoints: list, setup: str = "", stdin: list | None = None, engine: bool = False) -> dict:
    payload = {
        "helpers": HELPERS_SOURCE,
        "prelude": PRELUDE if engine else "",
        "engine": bool(engine),
        "setup": setup or "",
        "code": code,
        "stdin": list(stdin or []),
        "checkpoints": [normalize_checks(cp.get("checks")) for cp in checkpoints],
        "marker": RESULT_MARKER,
    }
    try:
        child = subprocess.run(
            [sys.executable, "-I", "-c", RUNNER],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timeout: the code ran too long (infinite loop?)", "traceback": "",
                "stdout": "", "checkpoints": []}
    at = child.stdout.rfind(RESULT_MARKER)
    if child.returncode != 0 or at < 0:
        return {"ok": False, "error": (child.stderr or child.stdout).strip()[-800:], "traceback": "",
                "stdout": "", "checkpoints": []}
    return json.loads(child.stdout[at + len(RESULT_MARKER):])


def checkpoint_status(result: dict, count: int) -> list[bool]:
    if not result["ok"]:
        return [False] * count
    return [all(passed for _, passed, _ in row) for row in result["checkpoints"]]


def first_failure(result: dict) -> tuple[int | None, str]:
    if not result["ok"]:
        return 0, result["error"]
    for index, row in enumerate(result["checkpoints"]):
        for _, passed, message in row:
            if not passed:
                return index + 1, message
    return None, ""


# ---------------------------------------------------------------------------------------------
# Reading load
# ---------------------------------------------------------------------------------------------

def _syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1 and not word.endswith("le"):
        count -= 1
    return max(1, count)


def reading_stats(text: str) -> tuple[int, float]:
    plain = re.sub(r"`[^`]*`", " code ", text or "")
    words = re.findall(r"[A-Za-z']+", plain)
    if not words:
        return 0, 0.0
    sentences = max(1, len(re.findall(r"[.!?]+(\s|$)", plain)))
    syllables = sum(_syllables(w) for w in words)
    grade = 0.39 * (len(words) / sentences) + 11.8 * (syllables / len(words)) - 15.59
    return len(words), round(grade, 1)


# ---------------------------------------------------------------------------------------------
# Verifying units
# ---------------------------------------------------------------------------------------------

class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict = {"units": [], "exercises": 0, "checkpoints": 0, "questions": 0, "wrong_answers": 0}

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def load_unit(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module.UNIT, module.ITEMS


class ConceptGate:
    def __init__(self) -> None:
        self.allowed = set(BASE_TOKENS)
        self.introduced_at: dict[str, str] = {}

    def introduce(self, tokens, where: str) -> None:
        for token in tokens or []:
            if token not in self.allowed:
                self.allowed.add(token)
                self.introduced_at[token] = where

    def check(self, report: Report, where: str, label: str, code: str | None, preview=(), exempt=()) -> None:
        if not code or not code.strip():
            return
        try:
            tokens = set(concept_tokens(code, set(exempt)))
        except SyntaxError as exc:
            if "___" in code:  # fill-in-the-blank code is allowed to be incomplete
                return
            if label == "starter":  # starters may contain deliberate placeholders like <option>
                report.warn(where, f"starter is not valid Python yet ({exc.msg}); make sure that is intended")
                return
            report.error(where, f"{label} is not valid Python: {exc}")
            return
        unknown = sorted(tokens - self.allowed - set(preview or ()))
        if unknown:
            report.error(where, f"{label} uses concepts not introduced yet: {', '.join(unknown)}")


def defined_names(setup: str) -> set[str]:
    if not setup:
        return set()
    names = set()
    for node in ast.walk(ast.parse(setup)):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return names


def solution_names(code: str) -> set[str]:
    """Every name a piece of code uses or makes: variables, functions, parameters, attributes."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Name):
            found.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found.add(node.name)
        elif isinstance(node, ast.arg):
            found.add(node.arg)
        elif isinstance(node, ast.Attribute):
            found.add(node.attr)
    return found


def verify_exercise(ex: dict, where: str, gate: ConceptGate, report: Report, kind: str = "exercise") -> None:
    report.stats["exercises"] += 1
    checkpoints = ex.get("checkpoints") or []
    report.stats["checkpoints"] += len(checkpoints)
    setup = ex.get("setup", "")
    stdin = ex.get("stdin", [])
    engine = bool(ex.get("engine", False))
    exempt = defined_names(setup)
    for field in ("id", "title", "starter", "solution"):
        if field not in ex:
            report.error(where, f"missing field {field!r}")
            return
    if kind in ("exercise",) and not ex.get("martu"):
        report.error(where, "exercise has no Mar'tu explanation (martu)")
    if not checkpoints:
        report.error(where, "no checkpoints")
        return
    gate.introduce(ex.get("introduces"), where)
    preview = ex.get("preview", [])
    for label in ("starter", "solution", "example"):
        gate.check(report, where, label, ex.get(label), preview, exempt)
    for i, partial in enumerate(ex.get("partials") or []):
        gate.check(report, where, f"partial {i + 1}", partial, preview, exempt)

    for i, cp in enumerate(checkpoints, 1):
        if not cp.get("checks"):
            report.error(where, f"checkpoint {i} has no checks")
        hints = cp.get("hints") or []
        if len(hints) < 2:
            report.error(where, f"checkpoint {i} needs a hint ladder of at least 2 hints (has {len(hints)})")
        names = [name for name, _ in normalize_checks(cp.get("checks"))]
        if len(names) != len(set(names)):
            report.error(where, f"checkpoint {i} has two checks with the same name (the site tells them apart by name)")
        if "dictated" in cp and not isinstance(cp["dictated"], bool):
            report.error(where, f"checkpoint {i} dictated must be True or False")
        words, grade = reading_stats(cp.get("text", ""))
        if grade > 9:
            report.warn(where, f"checkpoint {i} text reads at grade {grade}")

    words, grade = reading_stats(ex.get("martu", ""))
    if words > 230:
        report.warn(where, f"Mar'tu's explanation is long ({words} words)")
    if grade > 9:
        report.warn(where, f"Mar'tu's explanation reads at grade {grade}")

    solution = run(ex["solution"], checkpoints, setup, stdin, engine)
    status = checkpoint_status(solution, len(checkpoints))
    if not all(status):
        index, message = first_failure(solution)
        report.error(where, f"solution fails at checkpoint {index}: {message}")

    starter = run(ex["starter"], checkpoints, setup, stdin, engine)
    starter_status = checkpoint_status(starter, len(checkpoints))
    if ex.get("starter_passes"):
        if not all(starter_status):
            report.error(where, f"starter_passes=True but starter fails: {first_failure(starter)}")
    elif all(starter_status):
        report.error(where, "starter code already passes every checkpoint")

    for k, partial in enumerate(ex.get("partials") or [], 1):
        result = run(partial, checkpoints, setup, stdin, engine)
        st = checkpoint_status(result, len(checkpoints))
        if not all(st[:k]):
            report.error(where, f"partial {k} should pass checkpoints 1..{k} but got {st} ({first_failure(result)[1]})")
        if k < len(checkpoints) and st[k]:
            report.error(where, f"partial {k} unexpectedly passes checkpoint {k + 1}")

    for wrong in ex.get("wrong_answers") or []:
        report.stats["wrong_answers"] += 1
        result = run(wrong["code"], checkpoints, setup, stdin, engine)
        index, message = first_failure(result)
        label = f"wrong answer ({wrong.get('why', '?')})"
        if index is None:
            report.error(where, f"{label} PASSES every checkpoint — the checks are too loose")
            continue
        expected = wrong.get("fails_at")
        if expected is not None and expected != index:
            report.error(where, f"{label} fails at checkpoint {index}, expected {expected}: {message}")
        needle = wrong.get("message_contains")
        if needle and needle.lower() not in message.lower():
            report.error(where, f"{label} message {message!r} does not mention {needle!r}")

    if ex.get("example") and "example_output" in ex:
        result = run(ex["example"], [], setup, stdin, engine)
        if not result["ok"]:
            report.error(where, f"example crashes: {result['error']}")
        elif result["stdout"].rstrip() != str(ex["example_output"]).rstrip():
            report.error(where, f"example prints {result['stdout']!r}, example_output says {ex['example_output']!r}")

    # predict = dict(q=..., code=<optional, defaults to the starter>, choices=[...], answer=<index or exact text>, explain=...)
    predict = ex.get("predict")
    if predict:
        if not predict.get("explain"):
            report.error(where, "predict has no explanation (explain)")
        p_code = predict.get("code") or ex["starter"]
        gate.check(report, where, "predict code", p_code, preview, exempt)
        answer = predict.get("answer")
        choices = predict.get("choices") or []
        if len(choices) < 2:
            report.error(where, "predict needs at least 2 choices (the site shows a one-click choice)")
        elif isinstance(answer, str) and answer not in choices:
            report.error(where, f"predict answer {answer!r} is not one of the choices")
        if isinstance(answer, int):
            if not (0 <= answer < len(choices)):
                report.error(where, "predict answer index out of range")
                answer = None
            else:
                answer = choices[answer]
        if answer is not None:
            result = run(p_code, [], setup, stdin, engine)
            actual = _norm(result["stdout"]) if result["ok"] else f"ERROR: {result['error']}"
            if _norm(str(answer)) != actual and not (str(answer).startswith("ERROR") and actual.startswith("ERROR")):
                report.error(where, f"predict answer {answer!r} but the code prints {actual!r}")

    names = ex.get("names")
    if names is not None and not (isinstance(names, (list, tuple)) and all(isinstance(n, str) and n for n in names)):
        report.error(where, "names must be a list of strings")
    elif names:
        # "Names to use" chips must be names the solution really uses (a typo there teaches the typo).
        try:
            used = solution_names(ex["solution"])
        except SyntaxError:
            used = None
        for name in names if used is not None else []:
            if name not in used:
                report.warn(where, f"names lists {name!r}, but the solution never uses it")
    for field in ("pick", "pair_talk"):
        if field in ex and not (isinstance(ex[field], str) and ex[field].strip()):
            report.error(where, f"{field} must be text")
    if "solo" in ex and not isinstance(ex["solo"], bool):
        report.error(where, "solo must be True or False")
    if "explainer" in ex and ex["explainer"] not in ("full", "lean"):
        report.error(where, "explainer must be \"full\" or \"lean\"")

    bonus = ex.get("bonus")
    if bonus:
        bonus_cp = [{"checks": bonus.get("checks")}]
        result = run(bonus.get("solution", ""), bonus_cp, setup, stdin, engine)
        if not all(checkpoint_status(result, 1)):
            report.error(where, f"bonus solution fails: {first_failure(result)[1]}")
        base = run(ex["solution"], bonus_cp, setup, stdin, engine)
        if all(checkpoint_status(base, 1)):
            report.warn(where, "the plain solution already passes the bonus checks")

    assemble = ex.get("assemble")
    if assemble:
        lines = list(assemble.get("lines") or [])
        if len(lines) < 2:
            report.error(where, f"assemble needs at least 2 lines (has {len(lines)})")
        else:
            # The player puts exactly these lines in the editor (starter comments are dropped).
            code = "\n".join(lines) + "\n"
            gate.check(report, where, "assemble", code, preview, exempt)
            result = run(code, checkpoints, setup, stdin, engine)
            if not all(checkpoint_status(result, len(checkpoints))):
                index, message = first_failure(result)
                report.error(where, f"assemble lines fail at checkpoint {index}: {message}")
            else:
                assemble_giveaways(ex, lines, where, report)
        for distractor in assemble.get("distractors") or []:
            if distractor in lines:
                report.error(where, f"assemble distractor {distractor!r} is also one of the right lines")


def assemble_giveaways(ex: dict, lines: list, where: str, report: Report) -> None:
    """A warning, never an error: an Assemble line `row = 60` that pins the number a goal-only step (dictated=False)
    asks the student to work out, like a trace row. Any other number there fails that step, so "More structure"
    hands over the answer before "Show me how" does. (Assemble shows the lines as they are.)"""
    checkpoints = ex.get("checkpoints") or []
    goal_only = [i for i, cp in enumerate(checkpoints) if cp.get("dictated") is False]
    if not goal_only:
        return
    # What the student reads before Show me how: Mar'tu, the steps, every hint but the last, the starter, the example.
    shown = "\n".join(str(part) for part in [
        ex.get("martu"), ex.get("starter"), ex.get("example"), ex.get("example_output"), ex.get("pick"),
        *[cp.get("text") for cp in checkpoints], *[hint for cp in checkpoints for hint in (cp.get("hints") or [])[:-1]],
    ] if part)
    for at, line in enumerate(lines):
        row = re.fullmatch(r"(\s*([A-Za-z_]\w*)\s*=\s*)(-?\d+)\s*", line)
        # A number the task already shows (`3 torches`, a Broken spell's `def hours_left = 37`) gives nothing away:
        # only a number the student has to work out (a trace row's 30) does.
        if not row or re.search(rf"(?<![\w.]){re.escape(row.group(3))}(?!\w|\.\d)", shown):
            continue
        changed = list(lines)
        changed[at] = f"{row.group(1)}{int(row.group(3)) + 1}"
        result = run("\n".join(changed) + "\n", checkpoints, ex.get("setup", ""), ex.get("stdin", []),
                     bool(ex.get("engine", False)))
        status = checkpoint_status(result, len(checkpoints))
        if result["ok"] and any(not status[i] for i in goal_only):
            report.warn(where, f"assemble line {line.strip()!r} is the answer to a goal-only step (any other number "
                               "fails it): More structure would hand it over. Leave assemble out of this exercise")


def _norm(text: str) -> str:
    return "\n".join(line.rstrip() for line in str(text).strip().splitlines())


def verify_question(q: dict, where: str, gate: ConceptGate, report: Report) -> None:
    report.stats["questions"] += 1
    kind = q.get("type")
    if not q.get("explain"):
        report.error(where, "question has no explanation (explain)")
    if kind == "mc":
        if not (0 <= q.get("answer", -1) < len(q.get("choices", []))):
            report.error(where, "mc answer index out of range")
        gate.check(report, where, "question code", q.get("code"))
    elif kind == "predict":
        gate.check(report, where, "question code", q["code"])
        result = run(q["code"], [], q.get("setup", ""), q.get("stdin"), q.get("engine", False))
        actual = _norm(result["stdout"]) if result["ok"] else f"ERROR: {result['error']}"
        if _norm(q["answer"]) != actual and not (str(q["answer"]).startswith("ERROR") and actual.startswith("ERROR")):
            report.error(where, f"predict answer {q['answer']!r} but code prints {actual!r}")
        choices = q.get("choices")
        if choices and _norm(q["answer"]) not in [_norm(c) for c in choices]:
            report.error(where, "predict answer is not among the choices")
    elif kind == "fill":
        gate.check(report, where, "question code", q["code"].replace("___", str(q["answer"])))
        for answer in [q["answer"], *q.get("accept", [])]:
            code = q["code"].replace("___", str(answer))
            result = run(code, [], q.get("setup", ""), q.get("stdin"), q.get("engine", False))
            if not result["ok"] or _norm(result["stdout"]) != _norm(q["expected_output"]):
                report.error(where, f"fill answer {answer!r} gives {result['stdout'] or result['error']!r}")
    elif kind == "parsons":
        code = "\n".join(q["lines"]) + "\n"
        gate.check(report, where, "question code", code)
        result = run(code, [], q.get("setup", ""), q.get("stdin"), q.get("engine", False))
        if not result["ok"] or _norm(result["stdout"]) != _norm(q["expected_output"]):
            report.error(where, f"parsons lines in order give {result['stdout'] or result['error']!r}")
    elif kind == "bug":
        gate.check(report, where, "question fix", q["fix"])
        fixed = run(q["fix"], [], q.get("setup", ""), q.get("stdin"), q.get("engine", False))
        if not fixed["ok"] or _norm(fixed["stdout"]) != _norm(q["expected_output"]):
            report.error(where, f"bug fix gives {fixed['stdout'] or fixed['error']!r}")
        buggy = run(q["code"], [], q.get("setup", ""), q.get("stdin"), q.get("engine", False))
        if buggy["ok"] and _norm(buggy["stdout"]) == _norm(q["expected_output"]):
            report.error(where, "the buggy code already prints the expected output")
    else:
        report.error(where, f"unknown question type {kind!r}")


# Prose fields (FORMAT.md "Prose"): the marks the site renders are `code`, [[links]], *one star* and lists.
PROSE_FIELDS = {"martu_intro", "goals", "summary", "intro", "martu", "text", "label", "hints", "pass_line", "why",
                "takeaway", "q", "explain", "why_wrong", "body", "note", "pair_talk"}
GLOSSARY_LINK = re.compile(r"\[\[[A-Za-z][^\]|]*(?:\|[^\]]*)?\]\]")
EMPHASIS = re.compile(r"(?<![\w*])\*(?=[^\s*])([^*\n]*?[^\s*])\*(?![\w*])")


def prose_mark_problems(text: str) -> list[str]:
    """Marks the site would show as they are: a [[link]] inside `code`, **bold**, *stars* around a code span."""
    plain = re.sub(r"```[\s\S]*?```", " ", text)
    problems = [f"a [[glossary link]] inside `{span}`" for span in re.findall(r"`([^`\n]*)`", plain)
                if GLOSSARY_LINK.search(span)]
    # A link's shown text is plain words or one whole code span ([[len()|`len(wall)`]]); other backticks show the marks.
    for link in re.finditer(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]", plain):
        term, label = link.group(1), link.group(2)
        if "`" in term or (label and "`" in label and not re.fullmatch(r"`[^`\n\]]+`", label)):
            problems.append(f"a [[glossary link]] that mixes code and words: {link.group(0)} (show plain words, or one "
                            "code span)")
    words = re.sub(r"`[^`\n]*`", "CODE", plain)
    if "**" in words:
        problems.append("** (bold is not rendered: use *one star*)")
    problems += [f"*stars* around a code span: {m.group(0)}" for m in EMPHASIS.finditer(words) if "CODE" in m.group(1)]
    return problems


def prose_strings(value, where=""):
    """(where, text) for every prose string in a unit's data (code fields are skipped)."""
    if isinstance(value, list):
        for i, entry in enumerate(value):
            yield from prose_strings(entry, f"{where}[{i}]")
    elif isinstance(value, dict):
        for key, child in value.items():
            at = f"{where}.{key}" if where else str(key)
            if key in PROSE_FIELDS:
                values = child if isinstance(child, list) else list(child.values()) if isinstance(child, dict) else [child]
                for i, text in enumerate(values):
                    if isinstance(text, str):
                        yield at if len(values) == 1 else f"{at}[{i}]", text
            else:
                yield from prose_strings(child, at)


def start_of_line(hints, solution=None) -> str | None:
    """The site's Start me off (exercise-logic.ts startOfLine): the first code span of the last hint, up to and
    including its first `(` or lone `=`, or a list's `[` (`print(chalk_wall[`, `return wall[`) when Mar'tu's
    version uses that. None when there is nothing safe to give."""
    last = hints[-1] if isinstance(hints, (list, tuple)) and len(hints) >= 2 and isinstance(hints[-1], str) else None
    span = re.search(r"`([^`\n]+)`", last or "")
    if not span:
        return None
    text = span.group(1).strip()
    cut = re.match(r"^(.*?)(\(|[+\-*/]?=(?!=))", text)
    if not cut or re.search(r"[=!<>]$", cut.group(1)):
        return None
    base = (cut.group(1) + cut.group(2)).strip()
    bracket = re.match(r"^([^\[]*?[A-Za-z_]\w*\s*\[)[^\]]*$", cut.group(1)) if cut.group(2) == "(" else None
    listed = bracket.group(1).strip() if bracket else None
    if listed is None and base == "print(":
        more = re.match(r"^print\(\s*[A-Za-z_]\w*\s*\[", text)
        listed = more.group(0) if more else None
    squash = lambda value: re.sub(r"\s+", "", value)  # noqa: E731
    used = lambda value: not isinstance(solution, str) or squash(value) in squash(solution)  # noqa: E731
    start = listed if listed and used(listed) else base
    return start if start and start != "(" and len(start) < len(text) else None


_PLACES_FROM_ORDER = {"order": None}


def min_order_for_places(ex: dict) -> bool:
    """The Start me off place warning is on from Unit 5 (the unit being verified sets the order)."""
    order = _PLACES_FROM_ORDER["order"]
    return isinstance(order, int) and order >= 5


def ladder_warnings(ex: dict, where: str, report: Report) -> None:
    """FORMAT.md's hint ladder: point first, the step's own line last (Start me off is cut from it)."""
    ladders = [(f"checkpoint {i}", cp.get("hints") or [], ex.get("solution"))
               for i, cp in enumerate(ex.get("checkpoints") or [], 1)]
    if isinstance(ex.get("bonus"), dict):
        ladders.append(("bonus", ex["bonus"].get("hints") or [], ex["bonus"].get("solution") or ex.get("solution")))
    squash = lambda text: re.sub(r"\s+", "", text)  # noqa: E731
    for label, hints, solution in ladders:
        if hints and isinstance(hints[0], str) and hints[0].startswith("Start like this"):
            report.warn(where, f"{label} hint 1 is a 'Start like this': the site shows hint 1 as Where to look. "
                               "Put the step's own line in the last hint instead (FORMAT.md, checkpoint hints)")
        start = None if ex.get("solo") else start_of_line(hints, solution)
        if start and isinstance(solution, str) and squash(start) not in squash(solution):
            report.warn(where, f"{label}: the last hint's first code span starts `{start}`, which Mar'tu's version "
                               "never uses, so the site drops Start me off. Put the step's own line first in the "
                               "last hint (FORMAT.md, checkpoint hints)")
        # From Unit 5 on: a hint that says where the line goes in words the site cannot read ("Change line 4 to",
        # "under comment 2", "above the `print`") leaves Start me off at the end of the code.
        if start and label != "bonus" and min_order_for_places(ex) and isinstance(hints[-1], str):
            last = hints[-1]
            placed = re.search(r"\b(in place of|on the line after|under|above)\s+(?:the\s+)?`[^`\n]+`", last)
            vague = re.search(r"\b(Change (?:line \d+|the last line) to|[Uu]nder (?:comment \d+|the (?:first|second|last) "
                              r"comment|the comment)|above the `?print`?|below the (?:comments|sheet))", last)
            if vague and not placed:
                report.warn(where, f"{label}: the last hint says where the line goes ({vague.group(0)!r}) in words Start "
                                   "me off cannot read, so it lands at the end of the code. Say it with in place of "
                                   "`...`, under `# N.`, on the line after `...` or above `...` (FORMAT.md, hints)")


def verify_unit(path: Path, gate: ConceptGate, report: Report) -> None:
    unit, items = load_unit(path)
    for at, text in prose_strings({"UNIT": unit, "ITEMS": items}):
        for problem in prose_mark_problems(text):
            report.warn(path.stem, f"{at}: {problem}")
        # An Another way label sits in a button and a pass line in the "Done!" line: `code` shows, a link cannot.
        if re.search(r"\.(label|pass_line)(\[\d+\])?$", at) and GLOSSARY_LINK.search(text):
            report.warn(path.stem, f"{at}: a [[glossary link]] in a label or pass line shows as plain words")
    # A Quick Check form that also needs its questions: the `<id>-questions` quiz must exist and have enough.
    for item in items:
        need = item.get("questions_to_pass")
        if item.get("kind") != "testout" or need is None:
            continue
        quiz = next((q for q in items if q.get("kind") == "quiz" and q.get("id") == f"{item.get('id')}-questions"), None)
        if isinstance(need, bool) or not isinstance(need, int) or need < 1:
            report.error(f"{path.stem}/{item.get('id')}", "questions_to_pass must be a whole number, 1 or more")
        elif quiz is None:
            report.error(f"{path.stem}/{item.get('id')}", f"questions_to_pass needs a quiz with the id {item.get('id')}-questions")
        elif need > len(quiz.get("questions", [])):
            report.error(f"{path.stem}/{item.get('id')}", f"questions_to_pass is {need}, but the quiz has "
                                                          f"{len(quiz.get('questions', []))} questions")
    # Unit 1 predates the ladder rule and is frozen; from Unit 2 on, a 'Start like this' first hint is flagged.
    _PLACES_FROM_ORDER["order"] = unit.get("order")
    if isinstance(unit.get("order"), int) and unit["order"] >= 2:
        for item in items:
            playables = [item] if item.get("kind") in ("project", "challenge") else item.get("exercises", [])
            for ex in playables:
                ladder_warnings(ex, f"{path.stem}/{item.get('id')}" + ("" if ex is item else f"/{ex.get('id')}"), report)
    summary = {"file": path.name, "id": unit.get("id"), "title": unit.get("title"), "items": []}
    for field in ("id", "order", "title", "martu_intro", "goals", "campaign_links"):
        if field not in unit:
            report.error(path.name, f"UNIT missing {field!r}")
    for item in items:
        where = f"{path.stem}/{item.get('id')}"
        kind = item.get("kind")
        summary["items"].append({"kind": kind, "id": item.get("id"), "title": item.get("title")})
        if kind in ("lesson", "testout"):
            for ex in item.get("exercises", []):
                verify_exercise(ex, f"{where}/{ex.get('id')}", gate, report)
        elif kind == "article":
            for example in item.get("examples", []):
                gate.introduce(item.get("introduces"), where)
                gate.check(report, where, "article example", example.get("code"))
                if "output" in example:
                    result = run(example["code"], [], example.get("setup", ""), example.get("stdin"),
                                 example.get("engine", False))
                    if not result["ok"] or _norm(result["stdout"]) != _norm(example["output"]):
                        report.error(where, f"article example prints {result['stdout'] or result['error']!r}")
            for ex in item.get("exercises", []):
                verify_exercise(ex, f"{where}/{ex.get('id')}", gate, report)
        elif kind in ("project", "challenge"):
            verify_exercise(item, where, gate, report, kind=kind)
        elif kind == "quiz":
            for i, q in enumerate(item.get("questions", []), 1):
                verify_question(q, f"{where}/q{i}", gate, report)
        elif kind == "cheatsheet":
            for entry in item.get("entries", []):
                if entry.get("code") and "output" in entry:
                    result = run(entry["code"], [], entry.get("setup", ""), entry.get("stdin"),
                                 entry.get("engine", False))
                    if not result["ok"] or _norm(result["stdout"]) != _norm(entry["output"]):
                        report.error(where, f"cheatsheet {entry.get('concept')} prints {result['stdout'] or result['error']!r}")
        else:
            report.error(where, f"unknown item kind {kind!r}")
    report.stats["units"].append(summary)


def main(argv: list[str]) -> int:
    json_out = None
    if "--json" in argv:
        at = argv.index("--json")
        json_out = argv[at + 1]
        argv = argv[:at] + argv[at + 2:]
    prefixes = argv
    unit_dir = Path(os.environ.get("PROTOTYPE_DIR", HERE))
    files = sorted(unit_dir.glob("u[0-9][0-9]*_*.py"), key=lambda f: f.name.split("_")[0])
    report = Report()
    gate = ConceptGate()
    # When checking only some units, earlier units may not be written yet. concept_map.json (from the
    # curriculum plan) says what each unit WILL introduce: {"units": [{"prefix": "u01", "introduces": [...]}]}.
    plan_path = unit_dir / "concept_map.json"
    if prefixes and plan_path.exists():
        first = min(p.split("_")[0] for p in prefixes)
        for planned in json.loads(plan_path.read_text(encoding="utf8")).get("units", []):
            if planned["prefix"] < first and not first.startswith(planned["prefix"]):
                gate.introduce(planned.get("introduces"), f"{planned['prefix']} (planned)")
    for path in files:
        selected = not prefixes or any(path.name.startswith(p) for p in prefixes)
        if selected:
            verify_unit(path, gate, report)
        else:
            # Earlier units still introduce concepts, so walk them without running anything.
            unit, items = load_unit(path)
            for item in items:
                gate.introduce(item.get("introduces"), path.stem)
                for ex in [item, *item.get("exercises", [])]:
                    gate.introduce(ex.get("introduces"), path.stem)
    for line in report.warnings:
        print("WARN ", line)
    for line in report.errors:
        print("ERROR", line)
    s = report.stats
    print(
        f"\n{len(s['units'])} units, {s['exercises']} exercises/projects/challenges, {s['checkpoints']} checkpoints, "
        f"{s['wrong_answers']} wrong answers, {s['questions']} quiz questions — "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
    )
    if json_out:
        Path(json_out).write_text(json.dumps({"errors": report.errors, "warnings": report.warnings, "stats": s,
                                              "introduced_at": gate.introduced_at}, indent=2))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
