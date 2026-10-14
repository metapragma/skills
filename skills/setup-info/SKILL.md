---
name: setup-info
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Setup Info

You don't remember every skill, so ask.

This router recommends the next step. It does not run setup, publish work, or
launch other skills merely by being read. Honor the user's scope and
authorization. Read `docs/agents/domain.md` when domain-document routing
matters; otherwise inspect existing project instructions and domain documents.

## Start with pragma mode

For most engineering work, recommend **`/pragma-mode <goal>`**. It matches the
task to a playbook, copies the playbook's steps into the todo list, and runs
the skills below as those steps, under shared house rules and principles. Its
routes table, in [pragma-mode](../pragma-mode/SKILL.md), is the single list of
playbooks: investigation, bug fix, feature, multi-session feature,
refactoring, perf, hillclimb, forensics, prototype, skill change, pickup and
pause, and committing.

A good prompt carries the goal and a check that can pass or fail ("repro
first, then fix; done when the 60k-row export keeps every row"). The user
doesn't need to name skills; the playbook sequences them.

## Call a skill directly

Recommend a skill by name when the user wants one step, not a whole playbook,
or when the work fits none of the playbooks.

**Building blocks the playbooks use**

- **`/grilling`**: interview the user to sharpen a plan, design, or idea. In a
  working directory, record the agreed terms and decisions with
  `/domain-modeling` as you go.
- **`/how`**: explain how a subsystem works, as a walkthrough, a map of
  modules and callers, or a short post.
- **`/why`**: recover the historical rationale behind code or a decision,
  separating documented intent from inference. Read-only.
- **`/prototype`**: throwaway code that answers one design or behavior
  question.
- **`/to-spec`** and **`/to-tickets`**: turn a settled thread into a spec, then
  into tracer-bullet tickets with blocking edges. Tickets these produce are
  already agent-ready; don't triage them.
- **`/implement`**: build from a spec or tickets; it drives `/tdd` and
  `/code-review`.
- **`/tdd`**: red, green, refactor at agreed seams.
- **`/code-review`**: review a branch, commit, staged candidate, or working
  changes. Read-only unless fixes are requested.
- **`/verification`**: prove a change with the project's real checks, or set
  up and audit those checks.
- **`/diagnosing-bugs`**: the hard-bug loop. It builds a feedback loop that
  goes red on the bug before it theorizes.
- **`/benchmark-checklist`**: vet a measured number before reporting it.
- **`/blast-radius`**: find what a change breaks beyond its diff, and prove
  the fact it is safe because of.
- **`/handoff`**: a resumable summary for another session, directory, or
  person.

**On-ramps that feed the playbooks**

- **`/triage`**: move incoming issues and external pull requests, the ones you
  didn't create, through triage roles into agent-ready briefs.
- **`/wayfinder`**: chart a huge, foggy effort as decision tickets until the
  way is clear. When the map clears, it hands off to `/to-spec`, not straight
  to implementation, unless the effort turned out small.

**Design and contracts**

- **`/codebase-design`**: the deep-module vocabulary, plus references for
  designing an interface twice, sketching a shape first, and screening it for
  red flags.
- **`/domain-modeling`**: sharpen the project's domain language, the glossary,
  and its ADRs.
- **`/challenge-the-design`**: re-evaluate a proposal from the codebase-wide,
  long-term view before implementation.
- **`/api-and-interface-design`**: define or review consumer-facing contracts.
- **`/improve-codebase-architecture`**: survey for deepening opportunities in
  a spare moment; pick one to start a feature from.

**Writing and explaining**

- **`/technical-writing`**: human-facing docs for their audience and purpose.
- **`/writing-for-agents`**: skills, `AGENTS.md`, and other agent-facing docs.
- **`/frontend-integration-handoff`**: document backend behavior for frontend
  integration.
- **`/show-me`**: a visual explanation: diagrams, code sketches, or a focused
  HTML page.
- **`/wait-what`**: re-pitch a message that didn't land, in plain words.
- **`/teach`** and **`/drill`**: learn a concept over several sessions, or
  reason through an idea with concrete examples.

**Other standalone skills**

- **`/research`**: a background investigation against primary sources that
  leaves a cited Markdown file.
- **`/to-questionnaire`**: a questionnaire for someone else when the missing
  answer lives in their head.
- **`/wizard`**: an interactive script for steps only a human can perform.
- **`/retro`**: an evidence-backed session retrospective; recommendations
  first.
- **`/skill-doctor`**: audit skills across local sessions and propose
  evidence-backed changes.

**Staged, not installed:** `deslop`, `test-audit`, and `quality-gates`. They
are trial candidates, not callable steps.

## Phase boundaries

When a chunk of work ends, choose between continuing, a fresh session, a
handoff, a subagent, or the runtime's own compaction. Read
[PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) when choosing how to continue or
transfer work. Prefer a completed boundary, but preserve partial state when an
interruption is unavoidable.

## Setup

**`/setup`** configures the issue tracker, triage labels, and doc layout that
the tracker-based skills assume. Recommend it when that configuration is
missing; valid existing configuration needs no repeat setup. Direct testing or
review with enough task context need not wait for it. Setup does not authorize
later external actions.
