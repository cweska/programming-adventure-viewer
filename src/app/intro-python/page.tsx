import type { Metadata } from "next";
import { CourseMap } from "../../components/course/CourseMap";
import { allUnits, courseMeta, glossaryForTexts, unitOutline } from "../../lib/course/registry";

export const metadata: Metadata = {
  title: "Intro to Python · Emberkeep",
  description: "Learn the Python you need for the adventure, with Mar'tu.",
};

export default function IntroPythonPage() {
  // Every unit goes to the client as an outline (titles, item kinds, exercise ids); the map hides
  // unpublished ones unless ?preview=1.
  const units = allUnits.map((unit) => ({ ...unitOutline(unit), goals: unit.goals }));
  const glossary = glossaryForTexts([courseMeta.intro, ...allUnits.flatMap((unit) => unit.goals)]);
  return <CourseMap title={courseMeta.title} intro={courseMeta.intro} units={units} glossary={glossary} />;
}
