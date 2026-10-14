---
name: code-review
description: "Review a branch, commit, staged candidate, or working changes for correctness and risk, standards, and specification compliance. Use for code review or review since a fixed point."
---

Review the requested candidate through three distinguishable lenses:

- **Correctness and Risk**: defects, regressions, and missing verification, even
  when neither the specification nor the standards mention them.
- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / spec?

Review is read-only unless fixes are requested. Use one reviewer for a small
change. For a broad change, bounded independent reviewers may cover distinct
lenses when delegation is available and authorized; do not require delegation
to complete a review.

Use the configured issue tracker when needed. If its configuration is missing,
ask the user to invoke `setup` rather than starting setup
automatically. A supplied spec or task description can support review without it.

## Process

### 1. Pin the candidate

State the mode, resolved base and head SHAs, and in-scope paths. Honor the user's
target; ask if ambiguous. A pre-commit implementation review defaults to the
complete task-owned working candidate, not committed history alone.

- **Committed branch/PR:** resolve the actual target branch and compute
  `git merge-base <target> HEAD`. Review `git diff <base-sha> <head-sha>`;
  exclude dirty changes and disclose that exclusion.
- **One commit:** compare the commit with its parent, not a merge base. For a
  root commit use the empty tree; clarify the intended parent of a merge commit.
- **Staged candidate:** use `git diff --cached <base-sha>`. Default the base to
  HEAD; read the index versions, not unstaged working-file replacements.
- **Complete working candidate:** use `git diff <base-sha>` for tracked content.
  For uncommitted work default to HEAD; for a whole branch including pending
  edits use its pinned merge base. Also inspect relevant untracked files from
  `git ls-files --others --exclude-standard -z`: ordinary diffs omit them.

For dirty work, inspect `git status --short`, `git diff --cached`, and `git diff`
to distinguish staged from unstaged content. In working mode, evaluate the final
combined candidate; flag an index-only defect separately if a staged-only commit
would reintroduce it. Never claim the index was reviewed by reading only the
working tree. Preserve unrelated dirty work and report scope exclusions; ask
when task ownership cannot be determined. Do not stash, reset, or stage files
merely to assemble a review.

Validate refs before reviewing. An empty tracked diff is not an empty candidate
until staged and relevant untracked content have been accounted for in the
selected mode. Report genuinely empty scope without inventing findings.

Bind evidence to the reviewed content: use immutable Git objects for committed
and index snapshots, and record content hashes or a read-only copy of in-scope
working/untracked files plus their path inventory. Before reporting, verify
that the selected content has not changed, including added or removed paths.
If it changed, re-review affected content or report the review as stale. A base
SHA or an unchanged status listing alone does not identify dirty file contents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Use the user's task description as requirements when sufficient. If intent
   remains unclear, ask. Without a spec, mark Spec as unavailable and continue
   correctness and standards review; do not invent requirements.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Use these as investigation prompts, not findings by themselves. Establish a
concrete comprehension, coupling, or maintenance cost before recommending a
change; choose the smallest remedy that preserves useful boundaries.

- **Mysterious Name**: a name obscures the concept in its actual context; consider a clearer domain term.
- **Duplicated Code**: repeated logic represents the same rule and must change together; consider sharing it, not merely merging similar syntax.
- **Feature Envy**: knowledge of another module's internals creates coupling; consider moving the behavior toward its owner.
- **Data Clumps**: fields travel together because they form a coherent concept; consider a type when it clarifies their relationship.
- **Primitive Obsession**: interchangeable primitives obscure distinct meanings or invariants; consider a domain type where it prevents misuse.
- **Repeated Switches**: duplicated dispatch rules drift; consider one owner or dispatcher. A clear switch alone does not justify polymorphism.
- **Shotgun Surgery**: one rule requires coordinated edits in unrelated places; consider consolidating its ownership.
- **Divergent Change**: unrelated responsibilities force changes to the same module; consider separating them when it reduces coupling.
- **Speculative Generality**: unused flexibility adds present complexity without a supported consumer; consider simplifying after checking compatibility obligations.
- **Message Chains**: callers depend on internal navigation details; consider exposing the operation they actually need.
- **Middle Man**: delegation adds no meaningful boundary; consider removal only after checking policy, compatibility, and substitution roles.
- **Refused Bequest**: an implementation cannot honor its inherited contract; consider composition or a narrower interface.

