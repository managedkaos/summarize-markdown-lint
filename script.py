import sys
import re
from collections import defaultdict

def summarize_linting_output_by_error(linting_output):
    errors_summary = defaultdict(list)
    pattern = re.compile(r"^(.*):(\d+)(?::(\d+))? (MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split('\n')
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, col_number, error_code, message = match.groups()
            location = f"{file_path}: Line {line_number}"
            if col_number:
                location += f":{col_number}"
            errors_summary[f"{error_code} - {message}"].append(location)

    for error, occurrences in errors_summary.items():
        print(f"### {error}")
        for occurrence in occurrences:
            print(f"- {occurrence}")
        print()

def summarize_linting_output(linting_output):
    errors_by_file = defaultdict(list)
    pattern = re.compile(r"^(.*):(\d+)(?::(\d+))? (MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split('\n')
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, col_number, error_code, message = match.groups()
            location = f"Line {line_number}"
            if col_number:
                location += f":{col_number}"
            errors_by_file[file_path].append(f"{location}: {error_code} - {message}")

    for file_path, errors in errors_by_file.items():
        print(f"### {file_path}")
        for error in errors:
            print(f"- {error}")
        print()

def read_input():
    if not sys.stdin.isatty():
        # Reading from STDIN
        linting_output = sys.stdin.read()
    else:
        # Reading from a file
        if len(sys.argv) != 2:
            print("Usage: python summarize_lint_by_error.py <file_path>")
            sys.exit(1)
        file_path = sys.argv[1]
        with open(file_path, 'r') as file:
            linting_output = file.read()
    return linting_output

if __name__ == "__main__":
    linting_output = read_input()
    summarize_linting_output_by_file(linting_output)
    summarize_linting_output_by_error(linting_output)