"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { TreeNode } from "@/types/file";

type Props = {
  projectId: string;
  selectedFileId?: number | null;
  onFileSelect: (fileId: number) => void;
};

function TreeItem({
  node,
  selectedFileId,
  onFileSelect,
}: {
  node: TreeNode;
  selectedFileId?: number | null;
  onFileSelect: (fileId: number) => void;
}) {
  const [open, setOpen] = useState(true);

  if (node.type === "folder") {
    return (
      <div className="ml-2">
        <button
          onClick={() => setOpen(!open)}
          className="flex items-center gap-1 text-left text-sm font-medium"
        >
          <span>{open ? "📂" : "📁"}</span>
          <span>{node.name}</span>
        </button>

        {open && (
          <div className="ml-4 border-l pl-2">
            {node.children.map((child) => (
              <TreeItem
                key={child.path}
                node={child}
                selectedFileId={selectedFileId}
                onFileSelect={onFileSelect}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  const isSelected = selectedFileId === node.file_id;

  return (
    <button
      className={`ml-2 block w-full rounded px-2 py-1 text-left text-sm ${
        isSelected
          ? "bg-black text-white"
          : "text-gray-700 hover:bg-gray-100 hover:text-black"
      }`}
      onClick={() => {
        if (node.file_id) {
          onFileSelect(node.file_id);
        }
      }}
    >
      📄 {node.name}
    </button>
  );
}

export default function RepositoryTree({
  projectId,
  selectedFileId,
  onFileSelect,
}: Props) {
  const [tree, setTree] = useState<TreeNode | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTree() {
      try {
        const data = await apiFetch(`/projects/${projectId}/files/tree`, {
          auth: true,
        });

        setTree(data);
      } finally {
        setLoading(false);
      }
    }

    loadTree();
  }, [projectId]);

  if (loading) {
    return (
      <section className="rounded border p-4">
        <p className="text-sm text-gray-500">Loading repository tree...</p>
      </section>
    );
  }

  if (!tree || tree.children.length === 0) {
    return (
      <section className="rounded border p-4">
        <h2 className="text-xl font-semibold">Repository Files</h2>
        <p className="mt-2 text-sm text-gray-500">
          No files found yet. Upload and scan a repository first.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded border p-4">
      <h2 className="mb-3 text-xl font-semibold">Repository Files</h2>

      <div className="max-h-[600px] overflow-auto rounded bg-gray-50 p-3">
        {tree.children.map((child) => (
          <TreeItem
            key={child.path}
            node={child}
            selectedFileId={selectedFileId}
            onFileSelect={onFileSelect}
          />
        ))}
      </div>
    </section>
  );
}