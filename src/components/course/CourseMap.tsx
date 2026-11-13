"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { coursePreset, unitProgress, useCourseProgress, type ProgressUnit, type UnitProgress } from "../../lib/course/progress";
import type { GlossaryEntry } from "../../lib/course/schema";
import { ProgressBar } from "./CourseBits";
import { unitHref } from "./course-links";
import { CourseSettings, PlacementQuestion } from "./CourseSettings";
import { MarTu } from "./MarTu";
import { Prose } from "./Prose";

export type MapUnit = ProgressUnit & { goals: string[] };

export type CourseMapProps = {
  title: string;
  intro: string;
  /** Every unit in order, unpublished ones too (hidden unless ?preview=1). */
  units: MapUnit[];
  glossary: GlossaryEntry[];
};

/** ?preview=1, read in the browser (static pages cannot vary by query string). */
export function usePreviewFlag(): boolean {
  const [preview, setPreview] = useState(false);
  useEffect(() => {
    try {
      setPreview(new URLSearchParams(window.location.search).get("preview") === "1");
    } catch {
      setPreview(false);
    }
  }, []);
  return preview;
}

export function unitStatusText(progress: UnitProgress): string {
  if (progress.testedOut) return "Tested out";
  if (progress.complete) return "Complete";
  if (!progress.started) return "Not started";
  return `${progress.done} of ${progress.total} done`;
}

function unitAction(progress: UnitProgress): string {
  if (progress.complete) return "Review";
  if (progress.started) return "Continue";
  return "Start";
}

/** The course map: Mar'tu's welcome, then every unit in order with its progress. */
export function CourseMap({ title, intro, units, glossary }: CourseMapProps) {
  const progress = useCourseProgress();
  const preview = usePreviewFlag();
  const visible = units.filter((unit) => preview || unit.published);
  const stats = visible.map((unit) => ({ unit, progress: unitProgress(unit, progress) }));
  const nextUp = stats.find((entry) => !entry.progress.complete)?.unit.id;

  return (
    <main className="course-page" data-testid="course-map">
      <header className="course-hero">
        <div>
          <p className="course-eyebrow">Mar&apos;tu&apos;s lessons</p>
          <h1>{title}</h1>
        </div>
        <CourseSettings />
      </header>

      {preview ? (
        <p className="course-banner" data-testid="preview-banner">
          Teacher preview: units that are not published yet are shown too.
        </p>
      ) : null}

      <PlacementQuestion />

      <MarTu text={intro} glossary={glossary} light={coursePreset(progress.settings) === "short"} />

      <section aria-labelledby="course-units-title" className="course-units">
        <h2 id="course-units-title">Units</h2>
        {stats.length === 0 ? (
          <p className="course-empty" data-testid="course-empty">
            Mar&apos;tu is still writing the first unit. Check back soon.
          </p>
        ) : (
          <ol className="unit-list">
            {stats.map(({ unit, progress: unitStats }) => {
              const isNext = unit.id === nextUp;
              return (
                <li
                  key={unit.id}
                  className={`unit-card${isNext ? " is-next" : ""}${unitStats.complete ? " is-complete" : ""}`}
                  data-testid={`unit-card-${unit.id}`}
                >
                  <div className="unit-card-head">
                    <p className="unit-number">Unit {unit.order}</p>
                    {isNext ? <span className="next-up">Next up</span> : null}
                    {!unit.published ? <span className="draft-tag">Not published</span> : null}
                  </div>
                  <h3>
                    <Link href={unitHref(unit.id)} data-testid={`unit-link-${unit.id}`}>
                      {unit.title}
                    </Link>
                  </h3>
                  {unit.subtitle ? <p className="unit-subtitle">{unit.subtitle}</p> : null}
                  {unit.goals.length > 0 ? (
                    <ul className="unit-goals">
                      {unit.goals.map((goal, index) => (
                        <li key={index}>
                          <Prose text={goal} glossary={glossary} inline />
                        </li>
                      ))}
                    </ul>
                  ) : null}
                  <div className="unit-card-foot">
                    <ProgressBar percent={unitStats.percent} label={`${unit.title} progress`} />
                    <p className="unit-status" data-testid={`unit-status-${unit.id}`}>
                      {unitStatusText(unitStats)}
                    </p>
                    <Link
                      className="course-button"
                      href={unitHref(unit.id)}
                      data-testid={`unit-begin-${unit.id}`}
                      aria-label={`${unitAction(unitStats)} ${unit.title}`}
                    >
                      {unitAction(unitStats)}
                    </Link>
                  </div>
                </li>
              );
            })}
          </ol>
        )}
      </section>
    </main>
  );
}
