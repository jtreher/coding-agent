from functions.run_python_file import run_code

def main() -> None:
    print(run_code("calculator", "main.py"))

    print(run_code("calculator", "main.py", ["3 + 5"]))

    print(run_code("calculator", "tests.py"))

    print(run_code("calculator", "../main.py"))

    print(run_code("calculator", "nonexistent.py"))

    print(run_code("calculator", "lorem.txt"))

if __name__ == "__main__":
    main()
