# Intro to Python: build plan through Tuesday Nov 17 (teacher: "create two units at the same time until Tuesday")

Scratchpad root: /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python
Workflow scripts: /root/.claude/projects/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/workflows/scripts/
Journals: .../subagents/workflows/<run>/journal.jsonl. Relaunch a dead run with Workflow({scriptPath, resumeFromRunId[, args]}).

## Rhythm
- Two CONTENT workflows at a time (staging dirs `uNN-staging`, never the repo), plus at most ONE SHIP workflow (the repo) at a time.
- Ship order is unit order. A unit ships only after the one before it.
- Content workflow script: intro-python-unit-content-wf_d1be2207-167.js, with args (see the Unit 3/4 launches): unitNum, unitId, order,
  title, subtitle, heading "## Unit N ·", prefix "uNN", stage "uNN-staging", coreMinutes, parts[{prefix, file, scope}], slips,
  earlierNote, extra, verifyNote. Before launching: mkdir uNN-staging; cp the repo's docs/intro-to-python/prototypes/u0*.py (shipped units)
  + concept_map.json into it; for units whose predecessor is still in staging, the planned concept map stands in (note it in earlierNote).
- Ship workflow pattern: intro-python-ship-unit2-*.js (build site needs + publish + generic parity e2e → browser review → fix). For unit N:
  copy staging uNN*.py into docs/intro-to-python/prototypes/ (only after the previous unit shipped), apply the content workflow's
  teacher site_requests, publish, full tests, review, fix. Then I commit (no [skip ci]), push, and open/extend a PR to main.
- PRs: one open PR at a time on branch claude/tender-archimedes-cdwhjl. If it is still open when the next unit ships, update its
  title/body to cover both. After a merge: `git merge origin/main` into the branch (non-destructive). The force-push restart was approved
  once for the worksheet cleanup; don't repeat it without asking.
- Autosave is OFF (mode "stop") so WIP never lands on a PR. Staging dirs live in the scratchpad, which has survived container restarts.
- Student-group files are PRIVATE: scratchpad/intro-python/private/ — never in the repo.
- Usage: check list_events kinds=["rate_limit_event"]. When the 5-hour window is near 100%, keep a send_later for its resetsAt + 5 min.
  The weekly window was reset by the teacher on Nov 13 ~9:54am MST; it resets again Tue Nov 17 3:00pm MST.

