import os, subprocess, sys, re

from typing import NoReturn, Union, List
from pathlib import Path, WindowsPath


def execve_with_program_name(
    program_name: str,
    args: Union[List[str], None] = None,
    glob_search: bool = False,
) -> Union[List[WindowsPath], NoReturn]:
    dirs = os.environ["PATH"].split(";")[:-1]

    results = []
    
    for dih in dirs:
        path = Path(dih)
        iterator = path.glob("*")

        if glob_search:
            for file_name in iterator:
                if program_name in str(file_name).lower():
                    results.append(file_name)
        else:
            for file_name in path.glob("*"):
                if re.search(f"\\\\{program_name}[^\\\\]*$", str(file_name), re.IGNORECASE):
                    results.append(file_name)

    if len(results) == 1:
        print(f"Single match: {results[0]}")
        if args is None:
            os.execve(results[0], [program_name], os.environ)
        else:
            os.execve(results[0], args, os.environ)
    else:
        return results

def get_int(prompt: str = "") -> int:
    while True:
        response = input(prompt)

        if response.isdigit():
            return int(response)

        print("That is not an integer pal", file=sys.stderr)

change_directory = None

inbuilt_commands = {
    "cd": change_directory,
}

def ask():
    while True:
        program = input("Enter program: ")

        if program[0] == "*":
            results = execve_with_program_name(program[1:], glob_search=True)
        else:            
            results = execve_with_program_name(program)

        if len(results) == 0:
            print("No matches found")
            continue

        prompt = ""
        print("Choose one of these or -1 to cancel")
        for i, res in enumerate(results):
            print(f"{i}. {res}", flush=False)


        if (response := get_int()) == -1:
            print("Cancelling...")
            continue
        elif response < -1:
            print("What are you on?", file=sys.stderr)
            continue

        if response >= len(results):
            print("Not gonna work buddy", file=sys.stderr)
            continue

        os.execve(results[response], [program], os.environ)

if __name__ == "__main__":
    ask()

            
