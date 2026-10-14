# Integrity

A green run proves something only if the checks still work. Agents under
pressure tend to weaken checks rather than fix code. Common moves:

- deleting or skipping tests;
- loosening assertions;
- raising thresholds;
- updating snapshots;
- adding `|| true`;
- committing with `--no-verify`.

Look for these moves mechanically. Don't rely on honesty.

## Diff Check

Compare the candidate with its merge base. Record each finding in the evidence
`integrity` list with its file and line:

| Finding | What to look for |
| --- | --- |
| Removed test | A deleted test file, test function, or table case |
| Added skip | New skip markers: `t.Skip`, `.skip`, `@pytest.mark.skip`, `xit`, `#[ignore]`, and similar |
| Weakened assertion | An assertion removed or loosened, such as an exact match replaced by a `contains`, or a widened tolerance |
| Changed gate | CI workflows, lint config, coverage or performance thresholds, required-case lists, or `|| true` added to a check command |
| Updated snapshot | Golden or snapshot files changed |
| Bypassed hook | `--no-verify` or hook-disable variables in the session's commands |

Count untracked gate files too, including files that a local exclude hides from
`git status`.

A finding is not automatically wrong. A requirement can change, and an obsolete
test can be removed. Each finding needs a reason that traces to the changed
requirement. A reviewer then decides. A finding without a reason fails the
integrity check.

## Red Before Green

For a bug fix or a new behavior, show that the new test fails without the
change:

1. Run the new test against the pre-change revision, in an isolated copy or a
   worktree.
2. Confirm that it fails on the asserted behavior. A compile error or a
   missing fixture doesn't count.
3. Run it on the candidate and confirm that it passes.

Record both runs. A test that was never red only shows that the code passes it,
not that it detects the defect.

## Detector Strength

Setup mode proves the paths with a planted defect. For ongoing strength, use
optional mutation testing on the changed files. Run it at the merge gate, not
in the inner loop. Treat surviving mutants in changed code as review input, not
as a score to maximize.
