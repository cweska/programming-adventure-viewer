import { getClassroomStore } from "../../../../lib/classroom/store";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type CodeBody = {
  studentId?: unknown;
  moduleId?: unknown;
  lessonId?: unknown;
  beatId?: unknown;
  code?: unknown;
};

// Keeps the code a student has typed but not run yet, so it is there when they come back.
export async function POST(request: Request) {
  let body: CodeBody;
  try {
    body = (await request.json()) as CodeBody;
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  if (
    typeof body.studentId !== "string" ||
    typeof body.moduleId !== "string" ||
    typeof body.lessonId !== "string" ||
    typeof body.beatId !== "string" ||
    typeof body.code !== "string"
  ) {
    return Response.json({ error: "The code is missing a student, lesson, or part." }, { status: 400 });
  }
  try {
    getClassroomStore().saveLatestCode({
      studentId: body.studentId,
      moduleId: body.moduleId,
      lessonId: body.lessonId,
      beatId: body.beatId,
      code: body.code,
    });
    return Response.json({ saved: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not save the code.";
    return Response.json({ error: message }, { status: 400 });
  }
}
