### Feature

**You own the design.** Plan it, delegate where it helps, review every diff,
and verify the result.

1. Settle the behavior and how you'll check it. When the request leaves real
   decisions open, run [grilling](../../grilling/SKILL.md), and record agreed
   terms and decisions with [domain-modeling](../../domain-modeling/SKILL.md)
   when the repository keeps domain docs. Skip this when the user supplied a
   checkable spec, and say so.
2. Run [how](../../how/SKILL.md) over the affected subsystem.
3. When a question needs a runnable answer (a state model, a UI, a timing),
   run the [Prototype](prototype.md) playbook and bring its answer back here.
4. Name the data shape and the structure that organizes it, per
   [model-the-domain](../principles/model-the-domain.md). When the code spans
   more than one function, sketch it with
   [codebase-design](../../codebase-design/SKETCH-FIRST.md), designing it twice
   when the shape has no precedent.
5. Write the throughput checkpoint as four todo items. Keep an item that does
   not apply, marked `n/a: <reason>`.
   - **Blocking first steps.** What must land before anything can run in
     parallel.
   - **Independent workstreams.** Disjoint files, services, or layers.
   - **Shared mutable state.** Split it first, per
     [separate-before-serializing-shared-state](../principles/separate-before-serializing-shared-state.md).
   - **Smallest safe decomposition.** When one worker is best, say why.
6. Build it with [implement](../../implement/SKILL.md), which runs tdd and
   code-review. Delegated edits follow the Delegation rules of
   [pragma-mode](../SKILL.md).
7. Run [verification](../../verification/SKILL.md) on every surface the change
   touches.
8. With the user's go-ahead, run [Committing](committing.md).

When the work turns out to need more than one session, switch to
[Feature, multi-session](feature-large.md) and keep what you settled.

**Reply:** what you built and for whom, what you chose and why (a table for
design alternatives), the throughput checkpoint, and the open decisions.
