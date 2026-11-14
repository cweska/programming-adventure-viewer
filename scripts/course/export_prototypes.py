#!/usr/bin/env python3
"""Export the Intro to Python prototype units (plain Python data) to the JSON the site reads.

Authored source (see docs/intro-to-python/prototypes/FORMAT.md):
    docs/intro-to-python/prototypes/uNN*_*.py     the course units, verified by harness.py
    scripts/course/sample/u00_sample.py          the teacher-preview sample unit (also the e2e fixture)

Output (never edit these by hand):
    content/courses/intro-python/units/<unit-id>.json          the unit, in the shape of src/lib/course/schema.ts
    content/courses/intro-python/units/<unit-id>.verify.json   harness-only data: partials, wrong answers, notes
    content/courses/intro-python/glossary.json                 every GLOSSARY entry, merged and sorted
    src/lib/course/units.generated.ts                          imports every unit JSON, in course order

Usage:
    python3 scripts/course/export_prototypes.py              # export (npm run course:export)
    python3 scripts/course/export_prototypes.py --check      # exit 1 if the committed files are stale
    python3 scripts/course/export_prototypes.py --sample-only --out DIR   # only the sample unit, into DIR

Options:
    --root DIR     repository root (default: the repository this script lives in)
    --src DIR      read prototype files from DIR instead of the default folders (repeatable)
    --out DIR      write DIR/units/*.json, DIR/glossary.json and DIR/units.generated.ts instead of the repo
    --sample-only  read only scripts/course/sample (needs --out, so the committed course is never replaced)

Output is deterministic: keys in schema order, 2-space JSON, UTF-8, trailing newline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import runpy
import sys
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parents[1]
PROTOTYPE_REL = Path("docs/intro-to-python/prototypes")
SAMPLE_REL = Path("scripts/course/sample")
CONTENT_REL = Path("content/courses/intro-python")
TS_REL = Path("src/lib/course/units.generated.ts")
FILE_GLOB = "u[0-9][0-9]*_*.py"  # the same glob harness.py uses

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOKEN = re.compile(r"^(node|op|const|call|attr|import):[A-Za-z_]+$")
LEADING_NUMBER = re.compile(r"^\s*\d+[.)]\s+")
RESERVED_UNIT_IDS = {"glossary", "placement", "cheatsheets", "preview"}
ITEM_KINDS = ("lesson", "quiz", "project", "challenge", "article", "cheatsheet", "testout")
QUESTION_TYPES = ("mc", "predict", "fill", "parsons", "bug")
CAMEOS = ("mar-tu", "oogrish", "gearshift", "bomb-shell", "lucky")


class Ctx:
    """Collects every problem so an author sees them all at once."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


Conv = Callable[[Any, str, Ctx], Any]

# ---------------------------------------------------------------------------------------------
# Value converters
# ---------------------------------------------------------------------------------------------


def text(value: Any, where: str, ctx: Ctx) -> str:
    if not isinstance(value, str):
        ctx.error(where, f"expected text, got {type(value).__name__}")
        return str(value)
    if not value.strip():
        ctx.error(where, "is empty")
    return value


def plain_str(value: Any, where: str, ctx: Ctx) -> str:
    """A string that may be empty (outputs, answers)."""
    if not isinstance(value, str):
        ctx.error(where, f"expected a string, got {type(value).__name__}")
        return str(value)
    return value


def boolean(value: Any, where: str, ctx: Ctx) -> bool:
    if not isinstance(value, bool):
        ctx.error(where, f"expected True or False, got {value!r}")
    return bool(value)


def integer(value: Any, where: str, ctx: Ctx) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        ctx.error(where, f"expected a whole number, got {value!r}")
        return 0
    return value


def slug(value: Any, where: str, ctx: Ctx) -> str:
    if not isinstance(value, str) or not SLUG.match(value):
        ctx.error(where, f"id {value!r} must be lower-case words joined by dashes (like 'read-the-wall')")
    return str(value)


def str_list(value: Any, where: str, ctx: Ctx) -> list[str]:
    if not isinstance(value, (list, tuple)):
        ctx.error(where, f"expected a list of strings, got {type(value).__name__}")
        return []
    out = []
    for i, item in enumerate(value):
        if not isinstance(item, str):
            ctx.error(f"{where}[{i}]", f"expected a string, got {item!r}")
        out.append(str(item))
    return out


def token_list(value: Any, where: str, ctx: Ctx) -> list[str]:
    tokens = str_list(value, where, ctx)
    for token in tokens:
        if not TOKEN.match(token):
            ctx.error(where, f"{token!r} is not a concept token (like 'node:For' or 'call:print')")
    return tokens


def code_lines(value: Any, where: str, ctx: Ctx) -> list[str]:
    """Code as an array of lines. The schema joins them with "\\n" and adds a final newline."""
    if not isinstance(value, str):
        ctx.error(where, f"expected code as a string, got {type(value).__name__}")
        return []
    if value == "":
        return []
    body = value[:-1] if value.endswith("\n") else value
    return body.split("\n")


