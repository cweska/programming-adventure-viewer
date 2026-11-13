import { describe, expect, it } from "vitest";
import type { RunResult } from "../languages/types";
import { checkMessage, flattenChecks, gradeCheckpoints, NOT_CHECKED_MESSAGE, NOT_DONE_MESSAGE } from "./grading";
import { runCourseChecks } from "./run-course";
import { checkpointSchema, type Checkpoint } from "./schema";

function checkpoint(id: string, checks: [string, string][]): Checkpoint {
  return checkpointSchema.parse({
    id,
    text: `Do ${id}.`,
    hints: ["A nudge.", "The answer."],
    checks: checks.map(([name, code]) => ({ name, code })),
  });
}

function result(partial: Partial<RunResult>): RunResult {
  return { ok: true, stdout: "", stderr: "", traceback: "", checks: [], stageEvents: [], ...partial };
}

const checkpoints = [
  checkpoint("make-name", [["exists", "assert 'name' in globals(), 'Make a variable called name.'"]]),
  checkpoint("print-name", [
    ["prints", "assert _lines() == [name], 'Print name.'"],
    ["uses-variable", "assert _uses('node:Name'), 'Use the variable.'"],
  ]),
  checkpoint("greet", [["greets", "assert 'Hi' in _captured_stdout, 'Say Hi too.'"]]),
];

describe("flattenChecks", () => {
  it("names every check checkpointId::checkName, in order", () => {
    expect(flattenChecks(checkpoints).map((check) => check.name)).toEqual([
      "make-name::exists",
      "print-name::prints",
      "print-name::uses-variable",
      "greet::greets",
    ]);
    expect(flattenChecks(checkpoints)[0]?.code).toBe("assert 'name' in globals(), 'Make a variable called name.'");
    expect(flattenChecks([])).toEqual([]);
  });
});

describe("gradeCheckpoints", () => {
  it("regroups passing and failing checks by checkpoint", () => {
    const grade = gradeCheckpoints(
      checkpoints,
      result({
        checks: [
          { name: "make-name::exists", passed: true, message: "" },
          { name: "print-name::prints", passed: true, message: "" },
          { name: "print-name::uses-variable", passed: false, message: "AssertionError: Use the variable." },
          { name: "greet::greets", passed: false, message: "AssertionError: Say Hi too." },
        ],
      }),
    );
    expect(grade).toEqual({
      crashed: false,
      checkpoints: [
        { id: "make-name", passed: true, message: "" },
        { id: "print-name", passed: false, message: "Use the variable." },
        { id: "greet", passed: false, message: "Say Hi too." },
      ],
      firstFailing: 1,
      allPassed: false,
    });
  });

  it("uses the FIRST failing check's message in a checkpoint", () => {
    const grade = gradeCheckpoints(
      checkpoints,
      result({
        checks: [
          { name: "make-name::exists", passed: true, message: "" },
          { name: "print-name::prints", passed: false, message: "AssertionError: Print name." },
          { name: "print-name::uses-variable", passed: false, message: "AssertionError: Use the variable." },
          { name: "greet::greets", passed: true, message: "" },
        ],
      }),
    );
    expect(grade.checkpoints[1]).toEqual({ id: "print-name", passed: false, message: "Print name." });
    expect(grade.checkpoints[2]?.passed).toBe(true);
    expect(grade.firstFailing).toBe(1);
  });

  it("reports allPassed when every checkpoint passes", () => {
    const grade = gradeCheckpoints(
      checkpoints,
      result({ checks: flattenChecks(checkpoints).map((check) => ({ name: check.name, passed: true, message: "" })) }),
    );
    expect(grade.allPassed).toBe(true);
    expect(grade.firstFailing).toBeNull();
    expect(grade.crashed).toBe(false);
  });

  it("fails every checkpoint with the explained error when the code crashed", () => {
    const traceback = [
      "Traceback (most recent call last):",
      '  File "main.py", line 1, in <module>',
      "    name = fireball",
      "NameError: name 'fireball' is not defined",
    ].join("\n");
    const grade = gradeCheckpoints(checkpoints, result({ ok: false, traceback }), "name = fireball\n");
    expect(grade.crashed).toBe(true);
    expect(grade.allPassed).toBe(false);
    expect(grade.firstFailing).toBe(0);
    const message =
      'Python doesn\'t know the name fireball. Did you mean to put quotes around it? Text needs quotes: "fireball"';
    expect(grade.checkpoints).toEqual([
      { id: "make-name", passed: false, message },
      { id: "print-name", passed: false, message },
      { id: "greet", passed: false, message },
    ]);
  });

  it("counts a timeout as a crash, even with no traceback", () => {
    const grade = gradeCheckpoints(checkpoints, result({ ok: false, timedOut: true }), "while True:\n    pass\n");
    expect(grade.crashed).toBe(true);
    expect(grade.checkpoints[0]?.message).toContain("ran for more than 5 seconds");
    expect(grade.checkpoints[0]?.message).toContain("while loop");
  });

  it("marks a missing check result as not checked instead of passing it", () => {
    const grade = gradeCheckpoints(checkpoints, result({ checks: [{ name: "make-name::exists", passed: true, message: "" }] }));
    expect(grade.checkpoints[0]?.passed).toBe(true);
    expect(grade.checkpoints[1]).toEqual({ id: "print-name", passed: false, message: NOT_CHECKED_MESSAGE });
  });

  it("matches results by name when the order is off", () => {
    const grade = gradeCheckpoints(
      checkpoints,
      result({
        checks: [
          { name: "greet::greets", passed: true, message: "" },
          { name: "print-name::uses-variable", passed: true, message: "" },
          { name: "print-name::prints", passed: true, message: "" },
          { name: "make-name::exists", passed: false, message: "AssertionError: Make a variable called name." },
        ],
      }),
    );
    expect(grade.checkpoints.map((grade) => grade.passed)).toEqual([false, true, true]);
    expect(grade.checkpoints[0]?.message).toBe("Make a variable called name.");
  });

  it("handles an exercise with no checkpoints", () => {
    expect(gradeCheckpoints([], result({}))).toEqual({ crashed: false, checkpoints: [], firstFailing: null, allPassed: false });
    expect(gradeCheckpoints([], result({ ok: false, traceback: "x" })).firstFailing).toBeNull();
  });
});

