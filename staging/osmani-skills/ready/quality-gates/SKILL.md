---
name: quality-gates
description: "Set up or revise project-specific quality gates with measurable criteria, explicit exceptions, and verified enforcement. Invoke explicitly for quality-gate setup, not routine code review."
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/addyosmani/agent-skills/tree/2686b620fc1fed2e8f60c704839c766b8594c6b6/skills/constraint-driven-development"
---

# Quality Gates

Make agreed quality requirements executable and hard to bypass accidentally.
Reuse the project's tools and conventions. A green check is evidence about what
it measured, not proof that the product is correct or safe.

## 1. Discover the existing gates

Read project instructions, build/test scripts, tool configuration, dependency
locks, CI jobs, and available required-check settings. Identify the installation
and workspace boundaries, supported environments, and the code each check covers.
Distinguish an advisory command, a CI job, and a check actually required to merge.
If remote protection settings are unavailable, report enforcement as unverified.

Measure relevant baselines with existing checks when feasible. Record commands,
versions, candidate identity, scope, and outcomes; distinguish a product failure
from missing tools, credentials, fixtures, or infrastructure. Preserve dirty work
and avoid commands that fix files, install software, or mutate remote state during
discovery unless those actions are authorized.

## 2. Agree the bar

Propose only gates justified by the project's risks: for example types, tests,
secret detection, dependency exposure, accessibility, resource budgets, or module
boundaries. Existing working gates may need no changes. Ask only about unresolved
choices that materially affect cost, coverage, or policy.

When a gate responds to recurring mistakes, identify the shared invariant and
cite distinct failures. Check whether a bounded ownership/interface change or
type construction would remove the opportunity more effectively than another
check. Propose product redesign separately; gate setup does not authorize it.
Prefer repairing existing enforcement, then a targeted static check or behavioral
test, over another reminder. Choose by coverage, cost, and false positives rather
than a mandatory hierarchy. Diagnostics should name the supported correction.

For each proposed gate, state:

- The requirement and why it matters.
- The executable check, covered paths or behaviors, and known blind spots.
- The measured baseline and proposed criterion, including units and any justified
  tolerance for noise. Use project needs rather than default coverage percentages.
- Whether it blocks or warns, where it runs, and its expected runtime.
- The owner and process for an exception or later change.

Get agreement before establishing new policy or installing its tools. If no user
is available, preserve existing gates and report the proposal; do not impose a
new default bar. Approval to draft a skill or policy is not approval to modify a
target project, install dependencies, or change hosted branch protections.

Ratchets can protect a useful baseline, but distinguish existing debt from new
regressions. Compare equivalent workloads and scopes. Baselines must not silently
reset to the current candidate, and legitimate changes in product requirements
may justify a reviewed budget change. Avoid metrics that reward empty tests,
excluded files, or reduced functionality.

## 3. Implement only approved gates

Keep executable configuration authoritative. Prefer existing scripts and CI over
a new runner or mandatory `CONSTRAINTS.md`. Put rationale, ownership, and exception
policy in the project's existing engineering documentation, linking to commands
and configuration instead of maintaining duplicate thresholds.

Use maintained tools appropriate to the installed stack and verify current
version-specific commands. Separate fast local feedback from expensive CI checks.
Use a representative running target for browser checks; report automated coverage
limits rather than treating a scanner pass as complete accessibility validation.

Scope checks by their semantics, not blindly by changed lines. A shared type,
dependency, or configuration change can affect untouched consumers. If diff-scoped,
resolve the correct base, include relevant pending/untracked files in local runs,
and handle renamed/deleted paths. State what broader CI still covers.

Preserve checker failures through wrappers and CI. Required checks must distinguish
violations from execution errors; missing reports, skipped jobs, and zero selected
tests must not silently count as verified success. An intentional no-applicable-work
case needs an explicit, tested rule, not a fallback that swallows errors.

Exceptions must name the specific rule and scope, reason, owner, approval, and
review or expiry condition. Require review of changes that relax thresholds,
suppress findings, remove assertions, skip tests, or alter selection and baselines.
Such changes can be legitimate; do not universally ban suppressions or test removal.
Never auto-remediate vulnerabilities or weaken checks merely to obtain green.

If protection against unauthorized weakening is required, identify who can edit
the gate, baseline, and CI policy and which independently controlled review or
required-check settings enforce it. An agent-editable guard is not tamper-proof.
Propose missing external controls; change them only with explicit authorization.

## 4. Verify enforcement and report

Exercise each new or changed gate on a known passing case and a deliberate,
representative violation. Use isolated fixtures or a disposable checkout, not
destructive edits to the user's working changes. Check failure exit status and
that the wrapper or CI job propagates it. For a recurring-mistake gate, reproduce
a real past failure in isolation when available; otherwise label the violating
fixture as synthetic. Verify a valid nearby case is accepted so the check does
not merely ban the whole construct. Test relevant exclusion, missing-report,
and execution-error cases so a broken checker cannot masquerade as a pass.

Redact sensitive scanner output. Record checks actually run, candidate and scope,
runtime, results, exceptions, and gaps. Local verification does not establish
hosted CI or merge enforcement; distinguish each layer and leave unavailable
layers explicitly unverified. Do not publish, commit, or change remote settings
without authorization.

Finish when the agreed gates are implemented and verified, or report precisely
what remains blocked. Stop adding gates once the agreed risks are covered. For a
staged trial, recommend installation only after a real-project pilot demonstrates
useful detection with acceptable runtime and false positives.
