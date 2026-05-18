# Docs-First Agent Workflow

The source of truth for this project is the repository-internal `docs/` directory.
External tools (Notion, Confluence, wiki, etc.) are NOT the source of truth.
They serve as mirror/index only — for handoff summaries, links, or indices.

## Core Flow

Every non-trivial code change follows this sequence:

```text
spec
-> ADR (if needed)
-> plan
-> failing tests
-> implementation
-> docs update
-> handoff update
-> python scripts/finish_task.py
-> optional external mirror apply
```

The finish flow is more precisely:

```text
implementation
-> tests
-> relevant docs/specs/runbooks update
-> docs/handoff/CURRENT_HANDOFF.md update
-> python scripts/finish_task.py
-> optional external mirror apply
```

`finish_task.py` is NOT a mid-flight check before handoff update. It is the final
validation gate of the entire working tree, including handoff.

## Work Start Check

Before any work, check the current repository state:

```bash
git status --short
git branch --show-current
git log --oneline -5
git diff --stat
```

Then read at minimum:

1. `docs/README.md`
2. `docs/WORKFLOW.md`
3. `docs/handoff/CURRENT_HANDOFF.md`
4. Relevant `docs/specs/`, `docs/runbooks/`, `docs/adrs/` for the files you will touch

Do not revert existing uncommitted changes. Do not touch files unrelated to the current task.

## Existing Repository Installation

To install this workflow into an existing repository, point the agent at the
canonical bootstrap URL. The target repository does not need to contain
`workflow-implementation.md`.

```text
Read https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md
and install docs-first workflow into this repository.
```

Local `workflow-implementation.md` files are still supported, but they are
optional.

The installer auto-detects:

- Project name from the target directory name
- Language from `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`,
  `requirements.txt`, or `setup.py`
- Source directory from `src/`, `app/`, or `lib/`
- Test directory from `tests/`, `test/`, or `spec/`
- Test command from the detected language and test directory

Use YAML in `workflow-implementation.md` only to override detection.

Agent install flow:

```text
read workflow-implementation.md
-> or read the remote bootstrap URL
-> run install_into_repo.py in dry-run mode with auto-detection
-> show detected config, planned workflow install, files, conflict copies, and directory tree
-> ask for explicit approval
-> run install_into_repo.py --apply only after approval
```

Dry-run command:

```bash
python /path/to/docs-first-workflow/scripts/install_into_repo.py \
  --target . \
  --template-root /path/to/docs-first-workflow \
  --bootstrap-url https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md
```

Apply command after approval:

```bash
python /path/to/docs-first-workflow/scripts/install_into_repo.py \
  --target . \
  --template-root /path/to/docs-first-workflow \
  --bootstrap-url https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md \
  --apply
```

The installer must not overwrite existing files by default. When a target file
already exists with different content, it writes a
`*.docs-first-workflow.new` conflict copy for manual review.

## Spec Contract

Implementation is governed by spec contracts. If a relevant spec exists, read it first.
If none exists, create a minimal spec in `docs/specs/` before implementation.

A spec must clearly define:

- Scope and out-of-scope
- Inputs, outputs, storage rules
- Error handling and mode-specific behavior (e.g., dry-run vs. apply)
- Requirement IDs and acceptance criteria
- Test mappings

Small documentation-only changes may proceed without a new spec. Any behavior-changing
code change must confirm or create a spec first.

## ADR Guidelines

Not every change needs an ADR. Create one in `docs/adrs/` when:

- The decision is hard to reverse (technology choices, architecture decisions)
- The change affects source of truth, storage, or external system boundaries
- The change has long-term impact on testing, deployment, or operations
- Multiple reasonable alternatives exist, and the reasoning should be recorded

ADRs do not replace specs. ADRs record *why* a decision was made; specs record
*what* the implementation must conform to.

## Plan Guidelines

Before non-trivial implementation, create a small execution plan in `docs/plans/`.

A plan includes:

- Related contract (spec, ADR, runbook references)
- Goal (one feature unit from the spec)
- Non-goals
- Task checklist (`[ ]` / `[x]`)
- Verification commands
- Handoff notes