describe("checkMessage", () => {
  it("strips the AssertionError prefix", () => {
    expect(checkMessage("AssertionError: Print `Hello, Tor`.")).toBe("Print `Hello, Tor`.");
    expect(checkMessage("AssertionError: line one\nline two")).toBe("line one\nline two");
  });

  it("gives a kind default for a bare assert", () => {
    expect(checkMessage("AssertionError")).toBe(NOT_DONE_MESSAGE);
    expect(checkMessage("AssertionError: ")).toBe(NOT_DONE_MESSAGE);
    expect(checkMessage("")).toBe(NOT_DONE_MESSAGE);
  });

  it("explains a name the check could not find", () => {
    expect(checkMessage("NameError: name 'chalk_wall' is not defined")).toBe(
      "Can't find `chalk_wall`. Make sure your code makes `chalk_wall`, spelled exactly like that.",
    );
  });

  it("wraps other errors raised while checking", () => {
    expect(checkMessage('TypeError: can only concatenate str (not "int") to str')).toBe(
      'Checking this step hit a problem: TypeError: can only concatenate str (not "int") to str. Look at the values your code makes.',
    );
    expect(checkMessage("Plain words.")).toBe("Plain words.");
  });
});

describe("grading a real course run", () => {
  it("flattens, runs and regroups a whole exercise", () => {
    const exercise = [
      checkpoint("make-hero", [["value", "assert hero == 'Lucky', 'Set hero to \"Lucky\".'"]]),
      checkpoint("greet", [
        ["prints", "assert _lines() == ['Hi Lucky'], 'Print Hi Lucky.'"],
        ["joins", "assert _uses('op:Add'), 'Join the words with +.'"],
      ]),
    ];
    const starter = 'hero = "Lucky"\nprint("Hi Lucky")\n';
    const starterGrade = gradeCheckpoints(exercise, runCourseChecks(starter, flattenChecks(exercise)), starter);
    expect(starterGrade.checkpoints).toEqual([
      { id: "make-hero", passed: true, message: "" },
      { id: "greet", passed: false, message: "Join the words with +." },
    ]);

    const solution = 'hero = "Lucky"\nprint("Hi " + hero)\n';
    expect(gradeCheckpoints(exercise, runCourseChecks(solution, flattenChecks(exercise)), solution).allPassed).toBe(true);

    const crash = 'hero = "Lucky\n';
    const crashGrade = gradeCheckpoints(exercise, runCourseChecks(crash, flattenChecks(exercise)), crash);
    expect(crashGrade.crashed).toBe(true);
    expect(crashGrade.checkpoints[0]?.message).toContain("missing its closing quote");

    const missing = 'print("Hi Lucky")\n';
    const missingGrade = gradeCheckpoints(exercise, runCourseChecks(missing, flattenChecks(exercise)), missing);
    expect(missingGrade.checkpoints[0]?.message).toBe("Can't find `hero`. Make sure your code makes `hero`, spelled exactly like that.");
  });
});

