import Link from "next/link";
import type { Module } from "../lib/lesson/schema";

function partCount(module: Module): number {
  return module.lessons
    .filter((lesson) => lesson.published)
    .reduce((total, lesson) => total + lesson.beats.length, 0);
}

export function ModulePicker({ modules }: { modules: Module[] }) {
  return (
    <main className="column">
      <section className="picker-intro">
        <h1>Choose today&apos;s module</h1>
        <p>Your teacher will tell you which module the party plays today.</p>
      </section>
      <ul className="module-list" data-testid="module-list">
        {modules.map((module) => (
          <li key={module.id} className="module-card" data-testid={`module-card-${module.id}`}>
            <p className="module-label">{module.campaign?.label ?? "Warm-up"}</p>
            <h2>{module.title}</h2>
            {module.summary ? <p className="module-summary">{module.summary}</p> : null}
            <p className="module-parts">{partCount(module)} parts</p>
            <Link className="module-begin" href={`/play/${module.id}`} data-testid={`begin-${module.id}`}>
              Begin
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
