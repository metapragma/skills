# Code quality

Use `sound`, `issue`, `not_applicable`, or `insufficient_evidence`. Assess the
final recorded candidate against the task's behavior and project conventions.
Separate correctness, readability, and maintainability when they lead to
different conclusions. Cite concrete code or verification evidence.

Use `not_applicable` for a task that did not change or assess code. Use
`insufficient_evidence` when a task changed code but the final artifact cannot
be recovered. A passing command or confident completion message alone does
not establish that the unseen code is sound. State the extent of verification
even when the visible candidate supports a judgment.

Use `issue` only for a defect or maintainability problem that remains in the
candidate being assessed. A defect corrected during the session can inform
efficiency without making the final code defective. Avoid imposing personal
style rules when project conventions provide a reasonable alternative.
