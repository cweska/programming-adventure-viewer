# Overnight assumptions (Nov 12–13, 2026)

The teacher went to bed at about 11:15pm MST and asked that questions wait until morning. These are the calls made
without them. Each one is easy to change in the morning.

| # | Assumption | Easy to change? |
|---|---|---|
| 1 | Unit 1 ships to students (`published: true`). Later units stay unpublished (preview only with `?preview=1`) until they pass every check, then publish. | Flip `published` in the unit's prototype and re-export. |
| 2 | The sample unit (every feature, for teachers) stays unpublished. Open it at `/intro-python/?preview=1`. | Same flag. |
| 3 | Progress is saved only in each student's browser. The teacher page with "Needs you now" and the mastery map come after noon. | n/a |
| 4 | The pull request to `main` is opened as soon as Unit 1 passes all tests, e2e and phone/desktop checks. Work on later units continues on the same branch, but unverified work only goes into `docs/intro-to-python/wip/`, which nothing on the site reads. | Merge whenever you like. |
| 5 | Students start at Unit 1 and the course map shows all published units. Nothing is locked: students can open any published item (Codecademy-style), and Quick Checks let confident students skip ahead. | A lock option can be added. |
| 6 | Mar'tu's re-grounding tone: name the struggle kindly once, then quick wins. Campaign links point back to code they already played. | Edit the prose. |
| 7 | Optional "Pair talk" prompts appear only where a talk-through helps. Each student still finishes every step on their own device. | Edit the prose. |
| 8 | Hero names and other personal values students type stay in their browser. Nothing a student types is sent anywhere. | n/a |
| 9 | Autosave commits are marked `[skip ci]` so they don't flood GitHub Actions. Deliberate commits run CI as usual. | n/a |

## Questions saved for the morning

(Added here as they come up, instead of waiting for an answer overnight.)
