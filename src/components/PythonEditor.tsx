"use client";

import { python } from "@codemirror/lang-python";
import { EditorView } from "@codemirror/view";
import CodeMirror, { type ReactCodeMirrorRef } from "@uiw/react-codemirror";
import { useId, useImperativeHandle, useMemo, useRef, type Ref } from "react";
import { planInsert, type InsertTarget, type InsertText, type InsertWhere } from "./editor-insert";
import { plainDarkTheme, pythonHighlighting } from "./editor-theme";

/** What a page can do with the editor besides typing (course chips, symbol tray, Mar'tu's pick). */
export type PythonEditorHandle = {
  /**
   * Put text in the code and give the editor the keyboard back. `where` (editor-insert.ts) says how: at the
   * cursor (the default), never inside a `#` note, on a line of its own, or as a note above the line. Before the
   * student has ever clicked into the editor, the text goes on a new line at the end instead of the top (a note
   * goes at the top), unless a `target` says where the step's line goes. `text` may be a function of what is before
   * it on its line. False when not mounted.
   */
  insert: (text: InsertText, where?: InsertWhere, target?: InsertTarget) => boolean;
  /** The text on the cursor's line before the cursor, and whether the student has placed the cursor. */
  cursorContext: () => { lineBefore: string; placed: boolean } | null;
  focus: () => void;
};

/** A focus this soon after a pointer press came from a click or tap. */
const POINTER_FOCUS_MS = 1_000;
/** Tab-moves-on lasts until a key is typed (CodeMirror needs a time limit: one that never runs out in class). */
const TAB_MOVES_ON_MS = 6 * 60 * 60 * 1_000;

/** Keys that do not count as typing in the editor (tabMovesOn stays on). */
const NOT_TYPING_KEYS = new Set(["Tab", "Escape", "Shift", "Control", "Alt", "Meta", "CapsLock", "Fn", "OS"]);

/** Visually hidden, still read by screen readers (inline so the campaign page needs no extra CSS). */
const SR_ONLY = {
  position: "absolute",
  width: 1,
  height: 1,
  padding: 0,
  margin: -1,
  overflow: "hidden",
  clip: "rect(0, 0, 0, 0)",
  whiteSpace: "nowrap",
  border: 0,
} as const;

export function PythonEditor({
  code,
  onChange,
  onBlur,
  describedBy,
  wrapLines = false,
  tabMovesOn = false,
  handleRef,
}: {
  code: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  /**
   * id of visible text that explains the editor's keys (Tab indents; Esc, then Tab, moves on). Without it,
   * the editor carries that sentence for screen readers itself, so nobody is trapped (WCAG 2.1.2).
   */
  describedBy?: string;
  /** Wrap long lines instead of scrolling sideways (narrow phone screens). */
  wrapLines?: boolean;
  /**
   * Keyboard arrival without a click: Tab and Shift+Tab move on (they do not indent) until the student types
   * a key in the editor. Tabbing through the page then never changes the code. A click or tap puts the cursor
   * in the code, so Tab indents straight away.
   */
  tabMovesOn?: boolean;
  handleRef?: Ref<PythonEditorHandle>;
}) {
  const ownHelpId = useId();
  const cmRef = useRef<ReactCodeMirrorRef>(null);
  const placed = useRef(false);
  const pointerAt = useRef(0);
  /** Keyboard arrival, and nothing typed since: Tab moves on (see tabMovesOn). */
  const untouched = useRef(false);
  // Read when the event fires, so the memoized extensions never call a stale handler.
  const onBlurRef = useRef(onBlur);
  onBlurRef.current = onBlur;
  const helpId = describedBy ?? `${ownHelpId}-keys`;

  useImperativeHandle(
    handleRef,
    () => ({
      insert(text: InsertText, where: InsertWhere = "cursor", target?: InsertTarget) {
        const view = cmRef.current?.view;
        if (!view) return false;
        const { from, to } = view.state.selection.main;
        const plan = planInsert(view.state.doc.toString(), { from, to }, placed.current, text, where, target);
        view.dispatch({
          changes: { from: plan.from, to: plan.to, insert: plan.insert },
          selection: { anchor: plan.anchor },
          scrollIntoView: true,
          userEvent: "input.type",
        });
        placed.current = true;
        view.focus();
        return true;
      },
      cursorContext() {
        const view = cmRef.current?.view;
        if (!view) return null;
        const head = view.state.selection.main.head;
        const line = view.state.doc.lineAt(head);
        return { lineBefore: line.text.slice(0, head - line.from), placed: placed.current };
      },
      focus() {
        cmRef.current?.view?.focus();
      },
    }),
    [],
  );

  const extensions = useMemo(() => {
    const attributes: Record<string, string> = { "aria-label": "Python editor", "aria-describedby": helpId };
    return [
      python(),
      pythonHighlighting,
      EditorView.contentAttributes.of(attributes),
      ...(wrapLines ? [EditorView.lineWrapping] : []),
      EditorView.domEventHandlers({
        pointerdown: (_event, view) => {
          pointerAt.current = Date.now();
          if (tabMovesOn) {
            untouched.current = false;
            view.setTabFocusMode(false);
          }
          return false;
        },
        focus: (_event, view) => {
          placed.current = true;
          // Arrived by keyboard (or a button handed the keyboard over): Tab moves on until a key is typed.
          // CodeMirror ends this mode by itself on the first key that is not Tab, Esc or a modifier.
          if (tabMovesOn && Date.now() - pointerAt.current > POINTER_FOCUS_MS) {
            untouched.current = true;
            view.setTabFocusMode(TAB_MOVES_ON_MS);
          }
          return false;
        },
        keydown: (event, view) => {
          if (!tabMovesOn || !untouched.current) return false;
          if (event.key === "Escape") {
            // CodeMirror shortens the mode to 2 seconds on Esc: nothing is typed yet, so keep it on.
            window.setTimeout(() => {
              if (untouched.current) view.setTabFocusMode(TAB_MOVES_ON_MS);
            }, 0);
          } else if (!NOT_TYPING_KEYS.has(event.key)) {
            untouched.current = false;
          }
          return false;
        },
        blur: () => {
          onBlurRef.current?.();
          return false;
        },
      }),
    ];
  }, [helpId, wrapLines, tabMovesOn]);

  return (
    <div className="editor-shell" data-testid="editor">
      {describedBy ? null : (
        <span id={helpId} style={SR_ONLY}>
          In the editor, Tab adds spaces. To leave the editor, press Esc, then Tab.
        </span>
      )}
      <CodeMirror
        ref={cmRef}
        value={code}
        minHeight="280px"
        theme={plainDarkTheme}
        basicSetup={{
          lineNumbers: true,
          foldGutter: false,
          syntaxHighlighting: false,
          closeBrackets: false,
          closeBracketsKeymap: false,
          highlightSelectionMatches: false,
          tabSize: 4,
        }}
        extensions={extensions}
        onChange={onChange}
      />
    </div>
  );
}
