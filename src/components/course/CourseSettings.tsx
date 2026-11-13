"use client";

import { useEffect, useId, useState } from "react";
import { progressIsSaving, setSettings, useCourseProgress, useProgressReady } from "../../lib/course/progress";

/** Help options: "Fewer words" (light mode) and read-aloud buttons. Saved with the course progress. */
export function CourseSettings({ className }: { className?: string }) {
  const { settings } = useCourseProgress();
  const ready = useProgressReady();
  const [canSpeak, setCanSpeak] = useState(true);
  const [saving, setSaving] = useState(true);
  const lightId = useId();
  const speakId = useId();

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
          <div className="course-setting">
            <input
              id={lightId}
              type="checkbox"
              checked={settings.light === true}
              disabled={!ready}
              onChange={(event) => setSettings({ light: event.target.checked })}
              data-testid="setting-light"
            />
            <label htmlFor={lightId}>
              <strong>Fewer words.</strong> Hide Mar&apos;tu&apos;s story lines and keep the steps.
            </label>
          </div>
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
