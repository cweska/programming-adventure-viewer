"use client";

import { python } from "@codemirror/lang-python";
import { EditorView } from "@codemirror/view";
import CodeMirror from "@uiw/react-codemirror";
import { plainDarkTheme, pythonHighlighting } from "./editor-theme";

export function PythonEditor({
  code,
  onChange,
}: {
  code: string;
  onChange: (value: string) => void;
}) {
  return (
    <div className="editor-shell" data-testid="editor">
      <CodeMirror
        value={code}
        height="280px"
        theme={plainDarkTheme}
        basicSetup={{
          lineNumbers: true,
          foldGutter: false,
          syntaxHighlighting: false,
          closeBrackets: false,
          closeBracketsKeymap: false,
          tabSize: 4,
        }}
        extensions={[
          python(),
          pythonHighlighting,
          EditorView.contentAttributes.of({ "aria-label": "Python editor" }),
        ]}
        onChange={onChange}
      />
    </div>
  );
}
