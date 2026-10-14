# Skill improvement guidelines

## Method

1. Cluster observations by root cause after assessment. Count independent incidents, not duplicated logs or continuations.
2. Prioritize severity and recurrence. Inspect successful cases and contradictory evidence before proposing a rule.
3. Verify each finding against the current repository and the agent's configuration before proposing any improvements. Drop what does not verify.
4. You are editing another agent's instructions. Keep those edits small and general. Before editing, state the intended behavioral rule and owning surface in one sentence, then make the smallest change that expresses it.
5. Prefer **replacing** existing guidance over **appending** another paragraph.

## When to propose changes

Do not propose changes by default. Proceed only when a concrete instruction is missing or wrong and the evidence links that gap to the observed failure. Ask: would a competent agent with the current instructions still be expected to fail this way? If yes, there is a gap. If no, defer.

File only when all of these are true:

- The failure is caused by a missing, wrong, or underspecified instruction on a concrete surface: the owning actor's configuration, a skill, or in-repo guidance.
- You can name that owning surface and the one reusable rule it should have stated.
- If that rule had been present and followed, it would plausibly prevent the observed failure without conflicting with successful behavior.
- The same gap appears in more than one source run, or is severe enough that a single occurrence still proves a missing contract.
- The current instructions still contain that gap, and the exact file and version can be identified for a reviewable proposal.

Do not file when:

- The existing instruction already required the correct behavior and the model ignored it
- The proposed gap is merely an unstated implementation method or an extra check that could have caught an ordinary mistake; a competent agent could already derive the required behavior from the task and format contract
- The failure is model variance: same prompt, same tools, different choice
- The only available edit is restating, hedging, or adding examples from these runs
- The real fix is product, infra, scorer, or code outside instruction surfaces

When nothing clears this bar, open no change and say, per finding, why not — that is a success. A speculative change is worse than none.

Store drafts separately from installed files unless application is requested.
An unavailable historical version supports a gap in assessment, not a procedural
accusation. A counterfactual explanation is a hypothesis; state a focused trial
that would test whether the proposed rule improves behavior. Neither findings
nor proposals have a minimum count.

Separate the behavioral contract from implementation detail. For each proposed
gap, state what decision or requirement a competent agent could not resolve from
the existing instructions. If the correct requirement was already clear, treat
the incident as execution failure unless a distinct instruction defect is
demonstrated. Repeated execution failures do not prove a missing instruction.
An explicit wrong rule or a required decision genuinely absent from the contract
can justify a change; omitting the algorithm for an already specified behavior
does not establish that defect.

