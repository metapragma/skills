# Enforcement

Gaps that are stated but accepted still ship. Make `not run` block the next
step at a point the agent can't bypass. Propose the smallest mechanism that
works, and implement it only with approval.

## Where Each Gate Sits

| Point | Role |
| --- | --- |
| Commit | Warn and record. Agents bypass local hooks, so a commit hook is early feedback, not a gate |
| Agent stop | Optional. A harness stop hook runs `verify` before the agent ends its turn |
| Review | The reviewer refuses to approve without a passing record for the current revision. A blocked check needs an explicit, owned acceptance |
| Merge | The hard gate. CI runs `verify` and blocks the merge on failure. A new commit invalidates the earlier result |

When CI can't run the checks, for example because the runner has no container
access, the review gate carries the weight. Record that limit in the config.

## Human Approval

A human approves at merge only when the change has high **blast radius**:

- authorization or access scope;
- data migrations;
- money or regulated records;
- external messages or other side effects;
- shared modules with many consumers;
- the gate or the checks themselves.

For other changes, the runner's verdict and an automated review are enough. A
fresh-context reviewer stays advisory; it never overrides the runner.

## Budgets

- **Retries.** Cap fix-and-retry cycles on the same failure. The default is 3.
  After that, hand off with the evidence.
- **Time.** Record the duration of each command. When the inner loop grows past
  a few minutes, narrow `fast` rather than skipping it.
- **Proportion.** Size the inner-loop checks to the change and the model. Always
  run the full gate before handoff.
