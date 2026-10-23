import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type { EmailMessage, Mailer } from "./mailer";
import { openClassroomStore, type ClassroomStore } from "./store";

const dirs: string[] = [];

function tempStore(): ClassroomStore {
  const dir = mkdtempSync(path.join(tmpdir(), "classroom-"));
  dirs.push(dir);
  return openClassroomStore(path.join(dir, "classroom.sqlite"));
}

afterEach(() => {
  for (const dir of dirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true });
  }
});

describe("classroom store", () => {
  it("creates a classroom, joins, resumes a beat, and saves the latest code", () => {
    const store = tempStore();
    const room = store.createClassroom({
      name: "Period 2",
      reportEmail: "t@school.edu",
      joinCode: "GATE",
    });
    expect(room.name).toBe("Period 2");
    expect(room.reportEmail).toBe("t@school.edu");
    expect(room.joinCode).toBe("GATE");

    const joined = store.join("GATE", "Mira");
    expect(joined.student.displayName).toBe("Mira");
    expect(joined.progress).toBeNull();

    store.saveProgress({
      studentId: joined.student.id,
      moduleId: "emberkeep",
      lessonId: "gate",
      beatId: "courtyard",
      status: "in_progress",
      latestCode: "return 'dark'\n",
    });

    const returning = store.join("GATE", "Mira");
    expect(returning.student.id).toBe(joined.student.id);
    expect(returning.progress?.beatId).toBe("courtyard");

    const resumed = store.resume(joined.student.id, "emberkeep");
    expect(resumed?.beatId).toBe("courtyard");

    const saved = store.saveLatestCode({
      studentId: joined.student.id,
      moduleId: "emberkeep",
      lessonId: "gate",
      beatId: "courtyard",
      code: "def light_torch(oil):\n    return 'lit'\n",
    });
    expect(saved.latestCode).toContain("light_torch");
    expect(store.resume(joined.student.id, "emberkeep")?.latestCode).toBe(saved.latestCode);
  });

  it("resumes the progress for the module being opened", () => {
    const store = tempStore();
    store.createClassroom({ name: "Period 2", reportEmail: "t@school.edu", joinCode: "LEY" });
    const student = store.join("LEY", "Mira").student;
    store.saveProgress({
      studentId: student.id,
      moduleId: "emberkeep",
      lessonId: "first-words",
      beatId: "say-shut",
      status: "in_progress",
      latestCode: "",
    });
    store.saveProgress({
      studentId: student.id,
      moduleId: "leylines-awaken",
      lessonId: "leylines-awaken",
      beatId: "program-movement",
      status: "in_progress",
      latestCode: "",
    });
    expect(store.join("LEY", "Mira", "emberkeep").progress?.beatId).toBe("say-shut");
    expect(store.join("LEY", "Mira", "leylines-awaken").progress?.beatId).toBe("program-movement");
    expect(store.join("LEY", "Mira", "training-grounds").progress).toBeNull();
  });

  it("reports one row per student per lesson", () => {
    const store = tempStore();
    const room = store.createClassroom({
      name: "Period 2",
      reportEmail: "t@school.edu",
      joinCode: "HALL",
    });
    const mira = store.join("HALL", "Mira").student;
    const sol = store.join("HALL", "Sol").student;

    store.saveProgress({
      studentId: mira.id,
      moduleId: "emberkeep",
      lessonId: "gate",
      beatId: "arrive",
      status: "in_progress",
      latestCode: "",
    });
    store.saveProgress({
      studentId: mira.id,
      moduleId: "emberkeep",
      lessonId: "hall",
      beatId: "answer",
      status: "completed",
      latestCode: "stage.say('hello')\n",
    });
    store.saveProgress({
      studentId: sol.id,
      moduleId: "emberkeep",
      lessonId: "gate",
      beatId: "courtyard",
      status: "in_progress",
      latestCode: "",
    });

    const rows = store.report(room.id);
    expect(rows).toHaveLength(3);
    expect(rows.filter((row) => row.displayName === "Mira")).toHaveLength(2);
    expect(rows.filter((row) => row.displayName === "Sol")).toHaveLength(1);
    const completed = rows.find((row) => row.lessonId === "hall");
    expect(completed?.completed).toBe(true);
    expect(completed?.beatId).toBe("answer");
  });

  it("emails lesson completion only when SMTP is configured", async () => {
    const store = tempStore();
    store.createClassroom({
      name: "Period 2",
      reportEmail: "t@school.edu",
      joinCode: "MAIL",
    });
    const student = store.join("MAIL", "Mira").student;
    const sent: EmailMessage[] = [];
    const mailer: Mailer = {
      send(message) {
        sent.push(message);
      },
    };
    const input = {
      studentId: student.id,
      moduleId: "emberkeep",
      lessonId: "gate",
      beatId: "answer",
      latestCode: "stage.say('done')\n",
    };

    const quiet = await store.completeLesson(input, { env: {}, mailer });
    expect(quiet.emailed).toBe(false);
    expect(sent).toHaveLength(0);
    expect(store.report(store.findByJoinCode("MAIL")!.id)[0]?.completed).toBe(true);

    const sentMail = await store.completeLesson(input, {
      env: {
        SMTP_HOST: "smtp.example",
        SMTP_PORT: "2525",
        SMTP_FROM: "theater@example.com",
      },
      mailer,
    });
    expect(sentMail.emailed).toBe(true);
    expect(sent).toHaveLength(1);
    expect(sent[0]?.to).toBe("t@school.edu");
    expect(sent[0]?.text).toContain("Mira");
    expect(sent[0]?.text).toContain("gate");
  });
});
