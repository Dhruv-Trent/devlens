from datetime import datetime
from pydantic import BaseModel


class IssueResponse(BaseModel):
    id: int
    project_id: int
    scan_run_id: int
    file_id: int | None = None
    type: str
    severity: str
    title: str
    description: str
    line_reference: str | None = None
    suggestion: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True