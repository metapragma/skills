---
name: challenge-the-design
description: Re-evaluate an existing feature or architecture proposal from the codebase-wide, long-term perspective; develop a stronger design, review it adversarially but fairly, and synthesize one final recommendation. Use after a Grill Me or planning session, when a proposal feels like a local optimum or averaged compromise, when asked for the best bigger-picture solution for long-term health, maintainability, or quality, or when asked to challenge and synthesize a proposed design before implementation.
---

# Challenge the Design

Run an architectural second pass over an existing proposal. Treat the proposal
as a candidate, not an anchor. Produce two independent assessments, then have a
third, independent judge compare them and deliver one evidence-backed design.

## Required agent workflow

1. The primary agent produces Assessment A using Pass 1.
2. A fresh subagent produces Assessment B using Pass 2, without seeing A.
3. A different fresh subagent acts as judge using Pass 3, receiving both complete
   assessments and the common task context. The judge owns the final synthesis.

These are required roles, not three modes simulated by the primary agent.
Invoking this skill requests this delegation, subject to runtime permissions.
If separate fresh contexts cannot be created, disclose the limitation and ask
how to proceed; do not silently substitute self-review or claim completion.
Do not require different models or external model CLIs.

Prepare one neutral brief containing the original user proposal, settled user
decisions, requirements, constraints, known unknowns, and repository/artifact
locations. Both assessors get the same brief and access to relevant source,
callers, tests, and ADRs. Identify the checkout and candidate version; if relevant
content changes, reconcile or rerun affected assessments before judging them.
Keep task facts separate from the primary agent's interpretations and preferences.

Create the second assessor and judge without inherited conversation history
(for tools with this control, use `fork_turns: "none"`). Supply the role-specific
instructions explicitly; do not ask subagents to invoke this whole workflow and
recursively spawn more agents. Keep their work read-only. Do not share Assessment
A, its preferred design, or its private reasoning with the second assessor, even
as a summary. Each assessor can investigate the repository independently.

Do not equate long-term thinking with more abstraction, infrastructure, or scope. A strong local design may win. Optimize for a coherent codebase, not the most ambitious diagram.

Treat “long-term” as minimizing sustained cognitive and change cost while protecting known invariants and credible evolution, not maximizing generality.

## Operating rules

- Preserve settled answers from the preceding discussion or Grill Me session. Do not restart the interview.
- Research questions in the repository instead of asking the user when the answer is discoverable.
- Separate facts, inferences, assumptions, and unknowns.
- Infer future pressure only from product direction, repeated patterns, existing extension points, or other repository evidence. Do not invent a roadmap.
- Prefer conceptual integrity, clear ownership, change locality, deep interfaces, and reversible evolution over pattern compliance for its own sake.
- Do not average competing designs. Synthesis means adjudicating disagreements and choosing a coherent result.
- Do not modify code or documents unless the user explicitly requests it.

## Establish the evidence base

Read the existing proposal and the conversation that produced it. Then inspect:

- repository instructions and domain documentation
- `CONTEXT.md`, relevant ADRs, plans, PRDs, and architecture documents
- affected modules, callers, dependencies, data ownership, and external contracts
- persistence, jobs, events, configuration, permissions, and failure handling
- tests and history that explain important constraints or deliberate tradeoffs

Extract the actual problem, non-negotiable invariants, present constraints, expected lifetime, and likely axes of change. Note conflicts between the proposal and runtime behavior.

## Pass 1: Reframe and redesign

### Diagnose the initial proposal

Steelman it first. State what it optimizes for, why it is attractive, and which constraints it handles well.

Then test whether it is a local optimum:

- Does it solve one feature while duplicating a broader domain capability?
- Does it preserve the wrong ownership or dependency direction?
- Does it expose implementation knowledge to callers?
- Does it add another source of truth, state machine, or policy location?
- Is it copying a local pattern whose original tradeoff no longer applies?
- Does it make the immediate diff small by exporting complexity to maintenance, testing, migration, or operations?
- Is the problem framed at the correct level of abstraction?

### Explore materially different options

Develop credible solution shapes at different levels of intervention. When supported by the repository, compare:

- the strongest version of the local proposal
- a domain or module-level redesign
- a broader shared capability or changed ownership model
- doing less, deferring machinery, or removing an unnecessary requirement

Do not create fake variety by renaming the same structure. Reject speculative platforms, pass-through layers, and generic abstractions with only hypothetical consumers.

Require every new abstraction to own meaningful policy, state, invariants, or complexity. Apply the deletion test: if removing it would not redistribute substantial complexity or weaken an invariant, it has not earned its place.

Evaluate each option for:

- domain fit and conceptual integrity
- ownership, dependency direction, and change locality
- interface depth and knowledge exposed to callers
- data integrity, concurrency, security, and failure isolation
- testability, debuggability, observability, and operability
- compatibility, migration, rollout, rollback, and reversibility
- cognitive load and maintenance cost
- credible future changes made easier or harder
- delivery cost and new complexity introduced now

Choose the strongest long-term candidate. Specify its responsibilities, conceptual interfaces, invariants, data and control flow, failure ownership, and evolution path clearly enough to review.

Freeze Assessment A with its evidence, alternatives, recommendation, tradeoffs,
and unresolved claims. Do not revise it to match Assessment B before judging.

## Pass 2: Independent second assessment

The second assessor starts from the neutral brief and original proposal, not
Assessment A's redesign. Independently apply the evidence gathering and design
criteria in Pass 1, choose a recommendation, and challenge its own candidate
using the checks below. Agreement with A is neither a goal nor a failure; the
assessor must not be told to invent an opposing design.

