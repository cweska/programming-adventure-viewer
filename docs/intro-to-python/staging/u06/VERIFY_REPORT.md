UNIT 6 FINAL VERIFICATION (staging: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u06-staging)

Unit 6 passes: 0 harness errors, a clean export, and every content rule passes once Unit 5's glossary is in. I made one fix (a fenced hint line that would fail CI), described below.

FINAL HARNESS SUMMARY (harness.py u06, concept_map.json in place):
3 units, 29 exercises/projects/challenges, 45 checkpoints, 527 wrong answers, 20 quiz questions — 0 errors, 2 warnings
- Both warnings are broken starters on purpose: "starter is not valid Python yet".
  - broken-spell-5a: the loop body is not indented.
  - solo-5c: a colon inside the one-line loop.

STEP 1 (concept_map.json moved aside, then put back; it is in place now):
- 29 errors, every one "node:Dict" (u05a in the plan). No other tokens failed.
- So the tokens to cross-check when Unit 5 ships: node:Dict only.
- I also checked against the real Unit 5 files. I copied u01–u04 and u06 from this staging dir and u05a/b/c from scratchpad/intro-python/u05-staging into /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u06verify/combined, with no concept map. Result: 0 errors, the same 2 warnings.
- With those real files, node:Dict, op:NotIn and attr:get come from u05a.
- Unit 6 introduces: For (predict-the-loop), While (countdown), Break (stop-at-the-first), Continue (skip-the-empty), ListComp (one-line-loops), IfExp (choose-in-one-line), and items/keys/values (the article).

