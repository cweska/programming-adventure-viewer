"use client";

import { useEffect, useState } from "react";
import { createClassroomInBrowser, reportClassroomInBrowser } from "../../lib/classroom/local-store";
import { isStaticExport, pagePath } from "../../lib/site";

type ReportRow = {
  studentId: string;
  displayName: string;
  moduleId: string;
  lessonId: string;
  beatId: string;
  status: "in_progress" | "completed";
  completed: boolean;
};

type ClassroomSummary = {
  id: string;
  name: string;
  reportEmail: string;
  joinCode: string;
};

export default function ClassroomPage() {
  const [name, setName] = useState("");
  const [reportEmail, setReportEmail] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [lookup, setLookup] = useState("");
  const [classroom, setClassroom] = useState<ClassroomSummary | null>(null);
  const [rows, setRows] = useState<ReportRow[]>([]);
  const [error, setError] = useState("");

  async function loadReport(code: string) {
    const body = isStaticExport
      ? reportClassroomInBrowser(code)
      : await (async () => {
          const response = await fetch(`/api/classroom/report?code=${encodeURIComponent(code)}`);
          const payload = (await response.json()) as {
            error?: string;
            classroom?: ClassroomSummary;
            rows?: ReportRow[];
          };
          if (!response.ok) {
            return { error: payload.error ?? "Could not load that report." };
          }
          return payload;
        })();
    if (!body.classroom) {
      setError(body.error ?? "Could not load that report.");
      setRows([]);
      return;
    }
    setError("");
    setClassroom(body.classroom);
    setRows(body.rows ?? []);
  }

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get("code");
    if (code) {
      setLookup(code);
      void loadReport(code);
    }
  }, []);

  async function createClassroom(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    const body = isStaticExport
      ? createClassroomInBrowser({ name, reportEmail, joinCode })
      : await (async () => {
          const response = await fetch("/api/classroom", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, reportEmail, joinCode }),
          });
          const payload = (await response.json()) as { error?: string; classroom?: ClassroomSummary };
          if (!response.ok) {
            return { error: payload.error ?? "Could not create the classroom." };
          }
          return payload;
        })();
    if (!body.classroom) {
      setError(body.error ?? "Could not create the classroom.");
      return;
    }
    setClassroom(body.classroom);
    setLookup(body.classroom.joinCode);
    setRows([]);
    const url = `${pagePath("/classroom")}?code=${encodeURIComponent(body.classroom.joinCode)}`;
    window.history.replaceState(null, "", url);
  }

  return (
    <main className="column">
      <form className="classroom-form" onSubmit={(event) => void createClassroom(event)}>
        <h1>Classroom</h1>
        <p>
          {isStaticExport
            ? "This browser keeps the class on this computer. Progress is not shared with other computers, and no email is sent."
            : "Create a class, share the join code, and read the report here. Email is sent only when SMTP is configured."}
        </p>
        <label>
          Classroom name
          <input aria-label="Classroom name" value={name} onChange={(event) => setName(event.target.value)} />
        </label>
        <label>
          Report email
          <input
            aria-label="Report email"
            value={reportEmail}
            onChange={(event) => setReportEmail(event.target.value)}
          />
        </label>
        <label>
          Join code
          <input aria-label="Join code" value={joinCode} onChange={(event) => setJoinCode(event.target.value)} />
        </label>
        <button type="submit">Create classroom</button>
      </form>

      <form
        className="classroom-form"
        onSubmit={(event) => {
          event.preventDefault();
          void loadReport(lookup);
        }}
      >
        <label>
          Load report
          <input aria-label="Load report" value={lookup} onChange={(event) => setLookup(event.target.value)} />
        </label>
        <button type="submit">Refresh report</button>
      </form>

      {error ? (
        <p className="validation-error" role="alert">
          {error}
        </p>
      ) : null}

      {classroom ? (
        <section className="report" data-testid="report">
          <h2>{classroom.name}</h2>
          <p>
            Join code <strong data-testid="created-code">{classroom.joinCode}</strong>
          </p>
          <p>Report email {classroom.reportEmail}</p>
          {rows.length === 0 ? (
            <p data-testid="report-empty">No students yet.</p>
          ) : (
            <table className="report-table" data-testid="report-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Lesson</th>
                  <th>Part</th>
                  <th>Completion</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={`${row.studentId}-${row.lessonId}`} data-testid="report-row">
                    <td>{row.displayName}</td>
                    <td>{row.lessonId}</td>
                    <td>{row.beatId}</td>
                    <td>{row.completed ? "Complete" : "In progress"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      ) : null}
    </main>
  );
}
