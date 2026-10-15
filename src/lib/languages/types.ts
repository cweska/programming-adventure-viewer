import type { StageEvent } from "../stage/bridge";

export type Explanation = {
  title: string;
  hint: string;
  raw: string;
};

export type CheckResult = {
  name: string;
  passed: boolean;
  message: string;
};

export type RunInput = {
  code: string;
  checks: { name: string; code: string }[];
};

export type RunResult = {
  ok: boolean;
  stdout: string;
  stderr: string;
  traceback: string;
  checks: CheckResult[];
  stageEvents: StageEvent[];
  timedOut?: boolean;
};

export interface LanguageAdapter {
  format(code: string): Promise<string>;
  run(input: RunInput): Promise<RunResult>;
  explain(traceback: string): Explanation;
}