def check_code(value: Any, where: str, ctx: Ctx) -> str | list[str]:
    """One-line checks stay strings (easier to read); longer ones become arrays of lines."""
    lines = code_lines(value, where, ctx)
    if not lines or not "".join(lines).strip():
        ctx.error(where, "check code is empty")
    return lines[0] if len(lines) == 1 else lines


def line_list(value: Any, where: str, ctx: Ctx) -> list[str]:
    """Parsons / assemble lines: a list of strings, or one string split into lines."""
    if isinstance(value, str):
        return code_lines(value, where, ctx)
    return str_list(value, where, ctx)


def list_of(conv: Conv) -> Conv:
    def convert(value: Any, where: str, ctx: Ctx) -> list:
        if not isinstance(value, (list, tuple)):
            ctx.error(where, f"expected a list, got {type(value).__name__}")
            return []
        return [conv(item, f"{where}[{i}]", ctx) for i, item in enumerate(value)]

    return convert


def one_of(options: tuple[str, ...]) -> Conv:
    def convert(value: Any, where: str, ctx: Ctx) -> str:
        if value not in options:
            ctx.error(where, f"{value!r} must be one of {', '.join(options)}")
        return str(value)

    return convert


# ---------------------------------------------------------------------------------------------
# Object converters (keys come out in schema order)
# ---------------------------------------------------------------------------------------------


def as_dict(value: Any, where: str, ctx: Ctx) -> dict:
    if not isinstance(value, dict):
        ctx.error(where, f"expected a dict(...), got {type(value).__name__}")
        return {}
    return value


def unknown_keys(src: dict, allowed: set[str], where: str, ctx: Ctx, hint: str = "") -> None:
    for key in src:
        if key not in allowed:
            ctx.error(where, f"unknown field {key!r}{hint} (see docs/intro-to-python/prototypes/FORMAT.md)")


def put(out: dict, dst: str, src: dict, key: str, conv: Conv, where: str, ctx: Ctx, required: bool = False) -> None:
    if key in src and src[key] is not None:
        out[dst] = conv(src[key], f"{where}.{key}", ctx)
    elif required:
        ctx.error(where, f"missing field {key!r}")


def check(value: Any, where: str, ctx: Ctx) -> dict:
    if isinstance(value, dict):
        unknown_keys(value, {"name", "code"}, where, ctx)
        name, code = value.get("name"), value.get("code")
    elif isinstance(value, (list, tuple)) and len(value) == 2:
        name, code = value
    else:
        ctx.error(where, "a check is a (name, code) pair")
        return {"name": "?", "code": ""}
    return {"name": text(name, f"{where}.name", ctx), "code": check_code(code, f"{where}.code", ctx)}


def checks_list(value: Any, where: str, ctx: Ctx) -> list:
    """A checkpoint's (or side quest's) checks. Names must differ: the site regroups results by name."""
    out = list_of(check)(value, where, ctx)
    unique(out, "name", where, ctx)
    return out


def checkpoint(cp: Any, index: int, where: str, ctx: Ctx) -> dict:
    cp = as_dict(cp, where, ctx)
    unknown_keys(cp, {"id", "text", "hints", "checks", "pass_line", "dictated"}, where, ctx)
    out: dict = {"id": slug(cp["id"], f"{where}.id", ctx) if "id" in cp else f"step-{index}"}
    if "text" in cp:
        out["text"] = LEADING_NUMBER.sub("", text(cp["text"], f"{where}.text", ctx), count=1)
    else:
        ctx.error(where, "missing field 'text'")
    put(out, "hints", cp, "hints", list_of(text), where, ctx, required=True)
    put(out, "checks", cp, "checks", checks_list, where, ctx, required=True)
    put(out, "passLine", cp, "pass_line", text, where, ctx)
    put(out, "dictated", cp, "dictated", boolean, where, ctx)
    return out


