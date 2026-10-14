---
name: deslop
description: "Clean unnecessary comments, speculative code, type shortcuts, and style drift from a requested diff without changing behavior. Use for a deslop or diff-cleanup pass before review."
license: MIT
metadata:
  source: "https://github.com/openclaw/openclaw/tree/91264b958cf11cda9b166fb134f22ca1c796c14c/.agents/skills/deslop"
---

# Deslop

Clean only the requested diff. Preserve behavior and unrelated work.
Review-only requests produce findings without edits.

## Scope

Use the user's comparison target. For a branch review, compare against the
merge base with its actual target branch; do not assume `main` or a particular
remote. For uncommitted work, inspect staged and unstaged changes plus relevant
untracked files. If the target is ambiguous, ask before editing.

Read applicable repository instructions and surrounding code to establish the
local conventions. Never turn this into a repository-wide cleanup.
Exclude generated and vendored files unless the user explicitly includes them.

## Checklist

Inspect changed hunks for:

- Comments that narrate syntax or merely restate the code rather than explain
  intent or a non-obvious constraint.
- Defensive checks or exception handlers that protect only imagined states or
  conflict with the surrounding module's error-handling policy.
- Casts or equivalent language-specific shortcuts that hide type errors rather
  than establish correctness, such as `as any` or `as unknown as T`.
- Intermediate variables or one-use helpers that add no domain meaning,
  duplication reduction, or control-flow clarity.
- Compatibility shims, aliases, retries, and fallbacks without an identified
  supported contract. Their absence of documentation is a question to
  investigate, not proof that they are unnecessary.
- Naming, control flow, imports, and formatting that conflict with local style.

Use the project's formatter for formatting changes, scoped to the relevant
files; avoid manual style churn or formatting unrelated code.

When cleanup edits are requested, fix only trivial, demonstrably behavior-neutral
findings. Removing a guard,
handler, retry, or fallback can change behavior; leave uncertain or functional
changes in place and report them for review. Preserve useful explanations,
security checks, and legitimate compatibility behavior.

Run the repository's relevant checks for any edits and inspect the final diff
for unintended changes. Report what changed, what was checked, and any items
left for review in a few sentences. Cleanup does not replace correctness or
safety review, and does not authorize commits, pushes, or publication.
