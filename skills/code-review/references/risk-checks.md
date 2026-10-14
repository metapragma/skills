# Risk Checks

Use only sections implicated by the change. Trace the affected behavior through
callers and boundaries; tie findings to the reviewed candidate and a plausible
failure. These prompts do not establish that a full security or performance
audit has been completed.

## Change Propagation

- State the behavioral difference, including effects not obvious from the edited
  lines. Trace affected contracts beyond direct callers: serialized fields,
  stored data, events, dynamic registration, alternate clients, flags, and
  build/runtime discovery. Tie each relevant consumer to evidence; symbol search
  alone cannot establish that no indirect consumer exists.
- Follow ordering where it matters: retries, asynchronous callbacks, teardown,
  cancellation, and mixed-version operation. When safety depends on a library's
  behavior, inspect the actual pinned version and local patches, not assumptions
  from another version's documentation.
- Identify the few assumptions that materially determine safety. There may be
  several; do not force the analysis into one fact. Describe a concrete failure
  if each assumption is false, the affected consumer, and the evidence that
  would distinguish safety from failure. Avoid speculative lists of everything
  a system could ever break.
- Test decisive assumptions with existing safe checks against the selected
  snapshot when feasible. Propose new regression tests or reproductions that
  require edits or consequential actions; read-only review does not authorize
  them. A scratch experiment, when authorized, must be isolated from user state
  and must exercise the relevant real code rather than restate the assumption.
- Separate assumptions checked in source, exercised by executable checks,
  observed in the running app, and still unverified. Record inputs, version,
  command, and outcome for checks actually run. A passing check supports its
  exercised conditions, not all consumers or the whole change.
- Report substantiated risks with a failure path and impact. Keep cleared concerns
  brief and distinguish them from missing evidence; no matching search result
  is a coverage limit, not proof of safety. Do not invent likelihood percentages.

## Shared Mutable State

- Identify the changed write targets, all relevant writers, and the invariants
  readers rely on. Follow overlapping read-modify-write operations; workers
  updating different fields in one file can still overwrite each other's work.
- Before recommending a lock, check whether independently owned state would
  remove the collision. Preserve shared state when partitioning would break
  atomicity or consistency; more files are not inherently safer.
- For required sharing, inspect actual enforcement: exclusive ownership, locks,
  transactions, or atomic conditional updates. Verify that it covers every
  writer and the full operation across the relevant threads or processes.
  Taking turns by convention does not prevent concurrent writes.
- Trace relevant failure, cancellation, and recovery paths, including stale
  ownership or partial updates. Support findings with a concrete interleaving
  or existing check against the candidate. Missing checks are a coverage gap,
  not proof of a race; review remains read-only unless fixes are requested.

## Dependencies

- For additions, check whether the existing stack already meets the need and
  whether the package's maintenance, provenance, license, and runtime or bundle
  cost fit the project. Assess the tradeoff rather than banning new dependencies.
- For upgrades, read release and migration notes spanning the actual version
  change. Inspect the authoritative lockfile and relevant transitive changes;
  successful installation and semver labels do not prove compatibility.
- Identify changed install scripts, package sources, and permissions before
  executing unfamiliar dependency code. Use the project's package manager and
  approval policy; review does not authorize automatic audit fixes or upgrades.
- Check known advisories against actual usage and exposure. An audit result
  alone neither proves exploitability nor rules out supply-chain compromise.
- Check tests around the behavior the dependency supplies. Compare baseline and
  candidate results where practical; disclose missing coverage. Recommend smaller
  upgrade groups when that improves diagnosis, while keeping coupled packages
  together. Do not impose one-package-per-change universally.

## Security and Trust Boundaries

- Identify the changed entry points, protected resources, and actors. Trace
  attacker-controlled values to queries, rendering, commands, URLs, and paths;
  check validation and safe handling at the relevant boundary.
- Distinguish authentication from authorization. Check resource ownership,
  tenant isolation, and field/action permissions, including alternate access
  paths introduced by the change.
- Follow sensitive data into responses, logs, errors, storage, and external
  services. Check whether the change introduces exposure or weakens an existing
  protection. Stored or internal data is not automatically trusted.
- For LLM features, treat retrieved content and model output as untrusted data.
  Check that application code enforces tool permissions and tenant boundaries,
  validates tool arguments, and preserves required approval for consequential
  actions. Prompt instructions alone are not an authorization boundary.
- Check bounds on expensive requests, uploads, retries, and agent loops when
  untrusted input can drive consumption. Derive limits from the service's needs,
  not universal numeric defaults.

## Performance and Resource Use

- Follow work as input size or concurrency grows: queries inside loops,
  unbounded fetching, fan-out, retries, blocking work, and repeated rendering.
  Explain the scaling mechanism; distinguish a plausible risk from measured cost.
- For query changes, inspect representative query plans and data sizes when
  available. Consider index write cost as well as read benefit; adding an index
  or rewriting a query is not proof of improvement.
- For caches, check keys against tenant, viewer, permissions, and other inputs
  that affect the result. Review invalidation, allowed staleness, concurrent
  misses, error handling, and memory bounds. Caching can create correctness bugs.
- Check lifecycle and aggregate limits for connections, workers, listeners,
  timers, and buffers, including error and cancellation paths. Per-process limits
  may exceed shared capacity when multiplied across instances.
- Compare equivalent workloads and environments for claimed improvements.
  Check relevant latency, throughput, memory, or browser interaction evidence;
  use project budgets and representative devices. Report assumptions and missing
  measurements instead of inventing timings or enforcing generic thresholds.
