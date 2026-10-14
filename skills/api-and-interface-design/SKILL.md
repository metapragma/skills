---
name: api-and-interface-design
description: "Design or review API and interface contracts: requests, responses, errors, authorization, pagination, retries, and compatibility. Use for new or changed endpoints and consumer-facing module contracts, not general architecture or routine internal refactors."
license: MIT
metadata:
  source: "https://github.com/addyosmani/agent-skills/tree/2686b620fc1fed2e8f60c704839c766b8594c6b6/skills/api-and-interface-design"
---

# API and Interface Design

Make the caller's contract explicit before changing its implementation. Scale
the work to the request: review requests produce findings, design requests
produce a proposal, and implementation requests may change code. Do not turn a
small interface change into a new architecture or API style.

## Establish the existing contract

Read applicable repository instructions, interface definitions, representative
callers, tests, and relevant design decisions. Use the project's existing domain
glossary and naming conventions. Follow its context map when present; do not
create a competing glossary or assume a particular filename is authoritative.

Identify consumers and the boundary: in-process module, HTTP endpoint, GraphQL
schema, event, or another protocol. Use the existing schema and documentation
tooling. Check installed versions and primary documentation when behavior is
version-sensitive. Separate observed behavior from intended behavior.

For an existing interface, identify what changes for callers before proposing a
replacement. Observable quirks may have consumers even when undocumented; look
for usage evidence rather than assuming either that nobody depends on them or
that every quirk must be preserved forever.

## Define the contract

Address the dimensions relevant to this change; mark unresolved decisions rather
than inventing requirements:

- **Inputs and outputs:** fields, types, units, bounds, defaults, nullability,
  omitted versus explicit null, unknown-field handling, and serialization.
  Separate caller-supplied values from server-owned fields. Use explicit variants
  where they prevent invalid states; types alone do not describe all semantics.
- **Effects:** state transitions, ordering, atomicity, partial success, and what
  completion means. For asynchronous work, specify how callers observe progress,
  failure, and cancellation.
- **Errors:** follow the project's error representation. Distinguish validation,
  authentication, authorization, absence, conflict, rate limits, and dependency
  failures as the protocol requires. Give callers stable machine-readable
  signals without exposing secrets or internal details. Define which failures
  are retryable rather than relying on message text.
- **Trust and authorization:** validate untrusted input and external responses
  where trust changes. Enforce resource, tenant, and field-level permissions
  server-side. Valid types do not establish authorization or business invariants.
  Stored data is not automatically trustworthy: consider legacy records, other
  writers, and migrations. Avoid redundant validation only where guarantees
  actually hold.
- **Collections:** bound result sizes where collections can grow. Choose cursor
  or offset pagination from access patterns and consistency needs, with stable
  ordering and a tie-breaker. Specify filtering, sorting, page limits, and what
  concurrent changes do to traversal. Do not require expensive total counts
  without a consumer need.
- **Updates and concurrency:** define replacement versus partial-update
  semantics, clearing fields, immutable fields, and lost-update handling. Choose
  the protocol's appropriate operation rather than universally preferring PATCH
  or PUT. Document preconditions or version checks when writers can conflict.
- **Retries:** define timeouts, retry limits, cancellation, and duplicate effects.
  For retryable side effects or idempotency keys, read
  [references/retry-safety.md](references/retry-safety.md).

Keep naming and protocol choices consistent with the project. Do not impose
TypeScript, camelCase, enum casing, REST resource conventions, or HTTP status
codes on interfaces where they do not apply.

## Evolve without surprising consumers

Prefer compatible extensions, but verify them: an optional field, enum value,
new error, or changed default can still break strict clients or change behavior.
Check source, wire, and behavioral compatibility as relevant. Include generated
clients and old/new deployments coexisting during rollout.

For a necessary breaking change, identify affected consumers, the transition
strategy, deprecation/removal criteria, and recovery options. Use the project's
versioning policy; neither permanent parallel versions nor a universal ban on
versioning is the default. Separate a design recommendation from authorization
to migrate data, publish a package, or deploy.

## Verify and report

Use the repository's existing test and schema tools. Select contract checks for
the changed behavior: valid and invalid input, permission boundaries, stable
errors, serialization, update semantics, and compatibility. For pagination or
retry changes, include the failure and concurrency cases they claim to handle.
Exercise the real boundary where practical; a mock that supplies the promised
behavior does not prove the implementation provides it.

Update the existing contract documentation alongside implementation. Report the
contract or findings, compatibility impact, key tradeoffs, and checks actually
run. Keep proposed checks distinct from passed checks; disclose unresolved
requirements and unavailable verification. Do not claim production readiness
from a schema or a happy-path example alone.
