let pyodidePromise = null;

function pyodideBase() {
  return new URL("../pyodide/", import.meta.url);
}

function boot() {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      const base = pyodideBase();
      const { loadPyodide } = await import(new URL("pyodide.mjs", base).href);
      const pyodide = await loadPyodide({ indexURL: base.href });
      globalThis.fetch = () => Promise.reject(new Error("Network is disabled"));
      if ("XMLHttpRequest" in globalThis) {
        globalThis.XMLHttpRequest = function XMLHttpRequestBlocked() {
          throw new Error("Network is disabled");
        };
      }
      return pyodide;
    })();
  }
  return pyodidePromise;
}

const GUARD = `
import builtins
_real_import = builtins.__import__
_blocked = {
    "js", "pyodide", "micropip", "urllib", "http", "socket", "ssl",
    "ftplib", "smtplib", "xmlrpc", "webbrowser", "requests", "httpx", "aiohttp",
}
def _guard(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root in _blocked:
        raise ModuleNotFoundError(f"No module named {name!r}")
    return _real_import(name, globals, locals, fromlist, level)
builtins.__import__ = _guard

class Stage:
    def say(self, text):
        _stage_say(str(text))
    def flare(self):
        _stage_flare()
    def focus(self, image_id):
        _stage_focus(str(image_id))

stage = Stage()

class Party:
    _directions = ("left", "right", "up", "down")

    def __init__(self):
        self._moves = []
        self.members = []

    def move(self, direction):
        if direction not in self._directions:
            raise ValueError(
                f'The party cannot move {direction!r}. Use "left", "right", "up", or "down".'
            )
        self._moves.append(direction)
        _stage_move(direction)

party = Party()

_prompts = []
_options = []
_spoken = []
_greens = []

def print_prompt(dialogue):
    text = str(dialogue)
    _prompts.append(text)
    _stage_prompt(text)

def print_options(*options):
    if len(options) < 1 or len(options) > 4:
        raise ValueError("print_options() needs between 1 and 4 options.")
    texts = [str(option) for option in options]
    _options.append(texts)
    _stage_options(len(texts))
    for index, text in enumerate(texts):
        _stage_option(index, text)

class User:
    def __init__(self):
        self._clicked = None

    def clicked(self):
        return self._clicked

user = User()

def speak_dialogue(option):
    _spoken.append(option)
    _stage_speak(str(option))

def make_option_green():
    _greens.append(user._clicked)
    _stage_highlight(str(user._clicked))

_casts = []
_mana_prints = []

def reinforce_barrier(caster):
    _casts.append(caster["character_name"])
    _stage_cast(str(caster["character_name"]))

def print_mana(caster, mana_bar):
    _mana_prints.append((caster["character_name"], str(mana_bar)))
    _stage_mana(str(caster["character_name"]), str(mana_bar), int(caster["mana"]), int(caster["max_mana"]))

def _required_roll(check):
    for roll in range(1, 21):
        if check(roll):
            return roll
    return 21

def show_roll(skill, roll, success, required):
    _stage_roll(str(skill), int(roll), bool(success), int(required))
`;

const NEWLINE = String.fromCharCode(10);

function formatTraceback(error) {
  const message = String(error && error.message ? error.message : error);
  const type = error && typeof error.type === "string" ? error.type.split(".").pop() : "";
  if (!type || message.includes(type + ":")) return message;
  return message + NEWLINE + type + ": " + message;
}

function pushChunk(bucket, text) {
  if (!text) return;
  bucket.push(text.endsWith(NEWLINE) ? text : text + NEWLINE);
}

function checkMessage(error) {
  const text = String(error && error.message ? error.message : error);
  const lines = text.split(NEWLINE).map((line) => line.trim()).filter(Boolean);
  return lines.length > 0 ? lines[lines.length - 1] : text;
}

boot()
  .then(() => {
    self.postMessage({ type: "ready" });
  })
  .catch((error) => {
    self.postMessage({ type: "failed", message: String(error && error.message ? error.message : error) });
  });

