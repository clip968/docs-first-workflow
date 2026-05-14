# Test Runbook

## Purpose

This runbook describes how to run tests for this project.

## Test Command

Language: `{{LANGUAGE}}`

```bash
{{TEST_COMMAND}}
```

Replace `{{TEST_COMMAND}}` with your project's actual test command, for example:

- Python (unittest): `python -m unittest discover -s tests -p "test_*.py"`
- Python (pytest): `python -m pytest tests/`
- Node.js: `npm test`
- Rust: `cargo test`
- Go: `go test ./...`

## Specific Tests

Run a specific test file:

```bash
<test command for a specific file>
```

## Switching Test Frameworks

To switch from unittest to pytest (or another framework):

1. Set the environment variable (no file changes needed):
   ```bash
   export WORKFLOW_TEST_COMMAND="python -m pytest {{TEST_DIR}}/"
   ```
   Then `python scripts/finish_task.py` will use pytest instead of unittest.
2. Or update the test command directly in `docs/runbooks/test.md` and `.github/workflows/docs-freshness.yml`.

## Verification

Test results must be recorded in `docs/handoff/CURRENT_HANDOFF.md` at task completion.

## Related

- Spec: `docs/specs/0000-project-overview.md`
- WORKFLOW: `docs/WORKFLOW.md`
