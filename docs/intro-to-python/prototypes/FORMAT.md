# Prototype unit format (the authored source of Intro to Python)

Every unit of the course is written as plain Python data in this folder. `harness.py` proves it works,
`scripts/course/export_prototypes.py` turns it into the JSON the site reads. **Edit the `.py` files, never
the JSON.**

```
docs/intro-to-python/prototypes/u01_hello_world.py   ─┐
docs/intro-to-python/prototypes/u03a_lists.py         ├─ harness.py (verify)  ─┐
docs/intro-to-python/prototypes/u03b_lists.py        ─┘                        │
scripts/course/sample/u00_sample.py   (teacher preview + e2e fixture)          │
                                                                               ▼
                                          scripts/course/export_prototypes.py (npm run course:export)
                                                                               │
              content/courses/intro-python/units/<unit-id>.json          ◄─────┤  what the site shows
              content/courses/intro-python/units/<unit-id>.verify.json   ◄─────┤  harness-only data (tests)
              content/courses/intro-python/glossary.json                 ◄─────┤  every GLOSSARY, merged
              src/lib/course/units.generated.ts                          ◄─────┘  imports every unit JSON
```

## The workflow

```bash
python3 docs/intro-to-python/prototypes/harness.py u03                            # verify one unit (prefix)
python3 docs/intro-to-python/prototypes/harness.py                                # verify every unit
PROTOTYPE_DIR=scripts/course/sample python3 docs/intro-to-python/prototypes/harness.py   # verify the sample
npm run course:export                                                             # write the JSON
python3 scripts/course/export_prototypes.py --check                               # is the JSON up to date?
npx vitest run src/lib/course/content.test.ts                                     # what CI checks
```

1. Write or change a `uNN_<slug>.py` file.
2. Run the harness until it reports `0 errors` (fix warnings about reading level where you can).
3. Run `npm run course:export` and commit the `.py` file **and** the generated files together.

CI runs `src/lib/course/content.test.ts`, which re-runs the harness, runs `export --check` (it fails if
you changed a prototype and forgot to export), parses every unit with the zod schema in
`src/lib/course/schema.ts`, and checks glossary links and ids.

Exporter options: `--check` (compare only, exit 1 if stale), `--sample-only --out DIR` (just the sample,
into DIR), `--src DIR` (read other folders), `--out DIR` (write somewhere else), `--root DIR`.
The exporter refuses unknown fields, so a typo like `starter_pases` is an error, not a silent no-op.
On any error it writes nothing.

## Files

