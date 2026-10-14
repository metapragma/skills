# Migrate Callers Then Delete Legacy APIs

When we decide a new API is the right design, migrate callers and remove the old API in the same refactor wave instead of preserving compatibility layers.

**Rule:**
- Do not keep legacy API paths only because internal callers still exist
- Inventory callers, migrate them, and delete the old API immediately
- Treat temporary adapters as exceptional and time-boxed, not default architecture
- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies** (all three must hold):
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative

**When it does not apply:** a contract that other teams, clients, or deployed services consume. A public HTTP API, a published package, a database schema read by other systems, or a frontend you do not deploy in the same change keeps its compatibility. Follow the [api-and-interface-design](../../api-and-interface-design/SKILL.md) skill for versioning and deprecation there.

Keeping both old and new APIs creates dual-path complexity, slows cleanup, and makes the codebase feel append-only.
