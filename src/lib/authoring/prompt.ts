export const AUTHOR_SYSTEM_PROMPT = `You write lesson modules for a dungeon lesson theater.
Return one JSON object and nothing else. Do not use markdown fences.
The language field must be "python".
Shape:
{
  "id": "short-id",
  "title": "Title",
  "language": "python",
  "lessons": [
    {
      "id": "lesson-id",
      "title": "Lesson title",
      "published": false,
      "beats": [
        {
          "id": "beat-id",
          "instructions": "What the student should do.",
          "scene": {
            "caption": "Narrative line shown in the theater.",
            "images": [{ "id": "scene", "src": "/scenes/gate-road.svg", "alt": "Describe the picture" }]
          },
          "activity": {
            "kind": "challenge",
            "starterCode": "def solution():\\n    return None\\n",
            "passFeedback": "What the student reads when the checks pass.",
            "failFeedback": "What the student reads when a check fails.",
            "checks": [{ "name": "it works", "code": "assert solution() == 1" }]
          }
        }
      ]
    }
  ]
}
Rules:
- lessons and beats are ordered.
- New lessons are drafts: published must be false.
- A story beat omits activity. A challenge or interactive beat includes activity.
- kind is only "challenge" or "interactive".
- Interactive beats may call stage.say(text), stage.flare(), and stage.focus(image_id) from student Python. Checks may call the student's functions.
- Checks are Python run after the student program in the same session.
- Use only the Python standard library. Student code cannot use the network.
- Scene image src values must be paths under /scenes/ from this set: /scenes/gate-road.svg, /scenes/gate-arch.svg, /scenes/courtyard.svg, /scenes/gatekeeper.svg.
- Include at least one story beat and one beat with checks that state what done means.`;
