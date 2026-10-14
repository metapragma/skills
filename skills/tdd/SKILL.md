---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red -> green -> refactor loop: establish missing behavior, implement
it, then improve the design while keeping that behavior intact. Use the testing
guidance below throughout the loop, not only at final review.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything — agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question — how deep the module is, where the seam belongs, what the interface should expose — use the `/codebase-design` skill for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Discover the checks.** Use the repository's test runner, wrappers, and CI
  configuration. Identify a focused command for the current slice and broader
  checks appropriate to its impact; do not assume a language or test command.
- **Red.** Write and run a test for the next missing behavior. Confirm it fails
  for the intended reason, not unrelated setup or infrastructure problems. For
  a bug fix, it must reproduce the reported defect. If it already passes,
  investigate whether the behavior exists or the test misses the case before
  adding implementation.
- **Green.** Add only enough implementation to satisfy that behavior and run
  the focused checks again. Preserve existing assertions and gates rather than
  weakening them to reach green. Do not anticipate unrelated features.
- **Refactor.** With tests green, make small, behavior-preserving improvements
  to the code just exercised when they remove real complexity. Preserve public
  contracts, error behavior, and relevant side-effect ordering. Re-run focused
  checks after each coherent change. Test setup may need adjustment, but the
  behavioral assertions must remain meaningful. Skip this step when no useful
  improvement is evident; green tests are evidence, not proof of equivalence.
- **One slice at a time.** Complete the cycle for one behavior before adding
  the next. If refactoring breaks a check, repair or undo only your affected
  edits before proceeding; preserve unrelated work. Broader redesign belongs
  in a separately scoped task, not an expanding cleanup pass.
- **Verify and review.** Run broader relevant checks before completion and
  report actual outcomes, skipped checks, and limitations. If tests cannot run,
  do not claim an observed red/green cycle. Code review assesses the resulting
  candidate separately; it does not replace in-cycle refactoring or authorize
  edits, commits, or publication.
