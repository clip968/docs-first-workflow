#!/usr/bin/env python3
"""
install_into_repo.py - Install docs-first workflow into an existing repository.

Default mode is a dry run. It prints the files that would be created or written
as conflict copies. Use --apply only after reviewing the plan.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen


BOOTSTRAP_FILE = "workflow-implementation.md"
CONFLICT_SUFFIX = ".docs-first-workflow.new"

PLACEHOLDERS = {
    "{{PROJECT_NAME}}": "project_name",
    "{{LANGUAGE}}": "language",
    "{{TEST_COMMAND}}": "test_command",
    "{{SOURCE_DIR}}": "source_dir",
    "{{TEST_DIR}}": "test_dir",
}

DEFAULT_CONFIG = {
    "project_name": "",
    "language": "python",
    "source_dir": "src",
    "test_dir": "tests",
    "test_command": "python -m unittest discover -s tests -p 'test_*.py'",
}

DEFAULT_INSTALL_PATHS = [
    "AGENTS.md",
    ".github/pull_request_template.md",
    ".github/workflows/docs-freshness.yml",
    ".pre-commit-config.yaml",
    "docs/README.md",
    "docs/INDEX.md",
    "docs/WORKFLOW.md",
    "docs/DOC_OWNERS.yml",
    "docs/specs/0000-project-overview.md",
    "docs/specs/0001-agent-workflow.md",
    "docs/adrs/0001-docs-as-source-of-truth.md",
    "docs/plans/.gitkeep",
    "docs/reports/.gitkeep",
    "docs/runbooks/test.md",
    "docs/runbooks/finish-task.md",
    "docs/handoff/CURRENT_HANDOFF.md",
    "docs/handoff/history/.gitkeep",
    "docs/templates/ADR_TEMPLATE.md",
    "docs/templates/HANDOFF_TEMPLATE.md",
    "docs/templates/PLAN_TEMPLATE.md",
    "docs/templates/REPORT_TEMPLATE.md",
    "docs/templates/RUNBOOK_TEMPLATE.md",
    "docs/templates/SPEC_TEMPLATE.md",
    "docs/templates/WORKFLOW_IMPLEMENTATION_TEMPLATE.md",
    "scripts/check_docs_freshness.py",
    "scripts/finish_task.py",
    "scripts/install_into_repo.py",
]


@dataclass(frozen=True)
class InstallAction:
    kind: str
    source: Path
    destination: Path
    relative_path: str
    content: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install docs-first workflow into an existing repository."
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Existing repository to install into (default: current directory).",
    )
    parser.add_argument(
        "--template-root",
        default=".",
        help="docs-first-workflow repository root (default: current directory).",
    )
    parser.add_argument(
        "--bootstrap",
        default=BOOTSTRAP_FILE,
        help="Bootstrap markdown file inside target or absolute path.",
    )
    parser.add_argument(
        "--bootstrap-url",
        help="Remote bootstrap markdown URL. GitHub blob URLs are converted to raw URLs.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write files. Omit this flag to print a dry-run preview only.",
    )
    return parser.parse_args(argv)


def parse_bootstrap_config(path: Path, target: Path) -> dict[str, str]:
    config: dict[str, str] = {}

    if not path.exists():
        return config

    return parse_bootstrap_text(path.read_text(encoding="utf-8"))


def parse_bootstrap_text(text: str) -> dict[str, str]:
    config: dict[str, str] = {}
    in_fence = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            language = stripped.removeprefix("```").strip().casefold()
            in_fence = not in_fence if not language or language in {"yaml", "yml"} else in_fence
            continue
        if not in_fence and not stripped.startswith(tuple(DEFAULT_CONFIG)):
            continue
        if ":" not in stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split(":", 1)
        normalized_key = key.strip()
        if normalized_key not in DEFAULT_CONFIG:
            continue
        config[normalized_key] = unquote_scalar(value.strip())

    return config


def load_install_config(
    *,
    target: Path,
    bootstrap: Path,
    bootstrap_text: str | None = None,
) -> dict[str, str]:
    config = detect_repo_config(target)
    if bootstrap_text is not None:
        config.update(parse_bootstrap_text(bootstrap_text))
    else:
        config.update(parse_bootstrap_config(bootstrap, target))
    config["test_command"] = test_command_for_config(config, target)
    return config


def normalize_bootstrap_url(url: str) -> str:
    marker = "https://github.com/"
    if not url.startswith(marker) or "/blob/" not in url:
        return url
    owner_repo_and_path = url.removeprefix(marker)
    owner, repo, remainder = owner_repo_and_path.split("/", 2)
    branch, path = remainder.removeprefix("blob/").split("/", 1)
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"


def fetch_bootstrap_url(url: str) -> str:
    normalized_url = normalize_bootstrap_url(url)
    with urlopen(normalized_url, timeout=15) as response:
        return response.read().decode("utf-8")


def detect_repo_config(target: Path) -> dict[str, str]:
    language = detect_language(target)
    source_dir = detect_first_existing_dir(target, ["src", "app", "lib"], DEFAULT_CONFIG["source_dir"])
    test_dir = detect_first_existing_dir(target, ["tests", "test", "spec"], DEFAULT_CONFIG["test_dir"])
    return {
        "project_name": target.name,
        "language": language,
        "source_dir": source_dir,
        "test_dir": test_dir,
        "test_command": test_command_for_language(language, test_dir, target),
    }


def detect_language(target: Path) -> str:
    if (target / "package.json").exists():
        return "node"
    if (target / "go.mod").exists():
        return "go"
    if (target / "Cargo.toml").exists():
        return "rust"
    if any((target / name).exists() for name in ("pyproject.toml", "requirements.txt", "setup.py")):
        return "python"
    return DEFAULT_CONFIG["language"]


def detect_first_existing_dir(target: Path, candidates: list[str], default: str) -> str:
    for candidate in candidates:
        if (target / candidate).is_dir():
            return candidate
    return default


def test_command_for_config(config: dict[str, str], target: Path) -> str:
    explicit = config.get("test_command")
    if explicit:
        return explicit
    return test_command_for_language(config["language"], config["test_dir"], target)


def test_command_for_language(language: str, test_dir: str, target: Path) -> str:
    if language == "node":
        return "npm test"
    if language == "go":
        return "go test ./..."
    if language == "rust":
        return "cargo test"
    return f"python -m unittest discover -s {test_dir} -p 'test_*.py'"


def unquote_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def bootstrap_path(target: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    return candidate if candidate.is_absolute() else target / candidate


def render_template(text: str, config: dict[str, str]) -> str:
    rendered = text
    for placeholder, config_key in PLACEHOLDERS.items():
        rendered = rendered.replace(placeholder, config[config_key])
    rendered = rendered.replace("<test command>", config["test_command"])
    return rendered


def collect_actions(
    *,
    template_root: Path,
    target: Path,
    config: dict[str, str],
) -> list[InstallAction]:
    actions: list[InstallAction] = []

    for relative_path in DEFAULT_INSTALL_PATHS:
        source = template_root / relative_path
        if not source.exists() or not source.is_file():
            continue

        content = render_template(source.read_text(encoding="utf-8"), config)
        destination = target / relative_path

        if destination.exists():
            existing = destination.read_text(encoding="utf-8")
            if existing == content:
                actions.append(
                    InstallAction("skip_identical", source, destination, relative_path, content)
                )
            else:
                actions.append(
                    InstallAction(
                        "conflict_copy",
                        source,
                        destination.with_name(destination.name + CONFLICT_SUFFIX),
                        relative_path,
                        content,
                    )
                )
        else:
            actions.append(InstallAction("create", source, destination, relative_path, content))

    return actions


def planned_tree(actions: list[InstallAction]) -> list[str]:
    installed_paths = sorted(
        action.destination.as_posix()
        for action in actions
        if action.kind in {"create", "conflict_copy", "skip_identical"}
    )
    return installed_paths


def print_plan(
    *,
    target: Path,
    bootstrap: Path,
    bootstrap_url: str | None,
    config: dict[str, str],
    actions: list[InstallAction],
    apply: bool,
) -> None:
    mode = "APPLY" if apply else "DRY RUN"
    print(f"{mode}: docs-first workflow installer")
    print(f"This will install docs-first workflow into: {target}")
    if bootstrap_url:
        print(f"Bootstrap URL: {bootstrap_url}")
    else:
        print(f"Bootstrap file: {bootstrap}")
    print("\nDetected config:")
    print(f"Project: {config['project_name']}")
    print(f"Language: {config['language']}")
    print(f"Source dir: {config['source_dir']}")
    print(f"Test dir: {config['test_dir']}")
    print(f"Test command: {config['test_command']}")

    sections = [
        ("create", "Would create:" if not apply else "Created:"),
        (
            "conflict_copy",
            "Would write conflict copies:" if not apply else "Wrote conflict copies:",
        ),
        ("skip_identical", "Would skip identical:" if not apply else "Skipped identical:"),
    ]
    for kind, label in sections:
        paths = [action.destination.relative_to(target).as_posix() for action in actions if action.kind == kind]
        if not paths:
            continue
        print(f"\n{label}")
        for path in paths:
            print(f"  - {path}")

    print("\nDirectory tree after install:")
    for path in planned_tree(actions):
        try:
            display_path = Path(path).relative_to(target).as_posix()
        except ValueError:
            display_path = path
        print(f"  {display_path}")

    if not apply:
        print("\nNo files were written. Run again with --apply after reviewing this plan.")


def apply_actions(actions: list[InstallAction]) -> None:
    for action in actions:
        if action.kind == "skip_identical":
            continue
        action.destination.parent.mkdir(parents=True, exist_ok=True)
        action.destination.write_text(action.content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = Path(args.target).resolve()
    template_root = Path(args.template_root).resolve()
    bootstrap = bootstrap_path(target, args.bootstrap).resolve()

    if not target.exists() or not target.is_dir():
        print(f"ERROR: target directory does not exist: {target}")
        return 1
    if not template_root.exists() or not template_root.is_dir():
        print(f"ERROR: template root does not exist: {template_root}")
        return 1

    bootstrap_text = fetch_bootstrap_url(args.bootstrap_url) if args.bootstrap_url else None
    config = load_install_config(
        target=target,
        bootstrap=bootstrap,
        bootstrap_text=bootstrap_text,
    )
    actions = collect_actions(template_root=template_root, target=target, config=config)
    print_plan(
        target=target,
        bootstrap=bootstrap,
        bootstrap_url=args.bootstrap_url,
        config=config,
        actions=actions,
        apply=args.apply,
    )

    if args.apply:
        apply_actions(actions)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
