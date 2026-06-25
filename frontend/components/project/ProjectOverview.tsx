"use client";

import type { ScanRun } from "@/types/scan";

type Props = {
  latestScan: ScanRun | null;
};

function statusClass(status?: string) {
  if (status === "completed") return "bg-green-100 text-green-700";
  if (status === "processing") return "bg-yellow-100 text-yellow-700";
  if (status === "failed") return "bg-red-100 text-red-700";
  return "bg-gray-100 text-gray-700";
}

export default function ProjectOverview({ latestScan }: Props) {
  return (
    <section className="rounded border p-4 space-y-4">
      <div>
        <h2 className="text-xl font-semibold">Project Overview</h2>
        <p className="text-sm text-gray-500">
          Latest scan summary and repository health snapshot.
        </p>
      </div>

      {!latestScan ? (
        <p className="rounded bg-gray-50 p-3 text-sm text-gray-500">
          No scans yet. Upload a repository zip to generate your first overview.
        </p>
      ) : (
        <>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Latest status:</span>
            <span
              className={`rounded px-2 py-1 text-xs font-medium ${statusClass(
                latestScan.status
              )}`}
            >
              {latestScan.status}
            </span>
          </div>

          <div className="grid gap-3 md:grid-cols-4">
            <div className="rounded bg-gray-50 p-3">
              <p className="text-sm text-gray-500">Total Files</p>
              <p className="text-2xl font-bold">{latestScan.total_files}</p>
            </div>

            <div className="rounded bg-gray-50 p-3">
              <p className="text-sm text-gray-500">Supported Files</p>
              <p className="text-2xl font-bold">{latestScan.supported_files}</p>
            </div>

            <div className="rounded bg-gray-50 p-3">
              <p className="text-sm text-gray-500">Chunks</p>
              <p className="text-2xl font-bold">{latestScan.chunk_count}</p>
            </div>

            <div className="rounded bg-gray-50 p-3">
              <p className="text-sm text-gray-500">Findings</p>
              <p className="text-2xl font-bold">{latestScan.issue_count}</p>
            </div>
          </div>

          {latestScan.error_message && (
            <div className="rounded bg-red-50 p-3 text-sm text-red-600">
              {latestScan.error_message}
            </div>
          )}
        </>
      )}
    </section>
  );
}