from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel):
    id: int
    project_id: int
    scan_run_id: int
    path: str
    filename: str
    extension: str | None = None
    language: str | None = None
    size_bytes: int
    content_preview: str | None = None
    summary: str | None = None
    is_supported: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TreeNode(BaseModel):
    name: str
    path: str
    type: str
    file_id: int | None = None
    children: list["TreeNode"] = []

TreeNode.model_rebuild()
