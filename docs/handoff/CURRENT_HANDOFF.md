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
- Planner / Executor workflow guidance added to README, WORKFLOW, plan template, handoff template, PR template, agent workflow spec, and finish-task runbook
- `scripts/finish_task.py` command parsing fixed so quoted unittest patterns work when subprocess receives argv directly
- `tests/test_finish_task.py` added for default test command quote stripping

In progress:

- Template release review, if this folder will be published separately

## Contract Links

- Spec: `docs/specs/0001-agent-workflow.md`
- ADR: `docs/adrs/0001-docs-as-source-of-truth.md`
- Runbook: `docs/runbooks/finish-task.md`
- Plan: docs-first workflow template hardening in current session

## Reviewed Docs

- `docs/WORKFLOW.md`
- `docs/templates/PLAN_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/runbooks/finish-task.md`
- `docs/specs/0001-agent-workflow.md`
- `README.md`

## Next Agent Reads First

1. `docs/WORKFLOW.md`
2. `docs/handoff/CURRENT_HANDOFF.md`
3. `docs/DOC_OWNERS.yml`
4. `docs/runbooks/test.md`
5. `docs/runbooks/finish-task.md`
6. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/`

## Next Work Candidates

1. Add a standalone release checklist for publishing the template repository.
2. Add CI coverage for `scripts/finish_task.py` if the template evolves beyond unittest.
3. Keep project-specific requirements out of this reusable template.

## Do Not Touch Without Explicit Scope

- Existing user changes
- Files outside current task scope

## Validation

```bash
python scripts/finish_task.py
```

Latest validation:

- `python -m unittest tests.test_finish_task`: OK
- `python -m unittest discover -s tests -p "test_*.py"`: OK, 15 tests
- `python scripts/check_docs_freshness.py --all`: OK
- `python scripts/finish_task.py`: OK

## External Tools

External tools (Notion, Confluence, etc.) are summary/index only. The implementation source of truth is repository docs. External mirror apply requires explicit maintainer request or approval.
