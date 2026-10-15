import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { EditorView } from "@codemirror/view";
import { tags } from "@lezer/highlight";

export const plainDarkTheme = EditorView.theme(
  {
    "&": {
      backgroundColor: "#121417",
      color: "#f4f7fb",
    },
    ".cm-content": {
      caretColor: "#f4f7fb",
      fontFamily: 'var(--font-mono), "IBM Plex Mono", ui-monospace, monospace',
      fontSize: "15px",
      lineHeight: "1.55",
    },
    ".cm-gutters": {
      backgroundColor: "#121417",
      color: "#9aa3b2",
      border: "none",
    },
    ".cm-activeLineGutter": {
      backgroundColor: "#1c2128",
      color: "#f4f7fb",
    },
    ".cm-activeLine": {
      backgroundColor: "#1c2128",
    },
    ".cm-selectionBackground, &.cm-focused .cm-selectionBackground": {
      backgroundColor: "#2c4466",
    },
    "&.cm-focused": {
      outline: "none",
    },
  },
  { dark: true },
);

const pythonHighlight = HighlightStyle.define([
  { tag: tags.keyword, color: "#9ecbff" },
  { tag: tags.string, color: "#b6ebc6" },
  { tag: tags.comment, color: "#a9b3c2", fontStyle: "italic" },
  { tag: tags.number, color: "#d7e4ff" },
  { tag: tags.function(tags.variableName), color: "#d7e4ff" },
  { tag: tags.definition(tags.variableName), color: "#f4f7fb" },
  { tag: tags.operator, color: "#f4f7fb" },
  { tag: tags.punctuation, color: "#f4f7fb" },
]);

export const pythonHighlighting = syntaxHighlighting(pythonHighlight);
