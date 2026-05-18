from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import install_into_repo


class InstallIntoRepoTests(unittest.TestCase):
    def test_detects_python_repo_without_user_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "my-python-repo"
            target.mkdir()
            (target / "pyproject.toml").write_text("[project]\nname = 'example'\n", encoding="utf-8")
            (target / "app").mkdir()
            (target / "spec").mkdir()
            (target / "workflow-implementation.md").write_text(
                "Install docs-first workflow. Run dry-run first.\n",
                encoding="utf-8",
            )

            config = install_into_repo.load_install_config(
                target=target,
                bootstrap=target / "workflow-implementation.md",
            )

            self.assertEqual(config["project_name"], "my-python-repo")
            self.assertEqual(config["language"], "python")
            self.assertEqual(config["source_dir"], "app")
            self.assertEqual(config["test_dir"], "spec")
            self.assertEqual(
                config["test_command"],
                "python -m unittest discover -s spec -p 'test_*.py'",
            )

    def test_detects_node_repo_without_user_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "my-node-repo"
            target.mkdir()
            (target / "package.json").write_text(
                '{"scripts": {"test": "vitest run"}}\n',
                encoding="utf-8",
            )
            (target / "lib").mkdir()
            (target / "test").mkdir()

            config = install_into_repo.load_install_config(
                target=target,
                bootstrap=target / "workflow-implementation.md",
            )

            self.assertEqual(config["language"], "node")
            self.assertEqual(config["source_dir"], "lib")
            self.assertEqual(config["test_dir"], "test")
            self.assertEqual(config["test_command"], "npm test")

    def test_bootstrap_yaml_overrides_detected_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "detected-name"
            target.mkdir()
            (target / "package.json").write_text('{"scripts": {"test": "jest"}}\n', encoding="utf-8")
            (target / "workflow-implementation.md").write_text(
                """
```yaml
project_name: Manual Name
language: python
source_dir: service
test_dir: checks
test_command: python -m unittest discover -s checks -p 'check_*.py'
```
""",
                encoding="utf-8",
            )

            config = install_into_repo.load_install_config(
                target=target,
                bootstrap=target / "workflow-implementation.md",
            )

            self.assertEqual(config["project_name"], "Manual Name")
            self.assertEqual(config["language"], "python")
            self.assertEqual(config["source_dir"], "service")
            self.assertEqual(config["test_dir"], "checks")
            self.assertEqual(
                config["test_command"],
                "python -m unittest discover -s checks -p 'check_*.py'",
            )

    def test_bootstrap_url_overrides_detected_values_without_local_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target-repo"
            target.mkdir()
            (target / "package.json").write_text('{"scripts": {"test": "vitest"}}\n', encoding="utf-8")
            bootstrap_text = """
```yaml
project_name: Remote Bootstrap Repo
language: python
source_dir: service
test_dir: checks
test_command: python -m unittest discover -s checks -p 'check_*.py'
```
"""

            config = install_into_repo.load_install_config(
                target=target,
                bootstrap=target / "workflow-implementation.md",
                bootstrap_text=bootstrap_text,
            )

            self.assertEqual(config["project_name"], "Remote Bootstrap Repo")
            self.assertEqual(config["language"], "python")
            self.assertEqual(config["source_dir"], "service")
            self.assertEqual(config["test_dir"], "checks")
            self.assertEqual(
                config["test_command"],
                "python -m unittest discover -s checks -p 'check_*.py'",
            )

    def test_github_blob_url_is_converted_to_raw_url(self) -> None:
        self.assertEqual(
            install_into_repo.normalize_bootstrap_url(
                "https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md"
            ),
            "https://raw.githubusercontent.com/clip968/docs-first-workflow/main/workflow-implementation.md",
        )

    def test_dry_run_prints_install_plan_without_writing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template = Path(tmp) / "template"
            target = Path(tmp) / "target"
            template.mkdir()
            target.mkdir()
            (template / "AGENTS.md").write_text("Project: {{PROJECT_NAME}}\n", encoding="utf-8")
            (template / "scripts").mkdir()
            (template / "scripts" / "finish_task.py").write_text("# finish\n", encoding="utf-8")
            (target / "workflow-implementation.md").write_text(
                """
# Workflow Implementation

```yaml
project_name: Existing Repo
source_dir: app
test_dir: spec
test_command: python -m unittest discover -s spec -p 'test_*.py'
```
""",
                encoding="utf-8",
            )

            output = io.StringIO()
            bootstrap_url = "https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md"
            with redirect_stdout(output):
                with mock.patch.object(
                    install_into_repo,
                    "fetch_bootstrap_url",
                    return_value="project_name: Remote Existing Repo\n",
                ):
                    exit_code = install_into_repo.main(
                        [
                            "--target",
                            str(target),
                            "--template-root",
                            str(template),
                            "--bootstrap-url",
                            bootstrap_url,
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertIn("DRY RUN", output.getvalue())
            self.assertIn("This will install docs-first workflow", output.getvalue())
            self.assertIn(f"Bootstrap URL: {bootstrap_url}", output.getvalue())
            self.assertIn("Detected config:", output.getvalue())
            self.assertIn("Project: Remote Existing Repo", output.getvalue())
            self.assertIn("Would create:", output.getvalue())
            self.assertIn("AGENTS.md", output.getvalue())
            self.assertIn("Directory tree after install:", output.getvalue())
            self.assertIn("Run again with --apply", output.getvalue())
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / "scripts" / "finish_task.py").exists())

    def test_apply_writes_files_after_explicit_approval_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template = Path(tmp) / "template"
            target = Path(tmp) / "target"
            template.mkdir()
            target.mkdir()
            (template / "AGENTS.md").write_text("Project: {{PROJECT_NAME}}\n", encoding="utf-8")
            (template / "docs").mkdir()
            (template / "docs" / "WORKFLOW.md").write_text(
                "Test command: {{TEST_COMMAND}}\n", encoding="utf-8"
            )
            (target / "workflow-implementation.md").write_text(
                """
```yaml
project_name: Existing Repo
test_command: python -m unittest discover -s tests -p 'test_*.py'
```
""",
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = install_into_repo.main(
                    [
                        "--target",
                        str(target),
                        "--template-root",
                        str(template),
                        "--apply",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                "Project: Existing Repo\n",
            )
            self.assertIn(
                "python -m unittest discover -s tests -p 'test_*.py'",
                (target / "docs" / "WORKFLOW.md").read_text(encoding="utf-8"),
            )

    def test_apply_preserves_existing_files_by_writing_conflict_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template = Path(tmp) / "template"
            target = Path(tmp) / "target"
            template.mkdir()
            target.mkdir()
            (template / "AGENTS.md").write_text("template agents\n", encoding="utf-8")
            (target / "AGENTS.md").write_text("existing agents\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = install_into_repo.main(
                    [
                        "--target",
                        str(target),
                        "--template-root",
                        str(template),
                        "--apply",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "existing agents\n")
            self.assertEqual(
                (target / "AGENTS.md.docs-first-workflow.new").read_text(encoding="utf-8"),
                "template agents\n",
            )


if __name__ == "__main__":
    unittest.main()
