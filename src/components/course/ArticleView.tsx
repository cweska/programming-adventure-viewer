"use client";

import Link from "next/link";
import type { ItemPageProps } from "../../lib/course/contracts";
import { itemKey, markRead, useCourseProgress, useProgressReady } from "../../lib/course/progress";
import { exerciseKey, type ArticleItem } from "../../lib/course/schema";
import { KindBadge } from "./CourseBits";
import { ExercisePlayer } from "./ExercisePlayer";
import { Prose } from "./Prose";
import { ReadAloud } from "./ReadAloud";
import { RunnableExample } from "./RunnableExample";

/** Try-it exercises at the end of an article (optional; saved under exerciseKey(unit, article, exercise)). */
function TryIt({ unit, item, glossary, settings }: ItemPageProps<ArticleItem>) {
  if (item.exercises.length === 0) return null;
  return (
    <section className="article-try" aria-labelledby="article-try-title" data-testid="article-try">
      <h2 id="article-try-title">Try it yourself</h2>
      {item.exercises.map((exercise) => (
        <ExercisePlayer
          key={exercise.id}
          unitId={unit.id}
          itemId={item.id}
          exerciseKey={exerciseKey(unit.id, item.id, exercise.id)}
          exercise={exercise}
          glossary={glossary}
          settings={settings}
          mode="try-it"
        />
      ))}
    </section>
  );
}

/** An article: Mar'tu's notes, runnable examples, optional try-it exercises, and "Mark as read". */
export function ArticleView(props: ItemPageProps<ArticleItem>) {
  const { unit, item, glossary, nextHref } = props;
  const progress = useCourseProgress();
  const ready = useProgressReady();
  const key = itemKey(unit.id, item.id);
  const read = progress.read[key] === true;

  return (
    <div className="course-reading article" data-testid="article">
      <header className="item-header">
        <KindBadge kind="article" />
        {item.optional ? <span className="optional-tag">Optional</span> : null}
        <h1>{item.title}</h1>
        {item.minutes ? <p className="item-meta">About {item.minutes} min to read</p> : null}
      </header>

      <div className="article-body">
        <Prose text={item.body} glossary={glossary} testId="article-body" />
        <ReadAloud text={item.body} />
      </div>

      {item.examples.length > 0 ? (
        <section className="article-examples" aria-labelledby="article-examples-title">
          <h2 id="article-examples-title">{item.examples.length === 1 ? "Example" : "Examples"}</h2>
          <p className="article-examples-help">Press Run to see what each one prints.</p>
          {item.examples.map((example, index) => (
            <RunnableExample
              key={index}
              code={example.code}
              stdin={example.stdin}
              index={index + 1}
              testPrefix="article-example"
            />
          ))}
        </section>
      ) : null}

      <TryIt {...props} />

      <div className="item-footer">
        {read ? (
          <p className="article-read" data-testid="article-read" role="status">
            <span aria-hidden="true">✓</span> You read this.
          </p>
        ) : (
          <button type="button" onClick={() => markRead(key)} disabled={!ready} data-testid="mark-read">
            Mark as read
          </button>
        )}
        <Link className="course-button" href={nextHref} data-testid="item-next">
          Next
        </Link>
      </div>
    </div>
  );
}
