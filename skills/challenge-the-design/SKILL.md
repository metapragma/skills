---
name: challenge-the-design
description: Re-evaluate an existing feature or architecture proposal from the codebase-wide, long-term perspective; develop a stronger design, review it adversarially but fairly, and synthesize one final recommendation. Use after a Grill Me or planning session, when a proposal feels like a local optimum or averaged compromise, when asked for the best bigger-picture solution for long-term health, maintainability, or quality, or when asked to challenge and synthesize a proposed design before implementation.
---

# Challenge the Design

Run an architectural second pass over an existing proposal. Treat the proposal as a candidate, not an anchor. Produce one evidence-backed final design through three separate modes of thought: redesign, adversarial review, and synthesis.

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

## Pass 2: Review the candidate adversarially but fairly

Freeze the candidate before reviewing it. Do not silently repair it while searching for flaws.

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

When independent agents are available, give the frozen candidate, constraints, and source evidence to a separate critic. Do not give the critic the intended verdict. Keep synthesis with the primary agent.

## Pass 3: Synthesize one final design

Adjudicate each material criticism explicitly: accept it, partially accept it, reject it, or mark it unresolved, with a reason.

Reconstruct the design from the surviving principles and constraints. Do not bolt every accepted suggestion onto the candidate; reconsider the whole when criticism changes a core premise. The final answer may retain the candidate, revise it, combine compatible elements, return to the original proposal, or recommend not building the abstraction.

Choose one direction. Identify the smallest first step that preserves a path to the target architecture, and separate that from shortcuts that would permanently undermine it.

## Output

Present one final synthesis rather than a transcript of competing voices. Include:

1. **Verdict**: the recommended direction in direct language.
2. **Problem and constraints**: the durable problem, invariants, and evidence-based change horizon.
3. **Bigger-picture map**: relevant ownership, modules, callers, dependencies, data, and flows in project vocabulary.
4. **Initial proposal assessment**: what it gets right and where it is or is not a local optimum.
5. **Options considered**: genuinely different designs and their decisive tradeoffs.
6. **Adversarial findings**: material objections, classification, and disposition.
7. **Final design**: responsibilities, conceptual interfaces, invariants, dependency direction, data flow, and failure ownership.
8. **Decision delta**: what stays, changes, and is discarded from both the initial and first-pass proposals.
9. **Evolution path**: staged implementation and migration with validation and rollback points.
10. **Costs, risks, and invalidation conditions**: honest downsides, unresolved evidence, and signals that would require revisiting the decision.

Be decisive without pretending certainty. Make the reasoning inspectable enough that another engineer can disagree with a specific premise rather than the whole recommendation.

## Quality gate

Before finishing, verify that:

- the system was mapped beyond the files named in the proposal
- at least one materially different problem framing was considered
- the preferred candidate was frozen and genuinely challenged
- criticisms are evidence-based, proportional, and resolved in the synthesis
- the final design is coherent rather than an averaged compromise
- complexity is removed, contained, or consciously paid for rather than renamed
- the migration path can begin incrementally without trapping the codebase in the tactical state
- speculative benefits and unknowns are labeled
- the recommendation is concrete enough to guide the next planning or implementation step
