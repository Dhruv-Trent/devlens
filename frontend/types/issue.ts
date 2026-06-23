export type Issue = {
    id: number;
    project_id: number;
    scan_run_id: number;
    file_id?: number | null;
    type: string;
    severity: "low" | "medium" | "high";
    title: string;
    description: string;
    line_reference?: string | null;
    suggestion?: string | null;
    created_at: string;
  };