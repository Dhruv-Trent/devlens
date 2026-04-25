import Link from "next/link";
import type { Project } from "@/types/project";

type Props = {
  project: Project;
};

export default function ProjectCard({ project }: Props) {
  return (
    <Link
      href={`/projects/${project.projects_id}`}
      className="block rounded border p-4 transition hover:bg-gray-50"
    >
      <h3 className="text-lg font-semibold">{project.name}</h3>

      <p className="mt-1 text-sm text-gray-600">
        {project.description || "No description added"}
      </p>

      <p className="mt-3 text-xs text-gray-400">
        Created: {new Date(project.created_at).toLocaleDateString()}
      </p>
    </Link>
  );
}