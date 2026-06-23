import os
import zipfile
import shutil
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.scan_run import ScanRun

from app.services.file_service import save_repository_files

from app.core.database import SessionLocal

from app.services.chunk_service import create_chunks_for_scan
from app.services.embedding_service import generate_embeddings_for_scan
from app.services.summary_service import generate_summaries_for_scan
from app.services.finding_service import generate_findings_for_scan

EXTRACT_DIR = "extracted_repos"

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "venv",
    "__pycache__",
    ".idea",
    ".vscode",
}

def is_safe_zip_path(base_dir: str, target_path: str) -> bool:
    base_dir = os.path.abspath(base_dir)
    target_path = os.path.abspath(target_path)
    return target_path.startswith(base_dir)

def safe_extract_zip(zip_path: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            target_path = os.path.join(extract_to, member.filename)

            if not is_safe_zip_path(extract_to, target_path):
                raise ValueError("Unsafe zip file path detected")

        zip_ref.extractall(extract_to)

def should_ignore_path(path_parts: list[str]) -> bool:
    return any(part in IGNORED_DIRS for part in path_parts)

def count_repository_files(extracted_path: str) -> int:
    total_files = 0

    for root, dirs, files in os.walk(extracted_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        relative_root = os.path.relpath(root, extracted_path)
        path_parts = [] if relative_root == "." else relative_root.split(os.sep)

        if should_ignore_path(path_parts):
            continue

        total_files += len(files)

    return total_files

def run_scan(scan_id: int):
    db = SessionLocal()
    try:
        scan = db.query(ScanRun).filter(ScanRun.scan_runs_id == scan_id).first()

        if not scan:
            return

        try:
            scan.status = "processing"
            scan.started_at = datetime.now(timezone.utc)
            db.commit()

            if not os.path.exists(scan.uploaded_zip_path):
                raise ValueError("Uploaded zip file not found")

            extract_path = os.path.join(
                EXTRACT_DIR,
                f"project_{scan.project_id}_scan_{scan.scan_runs_id}"
            )

            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)

            safe_extract_zip(scan.uploaded_zip_path, extract_path)

            total_files = count_repository_files(extract_path)

            file_result = save_repository_files(
                db=db,
                project_id=scan.project_id,
                scan_run_id=scan.scan_runs_id,
                extracted_path=extract_path,
                ignored_dirs=IGNORED_DIRS,
            )
            chunk_count = create_chunks_for_scan(db, scan.scan_runs_id)
            
            try:
                generate_embeddings_for_scan(db, scan.scan_runs_id)
            except Exception as embedding_error:
                print(f"Embedding generation failed: {embedding_error}")
                
            generate_summaries_for_scan(db, scan.scan_runs_id)
            
            issue_count = generate_findings_for_scan(db, scan.scan_runs_id)
            
            scan.extracted_path = extract_path
            scan.total_files = total_files
            scan.supported_files = file_result["supported_files"]
            scan.chunk_count = chunk_count
            scan.issue_count = issue_count
            scan.status = "completed"
            scan.completed_at = datetime.now(timezone.utc)
            db.commit()

        except Exception as e:
            db.rollback()

            scan = db.query(ScanRun).filter(ScanRun.scan_runs_id == scan_id).first()

            if scan:
                scan.status = "failed"
                scan.error_message = str(e)
                scan.completed_at = datetime.now(timezone.utc)
                db.commit()
    finally:
        db.close()