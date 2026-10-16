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
