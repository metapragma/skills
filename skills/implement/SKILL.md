---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Identify which behavior should change and which must stay intact. Use the
supplied requirements and relevant project contracts; ask about material gaps
instead of inventing acceptance criteria.

Use /tdd where possible, at pre-agreed seams.

## Behavior-Preserving Changes

For a refactor, identify the affected public behavior before moving structure:
outputs, errors, compatibility, and relevant side effects or ordering. State the
structural improvement being sought. Keep discovered bugs or new features
separate from the refactor unless the user approves the expanded scope.

Run relevant existing checks on the pre-change candidate and preserve the results
with its revision and relevant dirty-content identity. For meaningful coverage
gaps, capture representative behavior with a characterization test, snapshot,
or old-versus-new comparison using the project's tools. Agree new test boundaries
as required by /tdd. Choose cases that could expose the change, not a mandatory
harness for every rename. If a baseline cannot run, explain the gap before
claiming equivalence; typechecking and lint alone do not establish it.

A characterization records existing behavior, which may include bugs. Compare
it with the intended contract and keep discrepancies visible. Freeze relevant
inputs and control nondeterminism so differences mean something; document any
normalization that could hide a meaningful change.

Refactor in small coherent steps and rerun focused checks after each. Preserve
meaningful assertions; do not update expected results just because the new code
differs. For wider changes, replay the baseline against the final candidate or
compare old and new behavior under equivalent conditions. Account for changed
callers and discovery paths without assuming compatibility obligations vanished.
Report exercised cases, observed differences, and untested paths; matching
samples are evidence, not proof of every possible behavior.

## Validate and Review

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review on the complete task-owned working candidate,
including staged, unstaged, and relevant untracked changes. Pass the spec or
tickets, task scope, and comparison base: HEAD for new uncommitted work, or the
branch merge base when the task includes earlier commits. Preserve unrelated
changes. Resolve actionable findings and recheck affected code after fixes;
the reviewed content must match what is committed.

Commit only task-owned work to the current branch when the user has authorized
committing. Review completion alone does not authorize publication or a commit.
