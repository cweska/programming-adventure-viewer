import { getClassroomStore } from "../../../../lib/classroom/store";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export function GET(request: Request) {
  const code = new URL(request.url).searchParams.get("code") ?? "";
  const store = getClassroomStore();
  const classroom = store.findByJoinCode(code);
  if (!classroom) {
    return Response.json({ error: "That join code does not match a classroom." }, { status: 404 });
  }
  return Response.json({ classroom, rows: store.report(classroom.id) });
}
