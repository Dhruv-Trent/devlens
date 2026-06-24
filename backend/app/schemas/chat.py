from datetime import datetime
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


class ChatMessageResponse(BaseModel):
    id: int
    project_id: int
    scan_run_id: int | None = None
    role: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True