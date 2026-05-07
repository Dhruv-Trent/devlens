export type TreeNode = {
    name: string;
    path: string;
    type: "folder" | "file";
    file_id?: number | null;
    children: TreeNode[];
  };