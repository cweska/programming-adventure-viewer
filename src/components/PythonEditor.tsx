"use client";

import { python } from "@codemirror/lang-python";
import { EditorView } from "@codemirror/view";
import CodeMirror from "@uiw/react-codemirror";
import { plainDarkTheme, pythonHighlighting } from "./editor-theme";

export function PythonEditor({
  code,
  onChange,
  onBlur,
  describedBy,
  wrapLines = false,
}: {
  code: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  /** id of visible text that explains the editor's keys (Tab indents; Esc, then Tab, moves on). */
  describedBy?: string;
  /** Wrap long lines instead of scrolling sideways (narrow phone screens). */
  wrapLines?: boolean;
}) {
  const attributes: Record<string, string> = { "aria-label": "Python editor" };
  if (describedBy) attributes["aria-describedby"] = describedBy;
  return (
    <div className="editor-shell" data-testid="editor">
      <CodeMirror
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
        extensions={[
          python(),
          pythonHighlighting,
          EditorView.contentAttributes.of(attributes),
          ...(wrapLines ? [EditorView.lineWrapping] : []),
          EditorView.domEventHandlers({
            blur: () => {
              onBlur?.();
              return false;
            },
          }),
        ]}
        onChange={onChange}
      />
    </div>
  );
}
