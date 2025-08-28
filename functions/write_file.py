# functions/write_file.py
from pathlib import Path

def write_file(working_directory, file_path, content):
    try:
        base = Path(working_directory).resolve()
        p = Path(file_path)

        # Build absolute, normalized target path
        target = p.resolve() if p.is_absolute() else (base / p).resolve()

        # Block escapes outside working_directory
        try:
            target.relative_to(base)
        except ValueError:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'

        # Ensure parent folder exists (safe for the tests; creates file if missing)
        target.parent.mkdir(parents=True, exist_ok=True)

        # Overwrite the file with the provided content
        with target.open("w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
