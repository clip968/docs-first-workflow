# CURRENT_HANDOFF

## Repo

- GitHub: https://github.com/your-org/{{PROJECT_NAME}}
- Local path: /path/to/{{PROJECT_NAME}}
- Current branch: main
- Current phase: Workflow hardening

## Current State

Last completed task:

- Added DOC_OWNERS priority/fallback resolution so specific owner docs cannot be bypassed by broad rules.
- Added spike/report, handoff-history, docs index, and root AGENTS guidance to the workflow template.

Current task:

- Final validation for workflow hardening changes.

## Contract Links

- Spec: `docs/specs/0001-agent-workflow.md`
- ADR: `docs/adrs/0001-docs-as-source-of-truth.md`
- Runbook: `docs/runbooks/finish-task.md`
- Plan: docs-first workflow template hardening in current session

## Contract Review

- Related spec: `docs/specs/0001-agent-workflow.md`
- Contract changed: Yes
- Reason: DOC_OWNERS overlap handling, spike mode, handoff limits, docs index, and AGENTS guidance are now part of the workflow contract.
- Required docs updated:
  - `docs/WORKFLOW.md`
  - `docs/specs/0001-agent-workflow.md`
  - `docs/runbooks/finish-task.md`
  - `docs/handoff/CURRENT_HANDOFF.md`
- Verification:
  - Pending final `python scripts/finish_task.py`

## Reviewed Docs

- `docs/WORKFLOW.md`
- `docs/templates/PLAN_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/templates/REPORT_TEMPLATE.md`
- `docs/runbooks/finish-task.md`
- `docs/specs/0001-agent-workflow.md`
- `docs/INDEX.md`
- `AGENTS.md`
- `README.md`

## Next Agent Reads First

1. `docs/WORKFLOW.md`
2. `docs/handoff/CURRENT_HANDOFF.md`
3. `docs/DOC_OWNERS.yml`
4. `docs/INDEX.md`
5. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/`

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

- `python -m unittest discover -s tests -p "test_*.py"`: OK, 22 tests
- `python scripts/check_docs_freshness.py --all`: OK
- `python scripts/finish_task.py`: OK

## History Links

- `docs/handoff/history/` stores detailed past logs when needed.

## External Tools

External tools (Notion, Confluence, etc.) are summary/index only. The implementation source of truth is repository docs. External mirror apply requires explicit maintainer request or approval.
