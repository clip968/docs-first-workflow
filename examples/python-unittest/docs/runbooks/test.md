# Test Runbook (Example)

## Purpose

This runbook describes how to run tests for the example Python project.

## Test Command

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Specific Tests

```bash
python -m unittest tests.test_example_adder
```
