import { instructionBlocks, type InlinePart } from "../lib/lesson/instructions";

function Inline({ parts }: { parts: InlinePart[] }) {
  return (
    <>
      {parts.map((part, index) =>
        part.code ? (
          <code key={index} className="inline-code">
            {part.text}
          </code>
        ) : (
          <span key={index}>{part.text}</span>
        ),
      )}
    </>
  );
}

/** A part's instructions: one line per instruction, numbered steps, and code that looks like code. */
export function Instructions({ text }: { text: string }) {
  return (
    <div className="instruction-lines" data-testid="part-instructions">
      {instructionBlocks(text).map((block, index) =>
        block.kind === "line" ? (
          <p key={index}>
            <Inline parts={block.parts} />
          </p>
        ) : (
          <ol key={index} className="instruction-steps">
            {block.items.map((item, itemIndex) => (
              <li key={itemIndex}>
                <Inline parts={item} />
              </li>
            ))}
          </ol>
        ),
      )}
    </div>
  );
}
