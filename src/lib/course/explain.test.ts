import { describe, expect, it } from "vitest";
import { closeName, definedNames, explainCourseError } from "./explain";
import { runCourseChecks } from "./run-course";

/** Run the code like a course run and explain the real traceback Python gives. */
function explainRun(code: string, stdin?: string[]) {
  const result = runCourseChecks(code, [], { stdin });
  expect(result.ok, `expected ${JSON.stringify(code)} to crash`).toBe(false);
  return explainCourseError(result.traceback, code);
}

describe("explainCourseError: the class's real slips", () => {
  it("explains a missing closing quote, with the text quoted correctly", () => {
    const result = explainRun('print("Hello)\n');
    expect(result.title).toBe("Missing quote");
    expect(result.hint).toBe(
      'The text on line 1 is missing its closing quote. Text needs a quote at the start and at the end, like "Hello".',
    );
  });

  it("explains mismatched quote types", () => {
    const result = explainRun("print(\"fireball')\n");
    expect(result.title).toBe("Quotes don't match");
    expect(result.hint).toBe(
      `The text on line 1 starts with " but ends with '. Use the same kind of quote at both ends, like "fireball".`,
    );
  });

  it("explains an apostrophe inside single quotes", () => {
    const result = explainRun("print('It's fun')\n");
    expect(result.title).toBe("Apostrophe in text");
    expect(result.hint).toContain(`like "It's fun"`);
  });

  it("asks whether an unknown word should have been text", () => {
    const result = explainRun("spell = fireball\nprint(spell)\n");
    expect(result.title).toBe("Missing quotes?");
    expect(result.hint).toBe(
      'Python doesn\'t know the name fireball. Did you mean to put quotes around it? Text needs quotes: "fireball"',
    );
  });

  it("suggests quotes for several unquoted words in print", () => {
    const result = explainRun("print(Hello world)\n");
    expect(result.title).toBe("Missing quotes?");
    expect(result.hint).toBe('If Hello world is text, put quotes around it: "Hello world". Text needs quotes.');
  });

  it("explains def used to make a variable", () => {
    for (const code of ['def ("character")\n', 'def character = "Kratos"\n', 'def character("Kratos")\n']) {
      const result = explainRun(code);
      expect(result.title, code).toBe("def makes functions");
      expect(result.hint, code).toMatch(/^def is for making functions, not variables\. To make a variable/);
    }
    expect(explainRun('def character = "Kratos"\n').hint).toContain('character = "Kratos"');
  });

  it("does not call a real function header a variable slip", () => {
    const result = explainRun('def greet(name="Lucky")\n    print(name)\n');
    expect(result.title).toBe("Missing colon");
  });

  it("explains a dash where = belongs", () => {
    const result = explainRun('character - "Kratos"\nprint(character)\n');
    expect(result.title).toBe("Dash or equals?");
    expect(result.hint).toBe(
      'Line 1 uses a dash - where Python needs an equals sign =. To make a variable, write: character = "Kratos"',
    );
    const defined = explainRun('character = ""\ncharacter - "Kratos"\n');
    expect(defined.title).toBe("Dash or equals?");
    expect(defined.hint).toContain("Line 2");
  });

  it("explains a colon where = belongs", () => {
    const result = explainRun('character: "Kratos"\nprint(character)\n');
    expect(result.title).toBe("Colon or equals?");
    expect(result.hint).toContain('character = "Kratos"');
  });

  it("points out capital letters, using the name the code made", () => {
    const result = explainRun('Spell = "fire"\nprint(spell)\n');
    expect(result.title).toBe("Capital letters matter");
    expect(result.hint).toBe("Python sees spell and Spell as different names. Use Spell, with the same capital letters every time.");
    expect(explainRun('Print("hi")\n').hint).toContain("Use print");
  });

  it("suggests a close spelling from the code", () => {
    const result = explainRun("mana_cost = 5\nprint(mana_cots)\n");
    expect(result.title).toBe("Check the spelling");
    expect(result.hint).toContain("Did you mean mana_cost?");
  });

  it("never suggests the hidden course helpers", () => {
    const result = explainRun("count += 1\n");
    expect(result.hint).not.toContain("_count");
    expect(result.title).toBe("Make it first");
    expect(result.hint).toBe("Line 1 changes count, but count has no value yet. Give it a starting value first, like count = 0");
    expect(explainRun("print(count)\n").hint).not.toMatch(/\bround\b/);
  });

  it("explains a name used before it is made", () => {
    const result = explainRun("print(total_cost)\ntotal_cost = 68\n");
    expect(result.title).toBe("Used too early");
    expect(result.hint).toBe(
      "Line 1 uses total_cost, but total_cost is only made on line 2. Python runs from top to bottom, so make total_cost first.",
    );
  });

  it("explains IndentationError cases", () => {
    expect(explainRun('if True:\nprint("x")\n').hint).toBe(
      "The line after line 1 belongs inside the if, so it needs 4 spaces at the start.",
    );
    expect(explainRun('  print("x")\n').title).toBe("Extra spaces");
    expect(explainRun('if True:\n        print("a")\n    print("b")\n').title).toBe("Spaces don't line up");
    expect(explainRun("def greet():\nreturn 1\n").hint).toContain("inside the def");
  });

  it("explains joining text and a number, and suggests str()", () => {
    const result = explainRun('score = 5\nprint("Score: " + score)\n');
    expect(result.title).toBe("Text + number");
    expect(result.hint).toBe("Line 2 joins text and a number with +. Turn the number into text first with str(), like str(score).");
    expect(explainRun('score = 5\nprint(score + " points")\n').hint).toContain("str(score)");
  });

  it("explains that input() gives text", () => {
    const result = explainRun('age = input("Age? ")\nprint(age + 1)\n', ["12"]);
    expect(result.title).toBe("input() gives text");
    expect(result.hint).toContain("int(age)");
  });

  it("explains ZeroDivisionError", () => {
    const result = explainRun("print(10 / 0)\n");
    expect(result.title).toBe("Divided by zero");
    expect(result.hint).toContain("Line 1");
  });

  it("explains running out of input() answers", () => {
    const result = explainRun('a = input("A? ")\nb = input("B? ")\n', ["one"]);
    expect(result.title).toBe("Too many questions");
  });

  it("explains other common beginner errors", () => {
    expect(explainRun('print "hi"\n').hint).toBe('print needs parentheses around what it shows on line 1, like this: print("hi")');
    expect(explainRun("x = 5\nif x = 5:\n    print(x)\n").title).toBe("Use == to compare");
    expect(explainRun('print("hi"\n').title).toBe("Missing )");
    expect(explainRun('print("hi"))\n').title).toBe("Extra )");
    expect(explainRun("if True\n    print(1)\n").title).toBe("Missing colon");
    expect(explainRun('"Kratos" = character\n').hint).toContain('character = "Kratos"');
    expect(explainRun("print(“hi”)\n").title).toBe("Curly quotes");
    expect(explainRun('n = int("abc")\n').title).toBe("Not a number");
    expect(explainRun("items = [1, 2]\nprint(items[5])\n").title).toBe("Nothing at that position");
    expect(explainRun('print = "hi"\nprint("x")\n').title).toBe("Name already taken");
    expect(explainRun("import ranodm\n").title).toBe("No module with that name");
    expect(explainRun("import random\nprint(random.randnt(1, 6))\n").hint).toContain("Did you mean randint?");
    expect(explainRun('print("5" - 2)\n').title).toBe("Math with text");
    expect(explainRun("print(2(3 + 4))\n").title).toBe("Use * to multiply");
    expect(explainRun("def f(a):\n    return a\nf()\n").title).toBe("Wrong number of values");
    expect(explainRun("x = 5x\n").title).toBe("Number stuck to letters");
  });

  it("explains a forgotten import", () => {
    const result = explainRun("print(random.randint(1, 6))\n");
    expect(result.title).toBe("Missing import");
    expect(result.hint).toContain("import random");
  });

  it("explains timeouts and endless printing", () => {
    const timeout = explainCourseError("TimeoutError: The program ran too long and was stopped.", "while True:\n    x = 1\n");
    expect(timeout.title).toBe("Ran too long");
    expect(timeout.hint).toContain("while loop");
    expect(explainCourseError("The program ran too long and was stopped.", "").title).toBe("Ran too long");
    const flood = explainRun('while True:\n    print("again")\n');
    expect(flood.title).toBe("Printing forever?");
  });

  it("reads Pyodide-style <exec> tracebacks too", () => {
    const raw = [
      "Traceback (most recent call last):",
      '  File "/lib/python313.zip/_pyodide/_base.py", line 597, in eval_code_async',
      '  File "<exec>", line 3, in <module>',
      "NameError: name 'fireball' is not defined",
    ].join("\n");
    const result = explainCourseError(raw, 'a = 1\nb = 2\nprint(fireball)\n');
    expect(result.title).toBe("Missing quotes?");
    expect(result.raw).toBe(raw);
  });

  it("falls back to a plain explanation", () => {
    expect(explainCourseError("", "").title).toBe("Python error");
    const other = explainCourseError("Traceback (most recent call last):\nOverflowError: too big", "");
    expect(other.hint).toContain("OverflowError");
    expect(other.hint).not.toContain("theater");
    expect(explainCourseError("KeyError: 'gate'", "").title).toBe("Missing key");
    expect(explainCourseError("Python could not load its lesson tools (HTTP 404). Reload the page.", "")).toEqual({
      title: "Python had a problem",
      hint: "Python could not load its lesson tools (HTTP 404). Reload the page.",
      raw: "Python could not load its lesson tools (HTTP 404). Reload the page.",
    });
  });
});

describe("name helpers", () => {
  it("finds the names code makes, with their lines", () => {
    const names = definedNames(
      'pizza = 4\nfor i, item in enumerate(items):\n    pass\ndef add(a, b=2):\n    return a\nimport random as r\nx += 1\n',
    );
    expect(names).toEqual(
      expect.arrayContaining([
        { name: "pizza", line: 1 },
        { name: "i", line: 2 },
        { name: "item", line: 2 },
        { name: "add", line: 4 },
        { name: "a", line: 4 },
        { name: "b", line: 4 },
        { name: "r", line: 6 },
        { name: "x", line: 7 },
      ]),
    );
  });

  it("prefers a case match, then a close spelling", () => {
    expect(closeName("spell", ["Spell", "spells"])).toBe("Spell");
    expect(closeName("mana_cots", ["mana_cost", "max_mana"])).toBe("mana_cost");
    expect(closeName("left", ["list", "len"])).toBeNull();
    expect(closeName("count", ["_count"])).toBeNull();
  });
});
