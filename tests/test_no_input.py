import runpy
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

    def test_main_exits_quietly_on_empty_input(self):
        mock_stdin = StringIO("")
        mock_stdin.isatty = lambda: False
        with patch('sys.stdin', mock_stdin), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             self.assertRaises(SystemExit) as cm:
            runpy.run_module('script', run_name='__main__', alter_sys=True)
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(mock_stdout.getvalue(), "")


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ResourceWarning)
        unittest.main()
