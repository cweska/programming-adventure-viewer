import emberkeep from "../../../content/modules/emberkeep/first-words.json";
import leylinesAwaken from "../../../content/modules/leylines-awaken/module.json";
import trainingGrounds from "../../../content/modules/training-grounds/module.json";
import { moduleSchema, type Module } from "./schema";

export const bundledModules: Module[] = [emberkeep, leylinesAwaken, trainingGrounds].map((raw) =>
  moduleSchema.parse(raw),
);

export function findModule(id: string): Module | undefined {
  return bundledModules.find((module) => module.id === id);
}

export function studentModules(modules: Module[] = bundledModules): Module[] {
  return modules
    .filter((module) => module.lessons.some((lesson) => lesson.published))
    .slice()
    .sort((left, right) => {
      const leftOrder = left.campaign?.order ?? Number.POSITIVE_INFINITY;
      const rightOrder = right.campaign?.order ?? Number.POSITIVE_INFINITY;
      return leftOrder - rightOrder;
    });
}
