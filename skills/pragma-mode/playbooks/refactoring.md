### Refactoring

**You own the contract. The structure changes; the behavior does not.** A
cleanup that reveals a missing feature or a real bug splits it out: the
structural change ships first against the pinned behavior, and the rest goes
to Feature or Bug fix. Large, cross-cutting restructuring uses
[No playbook fits](../SKILL.md#no-playbook-fits).

1. Learn the contract with [how](../../how/SKILL.md), then pin the behavior
   before any structure moves, following the Behavior-Preserving Changes
   section of [implement](../../implement/SKILL.md). Type checks and lint are
   not a pin.
2. Name the structure the code is missing, per
   [model-the-domain](../principles/model-the-domain.md). Boring code stays
   when its shape is already clear and local. The reshape must delete branches
   or invalid states, not add indirection.
3. Name the target shape: the modules, types, and call graph you'd build today
   (see [redesign-from-first-principles](../principles/redesign-from-first-principles.md)).
   When the target spans more than one function, sketch it with
   [codebase-design](../../codebase-design/SKETCH-FIRST.md) first.
4. Subtract before you add: delete dead code, collapse one-caller wrappers,
   and drop redundant validators and orphaned references before introducing the
   new shape (see [subtract-before-you-add](../principles/subtract-before-you-add.md)).
5. Move in small steps, each keeping the pin green. For an internal API
   reshape, migrate every caller and delete the old API in the same pass, per
   [migrate-callers-then-delete-legacy-apis](../principles/migrate-callers-then-delete-legacy-apis.md).
   Check each rename against the actual files; renames silently miss usages in
   strings, docs, and configuration. Mechanical edits can go to a delegate with
   an exact brief.
6. Prove the behavior is unchanged with [verification](../../verification/SKILL.md),
   replaying the step 1 pin against the final code.
7. Keep the change only if it lowers reader load somewhere, per
   [minimize-reader-load](../principles/minimize-reader-load.md). Otherwise
   revert it.
8. Run [code-review](../../code-review/SKILL.md). With the user's go-ahead, run
   [Committing](committing.md): the subtraction first, then the reshape.

**Reply:** the structure that changed, the pin you held it against, the
equivalence evidence, the reader-load change, and what shipped versus what you
reverted. No new behavior.
