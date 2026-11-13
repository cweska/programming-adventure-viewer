import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { afterAll, describe, expect, it } from "vitest";
import { workerPrelude } from "../lesson/run-checks";
import { courseHelpersPath, pythonExecutable, runCourseChecks, type CourseRunOptions } from "./run-course";
import type { CourseCheck } from "./schema";

const repo = process.cwd();
const workerPath = path.join(repo, "public/workers/python-worker.js");
const harnessDir = path.join(repo, "docs/intro-to-python/prototypes");
const temp = mkdtempSync(path.join(os.tmpdir(), "course-run-"));

afterAll(() => {
  rmSync(temp, { recursive: true, force: true });
});

function check(name: string, code: string): CourseCheck {
  return { name, code };
}

function python(script: string, input = ""): string {
  const child = spawnSync(pythonExecutable(), ["-I", "-c", script], { input, encoding: "utf8", timeout: 60_000 });
  if (child.status !== 0) throw new Error(child.stderr || child.stdout);
  return child.stdout;
}

describe("runCourseChecks: course-run semantics", () => {
  it("runs the code, captures output, and runs checks in order", () => {
    const result = runCourseChecks('print("Hello, Tor")\n', [
      check("prints", "assert _lines() == ['Hello, Tor'], 'Print exactly Hello, Tor.'"),
      check("raw", "assert _captured_stdout == 'Hello, Tor\\n'"),
      check("wrong", "assert _lines() == ['Bye'], 'Say Bye.'"),
      check("bare", "assert False"),
    ]);
    expect(result.ok).toBe(true);
    expect(result.stdout).toBe("Hello, Tor\n");
    expect(result.traceback).toBe("");
    expect(result.checks).toEqual([
      { name: "prints", passed: true, message: "" },
      { name: "raw", passed: true, message: "" },
      { name: "wrong", passed: false, message: "AssertionError: Say Bye." },
      { name: "bare", passed: false, message: "AssertionError" },
    ]);
  });

  it("gives every check helper from the harness", () => {
    const code = "pizzas = 4\ntotal = pizzas * 12 + 20\nfixed = 68\nfor i in range(2):\n    print(i)\n";
    const result = runCourseChecks(code, [
      check("source", "assert _source == " + JSON.stringify(code)),
      check("uses", "assert _uses('node:For') and _uses('op:Mult') and not _uses('node:While')"),
      check("count", "assert _count('node:Assign') == 3, _count('node:Assign')"),
      check("expression", "assert _assigned_from_expression('total') and not _assigned_from_expression('fixed')"),
      check("lines", "assert _lines() == ['0', '1']"),
      check("tokens", "assert 'call:range' in _concept_tokens(_source)"),
    ]);
    expect(result.checks.filter((c) => !c.passed)).toEqual([]);
  });

  it("feeds input() from stdin and echoes it like a terminal", () => {
    const code = 'name = input("What is your name? ")\nprint("Welcome, " + name)\n';
    const result = runCourseChecks(code, [check("used", "assert _inputs_used() == 1")], { stdin: ["Lucky", "extra"] });
    expect(result.stdout).toBe("What is your name? Lucky\nWelcome, Lucky\n");
    expect(result.checks[0]?.passed).toBe(true);

    const short = runCourseChecks(code, [check("never", "assert True")], { stdin: [] });
    expect(short.ok).toBe(false);
    expect(short.checks).toEqual([]);
    expect(short.stdout).toBe("What is your name? ");
    expect(short.error).toBe("EOFError: This program asked for more input than it was given.");
  });

  it("uses fresh globals with no campaign objects unless the engine is on", () => {
    const plain = runCourseChecks("print(user)\n", []);
    expect(plain.ok).toBe(false);
    expect(plain.error).toBe("NameError: name 'user' is not defined");

    const engine = runCourseChecks(
      'party.move("left")\nprint_prompt("Who goes there?")\n',
      [check("moved", "assert party._moves == ['left']"), check("prompt", "assert _prompts == ['Who goes there?']")],
      { engine: true },
    );
    expect(engine.ok).toBe(true);
    expect(engine.checks.every((c) => c.passed)).toBe(true);
    expect(engine.stageEvents).toEqual([
      { type: "move", direction: "left" },
      { type: "prompt", text: "Who goes there?" },
    ]);
  });

  it("runs setup first, in the same namespace", () => {
    const result = runCourseChecks("print(hero)\n", [check("setup", "assert secret == 7")], {
      setup: 'hero = "Oogrish"\nsecret = 7\n',
    });
    expect(result.stdout).toBe("Oogrish\n");
    expect(result.checks[0]?.passed).toBe(true);
  });

  it("blocks network modules and allows the standard library", () => {
    for (const name of ["socket", "urllib.request", "http", "js", "pyodide"]) {
      const result = runCourseChecks(`import ${name}\n`, []);
      expect(result.error, name).toBe(`ModuleNotFoundError: No module named '${name}'`);
    }
    const ok = runCourseChecks("import random\nimport math\nrandom.seed(1)\nprint(random.randint(1, 6), math.floor(2.5))\n", []);
    expect(ok.ok).toBe(true);
    expect(ok.stdout).toBe("2 2\n");
  });

  it("shows only the student's lines in tracebacks", () => {
    const result = runCourseChecks('a = 1\nprint(fireball)\n', [check("never", "assert True")]);
    expect(result.ok).toBe(false);
    expect(result.checks).toEqual([]);
    expect(result.traceback).toContain('File "main.py", line 2, in <module>');
    expect(result.traceback).toContain("print(fireball)");
    expect(result.traceback).not.toContain("course_helpers");
    expect(result.traceback).not.toContain("<setup>");
    expect(result.error).toBe("NameError: name 'fireball' is not defined");

    const syntax = runCourseChecks('print("Hello)\n', []);
    expect(syntax.traceback).toContain('File "main.py", line 1');
    expect(syntax.error).toMatch(/^SyntaxError: unterminated string literal/);
  });

  it("keeps working when the student names variables str, len, type, isinstance or set", () => {
    const strength = runCourseChecks('str = 18\nprint("Strength:", str)\n', [check("prints", "assert _lines() == ['Strength: 18']")]);
    expect(strength).toMatchObject({ ok: true, stdout: "Strength: 18\n", error: "" });
    expect(strength.checks).toEqual([{ name: "prints", passed: true, message: "" }]);

    const bridge = runCourseChecks('len = 10\nprint("The bridge is", len, "steps long")\n', [
      check("count", "assert len(_lines()) == 1, 'One line.'"),
      check("value", "assert len == 10"),
    ]);
    expect(bridge.stdout).toBe("The bridge is 10 steps long\n");
    expect(bridge.checks.map((c) => c.passed)).toEqual([true, true]);

    const spell = runCourseChecks('type = "fire"\nprint(type)\n', [check("ice", "assert 'ice' in _captured_stdout, 'Use ice.'")]);
    expect(spell.ok).toBe(true);
    expect(spell.checks).toEqual([{ name: "ice", passed: false, message: "AssertionError: Use ice." }]);

    const asked = runCourseChecks('str = "Bob"\nname = input("Name? ")\nprint(name)\n', [], { stdin: ["Lucky"] });
    expect(asked).toMatchObject({ ok: true, stdout: "Name? Lucky\nLucky\n" });

    const many = runCourseChecks('isinstance = 1\nany = 2\nset = 3\ngetattr = 4\nlist = 5\nprint("ok")\n', [
      check("helpers", "assert _uses('node:Assign') and _count('node:Assign') == 5 and not _assigned_from_expression('set')"),
      check("lines", "assert _lines() == ['ok']"),
    ]);
    expect(many.checks.filter((c) => !c.passed)).toEqual([]);

    const crash = runCourseChecks("str = 1\nprint(fireball)\n", []);
    expect(crash.error).toBe("NameError: name 'fireball' is not defined");
    expect(crash.traceback).toContain('File "main.py", line 2');
    expect(crash.traceback).not.toContain("course_helpers");
  });

  it("treats exit() as the end of the program", () => {
    const result = runCourseChecks('print("one")\nexit()\nprint("two")\n', [check("one", "assert _lines() == ['one']")]);
    expect(result.ok).toBe(true);
    expect(result.checks[0]?.passed).toBe(true);
  });

  it("stops a program that prints forever with an explained error", () => {
    const result = runCourseChecks('while True:\n    print("again")\n', []);
    expect(result.ok).toBe(false);
    expect(result.error).toBe("TooMuchOutput: This program printed more than 200,000 characters, so it was stopped.");
    expect(result.stdout.length).toBeLessThanOrEqual(200_000);
  });

  it("reports a timeout instead of hanging", () => {
    const result = runCourseChecks("while True:\n    pass\n", [check("never", "assert True")], { timeoutMs: 1500 });
    expect(result.timedOut).toBe(true);
    expect(result.ok).toBe(false);
    expect(result.traceback).toBe("TimeoutError: The program ran too long and was stopped.");
  });
});

