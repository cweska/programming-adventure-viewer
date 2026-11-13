"use client";

import type { ItemPageProps } from "../../lib/course/contracts";
import { ArticleView } from "./ArticleView";
import { CheatsheetView } from "./CheatsheetView";
import { Breadcrumbs, unitLabel } from "./CourseBits";
import { COURSE_HREF, unitHref } from "./course-links";
import { CourseSettings } from "./CourseSettings";
import { LessonPlayer } from "./LessonPlayer";
import { QuizPlayer } from "./QuizPlayer";

function ItemBody(props: ItemPageProps) {
  const { item } = props;
  switch (item.kind) {
    case "lesson":
    case "project":
    case "challenge":
    case "testout":
      return <LessonPlayer {...props} />;
    case "quiz":
      return <QuizPlayer {...props} item={item} />;
    case "article":
      return <ArticleView {...props} item={item} />;
    case "cheatsheet":
      return <CheatsheetView {...props} item={item} />;
    default:
      return <p className="course-empty">This page is not ready yet.</p>;
  }
}

/** One course item: breadcrumbs and help options, then the player for its kind. */
export function ItemPage(props: ItemPageProps) {
  const { unit, item } = props;
  return (
    <main className={`course-page course-item-page kind-page-${item.kind}`} data-testid="item-page" data-kind={item.kind}>
      <div className="course-topbar no-print">
        <Breadcrumbs
          crumbs={[
            { href: COURSE_HREF, label: "Intro to Python" },
            { href: unitHref(unit.id), label: unitLabel(unit) },
            { label: item.title },
          ]}
        />
        <CourseSettings />
      </div>
      <ItemBody {...props} />
    </main>
  );
}
