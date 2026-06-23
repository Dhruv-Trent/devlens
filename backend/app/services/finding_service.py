import re
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.issue import Issue


TODO_PATTERNS = ["TODO", "FIXME", "HACK", "XXX"]

SECRET_PATTERNS = [
    r"API_KEY\s*=",
    r"SECRET\s*=",
    r"PASSWORD\s*=",
    r"TOKEN\s*=",
    r"PRIVATE_KEY",
    r"-----BEGIN PRIVATE KEY-----",
]

RISKY_PATTERNS = [
    ("eval(", "Use of eval()", "Avoid eval() because it can execute unsafe code."),
    ("exec(", "Use of exec()", "Avoid exec() unless absolutely necessary."),
    ("pickle.loads", "Unsafe deserialization", "Be careful with pickle.loads on untrusted data."),
    ("innerHTML", "Direct innerHTML usage", "Avoid direct innerHTML assignment where possible."),
]

TEST_INDICATORS = [
    "test",
    "tests",
    "__tests__",
    ".spec.",
    ".test.",
]


def create_issue(
    db: Session,
    project_id: int,
    scan_run_id: int,
    file_id: int | None,
    issue_type: str,
    severity: str,
    title: str,
    description: str,
    line_reference: str | None = None,
    suggestion: str | None = None,
):
    issue = Issue(
        project_id=project_id,
        scan_run_id=scan_run_id,
        file_id=file_id,
        type=issue_type,
        severity=severity,
        title=title,
        description=description,
        line_reference=line_reference,
        suggestion=suggestion,
    )

    db.add(issue)
    return issue


def detect_todo_comments(db: Session, file: File):
    content = file.content_preview or ""

    for line_number, line in enumerate(content.splitlines(), start=1):
        upper_line = line.upper()

        for pattern in TODO_PATTERNS:
            if pattern in upper_line:
                create_issue(
                    db=db,
                    project_id=file.project_id,
                    scan_run_id=file.scan_run_id,
                    file_id=file.id,
                    issue_type="todo_comment",
                    severity="low",
                    title=f"{pattern} comment found",
                    description=f"A {pattern} marker was found in this file.",
                    line_reference=str(line_number),
                    suggestion="Review this comment and either resolve it or convert it into a tracked task.",
                )
                break


def detect_long_file(db: Session, file: File):
    content = file.content_preview or ""
    line_count = len(content.splitlines())

    if line_count >= 800:
        severity = "high"
    elif line_count >= 500:
        severity = "medium"
    elif line_count >= 300:
        severity = "low"
    else:
        return

    create_issue(
        db=db,
        project_id=file.project_id,
        scan_run_id=file.scan_run_id,
        file_id=file.id,
        issue_type="long_file",
        severity=severity,
        title="Large file detected",
        description=f"This file has approximately {line_count} lines.",
        line_reference=None,
        suggestion="Consider splitting this file into smaller modules or components.",
    )


def detect_secret_patterns(db: Session, file: File):
    content = file.content_preview or ""

    for pattern in SECRET_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)

        if match:
            line_number = content[:match.start()].count("\n") + 1

            create_issue(
                db=db,
                project_id=file.project_id,
                scan_run_id=file.scan_run_id,
                file_id=file.id,
                issue_type="secret_pattern",
                severity="high",
                title="Possible hardcoded secret",
                description="This file contains a secret-like keyword or private key marker.",
                line_reference=str(line_number),
                suggestion="Move secrets into environment variables or a secure secret manager.",
            )


def detect_risky_patterns(db: Session, file: File):
    content = file.content_preview or ""

    for pattern, title, suggestion in RISKY_PATTERNS:
        index = content.find(pattern)

        if index != -1:
            line_number = content[:index].count("\n") + 1

            create_issue(
                db=db,
                project_id=file.project_id,
                scan_run_id=file.scan_run_id,
                file_id=file.id,
                issue_type="risky_pattern",
                severity="medium",
                title=title,
                description=f"The pattern `{pattern}` was found in this file.",
                line_reference=str(line_number),
                suggestion=suggestion,
            )


def detect_missing_tests(
    db: Session,
    project_id: int,
    scan_run_id: int,
    files: list[File],
):
    has_source_code = any(
        file.extension in [".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp"]
        for file in files
    )

    has_tests = any(
        indicator in file.path.lower()
        for file in files
        for indicator in TEST_INDICATORS
    )

    if has_source_code and not has_tests:
        create_issue(
            db=db,
            project_id=project_id,
            scan_run_id=scan_run_id,
            file_id=None,
            issue_type="missing_tests",
            severity="low",
            title="No obvious tests found",
            description="This repository appears to contain source code but no obvious test folder or test files were detected.",
            line_reference=None,
            suggestion="Add a tests folder or basic unit tests for the most important logic.",
        )


def generate_findings_for_scan(db: Session, scan_run_id: int) -> int:
    files = (
        db.query(File)
        .filter(
            File.scan_run_id == scan_run_id,
            File.is_supported == True,
        )
        .order_by(File.path.asc())
        .all()
    )

    if not files:
        return 0

    project_id = files[0].project_id

    db.query(Issue).filter(Issue.scan_run_id == scan_run_id).delete()
    db.commit()

    for file in files:
        detect_todo_comments(db, file)
        detect_long_file(db, file)
        detect_secret_patterns(db, file)
        detect_risky_patterns(db, file)

    detect_missing_tests(db, project_id, scan_run_id, files)

    issue_count = (
        db.query(Issue)
        .filter(Issue.scan_run_id == scan_run_id)
        .count()
    )

    db.commit()

    return issue_count