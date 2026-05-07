from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.file import File
from app.models.scan_run import ScanRun
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.utils.tree_utils import build_file_tree

router = APIRouter(tags=["files"])

@router.get("/projects/{project_id}/files/tree")
def get_project_file_tree(
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

    latest_scan = (
        db.query(ScanRun)
        .filter(
            ScanRun.project_id == project_id,
            ScanRun.status == "completed"
        )
        .order_by(ScanRun.completed_at.desc())
        .first()
    )

    if not latest_scan:
        return {
            "name": "root",
            "path": "",
            "type": "folder",
            "children": []
        }

    files = (
        db.query(File)
        .filter(
            File.project_id == project_id,
            File.scan_run_id == latest_scan.scan_runs_id,
            File.is_supported == True
        )
        .order_by(File.path.asc())
        .all()
    )

    return build_file_tree(files)