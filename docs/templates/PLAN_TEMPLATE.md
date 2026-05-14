# Plan: Title

## Status

Proposed | In Progress | Completed YYYY-MM-DD

## Related contract

- Spec: `docs/specs/...`
- ADR: `docs/adrs/...`
- Master plan: `docs/plans/...` (if this plan is part of a larger tracking plan)

## Goal

The small goal this plan will complete. It should correspond to one feature unit
from the spec.

## Non-goals

- What this plan will NOT do

## Tasks

Each task is a checklist item. Mark `[x]` when completed.

- [ ] task 1
- [ ] task 2
- [ ] task 3

## Verification

```bash
python -m unittest discover -s tests -p "test_*.py"
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
