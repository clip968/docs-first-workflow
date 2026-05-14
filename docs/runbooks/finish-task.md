# Finish Task Runbook

## Purpose

This runbook describes the final validation sequence that must be run before a task is considered complete.

## Steps

### 1. Update Handoff

Before running the finish gate, ensure `docs/handoff/CURRENT_HANDOFF.md` reflects:

- All completed changes
- Related spec/runbook/ADR references
- Validation commands and results
- Remaining TODO items
- Scope boundaries

### 2. Run Finish Gate

```bash
python scripts/finish_task.py
```

This runs in sequence:

1. `{{TEST_COMMAND}}` (unit tests)
2. `python scripts/check_docs_freshness.py --all` (docs freshness)
3. External mirror dry-run (if configured)
4. `git status --short`
5. `git diff --stat`

Any failure stops the gate with exit code 1.

Executor agents must not claim completion when this command fails. Record the
failed command, exit code, important log lines, and modified files in handoff,
then stop or ask for review.

### Failure Handling

| Step | Failure | Action |
|---|---|---|
| Unit tests | Tests fail | Fix failing tests first |
| Docs freshness | Missing docs | Verify required docs are updated alongside code |
| External mirror | Dry-run fails | Check handoff document exists |
| Git status | Unexpected files | Review working tree for unintended changes |

### Skip Options

Use only in exceptional circumstances:

```bash
python scripts/finish_task.py --skip-tests
python scripts/finish_task.py --skip-docs-check
```

When skip options are used, `SKIP` is explicitly printed in the output.

## Switching Test Frameworks

To switch from unittest to pytest:

1. Set the environment variable (no file changes needed):
   ```bash
   export WORKFLOW_TEST_COMMAND="python -m pytest {{TEST_DIR}}/"
   ```
2. Then `python scripts/finish_task.py` will use pytest instead of unittest.

## Docs Freshness Check

`finish_task.py` runs `check_docs_freshness.py --all`, which examines:

- Staged files
- Unstaged files
- Untracked files

The check reads `docs/DOC_OWNERS.yml` and validates:

- Every changed code file matches a rule.
- Each matching rule has at least one contract or procedure doc changed in the same working tree.
- `docs/handoff/CURRENT_HANDOFF.md` is changed when code changes.
- No invalid owner docs (archive, external URLs, plans) are used to satisfy requirements.

`docs/plans/**` and `docs/handoff/CURRENT_HANDOFF.md` do not replace contract
or procedure docs. Plan-only or handoff-only updates are not enough for
code-changing work.

## Related

- Spec: `docs/specs/0001-agent-workflow.md`
- WORKFLOW: `docs/WORKFLOW.md`
- Script: `scripts/check_docs_freshness.py`
- Script: `scripts/finish_task.py`
