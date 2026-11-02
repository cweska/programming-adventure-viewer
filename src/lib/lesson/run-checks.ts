import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import type { Check } from "./schema";

export type PythonCheckRun = {
  ok: boolean;
  error: string;
  stdout: string;
  checks: { name: string; passed: boolean; message: string }[];
  events: StageRecord[];
  calls: { ok: boolean; error: string; events: StageRecord[] }[];
};

export type StageRecord = Record<string, string | number | boolean | string[]>;

export function workerPrelude(): string {
  const worker = readFileSync(path.join(process.cwd(), "public/workers/python-worker.js"), "utf8");
  const match = worker.match(/const GUARD = `([\s\S]*?)`;/);
  if (!match) throw new Error("The Python worker has no GUARD prelude.");
  const prelude = match[1];
  if (prelude.includes("${") || prelude.includes("\\")) {
    throw new Error("The GUARD prelude must stay plain text so tests run the same Python as the browser.");
  }
  return prelude;
}

const RUNNER = `
import io
import json
import sys

payload = json.loads(sys.stdin.read())
buffer = io.StringIO()
real_stdout = sys.stdout
sys.stdout = buffer
namespace = {"__name__": "__main__"}
events = []
namespace["_stage_say"] = lambda text: events.append({"type": "say", "text": str(text)})
namespace["_stage_flare"] = lambda: events.append({"type": "flare"})
namespace["_stage_focus"] = lambda image_id: events.append({"type": "focus", "imageId": str(image_id)})
namespace["_stage_move"] = lambda direction: events.append({"type": "move", "direction": str(direction)})
namespace["_stage_prompt"] = lambda text: events.append({"type": "prompt", "text": str(text)})
namespace["_stage_options"] = lambda count: events.append({"type": "options", "options": [""] * int(count)})
namespace["_stage_option"] = lambda index, text: events[-1]["options"].__setitem__(int(index), str(text))
namespace["_stage_speak"] = lambda option: events.append({"type": "speak", "option": str(option)})
namespace["_stage_highlight"] = lambda option: events.append({"type": "highlight", "option": str(option)})
namespace["_stage_cast"] = lambda name: events.append({"type": "cast", "name": str(name)})
namespace["_stage_mana"] = lambda name, bar, mana, maximum: events.append(
    {"type": "mana", "name": str(name), "bar": str(bar), "mana": int(mana), "max": int(maximum)}
)
namespace["_stage_roll"] = lambda skill, roll, success, required: events.append(
    {"type": "roll", "skill": str(skill), "roll": int(roll), "success": bool(success), "required": int(required)}
)
exec(payload["prelude"], namespace, namespace)
ok = True
error = ""
try:
    exec(payload.get("setup", ""), namespace, namespace)
    exec(payload["code"], namespace, namespace)
except Exception as exc:
    ok = False
    error = f"{type(exc).__name__}: {exc}"
namespace["_captured_stdout"] = buffer.getvalue()
results = []
if ok:
    for check in payload["checks"]:
        try:
            exec(check["code"], namespace, namespace)
            results.append({"name": check["name"], "passed": True, "message": ""})
        except Exception as exc:
            results.append(
                {
                    "name": check["name"],
                    "passed": False,
                    "message": f"{type(exc).__name__}: {exc}",
                }
            )
calls = []
for call in payload.get("calls", []):
    start = len(events)
    try:
        exec(call, namespace, namespace)
        calls.append({"ok": True, "error": "", "events": events[start:]})
    except Exception as exc:
        calls.append({"ok": False, "error": f"{type(exc).__name__}: {exc}", "events": events[start:]})
sys.stdout = real_stdout
json.dump(
    {
        "ok": ok,
        "error": error,
        "stdout": namespace["_captured_stdout"],
        "checks": results,
        "events": events,
        "calls": calls,
    },
    sys.stdout,
)
`;

export function runPythonChecks(
  code: string,
  checks: Check[],
  options: { setup?: string; calls?: string[] } = {},
): PythonCheckRun {
  const child = spawnSync("python3", ["-c", RUNNER], {
    input: JSON.stringify({ code, checks, prelude: workerPrelude(), setup: options.setup ?? "", calls: options.calls ?? [] }),
    encoding: "utf8",
  });
  if (child.error) throw child.error;
  if (child.status !== 0) {
    throw new Error(child.stderr || child.stdout || "python3 failed");
  }
  return JSON.parse(child.stdout) as PythonCheckRun;
}
