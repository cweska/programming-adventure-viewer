import { createRequire } from "node:module";
import { copyFileSync, existsSync, mkdirSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

const require = createRequire(import.meta.url);
const root = process.cwd();

function packageDir(specifier) {
  const entry = require.resolve(specifier);
  let dir = path.dirname(entry);
  while (dir !== path.dirname(dir)) {
    if (existsSync(path.join(dir, "package.json"))) return dir;
    dir = path.dirname(dir);
  }
  throw new Error(`Could not locate package root for ${specifier}`);
}

function copyFiles(fromDir, destDir, predicate) {
  mkdirSync(destDir, { recursive: true });
  let copied = 0;
  for (const name of readdirSync(fromDir)) {
    const from = path.join(fromDir, name);
    if (!statSync(from).isFile()) continue;
    if (!predicate(name)) continue;
    copyFileSync(from, path.join(destDir, name));
    copied += 1;
  }
  if (copied === 0) {
    throw new Error(`No files copied from ${fromDir} to ${destDir}`);
  }
  console.log(`copied ${copied} files to ${path.relative(root, destDir)}`);
}

const pyodideDir = packageDir("pyodide");
copyFiles(pyodideDir, path.join(root, "public", "pyodide"), (name) => {
  if (name.endsWith(".d.ts") || name.endsWith(".md")) return false;
  if (name === "package.json" || name === "LICENSE") return false;
  return true;
});

const ruffDir = packageDir("@astral-sh/ruff-wasm-web");
const wasmNames = [];
function findWasm(dir, depth) {
  if (depth > 3) return;
  for (const name of readdirSync(dir)) {
    const from = path.join(dir, name);
    if (statSync(from).isDirectory()) {
      if (name !== "node_modules") findWasm(from, depth + 1);
      continue;
    }
    if (name.endsWith(".wasm")) wasmNames.push(from);
  }
}
findWasm(ruffDir, 0);
if (wasmNames.length === 0) {
  throw new Error(`No Ruff wasm file under ${ruffDir}`);
}
const ruffDest = path.join(root, "public", "ruff");
mkdirSync(ruffDest, { recursive: true });
for (const from of wasmNames) {
  copyFileSync(from, path.join(ruffDest, path.basename(from)));
  console.log(`copied ${path.basename(from)} to public/ruff`);
}
const ruffJs = path.join(ruffDir, "ruff_wasm.js");
if (!existsSync(ruffJs)) {
  throw new Error(`Missing ${ruffJs}`);
}
copyFileSync(ruffJs, path.join(ruffDest, "ruff_wasm.js"));
console.log("copied ruff_wasm.js to public/ruff");
