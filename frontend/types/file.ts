export type TreeNode = {
    name: string;
    path: string;
    type: "folder" | "file";
    file_id?: number | null;
    children: TreeNode[];
  };

  export type FileDetail = {
    id: number;
    project_id: number;
    scan_run_id: number;
    path: string;
    filename: string;
    extension?: string | null;
    language?: string | null;
    size_bytes: number;
    content_preview?: string | null;
    summary?: string | null;
    is_supported: boolean;
    created_at: string;
  };