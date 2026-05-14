# Docs-First Agent Workflow

The source of truth for this project is the repository-internal `docs/` directory. External tools (Notion, Confluence, wiki, etc.) are NOT the source of truth. They serve as mirror/index only — for handoff summaries, links, or indices.

## Core Flow

Every non-trivial code change follows this sequence:

```text
1. Work start check
2. Requirement confirmation
3. Related spec review
4. Write spec (if none exists)
5. Write ADR (if technical decision is needed)
6. Break spec into feature/test-sized tasks
7. For each task: write a failing test
8. Confirm failing test fails
9. Minimal implementation
10. Confirm test passes
11. Update related docs/specs/runbooks
12. Update docs/handoff/CURRENT_HANDOFF.md
13. Run python scripts/finish_task.py
14. Update external index/mirror (if applicable)
```

## Work Start Check

Before any work, check the current repository state:

```bash
git status --short
git branch --show-current
git log --oneline -5
git diff --stat
```

Then read at minimum:

1. `docs/README.md`
2. `docs/WORKFLOW.md`
3. `docs/handoff/CURRENT_HANDOFF.md`
4. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/` for the files you will touch

Do not revert existing uncommitted changes. Do not touch files unrelated to the current task.

## Spec Contract

Implementation is governed by spec contracts. If a relevant spec exists, read it first. If none exists, create a minimal spec in `docs/specs/` before implementation.

A spec must clearly define:

- Scope and out-of-scope
- Inputs, outputs, storage rules
- Error handling and mode-specific behavior (e.g., dry-run vs. apply)
- Requirement IDs and acceptance criteria
- Test mappings

Small documentation-only changes may proceed without a new spec. Any behavior-changing code change must confirm or create a spec first.

## ADR Guidelines

Not every change needs an ADR. Create one in `docs/adrs/` when:

- The decision is hard to reverse (technology choices, architecture decisions)
- The change affects source of truth, storage, or external system boundaries
- The change has long-term impact on testing, deployment, or operations
- Multiple reasonable alternatives exist, and the reasoning should be recorded

ADRs do not replace specs. ADRs record *why* a decision was made; specs record *what* the implementation must conform to.

## Plan Guidelines

Before non-trivial implementation, create a small execution plan in `docs/plans/`.

A plan includes:

- Related contract (spec, ADR, runbook references)
- Scope and out-of-scope
- Files to change
- For each task: red test name, implementation approach, verification method
- Done-when conditions

Plans are ephemeral execution guides. They are NOT long-term contracts, NOT source of truth, and do NOT satisfy DOC_OWNERS freshness requirements.

## TDD Rules

Behavior-changing code changes MUST start with a failing test.

```text
failing test -> implementation -> passing test
```

If a red test cannot be written first (e.g., the change is configuration, infrastructure, or documentation-only), the plan must explain why and name an alternative verification method.

## Docs Update Rules

After code changes, update the related documentation in the same working tree:

| Change type | Document to update |
|---|---|
| Behavior contract change | `docs/specs/` |
| Repeatable procedure change | `docs/runbooks/` |
| Technical decision change | `docs/adrs/` |
| Session/agent state change | `docs/handoff/CURRENT_HANDOFF.md` |

- `docs/archive/` documents are NOT valid contract owners.
- External tool documents (Notion, Confluence, etc.) are NOT valid contract owners.
- `docs/plans/` documents are NOT valid contract owners.

## Handoff Rules

`docs/handoff/CURRENT_HANDOFF.md` is the global state document for every code change. Update it whenever code changes.

The handoff must contain:

- Completed changes
- Related spec/runbook/ADR/plan references
- Validation commands and results
- Remaining TODO items
- Scope boundaries (what not to touch)

**Important:** The handoff alone does NOT satisfy per-path contract freshness. Changing only `CURRENT_HANDOFF.md` without updating the corresponding contract docs (specs or runbooks) will FAIL the docs freshness check.

## DOC_OWNERS Policy

`docs/DOC_OWNERS.yml` is the policy file that proves every code change is covered by a documentation contract.

It guarantees:

1. **Coverage**: Every changed code file is matched to a DOC_OWNERS rule.
2. **Freshness**: Code changes and their required documentation changes exist in the same working tree.
3. **Traceability**: Which spec/runbook/ADR governs this code is always trackable.

Policy summary:

- Code changes must match a `rules[].paths` entry.
- Matched rules require at least one `contract_docs` OR `procedure_docs` change.
- Code changes always require `docs/handoff/CURRENT_HANDOFF.md` to change.
- `docs/archive/**`, external URLs, and Notion documents are NOT valid owners.
- `docs/plans/**` are NOT valid owners.
- Handoff-only changes do NOT satisfy contract freshness.
- Unmatched code paths cause failure when `policy.unmatched_code: fail`.

## Final Validation

After updating the handoff, run the finish gate:

```bash
python scripts/finish_task.py
```

This runs:

1. Unit tests
2. Docs freshness check (`--all` mode)
3. External mirror dry-run (if configured)
4. `git status --short`
5. `git diff --stat`

All steps must pass. The finish gate is the last validation step before a task is considered complete.

## Git Rules

AI agents must NOT commit or push unless explicitly requested by the maintainer. If commit/push is requested, first report:

- Working tree scope
- Validation results
- Intended commit message

Do not revert user changes or unrelated modifications.
