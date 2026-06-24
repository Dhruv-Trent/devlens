from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat_message import ChatMessage
from app.models.scan_run import ScanRun
from app.models.file_chunk import FileChunk
from app.services.embedding_service import search_similar_chunks

client = OpenAI(api_key=settings.OPENAI_API_KEY)

CHAT_MODEL = "gpt-4o-mini"


def get_latest_completed_scan(db: Session, project_id: int):
    return (
        db.query(ScanRun)
        .filter(
            ScanRun.project_id == project_id,
            ScanRun.status == "completed",
        )
        .order_by(ScanRun.completed_at.desc())
        .first()
    )


def save_chat_message(
    db: Session,
    project_id: int,
    scan_run_id: int | None,
    role: str,
    message: str,
):
    chat_message = ChatMessage(
        project_id=project_id,
        scan_run_id=scan_run_id,
        role=role,
        message=message,
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return chat_message


def build_context_from_chunks(chunks: list[FileChunk]) -> str:
    context_blocks = []

    for chunk in chunks:
        file = chunk.file

        context_blocks.append(
            f"""
File path: {file.path}
Language: {file.language}
Chunk index: {chunk.chunk_index}

Content:
{chunk.content}
"""
        )

    return "\n---\n".join(context_blocks)


def answer_repository_question(
    db: Session,
    project_id: int,
    question: str,
):
    latest_scan = get_latest_completed_scan(db, project_id)

    if not latest_scan:
        return {
            "answer": "No completed scan exists for this project yet. Upload and scan a repository first.",
            "scan_run_id": None,
        }

    try:
        chunks = search_similar_chunks(
            db=db,
            query=question,
            project_id=project_id,
            scan_run_id=latest_scan.scan_runs_id,
            limit=6,
        )
    except Exception as retrieval_error:
        return {
            "answer": f"Chat backend is connected, but retrieval is not available yet: {str(retrieval_error)}",
            "scan_run_id": latest_scan.scan_runs_id,
        }

    if not chunks:
        return {
            "answer": "Chat backend is connected, but I could not find indexed repository context yet. This usually means embeddings are not available.",
            "scan_run_id": latest_scan.scan_runs_id,
        }

    if not settings.OPENAI_API_KEY:
        return {
            "answer": "Repository context was found, but no OpenAI API key is configured for answer generation.",
            "scan_run_id": latest_scan.scan_runs_id,
        }

    context = build_context_from_chunks(chunks)
    source_paths = sorted({chunk.file.path for chunk in chunks})

    prompt = f"""
You are DevLens, an AI software engineering assistant.

Answer the user's question using ONLY the repository context below.

Rules:
- Do not invent files, functions, routes, or behavior.
- If the context is insufficient, say what you could not confirm.
- Mention relevant file paths when useful.
- Be clear and practical.
- Keep the answer concise but helpful.

Repository context:
{context}

User question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions about codebases using only retrieved repository context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        answer = response.choices[0].message.content.strip()
        answer += "\n\nRelevant files:\n" + "\n".join(
            f"- {path}" for path in source_paths
        )

        return {
            "answer": answer,
            "scan_run_id": latest_scan.scan_runs_id,
        }

    except Exception as chat_error:
        return {
            "answer": f"Repository context was found, but answer generation failed: {str(chat_error)}",
            "scan_run_id": latest_scan.scan_runs_id,
        }


def get_chat_history(db: Session, project_id: int):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.project_id == project_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )