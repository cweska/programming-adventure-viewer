import type { LanguageAdapter } from "../types";
import { explainPython } from "./explain";
import { formatPython } from "./format";
import { runPython } from "./run";

export const pythonAdapter: LanguageAdapter = {
  format: formatPython,
  run: runPython,
  explain: explainPython,
};

export { explainPython } from "./explain";
export { formatPython } from "./format";
export { runPython, whenPythonReady, PythonTimeoutError } from "./run";
