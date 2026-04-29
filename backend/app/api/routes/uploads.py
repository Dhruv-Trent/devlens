import os

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.services.upload_service import (validate_zip_file,save_upload_file,create_pending_scan,)
from app.schemas.upload import UploadResponse
from app.services.scan_service import run_scan


router = APIRouter(tags=["uploads"])


@router.post("/projects/{project_id}/upload", response_model=UploadResponse)
def upload_repository_zip(
    project_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    validate_zip_file(file)

    uploaded_zip_path = save_upload_file(file, project_id)

    try:
        scan = create_pending_scan(
            db=db,
            project_id=project_id,
            uploaded_zip_path=uploaded_zip_path,
        )
        background_tasks.add_task(run_scan, scan.scan_runs_id)
    except Exception:
        if os.path.exists(uploaded_zip_path):
            os.remove(uploaded_zip_path)
        raise

    return scan