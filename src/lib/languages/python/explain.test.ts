import { describe, expect, it } from "vitest";
import { explainPython } from "./explain";

function trace(lastLine: string): string {
  return ["Traceback (most recent call last):", '  File "<exec>", line 1, in <module>', lastLine].join("\n");
}

describe("python explainers", () => {
  it("explains SyntaxError", () => {
    const raw = trace("SyntaxError: '(' was never closed");
    const result = explainPython(raw);
    expect(result.title).toBe("Syntax error");
    expect(result.hint).toBe(
      "Python could not read this code: '(' was never closed. Look for a missing colon, parenthesis, or quote.",
    );
    expect(result.raw).toBe(raw);
  });

  it("explains IndentationError", () => {
    const raw = trace("IndentationError: expected an indented block after function definition on line 1");
    const result = explainPython(raw);
    expect(result.title).toBe("Indentation error");
    expect(result.hint).toBe(
      "The indentation does not match the block above. Use four spaces for each nested level, and do not mix in tabs.",
    );
    expect(result.raw).toBe(raw);
  });

  it("explains ValueError with Python's own message", () => {
    const raw = trace(`ValueError: The party cannot move 'rigth'. Use "left", "right", "up", or "down".`);
    const result = explainPython(raw);
    expect(result.title).toBe("Value not allowed");
    expect(result.hint).toBe(`The party cannot move 'rigth'. Use "left", "right", "up", or "down".`);
  });

  it("explains NameError", () => {
    const raw = trace("NameError: name 'torch' is not defined");
    const result = explainPython(raw);
    expect(result.title).toBe("Unknown name");
    expect(result.hint).toBe(
      'Python does not know the name "torch". Define it before you use it, or check the spelling.',
    );
  });

  it("explains TypeError", () => {
    const raw = trace('TypeError: can only concatenate str (not "int") to str');
    const result = explainPython(raw);
    expect(result.title).toBe("Wrong type");
    expect(result.hint).toBe('This line mixes types: can only concatenate str (not "int") to str.');
  });

  it("explains IndexError", () => {
    const result = explainPython(trace("IndexError: list index out of range"));
    expect(result.title).toBe("Index out of range");
    expect(result.hint).toBe("That index is outside the sequence. Check the length before you read a position.");
  });

  it("explains KeyError", () => {
    const result = explainPython(trace("KeyError: 'gate'"));
    expect(result.title).toBe("Missing key");
    expect(result.hint).toBe('The dictionary has no key "gate". Use a key that is already there.');
  });

  it("explains AttributeError", () => {
    const result = explainPython(trace("AttributeError: 'NoneType' object has no attribute 'say'"));
    expect(result.title).toBe("Missing attribute");
    expect(result.hint).toBe('That value has no attribute "say". Check the object before the dot.');
  });

  it("explains ZeroDivisionError", () => {
    const result = explainPython(trace("ZeroDivisionError: division by zero"));
    expect(result.title).toBe("Division by zero");
    expect(result.hint).toBe("A number was divided by zero. Check the divisor before you divide.");
  });

  it("explains a missing import", () => {
    const missing = explainPython(trace("ModuleNotFoundError: No module named 'requests'"));
    expect(missing.title).toBe("Missing import");
    expect(missing.hint).toBe(
      'Python cannot import "requests" here. The player does not download packages or open the network.',
    );

    const imported = explainPython(trace("ImportError: cannot import name 'lamp' from 'math'"));
    expect(imported.title).toBe("Missing import");
    expect(imported.hint).toBe(
      "The import failed (cannot import name 'lamp' from 'math'). Check the module name and the name you are pulling from it.",
    );
  });

  it("keeps the raw traceback and one generic line for unknown errors", () => {
    const raw = trace("RuntimeError: the gate jammed");
    const result = explainPython(raw);
    expect(result.title).toBe("Python error");
    expect(result.hint).toBe("The theater does not have a specific hint for this error.");
    expect(result.raw).toContain("RuntimeError: the gate jammed");
  });
});
