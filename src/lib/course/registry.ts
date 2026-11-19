/**
 * The Intro to Python content registry. SERVER / TEST ONLY: it imports every unit's JSON, so a client
 * component that imported it would ship the whole course. Pages pick what they need and pass plain props.
 *
 * Parsing happens at import time, so a bad content file fails `npm test` first and `next build` second.
 */
import { z } from "zod";
import courseJson from "../../../content/courses/intro-python/course.json";
import glossaryJson from "../../../content/courses/intro-python/glossary.json";
import { COURSE_HREF, itemHref, unitHref } from "../../components/course/course-links";
import { findGlossaryEntry, glossaryRefs } from "../../components/course/prose-format";
import type { ProgressUnit } from "./progress";
import type { ItemPageProps, UnitSummary } from "./contracts";
import { isReadinessUnit, READINESS_ITEMS } from "./readiness";
import {
  courseMetaSchema,
  glossaryEntrySchema,
  unitSchema,
  type CourseMeta,
  type GlossaryEntry,
  type Item,
  type Unit,
} from "./schema";
import { rawUnits } from "./units.generated";

function describeIssues(error: z.ZodError): string {
  return error.issues
    .slice(0, 8)
    .map((issue) => `  - ${issue.path.join(".") || "(root)"}: ${issue.message}`)
    .join("\n");
}

function parseOrThrow<T>(schema: z.ZodType<T, z.ZodTypeDef, unknown>, raw: unknown, what: string): T {
  const result = schema.safeParse(raw);
  if (!result.success) throw new Error(`Intro to Python: ${what} is not valid.\n${describeIssues(result.error)}`);
  return result.data;
}

function rawId(raw: unknown): string {
  return raw && typeof raw === "object" && typeof (raw as { id?: unknown }).id === "string"
    ? (raw as { id: string }).id
    : "(no id)";
}

/** Parse and order a list of raw unit JSON values. Throws on bad content, duplicate ids or duplicate orders. */
export function parseUnits(raws: readonly unknown[]): Unit[] {
  const units = raws.map((raw) => parseOrThrow(unitSchema, raw, `unit "${rawId(raw)}"`));
  const ids = new Set<string>();
  const orders = new Map<number, string>();
  for (const unit of units) {
    if (ids.has(unit.id)) throw new Error(`Intro to Python: two units have the id "${unit.id}".`);
    ids.add(unit.id);
    const clash = orders.get(unit.order);
    if (clash) throw new Error(`Intro to Python: units "${clash}" and "${unit.id}" both have order ${unit.order}.`);
    orders.set(unit.order, unit.id);
    const itemIds = new Set<string>();
    for (const item of unit.items) {
      if (itemIds.has(item.id)) throw new Error(`Intro to Python: unit "${unit.id}" has two items with the id "${item.id}".`);
      itemIds.add(item.id);
    }
  }
  return units.slice().sort((left, right) => left.order - right.order);
}

export const courseMeta: CourseMeta = parseOrThrow(courseMetaSchema, courseJson, "course.json");

export const glossary: GlossaryEntry[] = parseOrThrow(z.array(glossaryEntrySchema), glossaryJson, "glossary.json");

/** Every unit in course order, unpublished ones included. */
export const allUnits: Unit[] = parseUnits(rawUnits);

/** Units a student sees on the map (published only). */
export function publishedUnits(units: readonly Unit[] = allUnits): Unit[] {
  return units.filter((unit) => unit.published);
}

export function findUnit(unitId: string, units: readonly Unit[] = allUnits): Unit | undefined {
  return units.find((unit) => unit.id === unitId);
}

export function findItem(
  unitId: string,
  itemId: string,
  units: readonly Unit[] = allUnits,
): { unit: Unit; item: Item } | undefined {
  const unit = findUnit(unitId, units);
  const item = unit?.items.find((candidate) => candidate.id === itemId);
  return unit && item ? { unit, item } : undefined;
}

/* ------------------------------------------------------------------------------------------------ */
/* Links: app paths for next/link (see course-links.ts)                                              */
/* ------------------------------------------------------------------------------------------------ */

export { COURSE_HREF, itemHref, unitHref };

