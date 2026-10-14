---
name: benchmark-checklist
description: Vet a performance measurement before you report or act on it. Use when you run a benchmark, or report a speedup or regression you measured.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/benchmark-checklist"
---

# Benchmark checklist

Use this when you produce a performance number: a before and after for a
change, a regression claim, a hillclimb harness, or a library or configuration
choice. Answer each question below with evidence from a run, not from a guess
about the code.

For a quick ballpark the user asked for, one run is enough. Still answer
questions 4 and 7, and say it was one run. Skip the rest unless that run looks
wrong. A choice between options is never a ballpark.

## Before you run anything

- Write down the claim you expect to make, in the words you would ship ("the
  export is 30% faster at p50 on the 60k-row dataset"). The questions test that
  sentence.
- Read the measurement script. Note what it times, what it counts, and what it
  ignores.
- Check the machine's load and core count. If it is busy, find out what is
  running. If you cannot stop it, alternate the sides so both see the same
  noise, and say so in the report.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you do not report,
   because profilers and tracers slow the work down. Use per-process CPU, a
   profiler for the runtime, I/O wait, and system-call counts; for a database,
   the query plan (`EXPLAIN ANALYZE`) and the statement statistics. Map the hot
   spot to source. Watch the load generator too: if it saturates first, you
   measured the load generator. If a change did not move the number, the
   limiter explains why, so find it before you call the change useless.
2. **Was it tuned?** Run every side the way production runs it: release
   builds, production flags and environment, batching and transaction settings,
   connection pools, caches as warm or cold as production sees them, and the
   same versions and data. If one side runs on defaults, you compared
   configurations, not implementations. A limiter that is a setting (a commit
   per row, a debug build, a missing index) means that side is untuned. Tune it
   and measure again before you pick a winner.
3. **Did it break limits?** Do the arithmetic. Compare bytes per second with
   disk and network bandwidth, and operations per second times the cost per
   operation with the cores available. Compare the time saved with the time the
   changed piece took: removing a piece that takes 10% of the run makes the run
   at most about 11% faster. A result past a limit means the run measured
   something other than the work, such as a cache, a no-op, or a bug.
4. **Did it error?** Count failures and non-success responses, and check that
   the outputs are correct, not just present. Rejections are often fast, and
   timeouts and retries are slow. If the script does not count errors, add the
   count.
5. **Does it reproduce?** Run each side at least 5 times, alternating the sides
   (A, B, A, B) so warmup, lazy initialization, caches, and drift don't favor
   one. Report the median and the range. A gap smaller than the run-to-run
   variation is no measurable difference. When the call is close, use a
   rank-sum test or the harness's own statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a
   user or client waits on, with realistic data sizes and concurrency. Report
   the micro result as a share of the whole.
7. **Did it even happen?** Confirm the work ran inside the timed region: the
   request reached the server, the rows were written, the bytes were read, and
   the code used the result. Lazy code and timeouts both produce numbers for
   work that never happened.

## Report

- Lead with the verdict: faster, slower, no measurable difference, or
  inconclusive.
- Give the number with its unit, the run count, the range, and the limiter. For
  example: "p50 41 ms → 33 ms, median of 7 runs per side, range 32 to 35 ms
  after, bound by JSON parsing on one core."
- The verdict is inconclusive when you claim a difference but cannot name the
  limiter, when a side ran untuned, or when you could not answer questions 4
  and 7. Name the gap.
- A pull request body carries one primary number. Put the runs, the range, and
  the limiter evidence in a linked artifact or notes file.
