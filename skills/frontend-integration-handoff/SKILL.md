---
name: frontend-integration-handoff
description: Create a standalone, implementation-ready backend-to-frontend handoff document for a completed or in-progress feature. Use after adding or changing APIs, DTOs, schemas, fields, validation, permissions, workflows, or other backend behavior that frontend developers must integrate, especially when asked to document a feature in docs/handoff or explain everything frontend needs without reading the backend code.
---

# Frontend Integration Handoff

Produce the document a frontend engineer can use as the sole technical guide for integrating the feature. Derive every claim from the repository; never fill gaps with plausible guesses.

## Establish the local format

1. Locate the repository root and its instructions.
2. Inspect `docs/handoff` and read roughly the three most recent documents by filename timestamp or modification time. Prefer recent documents from the same domain when available.
3. Follow their naming, structure, tone, and level of detail, but do not inherit omissions or stale facts.
4. If no convention exists, write `docs/handoff/YYYY-MM-DD-<feature>-frontend-handoff.md`.

## Build an evidence map

Treat the user-named feature as the scope anchor. Reconstruct the delivered contract from primary sources:

- Read the PRD, issue, plan, or specification when present.
- Inspect `git status`, the relevant diff, and recent commits. Do not assume the working-tree diff contains the entire feature.
- Trace routes through controllers or handlers, request and response DTOs, validators, services, persistence models, serializers, permissions, and generated API specifications.
- Read focused tests and fixtures. Use them to confirm edge cases and obtain realistic examples.
- Search field and enum names across the repository to uncover behavior defined away from the endpoint.
- Distinguish implemented behavior from planned behavior. Document only what the code supports, and label unresolved mismatches explicitly.

Keep notes mapping each documented statement to code or tests. Prefer runtime behavior over comments and stale prose when they conflict.

## Write the document

Make the handoff standalone. Include the following sections when applicable, adapting headings to the repository convention.

### Feature overview

Explain the user-visible capability, why it exists, which frontend surfaces it affects, and the end-to-end flow. State what changed and what did not change.

### Integration flow

Describe the exact sequence of frontend actions and API calls. Cover prerequisites, branching paths, state transitions, refresh or polling behavior, and terminal states. Make ownership clear: what frontend sends, what backend computes, and what the user can change.

### API contract

For every affected endpoint, document:

- HTTP method and full path
- purpose and when to call it
- authentication, authorization, and relevant role rules
- path, query, header, and body inputs
- success status and full response shape
- meaningful error statuses, error payloads, and recovery behavior
- pagination, sorting, filtering, idempotency, concurrency, caching, or rate-limit semantics
- complete realistic request and response examples

Do not write “standard fields omitted.” Show complete shapes needed for implementation, including nested objects and collections.

### Field reference

Account for every frontend-visible field. For each field, state as applicable:

- exact name and location
- type and format
- required, optional, nullable, or conditionally present status
- semantic meaning and source of truth
- allowed enum values and the meaning of each
- validation constraints, units, ranges, defaults, and normalization
- when it appears, changes, or becomes immutable
- display or interaction implications that follow from the contract

Clearly distinguish absent, `null`, empty string, empty array, zero, and false when the backend treats them differently. Explain timestamps, time zones, identifiers, money, precision, and ordering rules precisely.

### Frontend implementation guidance

Translate the contract into concrete integration work without prescribing an unrelated frontend architecture. Cover data fetching, mutations, local state, loading and empty states, validation, permissions, disabled actions, confirmation steps, errors, retries, optimistic updates, cache invalidation, and backward compatibility when relevant.

Provide a concise implementation checklist. Include generated-client or schema regeneration steps only when supported by the repository.

### Rollout and verification

Document migrations, feature flags, configuration, seed data, compatibility constraints, deployment order, and cleanup requirements that affect integration. Give test scenarios for the happy path, permissions, validation boundaries, state transitions, and important failures.

### Open questions

List only genuine unresolved items. Explain their integration impact and point to the conflicting or missing evidence. Never hide uncertainty inside definitive prose.

## Quality gate

Before finishing:

1. Cross-check every route, field, enum, status code, default, permission, and example against code or tests.
2. Confirm every changed frontend-visible contract is represented in the document.
3. Confirm examples are internally consistent and valid under documented constraints.
4. Remove backend implementation detail that cannot affect frontend behavior.
5. Expand vague phrases such as “etc.”, “as usual”, “standard response”, or “handle errors appropriately”.
6. Ensure the document contains no secrets, production credentials, private customer data, or invented values presented as facts.
7. Ensure a frontend engineer can implement and verify the integration without opening backend source files.

Report the created document path and summarize any open contract questions. Do not modify backend or frontend implementation unless the user also requested those changes.
