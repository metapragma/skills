### Hillclimb

**You own the metric and the integrity of the experiment.** This is sustained,
iterative improvement of one measurable thing against a target: latency,
throughput, memory, build time, flake rate, or an eval pass rate. A one-off fix
is Perf or Bug fix. The core discipline: one change, one measurement, keep or
revert. Never stack untested changes, and never claim a win from reading code.

1. Ground the workload with [how](../../how/SKILL.md). Name the workload
   dimensions that can move the result (data size, history, state,
   concurrency) and pick a case that reproduces the user's complaint. When no
   case reproduces it, fix the repro first. Fix one metric, the direction that
   counts as better, and a stop rule that pairs a target with a minimum number
   of attempts, such as "50% better than baseline and at least 10 attempts".
   Use the user's numbers when given; otherwise agree them.
2. Build the measurement harness and prove it is sensitive: contrasting
   workloads must separate as expected (see [build-the-lever](../principles/build-the-lever.md)).
   Vet it with [benchmark-checklist](../../benchmark-checklist/SKILL.md), make
   it print its error count and a count of the work done, then freeze it. Record
   the baseline and a green run of the regression checks before any change.
3. Open a [decision log](../references/decision-log.md) with one row per
   attempt: the hypothesis, the change, before, after, the regression checks,
   and kept or reverted. Read it before each attempt.
4. Ground each hypothesis in a specific mechanism ("move X off the startup path
   because it blocks the first request"), not "try caching something". For a
   speed metric, order hypotheses by the performance mantras in [Perf](perf.md).
5. Loop, one hypothesis per iteration:
   - Make the change, or give it to a delegate with a tight brief and review
     the diff. Independent hypotheses can run in parallel, each in its own
     worktree.
   - Measure with the frozen harness and run the regression checks.
   - Keep the change only when the metric moves past the noise and the checks
     stay green. Otherwise revert it completely.
   - Log the row either way. When the user has approved commits for this run,
     commit each kept change separately, staging only its files; otherwise keep
     each kept change as its own patch.
6. Push past the first plateau. After several rejections in a row, change the
   category of hypothesis, combine near-misses, reread the source, or try
   something more radical. Correctness and simplicity outrank the number:
   revert a win that breaks behavior, and keep a simplification that holds the
   number.
7. Stop when the stop rule is met, or when the remaining ideas cost more than
   they could gain. Never relax the stop rule to meet it. When you're stuck,
   say so.
8. Run [code-review](../../code-review/SKILL.md) on the kept changes. With the
   user's go-ahead, run [Committing](committing.md) with the kept changes in
   the order they landed.

**Reply:** the metric and target, baseline to final with the percent change,
attempts kept versus reverted, each kept change in one line, the decision log
path, and the next idea you'd try.
