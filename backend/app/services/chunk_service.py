from sqlalchemy.orm import Session

from app.models.file import File
from app.models.file_chunk import FileChunk

MAX_CHUNK_CHARS = 3000
CHUNK_OVERLAP_CHARS = 300

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def split_text_into_chunks(text: str) -> list[str]:
    if not text:
        return []

    lines = text.splitlines()
    chunks = []
    current_chunk = []

    current_size = 0

    for line in lines:
        line_size = len(line) + 1

        if current_size + line_size > MAX_CHUNK_CHARS and current_chunk:
            chunks.append("\n".join(current_chunk).strip())

            overlap_text = "\n".join(current_chunk)[-CHUNK_OVERLAP_CHARS:]
            current_chunk = [overlap_text, line]
            current_size = len(overlap_text) + line_size
        else:
            current_chunk.append(line)
            current_size += line_size

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    return [chunk for chunk in chunks if chunk]

def create_chunks_for_file(db: Session, file: File) -> int:
    if not file.is_supported or not file.content_preview:
        return 0

    chunks = split_text_into_chunks(file.content_preview)

    for index, chunk_content in enumerate(chunks):
        chunk = FileChunk(
            file_id=file.id,
            chunk_index=index,
            content=chunk_content,
            token_count_estimate=estimate_tokens(chunk_content),
        )

        db.add(chunk)

    return len(chunks)

def create_chunks_for_scan(db: Session, scan_run_id: int) -> int:
    db.query(FileChunk).filter(
        FileChunk.file_id.in_(
            db.query(File.id).filter(File.scan_run_id == scan_run_id)
        )
    ).delete(synchronize_session=False)

    db.commit()

    files = (
        db.query(File)
        .filter(
            File.scan_run_id == scan_run_id,
            File.is_supported == True
        )
        .order_by(File.path.asc())
        .all()
    )

    total_chunks = 0

    for file in files:
        total_chunks += create_chunks_for_file(db, file)

    db.commit()

    return total_chunks