"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { getToken, removeToken } from "@/lib/auth";
import type { Project } from "@/types/project";
import CreateProjectForm from "@/components/project/CreateProjectForm";
import ProjectCard from "@/components/project/ProjectCard";

type User = {
  id: number;
  name: string;
  email: string;
};

export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] = useState<User | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    async function loadDashboard() {
      try {
        const me = await apiFetch("/auth/me", { auth: true });
        const projectList = await apiFetch("/projects", { auth: true });

        setUser(me);
        setProjects(projectList);
      } catch {
        removeToken();
        router.push("/login");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [router]);

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

  function handleProjectCreated(project: Project) {
    setProjects((prev) => [project, ...prev]);
  }

  if (loading) {
    return <main className="p-6">Loading dashboard...</main>;
  }

  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto max-w-5xl space-y-8">
        <header className="flex items-center justify-between border-b pb-4">
          <div>
            <h1 className="text-3xl font-bold">DevLens Dashboard</h1>
            <p className="text-gray-600">
              Welcome, {user?.name}
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="rounded bg-red-600 px-4 py-2 text-white"
          >
            Logout
          </button>
        </header>

        <CreateProjectForm onProjectCreated={handleProjectCreated} />

        <section className="space-y-3">
          <h2 className="text-xl font-semibold">Your Projects</h2>

          {projects.length === 0 ? (
            <p className="rounded border p-4 text-gray-600">
              No projects yet. Create your first DevLens project above.
            </p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {projects.map((project) => (
                <ProjectCard key={project.projects_id} project={project} />
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}