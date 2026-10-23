import type { Explanation } from "../types";

const GENERIC_HINT = "The theater does not have a specific hint for this error.";

const EXCEPTION_LINE = /^([A-Za-z_][A-Za-z0-9_.]*):\s*(.*)$/gm;

function lastException(raw: string): { type: string; message: string } | null {
  const matches = [...raw.matchAll(EXCEPTION_LINE)];
  if (matches.length === 0) return null;
  const last = matches[matches.length - 1];
  const type = last[1]?.split(".").pop() ?? last[1];
  return { type, message: (last[2] ?? "").trim() };
}

function quotedName(message: string, pattern: RegExp): string | null {
  const match = message.match(pattern);
  return match?.[1] ?? null;
}

export function explainPython(traceback: string): Explanation {
  const raw = traceback ?? "";
  const parsed = lastException(raw);
  if (!parsed) {
    return { title: "Python error", hint: GENERIC_HINT, raw };
  }

  const { type, message } = parsed;

  switch (type) {
    case "IndentationError":
      return {
        title: "Indentation error",
        hint: "The indentation does not match the block above. Use four spaces for each nested level, and do not mix in tabs.",
        raw,
      };
    case "SyntaxError":
      return {
        title: "Syntax error",
        hint: message
          ? `Python could not read this code: ${message}. Look for a missing colon, parenthesis, or quote.`
          : "Python could not read this code. Look for a missing colon, parenthesis, or quote.",
        raw,
      };
    case "NameError": {
      const name = quotedName(message, /name '([^']+)' is not defined/);
      return {
        title: "Unknown name",
        hint: name
          ? `Python does not know the name "${name}". Define it before you use it, or check the spelling.`
          : "Python does not know one of the names in this line. Define it before you use it, or check the spelling.",
        raw,
      };
    }
    case "TypeError":
      return {
        title: "Wrong type",
        hint: message
          ? `This line mixes types: ${message}.`
          : "This line mixes types. Check the values you passed into the operation.",
        raw,
      };
    case "ValueError":
      return {
        title: "Value not allowed",
        hint: message || "That value is the right type but not one this code accepts. Check the value you passed in.",
        raw,
      };
    case "IndexError":
      return {
        title: "Index out of range",
        hint: "That index is outside the sequence. Check the length before you read a position.",
        raw,
      };
    case "KeyError": {
      const key = message.replace(/^['"]|['"]$/g, "");
      return {
        title: "Missing key",
        hint: key
          ? `The dictionary has no key "${key}". Use a key that is already there.`
          : "The dictionary does not contain that key. Use a key that is already there.",
        raw,
      };
    }
    case "AttributeError": {
      const attribute = quotedName(message, /attribute '([^']+)'/);
      return {
        title: "Missing attribute",
        hint: attribute
          ? `That value has no attribute "${attribute}". Check the object before the dot.`
          : "That value does not have the attribute you asked for. Check the object before the dot.",
        raw,
      };
    }
    case "ZeroDivisionError":
      return {
        title: "Division by zero",
        hint: "A number was divided by zero. Check the divisor before you divide.",
        raw,
      };
    case "ModuleNotFoundError": {
      const moduleName = quotedName(message, /No module named '([^']+)'/);
      return {
        title: "Missing import",
        hint: `Python cannot import "${moduleName ?? "that module"}" here. The player does not download packages or open the network.`,
        raw,
      };
    }
    case "ImportError":
      return {
        title: "Missing import",
        hint: message
          ? `The import failed (${message}). Check the module name and the name you are pulling from it.`
          : "The import failed. Check the module name and the name you are pulling from it.",
        raw,
      };
    default:
      return { title: "Python error", hint: GENERIC_HINT, raw };
  }
}