## Units (curriculum §3, docs/intro-to-python/design/curriculum.md)
| # | id | title / subtitle | parts | status |
|---|---|---|---|---|
| 1 | hello-world | Hello World / Words by the Fire | u01a-d | LIVE (#12, #13) |
| 2 | control-flow | Control Flow / The Ley Clock Decides | u02a-c | LIVE (PR #15 merged 23:49 UTC Nov 14 as 50e8d09) |
| 3 | first-recipes | Functions I / First Recipes | u03a-b | LIVE (PR #15 merged 23:49 UTC Nov 14 as 50e8d09) |
| 4 | lists | Lists / The Chalk Wall | u04a-c | LIVE (PR #15 merged 23:49 UTC Nov 14 as 50e8d09) |
| 5 | dictionaries | Dictionaries / Stat Sheets and Spell Books | u05a-c | LIVE (PR #15 merged 23:49 UTC Nov 14 as 50e8d09) |
| 6 | loops | Loops / Every Member of the Party | u06a-c | SHIP running 20:45 UTC (wf_a09314c0-eda, task w2nz6dega) in WORKTREE /home/user/pav-u6 (branch u6-ship-local from d39e1f0); args run-args/u06-ship.json |
| 7 | spell-recipes | Functions II / Spells You Can Hand Over | u07a-c | CONTENT DONE 09:20 UTC Nov 14 (0 errors, 0 warnings; u07-staging TEACHER_RESULT.json 7 site_requests; must not publish before Unit 6) |
| 8 | code-challenges | Code Challenges (optional) / Trials of the Yard | u08a-c | CONTENT DONE 13:50 UTC Nov 14 (0 errors; u08-staging TEACHER_RESULT.json 8 site_requests incl. challenge-crash checks + trials unlock gates) |
| 9 | strings | Strings / Runes and Ribbons | u09a-c | CONTENT DONE ~18:45 UTC Nov 14 (u09-staging TEACHER_RESULT.json 2 site_requests; VERIFY_REPORT.md) |
| 10 | readiness-check | Campaign Readiness Check / Before We Continue | u10a-c | CONTENT DONE ~20:00 UTC Nov 14 (u10-staging TEACHER_RESULT.json 10 site_requests — the readiness flow/testout wiring is a MUST; VERIFY_REPORT.md) |

After the units: teacher page ("Needs you now" / "Ready for more"), the per-skill mastery map, the step-through tracer.

## NEXT ON THE 21:50 UTC RESET (written 18:47 UTC, 5-hour window at 98%)
1. Check usage. Read notifications (PR #14 CI). Fix CI if red.
2. Unit 2 ship workflow wf_3a249563-553 (review → fix). If its task died: Workflow({scriptPath: <workflows/scripts/intro-python-ship-unit2-*.js>, resumeFromRunId: 'wf_3a249563-553'}).
   When done: verify (export --check, typecheck, lint, npm test), commit, push onto PR #14 if still open, else a follow-up PR from main.
3. Unit 4 content wf_7f5d6f25-c23: resume the same way if it died (script intro-python-unit-content-wf_d1be2207-167.js + its args from the journal/launch).
4. Launch Unit 5 content (Dictionaries, u05a-c) into u05-staging: copy repo u01*/u02* + u03-staging u03* + concept_map.json; earlierNote: "Unit 3 is verified in staging; Unit 4 (Lists) still in staging — use the planned concept map for list tokens."
5. Unit 3 ship: after Unit 2's ship workflow finishes. Copy u03-staging/u03*.py into the repo, apply TEACHER_RESULT.json site_requests, publish, test, review, fix.

## Status 22:02 UTC Nov 13
- 5-hour window reset to 0 at 21:50 UTC; next reset 02:50 UTC Nov 14 (resetsAt 1794624600). Weekly 13%.
- Running: Unit 2 fixer (ship), Unit 4 revise/verify (content), Unit 5 content.
- Next: when the Unit 2 fixer finishes → verify, commit, push, open follow-up PR "Unit 2 walkthrough fixes" → then Unit 3 ship.
  When Unit 4 content finishes → launch Unit 6 content (Loops, u06a-b) into u06-staging.

## Status 23:12 UTC Nov 13 (5-hour window 53% at 23:02; resets 02:50 UTC; weekly 20%)
- Generic ship script: scratchpad/intro-python/ship-unit.js (args: unitNum, unitId, title, subtitle, prefix, stage, repo, liveNote,
  siteNote, reviewFocus). Unit 3 runs it in the worktree so WIP never lands on PR #15 (the stop hook only checks the main checkout).
- When the Unit 3 ship finishes: verify in /home/user/pav-u3 (export --check, typecheck, lint, npm test), commit there on u3-ship-local,
  then in the main checkout: `git merge u3-ship-local` (after `git merge origin/main` if #15 merged), push, and open a PR (or extend #15 if
  still open — update its title/body). Then remove the worktree, and ship Unit 4 the same way (new worktree from the branch HEAD).
- When Unit 5 content finishes: launch Unit 7 content (Functions II, u07a-c) — staging gets u03/u04/u05 from staging + repo u01/u02.

## RESUME RECIPES (5-hour window 70% at 23:20 UTC, ~1%/min → full ≈ 23:50 UTC; resets 02:50 UTC)
- Unit 3 ship: Workflow({scriptPath: scratchpad/intro-python/ship-unit.js, resumeFromRunId: 'wf_3e0413b8-2d1', args: <run-args/u03-ship.json>})
- Unit 5 content: Workflow({scriptPath: <workflows/scripts/intro-python-unit-content-wf_d1be2207-167.js>, resumeFromRunId: 'wf_690cdcbc-d4e',
  args: <run-args/u05-content.json>}
- Unit 6 content: same script, resumeFromRunId 'wf_e365a2be-b7d', args: <run-args/u06-content.json>.
  (A resumed run with DIFFERENT args re-runs everything; if the exact args are lost, read them from the first agent prompts in the run's
  agent-*.jsonl files.)
- PR #15 is green and mergeable (CI success 23:13 UTC); waiting on the teacher.

## Status 02:58 UTC Nov 14 (5-hour window 0% after the 02:50 reset; next reset 07:50 UTC; weekly 27%)
- Resumed (same run IDs, so the RESUME RECIPES above still apply): Unit 3 ship wf_3e0413b8-2d1 (task wv2hlffvo; its build had been cut
  off part-way — the script now tells the build to review existing edits), Unit 5 content wf_690cdcbc-d4e (task wpr808b50; revise+verify
  left), Unit 6 content wf_e365a2be-b7d (task wgetzmt2e; harden u06a/b, author u06c, reps, teacher, revise, verify left).
- PR #15 still open, CI green; the teacher hasn't merged. Safety-net check-ins for #15 stopped (first check-in found nothing); still
  subscribed, so a merge or review wakes me.
- /home/user/pav-u3/node_modules is a symlink and shows as untracked — never commit it (git add specific paths there).
- Check-in at 07:55 UTC (trig via send_later).

## Status 03:52 UTC Nov 14 (5-hour window 43% at 03:49, ~0.8%/min → full ≈ 05:00 UTC; resets 07:50 UTC; weekly 32%)
- Running: Unit 3 ship (wv2hlffvo, run wf_3e0413b8-2d1), Unit 6 content (wgetzmt2e, run wf_e365a2be-b7d), Unit 7 content (w49ypual7,
  run wf_60a7d1eb-415, args run-args/u07-content.json). Unit 5 content is DONE.
- Ship queue after Unit 3: Unit 4 (3 site_requests incl. course-wide choice shuffle), then Unit 5 (18 site_requests).
- Next content after Unit 6 finishes: Unit 8 Code Challenges (u08a-c) — staging gets u03-u05 (+u07 if done) from staging.

## Status 04:52 UTC Nov 14 (5-hour window 88%, full within minutes; resets 07:50 UTC; weekly 38%)
- Unit 6 content DONE. Unit 8 content NOT launched (it would be cut off at once): launch it at the 07:55 check-in with
  Workflow({scriptPath: <content script>, args: <run-args/u08-content.json>}).
- Still running (will be cut off; resume with the recipes above): Unit 3 ship wf_3e0413b8-2d1, Unit 7 content wf_60a7d1eb-415
  (args run-args/u07-content.json).

## Status 07:53 UTC Nov 14 (teacher said "Restart"; 5-hour window 0% after the 07:50 reset; next reset 12:50 UTC; weekly 40%)
- Unit 3 ship: build + review DONE (build green: 824 unit tests, 121 e2e). Fixer resumed (task wbue2as1x, run wf_3e0413b8-2d1).
  Review found majors incl. the ledger's 'More structure' rung giving away every row, and the trace paste guard.
- Unit 7 content resumed (task woeqe3cxs, run wf_60a7d1eb-415): harden u07c, reps, teacher, revise, verify left.
- Unit 8 content launched (task wc7gn6nr5, run wf_612af33e-842).
- Old 07:55 check-in deleted; new one at 12:55 UTC.
- Resume recipe for Unit 8: same content script, resumeFromRunId 'wf_612af33e-842', args run-args/u08-content.json.

## Status 08:19 UTC Nov 14 (5-hour window 21% at 08:17, ~0.8%/min; resets 12:50 UTC; weekly 43%)
- PR #15 now = Unit 2 fixes + Unit 3 (CI will run on 147937e). Still subscribed.
- Running: Unit 4 ship (wn539ghs4), Unit 7 content (woeqe3cxs), Unit 8 content (wc7gn6nr5).
- When Unit 4 ship finishes: verify in pav-u4, commit there (git add -A -- . ':!node_modules'), then in the main checkout: if #15 is
  still open → git merge --ff-only u4-ship-local, push, retitle #15 (Units 2 fixes + 3 + 4); if #15 merged → git merge origin/main first,
  then merge u4-ship-local, push, open a new PR. Then Unit 5 ship (u05-staging, 18 site_requests).
- When Unit 7 content finishes → Unit 9 Strings content (u09a-b). When Unit 8 finishes → Unit 10 Readiness Check content (u10a-c).

## Status 09:25 UTC Nov 14 (5-hour window 77% at 09:22, ~0.9%/min → full ≈ 09:47; resets 12:50 UTC; weekly 50%)
- Unit 7 content DONE. PR #15 (Unit 2 fixes + Unit 3) CI green on 147937e, waiting on the teacher.
- Unit 9 content NOT launched yet (would be cut off): launch at 12:55 with the content script + run-args/u09-content.json.
- Still running (will be cut off; resume): Unit 4 ship wf_53aa04ee-e87 (args run-args/u04-ship.json), Unit 8 content wf_612af33e-842
  (args run-args/u08-content.json).

## Status ~09:50 UTC Nov 14 (5-hour window full; resets 12:50 UTC)
- Unit 4 ship: build + review DONE (build: 962 unit tests, 151 e2e green; course-wide choice shuffle in). FIX died at the limit →
  resume wf_53aa04ee-e87 with run-args/u04-ship.json.
- Unit 8 content: authors/harden/reps/teacher DONE; revise + verify died → resume wf_612af33e-842 with run-args/u08-content.json.
  Teacher site_requests include challenge-crash messages + trials unlock gates (site work for the Unit 8 ship).
- Then launch Unit 9 content (run-args/u09-content.json). Check-in trig_01AtPtsdXJ83ptR7RNr9t9GN at 12:55 UTC covers all of this.

## Status 12:58 UTC Nov 14 (5-hour window 0% after the 12:50 reset; next reset 17:50 UTC; weekly 53%)
- Resumed: Unit 4 ship fixer (w27gpt298, run wf_53aa04ee-e87), Unit 8 revise+verify (wde55eker, run wf_612af33e-842).
- Launched: Unit 9 content (wrxz4zegz, run wf_7029a018-95f).
- Check-in at 17:55 UTC. PR #15 still open (CI green), waiting on the teacher.

## Status ~13:48 UTC Nov 14
- Unit 4 shipped onto PR #15 (d2bd347). Unit 5 ship running in pav-u5.
- Content running: Unit 8 revise+verify (wde55eker), Unit 9 (wrxz4zegz). Next content: Unit 10 Readiness Check (u10a-c) when one finishes.

## Status 13:58 UTC Nov 14 (5-hour window 49% at 13:54; resets 17:50 UTC; weekly 60%)
- Unit 8 content DONE. Unit 10 content launched (the last unit to write). Unit 9 content running. Unit 5 ship running.
- After all content: only ships remain (5 running, then 6, 7, 8, 9, 10), then the teacher page / mastery map / tracer.

## Status ~15:00 UTC Nov 14 (5-hour window FULL; resets 17:50 UTC; weekly ~65%)
All three died at the limit. RESUME at 17:55 UTC (each: same scriptPath + resumeFromRunId + args file):
- Unit 5 ship: ship-unit.js, run wf_acae2a4f-e12, run-args/u05-ship.json. Its BUILD was cut off part-way in /home/user/pav-u5
  (the build prompt already tells it to review existing edits). Unit 5 ship's review + fix still to come.
- Unit 9 content: content script, run wf_7029a018-95f, run-args/u09-content.json (revise + verify left).
- Unit 10 content: content script, run wf_d13c3f4d-f94, run-args/u10-content.json (harden u10a/b, author u10c, reps, teacher, revise,
  verify left).
- PR #15 (Unit 2 fixes + Units 3 + 4) CI green on d2bd347; waiting on the teacher.

## Status 17:58 UTC Nov 14 (5-hour window 0% after the 17:50 reset; next reset 22:50 UTC; WEEKLY 66%, resets Tue Nov 17 22:00 UTC)
- Resumed: Unit 5 ship (task wgtn54273), Unit 9 content (wmd61o9uq), Unit 10 content (wutybcktd). Same run IDs as above.
- Weekly is burning ~13%/window. Remaining work likely exceeds the weekly quota (teacher OK'd using it all; monthly reset available).
  SHIP PRIORITY: 5 (running), 6, 7, 10 (core path to the campaign), then 8 (optional) and 9 (independent). The course map orders by
  `order`, so shipping 10 before 8/9 is fine.
- Check-in at 22:55 UTC.

## Status ~20:00 UTC Nov 14 — ALL CONTENT WRITTEN (Units 1-10). Only ships remain: 5 (fix phase running), then 6, 7, 10, 8, 9.

## Status 20:46 UTC Nov 14 (5-hour 81%, resets 22:50 UTC; weekly 77%)
- Unit 5 shipped onto PR #15 (d39e1f0). Unit 6 ship running in pav-u6 (resume: ship-unit.js, wf_a09314c0-eda, run-args/u06-ship.json).
- Next ships: 7 (u07-staging; must follow 6), 10, then 8, 9. Each new worktree: `node scripts/copy-runtime.mjs` for Pyodide in public/.
- The 22:55 UTC check-in (trig_01NA4MWSrBxzLtEUpHSEa5Aj) prompt is stale (mentions Unit 5); follow THIS status instead.

## Status after the window filled (~21:40 UTC Nov 14)
- Unit 6 ship: BUILD DONE and green (1281 unit tests, 200 e2e; loop timeouts verified). REVIEW died at the limit → resume
  wf_a09314c0-eda with run-args/u06-ship.json at the 22:55 UTC check-in (review + fix will run).

## Status 22:58 UTC Nov 14 (5-hour 0% after the 22:50 reset; next reset 03:50 UTC Nov 15; weekly 80%)
- Unit 6 ship resumed (task w3cft34r1, run wf_a09314c0-eda): review + fix left. Check-in at 03:55 UTC Nov 15.

## Status 23:50 UTC Nov 14 — PR #15 MERGED (Units 2 fixes, 3, 4, 5 live after Pages deploys). Branch merged with origin/main (88bdd5c).
- Unit 6 ship running in pav-u6 (branch u6-ship-local from d39e1f0). When done: commit in pav-u6, then in the main checkout
  `git merge u6-ship-local` (a normal merge; content of d39e1f0 == main), push, and open a NEW PR (#15 is merged — never reuse it).
  Subscribe to the new PR.
