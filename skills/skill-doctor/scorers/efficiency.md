# Efficiency

Use `direct`, `avoidable_rework`, or `insufficient_evidence`. Judge whether each
action reduced a live uncertainty or verified a changed candidate. The shortest
trace is not necessarily the most efficient investigation.

Expected TDD red tests, a regression reproduction, checks after edits, and
targeted rereads after new evidence are useful work. Identical arguments can
produce relevant new results when code, state, or environment changed. A failed
command is a lead, not proof of waste.

Use `avoidable_rework` for a concrete mistake or redundant action with an
available better path: for example, repeating a check on an unchanged candidate
without a reason, or repeatedly fixing an error an inspected contract already
explained. Cite the original records, context, and consequence. An eventually
fixed defect belongs here when it caused avoidable work; assess the final
candidate separately for code quality.

When prerequisites or the reason for a repeat are missing, use
`insufficient_evidence`. Do not infer elapsed time or cost from tool counts.
