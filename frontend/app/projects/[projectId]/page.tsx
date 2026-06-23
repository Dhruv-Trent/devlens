"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { getToken, removeToken } from "@/lib/auth";
import type { Project } from "@/types/project";
import RepositoryUpload from "@/components/project/RepositoryUpload";
import ScanList from "@/components/project/ScanList";
import RepositoryTree from "@/components/project/RepositoryTree";
import FileViewer from "@/components/project/FileViewer";
import type { FileDetail } from "@/types/file";
import FindingsPanel from "@/components/project/FindingsPanel";

export default function ProjectDetailPage() {
  const router = useRouter();
  const params = useParams();

  const projectId = params.projectId as string;

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  const [selectedFileId, setSelectedFileId] = useState<number | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileDetail | null>(null);
  const [fileLoading, setFileLoading] = useState(false);

  async function handleFileSelect(fileId: number) {
    setSelectedFileId(fileId);
    setFileLoading(true);

    try {
      const data = await apiFetch(`/files/${fileId}`, {
        auth: true,
      });

      setSelectedFile(data);
    } catch {
      setSelectedFile(null);
    } finally {
      setFileLoading(false);
    }
  }

  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    async function loadProject() {
      try {
        const data = await apiFetch(`/projects/${projectId}`, {
          auth: true,
        });

        setProject(data);
      } catch {
        router.push("/dashboard");
      } finally {
        setLoading(false);
      }
    }

    loadProject();
  }, [projectId, router]);

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

  if (loading) {
    return <main className="p-6">Loading project...</main>;
  }

  if (!project) {
    return <main className="p-6">Project not found.</main>;
  }

  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto max-w-5xl space-y-6">
        <header className="flex items-center justify-between border-b pb-4">
          <div>
            <Link href="/dashboard" className="text-sm text-blue-600">
              ← Back to dashboard
            </Link>

            <h1 className="mt-2 text-3xl font-bold">{project.name}</h1>

            <p className="text-gray-600">
              {project.description || "No description added"}
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="rounded bg-red-600 px-4 py-2 text-white"
          >
            Logout
          </button>
        </header>
        <RepositoryUpload projectId={projectId} />
        <ScanList projectId={projectId} />
        <FindingsPanel projectId={projectId} />
        <div className="grid gap-4 lg:grid-cols-[320px_1fr]">
          <RepositoryTree
            projectId={projectId}
            selectedFileId={selectedFileId}
            onFileSelect={handleFileSelect}
          />

          <FileViewer file={selectedFile} loading={fileLoading} />
        </div>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded border p-4">
            <h2 className="font-semibold">Files</h2>
            <p className="text-sm text-gray-500">Coming soon on Day 8</p>
          </div>

          <div className="rounded border p-4">
            <h2 className="font-semibold">Findings</h2>
            <p className="text-sm text-gray-500">Coming soon on Day 13</p>
          </div>

          <div className="rounded border p-4">
            <h2 className="font-semibold">Chat</h2>
            <p className="text-sm text-gray-500">Coming soon on Day 15</p>
          </div>
        </section>

        <section className="rounded border p-4">
          <h2 className="text-xl font-semibold">Project Workspace</h2>
          <p className="mt-2 text-gray-600">
            This page will later contain repository upload, scan history, file
            explorer, findings, and AI chat.
          </p>
        </section>
      </div>
    </main>
  );
}
