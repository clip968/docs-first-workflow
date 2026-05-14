# Spec: Agent Workflow

## Status

- Draft [ ] / Accepted [X] / Deprecated [ ]

## Context

This project uses AI-assisted development. This spec defines the workflow that agents (and human developers) must follow when making changes.

## Goals

- Define a repeatable, verifiable workflow for all code changes
- Ensure documentation stays synchronized with implementation
- Provide traceability from requirements to tests to code

## Non-goals

- This spec does NOT define project-specific implementation details
- This spec does NOT cover how external tools (Notion, CI, etc.) are configured

## Requirements

- REQ-WF-001: Before starting work, agents must read `docs/WORKFLOW.md`, `docs/handoff/CURRENT_HANDOFF.md`, and the relevant spec for the files being changed.
- REQ-WF-002: Non-trivial behavior changes require a spec before implementation.
- REQ-WF-003: ADRs are required only for hard-to-reverse technical decisions.
- REQ-WF-004: Execution plans in `docs/plans/` must split work into test-sized slices.
- REQ-WF-005: Each behavior-changing task must start with a failing test.
- REQ-WF-006: If a failing test cannot be written first, the plan must document the reason and alternative verification.
- REQ-WF-007: Docs freshness check (`check_docs_freshness.py`) must pass before a task is considered complete.
- REQ-WF-008: Handoff must be updated before running the final validation gate.
- REQ-WF-009: Agents must NOT commit or push unless explicitly requested.

## Acceptance Criteria

- AC-WF-001: A new feature implemented via this workflow produces: spec -> plan -> failing test -> implementation -> passing test -> docs update -> handoff update -> finish gate pass.
- AC-WF-002: Docs freshness check catches missing documentation changes and reports them in human-readable format.

## Test Mapping

- TEST-WF-001:
  - Covers: REQ-WF-007
  - Command: `python scripts/check_docs_freshness.py --all`

## Docs Ownership

- Code paths: `scripts/check_docs_freshness.py`, `scripts/finish_task.py`, `.github/workflows/**/*.yml`, `.pre-commit-config.yaml`
- Required docs: `docs/WORKFLOW.md`
- Runbooks: `docs/runbooks/finish-task.md`

## Open Questions

- (none)

## Verification

```bash
{{TEST_COMMAND}}
```
