# Background Work

Queues, workers, schedulers, webhooks, and retries. A request can succeed while
the work it started fails later.

## Checks

| Concern | Evidence |
| --- | --- |
| Handoff | The command enqueues work, and the real registered worker consumes it |
| Completion | The final durable effect appears. Observe it with bounded polling on a condition, not a fixed sleep |
| Duplicate delivery | Redelivering the same message produces no second effect |
| Stale input | Work that arrives after a lifecycle change is rejected or ignored as the contract says |
| Retry and terminal failure | Transient errors retry, and permanent errors land in a terminal state that is visible |
| Interruption | A worker killed mid-job, or a lease that expires, recovers without losing or duplicating work |
| Ordering and races | When two operations compete, test both completion orders. Show that the operations actually overlapped at the critical point, not merely that two goroutines or threads started |

## Practice

- Run workers inside the running system. Calling handlers directly skips the
  dispatch and registration wiring.
- Use fault injection at the boundary, for example a proxy that drops or delays
  responses, rather than editing the product code.
- For logic heavy on decisions, use property-based or state-machine tests.
  Generate operation sequences and check invariants after each step.
