# Spec: Example Adder Module

## Status

- Draft [ ] / Accepted [X] / Deprecated [ ]

## Context

This example demonstrates the docs-first workflow with a minimal Python module.

## Goals

- Provide a correct and tested add/subtract utility.
- Demonstrate the TDD workflow: failing test -> implementation -> passing test.

## Non-goals

- Not a full-featured arithmetic library.

## Requirements

- REQ-EX-001: `add(a, b)` returns the sum of integers a and b.
- REQ-EX-002: `subtract(a, b)` returns a minus b.

## Acceptance Criteria

- AC-EX-001: `add(2, 3)` returns `5`.
- AC-EX-002: `subtract(5, 3)` returns `2`.

## Test Mapping

- TEST-EX-001:
  - Covers: REQ-EX-001, AC-EX-001
  - Command: `python -m unittest discover -s tests -p "test_*.py"`

## Docs Ownership

- Code paths: `src/example_adder.py`
- Required docs: `docs/specs/0000-project-overview.md`
- Runbooks: `docs/runbooks/test.md`

## Verification

```bash
python -m unittest discover -s tests -p "test_*.py"
```
