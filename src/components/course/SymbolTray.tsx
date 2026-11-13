"use client";

import type { PointerEvent as ReactPointerEvent, MouseEvent as ReactMouseEvent } from "react";

/** The symbols that are hard to find on a phone or tablet keyboard, with what a screen reader says. */
export const TRAY_SYMBOLS: { text: string; name: string }[] = [
  { text: '"', name: "double quote" },
  { text: "'", name: "single quote" },
  { text: "(", name: "open bracket" },
  { text: ")", name: "close bracket" },
  { text: ":", name: "colon" },
  { text: "=", name: "equals" },
  { text: "+", name: "plus" },
  { text: "[", name: "open square bracket" },
  { text: "]", name: "close square bracket" },
  { text: "{", name: "open curly bracket" },
  { text: "}", name: "close curly bracket" },
  { text: "#", name: "hash" },
  { text: "_", name: "underscore" },
];

/** Keep the editor focused (and the on-screen keyboard up) while a tray button is pressed. */
function keepFocus(event: ReactPointerEvent | ReactMouseEvent) {
  event.preventDefault();
}

/**
 * A row of symbol buttons under the editor. CSS shows it only on touch screens and narrow windows
 * (course-exercise.css), where typing " ( ) : = is slow. Each press types the symbol at the cursor.
 */
export function SymbolTray({ onInsert, names = [] }: { onInsert: (text: string) => void; names?: readonly string[] }) {
  return (
    <div className="ex-symbols" role="group" aria-label="Symbols and names to type" data-testid="symbol-tray">
      {TRAY_SYMBOLS.map((symbol) => (
        <button
          key={symbol.text}
          type="button"
          className="ex-symbol"
          data-testid={`symbol-${symbol.name.replace(/\s+/g, "-")}`}
          aria-label={`Type ${symbol.name}`}
          onPointerDown={keepFocus}
          onMouseDown={keepFocus}
          onClick={() => onInsert(symbol.text)}
        >
          <code aria-hidden="true">{symbol.text}</code>
        </button>
      ))}
      {names.map((name) => (
        <button
          key={`name-${name}`}
          type="button"
          className="ex-symbol is-name"
          data-testid={`tray-name-${name}`}
          aria-label={`Type ${name}`}
          onPointerDown={keepFocus}
          onMouseDown={keepFocus}
          onClick={() => onInsert(name)}
        >
          <code aria-hidden="true">{name}</code>
        </button>
      ))}
    </div>
  );
}
