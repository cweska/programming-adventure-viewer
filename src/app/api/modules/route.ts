import { getCatalog } from "../../../lib/lesson/catalog";
import { moduleSchema } from "../../../lib/lesson/schema";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export function GET(request: Request) {
  const scope = new URL(request.url).searchParams.get("scope");
  const catalog = getCatalog();
  const modules = scope === "teacher" ? catalog.loadAll() : catalog.forStudents();
  return Response.json({ modules });
}

export async function PUT(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "The request was not JSON." }, { status: 400 });
  }
  const parsed = moduleSchema.safeParse(body);
  if (!parsed.success) {
    return Response.json({ error: "The draft does not match the lesson schema." }, { status: 422 });
  }
  const saved = getCatalog().save(parsed.data);
  return Response.json({ module: saved });
}
