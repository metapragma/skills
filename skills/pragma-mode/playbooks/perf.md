### Perf

**You own the measurement story.** Every fix ties to a measurement. Reading the
source is not measuring.

1. Capture a baseline on the surface where the slowness was reported, through
   the running-system recipe of [verification](../../verification/SKILL.md) and
   the perf branch of [diagnosing-bugs](../../diagnosing-bugs/SKILL.md). Vet
   the baseline, and every later number, with
   [benchmark-checklist](../../benchmark-checklist/SKILL.md).
2. Ground the hypotheses with [how](../../how/SKILL.md) and the profile.
   Generate fixes from the performance mantras, cheapest first, and stop at the
   first one that meets the target:
   1. Don't do it: stop work whose result nothing uses.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when nobody is waiting.
   6. Do it concurrently.
   7. Do it cheaper.
3. Plan the fix from the profile. When it spans more than one function, sketch
   it with [codebase-design](../../codebase-design/SKETCH-FIRST.md) first. Try
   one change at a time and measure each before the next, per
   [sequence-verifiable-units](../principles/sequence-verifiable-units.md).
4. Compare baseline and candidate under equivalent conditions. An
   inconclusive result, or a measurement on a different surface, is not a
   pass.
5. Run [verification](../../verification/SKILL.md) and
   [code-review](../../code-review/SKILL.md). With the user's go-ahead, run
   [Committing](committing.md), citing the primary number.

For sustained improvement against a target instead of a one-off fix, use
[Hillclimb](hillclimb.md).

**Reply:** the baseline number, the final number, the change with its run count
and range, the limiter, and the artifact paths.
