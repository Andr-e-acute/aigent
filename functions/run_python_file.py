from pathlib import Path
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        args = [] if args is None else list(args)

        base = Path(working_directory).resolve()
        p = Path(file_path)
        target = p.resolve() if p.is_absolute() else (base / p).resolve()

        # Block escapes outside working_directory
        try:
            target.relative_to(base)
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'

        # Must exist
        if not target.exists():
            return f'Error: File "{file_path}" not found.'

        # Must be a Python file
        if target.suffix.lower() != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        completed = subprocess.run(
            ["python3", str(target), *args],
            cwd=str(base),
            capture_output=True,
            text=True,
            timeout=30,
        )

        parts = []
        if completed.stdout:
            parts.append("STDOUT:\n" + completed.stdout.strip())
        if completed.stderr:
            parts.append("STDERR:\n" + completed.stderr.strip())
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if not parts:
            return "No output produced."

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
