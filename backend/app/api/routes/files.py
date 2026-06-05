from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.file import File
from app.models.scan_run import ScanRun
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.utils.tree_utils import build_file_tree
from app.models.file_chunk import FileChunk
from app.schemas.file_chunk import FileChunkResponse

from app.schemas.file import FileResponse
from app.services.embedding_service import search_similar_chunks

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

@router.get("/files/{file_id}", response_model=FileResponse)
def get_file_detail(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    project = get_project_by_id(db, file.project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return file

@router.get("/files/{file_id}/chunks", response_model=list[FileChunkResponse])
def get_file_chunks(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    project = get_project_by_id(db, file.project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return (
        db.query(FileChunk)
        .filter(FileChunk.file_id == file_id)
        .order_by(FileChunk.chunk_index.asc())
        .all()
    )
    
@router.get("/projects/{project_id}/search-chunks")
def search_chunks(
    project_id: int,
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    try:
        chunks = search_similar_chunks(
            db=db,
            query=q,
            project_id=project_id,
            limit=5,
    )
    except Exception:
        return []

    return [
        {
            "chunk_id": chunk.id,
            "file_id": chunk.file_id,
            "chunk_index": chunk.chunk_index,
            "content_preview": chunk.content[:500],
            "token_count_estimate": chunk.token_count_estimate,
        }
        for chunk in chunks
    ]