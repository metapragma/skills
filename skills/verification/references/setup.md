# Setup Mode

Build the verification paths an agent needs in this codebase. Then prove the
paths work from an empty state. Reuse existing checks and conventions, and add
only what is missing.

Ask before any consequential step, such as:

- installing tools;
- pulling images;
- changing harness, CI, or repository settings;
- touching shared environments.

Setup authorizes building and proving the paths. It does not authorize product
fixes.

## 1. Find Surfaces

List what users and clients actually touch: a browser UI, an HTTP or RPC
service, a database, background work, a CLI, a library API, a mobile app, or
features backed by AI models. Then read the matching
[surfaces/](surfaces/) references. Read the project's instructions
(`AGENTS.md`, `CLAUDE.md`) and any testing or verification policy it already
has. That policy decides which evidence a change needs, so you don't have to
invent one.

Done when every surface is listed and has a source citation, for example a
route registry, a CLI entry point, or a schema.

## 2. Inventory

For each layer, record the existing commands. Note what actually executes and
what each command substitutes.

| Layer | Question |
| --- | --- |
| Runtime | Can an agent run the checks here? See [agent-runtime.md](agent-runtime.md) |
| Static | Build, type-check, lint, format |
| Focused | Fast tests on the changed scope |
| Suites | Required suites against real dependencies |
| Running system | Boot the real binary, use a real identity, drive journeys |
| Effects | Durable state, emitted work, files, and logs after a journey |
| Evidence | A record bound to the revision |
| Gate | What stops a merge when the evidence is missing |

Substitutions include stubbed auth, in-memory fakes, mocked providers, a
shared environment, and tests that skip when an environment variable is unset.
A check that skips silently counts as a gap, not as coverage.

Done when every layer either has a command with an observed result, or is
marked as a gap.

## 3. Rank Gaps

Rank gaps by the defects that actually escaped. Use these sources, best first:

1. output from `retro` or `skill-doctor` for this project, when it exists;
2. bug reports and issues;
3. incident notes;
4. `git log` messages for fixes.

Escapes usually gather at one boundary, often the running service. Close that
boundary first. Present the ranked list and get the user's selection before
you build.

## 4. Build

Build only the selected gaps. Use the project's language and runner.

### Commands

Use the existing task runner: make, just, Task, npm scripts, mise, or similar.
Add a runner only when none exists, and only with approval. Keep each target a
one-line call.

Put the logic in one small command-line tool written in the project's main
language, with a subcommand per command. Extend an existing verification tool if
the project has one. In that language the logic can be unit-tested, and it can do
the following without parsing text:

- read structured test output (`go test -json`, JUnit XML, or a reporter's JSON) to
  get exact counts of run, skipped, and cached tests;
- query the database through the project's own driver;
- build the JSON record.

Shell is fine for glue, such as calling `docker` or the stack's own CLI, but not for
parsing or JSON.

| Name | Contract |
| --- | --- |
| `doctor` | Read-only. Prints JSON that names each missing prerequisite, and exits non-zero when anything required is missing. Never pulls images and never skips health checks. |
| `up` / `down` | `up` starts an owned instance, writes its connection details (ports, URLs, token paths) to a state file, and returns only when the instance is usable. `down` removes only what that state file records. |
| `fast` | Checks the changed scope for the inner loop. Aim for about a minute. |
| `<surface>` | Checks one surface, for example `db`, `api`, or `browser`. |
| `verify` | The full required set: the merge gate. |
| `mutation` | Optional. Mutation testing scoped to changed files. |

Every command follows these rules:

- **Exit code.** The exit code is the verdict.
- **Output.** Stdout prints failures and a one-line summary.
- **Run directory.** Full logs and the evidence record go to
  `.verification/runs/<UTC timestamp>-<short revision>/`, which git ignores.
- **Empty runs.** A run that executes zero tests fails. When a command legitimately
  has nothing to check, for example `fast` with no changed code, it prints an
  explicit empty-scope marker, and the record keeps that marker as the reason.
- **Cached results.** A test runner that replays cached results executed nothing.
  The check fails.
- **Skips.** A required case that is skipped fails.

Before you rely on the new files, confirm git can track them. A local exclude,
such as `.git/info/exclude`, can hide them from `git status`. A tracked file must
never depend on a file that is hidden or untracked.

When the test runner already prepares a real dependency, for example by applying
migrations with project-specific patches, move that step into a script. The runner
and `up` then both call it, so the two paths can't drift apart.

### Running System

Make `up` reach a **usable** state from empty data:

- migrations applied;
- seed data loaded;
- a test identity authenticated;
- one authenticated request succeeding.

Prefer the production composition and the real identity provider running
locally over stubs. See [surfaces/identity.md](surfaces/identity.md). When an
irrelevant missing asset blocks startup, create it as scaffolding that names
itself, and remove it in `down`.

Make starting the application its own step, and let it take another build as an
argument. The proofs below then run a defective copy or a pre-fix revision
against the same stack and data.

### Project Config

Write `docs/agents/verification.md`. Keep it short. Cache only what the agent
can't find by looking: the commands are already listed in the runner. Then add
one line to `AGENTS.md` (or `CLAUDE.md`) that points to the config and to this
skill.

```markdown
# Verification

Surfaces: <list, with the reference each uses>
Runner: <task | make | npm ...>; commands: doctor, up, down, fast, verify, <surfaces>
Policy: <path to the project's risk-to-evidence policy, if any>

## Identities
<test users, roles, and how a token is minted locally; no secret values>

## Journeys
- <id>: <entry point> → <expected observable result and durable effect>

## Gotchas
<readiness traps, seed gaps, ports, sandbox needs, unsafe actions>
```

With more than about five journeys, move them to
`docs/agents/verification/<journey>.md`. Give each journey its entry points,
drive steps, expected results, effects to check, and gotchas. When seed data
lacks a precondition that a journey needs, the journey fails and the reason
goes in Gotchas. Keep the journey at full strength rather than weakening it to
pass.

## 5. Prove

Run the setup from a fresh state:

1. `doctor`
2. `up`
3. Drive one high-risk journey.
4. Observe its effects.
5. Write the evidence record.
6. `down`
7. Confirm that the evidence still exists.

Then show that the new paths catch defects:

- **Planted defect.** In an isolated copy, introduce one realistic defect, for
  example removing an access guard or dropping a required field. The relevant
  check must go red for that reason. A compile error or a missing service
  doesn't count.
- **Past escape.** When the project has one, replay it. The check must go red on
  the pre-fix revision and green on the fixed one.

If the proof ran in a stand-in for the real target, for example a local stack
in place of a remote one, list every setup step the stand-in performed that the
target won't. Those steps remain unverified.

Done when both proofs pass, or the report names each one that is blocked and
why. A setup that has never run end to end is a draft.

## 6. Propose the Gate

Use [enforcement.md](enforcement.md) to propose the smallest mechanism that
makes `not run` block the next step. Implement it only with approval.

## Report

Include:

- the config path;
- the commands added or reused;
- the inventory, with the remaining gaps;
- the proofs and their evidence paths;
- the cleanup outcome;
- the proposed gate.
