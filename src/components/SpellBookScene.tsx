"use client";

import type { SceneImage, SpellBook } from "../lib/lesson/schema";
import { publicPath } from "../lib/site";

/**
 * The open spell book. When the part passes, the spell's name inks itself in
 * over the pencil sketch, then its cost and required affinity appear. The text
 * sits on the right-hand page of fil-spell-book.svg, so both share one 960x540 frame.
 */
export function SpellBookScene({
  image,
  spellBook,
  inked,
}: {
  image: SceneImage | undefined;
  spellBook: SpellBook;
  inked: boolean;
}) {
  return (
    <div className="spell-book" data-testid="spell-book" data-inked={inked ? "true" : "false"}>
      <svg className="spell-book-art" viewBox="0 0 960 540" role="img" aria-label={image?.alt ?? "A spell book"}>
        {image ? <image href={publicPath(image.src)} x={0} y={0} width={960} height={540} /> : null}
        {inked ? (
          <g className="ink" data-testid="spell-book-ink">
            <circle className="ink-sigil" cx={645} cy={200} r={78} />
            <text className="ink-line ink-title" x={645} y={330} textAnchor="middle">
              {spellBook.spell}
            </text>
            <text className="ink-line ink-stat ink-cost" x={645} y={380} textAnchor="middle">
              Mana cost: {spellBook.manaCost}
            </text>
            <text className="ink-line ink-stat ink-affinity" x={645} y={418} textAnchor="middle">
              Required affinity: {spellBook.requiredAffinity}
            </text>
          </g>
        ) : null}
      </svg>
      {inked ? (
        <p className="scene-success" data-testid="spell-book-success" role="status">
          {spellBook.success}
        </p>
      ) : null}
    </div>
  );
}
