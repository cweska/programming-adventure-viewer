import { getClassroomStore } from "../../../lib/classroom/store";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  let body: { name?: unknown; reportEmail?: unknown; joinCode?: unknown };
  try {
    body = (await request.json()) as { name?: unknown; reportEmail?: unknown; joinCode?: unknown };
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  if (
    typeof body.name !== "string" ||
    typeof body.reportEmail !== "string" ||
    typeof body.joinCode !== "string"
  ) {
    return Response.json({ error: "Name, report email, and join code are required." }, { status: 400 });
  }
  try {
    const classroom = getClassroomStore().createClassroom({
      name: body.name,
      reportEmail: body.reportEmail,
      joinCode: body.joinCode,
    });
    return Response.json({ classroom });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not create the classroom.";
    return Response.json({ error: message }, { status: 400 });
  }
}