describe("course_helpers.py stays in step with the worker", () => {
  const worker = readFileSync(workerPath, "utf8");

  it("blocks exactly the modules GUARD blocks, and exempts exactly GUARD's names", () => {
    const script = `
import ast, json, sys
data = json.loads(sys.stdin.read())
guard = ast.parse(data["guard"])
blocked = next(ast.literal_eval(node.value) for node in guard.body
               if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "_blocked")
names = {node.name if isinstance(node, (ast.FunctionDef, ast.ClassDef)) else getattr(node.targets[0], "id", "")
         for node in guard.body
         if isinstance(node, (ast.FunctionDef, ast.ClassDef))
         or (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name))}
ns = {"__name__": "course_helpers"}
exec(compile(data["helpers"], "course_helpers.py", "exec"), ns)
print(json.dumps({
    "blocked": sorted(blocked) == sorted(ns["_COURSE_BLOCKED_IMPORTS"]),
    "names": sorted(names) == sorted(ns["_COURSE_CAMPAIGN_NAMES"]),
}))
`;
    const out = python(script, JSON.stringify({ guard: workerPrelude(), helpers: readFileSync(courseHelpersPath(), "utf8") }));
    expect(JSON.parse(out)).toEqual({ blocked: true, names: true });
  });

  it("is fetched by the worker before the network is disabled", () => {
    const load = worker.indexOf('new URL("course_helpers.py", import.meta.url)');
    const helpersAwaited = worker.indexOf("courseHelpers = await helpers;");
    const disabled = worker.indexOf("globalThis.fetch = () => Promise.reject");
    expect(load).toBeGreaterThan(-1);
    expect(helpersAwaited).toBeGreaterThan(-1);
    expect(helpersAwaited).toBeLessThan(disabled);
    expect(worker).toContain('data.type === "course-run"');
  });

  it("keeps the campaign GUARD extractable as plain text", () => {
    expect(workerPrelude()).toContain("class Party:");
  });

  it("leaves the import guard off when tools load it as course_helpers", () => {
    const out = python(
      `
import json, sys
ns = {"__name__": "course_helpers"}
exec(compile(sys.stdin.read(), "course_helpers.py", "exec"), ns)
import urllib.parse
print(json.dumps(ns["_concept_tokens"]("x = 1\\nparty.move('left')\\n")))
`,
      readFileSync(courseHelpersPath(), "utf8"),
    );
    expect(JSON.parse(out)).toEqual(
      expect.arrayContaining(["node:Module", "node:Assign", "const:int", "const:str", "node:Call"]),
    );
    expect(JSON.parse(out)).not.toContain("attr:move");
  });
});