Plans are ephemeral execution guides. They are NOT long-term contracts, NOT source
of truth, and do NOT satisfy DOC_OWNERS freshness requirements.

## Work Modes

Use the smallest mode that fits the work.

### Spike / Exploration Mode

Use spike mode when the next step is investigation rather than implementation:
external site structure review, fixture collection, parser option comparison,
live integration feasibility checks, or similar discovery work.

Spike mode flow:

```text
spike brief
-> investigation
-> report in docs/reports/
-> discard or convert to spec/plan
```

Spike mode may create notes, fixtures, and reports, but it must not change
production behavior. If the spike produces an implementation direction, convert
the result into a spec or plan and enter implementation mode.

### Implementation Mode

Use implementation mode for behavior changes and durable workflow changes.

Implementation mode flow:

```text
spec
-> plan
-> failing test
-> implementation
-> docs update
-> handoff update
-> finish_task
```

## Planner / Executor Split

Large or ambiguous work should be split before implementation. A planner
(maintainer, senior model, or higher-trust agent) writes the plan. An executor
(often a lower-trust or open-source model) performs exactly one bounded task from
that plan.

Recommended responsibilities:

- **Planner**: read specs/ADRs/runbooks, identify scope, write allowed files,
  docs required, red test, verification commands, and acceptance criteria.
- **Executor**: stay inside the plan scope, write the failing test first, make
  the smallest implementation, update required docs, update handoff, and run the
  finish gate.
- **Reviewer/CI**: decide completion from diff, command output, docs freshness,
  and handoff, not from the executor's prose.

Plans intended for open-source model execution MUST include:

- Allowed files and files explicitly out of scope
- Related spec/ADR/runbook links
- Required docs to update
- First red test or explanation why TDD does not apply
- Focused test, full test, docs freshness, and finish gate commands
- Handoff updates expected at completion

If the executor discovers that the plan is too broad or wrong, it updates the
plan and relevant contract docs first, then resumes implementation.

Plans that track a spec's multiple features should be organized under a version
folder:

```text
docs/plans/<version>/
  2026-05-14-<version>-01-<feature>.md
  2026-05-14-<version>-02-<next-feature>.md
```

With a master tracking plan at `docs/plans/YYYY-MM-DD-<phase>-master.md`.
The master plan tracks the completion status of each feature plan via checklists.

## TDD Rules

Behavior-changing code changes MUST start with a failing test.

```text
failing test -> implementation -> passing test
```

If a red test cannot be written first (e.g., the change is configuration,
infrastructure, or documentation-only), the plan must explain why and name an
alternative verification method.

The standard test command is:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Docs Update Rules

After code changes, update the related documentation in the same working tree:

| Change type | Document to update |
|---|---|
| Behavior contract change | `docs/specs/` |
| Repeatable procedure change | `docs/runbooks/` |
| Technical decision change | `docs/adrs/` |
| Investigation / spike result | `docs/reports/` |
| Session/agent state change | `docs/handoff/CURRENT_HANDOFF.md` |

- `docs/archive/` documents are NOT valid contract owners.
- External tool documents (Notion, Confluence, etc.) are NOT valid contract owners.
- `docs/plans/` documents are NOT valid contract owners.
- `docs/reports/` documents are NOT valid contract owners.
- Every plan should name the required docs to update. If code changes and no
  spec/runbook/ADR changes, assume the task is incomplete unless the plan states
  why the existing contract remains unchanged.

### Contract Review Exception

Some code changes fix implementation so it satisfies an existing contract. In
that case the spec or runbook may not need text changes. Do not make filler doc
edits just to pass the gate. Instead, record a contract review in the plan or
handoff:

```markdown
## Contract Review

- Related spec: `docs/specs/<spec>.md`
- Contract changed: No
- Reason: This task fixes implementation behavior to satisfy existing <REQ/AC>.
- Required docs updated:
  - `docs/handoff/CURRENT_HANDOFF.md`
- Verification:
  - `<focused test command>`
  - `python scripts/finish_task.py`
```

This is an explicit maintainer-reviewed exception path, not the default. The
default `finish_task.py` command still runs the docs freshness check without
`--allow-reviewed-docs`.

## Handoff Rules

