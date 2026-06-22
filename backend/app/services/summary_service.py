from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SUMMARY_MODEL = "gpt-4o-mini"


def generate_file_summary(file: File) -> str:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")

    content = file.content_preview or ""

    if not content.strip():
        return "No readable content available for this file."

    prompt = f"""
You are DevLens, an AI software engineering assistant.

Summarize this source file clearly for a developer.

Include:
- what the file is responsible for
- important functions/classes/components if visible
- any notable dependencies or patterns
- keep it concise, around 4-6 sentences

File path: {file.path}
Language: {file.language}

File content:
{content}
"""

    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You summarize source code files accurately and concisely.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def generate_summaries_for_scan(db: Session, scan_run_id: int) -> int:
    files = (
        db.query(File)
        .filter(
            File.scan_run_id == scan_run_id,
            File.is_supported == True,
        )
        .order_by(File.path.asc())
        .all()
    )

    summary_count = 0

    for file in files:
        if file.summary:
            continue

        try:
            file.summary = generate_file_summary(file)
            summary_count += 1
        except Exception as e:
            file.summary = f"Summary generation skipped or failed: {str(e)}"

    db.commit()

    return summary_count