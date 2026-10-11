"""
Summarize linting output by error and by file.
"""

import sys
import re
from collections import defaultdict


def _split_message_details(message):
    """Split a markdownlint message into summary text and bracketed details."""
    base_message = message.split(" [", 1)[0]
    details = re.findall(r"\[[^\]]+\]", message)
    return base_message, details


def _error_group_heading(error_code, message):
    """Build a stable by-error heading for a markdownlint rule."""
    base_message, _ = _split_message_details(message)
    return f"{error_code} - {base_message}"


def _format_occurrence_details(message):
    """Format per-occurrence bracket details for checklist lines."""
    _, details = _split_message_details(message)
    return " ".join(details)


def _error_sort_key(error_heading):
    """Sort by markdown rule number, then heading text."""
    match = re.match(r"^MD(\d+)", error_heading)
    if match:
        return (int(match.group(1)), error_heading)
    return (float("inf"), error_heading)


def summarize_linting_output_by_error(linting_output):
    """
    Summarize linting output by error.
    """
    errors_summary = defaultdict(list)
    pattern = re.compile(r"^(.*?):(\d+)(?::\d+)? (?:\w+ )?(MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split("\n")
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, error_code, message = match.groups()
            location = f"{file_path}:{line_number}: Line {line_number}"
            occurrence_details = _format_occurrence_details(message)
            if occurrence_details:
                location = f"{location} {occurrence_details}"
            errors_summary[_error_group_heading(error_code, message)].append(location)

    print("## By Error\n")

    for error in sorted(errors_summary.keys(), key=_error_sort_key):
        occurrences = errors_summary[error]
        print(f"### {error}")
        for occurrence in occurrences:
            print(f"- [ ] {occurrence}")
        print()


def summarize_linting_output_by_file(linting_output):
    """
    Summarize linting output by file.
    """
    errors_by_file = defaultdict(list)
    pattern = re.compile(r"^(.*?):(\d+)(?::\d+)? (?:\w+ )?(MD\d+/\S+) (.*)$")

    lines = linting_output.strip().split("\n")
    for line in lines:
        match = pattern.match(line)
        if match:
            file_path, line_number, error_code, message = match.groups()
            location = f"Line {line_number}"
            errors_by_file[file_path].append(f"{location}: {error_code} - {message}")

    print("## By file\n")

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


def has_lint_errors(linting_output):
    """Return True if the linting output contains any parseable errors."""
    pattern = re.compile(r"^(.*?):(\d+)(?::\d+)? (?:\w+ )?(MD\d+/\S+) (.*)$")
    return any(pattern.match(line) for line in linting_output.strip().split("\n"))


if __name__ == "__main__":
    linting_output = read_input()
    if not has_lint_errors(linting_output):
        sys.exit(0)
    print("# Linting Summary\n")
    summarize_linting_output_by_file(linting_output)
    summarize_linting_output_by_error(linting_output)
