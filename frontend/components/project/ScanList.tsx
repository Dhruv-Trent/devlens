"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { ScanRun } from "@/types/scan";

type Props = {
  projectId: string;
};

export default function ScanList({ projectId }: Props) {
  const [scans, setScans] = useState<ScanRun[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadScans() {
      try {
        const data = await apiFetch(`/projects/${projectId}/scans`, {
          auth: true,
        });

        setScans(data);
      } finally {
        setLoading(false);
      }
    }

    loadScans();
  }, [projectId]);

  if (loading) {
    return <p className="text-sm text-gray-500">Loading scans...</p>;
  }

  return (
    <section className="rounded border p-4 space-y-3">
      <h2 className="text-xl font-semibold">Recent Scans</h2>

      {scans.length === 0 ? (
        <p className="text-sm text-gray-500">No scans yet.</p>
      ) : (
        <div className="space-y-2">
          {scans.map((scan) => (
            <div key={scan.scan_runs_id} className="rounded bg-gray-50 p-3 text-sm">
              <p>Scan ID: {scan.scan_runs_id}</p>
              <p>Status: {scan.status}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}