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
 * front on the unit page), or the unit page when this is the last one.
 */
export function nextHref(unit: Pick<Unit, "id" | "items">, item: Pick<Item, "id">): string {
  const at = unit.items.findIndex((candidate) => candidate.id === item.id);
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
    items: unit.items.map((item) => ({ id: item.id, kind: item.kind, title: item.title, optional: item.optional })),
  };
}

/** The exercise ids an item contains (lessons, test-outs, articles); empty for one-exercise items. */
function exerciseIdsOf(item: Item): string[] {
  return "exercises" in item ? item.exercises.map((exercise) => exercise.id) : [];
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
      exercises: exerciseIdsOf(item).map((id) => ({ id })),
    })),
  };
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
