"""
Tests for check_docs_freshness.py.

These tests use the new DOC_OWNERS schema (version 1 with rules)
to verify the docs freshness validation logic.

Run:
    python -m unittest discover -s tests -p "test_*.py"
    # or override with env:
    WORKFLOW_TEST_COMMAND="python -m unittest discover -s tests -p 'test_*.py'" python scripts/finish_task.py
"""

from __future__ import annotations

import argparse
import os
import unittest
from unittest import mock

from scripts import check_docs_freshness


NEW_DOC_OWNERS = """
version: 1

policy:
  unmatched_code: fail
  archive_docs_are_invalid_owners: true
  external_index_is_invalid_owner: true
  handoff_only_satisfies_contract: false

code_paths:
  - "src/**/*.py"
  - "scripts/**/*.py"
  - "tests/**/*.py"

ignored_paths:
  - "docs/**"
  - "data/**"
  - "__pycache__/**"
  - "*.pyc"

global_required_on_code_change:
  changed:
    - "docs/handoff/CURRENT_HANDOFF.md"

rules:
  - id: project-core
    paths:
      - "src/**/*.py"
    contract_docs:
      - "docs/specs/0000-project-overview.md"
    procedure_docs:
      - "docs/runbooks/test.md"
"""


LEGACY_DOC_OWNERS = """
src/foo.py:
  required_docs:
    - docs/specs/0000-project-overview.md
    - docs/runbooks/test.md
    - docs/handoff/CURRENT_HANDOFF.md
"""


OVERLAPPING_DOC_OWNERS = """
version: 1

policy:
  unmatched_code: fail
  multiple_matches: require_highest_priority
  fallback_rules_allowed: true

code_paths:
  - "src/**/*.py"

global_required_on_code_change:
  changed:
    - "docs/handoff/CURRENT_HANDOFF.md"

rules:
  - id: broad-python
    priority: 30
    fallback: true
    paths:
      - "src/**/*.py"
    contract_docs:
      - "docs/specs/broad-python.md"

  - id: guide-ff14-crawler
    priority: 90
    paths:
      - "src/guide_ff14/**/*.py"
    contract_docs:
      - "docs/specs/guide-ff14-crawler.md"
"""


AMBIGUOUS_DOC_OWNERS = """
version: 1

policy:
  unmatched_code: fail
  multiple_matches: require_highest_priority

code_paths:
  - "src/**/*.py"

global_required_on_code_change:
  changed:
    - "docs/handoff/CURRENT_HANDOFF.md"

rules:
  - id: crawler-a
    priority: 90
    paths:
      - "src/guide_ff14/**/*.py"
    contract_docs:
      - "docs/specs/crawler-a.md"

  - id: crawler-b
    priority: 90
    paths:
      - "src/guide_ff14/**/*.py"
    contract_docs:
      - "docs/specs/crawler-b.md"
"""


