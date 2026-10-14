### Bug fix

**You own the fix. Every shipped line traces to runtime evidence.** A change
that "might help" is a hypothesis, not a fix, and it does not ship. When
evidence refutes a hypothesis, revert what it motivated.

1. Reproduce the bug yourself on the surface where it was reported. Build the
   feedback loop with [diagnosing-bugs](../../diagnosing-bugs/SKILL.md)
   (Phase 1), and use the project config of
   [verification](../../verification/SKILL.md) to run the system. Ask the user
   to reproduce only after you have driven the surface as far as it goes, and
   name the specific reason you can't reach the bug. Done when one command goes
   red on this bug.
2. Narrow the cause with the hypothesis and instrumentation phases of
   diagnosing-bugs. Seed the hypotheses with [how](../../how/SKILL.md) for the
   subsystem and [why](../../why/SKILL.md) for its regression history. When
   two fixes that share one premise have failed, apply
   [attack-the-premise](../principles/attack-the-premise.md). Done when
   runtime evidence confirms the mechanism.
3. Plan the smallest fix the evidence justifies, and name its data shape. When
   the fix crosses a function boundary, sketch it first with
   [codebase-design](../../codebase-design/SKETCH-FIRST.md).
4. Write the regression check before the fix, following the red, green, and
   refactor loop of [tdd](../../tdd/SKILL.md). The seam is the one the step 1
   loop already reached, so it needs no separate confirmation from the user.
   When a new test is impractical (it would need broad harness setup, brittle
   mocks, or production-only state), keep the step 1 command as the
   regression check and say so.
5. Fix the bug. Run the check until it passes, then run
   [verification](../../verification/SKILL.md) on the same surface. The
   original repro must pass. An inconclusive run, or a run on a different
   surface, is not a pass.
6. Run [code-review](../../code-review/SKILL.md) on the complete working
   candidate, with the bug report as the spec. Finish Phase 6 of
   diagnosing-bugs, including the removal of tagged debug logs.
7. With the user's go-ahead, run [Committing](committing.md). The failing
   check lands before the fix.

**Reply:** what was broken, the root cause, the fix, and how you verified it,
with the failing and then passing output pasted verbatim.
