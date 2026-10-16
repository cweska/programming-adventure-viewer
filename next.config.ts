import type { NextConfig } from "next";

const staticExport = process.env.STATIC_EXPORT === "1";
const pagesBasePath = "/programming-adventure-viewer";

const nextConfig: NextConfig = {
  serverExternalPackages: ["better-sqlite3"],
  env: {
    NEXT_PUBLIC_STATIC_EXPORT: staticExport ? "1" : "",
    NEXT_PUBLIC_BASE_PATH: staticExport ? pagesBasePath : "",
  },
};

if (staticExport) {
  nextConfig.output = "export";
  nextConfig.basePath = pagesBasePath;
  nextConfig.assetPrefix = pagesBasePath;
  nextConfig.trailingSlash = true;
  nextConfig.images = { unoptimized: true };
  nextConfig.pageExtensions = ["tsx", "jsx", "mdx"];
}

export default nextConfig;
