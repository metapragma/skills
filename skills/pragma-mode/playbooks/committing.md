### Committing

**You own what gets recorded.** Run this playbook only with the user's
go-ahead for the commit or pull request in question.

1. Commit only task-owned changes, staged by explicit path. Leave unrelated
   work untouched.
2. Order small commits so the history reads as an argument: the failing test
   before the fix, the subtraction before the reshape, the scaffold before the
   feature. See [sequence-verifiable-units](../principles/sequence-verifiable-units.md).
   The committed content must match what [code-review](../../code-review/SKILL.md)
   reviewed; review again after any later edit.
3. Follow the repository's commit-message convention from `git log`. With no
   clear convention, use Conventional Commits, `type(scope): subject`.
4. Write commit bodies and pull request descriptions with
   [technical-writing](../../technical-writing/SKILL.md). A pull request body
   has these sections, each one to three short lines, and drops any section
   with nothing to say:
   - **Why.** The problem and the approach.
   - **What changed.** Name a symbol or path only when it carries the change.
   - **Scope.** What this covers and what it deliberately leaves out.
   - **Tradeoffs.** Rejected alternatives a reviewer would ask about.
   - **Blast radius.** Who or what the change touches, and why that is safe.
   - **Verification.** Each real check that ran, with its outcome.
5. Push and open a pull request only when the user asked for it. Use the
   harness's pull request tool when it has one, or the repository's forge CLI.

**Reply:** the commits made, by subject; the pull request link, if one was
opened; and anything left uncommitted.
