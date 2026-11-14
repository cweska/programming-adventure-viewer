/** Pure helpers for <CardSort> (client-safe, no React). */

export type CardSortData = { groups: string[]; cards: { text: string; group: number }[]; explain: string };

/** For each card: is the student's pick its group? An unpicked card is not right. */
export function cardSortMarks(sort: CardSortData, picks: readonly (number | null)[]): boolean[] {
  return sort.cards.map((card, index) => picks[index] === card.group);
}
