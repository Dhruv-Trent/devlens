"use client";

import type { FileDetail } from "@/types/file";

type Props = {
  file: FileDetail | null;
  loading?: boolean;
};

function formatBytes(bytes: number) {
  if (bytes === 0) return "0 Bytes";

  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));

  return `${parseFloat((bytes / Math.pow(1024, i)).toFixed(2))} ${sizes[i]}`;
}

export default function FileViewer({ file, loading = false }: Props) {
  if (loading) {
    return (
      <section className="rounded border p-4">
        <p className="text-sm text-gray-500">Loading file...</p>
      </section>
    );
  }

  if (!file) {
    return (
      <section className="rounded border p-4">
        <h2 className="text-xl font-semibold">File Viewer</h2>
        <p className="mt-2 text-sm text-gray-500">
          Select a file from the repository tree to view its details.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded border p-4 space-y-4">
      <div>
        <h2 className="text-xl font-semibold">{file.filename}</h2>
        <p className="text-sm text-gray-500">{file.path}</p>
      </div>

      <div className="flex flex-wrap gap-2 text-xs">
        <span className="rounded bg-gray-100 px-2 py-1">
          Language: {file.language || "Unknown"}
        </span>

        <span className="rounded bg-gray-100 px-2 py-1">
          Extension: {file.extension || "None"}
        </span>

        <span className="rounded bg-gray-100 px-2 py-1">
          Size: {formatBytes(file.size_bytes)}
        </span>

        <span className="rounded bg-gray-100 px-2 py-1">
          Supported: {file.is_supported ? "Yes" : "No"}
        </span>
      </div>

      <div className="rounded bg-gray-50 p-4">
        <h3 className="mb-2 font-semibold">Summary</h3>
        <p className="text-sm text-gray-600 whitespace-pre-line">
          {file.summary ||
            "No summary available yet. Upload and scan the repository again."}
        </p>
      </div>

      <div>
        <h3 className="mb-2 font-semibold">Content Preview</h3>

        {file.content_preview ? (
          <pre className="max-h-[500px] overflow-auto rounded bg-black p-4 text-sm text-white">
            <code>{file.content_preview}</code>
          </pre>
        ) : (
          <p className="rounded bg-gray-50 p-4 text-sm text-gray-500">
            No preview available for this file.
          </p>
        )}
      </div>
    </section>
  );
}