/**
 * Where "Next" goes after an item: the next item in the unit, skipping the Quick Check (it is offered up
 * front on the unit page), or the unit page when this is the last one. In a readiness unit (one that holds a required
 * test-out) the forms are items like any other: a form's questions lead to its tasks, and every other item leads to
 * the next core item (Part 1, the mini-boss, the explain question), or back to the unit page. The page itself sends
 * Continue after Part 1 to Mar'tu's notes only when something was missed (LessonPlayer, readiness.ts afterPart1).
 */
export function nextHref(unit: Pick<Unit, "id" | "items">, item: Pick<Item, "id">): string {
  const at = unit.items.findIndex((candidate) => candidate.id === item.id);
  if (at >= 0 && isReadinessUnit(unit.items)) {
    const form = unit.items.find((candidate) => candidate.kind === "testout" && `${candidate.id}-questions` === item.id);
    if (form) return itemHref(unit.id, form.id);
    const next = unit.items.slice(at + 1).find((candidate) => !candidate.optional);
    return next ? itemHref(unit.id, next.id) : unitHref(unit.id);
  }
  if (at >= 0) {
    const next = unit.items.slice(at + 1).find((candidate) => candidate.kind !== "testout");
    if (next) return itemHref(unit.id, next.id);
  }
  return unitHref(unit.id);
}

/* ------------------------------------------------------------------------------------------------ */
/* What pages pass to the client                                                                     */
/* ------------------------------------------------------------------------------------------------ */

export function unitSummary(unit: Unit): UnitSummary {
  return {
    id: unit.id,
    order: unit.order,
    title: unit.title,
    ...(unit.subtitle ? { subtitle: unit.subtitle } : {}),
    items: unit.items.map((item) => ({
      id: item.id,
      kind: item.kind,
      title: item.title,
      optional: item.optional,
      ...gateFields(item, isReadinessUnit(unit.items)),
    })),
  };
}

/**
 * What a Quick Check's pass needs to know: a form's tasks and question count to pass, a quiz's size. A readiness
 * unit also needs every exercise's id (its mini-bosses' Compare and result) and its quizzes' question ids (twins).
 */
function gateFields(
  item: Item,
  readiness = false,
): { exercises?: { id: string; title?: string }[]; questionsToPass?: number; questionCount?: number; questionIds?: string[] } {
  if (item.kind === "testout") {
    return { exercises: exerciseOutline(item, readiness), ...(item.questionsToPass ? { questionsToPass: item.questionsToPass } : {}) };
  }
  if (item.kind === "quiz") {
    return { questionCount: item.questions.length, ...(readiness ? { questionIds: item.questions.map((question) => question.id) } : {}) };
  }
  return {};
}

/**
 * The exercises an item contains (lessons, test-outs, articles; empty for one-exercise items) as the outline carries
 * them: their ids, and in a readiness unit a test-out's task titles too (the
 * unit page and the form's end name a task not tried yet: readiness.ts lockReason).
 */
function exerciseOutline(item: Item, readiness: boolean): { id: string; title?: string }[] {
  if (!("exercises" in item)) return [];
  return item.exercises.map((exercise) => (readiness && item.kind === "testout" ? { id: exercise.id, title: exercise.title } : { id: exercise.id }));
}

/** A unit as the course map and unit page need it: no exercise content, just enough for progress maths. */
export function unitOutline(unit: Unit): ProgressUnit {
  return {
    id: unit.id,
    order: unit.order,
    title: unit.title,
    ...(unit.subtitle ? { subtitle: unit.subtitle } : {}),
    published: unit.published,
    items: unit.items.map((item) => ({
      id: item.id,
      kind: item.kind,
      title: item.title,
      optional: item.optional,
      ...(item.summary ? { summary: item.summary } : {}),
      ...(item.minutes ? { minutes: item.minutes } : {}),
      exercises: exerciseOutline(item, isReadinessUnit(unit.items)),
      ...(item.kind === "testout" && item.questionsToPass ? { questionsToPass: item.questionsToPass } : {}),
      ...(item.kind === "quiz" ? { questionCount: item.questions.length } : {}),
      ...(item.kind === "quiz" && isReadinessUnit(unit.items) ? { questionIds: item.questions.map((question) => question.id) } : {}),
    })),
  };
}

/**
 * A Readiness Check skill's "Start here" lesson, resolved: where it is and what the student saw it called, and the
 * skill's own parts in form A as the student saw them ("Question 2 and *Store, then pass it on*").
 */
export type ReadinessRoute = { n: number; href: string; label: string; seen: string };

