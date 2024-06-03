import unittest
from unittest.mock import patch
import sys
from io import StringIO
import script
import warnings

class TestSummarizeLintByError(unittest.TestCase):

    def setUp(self):
        self.test_content = """\
ch0_intro/00_01_introduction/README.md:15 MD012/no-multiple-blanks Multiple consecutive blank lines [Expected: 1; Actual: 2]
ch1_pipelines/01_01_create_a_pipeline/README.md:14 MD022/blanks-around-headings Headings should be surrounded by blank lines [Expected: 1; Actual: 0; Below] [Context: "## Versions for `default-image`"]
"""

    @patch('sys.stdin', new_callable=StringIO)
    def test_summarize_lint_by_error_from_stdin(self, mock_stdin):
        mock_stdin.write(self.test_content)
        mock_stdin.seek(0)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            script.read_input = lambda: sys.stdin.read()
            script.summarize_linting_output_by_error(script.read_input())
            output = mock_stdout.getvalue()
            expected_output = """\
## By Error
### MD012/no-multiple-blanks - Multiple consecutive blank lines [Expected: 1; Actual: 2]
- [ ] ch0_intro/00_01_introduction/README.md: Line 15

### MD022/blanks-around-headings - Headings should be surrounded by blank lines [Expected: 1; Actual: 0; Below] [Context: "## Versions for `default-image`"]
- [ ] ch1_pipelines/01_01_create_a_pipeline/README.md: Line 14

"""
            self.assertEqual(output, expected_output)

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ResourceWarning)
        unittest.main()

