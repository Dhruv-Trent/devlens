from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file_chunk import FileChunk

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_embedding(text: str) -> list[float]:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")

    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding

def generate_embeddings_for_scan(db: Session, scan_run_id: int) -> int:
    chunks = (
        db.query(FileChunk)
        .join(FileChunk.file)
        .filter(FileChunk.file.has(scan_run_id=scan_run_id))
        .order_by(FileChunk.id.asc())
        .all()
    )
    
    embedded_count = 0

    for chunk in chunks:
        if chunk.embedding is not None:
            continue

        embedding = generate_embedding(chunk.content)
        chunk.embedding = embedding
        embedded_count += 1

    db.commit()

    return embedded_count


def search_similar_chunks(
    db: Session,
    query: str,
    project_id: int,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    results = (
        db.query(FileChunk)
        .join(FileChunk.file)
        .filter(FileChunk.file.has(project_id=project_id))
        .filter(FileChunk.embedding.isnot(None))
        .order_by(FileChunk.embedding.l2_distance(query_embedding))
        .limit(limit)
        .all()
    )

    return results