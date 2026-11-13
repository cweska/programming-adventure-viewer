"""Course-run helpers for the Intro to Python course (Mar'tu's lessons).

This file is the single source of truth for how a course run behaves. The same text runs:
  * in the browser, in public/workers/python-worker.js ("course-run" messages, Pyodide's Python 3.13),
  * in tests and tools, in src/lib/course/run-course.ts (CPython 3.12+),
  * in the prototype verifier, docs/intro-to-python/prototypes/harness.py (CPython 3.12+).

Every host runs one course job the same way, in a FRESH namespace each time:

    ns = {"__name__": "__main__"}       # plus the _stage_* callbacks when the engine is on
    exec(<this file>, ns)               # 1. import guard  2. check helpers  3. input() shim  4. runner
    if engine:
        exec(GUARD, ns)                 # campaign objects: party, user, stage, print_prompt, ...
    result = ns["_course_run"](code, setup, checks, stdin)

``_course_run`` feeds ``stdin`` to the input() shim, sets ``_source`` = code, runs ``setup`` and then the
student's code (as "main.py") with stdout captured. If that ran without an exception it sets
``_captured_stdout`` and runs each check in the same namespace. It returns
``{"ok", "stdout", "stderr", "traceback", "error", "checks": [{"name", "passed", "message"}]}``.

Checks can use everything the student defined, plus:
    _captured_stdout     everything printed (prompts and echoed input() answers included)
    _lines()             printed lines, stripped, blanks removed
    _source              the student's code as text
    _uses(token)         True if the student's code contains a concept token, e.g. _uses("node:For")
    _count(token)        how many times a concept token appears
    _assigned_from_expression(name)  True if `name` is assigned from something other than a plain literal
    _inputs_used()       how many input() answers were consumed

Keep this plain standard-library Python that runs on CPython 3.12 and 3.13. Executing it with
``__name__ == "course_helpers"`` (tools that only want the tokenizer) skips the import guard.

The helpers live in the student's namespace, and students name things ``str``, ``len`` and ``type``
(strength, length, spell type). So every helper takes the builtins it needs from the ``builtins``
module inside its factory (closure variables), never from the namespace the student's code changes.
"""

# ---------------------------------------------------------------------------------------------
# 1. Import guard: block the same network modules as the campaign GUARD in python-worker.js.
# ---------------------------------------------------------------------------------------------

_COURSE_BLOCKED_IMPORTS = frozenset({
    "js", "pyodide", "micropip", "urllib", "http", "socket", "ssl",
    "ftplib", "smtplib", "xmlrpc", "webbrowser", "requests", "httpx", "aiohttp",
})