function createGlobals(pyodide, sink) {
  const globals = pyodide.runPython("{}");
  const emit = (event) => sink.events.push(event);
  globals.set("_stage_say", (text) => emit({ type: "say", text: String(text) }));
  globals.set("_stage_flare", () => emit({ type: "flare" }));
  globals.set("_stage_focus", (imageId) => emit({ type: "focus", imageId: String(imageId) }));
  globals.set("_stage_move", (direction) => emit({ type: "move", direction: String(direction) }));
  globals.set("_stage_prompt", (text) => emit({ type: "prompt", text: String(text) }));
  globals.set("_stage_options", (count) =>
    emit({ type: "options", options: Array.from({ length: Number(count) }, () => "") }),
  );
  globals.set("_stage_option", (index, text) => {
    const last = sink.events[sink.events.length - 1];
    if (last && last.type === "options") last.options[Number(index)] = String(text);
  });
  globals.set("_stage_speak", (option) => emit({ type: "speak", option: String(option) }));
  globals.set("_stage_highlight", (option) => emit({ type: "highlight", option: String(option) }));
  globals.set("_stage_cast", (name) => emit({ type: "cast", name: String(name) }));
  globals.set("_stage_mana", (name, bar, mana, max) =>
    emit({ type: "mana", name: String(name), bar: String(bar), mana: Number(mana), max: Number(max) }),
  );
  globals.set("_stage_roll", (skill, roll, success, required) =>
    emit({ type: "roll", skill: String(skill), roll: Number(roll), success: Boolean(success), required: Number(required) }),
  );
  return globals;
}

async function runIn(pyodide, globals, code) {
  const returned = await pyodide.runPythonAsync(String(code ?? ""), { globals });
  if (returned && typeof returned.destroy === "function") returned.destroy();
}

function capture(pyodide) {
  const output = { stdout: [], stderr: [] };
  pyodide.setStdout({ batched: (text) => pushChunk(output.stdout, String(text)) });
  pyodide.setStderr({ batched: (text) => pushChunk(output.stderr, String(text)) });
  return output;
}

async function flush(pyodide, globals) {
  try {
    await runIn(pyodide, globals, "import sys\nsys.stdout.flush()\n");
  } catch {
    // A flush failure should not hide output already captured.
  }
}

const sessions = new Map();

async function runProgram(data) {
  const pyodide = await boot();
  const output = capture(pyodide);
  const sink = { events: [] };
  const globals = createGlobals(pyodide, sink);

  let ok = true;
  let traceback = "";
  try {
    await runIn(pyodide, globals, GUARD);
    if (data.setup) await runIn(pyodide, globals, data.setup);
    await runIn(pyodide, globals, data.code);
  } catch (error) {
    ok = false;
    traceback = formatTraceback(error);
  }

  const checks = [];
  if (ok) {
    await flush(pyodide, globals);
    globals.set("_captured_stdout", output.stdout.join(""));
    for (const check of data.checks || []) {
      try {
        await runIn(pyodide, globals, check.code);
        checks.push({ name: String(check.name ?? "check"), passed: true, message: "" });
      } catch (error) {
        checks.push({
          name: String(check.name ?? "check"),
          passed: false,
          message: checkMessage(error),
        });
      }
    }
  }

  try {
    globals.destroy();
  } catch {
    // The proxy may already be gone after a hard Python failure.
  }
  return { ok, stdout: output.stdout.join(""), stderr: output.stderr.join(""), traceback, checks, stageEvents: sink.events };
}

function endSession(id) {
  const session = sessions.get(id);
  if (!session) return;
  sessions.delete(id);
  try {
    session.globals.destroy();
  } catch {
    // Already gone.
  }
}

async function runSession(data) {
  const pyodide = await boot();
  const output = capture(pyodide);
  let session = sessions.get(data.id);
  if (data.type === "session-start") {
    endSession(data.id);
    const sink = { events: [] };
    session = { sink, globals: createGlobals(pyodide, sink) };
    sessions.set(data.id, session);
  }
  if (!session) {
    return { ok: false, stdout: "", stderr: "", traceback: "RuntimeError: The game session has ended.", checks: [], stageEvents: [] };
  }
  session.sink.events = [];
  let ok = true;
  let traceback = "";
  try {
    if (data.type === "session-start") {
      await runIn(pyodide, session.globals, GUARD);
      if (data.setup) await runIn(pyodide, session.globals, data.setup);
    }
    await runIn(pyodide, session.globals, data.code);
  } catch (error) {
    ok = false;
    traceback = formatTraceback(error);
  }
  await flush(pyodide, session.globals);
  return { ok, stdout: output.stdout.join(""), stderr: output.stderr.join(""), traceback, checks: [], stageEvents: session.sink.events };
}

self.onmessage = async (event) => {
  const data = event.data || {};
  if (data.type === "session-end") {
    endSession(data.id);
    return;
  }
  let result;
  if (data.type === "run") result = await runProgram(data);
  else if (data.type === "session-start" || data.type === "session-call") result = await runSession(data);
  else return;
  self.postMessage({ type: "result", requestId: data.requestId, ...result });
};
