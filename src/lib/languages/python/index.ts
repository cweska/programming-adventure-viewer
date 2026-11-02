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
export { runPython, startPythonSession, whenPythonReady, PythonTimeoutError } from "./run";
