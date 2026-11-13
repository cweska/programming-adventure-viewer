import type { LanguageAdapter } from "../types";
import { explainPython } from "./explain";
import { formatPython } from "./format";
import { runPython, startPythonSession } from "./run";

export const pythonAdapter: LanguageAdapter = {
  format: formatPython,
  run: runPython,
  startSession: startPythonSession,
  explain: explainPython,
};

export { explainPython } from "./explain";
export { formatPython } from "./format";
export {
  runPython,
  runCourse,
  startPythonSession,
  whenPythonReady,
  PythonTimeoutError,
  COURSE_TIMEOUT_TRACEBACK,
  PYTHON_WORKER_VERSION,
  pythonWorkerUrl,
} from "./run";