class CheckDocsFreshnessTests(unittest.TestCase):
    """Test suite for check_docs_freshness.py core logic."""

    def config(self) -> check_docs_freshness.DocOwnersConfig:
        return check_docs_freshness.load_doc_owners_from_text(NEW_DOC_OWNERS)

    # --- Test 1: code file changed + matching contract doc changed => pass ---
    def test_code_file_with_matching_contract_and_handoff_passes(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/specs/0000-project-overview.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            self.config(),
        )

        self.assertFalse(result.should_fail)
        self.assertEqual(result.missing_rule_docs, {})
        self.assertEqual(result.missing_global_docs, [])

    # --- Test 2: code file changed + only handoff changed => fail ---
    def test_code_file_with_only_handoff_changed_fails_contract_freshness(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            self.config(),
        )

        self.assertTrue(result.should_fail)
        self.assertIn("src/foo.py", result.missing_rule_docs)
        detail = result.missing_rule_docs["src/foo.py"]
        self.assertEqual(detail["rule"], "project-core")
        self.assertIn("docs/specs/0000-project-overview.md", detail["required_docs"])

    # --- Test 3: code file changed + no matching rule => fail ---
    def test_code_file_with_no_matching_doc_owners_rule_fails(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "scripts/new_tool.py",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            self.config(),
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(result.unmatched_code_files, ["scripts/new_tool.py"])

    def test_overlapping_rule_requires_highest_priority_doc(self) -> None:
        config = check_docs_freshness.load_doc_owners_from_text(OVERLAPPING_DOC_OWNERS)

        result = check_docs_freshness.evaluate_freshness(
            [
                "src/guide_ff14/item_extractor.py",
                "docs/specs/broad-python.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            config,
        )

        self.assertTrue(result.should_fail)
        self.assertIn("src/guide_ff14/item_extractor.py", result.missing_rule_docs)
        detail = result.missing_rule_docs["src/guide_ff14/item_extractor.py"]
        self.assertEqual(detail["rule"], "guide-ff14-crawler")
        self.assertEqual(detail["required_docs"], ["docs/specs/guide-ff14-crawler.md"])

    def test_overlapping_rule_passes_when_highest_priority_doc_is_fresh(self) -> None:
        config = check_docs_freshness.load_doc_owners_from_text(OVERLAPPING_DOC_OWNERS)

        result = check_docs_freshness.evaluate_freshness(
            [
                "src/guide_ff14/item_extractor.py",
                "docs/specs/guide-ff14-crawler.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            config,
        )

        self.assertFalse(result.should_fail)

    def test_fallback_rule_applies_when_no_specific_rule_matches(self) -> None:
        config = check_docs_freshness.load_doc_owners_from_text(OVERLAPPING_DOC_OWNERS)

        result = check_docs_freshness.evaluate_freshness(
            [
                "src/shared/parser.py",
                "docs/specs/broad-python.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            config,
        )

        self.assertFalse(result.should_fail)

    def test_same_highest_priority_matches_are_ambiguous(self) -> None:
        config = check_docs_freshness.load_doc_owners_from_text(AMBIGUOUS_DOC_OWNERS)

        result = check_docs_freshness.evaluate_freshness(
            [
                "src/guide_ff14/item_extractor.py",
                "docs/specs/crawler-a.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            config,
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(
            result.ambiguous_rule_matches,
            {
                "src/guide_ff14/item_extractor.py": {
                    "priority": 90,
                    "rules": ["crawler-a", "crawler-b"],
                }
            },
        )

    # --- Test 4: code file changed + missing global handoff => fail ---
    def test_code_file_with_contract_doc_but_missing_global_handoff_fails(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/specs/0000-project-overview.md",
            ],
            self.config(),
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(result.missing_global_docs, ["docs/handoff/CURRENT_HANDOFF.md"])
        self.assertEqual(result.missing_rule_docs, {})

    # --- Test 5: ignored path changed => pass ---
    def test_ignored_path_change_is_ignored_and_passes(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "data/input.json",
                "src/__pycache__/foo.cpython-312.pyc",
            ],
            self.config(),
        )

        self.assertFalse(result.should_fail)
        self.assertFalse(result.classification["code_change"])

    # --- Test 6: archive doc cannot satisfy owner requirement ---
    def test_archive_doc_does_not_count_as_owner(self) -> None:
        text = NEW_DOC_OWNERS.replace(
            "docs/specs/0000-project-overview.md",
            "docs/archive/old-project-overview.md",
        )
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/archive/old-project-overview.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            check_docs_freshness.load_doc_owners_from_text(text),
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(
            result.invalid_owner_docs,
            {"project-core": ["docs/archive/old-project-overview.md"]},
        )

    # --- Test 7: external URL cannot satisfy owner requirement ---
    def test_external_doc_does_not_count_as_owner(self) -> None:
        text = NEW_DOC_OWNERS.replace(
            "docs/specs/0000-project-overview.md",
            "https://notion.so/example-page",
        )
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            check_docs_freshness.load_doc_owners_from_text(text),
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(
            result.invalid_owner_docs,
            {"project-core": ["https://notion.so/example-page"]},
        )

    def test_plan_and_report_docs_do_not_count_as_owners(self) -> None:
        text = NEW_DOC_OWNERS.replace(
            "docs/specs/0000-project-overview.md",
            "docs/plans/implementation-plan.md",
        ).replace(
            "docs/runbooks/test.md",
            "docs/reports/spike-report.md",
        )
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/plans/implementation-plan.md",
                "docs/reports/spike-report.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            check_docs_freshness.load_doc_owners_from_text(text),
        )

        self.assertTrue(result.should_fail)
        self.assertEqual(
            result.invalid_owner_docs,
            {
                "project-core": [
                    "docs/plans/implementation-plan.md",
                    "docs/reports/spike-report.md",
                ]
            },
        )

    # --- Test 8: legacy schema compatibility ---
    def test_legacy_doc_owners_schema_still_works(self) -> None:
        config = check_docs_freshness.load_doc_owners_from_text(LEGACY_DOC_OWNERS)
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/runbooks/test.md",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            config,
        )

        self.assertFalse(result.should_fail)
        self.assertEqual([rule.id for rule in config.rules], ["legacy:src/foo.py"])

    # --- Test 9: limited YAML parser without PyYAML ---
    def test_limited_yaml_parser_supports_new_schema_without_pyyaml(self) -> None:
        with mock.patch.object(check_docs_freshness, "yaml", None):
            config = check_docs_freshness.load_doc_owners_from_text(NEW_DOC_OWNERS)

        self.assertEqual(config.policy["unmatched_code"], "fail")
        self.assertEqual(config.global_required_on_code_change, ["docs/handoff/CURRENT_HANDOFF.md"])
        self.assertEqual(config.rules[0].id, "project-core")
        self.assertEqual(config.rules[0].paths, ["src/**/*.py"])

    def test_limited_yaml_parser_supports_priority_and_fallback(self) -> None:
        with mock.patch.object(check_docs_freshness, "yaml", None):
            config = check_docs_freshness.load_doc_owners_from_text(OVERLAPPING_DOC_OWNERS)

        self.assertEqual(config.policy["multiple_matches"], "require_highest_priority")
        self.assertEqual(config.policy["fallback_rules_allowed"], True)
        self.assertEqual(config.rules[0].priority, 30)
        self.assertEqual(config.rules[0].fallback, True)
        self.assertEqual(config.rules[1].priority, 90)
        self.assertEqual(config.rules[1].fallback, False)

    # --- Test 10: reviewed docs can optionally satisfy ---
    def test_reviewed_docs_can_optionally_satisfy_contract_docs(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            [
                "src/foo.py",
                "docs/handoff/CURRENT_HANDOFF.md",
            ],
            self.config(),
            reviewed_docs={"docs/runbooks/test.md"},
            allow_reviewed_docs=True,
        )

        self.assertFalse(result.should_fail)

    # --- Test 11: docs-only change passes ---
    def test_docs_file_only_change_passes(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            ["docs/specs/0000-project-overview.md"],
            self.config(),
        )

        self.assertFalse(result.should_fail)
        self.assertFalse(result.classification["code_change"])
        self.assertTrue(result.classification["docs_change"])

    def test_index_and_reports_are_classified_as_docs(self) -> None:
        classification = check_docs_freshness.classify_changed_files(
            ["docs/INDEX.md", "docs/reports/html-fixture-spike.md"],
            self.config(),
        )

        self.assertEqual(
            classification["docs_files"],
            ["docs/INDEX.md", "docs/reports/html-fixture-spike.md"],
        )
        self.assertEqual(classification["other_files"], [])

    # --- Test 12: override passes even without docs ---
    def test_override_passes_even_without_docs(self) -> None:
        result = check_docs_freshness.evaluate_freshness(
            ["src/foo.py"],
            self.config(),
            override=True,
        )

        self.assertFalse(result.should_fail)

    # --- Test 13: env override passes CLI check ---
    def test_env_override_passes_cli_check(self) -> None:
        with mock.patch.dict(os.environ, {"DOCS_UPDATE_NOT_REQUIRED": "1"}):
            with mock.patch.object(
                check_docs_freshness,
                "changed_files_from_args",
                return_value=["src/foo.py"],
            ):
                with mock.patch.object(
                    check_docs_freshness,
                    "load_doc_owners",
                    return_value=self.config(),
                ):
                    exit_code = check_docs_freshness.main(["--staged"])

        self.assertEqual(exit_code, 0)

    # --- Test 14: all mode collects staged, unstaged, and untracked ---
    def test_all_mode_collects_staged_unstaged_and_untracked(self) -> None:
        args = argparse.Namespace(staged=False, all=True, base=None, head=None)

        def fake_git_name_only(git_args: list[str]) -> list[str]:
            if git_args == ["diff", "--cached", "--name-only"]:
                return ["scripts/check_docs_freshness.py"]
            if git_args == ["diff", "--name-only"]:
                return ["docs/WORKFLOW.md"]
            if git_args == ["ls-files", "--others", "--exclude-standard"]:
                return ["docs/DOC_OWNERS.yml"]
            return []

        with mock.patch.object(
            check_docs_freshness,
            "run_git_name_only",
            side_effect=fake_git_name_only,
        ):
            paths = check_docs_freshness.changed_files_from_args(args)

        self.assertEqual(
            paths,
            [
                "scripts/check_docs_freshness.py",
                "docs/WORKFLOW.md",
                "docs/DOC_OWNERS.yml",
            ],
        )


if __name__ == "__main__":
    unittest.main()
