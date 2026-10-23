import { describe, expect, it } from "vitest";
import { createLocalClassroomStore, type KeyValueStorage } from "./local-store";

function memoryStorage(): KeyValueStorage {
  const values = new Map<string, string>();
  return {
    getItem(key) {
      return values.get(key) ?? null;
    },
    setItem(key, value) {
      values.set(key, value);
    },
  };
}

describe("browser classroom store", () => {
  it("keeps a class, a student, and a report in one browser", () => {
    const store = createLocalClassroomStore(memoryStorage());
    const room = store.createClassroom({
      name: "Period 2",
      reportEmail: "teacher@example.com",
      joinCode: "GATE",
    });
    expect(store.report(room.id)).toEqual([]);

    const joined = store.join("GATE", "Mira");
    expect(joined.student.displayName).toBe("Mira");
    expect(joined.progress).toBeNull();

    store.saveProgress({
      studentId: joined.student.id,
      moduleId: "emberkeep",
      lessonId: "first-words",
      beatId: "say-shut",
      status: "in_progress",
      latestCode: 'print("The gate is shut.")\n',
    });

    const returning = store.join("GATE", "Mira");
    expect(returning.student.id).toBe(joined.student.id);
    expect(returning.progress?.beatId).toBe("say-shut");
    expect(returning.progress?.status).toBe("in_progress");

    const rows = store.report(room.id);
    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      displayName: "Mira",
      lessonId: "first-words",
      beatId: "say-shut",
      completed: false,
    });
  });

  it("resumes the progress for the module being opened", () => {
    const store = createLocalClassroomStore(memoryStorage());
    store.createClassroom({ name: "Period 2", reportEmail: "teacher@example.com", joinCode: "GATE" });
    const student = store.join("GATE", "Mira").student;
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
    expect(store.join("GATE", "Mira", "emberkeep").progress?.beatId).toBe("say-shut");
    expect(store.join("GATE", "Mira", "leylines-awaken").progress?.beatId).toBe("program-movement");
    expect(store.join("GATE", "Mira", "training-grounds").progress).toBeNull();
  });

  it("does not share data across storage buckets", () => {
    const first = createLocalClassroomStore(memoryStorage());
    const second = createLocalClassroomStore(memoryStorage());
    first.createClassroom({
      name: "Period 2",
      reportEmail: "teacher@example.com",
      joinCode: "GATE",
    });
    expect(() => second.join("GATE", "Mira")).toThrow(/does not match/);
  });

  it("rejects a duplicate join code and a missing class", () => {
    const store = createLocalClassroomStore(memoryStorage());
    store.createClassroom({
      name: "Period 2",
      reportEmail: "teacher@example.com",
      joinCode: "GATE",
    });
    expect(() =>
      store.createClassroom({
        name: "Period 3",
        reportEmail: "other@example.com",
        joinCode: "GATE",
      }),
    ).toThrow(/already in use/);
    expect(store.findByJoinCode("MISSING")).toBeNull();
  });
});
