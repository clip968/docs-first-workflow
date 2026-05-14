# Spec: Project Overview

## Status

- Draft [ ] / Accepted [X] / Deprecated [ ]

## Context

This repository follows a docs-first agent workflow. This spec defines the overall project architecture and the contract that all code must satisfy.

## Goals

- Define the project's high-level architecture
- Establish the docs-first workflow as the development standard
- Define code quality and documentation requirements

## Non-goals

- This spec does NOT define implementation details for specific features
- This spec does NOT replace per-feature specs

## Requirements

- REQ-PRJ-001: Code changes must be accompanied by related documentation changes in the same working tree.
- REQ-PRJ-002: Behavior-changing code must follow the TDD workflow (failing test -> implementation -> passing test).
- REQ-PRJ-003: All code paths must be covered by DOC_OWNERS rules.
- REQ-PRJ-004: Every session must update `docs/handoff/CURRENT_HANDOFF.md` before validation.

## Acceptance Criteria

- AC-PRJ-001: Running `python scripts/finish_task.py` passes without errors.
- AC-PRJ-002: Running `python scripts/check_docs_freshness.py --all` passes after any code change with matching docs.

## Test Mapping

- TEST-PRJ-001:
  - Covers: REQ-PRJ-001, REQ-PRJ-002, REQ-PRJ-003
  - Command: `python -m unittest discover -s tests -p "test_*.py"`

## Docs Ownership

- Code paths: `{{SOURCE_DIR}}/**/*.py`, `app/**/*.py`
- Required docs: `docs/specs/0000-project-overview.md`
- Runbooks: `docs/runbooks/test.md`

## Open Questions

- (none)

## Verification

```bash
{{TEST_COMMAND}}
```
