# Plan: Title

## Status

Proposed | In Progress | Completed YYYY-MM-DD

## Related contract

- Spec: `docs/specs/...`
- ADR: `docs/adrs/...`
- Runbook: `docs/runbooks/...`
- Master plan: `docs/plans/...` (if this plan is part of a larger tracking plan)

## Goal

The small goal this plan will complete. It should correspond to one feature unit
from the spec.

## Non-goals

- What this plan will NOT do

## Execution Model

- Planner:
- Executor:
- Reviewer/CI:

Executor rules:

- Execute only one task from this plan at a time.
- Do not make plan-out-of-scope changes.
- If scope must change, update this plan and relevant contract docs first.
- Do not claim completion until `python scripts/finish_task.py` passes.

## Allowed Files

- May modify:
  - `path/to/file`
- Must not modify:
  - `path/to/protected-file`

## Docs Required

Code changes require both global handoff and at least one relevant contract or
procedure doc.

- Contract docs:
  - `docs/specs/...` or `docs/adrs/...`
- Procedure docs:
  - `docs/runbooks/...`
- Global handoff:
  - `docs/handoff/CURRENT_HANDOFF.md`

Do not use `docs/plans/` or handoff-only changes as substitutes for contract
freshness.

## Red Test

- First failing test:
  - `tests/...`
- If no red test applies:
  - Reason:
  - Alternative verification:

## Tasks

Each task is a checklist item. Mark `[x]` when completed.

- [ ] Task 1: one small, independently verifiable change
- [ ] Task 2: next small change, if needed
- [ ] Task 3: docs, handoff, and final verification

## Verification

```bash
python -m unittest tests.<focused_test_module>
python -m unittest discover -s tests -p "test_*.py"
python scripts/check_docs_freshness.py --all
python scripts/finish_task.py
```

## Handoff Updates

- What to reflect in `docs/handoff/CURRENT_HANDOFF.md`

---

## Plan Writing Rules

1. **Break spec into feature-sized units.** One plan = one feature (or one
   implementation step) from the spec.
2. **Number plan files for easy reference from the master plan.**
   Example: `docs/plans/v03/2026-05-14-v03-03-drive-api-auth.md`
3. **Tasks use checklists (`[ ]`/`[x]`).** A glance at the plan must show what
   is done and what is not.
4. **Feature plans live under `docs/plans/<phase>/`.**
   Example: `docs/plans/v03/`, `docs/plans/v04/`
5. **If one spec produces multiple plans, create a master plan.**
   The master plan lives at `docs/plans/YYYY-MM-DD-<phase>-master.md` and tracks
   each feature plan's completion status with checklists.
6. **Status must be one of: Proposed / In Progress / Completed YYYY-MM-DD.**
   Completed entries include the completion date.
7. **Plans for lower-trust executors must include Allowed Files, Docs Required,
   Red Test, and Verification.**
8. **Completion is judged by test output, docs freshness, finish gate, and diff
   review, not by agent claims.**