def card_sort(value: Any, where: str, ctx: Ctx) -> dict:
    """A one-click card sort on an Another way angle: dict(groups=[2 or 3 names], cards=[(code, group index), ...],
    explain="prose shown after Check my sort"). Every group gets at least one card."""
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"groups", "cards", "explain"}, where, ctx)
    out: dict = {}
    put(out, "groups", value, "groups", str_list, where, ctx, required=True)
    groups = out.get("groups", [])
    if not 2 <= len(groups) <= 3:
        ctx.error(f"{where}.groups", f"a card sort needs 2 or 3 groups, got {len(groups)}")
    cards = []
    raw = value.get("cards")
    if not isinstance(raw, (list, tuple)) or len(raw) < 2:
        ctx.error(f"{where}.cards", "a card sort needs 2 or more cards")
        raw = []
    for i, card in enumerate(raw):
        at = f"{where}.cards[{i}]"
        if isinstance(card, dict):
            unknown_keys(card, {"text", "group"}, at, ctx)
            shown, group = card.get("text"), card.get("group")
        elif isinstance(card, (list, tuple)) and len(card) == 2:
            shown, group = card
        else:
            ctx.error(at, "a card is (text, group index) or dict(text=..., group=...)")
            continue
        if not isinstance(shown, str) or not shown.strip():
            ctx.error(at, "a card needs its text")
        if isinstance(group, bool) or not isinstance(group, int) or not 0 <= group < len(groups):
            ctx.error(at, f"a card's group must be 0 to {len(groups) - 1}")
            continue
        cards.append({"text": shown, "group": group})
    for g in range(len(groups)):
        if cards and not any(card["group"] == g for card in cards):
            ctx.error(f"{where}.cards", f"no card goes in group {g} ({groups[g]!r})")
    out["cards"] = cards
    put(out, "explain", value, "explain", text, where, ctx, required=True)
    return out


def another_way(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"angle", "label", "text", "sort"}, where, ctx)
    out: dict = {}
    put(out, "angle", value, "angle", text, where, ctx, required=True)
    put(out, "label", value, "label", text, where, ctx)
    put(out, "text", value, "text", text, where, ctx, required=True)
    put(out, "sort", value, "sort", card_sort, where, ctx)
    return out


def bonus(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"by", "title", "text", "hints", "checks", "solution"}, where, ctx)
    out: dict = {}
    put(out, "by", value, "by", one_of(CAMEOS), where, ctx)
    put(out, "title", value, "title", text, where, ctx)
    put(out, "text", value, "text", text, where, ctx, required=True)
    put(out, "hints", value, "hints", list_of(text), where, ctx)
    put(out, "checks", value, "checks", checks_list, where, ctx, required=True)
    put(out, "solution", value, "solution", code_lines, where, ctx, required=True)
    return out


def assemble(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"lines", "distractors"}, where, ctx)
    out: dict = {}
    put(out, "lines", value, "lines", line_list, where, ctx, required=True)
    put(out, "distractors", value, "distractors", line_list, where, ctx)
    return out


def campaign_link(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"module", "part", "snippet", "why"}, where, ctx)
    out: dict = {}
    put(out, "module", value, "module", text, where, ctx, required=True)
    put(out, "part", value, "part", text, where, ctx, required=True)
    put(out, "snippet", value, "snippet", code_lines, where, ctx)
    put(out, "why", value, "why", text, where, ctx, required=True)
    return out


def example(value: Any, where: str, ctx: Ctx) -> dict:
    """An article example: dict(code=..., output=..., stdin=[...])."""
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"code", "output", "stdin"}, where, ctx, hint=" (site examples cannot have setup)")
    out: dict = {}
    put(out, "code", value, "code", code_lines, where, ctx, required=True)
    put(out, "output", value, "output", plain_str, where, ctx, required=True)
    put(out, "stdin", value, "stdin", str_list, where, ctx)
    return out


def cheatsheet_entry(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"concept", "code", "output", "note"}, where, ctx, hint=" (site entries cannot have setup or stdin)")
    out: dict = {}
    put(out, "concept", value, "concept", text, where, ctx, required=True)
    put(out, "code", value, "code", code_lines, where, ctx, required=True)
    put(out, "output", value, "output", plain_str, where, ctx)
    put(out, "note", value, "note", text, where, ctx)
    return out


def exercise_predict(value: Any, where: str, ctx: Ctx) -> dict:
    """Predict before Run: dict(q=..., code=<optional>, choices=[...], answer=<index or exact text>, explain=...)."""
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"q", "code", "choices", "answer", "explain"}, where, ctx, hint=" for an exercise predict")
    out: dict = {}
    put(out, "q", value, "q", text, where, ctx, required=True)
    put(out, "code", value, "code", code_lines, where, ctx)
    put(out, "choices", value, "choices", str_list, where, ctx, required=True)
    choices = out.get("choices", [])
    if "choices" in value and len(choices) < 2:
        ctx.error(where, "predict needs at least 2 choices (the site shows a one-click choice)")
    answer = value.get("answer")
    if isinstance(answer, bool) or answer is None:
        ctx.error(where, "predict needs an answer: the index of the right choice, or its exact text")
    elif isinstance(answer, int):
        if not 0 <= answer < len(choices):
            ctx.error(where, f"predict answer {answer} is not a choice index (0 to {len(choices) - 1})")
        out["answer"] = answer
    elif isinstance(answer, str):
        if answer not in choices:
            ctx.error(where, f"predict answer {answer!r} is not one of the choices")
        out["answer"] = choices.index(answer) if answer in choices else 0
    else:
        ctx.error(where, f"predict answer must be a choice index or text, got {answer!r}")
    put(out, "explain", value, "explain", text, where, ctx, required=True)
    return out


