import type { Module } from "./schema";

export function makeValidModule(): Module {
  return {
    id: "emberkeep",
    title: "Emberkeep",
    language: "python",
    lessons: [
      {
        id: "gate",
        title: "The Gate",
        published: true,
        beats: [
          {
            id: "arrive",
            instructions: "Read the gate, then continue.",
            scene: {
              caption: "The gate is shut.",
              images: [{ id: "road", src: "/scenes/gate-road.svg", alt: "The road to the gate" }],
            },
          },
          {
            id: "courtyard",
            instructions: "Define light_torch so the courtyard catches.",
            scene: {
              caption: "The courtyard is dark.",
              images: [{ id: "courtyard", src: "/scenes/courtyard.svg", alt: "A dark courtyard" }],
            },
            activity: {
              kind: "challenge",
              starterCode: "def light_torch(oil):\n    return 'dark'\n",
              passFeedback: "The torches catch.",
              failFeedback: "The sconces stay cold.",
              checks: [
                {
                  name: "oil lights the torch",
                  code: "assert light_torch('oil') == 'lit'",
                },
              ],
            },
          },
        ],
      },
      {
        id: "hall",
        title: "The Hall",
        published: false,
        beats: [
          {
            id: "answer",
            instructions: "Answer the gatekeeper with stage.say.",
            scene: {
              caption: "Who comes to Emberkeep?",
              images: [{ id: "keeper", src: "/scenes/gatekeeper.svg", alt: "The gatekeeper" }],
            },
            activity: {
              kind: "interactive",
              starterCode: "def answer(question):\n    stage.say('I seek the keep.')\n",
              passFeedback: "The gatekeeper nods.",
              failFeedback: "The gatekeeper waits.",
              checks: [{ name: "the hero answers", code: "answer('Who comes?')" }],
            },
          },
        ],
      },
    ],
  };
}
