import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ItemPage } from "../../../../components/course/ItemPage";
import { allUnits, findItem, itemPageProps } from "../../../../lib/course/registry";

export const dynamicParams = false;

/** Every item of every unit gets a page, unpublished units included. */
export function generateStaticParams() {
  return allUnits.flatMap((unit) => unit.items.map((item) => ({ unitId: unit.id, itemId: item.id })));
}

type Params = { params: Promise<{ unitId: string; itemId: string }> };

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { unitId, itemId } = await params;
  const found = findItem(unitId, itemId);
  return { title: found ? `${found.item.title} · ${found.unit.title} · Intro to Python` : "Intro to Python" };
}

export default async function ItemRoute({ params }: Params) {
  const { unitId, itemId } = await params;
  // Only this item, the glossary words it uses and a summary of its unit go to the browser.
  const props = itemPageProps(unitId, itemId);
  if (!props) notFound();
  return <ItemPage {...props} />;
}
