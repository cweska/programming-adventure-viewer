import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { UnitPage } from "../../../components/course/UnitPage";
import { allUnits, findUnit, glossaryForUnit, unitOutline } from "../../../lib/course/registry";
import { studentModules } from "../../../lib/lesson/modules";

export const dynamicParams = false;

/** Every unit gets a page, unpublished ones too (they are only hidden from the course map). */
export function generateStaticParams() {
  return allUnits.map((unit) => ({ unitId: unit.id }));
}

type Params = { params: Promise<{ unitId: string }> };

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { unitId } = await params;
  const unit = findUnit(unitId);
  return { title: unit ? `${unit.title} · Intro to Python` : "Intro to Python" };
}

export default async function UnitRoute({ params }: Params) {
  const { unitId } = await params;
  const unit = findUnit(unitId);
  if (!unit) notFound();
  const playable = studentModules();
  const campaign = unit.campaignLinks.flatMap((id) => {
    const module = playable.find((candidate) => candidate.id === id);
    return module ? [{ id: module.id, title: module.title }] : [];
  });
  return (
    <UnitPage
      unit={{ ...unitOutline(unit), martuIntro: unit.martuIntro, goals: unit.goals }}
      campaign={campaign}
      glossary={glossaryForUnit(unit)}
    />
  );
}
