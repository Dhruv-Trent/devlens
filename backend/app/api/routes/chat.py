from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.api.routes.auth import get_current_user
from app.services.project_service import get_project_by_id
from app.services.chat_service import (
    answer_repository_question,
    save_chat_message,
    get_chat_history,
)
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageResponse

router = APIRouter(tags=["chat"])


@router.post("/projects/{project_id}/chat", response_model=ChatResponse)
def chat_with_project(
    project_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id, current_user.user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required",
        )

    result = answer_repository_question(
        db=db,
        project_id=project_id,
        question=payload.message,
    )

    save_chat_message(
        db=db,
        project_id=project_id,
        scan_run_id=result["scan_run_id"],
        role="user",
        message=payload.message,
    )

    save_chat_message(
        db=db,
        project_id=project_id,
        scan_run_id=result["scan_run_id"],
        role="assistant",
        message=result["answer"],
    )

    return {"answer": result["answer"]}


@router.get("/projects/{project_id}/chat", response_model=list[ChatMessageResponse])
def list_project_chat_history(
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

    return get_chat_history(db, project_id)