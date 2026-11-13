"use client";

import type { ReactNode } from "react";
import type { GlossaryEntry } from "../../lib/course/schema";
import { publicPath } from "../../lib/site";
import { Prose } from "./Prose";
import { ReadAloud } from "./ReadAloud";

/**
 * Mar'tu's portrait and a speech bubble holding course prose (with glossary words and read-aloud).
 * `light` hides the story lines ("Fewer words"). Extra content (buttons, links) goes in `children`.
 */
export function MarTu({
  text,
  glossary = [],
  light = false,
  heading,
  size = "large",
  children,
  testId = "martu-says",
}: {
  text: string;
  glossary?: readonly GlossaryEntry[];
  light?: boolean;
  heading?: string;
  size?: "large" | "small";
  children?: ReactNode;
  testId?: string;
}) {
  return (
    <section className={`martu martu-${size}`} data-testid={testId} aria-label={heading ?? "Mar'tu says"}>
      <img className="martu-portrait" src={publicPath("/sprites/mar-tu.svg")} alt="" aria-hidden="true" />
      <div className="martu-bubble">
        <p className="martu-name">
          {heading ?? "Mar'tu"}
        </p>
        <Prose text={text} glossary={glossary} light={light} className="martu-text" />
        <div className="martu-actions">
          <ReadAloud text={text} />
          {children}
        </div>
      </div>
    </section>
  );
}