- Name: `uNN_<slug>.py`, for example `u01_hello_world.py`. `NN` is two digits. Files run in name order, and
  the [concept gate](#concept-tokens-and-the-gate) follows that order.
- A big unit can be split: `u03a_lists.py`, `u03b_lists.py`, ... Each part repeats the same `UNIT` dict
  (or at least the same `id`; any field two parts both give must match). Their `ITEMS` are joined in
  file order. Two different numbers (`u03`, `u04`) may not share a unit id.
- Each file defines three module-level names. No imports are needed.

| Name | Required | What it is |
| --- | --- | --- |
| `UNIT` | yes | `dict(...)` describing the unit |
| `ITEMS` | yes | list of item dicts, in the order students see them |
| `GLOSSARY` | no | list of glossary entries this file's prose links to |

Units appear on the site in `order`, not file-name order, and no two units may share an `order`.

## UNIT

| Field | Type | JSON | Notes |
| --- | --- | --- | --- |
| `id` | slug | `id` | lower-case words joined by dashes, e.g. `hello-world`. Not `glossary`, `placement`, `cheatsheets` or `preview` (those are pages). The JSON file is `units/<id>.json`. |
| `order` | int ≥ 1 | `order` | position on the course map |
| `title` | str | `title` | "Hello World" |
| `subtitle` | str, optional | `subtitle` | the in-world name, "Words by the Fire" |
| `published` | bool, default `False` | `published` | unpublished units show only with `?preview=1`. Flip to `True` when a unit is ready for students. |
| `martu_intro` | prose | `martuIntro` | Mar'tu's opening for the unit page |
| `goals` | list of str | `goals` | "You will be able to ..." lines (prose: backticks and glossary links work) |
| `campaign_links` | list of str | `campaignLinks` | campaign module ids this unit prepares for, e.g. `"leylines-awaken"` |
| `notes` | str | sidecar only | designer notes |

## GLOSSARY

```python
GLOSSARY = [
    dict(term="string", aliases=["strings", "text"], plain="Text inside quotes.", example='"Shield up."'),
]
```

| Field | Type | Notes |
| --- | --- | --- |
| `term` | str | what `[[term]]` links to (matching ignores case) |
| `aliases` | list of str, optional | other spellings that link to the same entry: `[[strings]]` |
| `plain` | str | the plain-English definition, first thing a student reads |
| `example` | str, optional | a tiny example (plain text, shown as code) |

Every file's `GLOSSARY` is merged into `glossary.json`, sorted by term. A term defined twice is kept once
(the first unit in course order wins; the exporter warns if the two definitions differ). Terms and
aliases must not repeat across entries. Every `[[link]]` in any prose must resolve, or CI fails.

## Prose (Mar'tu's text, checkpoint text, hints, article bodies, explanations)

- One paragraph per line: separate paragraphs with `\n`.
- Lines starting `1. `, `2. ` ... render as a numbered list.
- `` `backticks` `` render as inline code. Keep them balanced (CI checks).
- A fenced block renders as code: ` ```python\n...\n``` ` (CI checks fences are closed).
- `[[term]]` or `[[term|shown text]]` links to the glossary.
- Plain, short sentences: students are 11 to 15 and several read slowly. The harness warns above about a
  grade 9 reading level and above 230 words of Mar'tu text.
- Mar'tu's voice: dry, kind, short sentences, the occasional ", yes?". Keep the world (Tor, the Ley Clock,
  the chalk wall, the barrier, Oogrish, Gearshift, Bomb Shell, Lucky) but never at the cost of clarity.
- Never use a real student's name anywhere.

## Code fields

Code is a Python string, copied **exactly** (the harness runs exactly what the site runs). The exporter
writes code as an array of lines; the site joins them with `\n` and adds a final newline. A leading `\n`
(from a triple-quoted string that starts on the next line) is kept, so start the code on the first line:
`starter="print('hi')\n"`, or use implicit string concatenation as the sample unit does.

Code fields: `starter`, `solution`, `setup`, `example`, `partials`, wrong-answer `code`, bonus `solution`,
`campaign_link.snippet`, `predict.code`, question `code` / `fix`, article example `code`, cheatsheet `code`.
A check's code stays a string when it is one line, and becomes an array of lines when longer.

## ITEMS

Every item has:

| Field | Type | JSON | Notes |
| --- | --- | --- | --- |
| `kind` | str | `kind` | `lesson`, `quiz`, `project`, `challenge`, `article`, `cheatsheet`, `testout` |
| `id` | slug | `id` | unique within the unit; it is the page URL `/intro-python/<unit>/<item>/` |
| `title` | str | `title` | |
| `optional` | bool | `optional` | optional items never block progress. Default `False`, except `challenge`, `cheatsheet` and `testout` (default `True`). |
| `minutes` | int | `minutes` | rough time for a typical student |
| `summary` | str | `summary` | one line for the unit page |
| `notes` | str | sidecar only | designer notes (not for `project` / `challenge`, whose `notes` are exercise notes) |
| `introduces` | list of tokens | sidecar only | **article (and other non-exercise items) only**: concepts the item teaches, for the concept gate |

Kinds:

| Kind | Extra fields |
| --- | --- |
| `lesson` | `exercises=[EXERCISE, ...]` (at least one) |
| `quiz` | `questions=[QUESTION, ...]` (at least one) |
| `project` | every [EXERCISE field](#exercise) directly on the item (its checkpoints are the task list), plus `intro` (prose shown above the tasks). `support` defaults to `"light"`. The project's `id`/`title` are also its exercise id/title. |
| `challenge` | every EXERCISE field directly on the item, plus `level="core"` or `"advanced"` (default core) and `variant_of="<challenge item id>"` for an advanced variant. `support` defaults to `"light"`. |
| `article` | `body` (prose), `examples=[dict(code=..., output=..., stdin=[...])]` (runnable, output is verified; no `setup`), optional `exercises=[EXERCISE, ...]` (try-its) |
| `cheatsheet` | `entries=[dict(concept=..., code=..., output=..., note=...)]`. If `output` is given the harness runs the code and checks it, so leave `output` out for code that calls `input()`. No `setup`/`stdin`. |
| `testout` | `exercises=[EXERCISE, ...]`: the unit's Quick Check. Passing all of them tests out of the unit. Give each exercise `support="none"` (no hints shown; still write 2 hints, the schema needs them). |

## EXERCISE

| Field | Type | JSON | Notes |
| --- | --- | --- | --- |
| `id` | slug | `id` | unique within its item |
| `title` | str | `title` | |
| `martu` | prose | `martu` | Mar'tu's explanation: the Learn pane. Required for every exercise, project and challenge. |
| `example` | code | `example.code` | Mar'tu's worked example |
| `example_output` | str | `example.output` | exactly what `example` prints (verified). Required with `example`. |
| — | — | `example.stdin` | copied from the exercise `stdin` when the example calls `input(`, because the harness runs the example with the exercise's answers |
| `another_way` | list | `anotherWay` | `dict(angle="analogy", label="Think of jars", text="...")`: alternate explanations the student can open. `label` optional. |
| `introduces` | list of tokens | `introduces` | concepts this exercise teaches (opens the concept gate for this and later code) |
| `preview` | list of tokens | `preview` | concepts shown here *before* they are taught, on purpose (say why in `notes`) |
| `engine` | bool | `engine` | `True` loads the campaign objects (`party`, `print_prompt`, `print_options`, `user`, `_prompts`, ...). Off for ordinary exercises, so `print(user)` is a real NameError. |
| `setup` | code | `setup` | hidden code run before the student's code. Names it defines can be used by the student. |
| `stdin` | list of str | `stdin` | the answers `input()` gets, in order. The console echoes `prompt + answer` on one line. Asking for more raises `EOFError`. |
| `starter` | code | `starter` | what the editor starts with (may be `""`) |
| `checkpoints` | list | `checkpoints` | 1 to 12, see below |
| `solution` | code | `solution` | must pass every checkpoint |
| `starter_passes` | bool | `starterPasses` | `True` for "run this and read it" exercises: the starter already passes. Otherwise the starter must fail a checkpoint. |
| `tracer` | bool | `tracer` | offer the step-through tracer |
| `support` | `"full"` / `"light"` / `"none"` | `support` | full: hints, another way, solution after gating. light: hints after the first failed run. none: test-outs. |
| `bonus` | dict | `bonus` | a side quest, see below |
| `assemble` | dict | `assemble` | "Assemble it": the solution as shuffled lines, `dict(lines=[...in order...], distractors=[...])` (a string is split into lines). Students reach it through Help, under "More structure". |
| `campaign_link` | dict | `campaignLink` | Lucky's "What's in it for me?" box: `dict(module="leylines-awaken", part="program-dialogue-prompt", snippet="code", why="prose")`. `snippet` optional. |
| `takeaway` | str | `takeaway` | one line for the cheatsheet / skill map |
| `predict` | dict | `predict` | Predict before Run, see [below](#predict-before-run). Free: a thinking prompt, never a test, and it never blocks Run. Hidden in Quick Checks. |
| `names` | list of str | `names` | the "Names to use" chips: every exact name the steps ask for (variables, functions, parameters), e.g. `["caster", "mana"]`. Shown in every preset. The harness warns about a name the solution never uses. |
| `pick` | str | `pick` | Mar'tu's pick: a value to use when the student can't decide, e.g. `'"Gearshift"'` (shown as code; a value with `\n` shows as a block). Every other value the checks allow is still accepted, so only use it where the checks accept any value. The player wraps plain words in quotes; a pick that starts with `#` is a note and goes in as it is, on a line of its own. |
| `pair_talk` | prose | `pairTalk` | an optional "Pair talk" prompt, e.g. "Tell your partner why `mana` needs `str()`." The site adds the "Pair talk:" label. Every student still does every step on their own device (no shared-device steps). |
| `solo` | bool | `solo` | `True` for the lesson's SOLO item (one per lesson, about 2 minutes, done alone). Recorded, never blocking. Default `False`. |
| `partials` | list of code | sidecar only | staged solutions: partial *k* passes checkpoints 1..k and fails k+1 |
| `wrong_answers` | list | sidecar only | `dict(why="...", code="...", fails_at=2, message_contains="quotes")`: a known wrong answer must fail at checkpoint `fails_at` (0 = it crashes before the checks) with a message containing `message_contains` |
| `notes` | str | sidecar only | designer notes |

### Checkpoints

```python
dict(
    id="make-caster",                       # optional: defaults to "step-1", "step-2", ... by position
    text="1. Make a variable called `caster` that holds the text `\"Gearshift\"`.",
    hints=["point at the idea", "teach it", "show nearly the answer"],
    checks=[("caster holds Gearshift", "assert caster == 'Gearshift', 'Store the text Gearshift in caster.'")],
    pass_line="Gearshift: Visor dims. Name logged.",   # optional, shown when it turns green
    dictated=True,                          # optional: the text spells out the code to type
)
```

| Field | JSON | Notes |
| --- | --- | --- |
| `id` | `id` | slug, unique within the exercise. Give real ids once students use a unit: progress is saved by id, so renaming or reordering a `step-N` checkpoint resets it. |
| `text` | `text` | one action, at most two sentences. A leading `1. ` is stripped (the site numbers checkpoints). |
| `hints` | `hints` | the hint ladder, 2 to 5 rungs: point, teach, show. The site's Help control shows them as "Where to look" (the first), "Teach me" (the middle ones) and "Show me how" (the last), with "Another way" and "More structure" (Assemble it) in between, then "Compare with Mar'tu's version". Write the last hint with the step's own line in backticks (``Write `mana = 20` on its own line.``): its start up to the first `(` or `=` becomes "Start me off" (`mana =`), but only if the solution uses it. Never show an example's names there. |
| `checks` | `checks` | `(name, code)` pairs (or `dict(name=..., code=...)`) |
| `pass_line` | `passLine` | optional in-world line |
| `dictated` | `dictated` | optional bool. `True` when the text spells out the code to type ("Write `mana = 20`"); `False` for a goal-only step that gives the goal and the names, never the code ("Print a greeting that uses `name`."). The curriculum asks for at least one `dictated=False` step in every lesson (§2.1, lint g). Left out: not marked either way. |

**Checks** run after the student's code, in the same namespace, only if the code ran without an error.
The assert message is what the student sees: one plain sentence. Besides the student's own names a
check can use `_captured_stdout`, `_lines()` (printed lines, stripped, blanks removed), `_source`,
`_uses("node:For")`, `_count("call:print")`, `_assigned_from_expression("total")`, `_inputs_used()`, and
with `engine=True` the campaign records (`_prompts`, `_options`, `party._moves`, ...).

Rules the harness and the grading rely on:
- **Checks must stay true as later checkpoints are finished.** Use `'48' in _lines()`, not
  `_lines() == ['48']`, because the final solution must pass every checkpoint.
- Checkpoints are graded in order: the first failing one is the active one.
- A check that names a variable the student has not made raises `NameError`; the site turns that into a
  friendly "I looked for `caster` but could not find it" message, so you do not need to guard for it.
- Stop hard-coding with `_source` checks (`'Lucky' not in _source`) and prove it with a `wrong_answers` entry.

### Predict before Run

```python
predict=dict(
    q="Before you press Run: what will this line print?",
    code='print("Hours until the next burst:", 37)\n',   # optional: left out, the student predicts the starter
    choices=["Hours until the next burst: 37", "Hours until the next burst:37", '"Hours until the next burst:", 37'],
    answer=0,                                   # the right choice: its index, or its exact text
    explain="The quotes are not printed. The comma becomes one space.",   # shown after the guess, right or wrong
)
```

| Field | JSON | Notes |
| --- | --- | --- |
| `q` | `q` | prose: the question |
| `code` | `code` | optional code to predict. Left out, it is the exercise's `starter`. It runs with the exercise's `setup` and `stdin`, and the concept gate checks it. |
| `choices` | `choices` | 2 or more one-click choices. Write each one exactly as the console would show it. |
| `answer` | `answer` | the index of the right choice, or its exact text (the exporter turns text into the index). The harness runs `code` and fails if the right choice is not exactly what it prints. |
| `explain` | `explain` | prose shown after the guess, right or wrong |

### Bonus (side quest)

`dict(by="lucky", title="What's in it for me?", text="prose", hints=["..."], checks=[...], solution="code")`.
`by` is one of `mar-tu`, `oogrish`, `gearshift`, `bomb-shell`, `lucky` (default `lucky`). Its solution must
pass its checks, and the plain exercise solution should not (the harness warns).

## QUESTION

Every question has `type`, `q` (prose), `explain` (prose, shown after answering, right or wrong), and an
optional `id` (slug; defaults to `q-1`, `q-2`, ... by position). `notes` goes to the sidecar.

| Type | Fields | JSON names | Verified by the harness |
| --- | --- | --- | --- |
| `mc` | `code` (optional), `choices`, `answer` (index), `why_wrong={index: "why"}` | `whyWrong` (keys become `"0"`, `"1"` ...) | answer index in range |
| `predict` | `code`, `answer` (exact output), `choices` (optional), `setup`, `stdin` | | runs `code`; `answer` must be what it prints and be one of `choices` |
| `fill` | `code` with `___`, `answer`, `accept` (other right answers), `expected_output` | `expectedOutput` | every answer in place of `___` prints `expected_output` |
| `parsons` | `lines` (correct order), `distractors`, `expected_output` | `expectedOutput` | the lines in order print `expected_output` |
| `bug` | `code` (buggy), `fix`, `expected_output` | `expectedOutput` | `fix` prints `expected_output`; `code` does not |

Only `predict` questions may have `setup` or `stdin`.

## Concept tokens and the gate

No code a student *sees* (starter, solution, example, partials, quiz code, article examples) may use a
concept before some earlier exercise `introduces` it, in course order. Tokens look like `node:For`,
`op:Add`, `const:str`, `call:print`, `attr:append`, `import:random`. The full list is in the docstring
of `harness.py`. To show something early on purpose, list it in that exercise's `preview`.
The sample unit is verified on its own, so it introduces everything it uses.

## The `.verify.json` sidecar

Harness-only data never reaches a page. It lands in `units/<unit-id>.verify.json`, for tests:

```json
{
  "unit": "sample",
  "notes": "unit notes (only when given)",
  "items": { "<item id>": { "introduces": ["..."], "notes": "..." } },
  "exercises": {
    "<item id>/<exercise id>": {
      "partials": [["line", "line"]],
      "wrongAnswers": [{ "why": "...", "code": ["..."], "failsAt": 2, "messageContains": "..." }],
      "notes": "..."
    },
    "<project or challenge item id>": { "partials": [] }
  },
  "questions": { "<quiz id>/<question id>": { "notes": "..." } }
}
```

## Name mapping (prototype → JSON)

| Prototype | JSON |
| --- | --- |
| `martu_intro` | `martuIntro` |
| `campaign_links` | `campaignLinks` |
| `example` + `example_output` | `example: {code, output, stdin?}` |
| `another_way` | `anotherWay` |
| `starter_passes` | `starterPasses` |
| `campaign_link` | `campaignLink` |
| `pass_line` | `passLine` |
| `pair_talk` | `pairTalk` |
| `variant_of` | `variantOf` |
| `why_wrong` | `whyWrong` |
| `expected_output` | `expectedOutput` |
| `wrong_answers`, `fails_at`, `message_contains` | sidecar `wrongAnswers`, `failsAt`, `messageContains` |
| check `(name, code)` | `{ "name": ..., "code": ... }` |

Everything else keeps its name. Fields left out stay out of the JSON (the schema fills defaults), except
`published`, which is always written.

## The sample unit

`scripts/course/sample/u00_sample.py` (unit id `sample`, order 99, unpublished) uses every item kind,
every question type and every exercise feature above, including `predict`, `names`, `pick`, `pair_talk`,
`solo` and `dictated` (both `True` and `False`). It is the teacher's tour of the player and the e2e
fixture, so keep it passing and keep it covering everything (`content.test.ts` checks the coverage).
Open it on the site with `?preview=1`.
