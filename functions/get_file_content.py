from pathlib import Path
from .config import MAX_FILE_CHARS
def get_file_content(working_directory, file_path):
    try:
        base = Path(working_directory).resolve()
        p = Path(file_path)

        # Absolute paths should be honored as-is; relative paths are relative to base
        target = p.resolve() if p.is_absolute() else (base / p).resolve()

        # Ensure target is inside base
        try:
            target.relative_to(base)
        except ValueError:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
        if not target.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}".'
        with target.open("r", encoding="utf-8") as f:
            data = f.read()

        if len(data) > MAX_FILE_CHARS:
            data = (
                data[:MAX_FILE_CHARS]
                + f'\n[File "{file_path}" truncated at {MAX_FILE_CHARS} characters]\n'
            )

        return data

    except Exception as e:
        return f"Error: {e}"

