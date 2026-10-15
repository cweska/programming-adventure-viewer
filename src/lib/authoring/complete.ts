import { parseAuthorModelOutput, type AuthorResult } from "./parse";
import { AUTHOR_SYSTEM_PROMPT } from "./prompt";

type FetchLike = (input: string, init?: RequestInit) => Promise<Response>;

export type AppEnv = Record<string, string | undefined>;

export type AuthorRequest = {
  prompt: string;
  modelOutput?: string;
  env: AppEnv;
  fetchImpl?: FetchLike;
};

function notConfigured(prompt: string): AuthorResult {
  return {
    ok: false,
    error: "AI is not configured. Set AI_BASE_URL, AI_API_KEY, and AI_MODEL.",
    prompt,
  };
}

export async function authorFromPrompt(request: AuthorRequest): Promise<AuthorResult> {
  const prompt = request.prompt ?? "";
  if (!prompt.trim()) {
    return { ok: false, error: "Write a prompt before asking for a draft.", prompt };
  }

  if (request.modelOutput !== undefined) {
    return parseAuthorModelOutput(request.modelOutput, prompt);
  }

  const base = request.env.AI_BASE_URL?.replace(/\/$/, "");
  const key = request.env.AI_API_KEY;
  const model = request.env.AI_MODEL;
  if (!base || !key || !model) {
    return notConfigured(prompt);
  }

  const fetchImpl = request.fetchImpl ?? fetch;
  let response: Response;
  try {
    response = await fetchImpl(`${base}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        temperature: 0.2,
        messages: [
          { role: "system", content: AUTHOR_SYSTEM_PROMPT },
          { role: "user", content: prompt },
        ],
      }),
    });
  } catch {
    return {
      ok: false,
      error: "The model could not be reached.",
      prompt,
    };
  }

  if (!response.ok) {
    return {
      ok: false,
      error: `The model returned ${response.status}.`,
      prompt,
    };
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return { ok: false, error: "The model response was not JSON.", prompt };
  }

  const content = readContent(payload);
  if (!content) {
    return { ok: false, error: "The model response did not include a message.", prompt };
  }
  return parseAuthorModelOutput(content, prompt);
}

function readContent(payload: unknown): string | null {
  if (!payload || typeof payload !== "object") return null;
  const choices = (payload as { choices?: unknown }).choices;
  if (!Array.isArray(choices) || choices.length === 0) return null;
  const message = (choices[0] as { message?: { content?: unknown } }).message;
  return typeof message?.content === "string" ? message.content : null;
}
