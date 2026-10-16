const STORAGE_KEY = "emberkeep-classroom-local";

export type LocalClassroom = {
  id: string;
  name: string;
  reportEmail: string;
  joinCode: string;
  createdAt: string;
};

export type LocalStudent = {
  id: string;
  classroomId: string;
  displayName: string;
  createdAt: string;
};

export type LocalProgress = {
  classroomId: string;
  studentId: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: "in_progress" | "completed";
  latestCode: string;
  updatedAt: string;
};

export type LocalReportRow = {
  studentId: string;
  displayName: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: "in_progress" | "completed";
  completed: boolean;
  updatedAt: string;
};

type Database = {
  classrooms: LocalClassroom[];
  students: LocalStudent[];
  progress: LocalProgress[];
};

export type KeyValueStorage = {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
};

function required(value: string, label: string): string {
  const trimmed = value.trim();
  if (!trimmed) throw new Error(`${label} is required.`);
  return trimmed;
}

function emptyDatabase(): Database {
  return { classrooms: [], students: [], progress: [] };
}

function readDatabase(storage: KeyValueStorage): Database {
  const raw = storage.getItem(STORAGE_KEY);
  if (!raw) return emptyDatabase();
  try {
    const parsed = JSON.parse(raw) as Partial<Database>;
    return {
      classrooms: Array.isArray(parsed.classrooms) ? parsed.classrooms : [],
      students: Array.isArray(parsed.students) ? parsed.students : [],
      progress: Array.isArray(parsed.progress) ? parsed.progress : [],
    };
  } catch {
    return emptyDatabase();
  }
}

function writeDatabase(storage: KeyValueStorage, database: Database) {
  storage.setItem(STORAGE_KEY, JSON.stringify(database));
}

function latestProgress(database: Database, studentId: string): LocalProgress | null {
  const rows = database.progress.filter((item) => item.studentId === studentId);
  if (rows.length === 0) return null;
  return rows.reduce((latest, item) => (item.updatedAt > latest.updatedAt ? item : latest));
}

export function createLocalClassroomStore(storage: KeyValueStorage) {
  return {
    createClassroom(input: { name: string; reportEmail: string; joinCode: string }): LocalClassroom {
      const name = required(input.name, "Classroom name");
      const reportEmail = required(input.reportEmail, "Report email");
      const joinCode = required(input.joinCode, "Join code");
      if (!reportEmail.includes("@")) {
        throw new Error("Report email must look like an email address.");
      }
      const database = readDatabase(storage);
      if (database.classrooms.some((room) => room.joinCode === joinCode)) {
        throw new Error("That join code is already in use.");
      }
      const classroom: LocalClassroom = {
        id: crypto.randomUUID(),
        name,
        reportEmail,
        joinCode,
        createdAt: new Date().toISOString(),
      };
      database.classrooms.push(classroom);
      writeDatabase(storage, database);
      return classroom;
    },

    join(joinCode: string, displayName: string) {
      const code = required(joinCode, "Join code");
      const name = required(displayName, "Display name");
      const database = readDatabase(storage);
      const classroom = database.classrooms.find((room) => room.joinCode === code);
      if (!classroom) throw new Error("That join code does not match a classroom.");
      let student = database.students.find(
        (item) => item.classroomId === classroom.id && item.displayName === name,
      );
      if (!student) {
        student = {
          id: crypto.randomUUID(),
          classroomId: classroom.id,
          displayName: name,
          createdAt: new Date().toISOString(),
        };
        database.students.push(student);
        writeDatabase(storage, database);
      }
      return {
        classroom,
        student,
        progress: latestProgress(readDatabase(storage), student.id),
      };
    },

    saveProgress(input: {
      studentId: string;
      moduleId: string;
      lessonId: string;
      beatId: string;
      status: "in_progress" | "completed";
      latestCode: string;
    }): LocalProgress {
      const database = readDatabase(storage);
      const student = database.students.find((item) => item.id === input.studentId);
      if (!student) throw new Error("Unknown student.");
      const moduleId = required(input.moduleId, "Module");
      const lessonId = required(input.lessonId, "Lesson");
      const beatId = required(input.beatId, "Part");
      const next: LocalProgress = {
        classroomId: student.classroomId,
        studentId: student.id,
        moduleId,
        lessonId,
        beatId,
        status: input.status,
        latestCode: input.latestCode ?? "",
        updatedAt: new Date().toISOString(),
      };
      const index = database.progress.findIndex(
        (item) => item.studentId === student.id && item.moduleId === moduleId && item.lessonId === lessonId,
      );
      if (index >= 0) database.progress[index] = next;
      else database.progress.push(next);
      writeDatabase(storage, database);
      return next;
    },

    findByJoinCode(joinCode: string): LocalClassroom | null {
      const code = joinCode.trim();
      return readDatabase(storage).classrooms.find((room) => room.joinCode === code) ?? null;
    },

    report(classroomId: string): LocalReportRow[] {
      const database = readDatabase(storage);
      const rows = database.progress
        .filter((item) => item.classroomId === classroomId)
        .map((item) => {
          const student = database.students.find((entry) => entry.id === item.studentId);
          return {
            studentId: item.studentId,
            displayName: student?.displayName ?? "",
            moduleId: item.moduleId,
            lessonId: item.lessonId,
            beatId: item.beatId,
            status: item.status,
            completed: item.status === "completed",
            updatedAt: item.updatedAt,
          };
        });
      rows.sort((left, right) => {
        const byName = left.displayName.localeCompare(right.displayName, undefined, { sensitivity: "base" });
        if (byName !== 0) return byName;
        const byModule = left.moduleId.localeCompare(right.moduleId);
        if (byModule !== 0) return byModule;
        return left.lessonId.localeCompare(right.lessonId);
      });
      return rows;
    },
  };
}

let browserStore: ReturnType<typeof createLocalClassroomStore> | null = null;

export function localClassroomStore() {
  if (typeof window === "undefined") {
    throw new Error("Classroom storage is only available in the browser.");
  }
  if (!browserStore) browserStore = createLocalClassroomStore(window.localStorage);
  return browserStore;
}

function message(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

export function createClassroomInBrowser(input: { name: string; reportEmail: string; joinCode: string }) {
  try {
    return { classroom: localClassroomStore().createClassroom(input) };
  } catch (error) {
    return { error: message(error, "Could not create the classroom.") };
  }
}

export function joinClassroomInBrowser(displayName: string, joinCode: string) {
  try {
    const result = localClassroomStore().join(joinCode, displayName);
    return {
      student: {
        id: result.student.id,
        displayName: result.student.displayName,
        classroomId: result.student.classroomId,
      },
      progress: result.progress,
    };
  } catch (error) {
    return { error: message(error, "Could not join that classroom.") };
  }
}

export function saveProgressInBrowser(input: {
  studentId: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: "in_progress" | "completed";
  latestCode: string;
}) {
  localClassroomStore().saveProgress(input);
}

export function reportClassroomInBrowser(code: string) {
  try {
    const classroom = localClassroomStore().findByJoinCode(code);
    if (!classroom) return { error: "That join code does not match a classroom." };
    return { classroom, rows: localClassroomStore().report(classroom.id) };
  } catch (error) {
    return { error: message(error, "Could not load that report.") };
  }
}