`docs/handoff/CURRENT_HANDOFF.md` is the global state document for every code
change. Update it whenever code changes.

The handoff must contain:

- Current phase
- Current branch and local path
- Last completed task
- Next task
- Up to 5 documents the next agent should read first
- Latest finish gate result
- Scope boundaries and explicit "do not touch" items
- Links to detailed history entries, if needed

Keep `CURRENT_HANDOFF.md` short. Move detailed past logs to:

```text
docs/handoff/history/
  YYYY-MM-DD-<task>.md
```

**Important:** The handoff alone does NOT satisfy per-path contract freshness.
Changing only `CURRENT_HANDOFF.md` without updating the corresponding contract
docs (specs or runbooks) will FAIL the docs freshness check.

## DOC_OWNERS Policy

`docs/DOC_OWNERS.yml` is the policy file that proves every code change is covered
by a documentation contract.

It guarantees:

1. **Coverage**: Every changed code file is matched to a DOC_OWNERS rule.
2. **Freshness**: Code changes and their required documentation changes exist in
   the same working tree.
3. **Traceability**: Which spec/runbook/ADR governs this code is always trackable.

Policy summary:

- Code changes that match `code_paths` and are NOT in `ignored_paths` must match
  a rule.
- Each rule may define `priority` and `fallback`.
- When `policy.multiple_matches: require_highest_priority`, overlapping rules
  are resolved before freshness is checked.
- If `policy.fallback_rules_allowed: true`, fallback rules apply only when no
  non-fallback rule matches the changed file.
- The selected highest-priority rule requires at least one `contract_docs` OR
  `procedure_docs` change.
- If multiple selected rules have the same highest priority, the check fails as
  ambiguous ownership.
- Code changes always require `docs/handoff/CURRENT_HANDOFF.md` to change
  (via `global_required_on_code_change`).
- `docs/archive/**`, external URLs, and Notion documents are NOT valid owners.
- `docs/plans/**` are NOT valid owners.
- `docs/reports/**` are NOT valid owners.
- Handoff-only changes do NOT satisfy contract freshness.
- Unmatched code paths cause failure when `policy.unmatched_code: fail`.
- `--allow-reviewed-docs` is an exceptional helper flag. It is NOT part of the
  default workflow. `finish_task.py` runs without this flag.

Priority values should describe ownership specificity, not current task urgency.
Recommended scale:

| Priority | Meaning |
|---|---|
| 100 | Exact file owner |
| 90 | Feature/module owner |
| 70 | Subsystem/package owner |
| 50 | Tooling/workflow owner |
| 30 | Broad project fallback |

Task status belongs in `docs/plans/`, `docs/INDEX.md`, and
`docs/handoff/CURRENT_HANDOFF.md`; it must not be encoded by constantly changing
DOC_OWNERS priorities.

## Final Validation

After updating the handoff, run the finish gate:

```bash
python scripts/finish_task.py
```

This runs:

1. Unit tests
2. Docs freshness check (`--all` mode)
3. External mirror dry-run (if configured)
4. `git status --short`
5. `git diff --stat`

All steps must pass. External mirror/Notion apply is NOT included in the default
validation gate. It runs only when explicitly requested or approved by the
maintainer.

## Git Rules

AI agents must NOT commit or push unless explicitly requested by the maintainer.
If commit/push is requested, first report:

- Working tree scope
- Validation results
- Intended commit message

Do not revert user changes or unrelated modifications.

## External Documentation Migration Principles

If the project previously used an external tool (Notion, Confluence, wiki, etc.)
as source of truth, and all documents have been migrated to repo `docs/`:

- The external tool is NO LONGER source of truth.
- New documents follow these rules:

| Document type | Location |
|---|---|
| Technical decisions | `docs/adrs/` |
| Implementation contracts | `docs/specs/` |
| Task execution plans | `docs/plans/` |
| Session handoffs | `docs/handoff/CURRENT_HANDOFF.md` |
| Repeatable procedures | `docs/runbooks/` |

- The external tool serves as mirror/index only. If content is written there,
  write it in repo docs first, then add a summary/link to the external tool.
- Information that exists only in the external tool is considered stale.
- AI agents MUST prioritize repo `docs/` over any external tool content.
