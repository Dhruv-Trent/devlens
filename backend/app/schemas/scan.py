from pydantic import BaseModel
from datetime import datetime

class ScanRunResponse(BaseModel):
    scan_runs_id: int
    project_id: int
    status: str
    uploaded_zip_path: str | None = None
    extracted_path: str | None = None
    total_files: int = 0
    supported_files: int = 0
    chunk_count: int = 0
    issue_count: int = 0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True