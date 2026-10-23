import { Player } from "../../../components/Player";
import { bundledModules } from "../../../lib/lesson/modules";

export const dynamicParams = false;

export function generateStaticParams() {
  return bundledModules.map((module) => ({ moduleId: module.id }));
}

export default async function PlayPage({ params }: { params: Promise<{ moduleId: string }> }) {
  const { moduleId } = await params;
  return <Player moduleId={moduleId} />;
}
