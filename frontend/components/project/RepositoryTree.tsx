"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { TreeNode } from "@/types/file";

type Props = {
  projectId: string;
};

function TreeItem({ node }: { node: TreeNode }) {
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
              <TreeItem key={child.path} node={child} />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <button
      className="ml-2 block text-left text-sm text-gray-700 hover:text-black"
      onClick={() => console.log("Clicked file:", node.file_id)}
    >
      📄 {node.name}
    </button>
  );
}

export default function RepositoryTree({ projectId }: Props) {
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

      <div className="max-h-[500px] overflow-auto rounded bg-gray-50 p-3">
        {tree.children.map((child) => (
          <TreeItem key={child.path} node={child} />
        ))}
      </div>
    </section>
  );
}