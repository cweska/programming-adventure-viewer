"use client";

import { useEffect, useState } from "react";
import { whenPythonReady } from "../../lib/languages/python/run";

export type PythonStatus = "idle" | "loading" | "ready" | "failed";

export const PYTHON_STATUS_TEXT: Record<PythonStatus, string> = {
  idle: "",
  loading: "Python is waking up…",
  ready: "Python is ready.",
  failed: "Python could not load. Check the internet, then reload the page.",
};

/** Start loading Python in the background when `enabled`, and report how it is going. */
export function usePythonStatus(enabled: boolean): PythonStatus {
  const [status, setStatus] = useState<PythonStatus>("idle");
  useEffect(() => {
    if (!enabled) return;
    let alive = true;
    setStatus("loading");
    whenPythonReady().then(
      () => alive && setStatus("ready"),
      () => alive && setStatus("failed"),
    );
    return () => {
      alive = false;
    };
  }, [enabled]);
  return status;
}
