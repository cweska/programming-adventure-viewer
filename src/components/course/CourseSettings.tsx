"use client";

import Link from "next/link";
import { useEffect, useId, useRef, useState } from "react";
import {
  coursePreset,
  needsPlacement,
  presetForAnswer,
  progressIsSaving,
  setPreset,
  setSettings,
  useCourseProgress,
  useProgressReady,
  type CoursePreset,
  type PlacementAnswer,
} from "../../lib/course/progress";

const PRESETS: { value: CoursePreset; label: string; detail: string }[] = [
  {
    value: "more",
    label: "Show me more",
    detail: "Mar'tu's full explanations, with the example open.",
  },
  {
    value: "short",
    label: "Keep it short",
    detail: "The steps first. Explanations and examples are one tap away.",
  },
];

/**
 * Help options: "Show me more" / "Keep it short" (the preset, curriculum §2.3) and the read-aloud buttons.
 * Saved with the course progress. There is no badge anywhere that shows which preset is on.
 */
export function CourseSettings({ className }: { className?: string }) {
  const { settings } = useCourseProgress();
  const ready = useProgressReady();
  const [canSpeak, setCanSpeak] = useState(true);
  const [saving, setSaving] = useState(true);
  const groupId = useId();
  const speakId = useId();
  const preset = coursePreset(settings);

  useEffect(() => {
    try {
      setCanSpeak("speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined");
    } catch {
      setCanSpeak(false);
    }
    setSaving(progressIsSaving());
  }, []);

  return (
    <div className={["course-settings-wrap", className].filter(Boolean).join(" ")}>
      <details className="course-settings" data-testid="help-options">
        <summary>Help options</summary>
        <div className="course-settings-body">
          <fieldset className="course-preset" data-testid="setting-preset">
            <legend>How much should Mar&apos;tu explain?</legend>
            {PRESETS.map((option) => {
              const id = `${groupId}-${option.value}`;
              return (
                <div className="course-setting" key={option.value}>
                  <input
                    id={id}
                    type="radio"
                    name={groupId}
                    value={option.value}
                    checked={preset === option.value}
                    disabled={!ready}
                    onChange={() => setPreset(option.value)}
                    data-testid={`setting-preset-${option.value}`}
                  />
                  <label htmlFor={id}>
                    <strong>{option.label}.</strong> {option.detail}
                  </label>
                </div>
              );
            })}
          </fieldset>
          <div className="course-setting">
            <input
              id={speakId}
              type="checkbox"
              checked={settings.readAloud === true && canSpeak}
              disabled={!ready || !canSpeak}
              onChange={(event) => setSettings({ readAloud: event.target.checked })}
              data-testid="setting-read-aloud"
            />
            <label htmlFor={speakId}>
              <strong>Read aloud.</strong>{" "}
              {canSpeak ? "Show buttons that read Mar'tu's words out loud." : "This browser cannot read aloud."}
            </label>
          </div>
        </div>
      </details>
      {saving ? null : (
        <p className="course-settings-note" role="status" data-testid="progress-not-saving">
          This browser is not saving your progress. It will be lost when you close the tab.
        </p>
      )}
    </div>
  );
}

const ANSWERS: { answer: Exclude<PlacementAnswer, "skip">; label: string }[] = [
  { answer: "no", label: "No" },
  { answer: "a-little", label: "A little" },
  { answer: "yes", label: "Yes" },
];

/**
 * The one-time question on a first visit to the course map: "Have you typed code before?" (curriculum §2.3).
 * Every answer starts on "Show me more" (self-report can only add support); "Yes" is also offered the first
 * unit's Quick Check. It never sets anything else, and it shows only after hydration, when nothing has been
 * chosen or done yet in this browser.
 */
export function PlacementQuestion({ quickCheck }: { quickCheck?: { href: string; unitTitle: string } }) {
  const progress = useCourseProgress();
  const ready = useProgressReady();
  const [answered, setAnswered] = useState<PlacementAnswer | null>(null);
  const doneRef = useRef<HTMLDivElement>(null);
  const headingId = useId();

  useEffect(() => {
    // The buttons are gone after an answer: put the keyboard on the note that replaced them.
    if (answered) doneRef.current?.focus();
  }, [answered]);

  if (answered) {
    return (
      <div ref={doneRef} tabIndex={-1} className="course-placement-done" role="status" data-testid="placement-done">
        <p>
          Good. We start small. When you are stuck, Mar&apos;tu will offer help. You can change how much Mar&apos;tu
          explains any time, under Help options.
        </p>
        {answered === "yes" && quickCheck ? (
          <p data-testid="placement-quick-check">
            Already know some Python? Try the{" "}
            <Link href={quickCheck.href} data-testid="placement-quick-check-link">
              {quickCheck.unitTitle} Quick Check
            </Link>
            . Pass it and you can skip that unit&apos;s lessons. A miss costs nothing.
          </p>
        ) : null}
      </div>
    );
  }
  if (!ready || !needsPlacement(progress)) return null;

  const choose = (answer: PlacementAnswer) => {
    setPreset(presetForAnswer(answer));
    setAnswered(answer);
  };

  return (
    <section className="course-placement" aria-labelledby={headingId} data-testid="placement">
      <h2 id={headingId}>Have you typed code before?</h2>
      <p>Your answer only helps Mar&apos;tu choose where to start. You can change it any time. Every lesson stays open to you.</p>
      <div className="course-placement-actions" role="group" aria-labelledby={headingId}>
        {ANSWERS.map(({ answer, label }) => (
          <button key={answer} type="button" onClick={() => choose(answer)} data-testid={`placement-${answer}`}>
            {label}
          </button>
        ))}
        <button type="button" className="quiet-button" onClick={() => choose("skip")} data-testid="placement-skip">
          Skip
        </button>
      </div>
    </section>
  );
}
