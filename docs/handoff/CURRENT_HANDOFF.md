# CURRENT_HANDOFF

## Repo

- GitHub: https://github.com/your-org/{{PROJECT_NAME}}
- Local path: /path/to/{{PROJECT_NAME}}
- Current branch: main
- Current phase: Initial setup

## Current State

Completed:

- Repository ({{PROJECT_NAME}}) initialized with docs-first workflow template
- DOC_OWNERS configured for project layout
- Initial specs and runbooks created
- Pre-commit hooks configured for docs freshness

In progress:

- (first task here)

## Contract Links

- Spec: `docs/specs/0000-project-overview.md`
- ADR: `docs/adrs/0001-docs-as-source-of-truth.md`
- Runbook: `docs/runbooks/test.md`
- Plan: (none yet)

## Reviewed Docs

(None yet)

## Next Agent Reads First

1. `docs/WORKFLOW.md`
2. `docs/handoff/CURRENT_HANDOFF.md`
3. `docs/DOC_OWNERS.yml`
4. `docs/runbooks/test.md`
5. `docs/runbooks/finish-task.md`
6. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/`

## Next Work Candidates

1. Define project requirements in specs
2. Set up CI workflow
3. Write first feature

## Do Not Touch Without Explicit Scope

- Existing user changes
- Files outside current task scope

## Validation

```bash
python scripts/finish_task.py
```

## External Tools

External tools (Notion, Confluence, etc.) are summary/index only. The implementation source of truth is repository docs. External mirror apply requires explicit maintainer request or approval.
