import { describe, expect, it } from "vitest";
import { formatForTrigger, shouldAutoFormat } from "./format-policy";

describe("auto-format", () => {
  it("formats on blur, when code is loaded, and before run, but not on each keystroke", () => {
    expect(shouldAutoFormat("blur")).toBe(true);
    expect(shouldAutoFormat("load")).toBe(true);
    expect(shouldAutoFormat("run")).toBe(true);
    expect(shouldAutoFormat("change")).toBe(false);
  });

  it("leaves the buffer alone on change and formats for the other triggers", async () => {
    const format = async (code: string) => code.replace("=", " = ");
    await expect(formatForTrigger("change", "value=1", format)).resolves.toBe("value=1");
    await expect(formatForTrigger("blur", "value=1", format)).resolves.toBe("value = 1");
    await expect(formatForTrigger("load", "value=1", format)).resolves.toBe("value = 1");
    await expect(formatForTrigger("run", "value=1", format)).resolves.toBe("value = 1");
  });
});
