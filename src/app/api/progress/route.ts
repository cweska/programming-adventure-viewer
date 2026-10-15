import { createSmtpMailer } from "../../../lib/classroom/mailer";
import { getClassroomStore, type ProgressStatus } from "../../../lib/classroom/store";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type ProgressBody = {
  studentId?: unknown;
  moduleId?: unknown;
  lessonId?: unknown;
  beatId?: unknown;
  status?: unknown;
  latestCode?: unknown;
  preview?: unknown;
};

export async function POST(request: Request) {
  let body: ProgressBody;
  try {
    body = (await request.json()) as ProgressBody;
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  if (body.preview === true) {
    return Response.json({ saved: false, emailed: false });
  }
  if (
    typeof body.studentId !== "string" ||
    typeof body.moduleId !== "string" ||
    typeof body.lessonId !== "string" ||
    typeof body.beatId !== "string" ||
    (body.status !== "in_progress" && body.status !== "completed")
  ) {
    return Response.json({ error: "Progress is missing a student, lesson, or beat." }, { status: 400 });
  }
  const latestCode = typeof body.latestCode === "string" ? body.latestCode : "";
  const store = getClassroomStore();
  try {
    if (body.status === "completed") {
      const mailer = createSmtpMailer(process.env);
      const result = await store.completeLesson(
        {
          studentId: body.studentId,
          moduleId: body.moduleId,
          lessonId: body.lessonId,
          beatId: body.beatId,
          latestCode,
        },
        { env: process.env, mailer },
      );
      return Response.json({ saved: true, ...result });
    }
    const status: ProgressStatus = "in_progress";
    store.saveProgress({
      studentId: body.studentId,
      moduleId: body.moduleId,
      lessonId: body.lessonId,
      beatId: body.beatId,
      status,
      latestCode,
    });
    return Response.json({ saved: true, emailed: false });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not save progress.";
    return Response.json({ error: message }, { status: 400 });
  }
}
