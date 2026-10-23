import fs from "node:fs";
import path from "node:path";
import Database from "better-sqlite3";
import { isSmtpConfigured, type Mailer } from "./mailer";

export type Classroom = {
  id: string;
  name: string;
  reportEmail: string;
  joinCode: string;
  createdAt: string;
};

export type Student = {
  id: string;
  classroomId: string;
  displayName: string;
  createdAt: string;
};

export type ProgressStatus = "in_progress" | "completed";

export type Progress = {
  classroomId: string;
  studentId: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: ProgressStatus;
  latestCode: string;
  updatedAt: string;
};

export type ReportRow = {
  studentId: string;
  displayName: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: ProgressStatus;
  completed: boolean;
  updatedAt: string;
};

export type JoinResult = {
  classroom: Classroom;
  student: Student;
  progress: Progress | null;
};

export type ProgressInput = {
  studentId: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: ProgressStatus;
  latestCode: string;
};

export type CompletionOptions = {
  env: Record<string, string | undefined>;
  mailer?: Mailer | null;
};

export interface ClassroomStore {
  createClassroom(input: { name: string; reportEmail: string; joinCode: string }): Classroom;
  join(joinCode: string, displayName: string, moduleId?: string): JoinResult;
  resume(studentId: string, moduleId: string): Progress | null;
  saveLatestCode(input: {
    studentId: string;
    moduleId: string;
    lessonId: string;
    beatId: string;
    code: string;
  }): Progress;
  saveProgress(input: ProgressInput): Progress;
  report(classroomId: string): ReportRow[];
  findByJoinCode(joinCode: string): Classroom | null;
  completeLesson(
    input: {
      studentId: string;
      moduleId: string;
      lessonId: string;
      beatId: string;
      latestCode: string;
    },
    options: CompletionOptions,
  ): Promise<{ emailed: boolean }>;
}

type ClassroomRow = {
  id: string;
  name: string;
  report_email: string;
  join_code: string;
  created_at: string;
};

type StudentRow = {
  id: string;
  classroom_id: string;
  display_name: string;
  created_at: string;
};

type ProgressRow = {
  classroom_id: string;
  student_id: string;
  module_id: string;
  lesson_id: string;
  beat_id: string;
  status: ProgressStatus;
  latest_code: string;
  updated_at: string;
};

function mapClassroom(row: ClassroomRow): Classroom {
  return {
    id: row.id,
    name: row.name,
    reportEmail: row.report_email,
    joinCode: row.join_code,
    createdAt: row.created_at,
  };
}

function mapStudent(row: StudentRow): Student {
  return {
    id: row.id,
    classroomId: row.classroom_id,
    displayName: row.display_name,
    createdAt: row.created_at,
  };
}

function mapProgress(row: ProgressRow): Progress {
  return {
    classroomId: row.classroom_id,
    studentId: row.student_id,
    moduleId: row.module_id,
    lessonId: row.lesson_id,
    beatId: row.beat_id,
    status: row.status,
    latestCode: row.latest_code,
    updatedAt: row.updated_at,
  };
}

function required(value: string, label: string): string {
  const trimmed = value.trim();
  if (!trimmed) throw new Error(`${label} is required.`);
  return trimmed;
}

