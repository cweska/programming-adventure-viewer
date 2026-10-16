export const pagesBasePath = "/programming-adventure-viewer";

export const isStaticExport = process.env.NEXT_PUBLIC_STATIC_EXPORT === "1";

export const basePath = (process.env.NEXT_PUBLIC_BASE_PATH ?? "").replace(/\/$/, "");

export function withBase(base: string, path: string): string {
  if (!path.startsWith("/") || path.startsWith("//")) return path;
  const prefix = base.replace(/\/$/, "");
  if (!prefix) return path;
  if (path === prefix || path.startsWith(`${prefix}/`)) return path;
  return `${prefix}${path}`;
}

export function publicPath(path: string): string {
  return withBase(basePath, path);
}

export function pagePathFor(base: string, staticSite: boolean, path: string): string {
  const prefix = base.replace(/\/$/, "");
  if (path === "/" || path === "") return prefix ? `${prefix}/` : "/";
  const normalized = path.startsWith("/") ? path : `/${path}`;
  const joined = `${prefix}${normalized}`;
  if (staticSite && !joined.endsWith("/")) return `${joined}/`;
  return joined;
}

export function pagePath(path: string): string {
  return pagePathFor(basePath, isStaticExport, path);
}
