# Docs ({{PROJECT_NAME}})

`docs/` is the single source of truth for {{PROJECT_NAME}}'s implementation contracts and workflows. External tools (Notion, Confluence, etc.) are mirror/index only.

## Directory Roles

| Directory | Purpose |
|---|---|
| `specs/` | Implementation contracts defining requirements, acceptance criteria, and test mappings |
| `adrs/` | Architecture Decision Records: why hard-to-reverse decisions were made |
| `plans/` | Ephemeral implementation plans — split specs into testable tasks |
| `runbooks/` | Repeatable procedures: test, build, deploy, etc. |
| `handoff/` | Session state: what was done, what remains, what to read next |
| `templates/` | Document templates for specs, ADRs, plans, handoffs, and runbooks |

## Principles

- Implementation follows spec contracts.
- Non-trivial changes go through: spec -> ADR (if needed) -> plan -> failing tests -> implementation -> docs update -> handoff update -> finish_task.
- Behavior-changing code changes start with failing tests.
- `docs/handoff/CURRENT_HANDOFF.md` is the global state document for all code changes.
- `docs/DOC_OWNERS.yml` maps code paths to their governing specs and runbooks.
- `docs/plans/` and `docs/archive/` are NOT DOC_OWNERS owners.
- External tool documents are NOT DOC_OWNERS owners.

## Start Here

New sessions read in order:

1. `docs/WORKFLOW.md`
2. `docs/handoff/CURRENT_HANDOFF.md`
3. `docs/DOC_OWNERS.yml`
4. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/`

Before finishing, update handoff and run:

```bash
python scripts/finish_task.py
```

## Relationship to Original Project

This template was extracted from a real project workflow. The original project's `docs/` remains a concrete example of how this structure is applied in practice.
