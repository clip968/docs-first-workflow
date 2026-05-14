# Docs-First Agent Workflow Template: {{PROJECT_NAME}}

> **Git independence**: The `scripts/check_docs_freshness.py` and `scripts/finish_task.py` tools rely on `git diff` to detect changed files. Before using these tools inside this template directory, run `git init` to make it a standalone Git repository. Without this, git commands will traverse up to any parent repository, producing incorrect results.

A reusable, language-agnostic workflow template for AI-assisted software development. It enforces docs as source of truth, spec-contract-based implementation, task-level planning, TDD, and automated freshness validation.

## What This Is

This template encodes a proven workflow extracted from a real project. It is designed to help AI agents (and human developers) produce consistent, verifiable, well-documented code by following a structured process:

1. Read the docs first.
2. Write or update specs as implementation contracts.
3. Split work into testable slices.
4. Write failing tests before implementation.
5. Update documentation with code.
6. Validate through automated freshness checks.

## Principles

- **Docs are the source of truth.** External tools (Notion, Confluence, etc.) are mirror/index only.
- **Specs are implementation contracts.** A spec defines requirements, acceptance criteria, and test mappings.
- **Plans split specs into small testable tasks.** Plans are not long-term contracts; they are ephemeral execution guides.
- **Planner and executor roles are separate.** A higher-trust planner writes small plans; an executor agent performs one bounded task at a time.
- **Behavior changes start with failing tests.** If a red test cannot be written first, the plan must explain why.
- **DOC_OWNERS enforces docs freshness.** A configuration file maps code paths to their required contract and procedure docs.
- **Handoff is updated before final validation.** The handoff document carries state to the next agent session.
- **External tools are mirror/index only.** They never satisfy DOC_OWNERS contract requirements.
- **No commit/push unless explicitly requested.** Agents produce the working tree; maintainers decide when to commit.

## Directory Layout

```
workflow-template/
  README.md                    # This file
  LICENSE.example              # Example license (MIT)
  .gitignore                   # Standard ignores
  .pre-commit-config.yaml      # Pre-commit hook for docs freshness
  .github/
    pull_request_template.md   # PR template with TDD + docs sections
    workflows/
      docs-freshness.yml       # CI workflow for docs freshness
  docs/
    README.md                  # Docs directory overview
    WORKFLOW.md                # Full workflow specification
    DOC_OWNERS.yml             # Code-to-doc contract routing
    specs/                     # Implementation contracts
      0000-project-overview.md
      0001-agent-workflow.md
    adrs/                      # Architecture Decision Records
      0001-docs-as-source-of-truth.md
    plans/                     # Ephemeral implementation plans
      .gitkeep
    runbooks/                  # Repeatable procedures
      test.md
      finish-task.md
    handoff/
      CURRENT_HANDOFF.md       # Session state handoff
    templates/                 # Document templates
      SPEC_TEMPLATE.md
      PLAN_TEMPLATE.md
      ADR_TEMPLATE.md
      HANDOFF_TEMPLATE.md
      RUNBOOK_TEMPLATE.md
  scripts/
    check_docs_freshness.py    # Validates contract-freshness of changes
    finish_task.py             # Final validation gate (tests + freshness + git status)
    init_workflow_template.py  # One-time project initialization script
  tests/
    test_check_docs_freshness.py
  examples/
    python-unittest/           # Minimal working example
```

## How to Apply to a New Repository

### Automatic (via init script)

```bash
cd your-project
python workflow-template/scripts/init_workflow_template.py \
  --project-name "{{PROJECT_NAME}}" \
  --language {{LANGUAGE}} \
  --test-command "{{TEST_COMMAND}}" \
  --source-dir {{SOURCE_DIR}} \
  --test-dir {{TEST_DIR}}
```

Replace `{{PROJECT_NAME}}`, `{{TEST_COMMAND}}`, `{{SOURCE_DIR}}`, `{{TEST_DIR}}` with your project's actual values. The init script will substitute them across all template files.

### Manual

1. **Copy the template directory** into your repository:

   ```bash
   cp -r workflow-template your-project/workflow-template
   ```

