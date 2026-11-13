import { describe, expect, it } from "vitest";
import { closeName, definedNames, explainCourseError, explainQuietSlip, type ExplainContext } from "./explain";
import { runCourseChecks } from "./run-course";

/** Run the code like a course run and explain the real traceback Python gives. */
function explainRun(code: string, stdin?: string[], context?: ExplainContext) {
  const result = runCourseChecks(code, [], { stdin });
  expect(result.ok, `expected ${JSON.stringify(code)} to crash`).toBe(false);
  return explainCourseError(result.traceback, code, context);
}

/** The traceback Python gives for `code` (it must crash). */
function tracebackOf(code: string): string {
  const result = runCourseChecks(code, []);
  expect(result.ok, `expected ${JSON.stringify(code)} to crash`).toBe(false);
  return result.traceback;
}

describe("explainCourseError: the class's real slips", () => {
  it("explains a missing closing quote, with the text quoted correctly", () => {
    const result = explainRun('print("Hello)\n');
    expect(result.title).toBe("Missing quote");
    expect(result.hint).toBe(
      'The text on line 1 is missing its closing quote. Text needs a quote at the start and at the end, like this: print("Hello")',
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
    expect(result.title).toBe("Missing quotes");
    expect(result.hint).toBe(
      'Line 1 has words with no quotes around them, so Python tries to read them as code. Text needs quotes at the start and the end, like this: print("Hello world")',
    );
  });

  it("puts quotes around several words typed without them, using the student's own line", () => {
    const cases: [string, string][] = [
      ["caster = Gear shift\n", 'caster = "Gear shift"'],
      ["caster = spartin rage in barsed hamah\n", 'caster = "spartin rage in barsed hamah"'],
      ["caster = Gearshift.\n", 'caster = "Gearshift"'],
      ["line = The decay is accelerating.\n", 'line = "The decay is accelerating."'],
      ["print(Gearshift has 20 mana.)\n", 'print("Gearshift has 20 mana.")'],
      ['caster = "Gearshift"\nprint(caster has 20 mana.)\n', 'print(caster, "has 20 mana.")'],
    ];
    for (const [code, fixed] of cases) {
      const result = explainRun(code);
      expect(result.title, code).toBe("Missing quotes");
      expect(result.hint, code).toMatch(/has words with no quotes around them/);
      expect(result.hint.endsWith(`like this: ${fixed}`), `${code} -> ${result.hint}`).toBe(true);
    }
  });

  it("asks for a comma between two variables side by side", () => {
    const result = explainRun('caster = "Gearshift"\nmana = 20\nprint(caster mana)\n');
    expect(result.title).toBe("Missing comma");
    expect(result.hint).toBe("Line 3 has values side by side with nothing between them. Put a comma between them, like this: print(caster, mana)");
  });

  it("closes forgotten quotes before a + or a comma, not after the whole line", () => {
    const welcome = explainRun('name = input("Who goes there? ")\nprint("Welcome, + name)\n', ["Lucky"]);
    expect(welcome.title).toBe("Missing quote");
    expect(welcome.hint).toContain('print("Welcome, " + name)');
    expect(welcome.hint).not.toContain('"Welcome, + name"');
    const mana = explainRun('caster = "Gearshift"\nmana = 20\nprint(caster + " has + str(mana) + " mana.")\n');
    expect(mana.hint).toContain('print(caster + " has " + str(mana) + " mana.")');
    expect(explainRun('strength = 5\nprint("Strength:, strength)\n').hint).toContain('print("Strength:", strength)');
    // Real text with a comma or a plus sign keeps the plain advice.
    expect(explainRun('print("Hello, world)\n').hint).toContain('like this: print("Hello, world")');
    expect(explainRun('print("2 + 2 = 4)\n').hint).toContain('like this: print("2 + 2 = 4")');
  });

  it("offers the code's own variables when a lowercase name is unknown (a name copied from the example)", () => {
    const result = explainRun('name = input("Who goes there? ")\nprint("Hello, " + traveler)\n', ["Lucky"]);
    expect(result.title).toBe("Unknown name");
    expect(result.hint).toBe(
      'Python doesn\'t know traveler. If it\'s a variable, use one your code made: name (spelled exactly). If it\'s text, put quotes around it: "traveler"',
    );
    // A capitalized word is most likely text (a name like Gearshift).
    expect(explainRun('mana = 20\nprint(Gearshift)\n').title).toBe("Missing quotes?");
    // The variable being made on this line is not offered.
    expect(explainRun("spell = fireball\n").title).toBe("Missing quotes?");
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
    expect(explainRun('  print("x")\n').hint).not.toContain("line above");
    expect(explainRun('print("a")\n  print("x")\n').hint).toContain("line above");
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
    expect(explainRun('print "hi"\n').hint).toBe('print needs brackets ( ) around what it shows on line 1, like this: print("hi")');
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
    expect(result.title).toBe("Unknown name");
    expect(result.hint).toContain("use one your code made: a, b");
    expect(result.raw).toBe(raw);
    expect(explainCourseError(raw, "print(fireball)\n").title).toBe("Missing quotes?");
  });

  it("prefers the student's main.py line over helper <exec> frames", () => {
    const raw = [
      "Traceback (most recent call last):",
      '  File "<exec>", line 306, in _course_run',
      '  File "main.py", line 2, in <module>',
      '  File "<exec>", line 281, in write',
      "TypeError: unsupported operand type(s) for -: 'str' and 'int'",
    ].join("\n");
    expect(explainCourseError(raw, 'a = "x"\nprint(a - 1)\n').hint).toMatch(/^Line 2 /);
  });

  it("falls back to a plain explanation", () => {
    expect(explainCourseError("", "").title).toBe("Python error");
    const other = explainCourseError("Traceback (most recent call last):\nOverflowError: too big", "");
    expect(other.hint).toContain("OverflowError");
    expect(other.hint).not.toContain("theater");
    expect(explainCourseError("KeyError: 'gate'", "").title).toBe("Missing key");
    expect(explainCourseError("Python could not load its lesson tools (HTTP 404). Reload the page.", "")).toEqual({
      kind: "player-message",
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

/* The exact slips in docs/intro-to-python/design/reviews/curriculum-starting-from-zero.md (§0 and §4.1). */
describe("explainCourseError: starting-from-zero slips", () => {
  it("explains 5P + 2S (invalid decimal literal) with the student's own token", () => {
    const result = explainRun("total_cost = 5P + 2S\n");
    expect(result.kind).toBe("number-stuck-to-name");
    expect(result.hint).toContain("Python can't read 5P");
    expect(result.hint).toContain('doesn\'t mean "5 times P"');
    expect(result.hint).toContain("5 * P");
    // With variables already made, it points at them.
    const own = explainRun("pizza_cost = 4\nsoda_cost = 2\ntotal_cost = 5P + 2S\n");
    expect(own.hint).toContain("use them instead, like pizza_cost and soda_cost");
    // A real variable after the number: just put * in.
    const times = explainRun("pizzas = 4\ntotal_cost = 5pizzas\n");
    expect(times.hint).toBe("Python can't read 5pizzas: a number can't have letters stuck to it. To multiply, put * between them: 5 * pizzas");
    expect(explainRun("x = 3L + 5R\n").hint).toContain("3L");
  });

  it("explains a variable name that starts with a number", () => {
    const first = explainRun('1st_place = "Lucky"\n');
    expect(first.kind).toBe("name-starts-with-number");
    expect(first.hint).toBe("A variable name can't start with a number. Start it with a letter instead, like first_place.");
    expect(explainRun('1player = "Lucky"\n').hint).toContain("like player1");
  });

  it("explains a lone name on a line with no = and no print (NameError)", () => {
    const result = explainRun("canes_women\n");
    expect(result.kind).toBe("lone-name");
    expect(result.title).toBe("A name on its own");
    expect(result.hint).toBe(
      'Line 1 is only a name on its own, so Python looked for a variable called canes_women and found none. To make one, write canes_women = and then a value. To show words, write print("your words").',
    );
    const close = explainRun('caster = "Gearshift"\nCaster\n');
    expect(close.kind).toBe("lone-name");
    expect(close.hint).toContain("Did you mean caster? To show what caster holds, write print(caster).");
    expect(explainRun("Print\n").hint).toContain('Did you mean print? To show words, write print("your words").');
    // A lone name with a comment after it is still alone.
    expect(explainRun("canes_women  # the order\n").kind).toBe("lone-name");
  });

  it("explains def: and def ( ) used to make a variable, with the student's own name and value", () => {
    const colon = explainRun('def: Power_up= ("Fire Ball")\n');
    expect(colon.kind).toBe("def-for-variable");
    expect(colon.hint).toBe(
      'def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value, with no def: Power_up = "Fire Ball"',
    );
    // The sheet's real line also forgot the quote: one message fixes both.
    const both = explainRun('def: Power_up= ("Fire Ball\n');
    expect(both.kind).toBe("def-for-variable");
    expect(both.hint).toContain('Text needs a quote at both ends too: Power_up = "Fire Ball"');
    expect(explainRun('def ("character")\n').kind).toBe("def-for-variable");
    expect(explainRun('def character: "Kratos"\n').hint).toContain('character = "Kratos"');
  });

  it("explains '(' was never closed, with the line fixed", () => {
    const result = explainRun('Power_up = ("Fire Ball"\n');
    expect(result.kind).toBe("never-closed");
    expect(result.title).toBe("Missing )");
    expect(result.hint).toBe(
      'A ( on line 1 opens but never closes. Brackets come in pairs, like quotes. Add ) at the end of the line: Power_up = ("Fire Ball")',
    );
    // Python reports the line where the ( opened, even when the next line is fine.
    expect(explainRun('print("Fire Ball"\nprint("ready")\n').hint).toContain('print("Fire Ball")');
    // A list or dictionary over several lines: the closing bracket goes after the last item.
    const dict = explainRun('stats = {\n    "hp": 10,\n    "mana": 5\n');
    expect(dict.title).toBe("Missing }");
    expect(dict.hint).toContain("Add } on its own line after the last item.");
  });

  it("fixes a missing quote and a missing ) together, so the second error never comes", () => {
    const result = explainRun('Power_up = ("Fire Ball\n');
    expect(result.kind).toBe("missing-quote");
    expect(result.hint).toBe(
      'The text on line 1 is missing its closing quote, and the line is missing its closing ). Quotes and brackets come in pairs. Write: Power_up = ("Fire Ball")',
    );
  });

  it("explains a dash used for =, alone or with a missing quote", () => {
    expect(explainRun('character - "Zelda"\n').kind).toBe("dash-for-equals");
    const both = explainRun('chicken_sandwich - "Fireball\n');
    expect(both.kind).toBe("dash-and-quote");
    expect(both.hint).toBe(
      'Line 1 needs two fixes: the text needs its closing quote, and the dash - should be an equals sign =. Write: chicken_sandwich = "Fireball"',
    );
  });

  it("says 'One fixed' when a new error follows the one before (Python stops at the first error)", () => {
    const previous = tracebackOf('chicken_sandwich - "Fireball\n');
    const result = explainRun('chicken_sandwich - "Fireball"\n', [], { previous });
    expect(result.kind).toBe("dash-for-equals");
    expect(result.hint).toMatch(/^One fixed! Python found the next one\. Line 1 uses a dash/);
    // The same error again, or an error earlier in the code, gets no "One fixed".
    expect(explainRun('chicken_sandwich - "Fireball\n', [], { previous }).hint).not.toContain("One fixed");
    const later = tracebackOf('print("ok")\nprint(oops)\n');
    expect(explainRun('print(oops\nprint("ok")\n', [], { previous: later }).hint).not.toContain("One fixed");
    expect(explainRun("print(oops)\n", [], { previous: "TimeoutError: The program ran too long and was stopped." }).hint).not.toContain(
      "One fixed",
    );
  });

  it("asks for the comma at the end of a dictionary line", () => {
    const result = explainRun('stats = {\n    "hp": 10\n    "mana": 5\n}\n');
    expect(result.kind).toBe("missing-comma-in-list");
    expect(result.hint).toBe('Inside a dictionary { }, every item except the last needs a comma after it. Add a comma at the end of line 2: "hp": 10,');
    expect(explainRun("scores = [\n    10\n    20\n]\n").hint).toContain("Inside a list [ ]");
  });
});

describe("explainCourseError: the reviewer's findings", () => {
  it("quotes multi-word text even when the line already has quoted text", () => {
    const named = explainRun('print("Name:", spartan rage)\n');
    expect(named.kind).toBe("unquoted-words");
    expect(named.hint).toContain('like this: print("Name:", "spartan rage")');
    const joined = explainRun('caster = "The " + spartan rage in barsed hamah\n');
    expect(joined.hint).toContain('like this: caster = "The " + "spartan rage in barsed hamah"');
    expect(explainRun("caster = spartan rage in barsed hamah\n").hint).toContain('caster = "spartan rage in barsed hamah"');
    expect(explainRun("print(spartan rage in barsed hamah)\n").hint).toContain('print("spartan rage in barsed hamah")');
  });

  it("says a name is from the example, and names the task's variable instead", () => {
    const context = { example: 'traveler = input("Name? ")\nprint("Hello, " + traveler)\n', names: ["name"] };
    const result = explainRun('name = input("Who goes there? ")\nprint("Hello, " + traveler)\n', ["Lucky"], context);
    expect(result.kind).toBe("example-name");
    expect(result.title).toBe("Name from the example");
    expect(result.hint).toBe("traveler is the name from the example. This task uses name, so write name here.");
    expect(result.hint).not.toContain("quotes");
    // Without the task's names, the code's own variables are offered.
    const own = explainRun('name = input("Who goes there? ")\nprint("Hello, " + traveler)\n', ["Lucky"], { example: context.example });
    expect(own.hint).toBe("traveler is the name from the example. This task uses name, so write name here.");
    // A name the task shares with the example is not "from the example".
    expect(explainRun("print(name)\n", [], { example: context.example, names: ["traveler"] }).kind).not.toBe("example-name");
  });

  it("builds the missing-quote fix from the unclosed text, not from everything after the first quote", () => {
    const end = explainRun('name = "Lucky"\nprint("Welcome, " + name + "!)\n');
    expect(end.kind).toBe("missing-quote");
    expect(end.hint).toContain('like this: print("Welcome, " + name + "!")');
    expect(explainRun('print(str("Hi))\n').hint).toContain('print(str("Hi"))');
    const join = explainRun('name = "Lucky"\nprint("Welcome, + name)\n');
    expect(join.hint).toContain('print("Welcome, " + name)');
    // The apostrophe and mismatched cases keep their own advice.
    expect(explainRun("print('It's fun')\n").kind).toBe("apostrophe");
    expect(explainRun("print(\"It's fun')\n").hint).toContain('like "It\'s fun"');
  });
});

describe("explainCourseError: every explanation has a kind", () => {
  it("tags common errors with stable kinds", () => {
    const cases: [string, string][] = [
      ['print("Hello)\n', "missing-quote"],
      ["print(“hi”)\n", "curly-quote"],
      ["spell = fireball\n", "unquoted-word"],
      ['Spell = "fire"\nprint(spell)\n', "capital-letters"],
      ["mana_cost = 5\nprint(mana_cots)\n", "spelling"],
      ["count += 1\n", "make-it-first"],
      ["print(total)\ntotal = 1\n", "used-too-early"],
      ['score = 5\nprint("Score: " + score)\n', "text-plus-number"],
      ["print(10 / 0)\n", "divide-by-zero"],
      ['print "hi"\n', "print-needs-brackets"],
      ["if True\n    print(1)\n", "missing-colon"],
      ['if True:\nprint("x")\n', "indent"],
      ["print(random.randint(1, 6))\n", "missing-import"],
    ];
    for (const [code, kind] of cases) expect(explainRun(code).kind, code).toBe(kind);
    expect(explainCourseError("KeyError: 'gate'", "").kind).toBe("missing-key");
    expect(explainCourseError("", "").kind).toBe("other");
    expect(explainCourseError("The program ran too long and was stopped.", "").kind).toBe("timeout");
  });
});

describe("explainQuietSlip: lines that run with no error and do nothing", () => {
  it("catches a lone quoted string (Python runs it and forgets it)", () => {
    const slip = explainQuietSlip('"chick-fa-le_women"\n');
    expect(slip?.kind).toBe("bare-value");
    expect(slip?.line).toBe(1);
    expect(slip?.hint).toContain('To show it, put it inside print( ): print("chick-fa-le_women")');
    const named = explainQuietSlip('"chick-fa-le_women"\n', { missingName: "character" });
    expect(named?.hint).toBe(
      'Line 1 is a value on its own: "chick-fa-le_women". Python reads it, then forgets it, because no variable keeps it. To keep it, put character = in front of it: character = "chick-fa-le_women"',
    );
    expect(explainQuietSlip("# a note\n20\n")?.line).toBe(2);
  });

  it("catches a name alone, print with no brackets, and a dash that keeps nothing", () => {
    expect(explainQuietSlip('character = "Zelda"\ncharacter\n')).toMatchObject({ kind: "bare-name", line: 2, name: "character" });
    expect(explainQuietSlip("print\n")?.kind).toBe("print-without-brackets");
    const dash = explainQuietSlip("mana = 3\nmana - 20\n");
    expect(dash).toMatchObject({ kind: "dash-no-effect", line: 2, name: "mana" });
    expect(dash?.hint).toContain("write: mana = 20");
  });

  it("leaves real code alone: lists over several lines, docstrings, indented lines, calls", () => {
    for (const code of [
      'items = [\n"a",\n"b"\n]\n',
      'note = """\nhello\n"""\n',
      'if True:\n    "inside"\n',
      'print("hi")\nname = "x"\nprint(name)\n',
      "total = 5 - 2\n",
      'line = "a" \\\n    "b"\n',
    ]) {
      expect(explainQuietSlip(code), code).toBeNull();
    }
    // The lone line really does run with no error, which is why only a check can catch it.
    expect(runCourseChecks('"chick-fa-le_women"\n', []).ok).toBe(true);
  });
});

describe("the explainer never throws", () => {
  it("handles any traceback and any code (fuzzed)", () => {
    let seed = 12345;
    const random = () => {
      seed = (seed * 1103515245 + 12345) % 2147483648;
      return seed / 2147483648;
    };
    const pieces = [
      "print(", ")", "(", '"', "'", "def", ":", "=", "-", "+", "5P", "name", "caster", "\n", "  ", "#", "[", "]", "{", "}",
      '"""', "\\", ",", "traveler", "1st", "None", "if", "x", "€", "“", "\t",
    ];
    const messages = [
      "SyntaxError: unterminated string literal (detected at line 1)",
      "SyntaxError: invalid syntax",
      "SyntaxError: invalid syntax. Perhaps you forgot a comma?",
      "SyntaxError: '(' was never closed",
      "SyntaxError: '{' was never closed",
      "SyntaxError: invalid decimal literal",
      "NameError: name 'caster' is not defined",
      "NameError: name 'x' is not defined. Did you mean: 'X'?",
      "TypeError: unsupported operand type(s) for -: 'str' and 'str'",
      "TypeError: can only concatenate str (not \"int\") to str",
      "IndentationError: unexpected indent",
      "ValueError",
      "",
    ];
    for (let round = 0; round < 400; round += 1) {
      const code = Array.from({ length: Math.floor(random() * 14) }, () => pieces[Math.floor(random() * pieces.length)]).join("");
      const line = 1 + Math.floor(random() * 4);
      const raw = `Traceback (most recent call last):\n  File "main.py", line ${line}, in <module>\n${messages[Math.floor(random() * messages.length)]}`;
      const previous = random() < 0.5 ? undefined : raw.replace(`line ${line}`, `line ${line + 1}`);
      const result = explainCourseError(raw, code, { example: code.split("").reverse().join(""), names: ["name"], previous });
      expect(typeof result.hint, JSON.stringify({ code, raw })).toBe("string");
      expect(result.hint.length).toBeGreaterThan(0);
      expect(() => explainQuietSlip(code, { missingName: "name" })).not.toThrow();
    }
  });
});
