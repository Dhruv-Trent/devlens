from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):
    scan_id: int
    project_id: int
    status: str
    uploaded_zip_path: str
    created_at: datetime

    class Config:
        from_attributes = True
        