from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base

class FileChunk(Base):
    __tablename__ = "file_chunks"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count_estimate = Column(Integer, default=0)
    embedding = Column(Vector(1536), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    file = relationship("File", backref="chunks")