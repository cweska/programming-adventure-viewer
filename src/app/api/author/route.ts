import { authorFromPrompt } from "../../../lib/authoring/complete";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  let body: { prompt?: unknown; modelOutput?: unknown };
  try {
    body = (await request.json()) as { prompt?: unknown; modelOutput?: unknown };
  } catch {
    return Response.json({ ok: false, error: "The request was not JSON.", prompt: "" }, { status: 400 });
  }
  const prompt = typeof body.prompt === "string" ? body.prompt : "";
  const result = await authorFromPrompt({
    prompt,
    modelOutput: typeof body.modelOutput === "string" ? body.modelOutput : undefined,
    env: process.env,
  });
  return Response.json(result, { status: result.ok ? 200 : 422 });
}
