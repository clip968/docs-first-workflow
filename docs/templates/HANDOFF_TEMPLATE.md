# CURRENT_HANDOFF

## Repo

- GitHub:
- Local path:
- Current branch:
- Current phase:

## Current State

Last completed task:

-

Current task:

-

## Contract Links

- Spec:
- ADR:
- Runbook:
- Plan:

## Plan Execution Record

- Planner:
- Executor:
- Task performed:
- Work mode: Spike / Implementation
- Allowed files followed: Yes / No
- Scope changes made:

## Contract Review

- Related spec:
- Contract changed: Yes / No
- Reason:
- Required docs updated:
- Verification:

## Docs Updated

- Contract docs:
- Procedure docs:
- Handoff:
- Notes:

## Reviewed Docs

**Note:** Default `finish_task.py` validation does NOT treat this section as satisfying DOC_OWNERS contract freshness. Only explicit `--allow-reviewed-docs` mode considers this list as supplementary evidence.

-

## Next Agent Reads First

1. `docs/WORKFLOW.md`
2. `docs/handoff/CURRENT_HANDOFF.md`
3. `docs/DOC_OWNERS.yml`
4. `docs/INDEX.md`
5. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/`

Keep this list to five entries. Link detailed past context below instead of
expanding this file.

## Next Work Candidates

1.

## Do Not Touch Without Explicit Scope

- Existing user changes
- Files outside current task scope
-

## History Links

- `docs/handoff/history/...`

## Validation

```bash
# Run finish gate
python scripts/finish_task.py

# Or individual checks
<test command>
python scripts/check_docs_freshness.py --all
git status --short
git diff --stat
```

Validation evidence:

- Focused test:
- Full test:
- Docs freshness:
- Finish gate:

## External Tools

External tools (Notion, Confluence, etc.) are summary/index only. The implementation source of truth is repository docs. External mirror apply requires explicit maintainer request or approval.
