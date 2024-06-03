# Summarize Markdown Lint

A tool for summarizing the output from [davidanson/markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2).

## Usage

```bash
lint_command 2>&1 | docker run --interactive ghcr.io/managedkaos/summarize-markdown-lint:main
```

Run the process that calls `markdownlint` and pipe the output to the `summarize-markdown-lint` container.

Include the `2>&1` to capture the stderr output from the `markdownlint` command.  This is necessary because the `markdownlint` command writes to stderr.

For the `docker run` command, use the `--interactive` flag to allow the container to read from stdin.

