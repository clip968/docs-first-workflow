# Docs Index

Use this file as the quick routing map before editing code. Keep it short; put
details in specs, runbooks, plans, reports, or handoff history.

| Area | Code paths | Owner spec | Runbook | Representative tests | Current plan |
|---|---|---|---|---|---|
| Workflow checker | `scripts/check_docs_freshness.py`, `tests/test_check_docs_freshness.py` | `docs/WORKFLOW.md`, `docs/specs/0001-agent-workflow.md` | `docs/runbooks/finish-task.md` | `python -m unittest tests.test_check_docs_freshness -v` | Current session |
| Finish gate | `scripts/finish_task.py`, `tests/test_finish_task.py` | `docs/WORKFLOW.md`, `docs/specs/0001-agent-workflow.md` | `docs/runbooks/finish-task.md` | `python -m unittest tests.test_finish_task -v` | - |
| Workflow template docs | `README.md`, `docs/**`, `.github/pull_request_template.md`, `AGENTS.md` | `docs/specs/0001-agent-workflow.md` | `docs/runbooks/finish-task.md` | `python -m unittest discover -s tests -p "test_*.py"` | - |

## Owner Rule Priority

DOC_OWNERS priority is stable ownership metadata:

| Priority | Meaning |
|---|---|
| 100 | Exact file owner |
| 90 | Feature/module owner |
| 70 | Subsystem/package owner |
| 50 | Tooling/workflow owner |
| 30 | Broad project fallback |

Task status changes belong in plans and handoff, not in DOC_OWNERS priority.

## Spike Reports

Investigation-only work belongs in `docs/reports/`. Reports may inform later
specs and plans, but they are not contract owners and do not satisfy docs
freshness for code changes.
