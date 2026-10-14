---
name: technical-writing
description: "Write or revise human-facing technical documentation for its audience and purpose, preserving factual accuracy and useful detail."
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/technical-writing"
---

# Technical Writing

Write technical material a reader can understand and use without reconstructing
missing steps. Apply to requested documentation, RFCs, READMEs, PR descriptions,
or commit messages. Preserve the project's format, terminology, and ownership;
writing a draft does not authorize publication, a commit, or product changes.

For agent instructions, use the project's agent-writing conventions instead.
For product UI text, follow its copy guidelines. This skill is not a mandatory
rewrite of every conversational response.

## Establish the Reader and Purpose

Identify what the reader already knows and what the document should let them
do or understand. Infer this from the request and existing material; clarify
only choices that would materially change the document. Read the relevant
source, configuration, requirements, and existing documentation before making
project-specific claims. Preserve settled requirements and necessary caveats.

Choose a dominant purpose, using the Diataxis distinction:

- **Tutorial:** help a learner accomplish a concrete task. Give a safe starting
  state, manageable steps, observable results, and recovery from likely failures.
  Introduce concepts where the learner needs them.
- **How-to:** help a competent reader reach a named goal. Give prerequisites,
  ordered actions, consequential branches, verification, and cleanup or rollback
  when relevant. Link background rather than interrupting the procedure with it.
- **Reference:** make facts easy to find. Organize around the API, command,
  configuration, or other subject; state options, defaults, limits, errors, and
  supported versions. Derive from authoritative definitions where practical.
- **Explanation:** build understanding of a bounded topic. Show the mechanism,
  motivations, constraints, alternatives, and tradeoffs through a concrete case.
  Distinguish documented rationale from interpretation.

A README or RFC can serve several purposes. Separate them into navigable sections
or linked documents when that improves use; do not split a useful document merely
to enforce one mode. PR descriptions and commit messages are briefings: what
changed, why, and material verification or remaining risk, not complete manuals.

## Make the Meaning Clear

- Name who does what to which thing. Prefer active voice when it identifies the
  actor; keep passive voice when the actor is irrelevant or unknown.
- Use real symbol, command, flag, file, and domain names consistently. Define
  unfamiliar terms at first useful mention; avoid synonym cycling and invented
  jargon. Preserve precision rather than replacing every technical word.
- Put prerequisites and warnings before the actions they govern. State the
  common path first, then exceptions where readers need to decide between them.
- Use direct commands for instructions. Pair significant steps with expected
  output or an observable success condition, not merely "it should work."
- Keep a sentence's main relationship easy to follow. Split overloaded clauses,
  clarify pronouns, and keep modifiers such as "only" next to what they qualify.
  Retain articles, conditions, and verbs that prevent ambiguity.
- Cut filler and use ordinary words where they say the same thing. Keep necessary
  uncertainty, exceptions, and causal connections; brevity is not a word quota.
- Vary sentence length naturally. Use an analogy or diagram when it clarifies
  the actual subject, and explain its limits rather than treating it as evidence.

## Organize for the Task

Use headings that help the reader locate a task, fact, or question. Number ordered
steps; use bullets for peer items and tables for genuine comparisons or lookup.
Match the repository's heading, punctuation, and code-formatting conventions
rather than imposing universal sentence lengths, indentation, or banned words.

Link with descriptive text to the source that owns the detail. Keep the immediate
prerequisites and warnings beside their step. Avoid duplicating configuration,
thresholds, or generated inventories; link to their authority when sufficient.
Include detailed evidence in a supporting artifact when it would overwhelm a
briefing, without hiding important failures or qualifications.

## Verify Before Delivery

Check examples, commands, defaults, versions, paths, and links against their
sources. Run safe executable examples when feasible and authorized. For commands
with consequential effects, use isolated fixtures or report that execution was
not verified; writing a procedure does not authorize running it in production.
Keep secrets out of examples and evidence.

Separate current behavior, planned behavior, requirements, and opinions. Do not
remove uncertainty from reference material merely to make it sound authoritative.
Use explicit placeholder values only when substitution is intentional and explain
what the reader must supply. Label invented examples as illustrative.

For a revision, check that the new text preserves meaning, warnings, supported
cases, and the user's requested scope. Avoid unrelated prose churn. Deliver the
requested draft or file edits, with a brief note of material factual gaps or
unverified commands; do not append a report about every stylistic choice.
