"use client";

import type { ScanRun } from "@/types/scan";

type Props = {
  scans: ScanRun[];
  loading?: boolean;
};

function statusClass(status: string) {
  if (status === "completed") return "bg-green-100 text-green-700";
  if (status === "processing") return "bg-yellow-100 text-yellow-700";
  if (status === "failed") return "bg-red-100 text-red-700";
  return "bg-gray-100 text-gray-700";
}

function formatDate(value?: string | null) {
  if (!value) return "N/A";
  return new Date(value).toLocaleString();
}

export default function ScanList({ scans, loading = false }: Props) {
  if (loading) {
    return (
      <section className="rounded border p-4">
        <p className="text-sm text-gray-500">Loading scans...</p>
      </section>
    );
  }

  return (
    <section className="rounded border p-4 space-y-3">
      <div>
        <h2 className="text-xl font-semibold">Scan History</h2>
        <p className="text-sm text-gray-500">
          Previous repository uploads and scan results.
        </p>
      </div>

      {scans.length === 0 ? (
        <p className="rounded bg-gray-50 p-3 text-sm text-gray-500">
          No scans yet.
        </p>
      ) : (
        <div className="space-y-3">
          {scans.map((scan) => (
            <div key={scan.id} className="rounded border p-3">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-medium">Scan #{scan.id}</p>
                  <p className="text-xs text-gray-500">
                    Created: {formatDate(scan.created_at)}
                  </p>
                </div>

                <span
                  className={`rounded px-2 py-1 text-xs font-medium ${statusClass(
                    scan.status
                  )}`}
                >
                  {scan.status}
                </span>
              </div>

              <div className="mt-3 grid gap-2 text-sm md:grid-cols-4">
                <p>Total files: {scan.total_files}</p>
                <p>Supported: {scan.supported_files}</p>
                <p>Chunks: {scan.chunk_count}</p>
                <p>Findings: {scan.issue_count}</p>
              </div>

              <div className="mt-2 text-xs text-gray-500">
                <p>Started: {formatDate(scan.started_at)}</p>
                <p>Completed: {formatDate(scan.completed_at)}</p>
              </div>

              {scan.error_message && (
                <p className="mt-2 rounded bg-red-50 p-2 text-sm text-red-600">
                  {scan.error_message}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}