2. **Customize `docs/DOC_OWNERS.yml`**:
   - Update `code_paths` to match your project's source layout.
   - Update `ignored_paths` for your build artifacts and data directories.
   - Add rules mapping each code path group to its contract docs and runbooks.

3. **Write your first spec**: Create `docs/specs/0000-project-overview.md` describing your project's architecture and core requirements.

4. **Write a runbook**: Create `docs/runbooks/test.md` with the actual test command for your project.

5. **Initialize the handoff**: Update `docs/handoff/CURRENT_HANDOFF.md` with current project state.

6. **Run validation**:

   ```bash
   python scripts/finish_task.py
   ```

## How to Customize DOC_OWNERS

`docs/DOC_OWNERS.yml` is a contract routing table, not a human ownership file. It answers:

- Which docs must move with this code?
- Which spec owns this behavior?
- Which runbook verifies this behavior?
- Did the handoff get updated before final validation?

Edit the `rules` section to map your project's code paths to their required docs:

```yaml
rules:
  - id: my-service
    paths:
      - "src/**/*.py"
      - "app/**/*.py"
    contract_docs:
      - "docs/specs/0000-project-overview.md"
    procedure_docs:
      - "docs/runbooks/test.md"
```

## How to Run Validation

```bash
# Full finish gate (tests + docs freshness + git status)
python scripts/finish_task.py

# Skip specific checks
python scripts/finish_task.py --skip-tests
python scripts/finish_task.py --skip-docs-check

# Standalone docs freshness check
python scripts/check_docs_freshness.py --all               # staged + unstaged + untracked
python scripts/check_docs_freshness.py --staged             # pre-commit hook
python scripts/check_docs_freshness.py --base HEAD~1 --head HEAD  # CI diff check

# Override docs freshness requirement (use only in emergencies)
DOCS_UPDATE_NOT_REQUIRED=1 python scripts/check_docs_freshness.py --staged
```

## How Agents Should Use This Workflow

1. Read `docs/WORKFLOW.md` and `docs/handoff/CURRENT_HANDOFF.md` first.
2. Check `git status` before making changes.
3. Read the relevant spec for the code you are changing.
4. If no spec exists for the change, write one first.
5. Split the work into small tasks. Write a plan if the work is non-trivial.
6. For each behavior-changing task, write a failing test first.
7. Implement the minimum code to pass the test.
8. Update related docs (specs, runbooks, ADRs).
9. Update `docs/handoff/CURRENT_HANDOFF.md`.
10. Run `python scripts/finish_task.py` as the final validation gate.

## Planner / Executor Pattern

This template is designed for workflows where a higher-trust model or maintainer
decomposes work, then a lower-trust or open-source model executes one small plan.

Recommended split:

```text
Planner
-> reads specs/ADRs/runbooks
-> writes a task plan with allowed files, docs required, red test, verification

Executor
-> performs exactly one task from the plan
-> writes the failing test first
-> updates required docs
-> updates handoff
-> runs finish_task.py

Reviewer / CI
-> trusts command output, diff, and docs freshness, not the executor's prose
```

Executor task plans should include:

- Allowed files and forbidden files
- Related spec/ADR/runbook
- The first failing test or reason no red test applies
- Required docs to update
- Focused test, full test, docs freshness, and finish gate commands
- Handoff fields to update

## What Not to Do

- **Do not use plans as durable contracts.** Plans are ephemeral execution guides and do not satisfy DOC_OWNERS requirements.
- **Do not use archive docs as owners.** `docs/archive/` documents cannot fulfill contract freshness.
- **Do not use Notion/external tools as source of truth.** External tools are mirror/index only and never satisfy DOC_OWNERS.
- **Do not let handoff-only changes satisfy contract freshness.** The handoff document is a global state update but does not replace per-path contract docs.
- **Do not let plan-only changes satisfy contract freshness.** Plans are task instructions, not durable contracts.
- **Do not commit/push unless explicitly requested.** Agents produce the working tree and report results; maintainers control commits.

## Relationship to Source Project

This template was extracted from a real project workflow ([ffxiv-claw-bot](https://github.com/clip968/ffxiv-claw-bot)), but it intentionally removes project-specific behavior. Project-specific specs, runbooks, code paths, and external mirror details must be added by each repository.

The original project's workflow remains a concrete example of how this template can be applied.
