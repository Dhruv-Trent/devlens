"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";
import type { Project } from "@/types/project";

type Props = {
  onProjectCreated: (project: Project) => void;
};

export default function CreateProjectForm({ onProjectCreated }: Props) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Project name is required");
      return;
    }

    setLoading(true);

    try {
      const project = await apiFetch("/projects", {
        method: "POST",
        auth: true,
        body: JSON.stringify({
          name,
          description: description || null,
        }),
      });

      onProjectCreated(project);
      setName("");
      setDescription("");
    } catch (err: any) {
      setError(err.message || "Failed to create project");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded border p-4">
      <h2 className="text-xl font-semibold">Create New Project</h2>

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Project name"
        className="w-full rounded border px-3 py-2"
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Project description optional"
        className="w-full rounded border px-3 py-2"
        rows={3}
      />

      {error && <p className="text-sm text-red-500">{error}</p>}

      <button
        disabled={loading}
        className="rounded bg-black px-4 py-2 text-white disabled:opacity-60"
      >
        {loading ? "Creating..." : "Create Project"}
      </button>
    </form>
  );
}