export type ChatMessage = {
    id: number;
    project_id: number;
    scan_run_id?: number | null;
    role: "user" | "assistant";
    message: string;
    created_at: string;
  };
  
  export type LocalChatMessage = {
    id: string;
    role: "user" | "assistant";
    message: string;
  };