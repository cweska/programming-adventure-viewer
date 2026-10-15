export type FormatTrigger = "change" | "blur" | "load" | "run";

export function shouldAutoFormat(trigger: FormatTrigger): boolean {
  return trigger === "blur" || trigger === "load" || trigger === "run";
}

export async function formatForTrigger(
  trigger: FormatTrigger,
  code: string,
  format: (code: string) => Promise<string>,
): Promise<string> {
  if (!shouldAutoFormat(trigger)) return code;
  return format(code);
}
