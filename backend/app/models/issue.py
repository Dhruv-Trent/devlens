from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("devlens_users_projects.projects_id"), nullable=False)
    scan_run_id = Column(Integer, ForeignKey("devlens_users_scan_runs.scan_runs_id"), nullable=False)

    file_id = Column(Integer, ForeignKey("files.id"), nullable=True)

    type = Column(String, nullable=False)
    severity = Column(String, nullable=False, default="low")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    line_reference = Column(String, nullable=True)
    suggestion = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", backref="issues")
    scan_run = relationship("ScanRun", backref="issues")
    file = relationship("File", backref="issues")