---
name: retro
description: "Review a coding session and recommend evidence-backed improvements to the agent's environment."
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/in-progress/retro"
---

# Retrospective

Review the session the user names, or the current session by default. This is
an explicitly requested retrospective, not a mandatory end-of-task step.
Report recommendations first; change files, tooling, or configuration only when
the user asks. Do not require other skills or a particular agent runtime.

## Gather evidence

Read the available session messages, commands, results, and relevant repository
files. Inspect only logs needed for the requested session. Redact secrets and
omit unrelated private content. If the session or a crucial result is missing,
state the limitation rather than reconstructing it as fact.

For each recommendation, identify the concrete event, its effect on the work,
and the environmental change that could have prevented it. Distinguish observed
failure from a hypothesis. One incident can justify a fix, but does not by
itself justify a permanent rule for every project.

## Look for useful improvements

- **Navigation:** missing pointers, unclear ownership, or hidden dependencies
  that caused unnecessary exploration.
- **Checks:** mistakes that a test, type checker, linter, or existing CI gate
  could catch. Inspect existing commands and wiring before proposing new tools.
  Prefer repairing a broken or unused check over duplicating it.
- **Standards:** separate mechanically enforceable rules from judgment calls.
  Recommend deterministic checks for the former and concise review guidance for
  the latter. Both implementers and reviewers need the context relevant to their
  work; a diff alone may not establish correctness.
- **Instructions:** conflicting, stale, or redundant guidance. Prefer improving
  an existing instruction over adding another mandatory process.
- **Tool use:** expensive, repetitive calls that a better query or existing
  tool could replace. Propose custom tooling only when the benefit justifies it.
- **Information access:** missing logs, documentation, or environment facts that
  blocked reliable decisions. Identify any permissions needed; do not expand
  access or expose credentials as part of the retrospective.

Do not manufacture a finding for every category. Scale recommendations to the
impact and evidence; avoid treating missing infrastructure as automatically
wrong for a prototype or small project.

## Assess importance

Assess each finding by its effect and reach. Require the wider prevention
analysis below when evidence supports at least one of these conditions:

- **Serious effect:** a failure or concrete failure path can cause data loss,
  unauthorized access, an incorrect critical result, or a major service failure.
- **Repeated cost:** distinct incidents have the same cause and produce
  substantial repair time or repeated disruption.
- **Shared cause:** a defect in shared code or configuration exposes several
  features to a failure with a significant effect.

For repeated failures, group incidents by the rule they violate, not similar
wording. Inspect relevant available commits, reverts, review feedback, or prior
checks; keep the search scoped. Several mentions of one incident are not several
failures. If earlier evidence is unavailable, label repetition as unverified.

Keep low-impact findings with no substantial combined cost local. Judge risk and
cost in the project's context, without a fixed score or quota. State missing
evidence; a possible wider problem is not an established pattern.

## Prevent important failures

For each finding that meets the risk rule, identify the cause and the rule the
system must preserve. Trace relevant shared code, callers, or configuration to
establish where else the same failure can occur. Explain why existing checks let
it through, or state what evidence is missing. Limit this search to the cause
and affected paths, rather than starting a general codebase audit.

Look for the smallest proportionate way to prevent that class of failure:

1. Remove the opportunity through clear ownership, one source of truth, or a
   narrower interface when a bounded structural change earns its cost.
2. Use types or validated construction to exclude invalid states where the
   project's language can enforce the required rule.
3. Repair or add a targeted lint or static check for rules that can be checked
   automatically. Its error should name the supported fix, not just reject code.
4. Protect observable behavior with a regression test for mistakes those
   mechanisms cannot exclude. Check that the test distinguishes the failure.
5. Keep concise instructions for judgment calls and context the mechanism cannot
   convey. Link existing enforcement instead of maintaining duplicate policy.

A check detects a violation; a gate blocks further work, such as merging, when
the required check fails. For a proposed check, name the covered paths, known
gaps, and where it must run. State whether it should warn or block. Inspect
existing wiring before proposing a new gate; an optional command alone does not
establish enforcement.

Prefer prevention over another reminder, but do not require a refactor, tool,
or gate for every important finding. A wider analysis can conclude that a local
fix is sufficient; explain why it covers the cause and affected paths. State why
more intrusive enforcement is not warranted. A check passing today does not show
it would have caught the past mistake: propose replaying a representative failure
and a valid nearby case in isolation. Include a check that the gate reports the
failure and blocks the change. Note false positives and gaps rather than
promising permanent prevention.

When the project keeps an agent instruction file, recommend pairing each of
its rules with what enforces it: a check, a type, a test, or "judgment only".
A correction that repeats an existing rule with no enforcement is a repeat
failure. Recommend moving that rule up the list above in the same change, and
retiring a rule once its mistake can no longer happen.

Keep this a recommendation until changes are requested. Approval to improve a
skill is not approval to alter a target project's architecture, gates, or CI.

## Report

Present the highest-impact recommendations first. For each, give the session
evidence, proposed change, appropriate scope (task, project, or personal), and
how a later run would show whether it helped. Separate measured costs from
estimates. Name useful existing practices to preserve when relevant.

For each important finding, include the reason it meets the risk rule and the
wider analysis above, or name the evidence that prevents a conclusion. Check
that every finding that meets the rule is accounted for. Keep other findings
brief; they need no expanded analysis or new gate.

Finish with the smallest worthwhile next step, or say that no environmental
change is justified. The output is advice, not authorization to implement it.