def _course_install_import_guard(blocked):
    import builtins
    import sys
    from builtins import ModuleNotFoundError, getattr

    # The Pyodide worker reuses one interpreter for every run, so wrap the real import only once.
    real = getattr(sys, "_course_real_import", None)
    if real is None:
        real = builtins.__import__
        sys._course_real_import = real

    def _guard(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root in blocked:
            raise ModuleNotFoundError(f"No module named {name!r}")
        return real(name, globals, locals, fromlist, level)

    builtins.__import__ = _guard


if __name__ != "course_helpers":
    _course_install_import_guard(_COURSE_BLOCKED_IMPORTS)
del _course_install_import_guard


# ---------------------------------------------------------------------------------------------
# 2. Concept tokens (copied exactly from harness.py, which now loads it from here) and check helpers.
# ---------------------------------------------------------------------------------------------

# Names the campaign GUARD defines (party, stage, user, ...). Attributes on them are exempt from tokens.
# run-course.test.ts and harness.py fail if this drifts from GUARD in python-worker.js.
_COURSE_CAMPAIGN_NAMES = frozenset({
    "Party", "Stage", "User", "_blocked", "_casts", "_greens", "_guard", "_mana_prints", "_options",
    "_prompts", "_real_import", "_required_roll", "_spoken", "make_option_green", "party", "print_mana",
    "print_options", "print_prompt", "reinforce_barrier", "show_roll", "speak_dialogue", "stage", "user",
})


def _course_make_tokenizer(campaign_names):
    import ast
    import builtins
    import re
    from builtins import any, bool, dir, float, int, isinstance, list, set, str, type

    PRELUDE_NAMES = set(campaign_names)
    BUILTIN_NAMES = set(dir(builtins))

    _NODE_NAMES = {
        ast.Assign: "node:Assign", ast.AugAssign: "node:AugAssign", ast.AnnAssign: "node:Assign",
        ast.If: "node:If", ast.For: "node:For", ast.While: "node:While", ast.Break: "node:Break",
        ast.Continue: "node:Continue", ast.FunctionDef: "node:FunctionDef", ast.Return: "node:Return",
        ast.Lambda: "node:Lambda", ast.List: "node:List", ast.Tuple: "node:Tuple", ast.Dict: "node:Dict",
        ast.Set: "node:Set", ast.Subscript: "node:Subscript", ast.Slice: "node:Slice",
        ast.ListComp: "node:ListComp", ast.DictComp: "node:DictComp", ast.SetComp: "node:ListComp",
        ast.GeneratorExp: "node:ListComp", ast.JoinedStr: "node:FString", ast.Import: "node:Import",
        ast.ImportFrom: "node:Import", ast.Match: "node:Match", ast.Try: "node:Try", ast.Pass: "node:Pass",
        ast.IfExp: "node:IfExp", ast.Global: "node:Global", ast.Nonlocal: "node:Global",
        ast.Starred: "node:Starred", ast.Assert: "node:Assert", ast.With: "node:With", ast.ClassDef: "node:Class",
        ast.Expr: "node:Expr", ast.Module: "node:Module", ast.Name: "node:Name", ast.Call: "node:Call",
        ast.Delete: "node:Delete", ast.Raise: "node:Raise",
    }

    _OP_NAMES = {
        ast.Add: "op:Add", ast.Sub: "op:Sub", ast.Mult: "op:Mult", ast.Div: "op:Div", ast.FloorDiv: "op:FloorDiv",
        ast.Mod: "op:Mod", ast.Pow: "op:Pow", ast.Eq: "op:Eq", ast.NotEq: "op:NotEq", ast.Lt: "op:Lt",
        ast.LtE: "op:LtE", ast.Gt: "op:Gt", ast.GtE: "op:GtE", ast.In: "op:In", ast.NotIn: "op:NotIn",
        ast.Is: "op:Is", ast.IsNot: "op:IsNot", ast.And: "op:And", ast.Or: "op:Or", ast.Not: "op:Not",
        ast.USub: "op:USub", ast.UAdd: "op:USub",
    }

    _ESCAPE = re.compile(r"\\[ntr\\'\"]")

    def concept_tokens(code: str, exempt_names: set[str] | None = None) -> list[str]:
        """Every concept token in ``code``, with repeats (so callers can count)."""
        exempt = set(PRELUDE_NAMES) | set(exempt_names or ())
        tree = ast.parse(code)
        defined = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        found: list[str] = []
        for node in ast.walk(tree):
            kind = type(node)
            if kind in _NODE_NAMES:
                found.append(_NODE_NAMES[kind])
            if isinstance(node, ast.BinOp) or isinstance(node, ast.AugAssign):
                found.append(_OP_NAMES.get(type(node.op), f"op:{type(node.op).__name__}"))
            elif isinstance(node, ast.UnaryOp):
                found.append(_OP_NAMES.get(type(node.op), f"op:{type(node.op).__name__}"))
            elif isinstance(node, ast.BoolOp):
                found.append(_OP_NAMES[type(node.op)])
            elif isinstance(node, ast.Compare):
                found.extend(_OP_NAMES.get(type(op), f"op:{type(op).__name__}") for op in node.ops)
            elif isinstance(node, ast.Constant):
                value = node.value
                if isinstance(value, bool):
                    found.append("const:bool")
                elif value is None:
                    found.append("const:None")
                elif isinstance(value, int):
                    found.append("const:int")
                elif isinstance(value, float):
                    found.append("const:float")
                elif isinstance(value, str):
                    found.append("const:str")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                    if name in BUILTIN_NAMES and name not in exempt and name not in defined:
                        found.append(f"call:{name}")
                if node.keywords:
                    found.append("node:KeywordArg")
            elif isinstance(node, ast.Attribute):
                base = node.value
                while isinstance(base, ast.Attribute):
                    base = base.value
                if isinstance(base, ast.Name) and base.id in exempt:
                    continue
                found.append(f"attr:{node.attr}")
            elif isinstance(node, ast.arguments):
                if node.defaults or node.kw_defaults:
                    found.append("node:DefaultArg")
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                found.extend(f"import:{n.split('.')[0]}" for n in names)
        # string-literal features that the AST hides
        for match in re.finditer(r"(\"\"\"|''')", code):
            found.append("const:multiline_str")
            break
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                segment = ast.get_source_segment(code, node) or ""
                if _ESCAPE.search(segment):
                    found.append("const:escape")
                    break
        return found

    def _lines():
        return [line.strip() for line in _captured_stdout.splitlines() if line.strip()]

    def _uses(token):
        return token in concept_tokens(_source)

    def _count(token):
        return concept_tokens(_source).count(token)

    def _assigned_from_expression(name):
        for node in ast.walk(ast.parse(_source)):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                if not isinstance(node.value, ast.Constant):
                    return True
        return False

    return concept_tokens, _lines, _uses, _count, _assigned_from_expression


_concept_tokens, _lines, _uses, _count, _assigned_from_expression = _course_make_tokenizer(_COURSE_CAMPAIGN_NAMES)
del _course_make_tokenizer


# ---------------------------------------------------------------------------------------------
# 3. input(): answers come from the exercise's scripted stdin, echoed like a terminal would show them.
# ---------------------------------------------------------------------------------------------

def _course_make_input():
    import sys
    from builtins import EOFError, len, list, str

    state = {"answers": [], "used": 0}

    def input(prompt=""):
        sys.stdout.write(str(prompt))
        if state["used"] >= len(state["answers"]):
            raise EOFError("This program asked for more input than it was given.")
        answer = state["answers"][state["used"]]
        state["used"] += 1
        sys.stdout.write(answer + "\n")
        return answer

    def _inputs_used():
        return state["used"]

    def _set_stdin(answers):
        state["answers"] = [str(answer) for answer in (answers or [])]
        state["used"] = 0

    return input, _inputs_used, _set_stdin


input, _inputs_used, _set_stdin = _course_make_input()
del _course_make_input


# ---------------------------------------------------------------------------------------------
# 4. The runner every host calls.
# ---------------------------------------------------------------------------------------------

def _course_make_runner():
    import ast
    import builtins
    import io
    import json
    import linecache
    import re
    import sys
    import traceback
    from builtins import (
        BaseException, Exception, SystemExit, callable, compile, dict, exec, getattr, globals, int, isinstance,
        len, list, str, super, type,
    )

    filename = "main.py"
    # A loop that prints forever fills memory and freezes the console long before the 5 second limit.
    # Stopping at this much output turns the most common endless loop into a quick, explained error.
    output_limit = 200_000

    # A BaseException, so a student's `except Exception:` inside the loop cannot swallow it.
    class TooMuchOutput(BaseException):
        pass

    TooMuchOutput.__qualname__ = "TooMuchOutput"

    class _Capture(io.StringIO):
        def __init__(self):
            super().__init__()
            self.room = output_limit

        def write(self, text):
            if isinstance(text, str):
                self.room -= len(text)
                if self.room < 0:
                    raise TooMuchOutput(f"This program printed more than {output_limit:,} characters, so it was stopped.")
            return super().write(text)

    # Python suggests "Did you mean: '_count'?" for helper names; a student never means those.
    hidden_suggestion = re.compile(r"\. Did you mean: '_[A-Za-z0-9_]*'\?$")

    def _remember_source(code):
        # Lets tracebacks show the student's line (and Python's ^^^^ markers) for "main.py".
        linecache.cache[filename] = (len(code), None, code.splitlines(True), filename)

    def _student_traceback(exc):
        try:
            te = traceback.TracebackException(type(exc), exc, exc.__traceback__, compact=True)
            te.stack = traceback.StackSummary.from_list([frame for frame in te.stack if frame.filename == filename])
            lines = "".join(te.format()).rstrip("\n").split("\n")
        except Exception:  # noqa: BLE001 - never let formatting hide the student's error
            lines = [_check_message(exc)]
        name = getattr(exc, "name", None)
        if not (isinstance(name, str) and name.startswith("_")):
            lines[-1] = hidden_suggestion.sub("", lines[-1])
        last = [line.strip() for line in lines if line.strip()]
        return "\n".join(lines), (last[-1] if last else type(exc).__name__)

    def _check_message(exc):
        kind = getattr(type(exc), "__name__", "Error")
        try:
            text = str(exc)
        except Exception:  # noqa: BLE001 - a broken __str__ must not hide the result
            text = ""
        return f"{kind}: {text}" if text else kind

    def _check_namespace(ns, check_code):
        """The namespace a check runs in: the student's, except for builtins the check only CALLS.

        A student who writes ``len = 10`` hides the builtin ``len`` from a check like
        ``assert len(_lines()) == 2``. When the student's value is not callable and the check uses the
        name only as ``name(...)``, the check gets a copy of the namespace with the builtin put back.
        """
        try:
            tree = ast.parse(check_code)
        except SyntaxError:
            return ns
        uses, calls = {}, {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                uses[node.id] = uses.get(node.id, 0) + 1
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                calls[node.func.id] = calls.get(node.func.id, 0) + 1
        restore = {}
        for name, count in calls.items():
            real = getattr(builtins, name, None)
            if real is None or name not in ns or uses.get(name) != count:
                continue
            value = ns[name]
            if value is not real and not callable(value):
                restore[name] = real
        if not restore:
            return ns
        local = dict(ns)
        local.update(restore)
        return local

    def _course_run(code, setup="", checks=(), stdin=()):
        ns = globals()
        code = str(code or "")
        setup = str(setup or "")
        _set_stdin(list(stdin or []))
        ns["_source"] = code
        out, err = _Capture(), io.StringIO()
        real_out, real_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = out, err
        ok, trace, error, stdout = True, "", "", ""
        results = []
        try:
            try:
                if setup.strip():
                    exec(compile(setup, "<setup>", "exec"), ns)
                _remember_source(code)
                exec(compile(code, filename, "exec"), ns)
            except SystemExit as stop:
                # exit() and quit() end the program, like in a terminal.
                if stop.code is not None and not isinstance(stop.code, int):
                    err.write(f"{stop.code}\n")
            except BaseException as exc:  # noqa: BLE001 - every student error becomes a result
                ok = False
                trace, error = _student_traceback(exc)
            stdout = out.getvalue()
            if ok:
                ns["_captured_stdout"] = stdout
                for check in checks or []:
                    name = "check"
                    try:
                        name = str(check.get("name", "check"))
                        check_code = str(check.get("code", ""))
                        exec(compile(check_code, "<check>", "exec"), _check_namespace(ns, check_code))
                        results.append({"name": name, "passed": True, "message": ""})
                    except BaseException as exc:  # noqa: BLE001
                        results.append({"name": name, "passed": False, "message": _check_message(exc)})
        finally:
            sys.stdout, sys.stderr = real_out, real_err
        return {
            "ok": ok,
            "stdout": stdout,
            "stderr": err.getvalue(),
            "traceback": trace,
            "error": error,
            "checks": results,
        }

    def _course_run_json(payload):
        job = json.loads(payload)
        result = _course_run(job.get("code", ""), job.get("setup", ""), job.get("checks", []), job.get("stdin", []))
        return json.dumps(result)

    return _course_run, _course_run_json


_course_run, _course_run_json = _course_make_runner()
del _course_make_runner
