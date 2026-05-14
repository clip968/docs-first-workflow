"""
finish_task.py - Final validation gate for task completion.

Runs in sequence:
1. Unit tests (configurable via WORKFLOW_TEST_COMMAND env var)
2. Docs freshness check
3. External mirror dry-run (if script exists)
4. git status --short
5. git diff --stat

All steps must pass for exit code 0.

Usage:
    python scripts/finish_task.py
    python scripts/finish_task.py --skip-tests
    python scripts/finish_task.py --skip-docs-check
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TEST_COMMAND = "python -m unittest discover -s tests -p 'test_*.py'"


def get_test_command() -> str:
    """Return the test command from WORKFLOW_TEST_COMMAND env or default."""
    return os.environ.get("WORKFLOW_TEST_COMMAND", DEFAULT_TEST_COMMAND)


def get_external_mirror_dry_run_command() -> str | None:
    """Return external mirror dry-run command if a script exists."""
    candidate = Path("scripts/sync_external_mirror.py")
    return f"python {candidate} --dry-run" if candidate.exists() else None


@dataclass(frozen=True)
class FinishCommand:
    label: str
    argv: list[str]


def build_finish_commands(
    *,
    skip_docs_check: bool,
    skip_tests: bool,
    skip_external_dry_run: bool,
) -> list[FinishCommand]:
    commands: list[FinishCommand] = []

    if not skip_tests:
        test_cmd = get_test_command()
        commands.append(
            FinishCommand(
                "unit tests",
                test_cmd.split(),
            )
        )

    if not skip_docs_check:
        commands.append(
            FinishCommand(
                "docs freshness check",
                [sys.executable, "scripts/check_docs_freshness.py", "--all"],
            )
        )

    if not skip_external_dry_run:
        ext_cmd = get_external_mirror_dry_run_command()
        if ext_cmd:
            commands.append(
                FinishCommand(
                    "external mirror dry-run",
                    ext_cmd.split(),
                )
            )

    commands.extend(
        [
            FinishCommand("git status", ["git", "status", "--short"]),
            FinishCommand("git diff stat", ["git", "diff", "--stat"]),
        ]
    )
    return commands


def run_command(command: FinishCommand) -> int:
    print(f"\n==> {command.label}")
    print("$ " + " ".join(command.argv))
    completed = subprocess.run(command.argv)
    if completed.returncode != 0:
        print(f"FAILED: {command.label} exited with {completed.returncode}")
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run task completion checks.")
    parser.add_argument("--skip-docs-check", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-external-dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.skip_tests:
        print("SKIP: unit tests")
    if args.skip_docs_check:
        print("SKIP: docs freshness check")
    if args.skip_external_dry_run:
        print("SKIP: external mirror dry-run")

    failures: list[str] = []
    for command in build_finish_commands(
        skip_docs_check=args.skip_docs_check,
        skip_tests=args.skip_tests,
        skip_external_dry_run=args.skip_external_dry_run,
    ):
        if run_command(command) != 0:
            failures.append(command.label)

    if failures:
        print("\nfinish_task failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("\nfinish_task ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
