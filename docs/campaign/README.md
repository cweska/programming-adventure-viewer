# Campaign modules

Each day of the campaign is one **module** that students pick on the home page. A module is a list of **parts**. There are three kinds of part:

| Kind | What students see | How it is marked in JSON |
| --- | --- | --- |
| Story | Scene art and a description box. The editor is hidden so the table can role-play. | `"editor": "hidden"`, no `board`, no `activity` |
| Programming | The game screen, the description box, and the Python editor. Passing the checks "builds" a game feature. | `board` + `activity` (with `unlocks`) |
| Gameplay | The game screen only. Continue unlocks when the party meets the goal. | `"editor": "hidden"`, `board` with a `goal` |

The game mechanics are already wired up in `src/lib/game/`. A programming part only switches a feature on (`movement`, `dialogue`, or `melee`) once its checks pass.

## Where things live

| Path | What it holds |
| --- | --- |
| `content/modules/<module>/module.json` | One module: its parts, captions, code, checks, and boards |
| `content/campaign/characters/` | Player characters made from the character sheets |
| `content/campaign/classes/` | Classes (Warrior, General, ...) and their base hit points |
| `content/campaign/npcs/` | People the party can talk to |
| `content/campaign/enemies/` | Things the party can fight |
| `content/campaign/maps/` | Game screens drawn as rows of letters |
| `content/campaign/dialogue/` | Conversation trees |
| `public/scenes/`, `public/sprites/` | Story art (960×540 SVG) and character tokens (64×64 SVG) |

New JSON files must also be imported in `src/lib/lesson/modules.ts` (modules) or `src/lib/campaign/registry.ts` (everything else). The site is a static export, so content is bundled at build time.

## From outline to JSON

| Outline line | JSON |
| --- | --- |
| Screen (a picture) | `scene.images` |
| Screen (the 2D game) | `board` |
| Description Box | `scene.caption` |
| Programming Editor/Console: Hidden | `"editor": "hidden"` |
| What students should do | `instructions` (shown under the title) |

A story part:

```json
{
  "id": "peaceful-night",
  "editor": "hidden",
  "instructions": "Read the scene. Press Continue when you are ready.",
  "scene": {
    "caption": "This night was a peaceful one...",
    "images": [{ "id": "hills", "src": "/scenes/leyline-hills-night.svg", "alt": "Grassy hills at night" }]
  }
}
```

A programming part that builds movement (see Part 4 of `leylines-awaken`):

```json
{
  "id": "program-movement",
  "instructions": "...",
  "scene": { "caption": "...", "images": [] },
  "board": { "map": "moonlit-hills", "party": ["gearshift", "oogrish"], "partyStart": [{ "x": 3, "y": 5 }, { "x": 2, "y": 5 }], "features": [] },
  "activity": {
    "kind": "interactive",
    "starterCode": "def move_left():\n    pass\n",
    "passFeedback": "...",
    "failFeedback": "One sentence.",
    "unlocks": ["movement"],
    "checks": [{ "name": "move_left steps left", "code": "party._moves.clear()\nmove_left()\nassert party._moves == [\"left\"], 'move_left() should call party.move(\"left\").'" }]
  }
}
```

Student code can call `party.move("left" | "right" | "up" | "down")`. Every call the checks make is also played on the game screen, so a wrong direction is easy to see.

A gameplay part:

```json
{
  "id": "beat-the-flashover",
  "editor": "hidden",
  "instructions": "Use the arrow keys or W A S D to walk to the cabin door.",
  "scene": { "caption": "...", "images": [] },
  "board": {
    "map": "moonlit-hills",
    "party": ["gearshift", "oogrish"],
    "partyStart": [{ "x": 3, "y": 5 }, { "x": 2, "y": 5 }],
    "actors": [{ "id": "mar-tu", "kind": "npc", "ref": "mar-tu", "x": 12, "y": 4 }],
    "features": ["movement"],
    "goal": { "type": "reach", "x": 11, "y": 3, "label": "the cabin door" }
  }
}
```

### Board fields

- `map`: a map id from `content/campaign/maps/`. Columns are `x` (0 on the left) and rows are `y` (0 at the top).
- `party` and `partyStart`: character ids and their starting tiles. The first character leads.
- `actors`: NPCs (`"kind": "npc"`, with an optional `dialogue` id) and enemies (`"kind": "enemy"`).
- `features`: what already works on this screen. A campaign module may only list features that an earlier programming part unlocked. A test enforces this.
- `goal`: `reach` a tile, `talk` to an actor until the conversation ends, or `defeat` every enemy.
- `seed`: fixes the dice so a fight plays the same way every time.

### Maps

`rows` are strings of equal length, and `legend` maps each letter to a tile. Players can walk on `grass`, `flowers`, `path`, `floor`, `sand`, and `door`. They cannot walk through `tree`, `rock`, `fence`, `water`, `wall`, `roof`, or `window`.

### Dialogue

Each node has a `speaker` (an NPC or character id), `text`, and either `options` (up to 9, each with `next`) or a `next`. A `next` of `null` ends the conversation.

## Rules the game uses

- Ability modifier = (score − 10) ÷ 2, rounded down.
- Hit points = class base HP + CON modifier.
- Defense = 10 + DEX modifier + armor bonus.
- Speed (tiles per turn) = 4 + half the ATH modifier, rounded down.
- Initiative = d20 + DEX modifier.
- Attack = d20 + STR modifier + 2. It hits when the total is at least the target's Defense. A natural 20 always hits and rolls the damage dice twice; a natural 1 always misses.
- Damage = weapon die + STR modifier, at least 1.

The combat log prints every roll (for example, "rolls 14 + 5 = 19 vs Defense 11"). Students can check the maths.

## Adding a character from a character sheet

1. **Never copy the student's name.** The character schema has no field for it and rejects unknown fields. `*.docx` files are ignored by git, so sheets cannot be committed by accident.
2. Copy the sheet into `content/campaign/characters/<id>.json`. Fill in anything left blank using the teacher's notes, and record what you filled in in `docs/campaign/characters.md`.
3. Use an existing class or add one in `content/campaign/classes/`.
4. Draw a 64×64 SVG token in `public/sprites/`.
5. Import the file in `src/lib/campaign/registry.ts`.

## The teacher practice yard

The **Training Grounds** module is unpublished, so students never see it. Open it from the Classroom page ("Open the practice yard"). It has a movement part, a dialogue part, and a melee fight. It is the place to try mechanics before they appear in the campaign. Nothing in it is saved.

## Tests

- `npm test` runs the unit tests. They cover movement, input, dialogue, combat maths, and every map, board, goal, and dialogue. They also run each module's reference Python against the same `party` object the browser uses, and the privacy checks.
- `npm run build && npm run test:e2e` plays the real site in Chromium: it walks the party with arrows and WASD, talks with number keys, and wins a sparring fight.
- GitHub Actions runs all of these on every push, then checks the GitHub Pages static export.
