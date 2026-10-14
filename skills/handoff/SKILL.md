---
name: handoff
description: Summarize the current task, work state, and verification in a handoff document another agent can safely resume.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a compact handoff for a fresh agent to resume the requested work. If the
user specifies the next session's focus, tailor the handoff to it. Creating the
handoff does not authorize continuing implementation, committing, or messaging
another agent.

## Establish the state

Use the available conversation and current artifacts, not reconstructed memory.
For repository work, inspect the checkout path, branch or detached HEAD, HEAD
SHA, and working-tree status. Inspect relevant staged, unstaged, and untracked
changes enough to distinguish task work from unrelated edits. Leave them intact;
label uncertain ownership rather than guessing. For non-repository work, record
the relevant artifact or environment state instead.

A status listing locates changes but does not identify their contents. Bind
verification to the tested commit or known candidate when available; if dirty
content cannot be identified reliably, say it needs rechecking. Do not invent
missing command output, decisions, or conversation history.

## Write the handoff

Include the following, keeping each section short. Mark material unknowns;
omit sections that genuinely do not apply.

- **Objective and constraints:** the current request, scope exclusions, and what
  remains before completion. Use the latest user direction over superseded plans.
- **Decisions:** accepted choices and their reasons. Label proposals and
  assumptions separately; link specs, plans, ADRs, and issues instead of copying
  their contents. Preserve important rejected approaches and why they failed or
  were ruled out, not the full exploration transcript.
- **Work state:** completed versus pending work, checkout identity, relevant
  changed/untracked paths, and whether changes are committed. Identify unrelated
  work to preserve. Note any running process needed to resume, its purpose and
  known identifier, without assuming it will survive the session.
- **Verification:** exact commands, working directory, outcomes, and which
  candidate they apply to. Distinguish passed, failed, skipped, and not run;
  mention edits since the last check and known baseline failures. Link long logs
  when accessible rather than copying them wholesale.
- **Open questions and authorization:** blockers, risks, and outstanding approval
  requests. Record explicit user authorization with its scope and source when
  available; a proposed action is not approval. A handoff is a record, not an
  independent grant of permission or a substitute for runtime approval gates.
- **Next action:** the first concrete step and the artifacts needed for it.
  Include subsequent steps only when already agreed and useful.
- **Suggested skills:** relevant, available skills and why they fit the next
  action, or "None needed." Suggestions are not instructions to load everything.

Use absolute paths for local artifacts and URLs for remote ones. Flag temporary
or machine-local resources that may be unavailable in another environment.
Redact secrets and unnecessary personal information from commands, URLs, logs,
and examples; use explicit placeholders where needed.

## Include a resume checklist

Tell the receiving agent to:

1. Read applicable repository instructions and the linked task artifacts.
2. Verify the actual checkout and changed files against the recorded state.
   Re-read relevant source; treat the handoff as a potentially stale summary.
3. Recheck affected verification when the candidate changed, its identity is
   unknown, or the next step depends on an unverified result. Distinguish observed
   implementation from intended behavior; surface material conflicts.
4. Confirm that consequential actions remain within the user's authorization
   and current permissions. Ask when authorization is missing or ambiguous, then
   resume at the recorded next action rather than restarting completed work.

## Deliver

Save to a uniquely named Markdown file in the operating system's temporary
directory, unless the user requests another location. Keep session state out of
domain glossaries and permanent project instructions. Check that local artifact
links exist, flag unavailable references, and reread the handoff for secrets,
unsupported completion claims, and missing next steps. Return the absolute path
as a clickable link and note that the file is temporary. Do not claim this
changes or compacts the runtime's conversation history.
