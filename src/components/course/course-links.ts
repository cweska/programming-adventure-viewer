/**
 * Intro to Python page links. These are app paths for next/link (no basePath, no trailing slash): Link
 * adds both itself for the static export. For a plain <a> or window.location, wrap them in pagePath()
 * from src/lib/site.ts. Client-safe (the registry re-exports them for server code).
 */

export const COURSE_HREF = "/intro-python";

export function unitHref(unitId: string): string {
  return `${COURSE_HREF}/${unitId}`;
}

export function itemHref(unitId: string, itemId: string): string {
  return `${COURSE_HREF}/${unitId}/${itemId}`;
}
