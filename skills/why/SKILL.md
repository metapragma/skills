---
name: why
description: "Investigate the historical rationale behind code or a design decision, separating documented intent from inference."
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/why"
---

# Why

Recover the reasons a system took its current shape. Code establishes what it
does; history and contemporary records may establish why it was built that way.
A plausible explanation is not evidence of intent.

This is a read-only investigation, not approval to change the code, record a new
decision, or contact its authors. Use available, authorized sources within the
named project and topic; redact secrets and unrelated private material.

## 1. Anchor the Question

Identify the decision, relevant paths and symbols, and the rationale the user
wants recovered. Resolve a clear referent from context; ask only when ambiguity
would materially change the investigation. Treat any reason the user suggests
as a hypothesis to check, not a conclusion to confirm.

Inspect the current implementation, callers, tests, project instructions, and
relevant domain documents or ADRs. Note the checkout revision and pertinent
pending changes. Distinguish historical code from the version in front of you.

## 2. Trace the Decision

Start with the closest evidence: comments, ADRs, Git history, and linked PRs or
tickets. Follow introduction, later revisions, and reverts as needed; blame
identifies last touch, not necessarily the originating decision. Account for
renames and moves. Useful commands, with actual paths and ranges substituted:

```bash
git blame -L <start>,<end> -- <file>
git log --follow -p -- <file>
git log --oneline -20 -- <file>
git show <commit> -- <file>
```

Read substantive commit messages and available PR bodies, review discussions,
and linked issues. Use the project's tracker or source-control tools rather
than assuming GitHub, a particular CLI, or a merge-message format. A checkout
without history can still support an investigation; report that limitation.

For each candidate explanation, collect the source, date/revision, what it
actually says, and how it relates to the target. Contemporary tests can reveal
the protected behavior without proving the author's reason for protecting it.
Separate the original motivation, later constraints, and present applicability.

## 3. Widen Only Where It Helps

When local history leaves a material question unanswered, inspect relevant
available sources: design documents, team discussions, incident reports, error
tracking, observability, or analytics. Discover connectors from the current
environment; do not assume a runtime-specific MCP directory or expand access.
Prefer linked records and narrow queries over mining whole accounts.

For defensive code, look for the incident or failure that prompted it. For a
threshold, look for a requirement or measurement recorded at the time. Present
runtime data may corroborate a mechanism but cannot establish past intent by
itself. Distinguish stale constraints from constraints shown to hold today.

For a broad investigation, bounded read-only source slices may be delegated when
available and authorized. Give each worker the same question and code anchor,
its source scope, and the confidence rules below. Require citations and search
gaps. Serial investigation is sufficient; no particular model or agent roster
is required. Verify decisive findings against their sources yourself.

Stop when the question is supported well enough to answer, or remaining progress
needs unavailable evidence or a human decision. Avoid a mandatory sweep of every
source category. Record material sources not searched and why, especially when
their absence limits the answer.

## 4. Calibrate the Answer

Classify substantive rationale claims by their evidence:

- **Direct:** a source explicitly states the reason. Cite it and identify whose
  explanation it is; an author's claim is not proof that the design succeeded.
- **Supported:** independent evidence converges without an explicit statement.
  Show the evidence and explain the inference rather than reporting intent as fact.
- **Inferred:** a reasonable interpretation with incomplete support. Name the
  reasoning and qualify it as likely or apparent.
- **Speculative:** a possible explanation among alternatives. Label it as a
  hypothesis and identify the evidence needed to distinguish it.
- **Unknown:** relevant searches did not establish the reason. Say what was
  searched and what remains missing.

Resolve contradictions by dates, versions, and source scope where possible;
otherwise retain both accounts. Do not prefer the latest record automatically,
turn missing evidence into proof that a constraint never existed, or rationalize
the code as necessarily intentional or correct. Agreement between agents is not
additional source evidence. Preserve confidence qualifications during synthesis.

## Report

Lead with the best-supported answer. Cite the code anchor and decisive historical
records, then separate documented reasons, interpretation, competing accounts,
and unresolved gaps as needed. Use only sections the question earns. Include the
material searches and unavailable sources; links should resolve to the actual
record, commit, or file version rather than a search page.

If this precedes a change, identify constraints to preserve, reasons that may no
longer apply, and checks needed before removal. Label recommendations separately
from historical findings. Do not treat a recovered explanation as authorization
to implement, publish, or rewrite the project's decision records.