/* -------------------------------------------------------------------------------------------- */
/* Parity: the same jobs through run-course.ts, the harness's run(), and the real browser worker  */
/* -------------------------------------------------------------------------------------------- */

type Job = { label: string; code: string; checks: CourseCheck[] } & Pick<CourseRunOptions, "setup" | "stdin" | "engine">;

const JOBS: Job[] = [
  {
    label: "passing and failing checks",
    code: 'name = "Lucky"\nprint("Hi " + name)\n',
    checks: [
      check("prints", "assert _lines() == ['Hi Lucky'], 'Greet Lucky.'"),
      check("joins", "assert _uses('op:Add'), 'Join with +.'"),
      check("loop", "assert _uses('node:For'), 'Use a for loop.'"),
      check("missing", "assert chalk_wall == 3, 'Make chalk_wall.'"),
    ],
  },
  {
    label: "input answers",
    code: 'a = input("First? ")\nb = input("Second? ")\nprint(a + b)\n',
    stdin: ["fire", "ball"],
    checks: [check("used", "assert _inputs_used() == 2"), check("out", "assert _lines()[-1] == 'fireball', _lines()")],
  },
  { label: "too many input calls", code: 'a = input("A? ")\nb = input("B? ")\n', stdin: ["x"], checks: [check("c", "assert True")] },
  { label: "name error", code: "print(fireball)\n", checks: [check("c", "assert True")] },
  { label: "syntax error", code: 'print("hi)\n', checks: [check("c", "assert True")] },
  { label: "def slip", code: 'def ("character")\n', checks: [] },
  { label: "campaign objects are off", code: 'party.move("left")\n', checks: [check("c", "assert True")] },
  {
    label: "engine on",
    code: 'party.move("up")\nprint_prompt("Halt!")\n',
    engine: true,
    checks: [check("moves", "assert party._moves == ['up']"), check("prompts", "assert _prompts == ['Halt!'], _prompts")],
  },
  {
    label: "setup and seeded random",
    code: "roll = random.randint(1, 20)\nprint(hero, roll)\n",
    setup: 'import random\nrandom.seed(7)\nhero = "Gearshift"\n',
    checks: [check("hero", "assert _lines()[0].startswith('Gearshift ')"), check("expr", "assert _assigned_from_expression('roll')")],
  },
  { label: "blocked import", code: "import urllib.request\n", checks: [] },
  { label: "exit", code: 'print("a")\nquit()\nprint("b")\n', checks: [check("a", "assert _lines() == ['a']")] },
  {
    label: "check errors",
    code: 'total = "68"\n',
    checks: [check("type", "assert total + 1 == 69"), check("bare", "assert total == 68")],
  },
  {
    label: "student names a variable str",
    code: 'str = 18\nprint("Strength:", str)\n',
    checks: [check("prints", "assert _lines() == ['Strength: 18'], _lines()"), check("assign", "assert _uses('node:Assign')")],
  },
  {
    label: "student names a variable len, check calls len()",
    code: 'len = 10\nprint("The bridge is", len, "steps long")\n',
    checks: [check("count", "assert len(_lines()) == 1, 'One line.'"), check("value", "assert len == 10")],
  },
  {
    label: "student names a variable type, with a failing check",
    code: 'type = "fire"\nprint(type)\n',
    checks: [check("ice", "assert 'ice' in _captured_stdout, 'Use ice.'"), check("fire", "assert type == 'fire'")],
  },
  {
    label: "student names a variable str, then input()",
    code: 'str = "Bob"\nname = input("Name? ")\nprint(name, str)\n',
    stdin: ["Lucky"],
    checks: [check("used", "assert _inputs_used() == 1"), check("out", "assert _lines()[-1] == 'Lucky Bob', _lines()")],
  },
  {
    label: "student shadows a builtin and then crashes",
    code: "str = 1\nprint(fireball)\n",
    checks: [check("c", "assert True")],
  },
];

