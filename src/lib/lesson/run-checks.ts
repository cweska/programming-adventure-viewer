import { spawnSync } from "node:child_process";
import type { Check } from "./schema";

export type PythonCheckRun = {
  ok: boolean;
  error: string;
  stdout: string;
  checks: { name: string; passed: boolean; message: string }[];
};

const RUNNER = `
import io
import json
import sys

payload = json.loads(sys.stdin.read())
buffer = io.StringIO()
real_stdout = sys.stdout
sys.stdout = buffer
namespace = {"__name__": "__main__"}
ok = True
error = ""
try:
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
sys.stdout = real_stdout
json.dump(
    {
        "ok": ok,
        "error": error,
        "stdout": namespace["_captured_stdout"],
        "checks": results,
    },
    sys.stdout,
)
`;

export function runPythonChecks(code: string, checks: Check[]): PythonCheckRun {
  const child = spawnSync("python3", ["-c", RUNNER], {
    input: JSON.stringify({ code, checks }),
    encoding: "utf8",
  });
  if (child.error) throw child.error;
  if (child.status !== 0) {
    throw new Error(child.stderr || child.stdout || "python3 failed");
  }
  return JSON.parse(child.stdout) as PythonCheckRun;
}
