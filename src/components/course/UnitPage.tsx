"use client";

import Link from "next/link";
import {
  coursePreset,
  itemStatus,
  nextUpItem,
  unitProgress,
  useCourseProgress,
  type ProgressItem,
  type ProgressUnit,
} from "../../lib/course/progress";
import type { GlossaryEntry } from "../../lib/course/schema";
import { Breadcrumbs, KindBadge, ProgressBar, StatusBadge, unitLabel } from "./CourseBits";
import { COURSE_HREF, itemHref } from "./course-links";
import { unitStatusText } from "./CourseMap";
import { CourseSettings } from "./CourseSettings";
import { MarTu } from "./MarTu";
import { Prose } from "./Prose";

export type UnitPageProps = {
  unit: ProgressUnit & { martuIntro: string; goals: string[] };
  /** Campaign modules this unit prepares for (id and title). */
  campaign: { id: string; title: string }[];
  glossary: GlossaryEntry[];
};

type QuickCheckForm = { form: ProgressItem; questions?: ProgressItem };

/** The rest of the Quick Check: the first form's questions, and the other forms for a fresh try. */
function QuickCheckMore({ unitId, forms }: { unitId: string; forms: QuickCheckForm[] }) {
  const [first, ...others] = forms;
  if (!first || (!first.questions && others.length === 0)) return null;
  return (
    <p className="quick-check-more" data-testid="quick-check-more">
      {first.questions && first.form.questionsToPass ? (
        // The questions count (questionsToPass): say so, with the number.
        <>
          To pass, finish the tasks, then get {first.form.questionsToPass} of the{" "}
          {first.questions.questionCount ?? ""}{" "}
          <Link href={itemHref(unitId, first.questions.id)} data-testid={`quick-check-link-${first.questions.id}`}>
            Quick Check questions
          </Link>{" "}
          right.{" "}
        </>
      ) : first.questions ? (
        <>
          After the tasks, try{" "}
          <Link href={itemHref(unitId, first.questions.id)} data-testid={`quick-check-link-${first.questions.id}`}>
            the Quick Check questions
          </Link>{" "}
          too, for practice: they don&apos;t change your pass.{" "}
        </>
      ) : null}
      {others.map(({ form, questions }) => (
        <span key={form.id}>
          Want different tasks? Try{" "}
          <Link href={itemHref(unitId, form.id)} data-testid={`quick-check-link-${form.id}`}>
            {formLabel(form.title ?? "another form")}
          </Link>
          {questions ? (
            <>
              {" "}
              and{" "}
              <Link href={itemHref(unitId, questions.id)} data-testid={`quick-check-link-${questions.id}`}>
                its questions
              </Link>
            </>
          ) : null}
          .{" "}
        </span>
      ))}
    </p>
  );
}

/** "Quick Check 1 · Form B" -> "Form B" (the part after the last ·), or the whole title. */
function formLabel(title: string): string {
  const part = title.split("·").pop()?.trim();
  return part && part !== title.trim() ? part : title;
}

