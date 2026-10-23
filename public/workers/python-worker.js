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

self.onmessage = async (event) => {
  const data = event.data || {};
  if (data.type !== "run") return;
  const pyodide = await boot();
  const stdout = [];
  const stderr = [];
  pyodide.setStdout({ batched: (text) => pushChunk(stdout, String(text)) });
  pyodide.setStderr({ batched: (text) => pushChunk(stderr, String(text)) });

  const events = [];
  const globals = pyodide.runPython("{}");
  globals.set("_stage_say", (text) => {
    events.push({ type: "say", text: String(text) });
  });
  globals.set("_stage_flare", () => {
    events.push({ type: "flare" });
  });
  globals.set("_stage_focus", (imageId) => {
    events.push({ type: "focus", imageId: String(imageId) });
  });
  globals.set("_stage_move", (direction) => {
    events.push({ type: "move", direction: String(direction) });
  });
  globals.set("_stage_prompt", (text) => {
    events.push({ type: "prompt", text: String(text) });
  });
  globals.set("_stage_options", (count) => {
    events.push({ type: "options", options: Array.from({ length: Number(count) }, () => "") });
  });
  globals.set("_stage_option", (index, text) => {
    const last = events[events.length - 1];
    if (last && last.type === "options") last.options[Number(index)] = String(text);
  });
  globals.set("_stage_speak", (option) => {
    events.push({ type: "speak", option: String(option) });
  });
  globals.set("_stage_highlight", (option) => {
    events.push({ type: "highlight", option: String(option) });
  });

  let ok = true;
  let traceback = "";
  try {
    const prepared = await pyodide.runPythonAsync(GUARD, { globals });
    if (prepared && typeof prepared.destroy === "function") prepared.destroy();
    const returned = await pyodide.runPythonAsync(String(data.code ?? ""), { globals });
    if (returned && typeof returned.destroy === "function") returned.destroy();
  } catch (error) {
    ok = false;
    traceback = formatTraceback(error);
  }

  const checks = [];
  if (ok) {
    try {
      const flushed = await pyodide.runPythonAsync("import sys\nsys.stdout.flush()\n", { globals });
      if (flushed && typeof flushed.destroy === "function") flushed.destroy();
    } catch {
      // A flush failure should not hide output already captured.
    }
    globals.set("_captured_stdout", stdout.join(""));
    for (const check of data.checks || []) {
      try {
        const returned = await pyodide.runPythonAsync(String(check.code ?? ""), { globals });
        if (returned && typeof returned.destroy === "function") returned.destroy();
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
  self.postMessage({
    type: "result",
    ok,
    stdout: stdout.join(""),
    stderr: stderr.join(""),
    traceback,
    checks,
    stageEvents: events,
  });
};
