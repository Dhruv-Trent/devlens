from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("devlens_users_projects.projects_id"),
        nullable=False,
    )

    scan_run_id = Column(
        Integer,
        ForeignKey("devlens_users_scan_runs.scan_runs_id"),
        nullable=True,
    )

    role = Column(String, nullable=False)  # user or assistant
    message = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", backref="chat_messages")
    scan_run = relationship("ScanRun", backref="chat_messages")