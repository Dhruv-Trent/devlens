"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { Issue } from "@/types/issue";

type Props = {
  projectId: string;
};

function severityClass(severity: string) {
  if (severity === "high") return "bg-red-100 text-red-700";
  if (severity === "medium") return "bg-yellow-100 text-yellow-700";
  return "bg-blue-100 text-blue-700";
}

export default function FindingsPanel({ projectId }: Props) {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadIssues() {
      try {
        const data = await apiFetch(`/projects/${projectId}/issues`, {
          auth: true,
        });

        setIssues(data);
      } finally {
        setLoading(false);
      }
    }

    loadIssues();
  }, [projectId]);

  if (loading) {
    return (
      <section className="rounded border p-4">
        <p className="text-sm text-gray-500">Loading findings...</p>
      </section>
    );
  }

  return (
    <section className="rounded border p-4 space-y-3">
      <div>
        <h2 className="text-xl font-semibold">Findings</h2>
        <p className="text-sm text-gray-500">
          Basic code quality and risk hints from the latest scan.
        </p>
      </div>

      {issues.length === 0 ? (
        <p className="rounded bg-gray-50 p-3 text-sm text-gray-500">
          No findings found for the latest scan.
        </p>
      ) : (
        <div className="space-y-3">
          {issues.map((issue) => (
            <div key={issue.id} className="rounded border p-3">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="font-semibold">{issue.title}</h3>
                  <p className="text-sm text-gray-600">{issue.description}</p>
                </div>

                <span
                  className={`rounded px-2 py-1 text-xs font-medium ${severityClass(
                    issue.severity
                  )}`}
                >
                  {issue.severity}
                </span>
              </div>

              <div className="mt-2 text-xs text-gray-500">
                <p>Type: {issue.type}</p>
                {issue.file_id && <p>File ID: {issue.file_id}</p>}
                {issue.line_reference && <p>Line: {issue.line_reference}</p>}
              </div>

              {issue.suggestion && (
                <p className="mt-2 rounded bg-gray-50 p-2 text-sm">
                  Suggestion: {issue.suggestion}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}