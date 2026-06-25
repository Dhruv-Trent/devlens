export type ScanRun = {
  id: number;
  project_id: number;
  status: "pending" | "processing" | "completed" | "failed";
  uploaded_zip_path?: string | null;
  extracted_path?: string | null;
  total_files: number;
  supported_files: number;
  chunk_count: number;
  issue_count: number;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  created_at: string;
};