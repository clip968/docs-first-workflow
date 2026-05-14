#!/usr/bin/env python3
"""
init_workflow_template.py - Apply the workflow template to a new project.

This script copies the workflow template into a target project directory
and replaces placeholders with project-specific values.

Usage:
    python init_workflow_template.py \\
        --project-name "my-project" \\
        --language python \\
        --test-command "python -m unittest discover -s tests -p 'test_*.py'" \\
        --source-dir src \\
        --test-dir tests

TODO:
    - Support --dry-run mode.
    - Support --force to overwrite existing files.
    - Auto-detect language from project files.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


PLACEHOLDER_PROJECT_NAME = "{{PROJECT_NAME}}"
PLACEHOLDER_LANGUAGE = "{{LANGUAGE}}"
PLACEHOLDER_TEST_COMMAND = "{{TEST_COMMAND}}"
PLACEHOLDER_SOURCE_DIR = "{{SOURCE_DIR}}"
PLACEHOLDER_TEST_DIR = "{{TEST_DIR}}"

TEMPLATE_DIR_NAME = "workflow-template"

# Files that contain placeholders needing replacement
PLACEHOLDER_FILES = [
    "README.md",
    "docs/WORKFLOW.md",
    "docs/DOC_OWNERS.yml",
    "docs/README.md",
    "docs/specs/0000-project-overview.md",
    "docs/specs/0001-agent-workflow.md",
    "docs/handoff/CURRENT_HANDOFF.md",
    "docs/runbooks/test.md",
    "docs/runbooks/finish-task.md",
    ".github/workflows/docs-freshness.yml",
    ".pre-commit-config.yaml",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a new project with the docs-first agent workflow template."
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Name of the project (e.g., 'my-project')",
    )
    parser.add_argument(
        "--language",
        default="python",
        help="Primary programming language (default: python)",
    )
    parser.add_argument(
        "--test-command",
        default="python -m unittest discover -s tests -p 'test_*.py'",
        help="Test command (default: python unittest)",
    )
    parser.add_argument(
        "--source-dir",
        default="src",
        help="Source code directory (default: src)",
    )
    parser.add_argument(
        "--test-dir",
        default="tests",
        help="Test directory (default: tests)",
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Target project directory (default: current directory)",
    )
    parser.add_argument(
        "--template-path",
        default=TEMPLATE_DIR_NAME,
        help=f"Path to the workflow template directory (default: {TEMPLATE_DIR_NAME})",
    )
    return parser.parse_args(argv)


def replace_placeholders_in_file(
    file_path: Path,
    project_name: str,
    language: str,
    test_command: str,
    source_dir: str,
    test_dir: str,
) -> None:
    """Replace placeholders in the given file with project-specific values."""
    if not file_path.exists():
        print(f"  WARNING: {file_path} not found, skipping")
        return

    content = file_path.read_text(encoding="utf-8")

    replacements = {
        PLACEHOLDER_PROJECT_NAME: project_name,
        PLACEHOLDER_LANGUAGE: language,
        PLACEHOLDER_TEST_COMMAND: test_command,
        PLACEHOLDER_SOURCE_DIR: source_dir,
        PLACEHOLDER_TEST_DIR: test_dir,
    }

    modified = False
    for placeholder, value in replacements.items():
        if placeholder in content:
            content = content.replace(placeholder, value)
            modified = True
            print(f"  Replaced {placeholder} -> {value}")
        # Also replace the raw <test command> placeholder
        if placeholder == PLACEHOLDER_TEST_COMMAND:
            content = content.replace("<test command>", value)

    if modified:
        file_path.write_text(content, encoding="utf-8")
        print(f"  Updated {file_path}")
    else:
        print(f"  No placeholders found in {file_path}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    template_path = Path(args.template_path)
    if not template_path.exists() or not template_path.is_dir():
        print(f"ERROR: Template directory not found: {template_path}", file=sys.stderr)
        return 1

    target_dir = Path(args.target).resolve()
    template_dir = template_path.resolve()

    print(f"Initializing workflow template for project: {args.project_name}")
    print(f"  Template: {template_dir}")
    print(f"  Target:   {target_dir}")
    print(f"  Language: {args.language}")
    print(f"  Test cmd: {args.test_command}")
    print(f"  Src dir:  {args.source_dir}")
    print(f"  Test dir: {args.test_dir}")
    print()

    # Copy template structure to target
    target_template = target_dir / TEMPLATE_DIR_NAME
    if target_template.exists():
        print(f"WARNING: {target_template} already exists, skipping copy")
        print("To re-initialize, remove it first and re-run.")
    else:
        print(f"Copying template to {target_template}...")
        shutil.copytree(template_dir, target_template, dirs_exist_ok=False)
        print("Copy complete.")

    # Replace placeholders
    print("\nReplacing placeholders...")
    for rel_path in PLACEHOLDER_FILES:
        file_path = target_template / rel_path
        replace_placeholders_in_file(
            file_path,
            args.project_name,
            args.language,
            args.test_command,
            args.source_dir,
            args.test_dir,
        )

    print(f"\nDone. Template initialized in {target_template}")
    print("\nNext steps:")
    print(f"  1. Review {target_template / 'docs/DOC_OWNERS.yml'} and customize rules.")
    print(f"  2. Review {target_template / 'docs/handoff/CURRENT_HANDOFF.md'} and update state.")
    print(f"  3. Run {target_template / 'scripts/finish_task.py'} to verify.")
    print("\nTo detach from this template repository:")
    print(f"  cd {target_template}")
    print("  git init && git add . && git commit -m 'initial workflow template'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
