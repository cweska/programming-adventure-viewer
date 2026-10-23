import { getClassroomStore } from "../../../../lib/classroom/store";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  let body: { joinCode?: unknown; displayName?: unknown; moduleId?: unknown };
  try {
    body = (await request.json()) as { joinCode?: unknown; displayName?: unknown; moduleId?: unknown };
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  if (typeof body.joinCode !== "string" || typeof body.displayName !== "string") {
    return Response.json({ error: "A display name and join code are required." }, { status: 400 });
  }
  try {
    const moduleId = typeof body.moduleId === "string" ? body.moduleId : undefined;
    const result = getClassroomStore().join(body.joinCode, body.displayName, moduleId);
    return Response.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not join that classroom.";
    return Response.json({ error: message }, { status: 404 });
  }
}
