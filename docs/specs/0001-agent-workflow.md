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
- REQ-WF-010: Plans intended for lower-trust or open-source model execution must define allowed files, required docs, red test or alternate verification, and final verification commands.
- REQ-WF-011: Code-changing tasks must update handoff and at least one relevant contract or procedure doc unless the plan explicitly explains why the existing contract remains unchanged.
- REQ-WF-012: DOC_OWNERS overlap must resolve by stable ownership specificity. Current task urgency must not change DOC_OWNERS priority.
- REQ-WF-013: Spike work must not change production behavior and must record investigation output in `docs/reports/` before converting to implementation work.
- REQ-WF-014: `CURRENT_HANDOFF.md` must stay focused on current state; detailed past logs belong in `docs/handoff/history/`.
- REQ-WF-015: Repositories using this template should include a root `AGENTS.md` and `docs/INDEX.md` so multiple agent tools share the same operating rules and routing map.

## Acceptance Criteria

- AC-WF-001: A new feature implemented via this workflow produces: spec -> plan -> failing test -> implementation -> passing test -> docs update -> handoff update -> finish gate pass.
- AC-WF-002: Docs freshness check catches missing documentation changes and reports them in human-readable format.
- AC-WF-003: A task plan can be handed to a lower-trust executor without relying on unstated context because it names scope, required docs, tests, and finish gate.
- AC-WF-004: When broad and specific DOC_OWNERS rules overlap, changing only the broad rule's docs does not satisfy the specific rule's contract freshness.
- AC-WF-005: Spike output can be stored as a report, but report-only changes cannot satisfy DOC_OWNERS owner requirements for code changes.

## Test Mapping

- TEST-WF-001:
  - Covers: REQ-WF-007, REQ-WF-012, AC-WF-004, AC-WF-005
  - Command: `python scripts/check_docs_freshness.py --all`
- TEST-WF-002:
  - Covers: REQ-WF-010, REQ-WF-011
  - Command: Review `docs/templates/PLAN_TEMPLATE.md` and `docs/WORKFLOW.md` sections for required executor fields.
- TEST-WF-003:
  - Covers: REQ-WF-013, REQ-WF-014, REQ-WF-015
  - Command: Review `docs/WORKFLOW.md`, `docs/templates/HANDOFF_TEMPLATE.md`, `AGENTS.md`, and `docs/INDEX.md`.

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
