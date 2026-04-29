export type ScanRun = {
    scan_runs_id: number;
    project_id: number;
    status: string;
    uploaded_zip_path?: string | null;
    created_at: string;
  };