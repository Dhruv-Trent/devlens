from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("devlens_users_projects.projects_id"), nullable=False)
    scan_run_id = Column(Integer, ForeignKey("devlens_users_scan_runs.scan_runs_id"), nullable=False)

    path = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    language = Column(String, nullable=True)
    size_bytes = Column(Integer, default=0)

    content_preview = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    is_supported = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", backref="files")
    scan_run = relationship("ScanRun", backref="files")