describe("grading: the slips a check alone would hide", () => {
  const makeCharacter = [
    checkpoint("make-character", [["value", "assert character == 'Zelda', 'Store the text Zelda in character.'"]]),
    checkpoint("show-character", [["prints", "assert 'Zelda' in _lines(), 'Print character.'"]]),
  ];

  function grade(code: string, context?: Parameters<typeof gradeCheckpoints>[3]) {
    return gradeCheckpoints(makeCharacter, runCourseChecks(code, flattenChecks(makeCharacter)), code, context);
  }

  it("names a lone quoted string (no error at all) and puts the missing name in front of it", () => {
    const result = grade('"Zelda"\n');
    expect(result.crashed).toBe(false);
    expect(result.checkpoints[0]?.message).toBe(
      'Line 1 is a value on its own: "Zelda". Python reads it, then forgets it, because no variable keeps it. To keep it, put character = in front of it: character = "Zelda"',
    );
  });

  it("names a value that was never printed when the run printed nothing", () => {
    const show = [checkpoint("show", [["prints", "assert 'Hello' in _lines(), 'Print Hello.'"]])];
    const code = '"Hello"\n';
    const result = gradeCheckpoints(show, runCourseChecks(code, flattenChecks(show)), code);
    expect(result.checkpoints[0]?.message).toContain('To show it, put it inside print( ): print("Hello")');
  });

  it("keeps the check's own message when the slip is not what failed", () => {
    // Something printed, and the check found its variable: the stray line is not this step's problem.
    const code = 'character = "Link"\nprint(character)\n"Zelda"\n';
    expect(grade(code).checkpoints[0]?.message).toBe("Store the text Zelda in character.");
  });

  it("names a dash that kept nothing, when the check is about that name", () => {
    const mana = [checkpoint("mana", [["value", "assert mana == 20, 'Store the number 20 in mana.'"]])];
    const code = "mana = 3\nmana - 20\n";
    const result = gradeCheckpoints(mana, runCourseChecks(code, flattenChecks(mana)), code);
    expect(result.checkpoints[0]?.message).toBe("Line 2 uses a dash - where = belongs, so nothing is kept. To store the value, write: mana = 20");
  });

  it("says when the code made a name with other capital letters, or the example's name", () => {
    expect(grade('Character = "Zelda"\nprint(Character)\n').checkpoints[0]?.message).toBe(
      "Can't find `character`. Your code made `Character`, but capital letters matter: use `character`.",
    );
    const example = 'hero = "Link"\nprint(hero)\n';
    expect(grade('hero = "Zelda"\nprint(hero)\n', { example, names: ["character"] }).checkpoints[0]?.message).toBe(
      "Can't find `character`. Your code made `hero`, the name from the example. This task uses `character`.",
    );
  });

  it("passes the context on to the crash explanation", () => {
    const example = 'traveler = input("Name? ")\nprint("Hello, " + traveler)\n';
    const code = 'character = "Zelda"\nprint(traveler)\n';
    const result = grade(code, { example, names: ["character"] });
    expect(result.crashed).toBe(true);
    expect(result.checkpoints[0]?.message).toBe("traveler is the name from the example. This task uses character, so write character here.");
  });
});