type Comparable = { ok: boolean; stdout: string | null; error: string; checks: [string, boolean, string][] };

function fromNode(job: Job): Comparable {
  const result = runCourseChecks(job.code, job.checks, { setup: job.setup, stdin: job.stdin, engine: job.engine });
  return {
    ok: result.ok,
    stdout: result.stdout,
    error: result.error,
    checks: result.checks.map((c) => [c.name, c.passed, c.message]),
  };
}

describe("parity with the prototype harness", () => {
  it("gives the same per-check results through harness.run() and runCourseChecks()", () => {
    const script = `
import json, sys
sys.path.insert(0, ${JSON.stringify(harnessDir)})
import harness
out = []
for job in json.loads(sys.stdin.read()):
    checkpoints = [{"checks": [[c["name"], c["code"]] for c in job["checks"]]}]
    result = harness.run(job["code"], checkpoints, job.get("setup") or "", job.get("stdin"), job.get("engine", False))
    rows = [row for group in result["checkpoints"] for row in group]
    out.append({"ok": result["ok"], "stdout": result["stdout"] if result["ok"] else None, "error": result["error"], "checks": rows})
print(json.dumps(out))
`;
    const harnessResults = JSON.parse(python(script, JSON.stringify(JOBS))) as Comparable[];
    JOBS.forEach((job, index) => {
      const node = fromNode(job);
      expect(harnessResults[index], job.label).toEqual({ ...node, stdout: node.ok ? node.stdout : null });
    });
  });

  it("still catches bad content: passing starters, loose checks, bad quiz keys, early concepts", () => {
    const unitDir = path.join(temp, "harness-selftest");
    rmSync(unitDir, { recursive: true, force: true });
    spawnSync("mkdir", ["-p", unitDir]);
    writeFileSync(path.join(unitDir, "u01_selftest.py"), SELFTEST_UNIT);
    const child = spawnSync(pythonExecutable(), [path.join(harnessDir, "harness.py")], {
      encoding: "utf8",
      env: { ...process.env, PROTOTYPE_DIR: unitDir },
      timeout: 120_000,
    });
    const output = child.stdout;
    expect(child.status, output + child.stderr).toBe(1);
    const errors = output.split("\n").filter((line) => line.startsWith("ERROR"));
    const expected = [
      "u01_selftest/bad/starter-passes: starter code already passes every checkpoint",
      "u01_selftest/bad/loose: wrong answer (hard-codes 5) PASSES every checkpoint",
      "u01_selftest/bad/gate: solution uses concepts not introduced yet: call:range, node:For",
      "u01_selftest/bad/no-engine: solution fails at checkpoint 0: NameError: name 'party' is not defined",
      "u01_selftest/quiz/q1: mc answer index out of range",
      "u01_selftest/quiz/q2: predict answer '11' but code prints '2'",
      "u01_selftest/quiz/q4: fill answer '3' gives '4\\n'",
      "u01_selftest/quiz/q5: parsons lines in order give 'b\\na\\n'",
      "u01_selftest/quiz/q6: the buggy code already prints the expected output",
    ];
    for (const line of expected) {
      expect(errors.some((error) => error.includes(line)), `${line}\n${output}`).toBe(true);
    }
    expect(errors.filter((error) => error.includes("/good/")), output).toEqual([]);
    expect(errors.filter((error) => error.includes("quiz/q3")), output).toEqual([]);
    expect(errors.length, output).toBe(expected.length);
  });
});