EXERCISE_KEYS = {
    "id", "title", "martu", "example", "example_output", "another_way", "introduces", "preview",
    "engine", "setup", "stdin", "starter", "checkpoints", "solution", "starter_passes", "tracer", "support", "bonus",
    "assemble", "campaign_link", "takeaway", "predict", "names", "pick", "pair_talk", "solo", "explainer",
}
EXERCISE_HARNESS_ONLY = {"partials", "wrong_answers", "notes"}


def exercise_fields(ex: dict, where: str, ctx: Ctx, verify: dict, verify_key: str, out: dict | None = None) -> dict:
    """The exercise fields shared by lesson exercises, projects, challenges, test-outs and article try-its."""
    out = {} if out is None else out
    put(out, "id", ex, "id", slug, where, ctx, required=True)
    put(out, "title", ex, "title", text, where, ctx, required=True)
    put(out, "martu", ex, "martu", text, where, ctx, required=True)
    if ex.get("example") is not None:
        if "example_output" not in ex:
            ctx.error(where, "example needs example_output (what it prints)")
        shown: dict = {
            "code": code_lines(ex["example"], f"{where}.example", ctx),
            "output": plain_str(ex.get("example_output", ""), f"{where}.example_output", ctx),
        }
        if ex.get("stdin") and "input(" in str(ex["example"]):
            # The harness runs the example with the exercise's stdin; the site needs it on the example.
            shown["stdin"] = str_list(ex["stdin"], f"{where}.stdin", ctx)
        out["example"] = shown
    elif "example_output" in ex:
        ctx.error(where, "example_output given without an example")
    put(out, "anotherWay", ex, "another_way", list_of(another_way), where, ctx)
    put(out, "introduces", ex, "introduces", token_list, where, ctx)
    put(out, "preview", ex, "preview", token_list, where, ctx)
    put(out, "engine", ex, "engine", boolean, where, ctx)
    if isinstance(ex.get("setup"), str) and ex["setup"].strip():
        out["setup"] = code_lines(ex["setup"], f"{where}.setup", ctx)
    elif ex.get("setup") not in (None, ""):
        ctx.error(f"{where}.setup", "expected code as a string")
    put(out, "stdin", ex, "stdin", str_list, where, ctx)
    put(out, "starter", ex, "starter", code_lines, where, ctx, required=True)
    if isinstance(ex.get("checkpoints"), (list, tuple)) and ex["checkpoints"]:
        cps = [checkpoint(cp, i, f"{where}.checkpoints[{i - 1}]", ctx) for i, cp in enumerate(ex["checkpoints"], 1)]
        unique(cps, "id", f"{where}.checkpoints", ctx)
        out["checkpoints"] = cps
    else:
        ctx.error(where, "needs a list of checkpoints")
    put(out, "solution", ex, "solution", code_lines, where, ctx, required=True)
    put(out, "starterPasses", ex, "starter_passes", boolean, where, ctx)
    put(out, "tracer", ex, "tracer", boolean, where, ctx)
    put(out, "support", ex, "support", one_of(("full", "light", "none")), where, ctx)
    put(out, "bonus", ex, "bonus", bonus, where, ctx)
    put(out, "assemble", ex, "assemble", assemble, where, ctx)
    # More structure for the step a student is on (the teacher's Unit 5 ruling): the harness's partials go to the
    # site with Assemble it, so the board shuffles only the lines the active step adds and keeps the rest in place.
    if "assemble" in out and isinstance(ex.get("partials"), (list, tuple)) and ex["partials"]:
        out["assemble"]["steps"] = list_of(code_lines)(ex["partials"], f"{where}.partials", ctx)
    put(out, "campaignLink", ex, "campaign_link", campaign_link, where, ctx)
    put(out, "takeaway", ex, "takeaway", text, where, ctx)
    put(out, "predict", ex, "predict", exercise_predict, where, ctx)
    put(out, "names", ex, "names", str_list, where, ctx)
    put(out, "pick", ex, "pick", text, where, ctx)
    put(out, "pairTalk", ex, "pair_talk", text, where, ctx)
    put(out, "solo", ex, "solo", boolean, where, ctx)
    put(out, "explainer", ex, "explainer", one_of(("full", "lean")), where, ctx)

    sidecar: dict = {}
    put(sidecar, "partials", ex, "partials", list_of(code_lines), where, ctx)
    put(sidecar, "wrongAnswers", ex, "wrong_answers", list_of(wrong_answer), where, ctx)
    put(sidecar, "notes", ex, "notes", text, where, ctx)
    if sidecar:
        verify["exercises"][verify_key] = sidecar
    return out


def wrong_answer(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"why", "code", "fails_at", "message_contains"}, where, ctx)
    out: dict = {}
    put(out, "why", value, "why", text, where, ctx, required=True)
    put(out, "code", value, "code", code_lines, where, ctx, required=True)
    put(out, "failsAt", value, "fails_at", integer, where, ctx)
    put(out, "messageContains", value, "message_contains", text, where, ctx)
    return out


