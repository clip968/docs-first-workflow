# ADR 0001: Docs as Source of Truth

## Status

Accepted [X] / Proposed [ ] / Superseded [ ]

## Context

When using AI agents to assist with software development, a common failure mode is that documentation becomes stale or is never updated. Agents also tend to treat their training knowledge as authoritative rather than looking at the actual repository.

We needed a mechanism that:

1. Forces documentation to stay synchronized with code changes.
2. Provides traceability from code to its governing specs.
3. Prevents external tools (Notion, Confluence, wikis) from becoming the authoritative reference.
4. Can be enforced programmatically in CI and pre-commit hooks.

## Decision

The repository `docs/` directory is the single source of truth. All implementation contracts, runbooks, and decisions live in Git alongside the code.

External tools (Notion, Confluence, etc.) are treated as index/mirror only. They summarize or link to the Git-managed docs but never replace them.

A `DOC_OWNERS.yml` file maps code paths to their required documentation (contract docs and procedure docs). A `check_docs_freshness.py` script validates that code changes are accompanied by matching documentation changes.

## Consequences

**Positive:**

- Documentation is always in Git, versioned alongside code.
- Agents can be directed to read `docs/` before making changes.
- CI can automatically reject changes that lack documentation updates.
- External tool drift does not affect the source of truth.
- The DOC_OWNERS schema provides traceability from code to spec to requirements to tests.

**Negative:**

- Extra overhead for small changes (changing a comment requires handoff update).
- Requires discipline to update docs before running the finish gate.
- Agents need explicit instructions to read docs first (not always natural for LLMs).

## Alternatives Considered

- **Notion as source of truth**: Rejected because Notion is outside Git, cannot be validated in CI, and is not version-controlled with code.
- **No enforcement (trust-based)**: Rejected because agents do not naturally update documentation without explicit enforcement.
- **Code comments only**: Rejected because comments in code do not provide cross-file traceability or requirement-to-test mapping.

## Related

- Spec: `docs/specs/0001-agent-workflow.md`
