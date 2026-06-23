from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.issue import Issue
from app.models.scan_run import ScanRun
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.schemas.issue import IssueResponse

router = APIRouter(tags=["findings"])


@router.get("/projects/{project_id}/issues", response_model=list[IssueResponse])
def list_project_issues(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    latest_scan = (
        db.query(ScanRun)
        .filter(
            ScanRun.project_id == project_id,
            ScanRun.status == "completed",
        )
        .order_by(ScanRun.completed_at.desc())
        .first()
    )

    if not latest_scan:
        return []

    return (
        db.query(Issue)
        .filter(
            Issue.project_id == project_id,
            Issue.scan_run_id == latest_scan.scan_runs_id,
        )
        .order_by(Issue.severity.desc(), Issue.created_at.desc())
        .all()
    )