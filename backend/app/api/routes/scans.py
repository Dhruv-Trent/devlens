from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.scan_run import ScanRun
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.schemas.scan import ScanRunResponse

router = APIRouter(tags=["scans"])

@router.get("/projects/{project_id}/scans", response_model=list[ScanRunResponse])
def list_project_scans(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return (
        db.query(ScanRun)
        .filter(ScanRun.project_id == project_id)
        .order_by(ScanRun.created_at.desc())
        .all()
    )

@router.get("/scans/{scan_id}", response_model=ScanRunResponse)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scan = db.query(ScanRun).filter(ScanRun.scan_runs_id == scan_id).first()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    project = get_project_by_id(db, scan.project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    return scan