SUPPORTED_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript React",
    ".jsx": "JavaScript React",
    ".java": "Java",
    ".c": "C",
    ".txt": "Text",
    ".json": "JSON",
    ".md": "Markdown",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".yaml": "YAML",
    ".yml": "YAML",
}

def get_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.split(".")[-1].lower()

def infer_language(filename: str) -> str | None:
    extension = get_extension(filename)
    return SUPPORTED_EXTENSIONS.get(extension)

def is_supported_file(filename: str) -> bool:
    extension = get_extension(filename)
    return extension in SUPPORTED_EXTENSIONS