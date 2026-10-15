import { formatSchemaError, moduleSchema, type Module } from "../lesson/schema";

export type AuthorSuccess = {
  ok: true;
  module: Module;
};

export type AuthorFailure = {
  ok: false;
  error: string;
  prompt: string;
};

export type AuthorResult = AuthorSuccess | AuthorFailure;

function extractJson(text: string): unknown {
  const trimmed = text.trim();
  const fence = trimmed.match(/```(?:json)?\s*([\s\S]*?)```/);
  const body = (fence ? fence[1] : trimmed).trim();
  try {
    return JSON.parse(body);
  } catch {
    const start = body.indexOf("{");
    const end = body.lastIndexOf("}");
    if (start >= 0 && end > start) {
      return JSON.parse(body.slice(start, end + 1));
    }
    throw new Error("Model output is not valid JSON.");
  }
}

export function parseAuthorModelOutput(modelOutput: string, teacherPrompt: string): AuthorResult {
  let value: unknown;
  try {
    value = extractJson(modelOutput);
  } catch {
    return {
      ok: false,
      error: "Model output is not valid JSON.",
      prompt: teacherPrompt,
    };
  }

  const parsed = moduleSchema.safeParse(value);
  if (!parsed.success) {
    return {
      ok: false,
      error: `The draft does not match the lesson schema.\n${formatSchemaError(parsed.error)}`,
      prompt: teacherPrompt,
    };
  }

  return { ok: true, module: parsed.data };
}
