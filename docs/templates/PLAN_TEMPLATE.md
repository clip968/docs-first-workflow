# Plan: <title>

## Related Contract

- Spec: `docs/specs/<spec-file>.md`
- Requirement IDs: REQ-<PROJECT>-001, REQ-<PROJECT>-002
- Acceptance criteria: AC-<PROJECT>-001, AC-<PROJECT>-002
- ADRs, if any: `docs/adrs/<adr-file>.md`

## Scope

### In Scope

-

### Out of Scope

-

## Task List

### TASK-001: <small feature/test slice>

- Related requirements:
  - REQ-<PROJECT>-001
- Files:
  - `src/...`
  - `tests/...`
- Red test:
  - Test name: `test_<name>`
  - Expected initial failure: <error or assertion>
- Implementation:
  - Minimal change:
- Verification:
  - Command: `<test command>`
- Done when:
  - The red test fails before implementation.
  - The test passes after implementation.
  - Related docs are updated.
  - Handoff is updated if this task completes the work.

### TASK-002: <next slice>

- Related requirements:
- Files:
- Red test:
- Implementation:
- Verification:
- Done when:

## Validation

- Unit test command: `<test command>`
- Docs freshness command: `python scripts/check_docs_freshness.py --all`
- Finish command: `python scripts/finish_task.py`

## Notes

- Risks:
- Follow-ups:
- Reason if red test cannot be written first:
