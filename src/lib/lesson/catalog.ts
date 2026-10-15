import fs from "node:fs";
import path from "node:path";
import { moduleSchema, type Module } from "./schema";

export type Catalog = {
  loadAll(): Module[];
  forStudents(): Module[];
  save(module: Module): Module;
  publishLesson(moduleId: string, lessonId: string): Module;
};

function readModules(dir: string, into: Map<string, Module>) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      readModules(full, into);
      continue;
    }
    if (!entry.name.endsWith(".json")) continue;
    const parsed = moduleSchema.parse(JSON.parse(fs.readFileSync(full, "utf8")));
    into.set(parsed.id, parsed);
  }
}

export function createCatalog(root: string): Catalog {
  const contentDir = path.join(root, "content");
  const dataDir = path.join(root, "data", "modules");

  function loadAll(): Module[] {
    const modules = new Map<string, Module>();
    readModules(contentDir, modules);
    readModules(dataDir, modules);
    return [...modules.values()];
  }

  function save(module: Module): Module {
    const parsed = moduleSchema.parse(module);
    fs.mkdirSync(dataDir, { recursive: true });
    fs.writeFileSync(path.join(dataDir, `${parsed.id}.json`), `${JSON.stringify(parsed, null, 2)}\n`);
    return parsed;
  }

  return {
    loadAll,
    forStudents() {
      return loadAll()
        .map((module) => ({
          ...module,
          lessons: module.lessons.filter((lesson) => lesson.published),
        }))
        .filter((module) => module.lessons.length > 0);
    },
    save,
    publishLesson(moduleId, lessonId) {
      const module = loadAll().find((item) => item.id === moduleId);
      if (!module) throw new Error("Unknown module.");
      const lesson = module.lessons.find((item) => item.id === lessonId);
      if (!lesson) throw new Error("Unknown lesson.");
      lesson.published = true;
      return save(module);
    },
  };
}

export function getCatalog(): Catalog {
  return createCatalog(process.cwd());
}