Select the claims whose failure would materially change the design decision.
For each, state the invariant, the conditions under which it is claimed to hold,
and why it matters. Keep assumptions separate from observed evidence. Focus on
the highest-risk uncertainties rather than manufacturing a quota of objections.

Try to construct a concrete counterexample or failure trace. Identify the source,
existing test, measurement, or smallest experiment that would distinguish the
claim from that counterexample. Inspect available evidence; propose experiments
that require edits, external access, or consequential actions rather than treating
design review as permission to perform them. Distinguish checks actually run from
proposed checks, and partial evidence from proof of the whole claim.

Begin with the strongest case for the candidate and the conditions under which it succeeds. Then try to disprove it using repository evidence and concrete scenarios:

- unexpected but valid product evolution
- partial failure, retry, concurrency, and recovery
- migration from current data and behavior
- mixed-version deployment and rollback
- authorization, privacy, and trust boundaries
- load, operability, debugging, and incident response
- bypass paths and enforcement of invariants
- test seams and sources of nondeterminism
- coupling to framework, storage, transport, or current consumers
- team comprehension and routine change cost

For every criticism, give evidence, impact, likelihood, and the smallest credible remedy. Classify it as:

- **Fatal**: invalidates the design or its core premise
- **Must fix**: retain the direction but revise it before implementation
- **Accepted tradeoff**: real cost outweighed by benefits
- **Unproven risk**: requires validation or a spike
- **Rejected objection**: does not survive evidence or proportionality

Do not manufacture objections for symmetry. Do not reward novelty, maximal flexibility, or theoretical purity. Critique the design at the same level of rigor used to create it.

“No material objection found” is a valid review result. If a fatal flaw exists, reject the candidate, promote the strongest remaining alternative, and run a focused adversarial review of that alternative before synthesis.

Return Assessment B with the same substance as A: problem framing, source
evidence, alternatives, recommended design, tradeoffs, and unresolved claims.
Freeze it before passing both assessments to the judge. Independence here means
separate reasoning contexts, not guaranteed statistical independence or correctness.

Validate every objection against the contract and repository evidence. Correct
misunderstood or incomplete context before changing a sound design. Reviewer
confidence, disagreement, or agreement is not evidence on its own.

Recheck material revisions against the affected claims, not the entire review by
default. Stop when no material objection remains unresolved, or further progress
requires missing evidence or a user decision. If another pass only repeats known
objections without new evidence, report the unresolved risk and next discriminating
check rather than looping. The original proposal may stand; unresolved issues
must remain visible rather than becoming an implied approval.

## Pass 3: Independent judge and final synthesis

Spawn a new judge, not either assessor. Give it the neutral brief, both complete
frozen assessments labeled A and B, and access to the same repository evidence.
Do not identify a favored answer or coach the judge toward the primary agent's
recommendation. The judge must inspect decisive claims against source rather
than treating agreement or confident prose as proof.

Compare the assessments' problem framing, assumptions, alternatives, evidence,
and tradeoffs. Identify substantive agreements and disagreements. Resolve each
material disagreement by the contract and evidence, not majority vote, author
identity, or splitting the difference. The judge can select either design,
synthesize compatible parts, retain the original proposal, or reject both.

Adjudicate each material criticism explicitly: accept it, partially accept it, reject it, or mark it unresolved, with a reason.

Reconstruct the design from the surviving principles and constraints. Do not bolt every accepted suggestion onto the candidate; reconsider the whole when criticism changes a core premise. The final answer may retain the candidate, revise it, combine compatible elements, return to the original proposal, or recommend not building the abstraction.

Choose one direction. Identify the smallest first step that preserves a path to the target architecture, and separate that from shortcuts that would permanently undermine it.

If decisive evidence is missing, give a conditional verdict and the smallest
check or user decision needed to settle it. The primary agent delivers the
judge's final result faithfully; it must not silently replace that verdict with
its own. If a factual error is discovered, send the evidence back to the judge
for correction and report any remaining disagreement explicitly.

## Output

The judge produces one final synthesis rather than a transcript of competing
voices. Include:

1. **Verdict**: the recommended direction in direct language.
2. **Problem and constraints**: the durable problem, invariants, and evidence-based change horizon.
3. **Bigger-picture map**: relevant ownership, modules, callers, dependencies, data, and flows in project vocabulary.
4. **Initial proposal assessment**: what it gets right and where it is or is not a local optimum.
5. **Options considered**: genuinely different designs and their decisive tradeoffs.
6. **Adversarial findings**: material objections, classification, and disposition.
7. **Final design**: responsibilities, conceptual interfaces, invariants, dependency direction, data flow, and failure ownership.
8. **Assessment comparison**: decisive agreements and disagreements between A and B, their disposition, and what stays or changes from the original proposal.
9. **Evolution path**: staged implementation and migration with validation and rollback points.
10. **Costs, risks, and invalidation conditions**: honest downsides, unresolved evidence, and signals that would require revisiting the decision.

Be decisive without pretending certainty. Make the reasoning inspectable enough that another engineer can disagree with a specific premise rather than the whole recommendation.

## Quality gate

Before finishing, verify that:

- Assessment B ran in a fresh subagent context without access to Assessment A
- a separate fresh judge received both full assessments and produced the verdict
- the final response identifies completion of both assessments and the judge,
  or clearly reports which required role could not run
- the system was mapped beyond the files named in the proposal
- at least one materially different problem framing was considered
- the preferred candidate was frozen and genuinely challenged
- criticisms are evidence-based, proportional, and resolved in the synthesis
- the final design is coherent rather than an averaged compromise
- complexity is removed, contained, or consciously paid for rather than renamed
- the migration path can begin incrementally without trapping the codebase in the tactical state
- speculative benefits and unknowns are labeled
- the recommendation is concrete enough to guide the next planning or implementation step
