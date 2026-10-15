type RuffWorkspace = {
  format(code: string): string;
};

type RuffModule = {
  default: (moduleOrPath?: unknown) => Promise<unknown>;
  Workspace: new (options: Record<string, unknown>, encoding: number) => RuffWorkspace;
  PositionEncoding: { Utf16: number };
};

let workspacePromise: Promise<RuffWorkspace> | null = null;

async function loadRuff(): Promise<RuffModule> {
  const importer = new Function("specifier", "return import(specifier)") as (
    specifier: string,
  ) => Promise<RuffModule>;
  return importer("/ruff/ruff_wasm.js");
}

async function loadWorkspace(): Promise<RuffWorkspace> {
  const ruff = await loadRuff();
  await ruff.default({ module_or_path: "/ruff/ruff_wasm_bg.wasm" });
  return new ruff.Workspace(
    {
      "line-length": 88,
      "indent-width": 4,
      format: {
        "indent-style": "space",
        "quote-style": "double",
      },
    },
    ruff.PositionEncoding.Utf16,
  );
}

export async function formatPython(code: string): Promise<string> {
  if (!workspacePromise) {
    workspacePromise = loadWorkspace().catch((error: unknown) => {
      workspacePromise = null;
      throw error;
    });
  }
  const workspace = await workspacePromise;
  return workspace.format(code);
}
