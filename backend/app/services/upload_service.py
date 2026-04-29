import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.scan_run import ScanRun

UPLOAD_DIR = "uploads"
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB

def validate_zip_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .zip files are allowed"
        )

def save_upload_file(file: UploadFile, project_id: int) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    safe_filename = file.filename.replace(" ", "_")
    unique_filename = f"project_{project_id}_{uuid4()}_{safe_filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    total_size = 0

    with open(file_path, "wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break

            total_size += len(chunk)

            if total_size > MAX_UPLOAD_SIZE:
                buffer.close()
                os.remove(file_path)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File too large. Maximum size is 50 MB"
                )

            buffer.write(chunk)

    return file_path

def create_pending_scan(db: Session, project_id: int, uploaded_zip_path: str):
    scan = ScanRun(
        project_id=project_id,
        status="pending",
        uploaded_zip_path=uploaded_zip_path,
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan