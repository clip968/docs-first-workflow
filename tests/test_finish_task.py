from __future__ import annotations

import unittest
from unittest import mock

from scripts import finish_task


class FinishTaskTests(unittest.TestCase):
    def test_default_test_command_strips_shell_quotes_from_unittest_pattern(self) -> None:
        with mock.patch.dict("os.environ", {}, clear=True):
            commands = finish_task.build_finish_commands(
                skip_docs_check=True,
                skip_tests=False,
                skip_external_dry_run=True,
            )

        self.assertEqual(
            commands[0].argv,
            ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        )


if __name__ == "__main__":
    unittest.main()