PYODIDE CROSS-CHECK (the site's real runtime):
- I ran every solution, partial and wrong answer (569 runs) through public/workers/python-worker.js in Node.
- 0 mismatches against the harness; the slowest run took 255 ms.
- This proves the checks' sys.settrace line guard works in Pyodide. Unit 6 is the first unit to use sys.settrace.

INFINITE LOOPS:
- Every while-loop wrong answer prints inside its loop. Each one stops within milliseconds with "TooMuchOutput: This program printed more than 200,000 characters, so it was stopped." (fails_at 0). The site explains it as "Printing forever?".
- None of them waits for the 6 s harness timeout or the 5 s site timeout.
- Reruns inside checks are capped at 20,000 characters and 20,000 lines, and say "With other values, your loop never stopped".
- I also tried two silent endless loops (no print inside the loop). Both failed in under 70 ms with their own step messages.
- 5B-02 explains the limit honestly: 200,000 characters of printing or 5 seconds. It does not invent a "step limit".

FIX MADE (u06a_loops_for_while.py, bars-for-everyone, CP2 "the-empty-blocks", hints[1]):
- Problem: the hint had a 60-character line inside a fence. That fails content.test.ts, which allows 36 characters per fenced line.
- The designer notes say the teacher's ruling dictated this one-line jar return. I kept the line word for word, but as an inline code span, which wraps on a phone: "With other names: `return "#" * jar["left"] + "." * (jar["size"] - jar["left"])`. The round brackets do the taking away first."
- I updated the matching designer notes (the module docstring and the exercise notes).
- I re-ran the harness, the export and the Pyodide runs after the change.
- Please confirm this change with the teacher.

STEP 2 (export):
- Command: export_prototypes.py --src u06-staging --out u06-staging-export. It exports with no errors, so there are no unknown fields.
- I checked the content rules on that export plus the sample unit, with a scratch copy of the checks in content.test.ts: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u06verify/check.ts. These pass:
  - unitSchema (zod) parses
  - ids are unique, and unit orders are unique
  - checkpoint text has no leading numbers
  - backticks are balanced and fences are closed
  - no **bold**, no *stars* around code, no [[link]] inside code
  - fenced lines are 36 characters or fewer
  - the .verify.json sidecar matches
  - no glossary term or alias repeats
- The only failure: [[dictionary]] and [[key]] in the article looping-over-a-dictionary body do not resolve yet. Unit 5's u05a GLOSSARY in u05-staging defines both terms. With the real Unit 5 files in the export, the result is "OK: no content-rule problems".
- None of Unit 6's 13 new glossary terms or aliases repeats a term from Units 1–5 or the sample.
- git status in the repo is clean.

STEP 3 (consistency):
- The UNIT dict is identical in u06a, u06b and u06c: id loops, order 6, title Loops, subtitle "Every Member of the Party", published True, campaign_links ["friends-in-low-places"].
- Item ids are unique.
- Every exercise campaign_link points at a real beat id in content/modules/friends-in-low-places/module.json: spell-book, chalk-wall, mana-bars, hold-the-barrier, ley-clock, thirty-two-hours.
- Mar'tu's voice and the callbacks are there:
  - the martu_intro uses the spec's framing
  - "The decay is accelerating. Now you have seen it yourself."
  - "If this is right, we run out of nights."
  - `for member in party.members:`
  - break is presented as a bridge to Unit 7's early return
- No reading-level or length warnings.
- No student names or ids appear.
- No engine=True and no randomness.
- Solo items and every Quick Check exercise use explainer="lean". The Quick Check messages name the slip and the evidence, never the fix.
- Both Quick Check forms set questions_to_pass=3, as Unit 2 does.
- Every slip on the class's list has at least one wrong_answers entry.
- The real data is used: party mana 9/18, 10/20, 12/24, 13/26 (total 88), and the wall 48, 48, 47, 46, 44, 41, 37 (shrinks 0 1 1 2 3 4).

ITEM LIST (kind | id | title | minutes | optional | exercises or questions)
u06a:
- quiz | 5a-remembers | Mar'tu remembers… | 2 | yes | 2 questions
- lesson | for-each-yes | For Each, Yes? | 38 | no | 9 exercises: predict-the-loop, each-mark, each-member, running-total, how-much-each-gap-shrank, loop-with-a-check, bars-for-everyone (3 CPs), broken-spell-5a (4 CPs), solo-5a
- quiz | 5b-remembers | Mar'tu remembers… | 2 | yes | 2 questions
- lesson | while-the-clock-ticks | While the Clock Ticks | 15 | no | 5 exercises: countdown (2 CPs), the-loop-that-never-ends, stop-at-the-first, forecast, solo-5b
- quiz | loops-quiz | Loops Quiz | 8 | no | 8 questions
u06b:
- project | the-velocite-watch | The Velocite Watch | 20 | no | 1 (5 task checkpoints)
- challenge | gearshifts-forecast | Gearshift's Forecast | 10 | yes | 1 (2 CPs)
- lesson | extra-loops-that-end | Extra practice: Loops That End | 3 | yes | 1 (broken-spell-5b, 2 CPs)
- lesson | loops-in-one-line | Loops in One Line | 20 | yes | 5 exercises: skip-the-empty, loops-in-loops, one-line-loops (2 CPs), choose-in-one-line, solo-5c
- article | looping-over-a-dictionary | Looping Over a Dictionary | 10 | yes | 1 try-it (spell-costs, 2 CPs)
u06c:
- testout | qc5-a | Quick Check 6 · Form A | 14 | yes | 3 exercises, questions_to_pass=3
- quiz | qc5-a-questions | Quick Check 6 · Form A questions | 4 | yes | 4 questions
- testout | qc5-b | Quick Check 6 · Form B | 14 | yes | 3 exercises, questions_to_pass=3
- quiz | qc5-b-questions | Quick Check 6 · Form B questions | 4 | yes | 4 questions
- cheatsheet | chalk-notes | Mar'tu's Chalk Notes: Loops | — | yes | 20 entries

MINUTES:
- The curriculum core (5A + 5B + Quiz) is 37 + 14 + 8 = 59. As built it is 38 + 15 + 8 = 61.
  - 5A is +1: the teacher's ruling added a predict and a Run in bars-for-everyone.
  - 5B is +1.
- With the project, the required total is 81 (the curriculum says 79).
- Everything, optional items included, is 164 minutes.

REMAINING CONCERNS:
1. [[dictionary]] and [[key]] (article body) and node:Dict depend on Unit 5 shipping with the u05a GLOSSARY and concepts as they are now in u05-staging. If Unit 5 renames those terms, CI breaks.
2. Please confirm the inline-code change for the teacher-dictated jar hint above.
3. Long lines in editor code (130 student-visible lines over 36 characters) follow the same practice as Units 2 and 4, and CI does not check them. Two are on purpose: the 49-character 5A-03 Example (teacher ruling) and a 41-character predict choice in predict-the-loop.
4. broken-spell-5a has no partials. They are impossible, because bug 2 crashes before any check runs. Wrong answers at fails_at 3 and 4 cover those stages. forecast (change one number) and solo-5c have no assemble, which matches the earlier units.
5. The rerun rosters in u06b use "Zelda" and "Kratos". These are third-party game characters, quoted from the worksheet. They could appear in a check message such as "Zelda, with 7 mana, did not print". Unit 1 already uses "Zelda", so this is house style, but it is a small originality and IP nit.
6. There are additions beyond the curriculum table: the u06c file and the optional Gearshift's Forecast challenge (10 min). The Quick Check ids are qc5-a/qc5-b with the title "Quick Check 6", the same pattern as Unit 4's qc3-a "Quick Check 4".

FILES:
- Edited: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u06-staging/u06a_loops_for_while.py
- Export: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u06-staging-export
- Check with the real Unit 5: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u06verify/combined-export
- Verifier scripts: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u06verify/check.ts and /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u06verify/pyrun.mjs