const SELFTEST_UNIT = String.raw`
UNIT = dict(id="selftest", order=1, title="Self test", martu_intro="Hi.", goals=["test"], campaign_links=[])

ITEMS = [
    dict(kind="lesson", id="good", title="Good", exercises=[
        dict(id="greet", title="Greet", martu="Say hi.",
             introduces=["node:Assign", "call:input", "call:print", "const:str", "op:Add", "const:int"],
             stdin=["Lucky"], example="print('Hi')", example_output="Hi",
             starter="# ask for a name\n", solution="name = input('Name? ')\nprint('Hi ' + name)\n",
             partials=["name = input('Name? ')\n"],
             checkpoints=[
                 dict(text="Ask for a name.", hints=["Use input().", "name = input('Name? ')"],
                      checks=[("asks", "assert _inputs_used() == 1, 'Ask one question with input().'")]),
                 dict(text="Greet them.", hints=["Use print.", "print('Hi ' + name)"],
                      checks=[("greets", "assert _lines()[-1] == 'Hi Lucky', 'Print Hi and the name.'"),
                              ("joins", "assert _uses('op:Add'), 'Join the text with +.'")]),
             ],
             wrong_answers=[dict(why="hard-codes the name", code="name = input('Name? ')\nprint('Hi', name)\n",
                                 fails_at=2, message_contains="join"),
                            dict(why="asks twice", code="a = input('A? ')\nb = input('B? ')\n", fails_at=0,
                                 message_contains="more input")]),
        dict(id="engine-move", title="Move", martu="Move.", engine=True,
             starter="", solution="party.move('left')\n",
             checkpoints=[dict(text="Move left.", hints=["a", "b"],
                               checks=[("moved", "assert party._moves == ['left'], 'Move left.'")])]),
    ]),
    dict(kind="lesson", id="bad", title="Bad", exercises=[
        dict(id="starter-passes", title="Oops", martu="x", starter="print('Hi')\n", solution="print('Hi')\n",
             checkpoints=[dict(text="Print Hi.", hints=["a", "b"],
                               checks=[("hi", "assert _lines() == ['Hi'], 'Print Hi.'")])]),
        dict(id="loose", title="Loose", martu="x", starter="", solution="x = 2 + 3\n",
             checkpoints=[dict(text="Make x.", hints=["a", "b"], checks=[("x", "assert x == 5, 'Make x 5.'")])],
             wrong_answers=[dict(why="hard-codes 5", code="x = 5\n", fails_at=1)]),
        dict(id="gate", title="Gate", martu="x", starter="", solution="for i in range(2):\n    print(i)\n",
             checkpoints=[dict(text="Count.", hints=["a", "b"],
                               checks=[("count", "assert _lines() == ['0', '1'], 'Count.'")])]),
        dict(id="no-engine", title="No engine", martu="x", starter="", solution="party.move('left')\n",
             checkpoints=[dict(text="Move.", hints=["a", "b"],
                               checks=[("moved", "assert party._moves == ['left'], 'Move left.'")])]),
    ]),
    dict(kind="quiz", id="quiz", title="Quiz", questions=[
        dict(type="mc", q="Pick", choices=["a", "b"], answer=5, explain="x"),
        dict(type="predict", q="What prints?", code="print(1 + 1)", answer="11", explain="x"),
        dict(type="predict", q="What prints?", code="print(2 + 2)", answer="4", explain="x"),
        dict(type="fill", q="Fill", code="print(___ + 1)", answer="2", accept=["3"], expected_output="3", explain="x"),
        dict(type="parsons", q="Order", lines=["print('b')", "print('a')"], expected_output="a\nb", explain="x"),
        dict(type="bug", q="Fix", code="print('ok')", fix="print('ok')", expected_output="ok", explain="x"),
    ]),
]
`;

