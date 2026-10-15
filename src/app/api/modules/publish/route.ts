import { getCatalog } from "../../../../lib/lesson/catalog";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  let body: { moduleId?: unknown; lessonId?: unknown };
  try {
    body = (await request.json()) as { moduleId?: unknown; lessonId?: unknown };
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  if (typeof body.moduleId !== "string" || typeof body.lessonId !== "string") {
    return Response.json({ error: "Choose a module and a lesson to publish." }, { status: 400 });
  }
  try {
    const module = getCatalog().publishLesson(body.moduleId, body.lessonId);
    return Response.json({ module });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not publish that lesson.";
    return Response.json({ error: message }, { status: 404 });
  }
}
