"use client";

import Link from "next/link";
import type { ItemStatus } from "../../lib/course/contracts";
import type { Item } from "../../lib/course/schema";

export const KIND_LABEL: Record<Item["kind"], string> = {
  lesson: "Lesson",
  quiz: "Quiz",
  project: "Project",
  challenge: "Challenge",
  article: "Article",
  cheatsheet: "Cheatsheet",
  testout: "Quick Check",
};

export const STATUS_LABEL: Record<ItemStatus, string> = {
  "not-started": "Not started",
  "in-progress": "In progress",
  done: "Done",
  "tested-out": "Tested out",
};

const STATUS_MARK: Record<ItemStatus, string> = {
  "not-started": "○",
  "in-progress": "◐",
  done: "✓",
  "tested-out": "✓",
};

export function KindBadge({ kind }: { kind: Item["kind"] }) {
  return <span className={`kind-badge kind-${kind}`}>{KIND_LABEL[kind]}</span>;
}

/** Status as an icon and words (never colour alone). */
export function StatusBadge({ status, testId }: { status: ItemStatus; testId?: string }) {
  return (
    <span className={`status-badge status-${status}`} data-testid={testId} data-status={status}>
      <span aria-hidden="true">{STATUS_MARK[status]}</span> {STATUS_LABEL[status]}
    </span>
  );
}

/** A labelled progress bar (0 to 100). */
export function ProgressBar({ percent, label, testId }: { percent: number; label: string; testId?: string }) {
  const value = Math.max(0, Math.min(100, Math.round(percent)));
  return (
    <div
      className="course-progress"
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={value}
      data-testid={testId}
    >
      <div className="course-progress-fill" style={{ width: `${value}%` }} />
    </div>
  );
}

export type Crumb = { href?: string; label: string };

/** Intro to Python › Unit › Item. The last crumb is the current page. */
export function Breadcrumbs({ crumbs }: { crumbs: Crumb[] }) {
  return (
    <nav className="course-crumbs" aria-label="Breadcrumb" data-testid="course-breadcrumbs">
      <ol>
        {crumbs.map((crumb, index) => {
          const last = index === crumbs.length - 1;
          return (
            <li key={`${crumb.label}-${index}`}>
              {crumb.href && !last ? (
                <Link href={crumb.href}>{crumb.label}</Link>
              ) : (
                <span aria-current={last ? "page" : undefined}>{crumb.label}</span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export function unitLabel(unit: { order: number; title: string }): string {
  return `Unit ${unit.order}: ${unit.title}`;
}