/* -------------------------------------------------------------------------------------------- */
/* The real browser worker, run in Node with Pyodide (Python 3.13)                               */
/* -------------------------------------------------------------------------------------------- */

const pyodideReady = existsSync(path.join(repo, "public/pyodide/pyodide.mjs"));

// Loads python-worker.js as-is, except two test-only rewrites Node needs: import.meta.url points at the real
// worker file, and Pyodide gets a filesystem path for indexURL. Then it posts the jobs as "course-run" messages.
const WORKER_DRIVER = String.raw`
import { readFileSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
const [workerPath, copyPath] = process.argv.slice(2);
const jobs = JSON.parse(readFileSync(0, "utf8"));
const realFetch = globalThis.fetch;
globalThis.fetch = async (url) => {
  const href = String(url);
  if (href.startsWith("file:")) return new Response(await readFile(fileURLToPath(href)), { status: 200 });
  return realFetch(url);
};
let ready;
const readyMessage = new Promise((resolve) => (ready = resolve));
const waiting = new Map();
globalThis.self = {
  postMessage(message) {
    if (message.type === "ready" || message.type === "failed") ready(message);
    else if (message.type === "result") waiting.get(message.requestId)?.(message);
  },
};
let source = await readFile(workerPath, "utf8");
source = source.replaceAll("import.meta.url", JSON.stringify(pathToFileURL(workerPath).href));
source = source.replace("loadPyodide({ indexURL: base.href })", "loadPyodide({ indexURL: decodeURIComponent(base.pathname) })");
await writeFile(copyPath, source);
await import(pathToFileURL(copyPath).href);
const boot = await readyMessage;
if (boot.type !== "ready") throw new Error(boot.message);
const results = [];
let requestId = 1;
for (const job of jobs) {
  const id = requestId++;
  const result = await new Promise((resolve) => {
    waiting.set(id, resolve);
    self.onmessage({ data: { type: "course-run", requestId: id, code: job.code, checks: job.checks, setup: job.setup ?? "", stdin: job.stdin ?? [], engine: job.engine === true } });
  });
  results.push(result);
}
process.stdout.write(JSON.stringify(results));
process.exit(0);
`;

describe("parity with the browser worker (Pyodide)", () => {
  it.skipIf(!pyodideReady)("gives the same results as runCourseChecks() for every job", () => {
    const driver = path.join(temp, "driver.mjs");
    writeFileSync(driver, WORKER_DRIVER);
    const child = spawnSync(process.execPath, [driver, workerPath, path.join(temp, "worker-copy.mjs")], {
      input: JSON.stringify(JOBS),
      encoding: "utf8",
      timeout: 120_000,
      maxBuffer: 64 * 1024 * 1024,
    });
    expect(child.status, child.stderr).toBe(0);
    const results = JSON.parse(child.stdout) as {
      ok: boolean;
      stdout: string;
      traceback: string;
      checks: { name: string; passed: boolean; message: string }[];
      stageEvents: unknown[];
    }[];
    JOBS.forEach((job, index) => {
      const node = runCourseChecks(job.code, job.checks, { setup: job.setup, stdin: job.stdin, engine: job.engine });
      const browser = results[index];
      const lastLine = (text: string) => text.trim().split("\n").at(-1) ?? "";
      expect(
        {
          ok: browser.ok,
          stdout: browser.stdout,
          error: lastLine(browser.traceback),
          checks: browser.checks,
          stageEvents: browser.stageEvents,
        },
        job.label,
      ).toEqual({ ok: node.ok, stdout: node.stdout, error: node.error, checks: node.checks, stageEvents: node.stageEvents });
    });
  }, 120_000);

  it("is importable as a module URL", () => {
    expect(pathToFileURL(workerPath).href).toMatch(/python-worker\.js$/);
  });
});