export function openClassroomStore(filename: string): ClassroomStore {
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  const db = new Database(filename);
  db.pragma("journal_mode = WAL");
  db.exec(`
    CREATE TABLE IF NOT EXISTS classrooms (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      report_email TEXT NOT NULL,
      join_code TEXT NOT NULL UNIQUE,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS students (
      id TEXT PRIMARY KEY,
      classroom_id TEXT NOT NULL,
      display_name TEXT NOT NULL,
      created_at TEXT NOT NULL,
      UNIQUE (classroom_id, display_name),
      FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
    );
    CREATE TABLE IF NOT EXISTS progress (
      student_id TEXT NOT NULL,
      classroom_id TEXT NOT NULL,
      module_id TEXT NOT NULL,
      lesson_id TEXT NOT NULL,
      beat_id TEXT NOT NULL,
      status TEXT NOT NULL,
      latest_code TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      PRIMARY KEY (student_id, module_id, lesson_id),
      FOREIGN KEY (student_id) REFERENCES students(id),
      FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
    );
  `);

  const insertClassroom = db.prepare(
    `INSERT INTO classrooms (id, name, report_email, join_code, created_at)
     VALUES (@id, @name, @report_email, @join_code, @created_at)`,
  );
  const classroomByCode = db.prepare(`SELECT * FROM classrooms WHERE join_code = ?`);
  const classroomById = db.prepare(`SELECT * FROM classrooms WHERE id = ?`);
  const studentByName = db.prepare(
    `SELECT * FROM students WHERE classroom_id = ? AND display_name = ?`,
  );
  const studentById = db.prepare(`SELECT * FROM students WHERE id = ?`);
  const insertStudent = db.prepare(
    `INSERT INTO students (id, classroom_id, display_name, created_at)
     VALUES (@id, @classroom_id, @display_name, @created_at)`,
  );
  const latestForStudent = db.prepare(
    `SELECT * FROM progress WHERE student_id = ? ORDER BY updated_at DESC LIMIT 1`,
  );
  const resumeRow = db.prepare(
    `SELECT * FROM progress WHERE student_id = ? AND module_id = ? ORDER BY updated_at DESC LIMIT 1`,
  );
  const upsertProgress = db.prepare(`
    INSERT INTO progress (
      student_id, classroom_id, module_id, lesson_id, beat_id, status, latest_code, updated_at
    ) VALUES (
      @student_id, @classroom_id, @module_id, @lesson_id, @beat_id, @status, @latest_code, @updated_at
    )
    ON CONFLICT(student_id, module_id, lesson_id) DO UPDATE SET
      beat_id = excluded.beat_id,
      status = excluded.status,
      latest_code = excluded.latest_code,
      updated_at = excluded.updated_at
  `);
  const reportRows = db.prepare(`
    SELECT
      s.id AS student_id,
      s.display_name,
      p.module_id,
      p.lesson_id,
      p.beat_id,
      p.status,
      p.updated_at
    FROM progress p
    JOIN students s ON s.id = p.student_id
    WHERE p.classroom_id = ?
    ORDER BY s.display_name COLLATE NOCASE, p.module_id, p.lesson_id
  `);

  function requireStudent(studentId: string): StudentRow {
    const student = studentById.get(studentId) as StudentRow | undefined;
    if (!student) throw new Error("Unknown student.");
    return student;
  }

  function writeProgress(input: ProgressInput): Progress {
    const student = requireStudent(input.studentId);
    const updatedAt = new Date().toISOString();
    upsertProgress.run({
      student_id: student.id,
      classroom_id: student.classroom_id,
      module_id: required(input.moduleId, "Module"),
      lesson_id: required(input.lessonId, "Lesson"),
      beat_id: required(input.beatId, "Part"),
      status: input.status,
      latest_code: input.latestCode ?? "",
      updated_at: updatedAt,
    });
    const row = db
      .prepare(
        `SELECT * FROM progress WHERE student_id = ? AND module_id = ? AND lesson_id = ?`,
      )
      .get(student.id, input.moduleId, input.lessonId) as ProgressRow;
    return mapProgress(row);
  }

  return {
    createClassroom(input) {
      const name = required(input.name, "Classroom name");
      const reportEmail = required(input.reportEmail, "Report email");
      const joinCode = required(input.joinCode, "Join code");
      if (!reportEmail.includes("@")) {
        throw new Error("Report email must look like an email address.");
      }
      if (classroomByCode.get(joinCode)) {
        throw new Error("That join code is already in use.");
      }
      const classroom: ClassroomRow = {
        id: crypto.randomUUID(),
        name,
        report_email: reportEmail,
        join_code: joinCode,
        created_at: new Date().toISOString(),
      };
      insertClassroom.run(classroom);
      return mapClassroom(classroom);
    },

    join(joinCode, displayName, moduleId) {
      const code = required(joinCode, "Join code");
      const name = required(displayName, "Display name");
      const classroom = classroomByCode.get(code) as ClassroomRow | undefined;
      if (!classroom) throw new Error("That join code does not match a classroom.");
      let student = studentByName.get(classroom.id, name) as StudentRow | undefined;
      if (!student) {
        student = {
          id: crypto.randomUUID(),
          classroom_id: classroom.id,
          display_name: name,
          created_at: new Date().toISOString(),
        };
        insertStudent.run(student);
      }
      const progress = (moduleId ? resumeRow.get(student.id, moduleId) : latestForStudent.get(student.id)) as
        | ProgressRow
        | undefined;
      return {
        classroom: mapClassroom(classroom),
        student: mapStudent(student),
        progress: progress ? mapProgress(progress) : null,
      };
    },

    resume(studentId, moduleId) {
      const row = resumeRow.get(studentId, moduleId) as ProgressRow | undefined;
      return row ? mapProgress(row) : null;
    },

    saveLatestCode(input) {
      const existing = db
        .prepare(
          `SELECT * FROM progress WHERE student_id = ? AND module_id = ? AND lesson_id = ?`,
        )
        .get(input.studentId, input.moduleId, input.lessonId) as ProgressRow | undefined;
      return writeProgress({
        studentId: input.studentId,
        moduleId: input.moduleId,
        lessonId: input.lessonId,
        beatId: input.beatId || existing?.beat_id || "",
        status: existing?.status ?? "in_progress",
        latestCode: input.code,
      });
    },

    saveProgress(input) {
      return writeProgress(input);
    },

    report(classroomId) {
      const rows = reportRows.all(classroomId) as Array<{
        student_id: string;
        display_name: string;
        module_id: string;
        lesson_id: string;
        beat_id: string;
        status: ProgressStatus;
        updated_at: string;
      }>;
      return rows.map((row) => ({
        studentId: row.student_id,
        displayName: row.display_name,
        moduleId: row.module_id,
        lessonId: row.lesson_id,
        beatId: row.beat_id,
        status: row.status,
        completed: row.status === "completed",
        updatedAt: row.updated_at,
      }));
    },

    findByJoinCode(joinCode) {
      const row = classroomByCode.get(joinCode.trim()) as ClassroomRow | undefined;
      return row ? mapClassroom(row) : null;
    },

    async completeLesson(input, options) {
      const saved = writeProgress({
        studentId: input.studentId,
        moduleId: input.moduleId,
        lessonId: input.lessonId,
        beatId: input.beatId,
        status: "completed",
        latestCode: input.latestCode,
      });
      if (!isSmtpConfigured(options.env) || !options.mailer) {
        return { emailed: false };
      }
      const student = requireStudent(input.studentId);
      const classroom = classroomById.get(student.classroom_id) as ClassroomRow;
      await options.mailer.send({
        to: classroom.report_email,
        subject: `Lesson complete: ${student.display_name}`,
        text: [
          `Classroom: ${classroom.name}`,
          `Student: ${student.display_name}`,
          `Module: ${saved.moduleId}`,
          `Lesson: ${saved.lessonId}`,
          `Part: ${saved.beatId}`,
          "The lesson is complete.",
        ].join("\n"),
      });
      return { emailed: true };
    },
  };
}

const globalStore = globalThis as typeof globalThis & { __classroomStore?: ClassroomStore };

export function getClassroomStore(): ClassroomStore {
  if (!globalStore.__classroomStore) {
    globalStore.__classroomStore = openClassroomStore(
      path.join(process.cwd(), "data", "classroom.sqlite"),
    );
  }
  return globalStore.__classroomStore;
}