/** A unit: Mar'tu's intro, the goals, the Quick Check offer, and every item with its status. */
export function UnitPage({ unit, campaign, glossary }: UnitPageProps) {
  const progress = useCourseProgress();
  const stats = unitProgress(unit, progress);
  // A Quick Check can have more than one form (qc1-a, qc1-b), each with its questions quiz (qc1-a-questions).
  // They all live in the Quick Check offer, not in the lesson list.
  const forms = unit.items
    .filter((item) => item.kind === "testout")
    .map((form) => ({ form, questions: unit.items.find((item) => item.kind === "quiz" && item.id === `${form.id}-questions`) }));
  const quickCheck = forms[0]?.form;
  const inOffer = new Set(forms.flatMap(({ form, questions }) => (questions ? [form.id, questions.id] : [form.id])));
  const items = unit.items.filter((item) => !inOffer.has(item.id));
  const nextUp = nextUpItem(unit.id, items, progress);
  const light = coursePreset(progress.settings) === "short";

  return (
    <main className="course-page" data-testid="unit-page" data-unit={unit.id}>
      <div className="course-topbar">
        <Breadcrumbs crumbs={[{ href: COURSE_HREF, label: "Intro to Python" }, { label: unitLabel(unit) }]} />
        <CourseSettings />
      </div>

      {!unit.published ? (
        <p className="course-banner" data-testid="unpublished-banner">
          Teacher preview: this unit is not published yet, so it is not on the course map.
        </p>
      ) : null}

      <header className="unit-hero">
        <p className="course-eyebrow">Unit {unit.order}</p>
        <h1>{unit.title}</h1>
        {unit.subtitle ? <p className="unit-subtitle">{unit.subtitle}</p> : null}
        <div className="unit-hero-progress">
          <ProgressBar percent={stats.percent} label={`${unit.title} progress`} />
          <p className="unit-status" data-testid={`unit-status-${unit.id}`}>
            {unitStatusText(stats)}
          </p>
        </div>
      </header>

      <MarTu text={unit.martuIntro} glossary={glossary} light={light} />

      <section className="unit-goals-box" aria-labelledby="unit-goals-title">
        <h2 id="unit-goals-title">In this unit you will</h2>
        <ul className="unit-goals">
          {unit.goals.map((goal, index) => (
            <li key={index}>
              <Prose text={goal} glossary={glossary} inline />
            </li>
          ))}
        </ul>
      </section>

      {quickCheck ? (
        <aside className={`quick-check-offer${stats.testedOut ? " is-passed" : ""}`} data-testid="quick-check-offer">
          {stats.testedOut ? (
            <>
              <p>
                <strong>You passed the Quick Check.</strong> You can skip ahead, or try the lessons and side quests
                anyway.
              </p>
              <Link href={itemHref(unit.id, quickCheck.id)} data-testid="testout-start">
                Open the Quick Check again
              </Link>
            </>
          ) : (
            <>
              <p>
                <strong>Already know this?</strong> Try the Quick Check. Pass it and this unit counts as done. No hints,
                no pressure: you can always do the lessons.
              </p>
              <Link className="course-button" href={itemHref(unit.id, quickCheck.id)} data-testid="testout-start">
                Try the Quick Check
              </Link>
            </>
          )}
          <QuickCheckMore unitId={unit.id} forms={forms} />
        </aside>
      ) : null}

      <section aria-labelledby="unit-items-title" className="unit-items">
        <h2 id="unit-items-title">Lessons and more</h2>
        <ol className="item-list">
          {items.map((item) => {
            const status = itemStatus(unit.id, item, progress);
            const isNext = nextUp?.id === item.id;
            return (
              <li
                key={item.id}
                className={`item-row kind-row-${item.kind}${isNext ? " is-next" : ""}`}
                data-testid={`item-row-${item.id}`}
              >
                <div className="item-row-badges">
                  <KindBadge kind={item.kind} />
                  {item.optional ? <span className="optional-tag">Optional</span> : null}
                  {isNext ? <span className="next-up">Next up</span> : null}
                </div>
                <div className="item-row-main">
                  <h3>
                    <Link href={itemHref(unit.id, item.id)} data-testid={`item-link-${item.id}`}>
                      {item.title}
                    </Link>
                  </h3>
                  {item.summary ? <Prose text={item.summary} glossary={glossary} className="item-row-summary" /> : null}
                </div>
                <div className="item-row-side">
                  {item.minutes ? <span className="item-minutes">About {item.minutes} min</span> : null}
                  <StatusBadge status={status} testId={`item-status-${item.id}`} />
                </div>
              </li>
            );
          })}
        </ol>
      </section>

      {campaign.length > 0 ? (
        <aside className="unit-campaign" data-testid="unit-campaign">
          <p>
            <strong>Where you will use this:</strong>{" "}
            {campaign.map((module, index) => (
              <span key={module.id}>
                {index > 0 ? ", " : null}
                <Link href={`/play/${module.id}`}>{module.title}</Link>
              </span>
            ))}
          </p>
        </aside>
      ) : null}

      <p className="course-back">
        <Link href={COURSE_HREF} data-testid="back-to-course">
          Back to the course map
        </Link>
      </p>
    </main>
  );
}
