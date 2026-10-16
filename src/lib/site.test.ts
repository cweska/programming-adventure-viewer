import { describe, expect, it } from "vitest";
import { pagePathFor, withBase } from "./site";

describe("static asset paths", () => {
  it("leaves root-absolute paths alone when there is no base path", () => {
    expect(withBase("", "/scenes/gate-road.svg")).toBe("/scenes/gate-road.svg");
    expect(withBase("", "/workers/python-worker.js")).toBe("/workers/python-worker.js");
    expect(withBase("", "/ruff/ruff_wasm.js")).toBe("/ruff/ruff_wasm.js");
  });

  it("prefixes public files for the Pages site", () => {
    const base = "/programming-adventure-viewer";
    expect(withBase(base, "/scenes/gate-road.svg")).toBe(
      "/programming-adventure-viewer/scenes/gate-road.svg",
    );
    expect(withBase(base, "/pyodide/pyodide.mjs")).toBe(
      "/programming-adventure-viewer/pyodide/pyodide.mjs",
    );
    expect(withBase(base, "/workers/python-worker.js")).toBe(
      "/programming-adventure-viewer/workers/python-worker.js",
    );
    expect(withBase(`${base}/`, "/ruff/ruff_wasm_bg.wasm")).toBe(
      "/programming-adventure-viewer/ruff/ruff_wasm_bg.wasm",
    );
  });

  it("does not prefix a path that already includes the base", () => {
    expect(withBase("/programming-adventure-viewer", "/programming-adventure-viewer/scenes/gate.svg")).toBe(
      "/programming-adventure-viewer/scenes/gate.svg",
    );
  });

  it("builds page urls with a trailing slash only for the static site", () => {
    expect(pagePathFor("", false, "/")).toBe("/");
    expect(pagePathFor("", false, "/classroom")).toBe("/classroom");
    expect(pagePathFor("/programming-adventure-viewer", true, "/")).toBe("/programming-adventure-viewer/");
    expect(pagePathFor("/programming-adventure-viewer", true, "/classroom")).toBe(
      "/programming-adventure-viewer/classroom/",
    );
    expect(pagePathFor("/programming-adventure-viewer", true, "/author")).toBe(
      "/programming-adventure-viewer/author/",
    );
  });
});
