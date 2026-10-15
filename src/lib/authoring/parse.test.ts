import { describe, expect, it, vi } from "vitest";
import { makeValidModule } from "../lesson/fixtures";
import { authorFromPrompt } from "./complete";
import { parseAuthorModelOutput } from "./parse";

const prompt = "A gate, a torch, and a gatekeeper. Keep this prompt.";

describe("authoring parser", () => {
  it("turns valid model output into a module", () => {
    const direct = parseAuthorModelOutput(JSON.stringify(makeValidModule()), prompt);
    expect(direct.ok).toBe(true);
    if (direct.ok) expect(direct.module.title).toBe("Emberkeep");

    const fenced = parseAuthorModelOutput("```json\n" + JSON.stringify(makeValidModule()) + "\n```", prompt);
    expect(fenced.ok).toBe(true);
  });

  it("rejects invalid JSON and keeps the teacher prompt", () => {
    const result = parseAuthorModelOutput("{not json", prompt);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toMatch(/not valid JSON/);
      expect(result.prompt).toBe(prompt);
    }
  });

  it("rejects schema-invalid JSON and keeps the teacher prompt", () => {
    const result = parseAuthorModelOutput(
      JSON.stringify({ ...makeValidModule(), language: "lua" }),
      prompt,
    );
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toMatch(/lesson schema/);
      expect(result.prompt).toBe(prompt);
    }
  });
});

describe("authorFromPrompt", () => {
  it("does not call the model when output is already provided", async () => {
    const fetchImpl = vi.fn();
    const result = await authorFromPrompt({
      prompt,
      modelOutput: "{nope",
      env: { AI_BASE_URL: "https://example.invalid/v1", AI_API_KEY: "test", AI_MODEL: "test" },
      fetchImpl,
    });
    expect(fetchImpl).not.toHaveBeenCalled();
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.prompt).toBe(prompt);
  });

  it("does not call the network when AI is not configured", async () => {
    const fetchImpl = vi.fn();
    const result = await authorFromPrompt({
      prompt,
      env: {},
      fetchImpl,
    });
    expect(fetchImpl).not.toHaveBeenCalled();
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.prompt).toBe(prompt);
  });

  it("parses a fake model response without leaving the prompt behind on failure", async () => {
    const fetchImpl = vi.fn(async () => {
      return new Response(JSON.stringify({ choices: [{ message: { content: "{still bad" } }] }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    });
    const result = await authorFromPrompt({
      prompt,
      env: { AI_BASE_URL: "https://example.invalid/v1", AI_API_KEY: "test", AI_MODEL: "demo" },
      fetchImpl,
    });
    expect(fetchImpl).toHaveBeenCalledOnce();
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.prompt).toBe(prompt);
  });

  it("accepts schema JSON from a fake model response", async () => {
    const fetchImpl = vi.fn(async () => {
      return new Response(
        JSON.stringify({ choices: [{ message: { content: JSON.stringify(makeValidModule()) } }] }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      );
    });
    const result = await authorFromPrompt({
      prompt,
      env: { AI_BASE_URL: "https://example.invalid/v1", AI_API_KEY: "test", AI_MODEL: "demo" },
      fetchImpl,
    });
    expect(result.ok).toBe(true);
    if (result.ok) expect(result.module.id).toBe("emberkeep");
  });
});
