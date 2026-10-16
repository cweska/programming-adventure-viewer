"use client";

import { useState } from "react";
import { parseAuthorModelOutput } from "../../lib/authoring/parse";
import type { Activity, Beat, Module } from "../../lib/lesson/schema";
import { isStaticExport, pagePath } from "../../lib/site";

const PREVIEW_STORAGE_KEY = "emberkeep-preview";

export default function AuthorPage() {
  const [prompt, setPrompt] = useState("");
  const [modelOutput, setModelOutput] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [draft, setDraft] = useState<Module | null>(null);
  const [busy, setBusy] = useState(false);

  function applyParsed(result: ReturnType<typeof parseAuthorModelOutput>) {
    if (!result.ok) {
      setError(result.error);
      setDraft(null);
      return;
    }
    setError("");
    setDraft(result.module);
    setStatus("Draft matches the lesson schema.");
  }

  function checkDraft() {
    applyParsed(parseAuthorModelOutput(modelOutput, prompt));
  }

  async function generate() {
    if (isStaticExport) {
      setError("AI drafting needs the local app.");
      setStatus("");
      return;
    }
    setBusy(true);
    setStatus("");
    try {
      const response = await fetch("/api/author", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const result = (await response.json()) as ReturnType<typeof parseAuthorModelOutput> & {
        error?: string;
        prompt?: string;
      };
      if (!result.ok) {
        setError(result.error ?? "The draft could not be created.");
        return;
      }
      setError("");
      setDraft(result.module);
      setModelOutput(JSON.stringify(result.module, null, 2));
      setStatus("Draft matches the lesson schema.");
    } catch {
      setError("The model could not be reached.");
    } finally {
      setBusy(false);
    }
  }

  function updateBeat(lessonId: string, beatId: string, patch: Partial<Beat>) {
    setDraft((current) => {
      if (!current) return current;
      return {
        ...current,
        lessons: current.lessons.map((lesson) => {
          if (lesson.id !== lessonId) return lesson;
          return {
            ...lesson,
            beats: lesson.beats.map((beat) => (beat.id === beatId ? { ...beat, ...patch } : beat)),
          };
        }),
      };
    });
  }

  function updateActivity(lessonId: string, beatId: string, patch: Partial<Activity>) {
    setDraft((current) => {
      if (!current) return current;
      return {
        ...current,
        lessons: current.lessons.map((lesson) => {
          if (lesson.id !== lessonId) return lesson;
          return {
            ...lesson,
            beats: lesson.beats.map((beat) => {
              if (beat.id !== beatId || !beat.activity) return beat;
              return { ...beat, activity: { ...beat.activity, ...patch } };
            }),
          };
        }),
      };
    });
  }

  async function saveDraft() {
    if (!draft) return;
    setBusy(true);
    try {
      const response = await fetch("/api/modules", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draft),
      });
      const body = (await response.json()) as { error?: string; module?: Module };
      if (!response.ok || !body.module) {
        setError(body.error ?? "The draft could not be saved.");
        return;
      }
      setDraft(body.module);
      setError("");
      setStatus("Draft saved.");
    } catch {
      setError("The draft could not be saved.");
    } finally {
      setBusy(false);
    }
  }

  async function publish(lessonId: string) {
    if (!draft) return;
    setBusy(true);
    try {
      const saved = await fetch("/api/modules", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draft),
      });
      if (!saved.ok) {
        const body = (await saved.json()) as { error?: string };
        setError(body.error ?? "Save the draft before publishing.");
        return;
      }
      const response = await fetch("/api/modules/publish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ moduleId: draft.id, lessonId }),
      });
      const body = (await response.json()) as { error?: string; module?: Module };
      if (!response.ok || !body.module) {
        setError(body.error ?? "Could not publish that lesson.");
        return;
      }
      setDraft(body.module);
      setError("");
      setStatus("Lesson published.");
    } catch {
      setError("Could not publish that lesson.");
    } finally {
      setBusy(false);
    }
  }

  function openPreview() {
    if (!draft) return;
    sessionStorage.setItem(PREVIEW_STORAGE_KEY, JSON.stringify(draft));
    window.location.href = `${pagePath("/")}?preview=1`;
  }

  return (
    <main className="column">
      <section className="author-form">
        <h1>Author a lesson</h1>
        <p>Describe the scenarios, the challenges, and what done means. The language is Python.</p>
        <label>
          Lesson prompt
          <textarea
            aria-label="Lesson prompt"
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
          />
        </label>
        <label>
          Model output
          <textarea
            aria-label="Model output"
            value={modelOutput}
            onChange={(event) => setModelOutput(event.target.value)}
            placeholder="Paste model JSON here to check it without calling a model."
          />
        </label>
        <div className="toolbar">
          <button type="button" onClick={checkDraft}>
            Check draft
          </button>
          <button type="button" onClick={() => void generate()} disabled={busy}>
            Draft with AI
          </button>
        </div>
        {error ? (
          <p className="validation-error" data-testid="validation-error" role="alert">
            {error}
          </p>
        ) : null}
        {status ? <p data-testid="author-status">{status}</p> : null}
      </section>

      {draft
        ? draft.lessons.map((lesson) => (
            <section key={lesson.id} className="beat-edit">
              <h2>
                {lesson.title}{" "}
                <span>{lesson.published ? "Published" : "Draft"}</span>
              </h2>
              <div className="toolbar">
                <button type="button" onClick={() => void saveDraft()} disabled={busy}>
                  Save draft
                </button>
                <button type="button" onClick={() => void publish(lesson.id)} disabled={busy || lesson.published}>
                  {lesson.published ? "Published" : "Publish lesson"}
                </button>
                <button type="button" onClick={openPreview}>
                  Open preview
                </button>
              </div>
              {lesson.beats.map((beat) => (
                <div key={beat.id} className="check-edit">
                  <label>
                    Caption
                    <textarea
                      aria-label={`Caption for ${beat.id}`}
                      value={beat.scene.caption}
                      onChange={(event) =>
                        updateBeat(lesson.id, beat.id, {
                          scene: { ...beat.scene, caption: event.target.value },
                        })
                      }
                    />
                  </label>
                  <label>
                    Instructions
                    <textarea
                      aria-label={`Instructions for ${beat.id}`}
                      value={beat.instructions}
                      onChange={(event) => updateBeat(lesson.id, beat.id, { instructions: event.target.value })}
                    />
                  </label>
                  {beat.activity ? (
                    <>
                      <label>
                        Starter code
                        <textarea
                          aria-label={`Starter code for ${beat.id}`}
                          value={beat.activity.starterCode}
                          onChange={(event) =>
                            updateActivity(lesson.id, beat.id, { starterCode: event.target.value })
                          }
                        />
                      </label>
                      <label>
                        Pass feedback
                        <textarea
                          aria-label={`Pass feedback for ${beat.id}`}
                          value={beat.activity.passFeedback}
                          onChange={(event) =>
                            updateActivity(lesson.id, beat.id, { passFeedback: event.target.value })
                          }
                        />
                      </label>
                      <label>
                        Fail feedback
                        <textarea
                          aria-label={`Fail feedback for ${beat.id}`}
                          value={beat.activity.failFeedback}
                          onChange={(event) =>
                            updateActivity(lesson.id, beat.id, { failFeedback: event.target.value })
                          }
                        />
                      </label>
                      {beat.activity.checks.map((check, index) => (
                        <div key={`${beat.id}-${index}`} className="check-edit">
                          <label>
                            Check name
                            <input
                              aria-label={`Check name ${index + 1} for ${beat.id}`}
                              value={check.name}
                              onChange={(event) => {
                                const checks = beat.activity!.checks.map((item, itemIndex) =>
                                  itemIndex === index ? { ...item, name: event.target.value } : item,
                                );
                                updateActivity(lesson.id, beat.id, { checks });
                              }}
                            />
                          </label>
                          <label>
                            Check code
                            <textarea
                              aria-label={`Check code ${index + 1} for ${beat.id}`}
                              value={check.code}
                              onChange={(event) => {
                                const checks = beat.activity!.checks.map((item, itemIndex) =>
                                  itemIndex === index ? { ...item, code: event.target.value } : item,
                                );
                                updateActivity(lesson.id, beat.id, { checks });
                              }}
                            />
                          </label>
                        </div>
                      ))}
                    </>
                  ) : null}
                </div>
              ))}
            </section>
          ))
        : null}
    </main>
  );
}
