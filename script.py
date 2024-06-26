"""
Summarize linting output by error and by file.
"""
import sys
import re
from collections import defaultdict


def summarize_linting_output_by_error(linting_output):
    """
    Summarize linting output by error.
    """
    errors_summary = defaultdict(list)
    pattern = re.compile(r"^(.*):(\d+)(?::(\d+))? (MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split("\n")
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, col_number, error_code, message = match.groups()
            location = f"{file_path}: Line {line_number}"
            if col_number:
                location += f":{col_number}"
            errors_summary[f"{error_code} - {message}"].append(location)

    print("## By Error")

    for error, occurrences in errors_summary.items():
        print(f"### {error}")
        for occurrence in occurrences:
            print(f"- [ ] {occurrence}")
        print()


def summarize_linting_output_by_file(linting_output):
    """
    Summarize linting output by file.
    """
    errors_by_file = defaultdict(list)
    pattern = re.compile(r"^(.*):(\d+)(?::(\d+))? (MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split("\n")
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, col_number, error_code, message = match.groups()
            location = f"Line {line_number}"
            if col_number:
                location += f":{col_number}"
            errors_by_file[file_path].append(f"{location}: {error_code} - {message}")

    print("## By File")

    for file_path, errors in errors_by_file.items():
        print(f"### {file_path}")
        for error in errors:
            print(f"- [ ] {error}")
        print()


def read_input():
    """
    Read input from STDIN or a file.
    """

    # Reading from STDIN
    if not sys.stdin.isatty():
        linting_output = sys.stdin.read()

    # Reading from a file
    else:
        if len(sys.argv) != 2:
            print("Usage: python script.py <file_path>")
            sys.exit(1)
        file_path = sys.argv[1]
        with open(file_path, "r") as file:
            linting_output = file.read()
    return linting_output


if __name__ == "__main__":
    print("# Linting Summary")
    linting_output = read_input()
    summarize_linting_output_by_file(linting_output)
    summarize_linting_output_by_error(linting_output)
