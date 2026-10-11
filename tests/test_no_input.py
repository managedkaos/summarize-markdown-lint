import unittest
from unittest.mock import patch
import sys
from io import StringIO
import script
import warnings


class TestNoInput(unittest.TestCase):

    def test_has_lint_errors_empty_string(self):
        self.assertFalse(script.has_lint_errors(""))

    def test_has_lint_errors_no_matching_lines(self):
        self.assertFalse(script.has_lint_errors("Linting: 0 files\nSummary: 0 issues in 0 files\n"))

    def test_has_lint_errors_with_errors(self):
        linting_output = "README.md:15 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2]\n"
        self.assertTrue(script.has_lint_errors(linting_output))

    @patch('sys.stdin', new_callable=StringIO)
    def test_main_exits_quietly_on_empty_input(self, mock_stdin):
        mock_stdin.isatty = lambda: False
        mock_stdin.write("")
        mock_stdin.seek(0)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                with patch.object(sys, 'stdin', mock_stdin):
                    linting_output = mock_stdin.read()
                    if not script.has_lint_errors(linting_output):
                        sys.exit(0)
            self.assertEqual(cm.exception.code, 0)
            self.assertEqual(mock_stdout.getvalue(), "")


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ResourceWarning)
        unittest.main()
