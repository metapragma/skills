---
name: verification
description: Verify a change by running the project's real checks and reporting evidence, or set up and repair the verification paths an agent needs in a codebase. Use when finishing a change, when asked to prove something works, or when asked to set up or audit verification.
---

# Verification

A claim about a change is only as strong as the checks that actually ran
against it. Project commands produce the **verdict**: the exit code is the
result, and the agent's own report never stands in for it. This skill decides
which checks a change needs, runs them, and reports **evidence**. Each required
check ends as `passed`, `failed`, `blocked`, or `not run`, and the report marks
every gap visibly.

## Route

Read `docs/agents/verification.md` in the target repository. It is the
**project config**: surfaces, commands, identities, journeys, and gotchas.

- **No config:** run setup. Read [references/setup.md](references/setup.md).
- **Audit:** use this mode when the user asks for one, or when a command or
  recipe misled this run. Read [references/audit.md](references/audit.md).
- **Otherwise:** follow use mode below.

For each surface the change touches, read the matching file in
[references/surfaces/](references/surfaces/). Read only those.

## Use Mode

1. **Acceptance.** Before running anything, list the checks this change must
   pass. Take them from the project config and the project's risk policy. A bug
   fix needs a test that goes **red** on the pre-change revision and green
   after. Done when every changed behavior maps to at least one named check.
2. **Inner loop.** Run the fast command on the changed scope while you work.
   When the same failure survives 3 fix attempts, stop. Report the failure with
   its evidence, and keep the check unchanged.
3. **Running system.** Do this when the change touches a surface the config
   lists as runnable:
   1. Start an **owned** instance.
   2. Run doctor until the instance is **usable**.
   3. Drive the affected journey the way a user or client would.
   4. Observe the durable effects.
   5. Tear down only what you started.

   Done when each affected journey has a status.
4. **Gate run.** Run the full verify command on the final revision, then the
   integrity check in [references/integrity.md](references/integrity.md). Done
   when both finish on the revision you are about to hand off. Results from an
   earlier revision don't count.
5. **Report.** Give the evidence table described in
   [references/evidence.md](references/evidence.md). For each `blocked` or
   `not run` check, name a reason and the person who owns the gap. Screenshots
   and video are artifacts the user requests; capture them when asked.

A change with high blast radius also needs a human approval at merge. See
[references/enforcement.md](references/enforcement.md).

## Rules

- **Ready means usable.** An instance is ready when one authenticated journey
  succeeds. A port that answers is not enough.
- **Zero means failed.** A command that ran zero tests reports `failed`, even
  when its exit code is 0. The same holds for a required case that was skipped.
- **Changes to checks are integrity items.** Change a test, assertion,
  threshold, snapshot, or CI step only when the requirement itself changed.
  Record every such change in the evidence.
- **Owned and isolated.** Use dynamic ports, separate data, and resources that
  carry this run's name. Clean up by name or recorded ID only.
- **Local first.** Verify against disposable local instances. Shared or live
  environments need explicit permission for each action. A `localhost` address
  can still forward to a shared or production system, so check where it leads.
