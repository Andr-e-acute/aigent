# tests.py
from pathlib import Path
from functions.run_python_file import run_python_file

if __name__ == "__main__":
    # Ensure working dir exists
    base = Path("calculator")
    base.mkdir(parents=True, exist_ok=True)

    # 0) Create a tiny Python script that prints something
    echo_path = base / "echo.py"
    echo_path.write_text('print("hello from echo")\n', encoding="utf-8")

    # 1) Run it -> should produce STDOUT:
    print(run_python_file("calculator", "echo.py"))

    # 2) Nonexistent file -> should contain: File "nonexistent.py" not found
    print(run_python_file("calculator", "nonexistent.py"))

    # 3) Outside working dir -> should contain: Cannot execute "../main.py" as it is outside
    print(run_python_file("calculator", "../main.py"))