def exercise(value: Any, where: str, ctx: Ctx, verify: dict, verify_key: str) -> dict:
    ex = as_dict(value, where, ctx)
    unknown_keys(ex, EXERCISE_KEYS | EXERCISE_HARNESS_ONLY, where, ctx)
    return exercise_fields(ex, where, ctx, verify, verify_key)


QUESTION_KEYS = {
    "mc": ["type", "id", "q", "code", "choices", "answer", "why_wrong", "explain"],
    "predict": ["type", "id", "q", "code", "setup", "stdin", "choices", "answer", "explain"],
    "fill": ["type", "id", "q", "code", "answer", "accept", "expected_output", "explain"],
    "parsons": ["type", "id", "q", "lines", "distractors", "expected_output", "explain"],
    "bug": ["type", "id", "q", "code", "fix", "expected_output", "explain"],
}


def why_wrong(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    out = {}
    for key in sorted(value, key=lambda k: (int(k) if str(k).isdigit() else 1_000_000, str(k))):
        if not str(key).isdigit():
            ctx.error(where, f"why_wrong keys are choice numbers (0, 1, ...), not {key!r}")
        out[str(key)] = text(value[key], f"{where}[{key}]", ctx)
    return out


def answer_text(value: Any, where: str, ctx: Ctx) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return plain_str(value, where, ctx)


def question(value: Any, index: int, where: str, ctx: Ctx, verify: dict, verify_prefix: str) -> dict:
    q = as_dict(value, where, ctx)
    kind = q.get("type")
    if kind not in QUESTION_KEYS:
        ctx.error(where, f"question type {kind!r} must be one of {', '.join(QUESTION_TYPES)}")
        return {"type": str(kind), "id": f"q-{index}"}
    unknown_keys(q, set(QUESTION_KEYS[kind]) | {"notes"}, where, ctx, hint=f" for a {kind} question")
    out: dict = {"type": kind, "id": slug(q["id"], f"{where}.id", ctx) if "id" in q else f"q-{index}"}
    put(out, "q", q, "q", text, where, ctx, required=True)
    if kind == "mc":
        put(out, "code", q, "code", code_lines, where, ctx)
        put(out, "choices", q, "choices", str_list, where, ctx, required=True)
        put(out, "answer", q, "answer", integer, where, ctx, required=True)
        put(out, "whyWrong", q, "why_wrong", why_wrong, where, ctx)
    elif kind == "predict":
        put(out, "code", q, "code", code_lines, where, ctx, required=True)
        if isinstance(q.get("setup"), str) and q["setup"].strip():
            out["setup"] = code_lines(q["setup"], f"{where}.setup", ctx)
        put(out, "stdin", q, "stdin", str_list, where, ctx)
        put(out, "choices", q, "choices", str_list, where, ctx)
        put(out, "answer", q, "answer", answer_text, where, ctx, required=True)
    elif kind == "fill":
        put(out, "code", q, "code", code_lines, where, ctx, required=True)
        if "___" not in str(q.get("code", "")):
            ctx.error(where, "fill code needs ___ where the answer goes")
        put(out, "answer", q, "answer", answer_text, where, ctx, required=True)
        put(out, "accept", q, "accept", list_of(answer_text), where, ctx)
        put(out, "expectedOutput", q, "expected_output", plain_str, where, ctx, required=True)
    elif kind == "parsons":
        put(out, "lines", q, "lines", line_list, where, ctx, required=True)
        put(out, "distractors", q, "distractors", line_list, where, ctx)
        put(out, "expectedOutput", q, "expected_output", plain_str, where, ctx, required=True)
    elif kind == "bug":
        put(out, "code", q, "code", code_lines, where, ctx, required=True)
        put(out, "fix", q, "fix", code_lines, where, ctx, required=True)
        put(out, "expectedOutput", q, "expected_output", plain_str, where, ctx, required=True)
    put(out, "explain", q, "explain", text, where, ctx, required=True)
    if q.get("notes"):
        verify["questions"][f"{verify_prefix}/{out['id']}"] = {"notes": text(q["notes"], f"{where}.notes", ctx)}
    return out


ITEM_BASE_KEYS = {"kind", "id", "title", "optional", "minutes", "summary"}
ITEM_KEYS = {
    "lesson": {"exercises"},
    "quiz": {"questions"},
    "project": {"intro"} | EXERCISE_KEYS,
    "challenge": {"level", "variant_of"} | EXERCISE_KEYS,
    "article": {"body", "examples", "exercises"},
    "cheatsheet": {"entries"},
    "testout": {"exercises", "questions_to_pass"},
}
# Harness-only item fields (they go to the .verify.json sidecar).
ITEM_HARNESS_ONLY = {"introduces", "notes"}


def item(value: Any, where: str, ctx: Ctx, verify: dict) -> dict:
    src = as_dict(value, where, ctx)
    kind = src.get("kind")
    if kind not in ITEM_KINDS:
        ctx.error(where, f"item kind {kind!r} must be one of {', '.join(ITEM_KINDS)}")
        return {"kind": str(kind), "id": str(src.get("id"))}
    exercise_like = kind in ("project", "challenge")
    harness_only = EXERCISE_HARNESS_ONLY if exercise_like else ITEM_HARNESS_ONLY
    unknown_keys(src, ITEM_BASE_KEYS | ITEM_KEYS[kind] | harness_only, where, ctx, hint=f" for a {kind}")
    out: dict = {"kind": kind}
    put(out, "id", src, "id", slug, where, ctx, required=True)
    item_id = str(src.get("id"))
    where = f"{where.rsplit('/', 1)[0]}/{item_id}"
    put(out, "title", src, "title", text, where, ctx, required=True)
    put(out, "optional", src, "optional", boolean, where, ctx)
    put(out, "minutes", src, "minutes", integer, where, ctx)
    put(out, "summary", src, "summary", text, where, ctx)

    def exercises(required: bool) -> None:
        raw = src.get("exercises")
        if raw is None and not required:
            return
        if not isinstance(raw, (list, tuple)) or (required and not raw):
            ctx.error(where, "needs a list of exercises")
            return
        converted = []
        for ex in raw:
            ex_id = ex.get("id") if isinstance(ex, dict) else None
            converted.append(exercise(ex, f"{where}/{ex_id}", ctx, verify, f"{item_id}/{ex_id}"))
        out["exercises"] = converted
        unique(out["exercises"], "id", f"{where}.exercises", ctx)

    if kind in ("lesson", "testout"):
        exercises(required=True)
    if kind == "testout":
        # The form passes only with this many of its questions right too (the `<id>-questions` quiz).
        put(out, "questionsToPass", src, "questions_to_pass", integer, where, ctx)
    elif kind == "quiz":
        raw = src.get("questions")
        if not isinstance(raw, (list, tuple)) or not raw:
            ctx.error(where, "needs a list of questions")
        else:
            out["questions"] = [question(q, i, f"{where}/q{i}", ctx, verify, item_id) for i, q in enumerate(raw, 1)]
            unique(out["questions"], "id", f"{where}.questions", ctx)
    elif kind == "project":
        put(out, "intro", src, "intro", text, where, ctx)
        # The project's id and title are its exercise id and title too.
        exercise_fields(src, where, ctx, verify, item_id, out)
    elif kind == "challenge":
        put(out, "level", src, "level", one_of(("core", "advanced")), where, ctx)
        put(out, "variantOf", src, "variant_of", slug, where, ctx)
        exercise_fields(src, where, ctx, verify, item_id, out)
    elif kind == "article":
        put(out, "body", src, "body", text, where, ctx, required=True)
        put(out, "examples", src, "examples", list_of(example), where, ctx)
        exercises(required=False)
    elif kind == "cheatsheet":
        put(out, "entries", src, "entries", list_of(cheatsheet_entry), where, ctx, required=True)

    if not exercise_like:
        sidecar: dict = {}
        put(sidecar, "introduces", src, "introduces", token_list, where, ctx)
        put(sidecar, "notes", src, "notes", text, where, ctx)
        if sidecar:
            verify["items"][item_id] = sidecar
    return out


def unique(rows: list[dict], key: str, where: str, ctx: Ctx) -> None:
    seen: set = set()
    for row in rows:
        value = row.get(key)
        if value in seen:
            ctx.error(where, f"duplicate {key} {value!r}")
        seen.add(value)


def glossary_entry(value: Any, where: str, ctx: Ctx) -> dict:
    value = as_dict(value, where, ctx)
    unknown_keys(value, {"term", "aliases", "plain", "example"}, where, ctx)
    out: dict = {}
    put(out, "term", value, "term", text, where, ctx, required=True)
    put(out, "aliases", value, "aliases", str_list, where, ctx)
    put(out, "plain", value, "plain", text, where, ctx, required=True)
    put(out, "example", value, "example", text, where, ctx)
    return out


UNIT_KEYS = ["id", "order", "title", "subtitle", "published", "martu_intro", "goals", "campaign_links"]
UNIT_HARNESS_ONLY = {"notes"}

# ---------------------------------------------------------------------------------------------
# Loading and exporting
# ---------------------------------------------------------------------------------------------


def prototype_files(dirs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for folder in dirs:
        if folder.is_dir():
            files.extend(sorted(folder.glob(FILE_GLOB), key=lambda f: (f.name.split("_")[0], f.name)))
    return files


def load(path: Path) -> dict:
    sys.path.insert(0, str(path.parent))
    try:
        return runpy.run_path(str(path), run_name=f"prototype_{path.stem}")
    finally:
        sys.path.pop(0)


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def ts_ident(unit_id: str) -> str:
    return "unit_" + re.sub(r"[^A-Za-z0-9]", "_", unit_id)


def render_ts(unit_ids: list[str], content_dir: Path, ts_path: Path) -> str:
    lines = [
        "// GENERATED by scripts/course/export_prototypes.py -- do not edit by hand.",
        "// Run `npm run course:export` to regenerate (CI fails if this file is stale).",
    ]
    for unit_id in unit_ids:
        target = os.path.relpath(content_dir / "units" / f"{unit_id}.json", ts_path.parent).replace(os.sep, "/")
        if not target.startswith("."):
            target = f"./{target}"
        lines.append(f'import {ts_ident(unit_id)} from "{target}";')
    lines.append("")
    lines.append("/** Every content/courses/intro-python/units/*.json in course order (unpublished ones too). Parse with unitSchema. */")
    if unit_ids:
        lines.append("export const rawUnits: unknown[] = [")
        lines.extend(f"  {ts_ident(unit_id)}," for unit_id in unit_ids)
        lines.append("];")
    else:
        lines.append("export const rawUnits: unknown[] = [];")
    return "\n".join(lines) + "\n"


def export(sources: list[Path], content_dir: Path, ts_path: Path, root: Path, ctx: Ctx) -> dict[Path, str]:
    """Return {output path: file text} for every generated file."""
    groups: dict[str, dict] = {}
    glossary: dict[str, tuple[dict, str]] = {}
    for path in prototype_files(sources):
        shown = path.relative_to(root) if path.is_relative_to(root) else path
        try:
            module = load(path)
        except Exception as exc:  # noqa: BLE001 -- report any authoring mistake with its file name
            ctx.error(str(shown), f"could not load: {type(exc).__name__}: {exc}")
            continue
        unit, items = module.get("UNIT"), module.get("ITEMS")
        if not isinstance(unit, dict) or not isinstance(items, (list, tuple)):
            ctx.error(str(shown), "needs UNIT = dict(...) and ITEMS = [...]")
            continue
        unit_id = unit.get("id")
        number = re.match(r"u(\d\d)", path.name).group(1)  # type: ignore[union-attr]
        group = groups.setdefault(str(unit_id), {"unit": {}, "items": [], "files": [], "numbers": set()})
        group["files"].append(str(shown))
        group["numbers"].add(number)
        for key, value in unit.items():
            if key in group["unit"] and group["unit"][key] != value:
                ctx.error(str(shown), f"UNIT[{key!r}] differs from an earlier part of unit {unit_id!r}")
            group["unit"].setdefault(key, value)
        group["items"].extend((raw, str(shown)) for raw in items)
        for i, entry in enumerate(module.get("GLOSSARY") or []):
            converted = glossary_entry(entry, f"{shown}: GLOSSARY[{i}]", ctx)
            term = str(converted.get("term", "")).strip()
            key = term.lower()
            if key in glossary:
                if glossary[key][0] != converted:
                    ctx.warn(str(shown), f"glossary term {term!r} is also defined in {glossary[key][1]}; keeping that one")
            else:
                glossary[key] = (converted, str(shown))

    outputs: dict[Path, str] = {}
    units: list[tuple[int, str, str]] = []
    for unit_id, group in groups.items():
        where = group["files"][0]
        if len(group["numbers"]) > 1:
            ctx.error(where, f"unit id {unit_id!r} is used by more than one unit number: {', '.join(group['files'])}")
        src = group["unit"]
        unknown_keys(src, set(UNIT_KEYS) | UNIT_HARNESS_ONLY, f"{where}: UNIT", ctx)
        if unit_id in RESERVED_UNIT_IDS:
            ctx.error(where, f"unit id {unit_id!r} collides with a course page; pick another")
        verify: dict = {"unit": unit_id}
        if src.get("notes"):
            verify["notes"] = text(src["notes"], f"{where}: UNIT.notes", ctx)
        verify.update(items={}, exercises={}, questions={})
        out: dict = {}
        put(out, "id", src, "id", slug, f"{where}: UNIT", ctx, required=True)
        put(out, "order", src, "order", integer, f"{where}: UNIT", ctx, required=True)
        put(out, "title", src, "title", text, f"{where}: UNIT", ctx, required=True)
        put(out, "subtitle", src, "subtitle", text, f"{where}: UNIT", ctx)
        out["published"] = boolean(src.get("published", False), f"{where}: UNIT.published", ctx)
        put(out, "martuIntro", src, "martu_intro", text, f"{where}: UNIT", ctx, required=True)
        put(out, "goals", src, "goals", list_of(text), f"{where}: UNIT", ctx, required=True)
        put(out, "campaignLinks", src, "campaign_links", str_list, f"{where}: UNIT", ctx)
        out["items"] = [item(raw, f"{shown}: {unit_id}/{i}", ctx, verify) for i, (raw, shown) in enumerate(group["items"])]
        if not out["items"]:
            ctx.error(where, "the unit has no ITEMS")
        unique(out["items"], "id", f"{unit_id}.items", ctx)
        for form in [entry for entry in out["items"] if entry.get("kind") == "testout" and "questionsToPass" in entry]:
            quiz = next((entry for entry in out["items"] if entry.get("kind") == "quiz" and entry.get("id") == f"{form['id']}-questions"), None)
            if quiz is None:
                ctx.error(f"{unit_id}/{form['id']}", f"questions_to_pass needs a quiz with the id {form['id']}-questions")
            elif not 1 <= form["questionsToPass"] <= len(quiz.get("questions", [])):
                ctx.error(f"{unit_id}/{form['id']}", f"questions_to_pass is {form['questionsToPass']}, but "
                          f"{quiz['id']} has {len(quiz.get('questions', []))} questions")
        outputs[content_dir / "units" / f"{unit_id}.json"] = render_json(out)
        outputs[content_dir / "units" / f"{unit_id}.verify.json"] = render_json(verify)
        units.append((out.get("order", 0), group["files"][0], unit_id))

    units.sort()
    for (order_a, file_a, id_a), (order_b, file_b, id_b) in zip(units, units[1:]):
        if order_a == order_b:
            ctx.error(file_b, f"unit {id_b!r} has the same order ({order_b}) as unit {id_a!r} in {file_a}")
    entries = [entry for entry, _ in sorted(glossary.values(), key=lambda pair: str(pair[0].get("term", "")).lower())]
    # A [[link]] resolves by term or alias, so no name may belong to two entries (even from different files).
    owners: dict[str, str] = {}
    for entry, shown in glossary.values():
        for name in [entry.get("term", ""), *(entry.get("aliases") or [])]:
            key = str(name).strip().lower()
            if key in owners and owners[key] != entry.get("term"):
                ctx.error(shown, f"glossary name {name!r} of {entry.get('term')!r} is already a term or alias of {owners[key]!r}")
            owners.setdefault(key, str(entry.get("term")))
    outputs[content_dir / "glossary.json"] = render_json(entries)
    outputs[ts_path] = render_ts([unit_id for _, _, unit_id in units], content_dir, ts_path)
    return outputs


def generated_unit_files(content_dir: Path) -> set[Path]:
    folder = content_dir / "units"
    return set(folder.glob("*.json")) if folder.is_dir() else set()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Export Intro to Python prototypes to the site's JSON.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--src", type=Path, action="append", default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="fail if the committed output is stale")
    parser.add_argument("--sample-only", action="store_true", help="only read scripts/course/sample")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if args.sample_only and args.out is None:
        print("--sample-only needs --out DIR (it must not replace the committed course).", file=sys.stderr)
        return 2
    if args.check and args.out is not None:
        print("--check compares against the committed files; do not combine it with --out.", file=sys.stderr)
        return 2
    if args.src:
        sources = [s if s.is_absolute() else root / s for s in args.src]
    elif args.sample_only:
        sources = [root / SAMPLE_REL]
    else:
        sources = [root / PROTOTYPE_REL, root / SAMPLE_REL]
    if args.out is not None:
        content_dir = args.out.resolve()
        ts_path = content_dir / "units.generated.ts"
    else:
        content_dir = root / CONTENT_REL
        ts_path = root / TS_REL

    ctx = Ctx()
    outputs = export(sources, content_dir, ts_path, root, ctx)
    for line in ctx.warnings:
        print("WARN ", line)
    if ctx.errors:
        for line in ctx.errors:
            print("ERROR", line)
        print(f"\nExport failed with {len(ctx.errors)} error(s); nothing was written.", file=sys.stderr)
        return 1

    def rel(path: Path) -> str:
        return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)

    unit_count = sum(1 for p in outputs if p.name.endswith(".json") and not p.name.endswith(".verify.json") and p.parent.name == "units")
    if args.check:
        changed = [p for p, body in outputs.items() if p.exists() and p.read_text(encoding="utf8") != body]
        missing = [p for p in outputs if not p.exists()]
        extra = sorted(generated_unit_files(content_dir) - set(outputs))
        if changed or missing or extra:
            print("Intro to Python content is out of date: the prototypes and the exported JSON do not match.")
            for label, paths in (("changed", changed), ("missing", missing), ("not exported by any prototype", extra)):
                for path in sorted(paths):
                    print(f"  {label}: {rel(path)}")
            print("Run `npm run course:export` (python3 scripts/course/export_prototypes.py) and commit the result.")
            return 1
        print(f"Intro to Python content is up to date ({unit_count} units).")
        return 0

    written = 0
    for path, body in outputs.items():
        if path.exists() and path.read_text(encoding="utf8") == body:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf8")
        written += 1
    removed = sorted(generated_unit_files(content_dir) - set(outputs))
    for path in removed:
        path.unlink()
    print(
        f"Exported {unit_count} unit(s) to {rel(content_dir)} "
        f"({written} file(s) written, {len(removed)} stale file(s) removed)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
