from cProfile import label
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
def test():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)
# Helper function to display results
    def show(label, value):
        print(f"--- {label} ---")
        print(value if isinstance(value, str) else repr(value))
        print()

    # Truncation check
    show("lorem (truncated)", get_file_content("calculator", "lorem.txt"))

    # Normal reads
    show("main.py", get_file_content("calculator", "main.py"))
    show("pkg/calculator.py", get_file_content("calculator", "pkg/calculator.py"))

    # Outside working dir -> error
    show("outside", get_file_content("calculator", "/bin/cat"))

    # Missing file -> error
    show("missing", get_file_content("calculator", "pkg/does_not_exist.py"))
    

if __name__ == "__main__":
    # 1) Overwrite lorem.txt inside working dir
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # 2) Write inside a subfolder of working dir
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    # 3) Attempt to write outside working dir (should error)
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
        # 1) Should print calculator usage/help (whatever main.py prints with no args)
    print(run_python_file("calculator", "main.py"))

    # 2) Should run and print a numeric result (e.g., 8 for 3 + 5)
    print(run_python_file("calculator", "main.py", ["3", "+", "5"]))

    # 3) Outside working dir (expect "outside" error)
    print(run_python_file("calculator", "../main.py"))

    # 4) Not a Python file (change "lorem.txt" to any non-.py file you have in calculator/)
    print(run_python_file("calculator", "lorem.txt"))

    # 5) Missing file
    print(run_python_file("calculator", "nonexistent.py"))