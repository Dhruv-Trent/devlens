from pydantic import BaseModel
from datetime import datetime

class FileChunkResponse(BaseModel):
    id: int
    file_id: int
    chunk_index: int
    content: str
    token_count_estimate: int
    created_at: datetime

    class Config:
        from_attributes = True