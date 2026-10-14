---
name: test-audit
description: "Evaluate whether tests catch meaningful regressions. Use when assessing proposed tests or auditing existing tests for duplication, weak assertions, and implementation coupling."
license: MIT
metadata:
  source: "https://github.com/openclaw/openclaw/tree/91264b958cf11cda9b166fb134f22ca1c796c14c/.agents/skills/test-audit"
---

# Test Audit

Two modes, one value bar: assess proposed tests or audit existing coverage.
Optimize for confidence, not test count or deletion count. Stay within the
requested scope; a review request produces findings, not unsolicited edits.

Read applicable repository instructions and discover the project's test runner,
validation commands, and CI routing from its documentation and configuration.

## Authoring gate

Before adding or approving a test, answer four questions:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage not already catch that failure? Prefer extending
   an existing case over duplicating it. Coverage at another layer needs its own
   distinct risk, such as transport, integration, or lifecycle behavior.
4. Does it require a production export, flag, wrapper, or injection hook solely
   for the test? Prefer the real interface. Investigate whether the hook is an
   unnecessary exposure or a legitimate boundary for isolating dependencies;
   test use alone is not a reason to remove a sound design.

Check the proposed test against the patterns and retention criteria below.
For a bug regression, demonstrate failure on pre-fix behavior for the intended
reason and success after the fix. Use an isolated baseline or controlled
reproduction without disturbing unrelated work. When that proof cannot be
obtained, report the limitation rather than claiming the regression is verified.

## Low-value patterns

Treat these as investigation candidates, not automatic deletion rules:

- Assertion-free probes that only increase coverage numbers.
- Self-comparisons or expected values produced by the code under test.
- Copied inventories, manifests, export lists, or exact source-text assertions
  that merely restate implementation.
- Private predicate or call-shape tests duplicated by stronger behavioral tests.
- Repeated tests of the same contract without a distinct failure mode.
- Tests that exist only to preserve obsolete test-only exports or wrappers.
- Mocks that implement the very behavior being asserted, or substitute one
  identical fake for dependencies with meaningfully different behavior.
- Fixtures that prearrange the state or callback ordering the real code should
  produce, or assertions against a store the exercised path never writes.
- Capability checks that restate flags rather than exercise promised behavior.
- Negative tests that pass because an unrelated guard rejects the input before
  the intended code path is reached.
- Names that claim more than the inputs and assertions actually exercise.

## Retention criteria

Keep tests that independently protect a meaningful contract: an API, protocol,
configuration, migration, storage, security, platform behavior, package,
release, architecture rule, or generated output. Also keep:

- Call ordering when the order is observable behavior.
- Regressions with a credible failure mode.
- Source inspection when it is the cheapest independent contract check and
  survives unrelated identifier or layout changes.
- Tests that catch distinct failures at different layers, even when their
  scenarios look similar.

Static, slow, or implementation-adjacent does not mean useless. A test that
breaks during a behavior-preserving refactor merits investigation, not automatic
deletion. A failing baseline may expose a product bug; never remove a test just
to make the suite pass.

## Audit workflow

Start with read-only discovery. For a small addition or assertion change, read
the test, relevant production behavior, and nearby coverage; apply the authoring
gate without requiring a broader audit. Before removing or consolidating tests,
or when the contract is uncertain, also investigate callers, dependencies, CI
routing, and history explaining why the tests exist. Inspect dependency source
or types when needed to establish the asserted contract. Prefer a few
high-confidence findings over a speculative inventory.

For removal or consolidation candidates, record:

- Its name and location, the contract it protects, and the failure it detects.
- Relevant history and production callers of any helper proposed for removal.
- The stronger remaining proof, or evidence that the contract is obsolete.
- Unique assertions that must move into retained coverage before removal.
- The proposed action: retain, repair, consolidate, or delete.
- Risk and the focused validation command.

An integration test is not automatically stronger than a unit test. Compare the
actual failures each catches, reliability, runtime, and how clearly failures
identify the problem. Consolidate only when retained coverage preserves the
contract and the tradeoff is justified; keep fast, precise tests when they add
distinct value.

Keep uncertain candidates. Missing history or unavailable execution is a
limitation to report, not evidence that a test is redundant.

When edits are requested, make one coherent batch. Preserve unique contracts
before consolidating tests. Remove obsolete support code only after checking
its consumers; do not introduce unrelated production refactors. Record product
bugs as separate findings unless fixing them is within the user's request.

## Validation

1. Capture the relevant baseline results before editing. Keep pre-existing
   failures separate from new failures.
2. Run affected tests and related integration or sibling coverage using the
   project's actual runner. Keep source stable during each run. Confirm that
   tests were discovered and executed; a zero-test run is not a pass.
3. When replacing source inspections, run the executable or contract check that
   now supplies the proof. For repaired weak assertions, demonstrate that the
   intended failure is caught through a controlled input or isolated mutation.
4. Run applicable formatting, static checks, and repository-required validation.
   Update test discovery or CI configuration if tests moved.
5. Review the final diff against the evidence: did any removed test provide the
   only proof of a contract? Restore coverage for any gap before finishing.

Report changes or recommendations, retained false positives, checks actually
run, failures or unavailable checks, and remaining risks. An audit does not
authorize commits, pushes, pull requests, or merges.
