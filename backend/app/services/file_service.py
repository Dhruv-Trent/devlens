import os
from sqlalchemy.orm import Session

from app.models.file import File
from app.utils.language_utils import get_extension, infer_language, is_supported_file

MAX_PREVIEW_CHARS = 8000

def read_text_preview(file_path: str) -> str | None:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            preview = f.read(MAX_PREVIEW_CHARS)

        return preview.replace("\x00", "")
    except Exception:
        return None

def save_repository_files(
    db: Session,
    project_id: int,
    scan_run_id: int,
    extracted_path: str,
    ignored_dirs: set[str],
):
    saved_files = []
    supported_count = 0

    # Remove old files for this scan if rerun happens
    db.query(File).filter(File.scan_run_id == scan_run_id).delete()
    db.commit()

    for root, dirs, files in os.walk(extracted_path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, extracted_path)

            extension = get_extension(filename)
            language = infer_language(filename)
            supported = is_supported_file(filename)

            preview = read_text_preview(full_path) if supported else None

            size_bytes = os.path.getsize(full_path)

            file_record = File(
                project_id=project_id,
                scan_run_id=scan_run_id,
                path=relative_path,
                filename=filename,
                extension=extension,
                language=language,
                size_bytes=size_bytes,
                content_preview=preview,
                summary=None,
                is_supported=supported,
            )

            db.add(file_record)
            saved_files.append(file_record)

            if supported:
                supported_count += 1

    db.commit()

    return {
        "saved_files": len(saved_files),
        "supported_files": supported_count,
    }