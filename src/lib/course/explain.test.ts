import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import {
  closeName,
  definedNames,
  explainCourseError,
  explainQuietSlip,
  foreignNames,
  GOT_FURTHER_LINE,
  leanExplanation,
  slipName,
  type ExplainContext,
} from "./explain";
import { flattenChecks, gradeCheckpoints } from "./grading";
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

  it("reads an apostrophe inside double-quoted text as an apostrophe, not a closing quote", () => {
    // Unit 1's first exercise: the closing quote dropped from Mar'tu's line. Not "Quotes don't match ... like "Hi. It is me, Mar"".
    const result = explainRun('print("Hi. It is me, Mar\'tu.)\n');
    expect(result.title).toBe("Missing quote");
    expect(result.hint).toBe(
      'The text on line 1 is missing its closing quote. Text needs a quote at the start and at the end, like this: print("Hi. It is me, Mar\'tu.")',
    );
    expect(explainRun('print("The guards\' post is cold)\n').hint).toContain('print("The guards\' post is cold")');
    // A real mismatch with an apostrophe earlier in the text is still a mismatch.
    const mismatch = explainRun("print(\"Barrier's holding.')\n");
    expect(mismatch.title).toBe("Quotes don't match");
    expect(mismatch.hint).toContain(`like "Barrier's holding."`);
  });

  it("explains Unit 1's name slips: a space or a dash in a name", () => {
    const space = explainRun("Max_Mana = 18\nmagical affinity = 9\nprint(magical_affinity)\n");
    expect(space.kind).toBe("space-in-name");
    expect(space.hint).toBe(
      "A name can't have spaces on line 2. Python reads magical and affinity as separate names. Join the words with _ instead: magical_affinity = 9",
    );
    const dash = explainRun("magical-affinity = 9\n");
    expect(dash.kind).toBe("dash-in-name");
    expect(dash.hint).toContain("Python reads - as minus. Join the words with _ instead: magical_affinity = 9");
    // Other slips keep their own advice.
    expect(explainRun("mana = 5\nif mana = 5:\n    print(mana)\n").kind).toBe("compare-with-double-equals");
    expect(explainRun('def companion = "Gearshift"\n').kind).toBe("def-for-variable");
  });

  it("explains Unit 1's math slips: brackets for the gap, and a number in quotes", () => {
    const bar = explainRun('full = "█"\nempty = "░"\nmana = 3\nmax_mana = 5\nbar = full * mana + empty * max_mana - mana\n');
    expect(bar.kind).toBe("bar-needs-brackets");
    expect(bar.hint).toContain("Put brackets around the subtraction so it happens first: bar = full * mana + empty * (max_mana - mana)");
    expect(explainRun('mana = 3\nprint("░" * 5 - mana)\n').hint).toContain('print("░" * (5 - mana))');
    expect(explainRun('mana = 3\nprint(5 - mana * "░")\n').hint).toContain('print((5 - mana) * "░")');
    const quoted = explainRun('stamina = 15\nstamina = stamina - "4"\n');
    expect(quoted.kind).toBe("number-in-quotes");
    expect(quoted.hint).toBe('"4" on line 2 has quotes, so Python treats it as text, not a number. Numbers have no quotes: write 4.');
    // Text that is really text still gets the general advice.
    expect(explainRun('print("Mana" - 3)\n').kind).toBe("math-with-text");
  });

  it("explains two apostrophes typed for a double quote, and a ) typed inside the quotes", () => {
    const twice = explainRun("print(''Shield up'')\n");
    expect(twice.kind).toBe("two-single-quotes");
    expect(twice.hint).toContain('Use one " at each end of the text: print("Shield up")');
    const inside = explainRun('print("Shield up!)"\n');
    expect(inside.kind).toBe("never-closed");
    expect(inside.hint).toBe(
      'The ) on line 1 is inside the quotes, so Python reads it as part of the text. Move it after the closing quote: print("Shield up!")',
    );
  });

  it("names the OPENING quote when only the closing one was typed", () => {
    const result = explainRun('print(Fireball")\n');
    expect(result.title).toBe("Missing quote");
    expect(result.hint).toBe(
      'The text on line 1 is missing its opening quote. Text needs a quote at the start and at the end, like this: print("Fireball")',
    );
    expect(explainRun('hero = Bomb Shell"\n').hint).toContain('hero = "Bomb Shell"');
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

describe("explainCourseError: Unit 1 play-through findings", () => {
  it("sends a case slip to the task's name, and to the line that made the box (name-and-value, exact-names, mend-three)", () => {
    const character = explainRun('Character = "Kratos"\nprint(character)\n', [], { names: ["character"] });
    expect(character.kind).toBe("capital-letters");
    expect(character.hint).toBe(
      "Line 1 makes `Character`, but this task's box is `character`. Python sees them as two different names, because the capital letters differ. Rename it on line 1: `character = \"Kratos\"`",
    );
    expect(character.hint).not.toContain("Use Character");
    const mana = explainRun("Max_Mana = 18\nprint(max_mana)\n", [], { names: ["magical_affinity", "max_mana"] });
    expect(mana.hint).toContain("this task's box is `max_mana`");
    expect(mana.hint).toContain("Rename it on line 1: `max_mana = 18`");
    const stamina = explainRun(
      'print("The fire is low.")\nstamina = 15\nstamina = stamina - 4\nMax_Stamina = 16\nprint(max_stamina)\n',
      [],
      { names: ["stamina", "max_stamina"] },
    );
    expect(stamina.hint).toContain("Line 4 makes `Max_Stamina`, but this task's box is `max_stamina`");
    expect(stamina.hint).toContain("`max_stamina = 16`");
    // The box made right and used wrong: write the task's name where it is used.
    const used = explainRun('character = "Kratos"\nprint(Character)\n', [], { names: ["character"] });
    expect(used.hint).toContain("Line 2 uses `Character`, but this task's box is `character`");
    expect(used.hint).toContain("Write `character` on line 2");
    // Neither spelling is the task's: make both lines match, without picking one.
    const neither = explainRun('Spell = "fire"\nprint(spell)\n', [], { names: ["mana"] });
    expect(neither.hint).toContain("Make both lines match");
    expect(neither.hint).not.toContain("Use Spell");
    // A builtin with a capital keeps its own advice.
    expect(explainRun('Print("hi")\n', [], { names: ["print"] }).hint).toContain("Use print");
  });

  it("says `mana = mana - spell_cost` for a subtraction that keeps nothing (spend-mana, Quick Check status line)", () => {
    const spend = explainQuietSlip("mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana - spell_cost\nprint(mana)\n");
    expect(spend?.kind).toBe("dash-no-effect");
    expect(spend?.hint).toBe(
      "Line 4 works out mana - spell_cost, but nothing keeps the answer, so mana does not change. To keep it, put `mana =` in front: `mana = mana - spell_cost`",
    );
    expect(spend?.hint).not.toContain("mana = spell_cost");
    // A number: Mar'tu's version says whether it is a spend (mana = mana - 3) or a new value (mana = 14).
    const spendNumber = explainQuietSlip("mana = 20\nmana - 3\nprint(mana)\n", { context: { solution: "mana = 20\nmana = mana - 3\nprint(mana)\n" } });
    expect(spendNumber?.hint).toContain("`mana = mana - 3`");
    const newValue = explainQuietSlip("mana = 26\nmana = 21\nmana - 14\nprint(mana)\n", {
      context: { names: ["mana"], solution: "mana = 26\nmana = 21\nmana = 14\nprint(mana)\n" },
    });
    expect(newValue?.hint).toContain("write: mana = 14");
    // Graded like the site: the step message is the slip, not "mana = spell_cost".
    const checkpoints = [{ id: "spend", text: "Spend one spell.", hints: ["a", "b"], checks: [{ name: "spent", code: "assert mana == 14, 'mana did not change'" }] }];
    const code = "mana = 20\nspell_cost = 6\nmana - spell_cost\nprint(mana)\n";
    const grade = gradeCheckpoints(checkpoints, runCourseChecks(code, flattenChecks(checkpoints)), code, { names: ["mana", "spell_cost"] });
    expect(grade.checkpoints[0].message).toContain("`mana = mana - spell_cost`");
  });

  it("points to print, never to a variable, in a task that only prints (Lesson 1A)", () => {
    const printOnly = { names: ["print"], solution: 'print("_ - = are side by side.")\n' };
    const def = explainRun('# Type the symbols\ndef ("symbols")\n', [], printOnly);
    expect(def.kind).toBe("def-for-variable");
    expect(def.hint).toBe('`def` is not needed here: this task only shows words. To show them, write `print("symbols")`');
    const words = { solution: 'print("Steady, now. We go together.")\n' };
    expect(explainRun('def ("Steady now")\n', [], words).hint).toContain('`print("Steady now")`');
    const dash = explainRun('oogrish - "Steady now"\n', [], words);
    expect(dash.kind).toBe("dash-for-equals");
    expect(dash.hint).toContain('write `print("Steady now")`');
    expect(dash.hint).not.toMatch(/variable|oogrish =/);
    const bare = explainQuietSlip('"_ - ="\n', { context: printOnly });
    expect(bare?.kind).toBe("bare-value");
    expect(bare?.hint).toBe('Line 1 is words in quotes with no print, so Python reads it, then forgets it. To show it, write `print("_ - =")`');
    expect(explainRun("Steady\n", [], words).hint).toContain('`print("Steady")`');
    // Once the task makes boxes, the variable advice is right again.
    expect(explainRun('def ("character")\n', [], { names: ["character"], solution: 'character = "Kratos"\nprint(character)\n' }).hint).toContain(
      'character = "your value"',
    );
  });

  it("reads a quoted box name as quotes on a name, and keeps Name goes first for a real swap", () => {
    const quoted = explainRun('"weapon" = "Telegun"\n', [], { names: ["weapon", "companion", "glug_sips", "hero"] });
    expect(quoted.kind).toBe("quoted-name");
    expect(quoted.hint).toBe('A box\'s name has no quotes on line 1. Take the quotes off weapon: `weapon = "Telegun"`');
    expect(quoted.hint).not.toContain("Kratos");
    const swap = explainRun('"Lucky" = hero\n');
    expect(swap.kind).toBe("name-goes-first");
    expect(swap.hint).toContain('hero = "Lucky"');
  });

  it("never suggests a module or a builtin the student has not met (moth is not math)", () => {
    const solo = { names: ["familiar"], solution: 'familiar = "a grumpy moth"\nprint(familiar)\n' };
    for (const word of ["moth", "mop", "ant"]) {
      const result = explainRun(`familiar = ${word}\nprint(familiar)\n`, [], solo);
      expect(result.kind, word).toBe("unquoted-word");
      expect(result.hint, word).toContain(`"${word}"`);
    }
    // An import makes math a name the code made.
    expect(explainRun("import math\nprint(meth.pi)\n").hint).toContain("math");
  });

  it("says a task's box is not made yet, and points at the bare value that should make it (broken-spell-1b)", () => {
    const names = { names: ["weapon", "companion", "glug_sips", "hero"] };
    const lucky = explainRun('weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\n"Lucky"\nprint(hero)\nprint(weapon)\n', [], names);
    expect(lucky.kind).toBe("not-made-yet");
    expect(lucky.hint).toBe(
      'hero is one of this task\'s boxes, but no line makes it yet. Line 4 has the value "Lucky" on its own: put `hero = ` in front of it, `hero = "Lucky"`',
    );
    const none = explainRun('weapon = "Telegun"\nprint(hero)\n', [], names);
    expect(none.hint).toContain("Make it above line 2");
    expect(none.hint).not.toContain('"hero"');
  });

  it("says One fixed only when the error moved later, or the same line now parses with a new slip", () => {
    const quote = tracebackOf("print(\"Shield up!')\n");
    expect(explainRun('print("Shield up!)"\n', [], { previous: quote }).hint).not.toContain("One fixed");
    const moth = tracebackOf("familiar = moth\n");
    expect(explainRun("familiar = cat\n", [], { previous: moth }).hint).not.toContain("One fixed");
    const shell = tracebackOf("companion = Bomb Shell\nprint(companion)\n");
    expect(explainRun("companion = kratos\nprint(companion)\n", [], { previous: shell, names: ["companion"] }).hint).not.toContain("One fixed");
    const first = tracebackOf('print("Shield up.)\nprint(Steady)\n');
    expect(explainRun('print("Shield up.")\nprint(Steady)\n', [], { previous: first }).hint).toMatch(/^One fixed!/);
  });

  it("explains plain words on a line, and symbols with no quotes, without a colon Unit 1 never taught", () => {
    const note = explainRun('Night watch\nprint("Steady, now.")\n');
    expect(note.kind).toBe("unquoted-words");
    expect(note.hint).toContain("start the line with #: `# Night watch`");
    expect(note.hint).toContain('`print("Night watch")`');
    expect(note.hint).not.toContain("colon");
    const symbols = explainRun("print(_ - =)\n");
    expect(symbols.hint).toContain('`print("_ - =")`');
    expect(symbols.hint).not.toContain("colon");
  });
});

describe("explainCourseError: Unit 2's slips (questions, if / elif / else, random, assert)", () => {
  const unit2: ExplainContext = { unitOrder: 2 };

  it("names a sign typed backwards, and writes the line with the sign the right way round", () => {
    const ge = explainRun("roll = 14\nneeded = 15\npassed = roll => needed\n", [], unit2);
    expect(ge.kind).toBe("sign-backwards");
    expect(ge.hint).toBe(
      "Line 3 has `=>`, a sign typed backwards. In Python the `=` always comes second: `>=`. Write: `passed = roll >= needed`",
    );
    expect(explainRun("roll = 5\nif roll =< 3:\n    print(roll)\n", [], unit2).hint).toContain("Write: `if roll <= 3:`");
    expect(explainRun('color = "red"\nprint(color =! "red")\n', [], unit2).hint).toContain('Write: `print(color != "red")`');
    // Signs inside text are words, not code.
    expect(explainRun('print("=> here"\n', [], unit2).kind).toBe("never-closed");
  });

  it("names a blank `___` left from the starter (not 'make it first')", () => {
    const blank = explainRun("roll = 12\nif ___:\n    print(roll)\n", [], unit2);
    expect(blank.kind).toBe("blank-left");
    expect(blank.title).toBe("Fill in the blank");
    expect(blank.hint).toContain("Line 2 still has the blank `___`");
    expect(blank.hint).not.toContain("___ =");
    expect(explainRun("import random\nroll = random.___(1, 6)\n", [], unit2).kind).toBe("blank-left");
  });

  it("names a comparison standing alone: `==` asks, and keeps nothing", () => {
    const made = explainRun('hero == "Lucky"\nprint(hero)\n', [], unit2);
    expect(made.kind).toBe("comparison-alone");
    expect(made.hint).toBe(
      'Line 1 uses `==`, which only asks "is it the same?". It makes nothing, so `hero` was never made. To put a value in a box, use one `=`: `hero = "Lucky"`',
    );
    // With no error at all, it is a quiet slip: a check that cannot find the box says why.
    const quiet = explainQuietSlip("roll = 14\nneeded = 15\nroll >= needed\n", { missingName: "passed" });
    expect(quiet).toMatchObject({ kind: "comparison-alone", line: 3 });
    expect(quiet?.hint).toContain("`passed = roll >= needed`");
    const changed = explainQuietSlip('hero = "Bob"\nhero == "Lucky"\n');
    expect(changed?.hint).toContain('use one `=`: `hero = "Lucky"`');
    expect(changed?.hint).toContain('`print(hero == "Lucky")`');
    // Real code is left alone: a box made from a question, a printed question, an if, a type note, a shift.
    for (const code of ["passed = 3 >= 2\n", "print(3 >= 2)\n", "if 3 >= 2:\n    print(1)\n", "passed: bool = 3 >= 2\n", "x = 1\nx << 2\n"]) {
      expect(explainQuietSlip(code)?.kind, code).not.toBe("comparison-alone");
    }
  });

  it("names unquoted text in an option, one word or several", () => {
    const words = explainRun('choice = "option 2"\nif choice == "option 1":\n    print(1)\nelif choice == option 2:\n    print(2)\n', [], unit2);
    expect(words.kind).toBe("unquoted-option");
    expect(words.hint).toBe(
      'Line 4 compares with option 2, words with no quotes, so Python tries to read them as code. Text in a comparison needs quotes too, like this: `elif choice == "option 2":`',
    );
    const word = explainRun('hero = "Lucky"\nprint(hero == Lucky)\n', [], unit2);
    expect(word.kind).toBe("unquoted-option");
    expect(word.hint).toContain('`print(hero == "Lucky")`');
  });

  it("names an elif or else out of place: after the else, with no if, or not lined up", () => {
    const after = explainRun("x = 1\nif x > 2:\n    print(1)\nelse:\n    print(2)\nelif x > 0:\n    print(3)\n", [], unit2);
    expect(after.kind).toBe("else-not-last");
    expect(after.hint).toContain("Line 6 has `elif` after the `else` on line 4");
    const second = explainRun("x = 1\nif x > 2:\n    print(1)\nelse:\n    print(2)\nelse:\n    print(3)\n", [], unit2);
    expect(second.kind).toBe("else-not-last");
    expect(second.hint).toContain("a second `else`");
    const alone = explainRun("x = 1\nelif x > 0:\n    print(3)\n", [], unit2);
    expect(alone.kind).toBe("elif-without-if");
    expect(alone.title).toBe("elif needs an if");
    const indented = explainRun("roll = 5\nif roll > 3:\n    print(1)\n    else:\n    print(2)\n", [], unit2);
    expect(indented.kind).toBe("else-not-lined-up");
    expect(indented.hint).toContain("the same spaces in front as line 2");
    const spelled = explainRun("roll = 5\nif roll > 3:\n    print(1)\nelse if roll > 1:\n    print(2)\n", [], unit2);
    expect(spelled.kind).toBe("elif-spelling");
    expect(spelled.hint).toContain("Write: `elif roll > 1:`");
    // A for loop's else is real Python, and a right chain with another slip keeps that slip's advice.
    expect(explainRun('choice = "a"\nif choice == "b":\n    print(1)\nelif choice == option 2:\n    print(2)\n', [], unit2).kind).toBe(
      "unquoted-option",
    );
  });

  it("names a number compared with text, and says which line made the text", () => {
    const made = explainRun('roll = 14\nneeded = "15"\npassed = roll >= needed\n', [], unit2);
    expect(made.kind).toBe("compare-number-text");
    expect(made.hint).toBe(
      'Line 2 makes `needed` with quotes: `needed = "15"`. Quotes make text, even when it looks like a number, so line 3 can\'t compare it with a number. Take the quotes off on line 2: `needed = 15`',
    );
    expect(explainRun('mana = 9\ncan_cast = mana >= "9"\n', [], unit2).hint).toContain("Numbers have no quotes: `can_cast = mana >= 9`");
    expect(explainRun('age = input("Age? ")\nprint(age > 12)\n', ["13"], unit2).hint).toContain("int(age)");
  });

  it("names one `=` inside print (a question in Unit 2, a box in Unit 1)", () => {
    const code = 'clock_color = "red"\nprint(clock_color = "red")\n';
    const asked = explainRun(code, [], unit2);
    expect(asked.kind).toBe("equals-in-print");
    expect(asked.hint).toContain('use `==`: `print(clock_color == "red")`');
    const unit1 = explainRun(code, [], { unitOrder: 1 });
    expect(unit1.kind).toBe("equals-in-print");
    expect(unit1.hint).not.toContain("==");
    expect(unit1.hint).toContain('`clock_color = "red"`, then show it: `print(clock_color)`');
  });

  it("names lower(answer): it is answer.lower()", () => {
    const result = explainRun('answer = "YES"\nsaid_yes = lower(answer) == "yes"\n', [], unit2);
    expect(result.kind).toBe("method-as-function");
    expect(result.hint).toContain('Write: `said_yes = answer.lower() == "yes"`');
  });

  it("names randint without random. (with or without the import), and random without its import", () => {
    const bare = explainRun("import random\nroll = randint(1, 6)\n", [], unit2);
    expect(bare.kind).toBe("randint-needs-random");
    expect(bare.hint).toContain("`roll = random.randint(1, 6)`");
    expect(bare.hint).not.toContain("import random");
    const none = explainRun("roll = randint(1, 20)\n", [], unit2);
    expect(none.kind).toBe("randint-needs-random");
    expect(none.hint).toContain("Add `import random` as the first line");
    expect(explainRun("roll = random.randint(1, 6)\n", [], unit2).kind).toBe("missing-import");
  });

  it("names the student's own assert that came out False", () => {
    const result = explainRun("roll = 14\nneeded = 15\npassed = roll >= needed\nassert passed == True\n", [], unit2);
    expect(result.kind).toBe("assert-failed");
    expect(result.hint).toContain("The `assert` on line 4 asked `passed == True` and got False");
    expect(explainRun('roll = 5\nassert roll > 9, "too low"\n', [], unit2).hint).toContain("Its note says: too low.");
  });

  it("names a missing colon (or a semicolon for one) with the line written right, and one = in a question", () => {
    const colon = explainRun("hours_left = 2\nif hours_left < 3\n    print(1)\n", [], unit2);
    expect(colon.kind).toBe("missing-colon");
    expect(colon.hint).toContain("Write: `if hours_left < 3:`");
    const semicolon = explainRun("hours_left = 2\nif hours_left < 3;\n    print(1)\n", [], unit2);
    expect(semicolon.kind).toBe("missing-colon");
    expect(semicolon.hint).toContain("not a semicolon `;`");
    expect(explainRun("roll = 5\nif roll > 3:\n    print(1)\nelse\n    print(2)\n", [], unit2).hint).toContain("Write: `else:`");
    expect(explainRun("roll = 5\nif roll = 3:\n    print(1)\n", [], unit2).hint).toContain("Write: `if roll == 3:`");
    expect(explainRun('answer = "YES"\nsaid_yes = answer.lower() = "yes"\n', [], unit2).hint).toContain(
      'Write: `said_yes = answer.lower() == "yes"`',
    );
    expect(explainRun("passed = True\nassert passed = False\n", [], unit2).kind).toBe("compare-with-double-equals");
  });

  it("never says 'make it with def' before the Functions unit", () => {
    expect(explainRun('shout("hi")\n', [], { unitOrder: 1 }).hint).not.toContain("def");
    expect(explainRun('shout("hi")\n', [], { unitOrder: 2 }).hint).not.toContain("def");
    expect(explainRun('shout("hi")\n', [], { unitOrder: 3 }).hint).toContain("make it with def");
    // Without a unit (an old caller), the advice is unchanged.
    expect(explainRun('shout("hi")\n').hint).toContain("make it with def");
  });
});

describe("explainCourseError: the lean explainer (explainer: \"lean\")", () => {
  it("names the kind of slip and the line, and leaves out the fix", () => {
    const code = "roll = 14\nneeded = 15\npassed = roll => needed\n";
    const lean = explainRun(code, [], { unitOrder: 2, explainer: "lean" });
    expect(lean.kind).toBe("sign-backwards");
    expect(lean.explainer).toBe("lean");
    expect(lean.title).toBe("Sign typed backwards");
    expect(lean.hint).toBe(
      "The slip is on line 3: a sign typed backwards. Python's last line, below, says what it found. Mend it yourself, then Run again.",
    );
    expect(lean.hint).not.toContain(">=");
    // Python's own message is kept whole, for the player to show.
    expect(lean.raw).toContain("SyntaxError: invalid syntax");
  });

  it("never gives the fixed line for any Unit 2 slip, and keeps titles free of code marks", () => {
    const codes = [
      "roll = 5\nif ___:\n    print(1)\n",
      'hero == "Lucky"\nprint(hero)\n',
      'choice = "a"\nif choice == option 2:\n    print(2)\n',
      'roll = 14\nneeded = "15"\npassed = roll >= needed\n',
      'clock_color = "red"\nprint(clock_color = "red")\n',
      'answer = "YES"\nprint(lower(answer))\n',
      "import random\nroll = randint(1, 6)\n",
      "x = 1\nelif x > 0:\n    print(3)\n",
      "roll = 5\nif roll > 3\n    print(1)\n",
    ];
    for (const code of codes) {
      const full = explainRun(code, [], { unitOrder: 2 });
      const lean = explainRun(code, [], { unitOrder: 2, explainer: "lean" });
      expect(lean.kind, code).toBe(full.kind);
      expect(lean.hint, code).toContain(slipName(full.kind));
      expect(lean.hint, code).not.toContain("Write:");
      expect(lean.title, code).not.toContain("`");
    }
  });

  it("leaves a run that took too long as it is (there is no slip to name)", () => {
    const timeout = explainCourseError("TimeoutError: The program ran too long and was stopped.", "while True:\n    x = 1\n", {
      explainer: "lean",
    });
    expect(timeout.kind).toBe("timeout");
    expect(timeout.hint).toContain("while loop");
    expect(leanExplanation(timeout)).toBe(timeout);
  });
});

describe("explainCourseError: a run that got further", () => {
  const first = 'print("Shield up.)\nprint(Steady)\n';
  const second = 'print("Shield up.")\nprint(Steady)\n';

  it("in a debugging exercise, marks the progress and leaves the hint without a prefix (the player shows one line)", () => {
    const previous = tracebackOf(first);
    const result = explainRun(second, [], { previous, debugging: true });
    expect(result.gotFurther).toBe(true);
    expect(result.hint).not.toContain("One fixed");
    expect(GOT_FURTHER_LINE).toBe("Python got further: that slip is mended.");
    // Elsewhere the hint keeps its "One fixed!" start, as before.
    const ordinary = explainRun(second, [], { previous });
    expect(ordinary.gotFurther).toBe(true);
    expect(ordinary.hint).toMatch(/^One fixed! Python found the next one\./);
  });

  it("counts a different run-time slip on the same line as progress, but never the same error again", () => {
    const named = tracebackOf('roll = 12\nprint("Rolled: " + rol)\n');
    const typed = explainRun('roll = 12\nprint("Rolled: " + roll)\n', [], { previous: named, debugging: true });
    expect(typed.kind).toBe("text-plus-number");
    expect(typed.gotFurther).toBe(true);
    expect(explainRun('roll = 12\nprint("Rolled: " + rol)\n', [], { previous: named, debugging: true }).gotFurther).toBeUndefined();
  });

  it("keeps the progress mark in a lean explainer, with its prefix outside a debugging exercise", () => {
    const previous = tracebackOf(first);
    const lean = explainRun(second, [], { previous, explainer: "lean" });
    expect(lean.gotFurther).toBe(true);
    expect(lean.hint).toMatch(/^One fixed! Python found the next one\. The slip is on line 2/);
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

describe("explainCourseError: Unit 2 play-through findings", () => {
  it("names `else` with a question as its own slip, not a missing colon (full and lean)", () => {
    const code = "strength_roll = 14\nstrength_needed = 12\nif strength_roll >= strength_needed:\n    print(\"The latch pops open.\")\nelse strength_roll < strength_needed:\n    print(\"That latch hates me.\")\n";
    const full = explainRun(code);
    expect(full.kind).toBe("else-has-question");
    expect(full.hint).toContain("Write just `else:`");
    expect(full.hint).not.toMatch(/needs a colon/);
    const noColon = explainRun(code.replace("strength_needed:\n    print(\"That", "strength_needed\n    print(\"That"));
    expect(noColon.kind).toBe("else-has-question");
    const lean = explainRun(code, [], { explainer: "lean" });
    expect(lean.hint).toBe("The slip is on line 5: a question after `else`. Python's last line, below, says what it found. Mend it yourself, then Run again.");
    // `else:` itself and `else if` keep their own words.
    expect(explainRun("x = 1\nif x > 2:\n    print(1)\nelse if x > 0:\n    print(2)\n").kind).toBe("elif-spelling");
  });

  it("reads a capital on one of Python's words, and an elif with no question", () => {
    const big = explainRun("hours_left = 2\nIf hours_left < 3:\n    print(\"Get inside!\")\n");
    expect(big.kind).toBe("keyword-capital");
    expect(big.hint).toBe("Line 2 starts with `If`. Python's own words are all small letters: `if`, not `If`. Write: `if hours_left < 3:`");
    const otherwise = explainRun("x = 1\nif x < 3:\n    print(1)\nElse:\n    print(2)\n");
    expect(otherwise.kind).toBe("keyword-capital");
    expect(otherwise.hint).toContain("Write: `else:`");
    const bare = explainRun("x = 1\nif x < 3:\n    print(1)\nelif:\n    print(2)\n");
    expect(bare.kind).toBe("no-question");
    expect(bare.hint).toContain("`elif:` with no question");
    expect(bare.hint).toContain("write `else:` instead");
    expect(explainRun("If hours_left <= 2:\n    print(1)\n", [], { explainer: "lean" }).hint).toContain(
      "a capital letter in one of Python's words",
    );
    // Words typed without quotes that happen to start with a capital If are not read as Python's `if`.
    expect(explainRun("If you dare, enter\n").kind).not.toBe("keyword-capital");
    expect(explainRun("Import the dice\n").kind).not.toBe("keyword-capital");
    expect(explainRun("Import random\nprint(random.randint(1, 6))\n").hint).toContain("Write: `import random`");
  });

  it("offers the task's names only when one is close, and never quotes for a number in math (Anatomy of a fizzle)", () => {
    const starter =
      'hero = "Bomb Shell"\nmana = 12\nspell_cost = 5\nprint("Mana left: " + str(mana - mana_cost))\nprint(hero + " casts Shield.")\n\nbad_line = 0\nerror_type = ""\nmissing_name = ""\n';
    const result = explainRun(starter, [], { names: ["bad_line", "error_type", "missing_name"] });
    expect(result.kind).toBe("unknown-name");
    expect(result.hint).toBe("Python doesn't know mana_cost: no line in your code makes it. Line 3 makes `spell_cost`, which has a similar name.");
    expect(result.hint).not.toContain("bad_line");
    expect(result.hint).not.toContain("quotes");
    // A task name a letter or two away is still offered, with the quotes when text could go there.
    const near = explainRun('hero = "Lucky"\nprint(heroes_name)\n', [], { names: ["hero", "heros_name"] });
    expect(near.hint).toContain("use this task's name: heros_name");
  });

  it("counts any run that now reads after a SyntaxError as further (Broken spell 2B's import on line 1)", () => {
    const parse = tracebackOf("roll = random.randint(1, 20)\nx = 5\nif x <= 2:\n    print(1)\nelse:\n    print(2)\nelif x <= 12:\n    print(3)\n");
    const named = explainRun("roll = random.randint(1, 20)\nx = 5\nif x <= 2:\n    print(1)\nelif x <= 12:\n    print(3)\nelse:\n    print(2)\n", [], {
      previous: parse,
      debugging: true,
    });
    expect(named.kind).toBe("missing-import");
    expect(named.gotFurther).toBe(true);
    // The same unquoted slip on the same line is still not a fix.
    const shell = tracebackOf("companion = Bomb Shell\nprint(companion)\n");
    expect(explainRun("companion = kratos\nprint(companion)\n", [], { previous: shell, names: ["companion"] }).gotFurther).toBeUndefined();
  });

  it("asks for a comparison sign, not ==, when Mar'tu's version prints the box with another sign", () => {
    const solution = 'clock_color = "Red"\nclock_is_red = (clock_color == "red")\nprint(clock_is_red)\nprint(clock_color != "red")\n';
    const result = explainRun('clock_color = "red"\nprint(clock_color = "red")\n', [], { solution, unitOrder: 2 });
    expect(result.kind).toBe("equals-in-print");
    expect(result.hint).toContain("such as `==` (is the same as) or `!=`");
    expect(result.hint).not.toContain('print(clock_color == "red")');
    // With == in Mar'tu's version (or no version at hand), the line is written as before.
    expect(explainRun('clock_color = "red"\nprint(clock_color = "red")\n', [], { unitOrder: 2 }).hint).toContain('print(clock_color == "red")');
  });

  it("names def again when Python's 'expected (' led to a recipe, with no One fixed (= is not def)", () => {
    const previous = tracebackOf('def hero = "Lucky"\nprint(hero + " is ready.")\n');
    const result = explainRun('def hero(): "Lucky"\nprint(hero + " is ready.")\n', [], { previous, names: ["hero"], unitOrder: 2 });
    expect(result.kind).toBe("def-for-variable");
    expect(result.hint).toContain('`hero = "Lucky"`');
    expect(result.hint).not.toContain("One fixed");
    expect(result.gotFurther).toBeUndefined();
    expect(result.hint).not.toContain("unsupported operand");
  });
});

/* ---------------------------------------------------------------------------------------------- */
/* Unit 3 ("First Recipes"): the teacher's site requests, from the unit's own wrong answers        */
/* ---------------------------------------------------------------------------------------------- */

type RawCode = string | string[];
type RawExercise = {
  id: string;
  names?: string[];
  solution?: RawCode;
  starter?: RawCode;
  example?: { code: RawCode };
  explainer?: "full" | "lean";
  checkpoints?: { hints: string[] }[];
  bonus?: { solution?: RawCode };
};

/** Unit 3 as exported: every exercise (with its context) and the wrong answers the harness proved for it. */
const unit3 = (() => {
  const dir = path.join(process.cwd(), "content/courses/intro-python/units");
  const unit = JSON.parse(readFileSync(path.join(dir, "first-recipes.json"), "utf8")) as {
    order: number;
    items: (RawExercise & { kind: string; exercises?: RawExercise[] })[];
  };
  const side = JSON.parse(readFileSync(path.join(dir, "first-recipes.verify.json"), "utf8")) as {
    exercises: Record<string, { wrongAnswers?: { why: string; code: RawCode; failsAt: number; messageContains?: string }[] }>;
  };
  const text = (code: RawCode | undefined) => (Array.isArray(code) ? `${code.join("\n")}\n` : (code ?? ""));
  const exercises = new Map<string, RawExercise>();
  for (const item of unit.items) {
    if (item.kind === "project" || item.kind === "challenge") exercises.set(item.id, item);
    for (const exercise of item.exercises ?? []) exercises.set(`${item.id}/${exercise.id}`, exercise);
  }
  /** The wrong answer of `key` whose `why` contains `why`, with the context the player would give it. */
  return (key: string, why: string) => {
    const exercise = exercises.get(key);
    const wrong = side.exercises[key]?.wrongAnswers?.filter((entry) => entry.why.includes(why)) ?? [];
    expect(exercise, key).toBeTruthy();
    expect(wrong, `${key}: one wrong answer about "${why}"`).toHaveLength(1);
    const context: ExplainContext = {
      unitOrder: unit.order,
      names: exercise?.names,
      solution: text(exercise?.solution),
      example: exercise?.example ? text(exercise.example.code) : undefined,
      explainer: exercise?.explainer,
      // As the player works them out: the names of Mar'tu's Teach me examples in the hints.
      foreign: foreignNames({
        hints: (exercise?.checkpoints ?? []).flatMap((checkpoint) => checkpoint.hints),
        solution: [text(exercise?.solution), text(exercise?.bonus?.solution)].join("\n"),
        starter: text(exercise?.starter),
        names: exercise?.names,
      }),
    };
    return { code: text(wrong[0].code), context, failsAt: wrong[0].failsAt, python: wrong[0].messageContains ?? "" };
  };
})();

describe("explainCourseError: Unit 3's slips (recipes), from the unit's own wrong answers", () => {
  // [exercise, the wrong answer's `why`, Python 3.13's own words (proved by the harness), kind, what the hint says]
  const rows: [string, string, string, string, string][] = [
    // recipe-like-math (SFZ-2): f(x) = 5x, before compare-with-double-equals.
    ["recipes-with-names/send-it-back", "written like maths", "cannot assign to function call", "recipe-like-math",
      "Line 8 is math's way to write it. In Python a recipe (function) starts with `def`: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["extra-recipe-twins/double-cost", "(a call on the left)", "cannot assign to function call", "recipe-like-math",
      "`def double_cost(price):`, then an indented `return price * 2`."],
    ["extra-recipe-twins/double-cost", "(=, then a colon)", "invalid syntax", "recipe-like-math",
      "Line 1 makes the recipe with `=`, the way a box is made. In Python a recipe (function) starts with `def`: `def double_cost(price):`"],
    // quoted-ingredient (SFZ-5), before def-for-variable.
    ["recipes-with-names/send-it-back", "ingredient name in quotes", "invalid syntax", "quoted-ingredient",
      "Line 8 has an ingredient in quotes. Ingredient names have no quotes: `def max_fuel_for(cells):`"],
    // wrong-number-of-values (SFZ-6): the ingredients read from the student's own def line.
    ["recipes-with-names/ingredients", "hands over nothing", "missing 1 required positional argument", "wrong-number-of-values",
      "`warn` has 1 ingredient (`hero_name`). The call on line 6 hands over nothing. Hand over one value per ingredient."],
    ["recipes-with-names/ingredients", "hands over two values", "takes 1 positional argument", "wrong-number-of-values",
      "`warn` has 1 ingredient (`hero_name`). The call on line 6 hands over 2. Hand over one value per ingredient."],
    ["recipes-with-names/use-the-ingredients", "third call hands over one number", "missing 1 required positional argument",
      "wrong-number-of-values", "`show_hit` has 2 ingredients (`base_damage`, `bonus`). The call on line 6 hands over 1. Hand over one value per ingredient."],
    ["recipes-with-names/send-it-back", "no value handed over", "missing 1 required positional argument", "wrong-number-of-values",
      "`max_mana_for` has 1 ingredient (`affinity`). The call on line 5 hands over nothing."],
    ["extra-recipe-twins/cheer-on", "wrong number of arguments (one value)", "missing 1 required positional argument",
      "wrong-number-of-values", "`cheer_on` has 2 ingredients (`hero_name`, `words`). The call on line 10 hands over 1."],
    ["supply-run", "wrong number of arguments (one value)", "missing 1 required positional argument: 'price'", "wrong-number-of-values",
      "`item_cost` has 2 ingredients (`count`, `price`). The call on line 7 hands over 1."],
    // randint-backwards (SFZ-11): the student's own two values, swapped.
    ["recipes-with-names/roll-recipe", "randint(die_size, 1)", "empty range in randrange(20, 2)", "randint-backwards",
      "Line 5 rolls with the numbers the wrong way round. Smallest number first: `random.randint(1, die_size)`"],
    // Split on commas (RSWM-2): only the bare run of words is quoted; numbers and quoted values stay.
    ["extra-recipe-twins/cheer-on", "split-on-commas", "invalid syntax. Perhaps you forgot a comma?", "unquoted-words",
      'like this: cheer_on("Captain Glug", "Go now")'],
    ["recipes-with-names/ingredients", "two-word hero and no quotes", "invalid syntax. Perhaps you forgot a comma?", "unquoted-words",
      'like this: warn_hours("Captain Glug", 2)'],
    // The unit's names, where they do not exist: a recipe not made yet, called too early, or a name from its kitchen.
    ["recipes-with-names/send-it-back", "try line uncommented", "name 'max_fuel_for' is not defined", "recipe-not-made-yet",
      "`max_fuel_for` is one of this task's recipes, but no `def` line makes it yet. Write it with `def` above line 8, the line that calls it."],
    ["recipes-with-names/box-or-recipe", "called before it is defined", "name 'say_steady' is not defined", "recipe-called-too-early",
      "Line 1 calls `say_steady`, but its `def` is only on line 6."],
    ["recipes-with-names/ingredients", "used outside the recipe", "name 'hero_name' is not defined", "made-inside-recipe",
      "`hero_name` is an ingredient of `warn`, so it only exists inside the recipe while a call runs it. Line 6 is outside the recipe."],
    // A name the recipe never makes, on its `return` line (RNM): the recipe's own box, never "put quotes around it".
    ["recipes-with-names/return-the-right-box", "the starter: `return result`", "name 'result' is not defined", "not-in-recipe",
      "Line 3 hands back `result`, but no line in `armor_total` makes a box by that name. This recipe's box is `total`: hand that back."],
    ["recipes-with-names/broken-spell-6a", "still returns the Example's name", "name 'result' is not defined", "not-in-recipe",
      "This recipe's box is `total`: hand that back."],
    ["extra-recipe-twins/double-cost", "approximate ingredient name", "name 'cost' is not defined", "not-in-recipe",
      "Line 3 hands back `cost`, but `double_cost` has no box or ingredient by that name. Its ingredient is `price`: work the answer out from that."],
    // The store written the wrong way round: the new box on the left, the call on the right.
    ["recipes-with-names/store-then-pass", "store reversed", "name 'greeting' is not defined", "store-backwards",
      "Line 12 puts `greeting` into `get_greeting`, the wrong way round, so Python looks for a box `greeting` that no line makes. The new box goes on the left of `=`, the call on the right: `greeting = get_greeting()`"],
    ["recipes-with-names/send-it-back", "return not indented", "'return' outside function", "indent",
      "Line 3's `return` has no spaces in front, so it is outside the recipe `max_mana_for`."],
    ["recipes-with-names/broken-spell-6a", "def still makes the box", "expected '('", "def-for-variable",
      "`def` makes recipes (functions), not boxes. To make a box, write the name, an equals sign, then the value, with no `def`: `hours_left = 37`"],
    // The Unit 3 play-through: `return result` after `fuel = ...` with the try line on (the crash path) ends the
    // ping-pong too, and a box from another recipe's kitchen gets this recipe's own box.
    ["recipes-with-names/send-it-back", "with the try line on (the crash path", "name 'result' is not defined", "not-in-recipe",
      "`result` comes from Mar'tu's example. This recipe's box is `fuel`: hand that back."],
    ["recipes-with-names/send-it-back", "kitchen, with the try line on", "name 'total' is not defined", "made-inside-recipe",
      "`total` belongs to `max_mana_for`, so only that recipe can use it. Inside `max_fuel_for`, hand back its own box, `fuel`."],
    // def and = mixed up inside a recipe task: every form answers with the recipe's def line, never "make a box".
    ["recipes-with-names/send-it-back", "worked out from its ingredient (`max_fuel_for", "name 'cells' is not defined", "recipe-like-math",
      "Line 8 makes `max_fuel_for` with `=`, the way a box is made. `max_fuel_for` is a recipe in this task: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["recipes-with-names/send-it-back", "worked out from its ingredient, with the try line on", "name 'cells' is not defined", "recipe-like-math",
      "`max_fuel_for` is a recipe in this task: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["recipes-with-names/send-it-back", "is made, with the try line on (the box called)", "'int' object is not callable", "recipe-like-math",
      "Line 11 calls `max_fuel_for`, but line 9 makes `max_fuel_for` with `=`, so it is a box, not a recipe (function). `max_fuel_for` is a recipe in this task: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["recipes-with-names/send-it-back", "def mixed with =", "expected '('", "recipe-like-math",
      "Line 8 mixes `def` with `=`. `max_fuel_for` is a recipe in this task: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["recipes-with-names/send-it-back", "with def in front (`def max_fuel_for(cells) = cells * 5`)", "expected ':'", "recipe-like-math",
      "Line 8 puts `=` after the brackets, the way math writes it. In Python the colon goes right after the brackets, and the steps go below: `def max_fuel_for(cells):`, then an indented `return cells * 5`."],
    ["recipes-with-names/send-it-back", "and a colon at the end", "expected ':'", "recipe-like-math",
      "In Python the colon goes right after the brackets, and the steps go below: `def max_fuel_for(cells):`"],
    ["recipes-with-names/box-or-recipe", "the recipe's name in quotes after def", "invalid syntax", "quoted-recipe-name",
      "Line 5 has the recipe's name in quotes. A recipe's name has no quotes: it goes right after `def`, then ( ) and a colon: `def say_steady():`, with its steps indented under it."],
    ["recipes-with-names/box-or-recipe", "= used to make the recipe, then called", "'str' object is not callable", "recipe-like-math",
      "Line 3 calls `say_steady`, but line 2 makes `say_steady` with `=`, so it is a box, not a recipe (function). `say_steady` is a recipe in this task: `def say_steady():`, then its steps, indented under it."],
    // A recipe with no step (its `pass` deleted, or only a note): the rule, never "indent the next line".
    ["recipes-with-names/replace-pass", "pass deleted and nothing written yet", "expected an indented block after function definition on line 2", "indent",
      "`step_north` has no steps yet, and a recipe needs at least one step inside. Write its step under the def line, four spaces in (or put `pass` back while you think)."],
    ["recipes-with-names/replace-pass", "only a note left in the recipe", "expected an indented block after function definition on line 2", "indent",
      "`step_north` has no steps yet, and a recipe needs at least one step inside: a note with # doesn't count."],
    // An ingredient-like name inside the recipe: the ingredient, letter for letter, never quotes.
    ["recipes-with-names/ingredients", "an approximate parameter name", "name 'hero' is not defined", "unknown-name",
      "`hero` is not an ingredient of `warn`. Its ingredient is `hero_name`: use it letter for letter."],
    ["recipes-with-names/use-the-ingredients", "an approximate parameter name", "name 'damage' is not defined", "unknown-name",
      "`damage` is not an ingredient of `show_hit`. Its ingredients are `base_damage` and `bonus`: use `base_damage`, letter for letter."],
    // Start me off at the bottom (before a click): the line goes inside the recipe, in place of `pass`.
    ["recipes-with-names/ingredients", "Start me off pressed before a click", "name 'hero_name' is not defined", "made-inside-recipe",
      "Line 7 is outside the recipe: move this line inside `warn`, in place of `pass`, four spaces in."],
    // A name from a Teach me hint, called: the task's own recipe.
    ["recipes-with-names/store-then-pass", "the Teach me hint's names copied", "name 'get_note' is not defined", "example-name",
      "`get_note` comes from Mar'tu's example. This task's recipe is `get_greeting`: call that one, letter for letter."],
  ];

  it.each(rows)("%s, %s: Python says %s, the explainer names %s", (key, why, python, kind, hint) => {
    const { code, context, failsAt, python: proved } = unit3(key, why);
    expect(failsAt, "a crash wrong answer").toBe(0);
    const raw = tracebackOf(code);
    expect(raw).toContain(python);
    expect(python, "the words the harness proved for this wrong answer").toContain(proved);
    const full = explainCourseError(raw, code, { ...context, explainer: "full" });
    expect(full.kind, code).toBe(kind);
    expect(full.hint).toContain(hint);
    // Python's "positional argument" words are never the explanation (its last line still shows below it).
    expect(full.hint).not.toContain("positional argument");
  });

  it("names the slip, never the fix, in a lean exercise (SOLO and Quick Check), for every new kind", () => {
    const lean: [string, string, string, string][] = [
      ["qc-r1-a/write-a-recipe", "= used to make a recipe (a call on the left)", "recipe-like-math", "The slip is on line 1: a recipe written like math."],
      ["recipes-with-names/send-it-back", "ingredient name in quotes", "quoted-ingredient", "The slip is on line 8: an ingredient name in quotes."],
      ["recipes-with-names/solo-6a", "third call hands over one value", "wrong-number-of-values", "The slip is on line 6: the wrong number of values handed over."],
      ["qc-r1-a/roll-a-die", "one value handed to randint", "wrong-number-of-values", "The slip is on line 7: the wrong number of values handed over."],
      ["qc-r1-b/roll-a-die", "biggest number first", "randint-backwards", "The slip is on line 7: the numbers in the wrong order."],
      ["recipes-with-names/solo-6a", "two words with no quotes", "unquoted-words", "The slip is on line 6: words with no quotes."],
      ["qc-r1-a/write-a-recipe", "the starter (no recipe yet", "recipe-not-made-yet", "The slip is on line 5: a recipe that is not made yet."],
      ["qc-r1-b/write-a-recipe", "called before it is defined", "recipe-called-too-early", "The slip is on line 5: a recipe called before its `def`."],
      ["recipes-with-names/solo-6a", "a name the recipe never makes", "not-in-recipe", "The slip is on line 9: a name this recipe never makes."],
      ["recipes-with-names/solo-6a", "an ingredient printed outside its recipe", "made-inside-recipe", "The slip is on line 7: a name that only lives inside a recipe."],
    ];
    for (const [key, why, kind, hint] of lean) {
      const { code, context } = unit3(key, why);
      const leanContext = { ...context, explainer: "lean" as const };
      const result = explainRun(code, [], leanContext);
      expect(result.kind, `${key}: ${why}`).toBe(kind);
      expect(result.explainer).toBe("lean");
      expect(result.hint).toContain(hint);
      expect(result.title, `${key}: ${why}`).not.toContain("`");
      // The full version's fixed line never shows in the lean one.
      const full = explainRun(code, [], { ...context, explainer: "full" });
      const fix = full.hint.match(/`([^`]*(?:def |randint\(|\("|\(\w+, )[^`]*)`/)?.[1];
      if (fix) expect(result.hint, `${key}: ${why}`).not.toContain(fix);
      expect(slipName(kind as never)).toBeTruthy();
    }
    // The SOLO's unquoted two-word hero, in full: only the words get quotes, the number stays.
    const { code, context } = unit3("recipes-with-names/solo-6a", "two words with no quotes");
    expect(explainRun(code, [], { ...context, explainer: "full" }).hint).toContain('like this: heal("Moth Queen", 5)');
  });

  it("puts each new row before the old one that gave wrong advice", () => {
    const unit3Context: ExplainContext = { unitOrder: 3 };
    // recipe-like-math over compare-with-double-equals ("use two equals signs" was wrong advice).
    const math = "max_fuel_for(cells) = cells * 5\n";
    expect(explainRun(math, [], unit3Context).kind).toBe("recipe-like-math");
    expect(explainRun(math, [], unit3Context).hint).not.toContain("==");
    // A real question keeps its own advice, and before Unit 3 (no def yet) nothing changes.
    expect(explainRun("roll = 5\nif roll = 5:\n    print(roll)\n", [], unit3Context).kind).toBe("compare-with-double-equals");
    expect(explainRun(math, [], { unitOrder: 2 }).kind).toBe("compare-with-double-equals");
    expect(explainRun('print("hi") = 5\n', [], unit3Context).kind).not.toBe("recipe-like-math");
    expect(explainRun("show_hit(4, 3) = 7\n", [], unit3Context).kind).not.toBe("recipe-like-math");

    // quoted-ingredient over def-for-variable (which turned the recipe into a box: `max_fuel_for = "cells"`).
    const quoted = 'def max_fuel_for("cells"):\n    return cells * 5\n';
    const ingredient = explainRun(quoted, [], unit3Context);
    expect(ingredient.kind).toBe("quoted-ingredient");
    expect(ingredient.hint).not.toContain('max_fuel_for = "cells"');
    expect(explainRun('def heal("Moth Queen", 5):\n    pass\n', [], { unitOrder: 3, solution: "def heal(hero_name, amount):\n    pass\n" }).hint).toContain(
      "`def heal(hero_name, amount):`",
    );
    expect(explainRun("def show_hit(4, 3):\n    pass\n", [], unit3Context).hint).toContain(
      "a number where an ingredient's name goes. An ingredient is a name: `def show_hit(value1, value2):`",
    );
    // A box made with def is still that slip, in the unit's words; before Unit 3 the old words stay.
    expect(explainRun('def hero = "Lucky"\n', [], unit3Context).kind).toBe("def-for-variable");
    expect(explainRun(quoted, [], { unitOrder: 2 }).kind).toBe("def-for-variable");
    expect(explainRun(quoted).kind).toBe("def-for-variable");

    // Split on commas over missing-comma and over quoting the whole bracket ("Moth Queen, 5" made two values one).
    for (const context of [undefined, { unitOrder: 1 }, unit3Context]) {
      const heal = explainRun("def heal(hero_name, amount):\n    pass\nheal(Moth Queen, 5)\n", [], context);
      expect(heal.kind).toBe("unquoted-words");
      expect(heal.hint).toContain('like this: heal("Moth Queen", 5)');
      expect(heal.hint).not.toContain('"Moth Queen, 5"');
      const cheer = explainRun('def cheer_on(a, b):\n    pass\ncheer_on("Captain Glug", Go now)\n', [], context);
      expect(cheer.kind).not.toBe("missing-comma");
      expect(cheer.hint).toContain('cheer_on("Captain Glug", "Go now")');
    }
    // A name the program made stays outside the quotes: no guess when it sits in the run of words.
    const named = explainRun('hero = "Pip"\ndef heal(a, b):\n    pass\nheal(hero Lucky, 5)\n', [], unit3Context);
    expect(named.hint).not.toContain('"hero Lucky');
    // not-in-recipe and store-backwards: before the generic unknown-name row ("put quotes around it"), never over a
    // spelling slip of the recipe's own box, a name copied from the example, or a recipe that takes values.
    const rightBox = "def armor_total(base, bonus):\n    total = base + bonus\n    return result\n\nprint(armor_total(1, 2))\n";
    expect(explainRun(rightBox, [], unit3Context).kind).toBe("not-in-recipe");
    expect(explainRun(rightBox, [], unit3Context).hint).not.toContain("quotes");
    expect(explainRun(rightBox, [], { unitOrder: 2 }).kind).toBe("unknown-name");
    expect(explainRun(rightBox.replace("result", "totl"), [], unit3Context).kind).toBe("spelling");
    // A name copied from the example, on a `return` line in a recipe, gets this recipe's own box too (the U3 review:
    // the example-name row listed the task's names, with the recipe's box nowhere first).
    const copied = explainRun(rightBox, [], { ...unit3Context, example: "def f(a):\n    result = a\n    return result\n" });
    expect(copied.kind).toBe("not-in-recipe");
    expect(copied.hint).toBe("`result` comes from Mar'tu's example. This recipe's box is `total`: hand that back.");
    const twoBoxes = "def gold_for(gems):\n    coins = gems * 2\n    bonus = coins + 1\n    return answer\n\nprint(gold_for(1))\n";
    expect(explainRun(twoBoxes, [], unit3Context).hint).toContain(
      "This recipe's boxes are `coins` and `bonus`: hand back the one that holds the answer.",
    );
    const backwards = "def get_line(size):\n    return str(size)\n\ndef show():\n    get_line = line\n    print(line)\n\nshow()\n";
    expect(explainRun(backwards, [], unit3Context).kind).toBe("store-backwards");
    expect(explainRun(backwards, [], unit3Context).hint).toContain("`line = get_line(...)`, with one value per ingredient");
    // print keeps its own rows: a comma there is usually part of the sentence.
    expect(explainRun("print(Hello, my friend)\n").hint).not.toContain('print("Hello", "my friend")');
  });

  it("keeps each row to the units that taught it", () => {
    const roll = "import random\ndef roll_die(die_size):\n    return random.randint(die_size, 1)\nprint(roll_die(20))\n";
    expect(explainRun(roll, [], { unitOrder: 2 }).kind).toBe("randint-backwards");
    expect(explainRun(roll, [], { unitOrder: 1 }).kind).toBe("other");
    // The first value already 1: another slip emptied the range, so nothing is swapped.
    expect(explainRun("import random\nsize = 0\nprint(random.randint(1, size))\n", [], { unitOrder: 3 }).kind).toBe("other");
    // A recipe with no ingredients, and randint with one value.
    expect(explainRun('def warn():\n    print("Get inside!")\nwarn("Pip")\n', [], { unitOrder: 3 }).hint).toBe(
      "`warn` has no ingredients, but the call on line 3 hands over 1.",
    );
    expect(explainRun("import random\nprint(random.randint(6))\n", [], { unitOrder: 2 }).hint).toBe(
      "`random.randint` takes 2 values: the smallest number, then the biggest. The call on line 2 hands over 1.",
    );
    // Before Unit 3 (or with no unit) a call's count gets the plain words, never Python's.
    const count = explainRun("def f(a):\n    return a\nf()\n", [], { unitOrder: 2 });
    expect(count.hint).toBe("The function call on line 3 has the wrong number of values inside its ( ).");
    expect(explainRun("def f(a):\n    return a\nf()\n").hint).not.toContain("positional");
    // The recipe rows need Unit 3: a Unit 2 name keeps its Unit 2 words.
    expect(explainRun("print(max_fuel_for(4))\n", [], { unitOrder: 2, names: ["max_fuel_for"] }).kind).not.toBe("recipe-not-made-yet");
  });

  it("speaks the unit's words from Unit 3 on: recipes, not functions; boxes, not variables", () => {
    const unit3Context: ExplainContext = { unitOrder: 3 };
    expect(explainRun('shout("hi")\n', [], unit3Context).hint).toBe(
      "Python doesn't know a recipe (function) called shout. Check the spelling, or make it with def before you use it.",
    );
    expect(explainRun('def say_ready:\n    print("Ready.")\n', [], unit3Context).hint).toBe(
      "A `def` line needs ( ) after the recipe's name, then a colon: `def say_ready():`",
    );
    expect(explainRun('def say_ready:\n    print("Ready.")\n', [], { unitOrder: 2 }).hint).toContain("after the function's name");
    expect(explainRun('def steadying_words = "Steady, now.\n', [], unit3Context).hint).toContain(
      "`def` makes recipes (functions), not boxes.",
    );
    const inside = explainRun("def max_mana_for(affinity):\n    total = affinity * 2\n    return total\n\nmax_mana_for(13)\nprint(total)\n", [], unit3Context);
    expect(inside.kind).toBe("made-inside-recipe");
    expect(inside.hint).toContain("`total` is made inside `max_mana_for`, so it only exists inside that recipe. Line 6 is outside it.");
    // A box the code also makes outside the recipe is not this slip.
    expect(explainRun("total = 1\ndef f():\n    total = 2\nprint(totl)\n", [], unit3Context).kind).not.toBe("made-inside-recipe");
  });

  it("names a recipe that calls itself, with the line that does it", () => {
    const result = explainRun('def say_steady():\n    print("Steady, now.")\n    say_steady()\n\nsay_steady()\n', [], { unitOrder: 3 });
    expect(result.kind).toBe("never-ending-calls");
    expect(result.hint).toBe(
      "Line 3 calls `say_steady` inside `say_steady` itself, so it starts again and again and never stops. To call it, write the call below the recipe, with no spaces in front.",
    );
  });
});

describe("explainCourseError: the Unit 3 play-through (a reviewer who played the unit)", () => {
  const unit3Context: ExplainContext = { unitOrder: 3 };

  it("keeps the new recipe rows to Unit 3 and to the task's own recipes", () => {
    // A box of the student's own, called: a box, not a recipe (and multiply, for a number); before Unit 3, as before.
    const called = explainRun("mana = 5\nprint(mana(2))\n", [], unit3Context);
    expect(called.kind).toBe("not-a-function");
    expect(called.hint).toBe(
      "Line 2 calls `mana` with ( ), but line 1 makes `mana` with `=`, so it is a box, not a recipe (function). Only a recipe made with `def` can be called. To multiply by it, write * between them.",
    );
    expect(explainRun("mana = 5\nprint(mana(2))\n", [], { unitOrder: 2 }).kind).toBe("use-star-to-multiply");
    expect(explainRun("print(2(3 + 4))\n", [], unit3Context).kind).toBe("use-star-to-multiply");
    // f(x) = 5x with a def in front: before Unit 3 the old colon row stays.
    expect(explainRun("def fuel(cells) = cells * 5\n", [], { unitOrder: 2 }).kind).toBe("def-for-variable");
    expect(explainRun("def fuel(cells) = cells * 5\n", [], unit3Context).kind).toBe("recipe-like-math");
    // `def name = value` for a box of the student's own (not one of the task's recipes) is still def-for-variable.
    const solution = "def max_fuel_for(cells):\n    return cells * 5\n";
    expect(explainRun("def hero = 5\n", [], { ...unit3Context, solution, names: ["max_fuel_for"] }).kind).toBe("def-for-variable");
    expect(explainRun("def max_fuel_for = 5\n", [], { ...unit3Context, solution, names: ["max_fuel_for"] }).kind).toBe("recipe-like-math");
    expect(explainRun("def max_fuel_for = 5\n", [], { unitOrder: 2, solution, names: ["max_fuel_for"] }).kind).toBe("def-for-variable");
    // A box made with = whose right side crashes, when it is NOT a recipe of the task: the old rows.
    expect(explainRun("fuel = cells * 5\n", [], { ...unit3Context, solution, names: ["max_fuel_for", "cells"] }).kind).toBe("not-made-yet");
    // A quoted name after def with no step under it, in no recipe task, is still the def-for-variable slip.
    expect(explainRun('def ("character")\n', [], unit3Context).kind).toBe("def-for-variable");
    expect(explainRun('def ("say_steady"):\n    print("Steady.")\n', [], unit3Context).kind).toBe("quoted-recipe-name");
  });

  it("asks for a step in an empty recipe, and keeps the indent row when the step is there but not indented", () => {
    expect(explainRun("def warn(hero_name):\n\nwarn(\"Pip\")\n", [], unit3Context).hint).toBe(
      "`warn` has no steps yet, and a recipe needs at least one step inside. Write its step under the def line, four spaces in (or put `pass` back while you think).",
    );
    expect(explainRun('def warn(hero_name):\nprint(hero_name)\n', [], unit3Context).hint).toBe(
      "The line after line 1 belongs inside the def, so it needs 4 spaces at the start.",
    );
    // An `if` with nothing under it keeps its own words, and before Unit 3 (def is a slip there) nothing changes.
    expect(explainRun("roll = 3\nif roll > 2:\n\nprint(roll)\n", [], unit3Context).hint).toContain("belongs inside the if");
    expect(explainRun("def hero():\n\nprint(1)\n", [], { unitOrder: 1 }).hint).toBe(
      "The line after line 1 belongs inside the def, so it needs 4 spaces at the start.",
    );
  });

  it("never offers a recipe's name as the box a lone word in brackets meant, and keeps quotes out of an ingredient slip", () => {
    // Replace pass's `scout.step(north)` (the scout lives in the exercise's hidden setup, so a stand-in here).
    const steps = "def say(text):\n    print(text)\n\ndef step_north():\n    say(north)\n\nstep_north()\n";
    const lone = explainRun(steps, [], unit3Context);
    expect(lone.kind).toBe("unquoted-word");
    expect(lone.hint).toBe("Python doesn't know `north`: no line in your code makes it. If it's text, put quotes around it: `say(\"north\")`");
    expect(lone.hint).not.toContain("step_north`, which");
    // A box of the code's own that is like it is still named, after the quotes.
    const withBox = explainRun('north_gate = 2\ndef step_north():\n    pass\n\nprint(north)\n', [], unit3Context);
    expect(withBox.hint).toBe(
      "Python doesn't know `north`: no line in your code makes it. If it's text, put quotes around it: `print(\"north\")` If you meant a box, line 1 makes `north_gate`.",
    );
    // Outside any recipe a name like a box keeps the old row (Units 1-2 too).
    expect(explainRun('hero_name = "Pip"\nprint(hero + "!")\n', [], unit3Context).kind).toBe("unknown-name");
    expect(explainRun('hero_name = "Pip"\nprint(hero + "!")\n', [], unit3Context).hint).toContain("Line 1 makes `hero_name`, which has a similar name.");
  });

  it("works out the names of Mar'tu's Teach me examples, only from code in the hints, and uses them from Unit 3 on", () => {
    const foreign = foreignNames({
      hints: [
        "Which recipe hands back the line?",
        "`note = get_note()` catches what `get_note` hands back. `.lower()` would turn `\"SIT DOWN.\"` into `Sit down.`",
        "Write `greeting = get_greeting()` in place of `pass`.",
      ],
      solution: "def get_greeting():\n    return 'Hi'\n\ndef present():\n    greeting = get_greeting()\n",
      starter: "def present():\n    pass\n",
      names: ["get_greeting"],
    });
    expect(foreign).toEqual(["note", "get_note"]);
    const code = "def get_greeting():\n    return 'Hi'\n\ndef present():\n    note = get_note()\n\npresent()\n";
    const context: ExplainContext = { unitOrder: 3, names: ["get_greeting", "present"], solution: "def get_greeting():\n    return 'Hi'\n", foreign };
    expect(explainRun(code, [], context).hint).toBe(
      "`get_note` comes from Mar'tu's example. This task's recipe is `get_greeting`: call that one, letter for letter.",
    );
    expect(explainRun(code, [], { ...context, unitOrder: 2 }).kind).toBe("unknown-function");
  });

  it("names the new quoted-recipe-name slip in a lean exercise, never the def line", () => {
    const code = '# A recipe holds steps.\ndef ("say_steady"):\n    print("Steady, now.")\n\nsay_steady()\n';
    const lean = explainRun(code, [], { ...unit3Context, explainer: "lean" });
    expect(lean.kind).toBe("quoted-recipe-name");
    expect(lean.hint).toContain("The slip is on line 2: quotes around a recipe's name.");
    expect(lean.hint).not.toContain("def say_steady():");
  });
});

/* ---------------------------------------------------------------------------------------------- */
/* Unit 4 ("Lists"): the teacher's site requests, from the unit's own wrong answers                */
/* ---------------------------------------------------------------------------------------------- */

/** Unit 4 as exported: the wrong answer of `key` whose `why` contains `why`, with the context the player gives it. */
const unit4 = (() => {
  const dir = path.join(process.cwd(), "content/courses/intro-python/units");
  const unit = JSON.parse(readFileSync(path.join(dir, "lists.json"), "utf8")) as {
    order: number;
    items: (RawExercise & { kind: string; exercises?: RawExercise[] })[];
  };
  const side = JSON.parse(readFileSync(path.join(dir, "lists.verify.json"), "utf8")) as {
    exercises: Record<string, { wrongAnswers?: { why: string; code: RawCode; failsAt: number; messageContains?: string }[] }>;
  };
  const text = (code: RawCode | undefined) => (Array.isArray(code) ? `${code.join("\n")}\n` : (code ?? ""));
  const exercises = new Map<string, RawExercise>();
  for (const item of unit.items) {
    if (item.kind === "project" || item.kind === "challenge") exercises.set(item.id, item);
    for (const exercise of item.exercises ?? []) exercises.set(`${item.id}/${exercise.id}`, exercise);
  }
  return (key: string, why: string) => {
    const exercise = exercises.get(key);
    const wrong = side.exercises[key]?.wrongAnswers?.filter((entry) => entry.why.includes(why)) ?? [];
    expect(exercise, key).toBeTruthy();
    expect(wrong, `${key}: one wrong answer about "${why}"`).toHaveLength(1);
    const context: ExplainContext = {
      unitOrder: unit.order,
      names: exercise?.names,
      solution: text(exercise?.solution),
      example: exercise?.example ? text(exercise.example.code) : undefined,
      explainer: exercise?.explainer,
      debugging: ((exercise?.checkpoints ?? []) as { text?: string }[]).some((checkpoint) => /\bmend\b/i.test(checkpoint.text ?? "")),
      foreign: foreignNames({
        hints: (exercise?.checkpoints ?? []).flatMap((checkpoint) => checkpoint.hints),
        solution: [text(exercise?.solution), text(exercise?.bonus?.solution)].join("\n"),
        starter: text(exercise?.starter),
        names: exercise?.names,
      }),
    };
    return { code: text(wrong[0].code), context, failsAt: wrong[0].failsAt, python: wrong[0].messageContains ?? "", order: unit.order };
  };
})();

describe("explainCourseError: Unit 4's slips (lists), from the unit's own wrong answers", () => {
  // [exercise, the wrong answer's `why`, Python 3.13's own words, kind, what the full hint says]
  const rows: [string, string, string, string, string][] = [
    // (1) `chalk_wall(2) = 47`: round brackets after a list's name, on the left of `=` (never the `==` row).
    ["many-values-one-name/fix-a-mark", "round brackets: assigning to a call", "cannot assign to function call", "list-needs-square-brackets",
      "Line 5 puts ( ) after `chalk_wall`. To change one item, use square brackets: `chalk_wall[2] = 47`"],
    // (2) a comma between two positions: the half that fits first.
    ["many-values-one-name/lists-inside-lists", "a comma between the positions", "list indices must be integers or slices, not tuple",
      "comma-in-brackets",
      "Inside [ ], a comma asks for two positions at once. Row then item takes two pairs of brackets: `roster[2][0]`. A run of items takes a colon: `[0:2]`."],
    ["reading-the-wall-closely/slice-the-wall", "a comma for the colon", "list indices must be integers or slices, not tuple",
      "comma-in-brackets", "Inside [ ], a comma asks for two positions at once. A run of items takes a colon: `chalk_wall[0:2]`."],
    // (3) one number joined to a list with `+`.
    ["many-values-one-name/new-chalk-mark", "a number joined with +", 'can only concatenate list (not "int") to list', "list-plus-item",
      "`+` joins two lists. To add one item, use `.append()`: `chalk_wall.append(33)`"],
    ["qc3-a/make-append-read", "+ a number, not a list", 'can only concatenate list (not "int") to list', "list-plus-item",
      "To add one item, use `.append()`: `marks.append(33)`"],
    // (4) square brackets after a tool that is called: a method, a builtin, a type.
    ["many-values-one-name/new-chalk-mark", "square brackets for append's round ones", "'builtin_function_or_method' object is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `chalk_wall.append(33)`"],
    ["reading-the-wall-closely/sorted-or-sort", "square brackets for sorted's round ones", "'builtin_function_or_method' object is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `sorted(chalk_wall)`"],
    ["more-list-tools/biggest-and-smallest", "square brackets after max", "'builtin_function_or_method' object is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `max(chalk_wall)`"],
    ["reading-the-wall-closely/range-of-marks", "square brackets for range's round ones", "type 'range' is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `range(1, 9)`"],
    ["zip/spell-colors", "square brackets for zip's round ones", "type 'zip' is not subscriptable", "call-needs-round-brackets",
      "Call it with round brackets: `zip(heroes, colors)`"],
    ["extra-reading-the-wall/how-many-times", "square brackets instead of round ones", "'builtin_function_or_method' object is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `chalk_wall.count(48)`"],
    ["more-list-tools/remove-and-in", "square brackets after remove", "'builtin_function_or_method' object is not subscriptable",
      "call-needs-round-brackets", "Call it with round brackets: `chalk_wall.remove(99)`"],
    // A position read from `None` (`.sort()` hands back nothing): the unit's "nothing came back", never "wrong kind".
    ["extra-reading-the-wall/broken-spell-3b", "the starter: .sort() hands back None", "'NoneType' object is not subscriptable",
      "read-from-none",
      "Line 2 reads a position from `None`: nothing came back. `.sort()` sorts the list itself and hands back nothing. `sorted(chalk_wall)` hands back a sorted copy."],
    ["extra-reading-the-wall/broken-spell-3b", "x = x.sort(): the wall itself becomes None", "'NoneType' object is not subscriptable",
      "read-from-none", "and `chalk_wall` holds `None`: nothing came back. `.sort()` on line 2 sorts the list itself"],
    // Positions past the end, in the unit's words: `len(wall)` is one past the last position (the class's slip).
    ["many-values-one-name/how-long", "len(list) used as an index (spec)", "list index out of range", "nothing-at-position",
      "Line 4 uses `len(chalk_wall)` as a position. `len(chalk_wall)` counts the items, so it is one past the last position. Use `len(chalk_wall) - 1`, or `[-1]`."],
    ["many-values-one-name/broken-spell-3a", "len(list) used as the position", "list index out of range", "nothing-at-position",
      "`len(chalk_wall)` counts the items, so it is one past the last position."],
    ["many-values-one-name/first-is-zero", "position 7 for the newest", "list index out of range", "nothing-at-position",
      "Line 5 asks for a position `chalk_wall` doesn't have. `chalk_wall` holds 7 items, so its positions are 0 to 6."],
    ["many-values-one-name/how-long", "a counted position [6]: the starter's second call", "list index out of range", "nothing-at-position",
      "Inside the recipe, `wall` is whatever list the call hands over, and it may be shorter."],
    ["many-values-one-name/lists-inside-lists", "the inner position too big", "list index out of range", "nothing-at-position",
      "In a list of lists, check both numbers: the row first, then the item in that row."],
    ["tuples/cabin-on-the-map", "read by position, counting from 1", "tuple index out of range", "nothing-at-position",
      "`cabin` holds 2 items, so its positions are 0 to 1."],
    // Two lists side by side with no comma (Mar'tu's pick copied as rows): a comma after each, never "a comma inside [ ]".
    ["oogrishs-training-log", "rows over several lines with no comma", "list indices must be integers or slices, not tuple",
      "missing-comma-in-list", 'ends a list with no comma, and the next line starts another, so Python reads the second one as a position in the first. Put a comma after each one: `["cane parry", 7],`'],
    // A whole pair + 2: the inner position, never `.append()`.
    ["oogrishs-training-log", "the inner position forgotten", 'can only concatenate list (not "int") to list', "row-not-item",
      "`log[0]` is a whole row of `log`: a list, not a number. Add the inner position of the number in it too: `log[0][1] = log[0][1] + 2`"],
    // The wall's row copied as it looks: commas inside square brackets, or one box each (never "a missing quote").
    ["many-values-one-name/how-would-you-store-it", "the row copied as shown", "invalid syntax", "missing-comma",
      "Numbers side by side need commas, inside square brackets: `hours = [48, 48, 47, 46, 44, 41, 37]`. Or give each number a box of its own."],
    // (5) "'list' object is not callable": read a list with square brackets (after the shadowed-name row).
    ["many-values-one-name/first-is-zero", "round brackets: the list called like a recipe", "'list' object is not callable",
      "list-needs-square-brackets", "`chalk_wall` is a list. Read a list with square brackets: `chalk_wall[0]`"],
    ["many-values-one-name/how-long", "round brackets: the list called like a recipe (inside", "'list' object is not callable",
      "list-needs-square-brackets", "`wall` is a list. Read a list with square brackets: `wall[len(wall) - 1]`"],
    ["reading-the-wall-closely/slice-the-wall", "square brackets vs parentheses: the list called", "'list' object is not callable",
      "list-needs-square-brackets", "Read a list with square brackets: `chalk_wall[0:2]`"],
    ["many-values-one-name/broken-spell-3a", "commas mended, the list still called with ()", "'list' object is not callable",
      "list-needs-square-brackets", "Read a list with square brackets: `chalk_wall[0]`"],
    // (6) `sorted` (and `max`) after a dot: it goes in front (Python's "Did you mean 'sort'" would sort the wall).
    ["reading-the-wall-closely/sorted-or-sort", "sorted used as a list method", "has no attribute 'sorted'. Did you mean: 'sort'?",
      "tool-after-dot", "`sorted` goes in front: `sorted(chalk_wall)`. It hands back a sorted copy."],
    ["more-list-tools/biggest-and-smallest", "max as a list tool (dot)", "has no attribute 'max'", "tool-after-dot",
      "`max` goes in front: `max(chalk_wall)`. It hands back the biggest item."],
    // (7) bare words inside [ ]: quotes, before the missing-comma rows.
    ["oogrishs-training-log", "a drill with no quotes, on one line", "invalid syntax. Perhaps you forgot a comma?", "unquoted-words",
      'If storm kick is text, put quotes around it: "storm kick".'],
    ["oogrishs-training-log", "one row of a list over several lines", "invalid syntax. Perhaps you forgot a comma?", "unquoted-words",
      'If shield wall is text, put quotes around it: "shield wall".'],
    ["the-basement-inventory", "a part with no quotes, one item of a list over several lines", "invalid syntax. Perhaps you forgot a comma?",
      "unquoted-words", 'If tuning fork is text, put quotes around it: "tuning fork".'],
    // (8) `.remove()` handed a value the list does not hold.
    ["more-list-tools/remove-and-in", "remove by position (3), not value", "list.remove(x): x not in list", "not-on-the-list",
      "`.remove()` on line 6 looks for a value, not a position. There is no 3 on the list. Ask first with `in`."],
    ["more-list-tools/remove-and-in", "99 in quotes", "list.remove(x): x not in list", "not-on-the-list",
      'There is no "99" on the list: in quotes it is text, and the list holds numbers. Ask first with `in`.'],
    // Numbers side by side in a list: a comma (never "or + to join text").
    ["many-values-one-name/make-the-wall", "no commas (spec)", "invalid syntax. Perhaps you forgot a comma?", "missing-comma-in-list",
      "Inside a list, a comma goes between each two items. Line 2 has numbers side by side with no comma between them: `chalk_wall = [48, 48, 47, 46, 44, 41, 37]`"],
    // The unit's other list crashes, in the unit's words.
    ["oogrishs-training-log", "append with two things, not one pair", "list.append() takes exactly one argument (2 given)",
      "wrong-number-of-values", 'put them in their own square brackets: `log.append(["roll and rise", 6])`'],
    ["extra-reading-the-wall/how-many-times", "nothing in the brackets", "list.count() takes exactly one argument (0 given)",
      "wrong-number-of-values", "`.count()` on line 2 needs one value inside its round brackets: the value to count."],
    ["more-list-tools/remove-and-in", "the sides swapped", "argument of type 'int' is not iterable", "wrong-kind-of-value",
      "so the value goes first and the list after it on line 3: `has_32 = 32 in chalk_wall`"],
    ["tuples/cabin-on-the-map", "three names for two items", "not enough values to unpack (expected 3, got 2)", "wrong-number-of-values",
      "Line 6 has 3 names on the left of `=`, but the right side holds 2 items. Use one name per item: 2 names."],
  ];

  it.each(rows)("%s, %s: Python says %s, the explainer names %s", (key, why, python, kind, hint) => {
    const { code, context, failsAt, python: proved } = unit4(key, why);
    expect(failsAt, "a crash wrong answer").toBe(0);
    const raw = tracebackOf(code);
    expect(raw).toContain(python);
    expect(raw, "the words the harness proved for this wrong answer").toContain(proved);
    const full = explainCourseError(raw, code, { ...context, explainer: "full" });
    expect(full.kind, code).toBe(kind);
    expect(full.hint).toContain(hint);
  });

  it("leads with the half that fits: row then item for a list of lists, a colon for a run of items", () => {
    const nested = unit4("many-values-one-name/lists-inside-lists", "a comma between the positions");
    const rows = explainRun(nested.code, [], nested.context).hint;
    expect(rows.indexOf("Row then item")).toBeLessThan(rows.indexOf("colon"));
    const flat = unit4("reading-the-wall-closely/slice-the-wall", "a comma for the colon");
    const run = explainRun(flat.code, [], flat.context).hint;
    expect(run.indexOf("colon")).toBeLessThan(run.indexOf("row then item"));
  });

  it("names the slip, never the fix, in a lean exercise (SOLO and Quick Check), for every new kind", () => {
    const lean: [string, string, string, string][] = [
      ["many-values-one-name/solo-3a", "round brackets: the list called like a recipe", "list-needs-square-brackets",
        "The slip is on line 3: round brackets where a list needs square ones."],
      ["more-list-tools/solo-3c", "the starter (square brackets after max)", "call-needs-round-brackets",
        "The slip is on line 2: square brackets where a call needs round ones."],
      ["more-list-tools/solo-3c", "a dot instead of a call", "tool-after-dot", "The slip is on line 2: a tool written after a dot."],
      ["qc3-a/make-append-read", "+ a number, not a list", "list-plus-item", "The slip is on line 4: one item joined to a list with `+`."],
      ["qc3-b/make-append-read", "square brackets for append's round ones", "call-needs-round-brackets",
        "The slip is on line 6: square brackets where a call needs round ones."],
      ["qc3-a/make-append-read", "missing commas", "missing-comma-in-list", "The slip is on line 2: a missing comma in a list."],
      ["qc3-a/mend-the-reads", "sorted with square brackets", "call-needs-round-brackets",
        "The slip is on line 11: square brackets where a call needs round ones."],
      ["reading-the-wall-closely/solo-3b", "seat B's bug", "read-from-none", "The slip is on line 3: a position read from `None`."],
    ];
    for (const [key, why, kind, hint] of lean) {
      const { code, context } = unit4(key, why);
      expect(context.explainer, `${key} is a lean exercise`).toBe("lean");
      const result = explainRun(code, [], context);
      expect(result.kind, `${key}: ${why}`).toBe(kind);
      expect(result.explainer).toBe("lean");
      expect(result.hint).toContain(hint);
      expect(result.title, `${key}: ${why}`).not.toContain("`");
      // The full version's fixed code (its last code span with a bracket) never shows in the lean one.
      const full = explainRun(code, [], { ...context, explainer: "full" });
      const fix = [...full.hint.matchAll(/`([^`]*[[(][^`]*)`/g)].at(-1)?.[1];
      expect(fix, `${key}: the full hint shows the fixed code`).toBeTruthy();
      expect(result.hint, `${key}: ${why}`).not.toContain(fix as string);
    }
    // The kinds with no lean wrong answer in the unit get a lean name too, and never their fix.
    for (const [key, why, kind] of [
      ["many-values-one-name/fix-a-mark", "round brackets: assigning to a call", "list-needs-square-brackets"],
      ["many-values-one-name/lists-inside-lists", "a comma between the positions", "comma-in-brackets"],
      ["more-list-tools/remove-and-in", "remove by position (3), not value", "not-on-the-list"],
    ] as const) {
      const { code, context } = unit4(key, why);
      const result = explainRun(code, [], { ...context, explainer: "lean" });
      expect(result.kind).toBe(kind);
      expect(result.hint).toContain(`: ${slipName(kind)}.`);
      expect(result.hint).not.toMatch(/chalk_wall\[2\] = 47|roster\[2\]\[0\]|Ask first/);
    }
  });

  it("opens only from Unit 4 on: Units 1 to 3 keep their older advice for the same code", () => {
    const cases: [string, string, string][] = [
      ["many-values-one-name/fix-a-mark", "round brackets: assigning to a call", "compare-with-double-equals"],
      ["many-values-one-name/new-chalk-mark", "a number joined with +", "wrong-kind-of-value"],
      ["many-values-one-name/new-chalk-mark", "square brackets for append's round ones", "wrong-kind-of-value"],
      ["many-values-one-name/lists-inside-lists", "a comma between the positions", "wrong-kind-of-value"],
      ["many-values-one-name/first-is-zero", "round brackets: the list called like a recipe", "not-a-function"],
      ["reading-the-wall-closely/sorted-or-sort", "sorted used as a list method", "attribute-spelling"],
      ["oogrishs-training-log", "a drill with no quotes, on one line", "missing-comma"],
      ["more-list-tools/remove-and-in", "remove by position (3), not value", "other"],
      ["many-values-one-name/make-the-wall", "no commas (spec)", "missing-comma"],
      ["extra-reading-the-wall/broken-spell-3b", "the starter: .sort() hands back None", "wrong-kind-of-value"],
      ["oogrishs-training-log", "rows over several lines with no comma", "wrong-kind-of-value"],
      ["oogrishs-training-log", "the inner position forgotten", "wrong-kind-of-value"],
      ["many-values-one-name/how-would-you-store-it", "the row copied as shown", "cant-read-line"],
    ];
    for (const [key, why, before] of cases) {
      const { code, context, order } = unit4(key, why);
      expect(order).toBe(4);
      expect(explainRun(code, [], { ...context, unitOrder: 3 }).kind, `${key}: ${why}, in Unit 3`).toBe(before);
      expect(explainRun(code, [], { ...context, unitOrder: undefined }).kind, `${key}: ${why}, with no unit`).toBe(before);
    }
  });

  it("keeps each new row in its place: never the == row, never over a recipe or a shadowed name", () => {
    const unit4Context: ExplainContext = { unitOrder: 4 };
    // A list's name with ( ) on the left of `=`: never "use two equals signs".
    const assigned = explainRun("chalk_wall = [48, 74]\nchalk_wall(1) = 47\n", [], unit4Context);
    expect(assigned.kind).toBe("list-needs-square-brackets");
    expect(assigned.hint).not.toContain("==");
    // Unit 3's recipe written like math keeps its row, and a real question keeps the == row.
    expect(explainRun("max_fuel_for(cells) = cells * 5\n", [], unit4Context).kind).toBe("recipe-like-math");
    expect(explainRun("roll = 5\nif roll = 5:\n    print(roll)\n", [], unit4Context).kind).toBe("compare-with-double-equals");
    // A box that is not a list, called with ( ) on the left: not the list row.
    expect(explainRun("mana = 20\nmana(1) = 5\n", [], unit4Context).kind).not.toBe("list-needs-square-brackets");
    // `list` used as a name keeps the shadowed-name row.
    expect(explainRun("list = [1, 2]\nprint(list(range(3)))\n", [], unit4Context).kind).toBe("name-taken");
    // A recipe read with [ ] is a call too.
    const recipe = explainRun("def newest_mark(wall):\n    return wall[-1]\n\nprint(newest_mark[[9, 8, 7]])\n", [], unit4Context);
    expect(recipe.kind).toBe("call-needs-round-brackets");
    expect(recipe.hint).toContain("`newest_mark([9, 8, 7])`");
    // A number read with [ ] is not a call slip.
    expect(explainRun("mana = 20\nprint(mana[0])\n", [], unit4Context).kind).toBe("wrong-kind-of-value");
    // `.pop[]` (a SyntaxError): round brackets for the call, never "a missing quote".
    const pop = explainRun("chalk_wall = [48, 47]\nnewest = chalk_wall.pop[]\n", [], unit4Context);
    expect(pop.kind).toBe("call-needs-round-brackets");
    expect(pop.hint).toContain("Call it with round brackets: `chalk_wall.pop()`");
    // A one-item list beside the rest is rebuilt as one pair, never `[["roll and rise"], 6]`.
    const pair = explainRun('log = []\nlog.append(["roll and rise"], 6)\n', [], unit4Context);
    expect(pair.hint).toContain('`log.append(["roll and rise", 6])`');
    // Two lists side by side on one line.
    const side = explainRun('log = [["cane parry", 7] ["shield wall", 5]]\n', [], unit4Context);
    expect(side.kind).toBe("missing-comma-in-list");
    expect(side.hint).toContain('Put a comma after each one: `["cane parry", 7],`');
    // A list whose count can't be read for sure (it grew): the plain rule, never a wrong count or Unit 1's "3 items".
    const grown = explainRun("wall = [1, 2]\nwall.append(3)\nprint(wall[3])\n", [], unit4Context);
    expect(grown.hint).toContain("the last position is one less than the number of items");
    expect(grown.hint).not.toMatch(/holds \d|3 items/);
    // Text keeps its older words.
    expect(explainRun('name = "Lucky"\nprint(name[9])\n', [], unit4Context).hint).toContain("the text doesn't have");
    // `None` from a list tool kept in a box, and from a recipe with no return.
    const appended = explainRun("w = [3]\nx = w.append(4)\nprint(x[0])\n", [], unit4Context);
    expect(appended.kind).toBe("read-from-none");
    expect(appended.hint).toContain("`.append()` on line 2 adds to the list itself and hands back nothing.");
    expect(explainRun("def f(w):\n    print(w)\n\nx = f([1])\nprint(x[0])\n", [], unit4Context).hint).toContain("a recipe with no `return`");
    // A row + a number in a flat list is not a row slip (a number + a number never crashes); `chalk_wall + 33` keeps .append().
    expect(explainRun("chalk_wall = [1, 2]\nchalk_wall = chalk_wall + 33\n", [], unit4Context).kind).toBe("list-plus-item");
    // Text joined to a list: the same row, in the words for text.
    expect(explainRun('names = ["Pell"]\nnames = names + "Moss"\n', [], unit4Context).hint).toContain(
      "joins a list and one piece of text with `+`",
    );
  });
});