### 4. Review the selected content

Read the changed code and the callers, dependencies, and tests needed to judge
it. A diff alone may not show the relevant contract. For staged or committed
reviews, inspect surrounding source from the same snapshot, not dirty files.

- **Correctness and Risk:** trace plausible failures and regressions. Investigate
  security, concurrency, data integrity, performance, and operability where the
  change makes them relevant. Check whether tests exercise the claimed behavior
  and whether reported validation applies to this candidate. A skipped or failed
  check is not a pass. Do not weaken tests or gates during review.
- **Standards:** cite documented rules for violations; label smell-based findings
  as judgment calls. Avoid duplicating lint output or speculative refactors.
- **Spec:** identify missing requirements, incorrect behavior, and unrequested
  scope, citing the relevant requirement.

Check test effectiveness against the requirements, not just agreement with the
implementation. For a bug fix, identify an assertion that distinguishes the
broken behavior from the fix; inspect relevant error and boundary paths. Report
whether regression sensitivity was demonstrated or only inferred from reading.
Match verification to the claim: performance claims need representative baseline
and candidate measurements; visible UI behavior may need browser interaction or
screenshots. Unit tests alone do not establish either. Disclose unavailable
evidence without inventing results or requiring irrelevant checks.

Judge the resulting structure, not only the added lines. Trace ownership and
dependencies far enough to spot feature logic leaking into general modules,
hidden invariants, or a refactor that merely redistributes complexity. Assess
reader load along two axes: layers to trace and mutable state to remember. Follow
where values originate, who can change them, and any hidden ordering or duplicate
state that must stay synchronized. Before suggesting removal of a layer, check
the policy, invariants, compatibility, or substitution it provides; one caller
alone does not make it redundant. File size, line count, and helper count are
signals, not quality gates. For an actionable structural finding, explain the
concrete cost and suggest a bounded remedy, not an unrequested redesign. Separate
introduced or worsened problems from existing debt; mention existing debt only
when it materially affects this change.

When code is replaced or removed, check for newly orphaned callers, exports,
configuration, and dependencies. Check public consumers, dynamic registration,
and build/runtime discovery before calling something unused; lack of local
references alone is insufficient. Report cleanup candidates without deleting them.

For changes to shared behavior, data formats, lifecycle ordering, shared mutable
state, dependencies, trust boundaries, authorization, sensitive data, LLM tools,
queries, caches, or resource-intensive paths, read the applicable
sections of [Risk Checks](references/risk-checks.md). These are scoped review
prompts, not a mandatory whole-system audit. The Change Propagation section covers
indirect consumers and the assumptions that make a change safe beyond the diff.

If delegating, give each reviewer the exact candidate, scope, source access,
relevant requirements and standards, and a read-only assignment. Verify their
findings against the candidate; agreement between agents is not proof. Avoid
arbitrary output limits that could hide a serious defect.

For a contested design or a high-risk change, an independent second reviewer
helps when delegation is available: give a fresh agent the same candidate and
intent, without your own findings or reasoning. Say whether it was the same
model family as the author.

### 5. Aggregate

Lead with actionable findings ordered by severity. Label each finding's lens
so correctness, standards, and requirements remain distinguishable. Deduplicate
the same defect across lenses without dropping its evidence.

Each finding needs a file and line reference in the reviewed version, a concrete
failure or violated rule, impact, and evidence or a way to verify it. Separate
confirmed defects from unproven risks and intentional tradeoffs.

When more than one reviewer contributed findings, apply
[Lead Judgment](references/lead-judgment.md) before writing the report.

Distinguish required changes from optional suggestions as well as severity.
Require changes for substantiated defects, material risks, or unmet requirements;
state the evidence needed to resolve an uncertain risk. Keep taste and alternative
design preferences optional, and omit low-value nits. Accept sound improvements
that meet requirements and project conventions without demanding perfection or
unrelated cleanup. A favorable review is not permission to merge or deploy.

Finish with the reviewed mode and snapshot, exclusions, checks actually run,
and remaining gaps. State clearly when no issues were found, without implying
that unavailable checks passed. Relevant changes after review invalidate the
affected conclusions and require rechecking before claiming approval.
