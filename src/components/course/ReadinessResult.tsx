"use client";

import Link from "next/link";
import type { CourseProgress } from "../../lib/course/contracts";
import type { ProgressItem } from "../../lib/course/progress";
import { exerciseKey } from "../../lib/course/schema";
import {
  formName,
  formsUnlocked,
  joinAnd,
  LOCKED_FORM_TEXT,
  readinessResult,
  readinessVerdictText,
  untriedTaskNames,
  type ReadinessPlan,
  type ReadinessSkill,
  type SkillResult,
} from "../../lib/course/readiness";
import { itemHref } from "./course-links";
import { soloUnaided } from "./exercise-logic";
import { Prose } from "./Prose";

/** A Part 1 skill's review lesson, resolved on the server (registry.ts readinessRoutes). */
export type ReadinessRouteProp = { n: number; href: string; label: string; seen: string };

const BOSS_TEXT = {
  "not-done": "Mini-boss: not done yet.",
  // What Ready measures: Mar'tu's version was not opened (Help's other rungs are fine).
  "on-your-own": "Mini-boss: done without Mar'tu's version.",
  "with-compare": "Mini-boss: done with Mar'tu's version.",
} as const;

/** The twin of a missed skill in another form: its task there, or its questions. */
function twinHref(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, result: SkillResult): { href: string; label: string } | null {
  if (!result.twinForm) return null;
  const form = items.find((item) => item.id === result.twinForm);
  if (!form) return null;
  const task = result.skill.tasks?.[0];
  const exercise = task !== undefined ? form.exercises?.[task] : undefined;
  if (exercise) return { href: `${itemHref(unitId, form.id)}#${exercise.id}`, label: formName(form.title) };
  const quiz = plan.questions[form.id];
  return quiz ? { href: itemHref(unitId, quiz), label: `${formName(form.title)}'s questions` } : null;
}

/**
 * The Readiness Check's result on the unit page (curriculum §5.5, teacher site requests 3 and 4): Part 1 skill by skill
 * (a twin in form B or C counts), the mini-boss (on your own, or with Mar'tu's version), the verdict once both are in,
 * and every missed skill with its "Start here" lesson and the twin to try.
 */
export function ReadinessResult({
  unitId,
  items,
  plan,
  skills,
  routes,
  progress,
}: {
  unitId: string;
  items: readonly ProgressItem[];
  plan: ReadinessPlan;
  skills: readonly ReadinessSkill[];
  routes: readonly ReadinessRouteProp[];
  progress: CourseProgress;
}) {
  const result = readinessResult(unitId, items, plan, skills, progress);
  if (!result.visible) return null;
  // A twin opens with forms B and C (after Part 1 A and Mar'tu's notes): until then it is named, not linked.
  const twinsOpen = formsUnlocked(unitId, items, plan, progress);
  const untried = untriedTaskNames(items, plan, result.untried);
  const missed = result.skills.filter((entry) => !entry.passed);
  const twinBoss = result.nextBoss ? items.find((item) => item.id === result.nextBoss) : undefined;
  const miniBoss = plan.miniBoss ? items.find((item) => item.id === plan.miniBoss) : undefined;
  // The mini-boss that counts (readinessResult): the first one once it is done, else the second.
  const first = plan.miniBoss ? progress.exercises[exerciseKey(unitId, plan.miniBoss)] : undefined;
  const counted = first?.done === true ? first : plan.twinBoss ? progress.exercises[exerciseKey(unitId, plan.twinBoss)] : undefined;
  const unaided = soloUnaided(counted);
  return (
    <section
      className={`readiness-result${result.verdict ? ` is-${result.verdict}` : ""}`}
      aria-labelledby="readiness-result-title"
      data-testid="readiness-result"
      data-verdict={result.verdict ?? "waiting"}
      data-score={result.score}
      data-mini-boss={result.miniBoss}
    >
      <h2 id="readiness-result-title">Your Readiness Check</h2>
      <p data-testid="readiness-score">
        {result.score === result.total
          ? `Part 1: you passed all ${result.total} skills.`
          : `Part 1: you passed ${result.score} of the ${result.total} skills.`}
      </p>
      {untried.length > 0 ? (
        <p data-testid="readiness-untried">
          <Prose
            text={`Not tried yet in Part 1 A: ${joinAnd(untried)}. ${untried.length === 1 ? "It counts" : "They count"} as missed. Type your best try there, even if it is not finished, and press Run once.`}
            inline
          />
        </p>
      ) : null}
      <p data-testid="readiness-mini-boss">{BOSS_TEXT[result.miniBoss]}</p>
      {result.verdict ? (
        <p className="readiness-verdict" data-testid="readiness-verdict" role="status">
          {result.verdict === "ready" ? <span aria-hidden="true">★ </span> : null}
          {readinessVerdictText(result.verdict, result.score, result.total, unaided)}
        </p>
      ) : miniBoss ? (
        <p data-testid="readiness-waiting">
          Next: <Link href={itemHref(unitId, miniBoss.id)}>{miniBoss.title}</Link>. Then Mar&apos;tu tells you the result.
        </p>
      ) : null}
      {twinBoss ? (
        <p data-testid="readiness-next-boss">
          Next: <Link href={itemHref(unitId, twinBoss.id)}>{twinBoss.title}</Link>, on your own.
        </p>
      ) : null}
      {missed.length > 0 ? (
        <>
          <p className="readiness-list-title">Skills to look at again:</p>
          <ul className="readiness-missed" data-testid="readiness-missed">
            {missed.map((entry) => {
              const route = routes.find((candidate) => candidate.n === entry.skill.n);
              const twin = twinHref(unitId, items, plan, entry);
              // "*Write a function from its goal*: write a function from its goal." says it twice: once is enough.
              const seen = route?.seen ?? `Item ${entry.skill.n}`;
              const same = seen.replace(/\*/g, "").toLowerCase() === entry.skill.skill.replace(/`/g, "").toLowerCase();
              return (
                <li key={entry.skill.n} data-testid={`readiness-missed-${entry.skill.n}`}>
                  <Prose text={same ? `${seen}.` : `${seen}: ${entry.skill.skill}.`} inline />{" "}
                  {route ? (
                    <>
                      Start here:{" "}
                      <Link href={route.href} data-testid={`readiness-start-${entry.skill.n}`}>
                        {route.label}
                      </Link>
                      .{" "}
                    </>
                  ) : null}
                  {twin && twinsOpen ? (
                    <>
                      Then try its twin in{" "}
                      <Link href={twin.href} data-testid={`readiness-twin-${entry.skill.n}`}>
                        {twin.label}
                      </Link>
                      .
                    </>
                  ) : twin ? (
                    <span data-testid={`readiness-twin-locked-${entry.skill.n}`}>
                      Then, once the other forms open ({LOCKED_FORM_TEXT.replace(/^Opens /, "")}), try its twin in {twin.label}.
                    </span>
                  ) : null}
                </li>
              );
            })}
          </ul>
        </>
      ) : null}
    </section>
  );
}
