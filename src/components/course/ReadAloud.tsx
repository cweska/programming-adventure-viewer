"use client";

import { useEffect, useRef, useState } from "react";
import { useCourseProgress } from "../../lib/course/progress";
import { speakableText } from "./prose-format";

function speechSupported(): boolean {
  try {
    return typeof window !== "undefined" && "speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined";
  } catch {
    return false;
  }
}

/** Chrome stops long utterances part way, so speak a few sentences at a time. */
export function speechChunks(text: string, size = 220): string[] {
  const sentences = text.split(/(?<=[.!?])\s+/).filter((sentence) => sentence.trim());
  const chunks: string[] = [];
  for (const sentence of sentences) {
    const last = chunks.at(-1);
    if (last !== undefined && last.length + sentence.length + 1 <= size) chunks[chunks.length - 1] = `${last} ${sentence}`;
    else chunks.push(sentence);
  }
  return chunks;
}

/**
 * A "Read aloud" button for some course prose. It only shows when the browser can speak and the student
 * turned read-aloud on in Help options (or `always` is set).
 */
export function ReadAloud({
  text,
  label = "Read aloud",
  always = false,
  testId = "read-aloud",
}: {
  text: string;
  label?: string;
  always?: boolean;
  testId?: string;
}) {
  const { settings } = useCourseProgress();
  const [supported, setSupported] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const ours = useRef(false);

  useEffect(() => {
    setSupported(speechSupported());
    return () => {
      if (ours.current) {
        try {
          window.speechSynthesis.cancel();
        } catch {
          // nothing to stop
        }
      }
    };
  }, []);

  if (!supported || !(always || settings.readAloud)) return null;

  const stop = () => {
    try {
      window.speechSynthesis.cancel();
    } catch {
      // nothing to stop
    }
    ours.current = false;
    setSpeaking(false);
  };

  const start = () => {
    const chunks = speechChunks(speakableText(text));
    if (chunks.length === 0) return;
    try {
      window.speechSynthesis.cancel();
      chunks.forEach((chunk, index) => {
        const utterance = new SpeechSynthesisUtterance(chunk);
        utterance.rate = 0.92;
        utterance.lang = "en-US";
        if (index === chunks.length - 1) {
          utterance.onend = () => {
            ours.current = false;
            setSpeaking(false);
          };
        }
        utterance.onerror = () => {
          ours.current = false;
          setSpeaking(false);
        };
        window.speechSynthesis.speak(utterance);
      });
      ours.current = true;
      setSpeaking(true);
    } catch {
      setSpeaking(false);
    }
  };

  return (
    <button
      type="button"
      className="read-aloud"
      data-testid={testId}
      aria-pressed={speaking}
      onClick={speaking ? stop : start}
    >
      <span aria-hidden="true">{speaking ? "■" : "🔊"}</span> {speaking ? "Stop reading" : label}
    </button>
  );
}
