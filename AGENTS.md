# Agent Instructions

These rules apply to AI agents working in this repository.

## Start Sequence

Before changing files:

1. Check `git status --short`.
2. Read `docs/WORKFLOW.md`.
3. Read `docs/handoff/CURRENT_HANDOFF.md`.
4. Read `docs/DOC_OWNERS.yml`.
5. Read `docs/INDEX.md`.
6. Read the relevant owner spec and runbook for the files you will touch.

Do not revert existing user changes. Do not touch files outside the current task
scope.

## Work Modes

- Use spike mode for investigation only. Write results in `docs/reports/`.
- Spike mode must not change production behavior.
- Use implementation mode for durable behavior changes:
  `spec -> plan -> failing test -> implementation -> docs -> handoff -> finish_task`.

## Implementation Rules

- Behavior-changing code changes start with a failing test.
- Prefer `python -m unittest`; do not switch test frameworks unless the project
  already requires it.
- Update the selected DOC_OWNERS contract or procedure docs alongside code.
- Update `docs/handoff/CURRENT_HANDOFF.md` before final validation.
- Keep `CURRENT_HANDOFF.md` short and move detailed logs to
  `docs/handoff/history/`.
- Do not use `docs/plans/`, `docs/reports/`, or handoff-only changes as contract
  freshness substitutes.

## DOC_OWNERS Rules

- DOC_OWNERS priority means ownership specificity, not current task urgency.
- Specific non-fallback rules override broad fallback rules.
- If two highest-priority rules match the same file, fix the ownership ambiguity
  instead of working around it.

## Finish Gate

Run before claiming completion:

```bash
python scripts/finish_task.py
```

Do not commit or push unless the maintainer explicitly asks for it.
