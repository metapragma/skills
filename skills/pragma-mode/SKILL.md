---
name: pragma-mode
description: Run a task through a matched playbook, with house rules and engineering principles applied at every step.
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/poteto-mode"
---

# Pragma mode

Match the task to one playbook, run its steps in order, and hold every step to
the house rules and principles below.

## Start

1. **Match.** Pick one route from the table below. "New task" from the user
   means match again instead of continuing the previous playbook.
2. **Copy the steps.** Open the playbook and copy its numbered steps, word for
   word, into the todo list before any task-specific items. A step you choose
   not to do stays in the list as `skip: <reason>`.
3. **Run the steps.** A step that names a skill means: read that skill's
   `SKILL.md` at the given path, relative to the playbook file, and follow it
   for that step. The user invoked this mode, which covers reading and running
   every skill a step names.
4. **Reply** with the content the playbook's **Reply** line names, written per
   [Writing the reply](#writing-the-reply).

Done when every copied step is checked off or carries a skip reason, and the
reply covers each item its **Reply** line names.

## Routes

| The request is | Route |
|---|---|
| A read-only question: how does X work, why is Y this way, are we sure about Z, should we do X or Y | [Investigation](playbooks/investigation.md) |
| A reported defect to reproduce, root-cause, and fix | [Bug fix](playbooks/bug-fix.md) |
| New or changed behavior that fits in one session | [Feature](playbooks/feature.md) |
| New or changed behavior that spans sessions | [Feature, multi-session](playbooks/feature-large.md) |
| Change structure without changing behavior | [Refactoring](playbooks/refactoring.md) |
| A measured slowness to fix | [Perf](playbooks/perf.md) |
| Sustained improvement of one metric against a target | [Hillclimb](playbooks/hillclimb.md) |
| Diagnose a runtime symptom (leak, spin, stall, crash) from a live process or a captured artifact | [Forensics](playbooks/forensics.md) |
| A throwaway sketch to settle a design or behavior question | [Prototype](playbooks/prototype.md) |
| Write or edit a skill, playbook, or agent instruction file | [Skill change](playbooks/skill-change.md) |
| Pause work cleanly, or resume a previous session's work | [Pickup and pause](playbooks/pickup-and-pause.md) |
| What a change could break beyond its diff | the [blast-radius](../blast-radius/SKILL.md) skill |
| Commit the work, or open a pull request | [Committing](playbooks/committing.md) |
| Incoming issues or external pull requests to sort | the [triage](../triage/SKILL.md) skill |
| A foggy effort where the way to the goal isn't visible yet | the [wayfinder](../wayfinder/SKILL.md) skill |
| Nothing above fits | [No playbook fits](#no-playbook-fits) |

## House rules

- **Scope and authorization.** The user's request sets the scope. Edits inside
  that scope proceed. Commits, pushes, pull requests, tracker writes, messages,
  deployments, and any irreversible action wait for the user's explicit
  go-ahead in this conversation. A playbook step never grants it.
- **Facts before questions.** Before you ask the user something, decide whether
  running something could answer it: behavior, output, timing, layout, or
  whether a check tells two options apart. If so, run it, using the
  [prototype](../prototype/SKILL.md) skill when the answer needs a sketch. Ask
  only about product or preference calls that no experiment can settle, and
  give options with your recommendation.
- **Data shape first.** Before writing logic, name the data shape and the
  structure that organizes it, per [model-the-domain](principles/model-the-domain.md).
- **Proof on the real artifact.** Verify through the
  [verification](../verification/SKILL.md) skill before you call work done. A
  passing self-report, a compile, or an inconclusive run is not proof.
- **Candor.** When asked whether to do something, give your real judgment.
  "This doesn't earn its place" is a valid answer.
- **Broken skills.** When a skill misleads you mid-task, finish the task in the
  most visible correct way, then name the defect and the proposed fix in the
  reply as separate work.

## Delegation

Delegate when the harness offers subagents and the work is bounded: bulk
reading, independent slices, a mechanical edit with an exact brief, or an
independent review. You own the result either way. Read every delegated diff
and write your own summary.

- **Brief.** Each brief stands alone. It opens with "Read `<absolute path to
  this SKILL.md>` first and follow its house rules." It then names the goal,
  the files in scope, the data shape, the success check, and what to report.
- **Kind of work, not a model.** Describe the work: "a mechanical edit with an
  exact brief", "needs your strongest judgment", or "an independent review".
  The harness and the user's settings choose the model.
- **Fresh agent per round.** A fix round, retry, or follow-up goes to a fresh
  subagent with the consolidated brief: the original brief, every later
  directive, and the previous report. Reuse an agent only for state that is
  costly to move, such as its uncommitted checkout or a running process.
- **Independence.** An independent review comes from a fresh context that has
  not seen the author's reasoning. When the reviewer is the same model family
  as the author, say so in the reply.

## Writing the reply

- Lead with what changes for the consumer of the work: the end user, the
  caller of the code, or the next maintainer. Then give the details.
- Label every claim in the same sentence: **measured** (name the command or
  artifact), **inferred** (name the evidence), or **guess**.
- Run every check you can yourself. Hand the user only checks that need them.
- Link only artifacts you produced or read in this session.
- Keep every item the playbook's **Reply** line names. Short sentences are fine;
  dropped content is not.
- Name each principle that changed a decision, and the decision it changed.
  Cite only principles whose file you read in this session.

## Principles

Read a principle's file before you apply it.

**Core**

- [laziness-protocol](principles/laziness-protocol.md). Sizing a diff, or tempted to add layers or thread a new signal. Prefer deletion and the smallest change that solves the problem.
- [foundational-thinking](principles/foundational-thinking.md). Before writing logic: core types, scaffold-versus-feature order, what concurrent actors share.
- [redesign-from-first-principles](principles/redesign-from-first-principles.md). Integrating a new requirement. Redesign as if it had been there from the start.
- [attack-the-premise](principles/attack-the-premise.md). Two or more fixes that share one premise failed the same check. Question the premise before the next fix.
- [subtract-before-you-add](principles/subtract-before-you-add.md). Sequencing an addition, refactor, or rewrite. Remove dead weight first.
- [minimize-reader-load](principles/minimize-reader-load.md). Code that is hard to trace. Count layers and hidden state; collapse one-caller wrappers.
- [outcome-oriented-execution](principles/outcome-oriented-execution.md). A planned migration with declared phase boundaries. Converge on the target instead of keeping throwaway compatibility.
- [experience-first](principles/experience-first.md). Scope or UX tradeoffs. Choose the consumer's experience over implementation convenience.
- [exhaust-the-design-space](principles/exhaust-the-design-space.md). A decision with no precedent. Build two or three real alternatives before committing.
- [build-the-lever](principles/build-the-lever.md). Any non-trivial work. Build the script or codemod that does or proves it.

**Architecture**

- [model-the-domain](principles/model-the-domain.md). Stateful or branching logic. Encode the domain in a structure, not scattered conditionals.
- [boundary-discipline](principles/boundary-discipline.md). Validation, error handling, framework adapters. Guard at boundaries; keep business logic pure.
- [type-system-discipline](principles/type-system-discipline.md). Designing types or signatures. Make illegal states unrepresentable; parse external data at boundaries.
- [make-operations-idempotent](principles/make-operations-idempotent.md). Commands, jobs, or loops that run amid crashes and retries. Converge to the same end state.
- [migrate-callers-then-delete-legacy-apis](principles/migrate-callers-then-delete-legacy-apis.md). A new internal API while old callers exist. Migrate and delete in one pass; consumer-facing contracts are excluded.
- [separate-before-serializing-shared-state](principles/separate-before-serializing-shared-state.md). Concurrent actors might write the same file, key, branch, or row. Remove the sharing first.

**Verification**

- [prove-it-works](principles/prove-it-works.md). Before declaring done. Check the real artifact, not a proxy.
- [fix-root-causes](principles/fix-root-causes.md). Debugging. Reproduce first and ask why until you reach the cause.
- [sequence-verifiable-units](principles/sequence-verifiable-units.md). Multi-step work and commit order. Each unit ends in a check before the next starts.
- [test-behavior-not-implementation](principles/test-behavior-not-implementation.md). Writing, changing, or keeping a test. It must fail if every imported function returned `undefined`.
- [explain-the-number](principles/explain-the-number.md). Before trusting or reporting a measured number. Find its limiter and rule out what else it measured.

**Delegation and meta**

- [guard-the-context-window](principles/guard-the-context-window.md). Large outputs, long files, fan-out. Keep summaries in the main thread.
- [encode-lessons-in-structure](principles/encode-lessons-in-structure.md). You are writing the same instruction a second time. Make it a check, type, or script instead.

Long or multi-step runs keep a [decision log](references/decision-log.md).

## No playbook fits

Design a short playbook for this task before writing code:

1. **Frame.** State done as a check that can pass or fail, the scope with its
   rough size, and how much rigor the risk calls for. Present this to the user
   before a long run.
2. **Design.** Break the work into units that each land on their own, riskiest
   unknown first, with the verification harness and its baseline built before
   the change.
3. **Run.** Treat each unit as an experiment: state the hypothesis, make the
   smallest change, check it on the real artifact, keep it or revert it. A
   verdict is verified, not verified, or inconclusive; inconclusive is not a
   pass.
4. **Hand back.** Check the whole against the step 1 check, and reply with the
   playbook you designed, what is verified, and what remains open.
