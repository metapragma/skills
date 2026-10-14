### Forensics

**You own the diagnosis.** The deliverable is a cited diagnosis of a runtime
symptom, not a fix: a leak, a CPU spin, a stall, a slow query, a crash with no
reproduction. Hand the fix to [Bug fix](bug-fix.md) or [Perf](perf.md) once
the cause is known.

1. Get the evidence. Pick the branch that matches what you have:
   - **Live process:** capture the signal from the running system: a CPU
     profile for a spin, a heap snapshot for a leak, a trace or a slow-query
     log for a stall. Use the running-system recipe of
     [verification](../../verification/SKILL.md) to start an instance you own.
   - **Captured artifact:** someone already captured a profile, trace, dump,
     or log. Treat it as fixed data: read it, don't rerun it.

   Done when you hold a real artifact, not a theory.
2. Make it queryable. Load the artifact with the right tool for its format, or
   convert it into a form you can query (for example, one row per sample or
   frame in SQLite). Parse large artifacts in a delegate and keep only the
   reduced finding here, per [guard-the-context-window](../principles/guard-the-context-window.md).
3. Narrow to the cause: the frames that hold the most time and the path to
   them; for a leak, the retention chain from the leaked object to a root; for
   a stall, the blocked thread or connection and what it waits on.
4. Attribute it to source: the file, symbol, and line that allocates,
   schedules, or blocks. A frame with no source mapping is not yet a diagnosis.
   Resolve the symbols, or say the artifact doesn't carry them.
5. Confirm the mechanism. For a live process, add targeted instrumentation and
   watch the prediction hold. For an artifact, compare it with a paired
   before-and-after capture when one exists. Without either, report the
   finding as the strongest hypothesis the evidence supports.

**Reply:** the evidence and its format, the reduced finding, the source
location, how the mechanism was confirmed (or that it wasn't), and the artifact
paths.
