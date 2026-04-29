from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScanRun(Base):
    __tablename__ = "devlens_users_scan_runs"

    scan_runs_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("devlens_users_projects.project_id"), nullable=False)
   
    status = Column(String, nullable=False, default="pending")

    uploaded_zip_path = Column(String, nullable=True)
    extracted_path = Column(String, nullable=True)
    
    total_files = Column(Integer, default=0)
    supported_files = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    issue_count = Column(Integer, default=0)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", backref="devlens_users_scan_runs")