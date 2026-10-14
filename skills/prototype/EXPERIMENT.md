# Behavioral Experiment

Answer a narrow observable question with the smallest executable check. Use this
for actual behavior, output, ordering, or timing, not an interactive state-model
demo or a decision only the user can make.

## Define the Question

State the uncertainty and the observation that would settle it. Inspect existing
code, documentation, and checks first; they may already provide sufficient
evidence. For example, checking whether a parser accepts escaped quotes needs
representative inputs and actual outputs. Deciding whether it should accept them
needs a requirement, not just a successful run.

Choose inputs or conditions that distinguish the plausible answers. Record what
is controlled and what the check will not establish. Keep the experiment within
the user's requested scope; additional dependencies, access, or consequential
operations need appropriate approval.

## Run the Smallest Check

Use the project's existing runtime, executable, public API, or test harness.
Exercise the code and dependency versions actually in question, not a handwritten
look-alike. Record the checkout revision and relevant pending changes; an answer
about an unknown or different build must remain qualified.

When a new script is useful, keep it in an isolated scratch location. Use
disposable fixtures and owned processes. Keep secrets and unrelated private data
out of output. Cleanup removes only owned state and leaves the script and relevant
evidence available; no product edits or implementation changes are implied.

Print observable inputs, outputs, and errors, or use a focused assertion whose
failure identifies the tested condition. A script finishing successfully is not
enough if it never exercised the relevant path. For asynchronous behavior, wait
for the actual completion signal rather than an arbitrary delay.

For timing, state the measured operation, workload, environment, and repetitions.
Confirm the intended work completed correctly inside the timed interval; record
errors, timeouts, cache effects, and skipped work so less work cannot masquerade
as a speedup. Compare equivalent inputs, configuration, load, and relevant warm-up
conditions. Keep the sample count and spread with the result, and repeat enough
to assess variability for the decision; if the gap cannot be distinguished from
noise, report it as inconclusive rather than a reliable speedup.

Separate the measured difference from its cause. Use profiles or counters when
claiming a limiting resource or code path, and check whether the harness itself
limits the result. If the cause remains unknown, say so. A faster isolated step
does not establish an end-to-end improvement. Use an existing measurement harness
for broader performance decisions rather than stretching a small experiment
into a benchmark.

## Interpret and Report

Distinguish observed results from their explanation. Describe what happened
under the tested conditions, then what it supports and what remains uncertain.
If the check cannot distinguish the alternatives, revise the observation method
or report the result as inconclusive; do not choose the preferred answer anyway.

Return the question, exact command and working directory, target version,
representative results, artifact paths, conclusion, and limitations. Keep output
proportionate to the question. Propose the next implementation step when useful,
but do not promote the script to production or apply that step without scope
and authorization.