/**
 * The "Start here" lesson of every Part 1 skill of a readiness unit (readiness.ts READINESS_ITEMS), with the label the
 * student knows it by: "Unit 3 · Recipes With Names · Replace pass". Throws on a route to nothing (CI catches it).
 */
export function readinessRoutes(unitId: string, units: readonly Unit[] = allUnits): ReadinessRoute[] {
  const home = findUnit(unitId, units);
  const required = home?.items.find((item) => item.kind === "testout" && !item.optional);
  return (READINESS_ITEMS[unitId] ?? []).map((skill) => {
    const questions = (skill.questions ?? []).map((at) => at + 1);
    const asked = questions.length === 0 ? [] : [`${questions.length === 1 ? "Question" : "Questions"} ${questions.join(" and ")}`];
    const tasks = (skill.tasks ?? []).flatMap((at) => (required && "exercises" in required && required.exercises[at] ? [`*${required.exercises[at].title}*`] : []));
    const seen = [...asked, ...tasks].join(" and ");
    const unit = findUnit(skill.start.unit, units);
    const item = unit?.items.find((candidate) => candidate.id === skill.start.item);
    const exercise = item && "exercises" in item ? item.exercises.find((candidate) => candidate.id === skill.start.exercise) : undefined;
    if (!unit || !item || (skill.start.exercise && !exercise)) {
      throw new Error(`Intro to Python: readiness route ${skill.n} of "${unitId}" points to nothing.`);
    }
    const href = `${itemHref(unit.id, item.id)}${exercise ? `#${exercise.id}` : ""}`;
    const label = [`Unit ${unit.order}`, item.title, ...(exercise ? [exercise.title] : [])].join(" · ");
    return { n: skill.n, href, label, seen };
  });
}

/** Fields that hold code or answers, not prose: never scanned for [[glossary]] links. */
const CODE_FIELDS = new Set([
  "code",
  "starter",
  "solution",
  "setup",
  "fix",
  "lines",
  "distractors",
  "snippet",
  "output",
  "expectedOutput",
  "answer",
  "accept",
  "checks",
  "stdin",
  "introduces",
  "preview",
]);

/** Every prose string inside a value (skipping code fields), depth first. */
function proseStrings(value: unknown, out: string[] = []): string[] {
  if (typeof value === "string") {
    out.push(value);
  } else if (Array.isArray(value)) {
    for (const entry of value) proseStrings(entry, out);
  } else if (value && typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) {
      if (!CODE_FIELDS.has(key)) proseStrings(entry, out);
    }
  }
  return out;
}

/** The glossary entries that some prose links to with [[term]] (matching a term or an alias, any case). */
export function glossaryForTexts(texts: readonly string[], entries: readonly GlossaryEntry[] = glossary): GlossaryEntry[] {
  const found: GlossaryEntry[] = [];
  for (const text of texts) {
    for (const ref of glossaryRefs(text)) {
      const entry = findGlossaryEntry(entries, ref);
      if (entry && !found.includes(entry)) found.push(entry);
    }
  }
  return found;
}

/** Only the glossary entries an item's prose and hints reference. */
export function glossaryFor(item: Item, entries: readonly GlossaryEntry[] = glossary): GlossaryEntry[] {
  return glossaryForTexts(proseStrings(item), entries);
}

/** The glossary entries a unit page needs (Mar'tu's intro, the goals, item titles and summaries). */
export function glossaryForUnit(unit: Unit, entries: readonly GlossaryEntry[] = glossary): GlossaryEntry[] {
  return glossaryForTexts(
    [unit.martuIntro, ...unit.goals, ...unit.items.flatMap((item) => [item.title, item.summary ?? ""])],
    entries,
  );
}

export function itemSettings(meta: CourseMeta = courseMeta): ItemPageProps["settings"] {
  return {
    solutionAfterMinutes: meta.settings.solutionAfterMinutes,
    solutionAfterFailedRuns: meta.settings.solutionAfterFailedRuns,
    quizReadyPercent: meta.settings.quizReadyPercent,
  };
}

/** Everything an item page sends to the client, and nothing more. */
export function itemPageProps(unitId: string, itemId: string): ItemPageProps | undefined {
  const found = findItem(unitId, itemId);
  if (!found) return undefined;
  return {
    unit: unitSummary(found.unit),
    item: found.item,
    glossary: glossaryFor(found.item),
    nextHref: nextHref(found.unit, found.item),
    settings: itemSettings(),
  };
}
