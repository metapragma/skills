# Lead Judgment

Use this when more than one reviewer produced findings: delegated lens
reviewers, an independent second reviewer, or automated review comments. You
are the lead reviewer. Filter and decide; don't just aggregate. The other
reviewers saw a slice of the code and a short statement of intent. You know
what was tried, what constraints exist outside the code, and what is temporary
scaffolding.

## Filters

- **Filled space.** A reviewer with no serious issues tends to inflate nits to
  fill the review. When a reviewer's findings are all style and preference,
  the code is probably fine. Say so.
- **Hypothetical versus actual.** "What if this is null?" is a finding only if
  a caller can pass null. Trace the call site. When the input is validated
  upstream or the types prevent it, dismiss the finding.
- **Premature abstraction.** A suggestion to extract, generalize, or add an
  interface earns its place only when the code must change in a second way.
- **"I would have done it differently."** A preference is not a defect unless
  the reviewer shows a concrete problem with the current approach.
- **Missing context.** Findings about code the change didn't touch, patterns
  consistent with the rest of the codebase, or remedies that conflict with
  known constraints come from limited information. Dismiss them, and say why.

## When reviewers are right

Don't dismiss a finding because it is uncomfortable. Weight it up when two
reviewers raised it independently, when it names a concrete execution path,
or when it exposes a gap in your own model of the code. Security and
correctness findings deserve extra scrutiny even from a single reviewer.

## Buckets

Sort every finding into one bucket, with a one-line reason and the reviewers
that raised it:

- **Act on.** Real issues of correctness, security, or maintainability that
  would block the change. These are the required changes.
- **Consider.** Legitimate points whose cost-benefit is unclear right now.
- **Noted.** Valid but not actionable at this stage.
- **Dismissed.** Wrong, nitpicky, or missing context.

If the Act on list has more than about five items, filter harder. Keep the
Dismissed list in the report: it lets the user override your judgment where
they disagree.
