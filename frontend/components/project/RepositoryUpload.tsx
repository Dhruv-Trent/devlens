"use client";

import { useState } from "react";
import { getToken } from "@/lib/auth";
import type { ScanRun } from "@/types/scan";

type Props = {
  projectId: string;
};

export default function RepositoryUpload({ projectId }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [scan, setScan] = useState<ScanRun | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setScan(null);

    if (!file) {
      setError("Please choose a .zip file");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".zip")) {
      setError("Only .zip files are allowed");
      return;
    }

    const token = getToken();

    if (!token) {
      setError("You must be logged in");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/projects/${projectId}/upload`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setScan(data);
      setFile(null);
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded border p-4 space-y-4">
      <div>
        <h2 className="text-xl font-semibold">Upload Repository</h2>
        <p className="text-sm text-gray-600">
          Upload a repository as a .zip file to start a scan.
        </p>
      </div>

      <form onSubmit={handleUpload} className="space-y-3">
        <input
          type="file"
          accept=".zip"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block w-full rounded border px-3 py-2"
        />

        {error && <p className="text-sm text-red-500">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-60"
        >
          {loading ? "Uploading..." : "Upload Zip"}
        </button>
      </form>

      {scan && (
        <div className="rounded bg-gray-50 p-3 text-sm">
          <p className="font-medium">Upload successful</p>
          <p>Scan ID: {scan.scan_runs_id}</p>
          <p>Status: {scan.status}</p>
        </div>
      )}
      <p className="text-xs text-gray-500">
        Scan started. Refresh this page or check scan history later to see
        updated status.
      </p>
    </section>
  );
}
