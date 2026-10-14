# Procedure

Use `followed`, `violation`, `not_applicable`, or `insufficient_evidence`. Identify
the applicable user request and instruction version before judging behavior.
User instructions and runtime rules take precedence over skill guidance.

A current skill file cannot prove what a historical session required. A visible
read with its returned body, or a verified version linked to that session, can
establish the rule. If applicability or version is unavailable, leave that
portion unassessed. Use `not_applicable` when no procedural requirement applies.

Distinguish references, loading, and observed application. Do not judge a skill
audit, failed read, mention, or catalog listing as invocation. An explicit-only
skill needs the user's request or other established authorization. Its absence
from an unrelated session is not a violation or a coverage defect.

Cite the applicable rule and action for `followed` or `violation`. If the model
ignored a clear rule, record that observation without proposing repetition of
the same instruction as a fix. A proposal needs an actual instruction gap.
