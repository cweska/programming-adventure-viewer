"use client";

import { python } from "@codemirror/lang-python";
import { EditorView } from "@codemirror/view";
import CodeMirror, { type ReactCodeMirrorRef } from "@uiw/react-codemirror";
import { useId, useImperativeHandle, useMemo, useRef, type Ref } from "react";
import { plainDarkTheme, pythonHighlighting } from "./editor-theme";

/** What a page can do with the editor besides typing (course chips, symbol tray, Mar'tu's pick). */
export type PythonEditorHandle = {
  /**
   * Put text at the cursor (replacing a selection) and give the editor the keyboard back. Before the student
   * has ever clicked into the editor, the text goes at the end instead of the top. False when not mounted.
   */
  insert: (text: string) => boolean;
  /** The text on the cursor's line before the cursor, and whether the student has placed the cursor. */
  cursorContext: () => { lineBefore: string; placed: boolean } | null;
  focus: () => void;
};

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
  handleRef?: Ref<PythonEditorHandle>;
}) {
  const ownHelpId = useId();
  const cmRef = useRef<ReactCodeMirrorRef>(null);
  const placed = useRef(false);
  // Read when the event fires, so the memoized extensions never call a stale handler.
  const onBlurRef = useRef(onBlur);
  onBlurRef.current = onBlur;
  const helpId = describedBy ?? `${ownHelpId}-keys`;

  useImperativeHandle(
    handleRef,
    () => ({
      insert(text: string) {
        const view = cmRef.current?.view;
        if (!view) return false;
        const end = view.state.doc.length;
        let { from, to } = placed.current ? view.state.selection.main : { from: end, to: end };
        let insert = text;
        if (!placed.current && end > 0 && view.state.doc.sliceString(end - 1, end) !== "\n") insert = `\n${text}`;
        from = Math.max(0, Math.min(from, end));
        to = Math.max(from, Math.min(to, end));
        view.dispatch({
          changes: { from, to, insert },
          selection: { anchor: from + insert.length },
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
        focus: () => {
          placed.current = true;
          return false;
        },
        blur: () => {
          onBlurRef.current?.();
          return false;
        },
      }),
    ];
  }, [helpId, wrapLines]);

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
