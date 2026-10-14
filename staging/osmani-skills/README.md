# Osmani adaptations

`ready/quality-gates/` is an explicit-only draft, not an installed skill. No
project gates, dependencies, CI jobs, or branch protections have been changed.

Source: https://github.com/addyosmani/agent-skills at commit
`2686b620fc1fed2e8f60c704839c766b8594c6b6`.
Untouched originals and the MIT license are in `upstream/`: constraint-driven
development and its floor-guard reference, plus doubt-driven development.
The upstream files are provenance, not installed instructions or runnable policy.

Quality gates retains baseline measurement, explicit exceptions, staged checks,
and review of weakened enforcement. It removes mandatory files, numeric defaults,
fixed tools, automatic installation, and blanket bans on test removal or
suppressions. The upstream floor-guard implementation is not adopted or executed;
the draft favors existing tooling and verifies both failure and success paths.

The quality-gates draft also borrows recurring-mistake prevention from pstack's
`correct`: choose proportionate enforcement and test a past failure and a valid
nearby case. Pinned attribution and its MIT notice are in the draft's
`THIRD_PARTY_NOTICES.md`. This does not promote the draft or alter project gates.

Doubt-driven ideas are adapted directly into `skills/challenge-the-design/` as
claim-focused verification and bounded follow-up. The user-defined workflow
requires a blind second assessment and a separate independent judge.
There is no separate installed doubt-driven skill.

Before promoting quality gates, choose a real project, agree the relevant gates,
and verify known-good, known-bad, and checker-error cases without disturbing user
work. Record runtime, false positives, and the difference between local, CI, and
merge enforcement. Structural validation alone is not a completed pilot.
