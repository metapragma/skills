---
name: frontend-integration-handoff
description: Create a standalone, implementation-ready backend-to-frontend handoff document for a completed or in-progress feature. Use after adding or changing APIs, DTOs, schemas, fields, validation, permissions, workflows, or other backend behavior that frontend developers must integrate, especially when asked to document a feature in docs/handoff or explain everything frontend needs without reading the backend code.
---

# Frontend Integration Handoff

Produce the document a frontend engineer can use as the sole technical guide for implementing and verifying the integration without guessing. Ground contract claims in repository evidence; expose missing rules rather than inventing certainty.

## Writing standard

Use the shortest document that preserves every fact needed to integrate correctly. Apply **frontend relevance**: include a fact only when the frontend engineer needs it to make a call, construct a payload, interpret a result, determine action eligibility, handle an error, or verify frontend behavior. Describe the observable contract, not the backend steps that produce it. Keep necessary contract details even when they require a longer explanation.

Use direct statements, compact tables, and concrete examples. Define each rule and shared shape once, beside the flow, endpoint, or field it governs; reference that definition where reused. Keep investigation notes and backend implementation references in the internal evidence ledger. Include source links only when the frontend engineer can use them for integration; necessary contract facts must remain in the handoff.

## Language

Write all document prose, headings, explanations, instructions, and human-readable labels in Russian. Keep exact technical literals in their source language, including API paths, HTTP methods, DTO and field names, enum values, identifiers, code, JSON, commands, and file paths. Do not translate or transliterate those literals.

## Establish the local format

1. Locate the repository root and its instructions.
2. Inspect `docs/handoff` and read roughly the three most recent documents by filename timestamp or modification time. Prefer recent documents from the same domain when available.
3. Follow their conventions where consistent with this skill's clarity and relevance requirements; do not inherit repetition, omissions, or stale facts.
4. If no convention exists, write `docs/handoff/YYYY-MM-DD-<feature>-frontend-handoff.md`.

## Build an evidence map

Treat the user-named feature as the scope anchor. Include unchanged contracts and prerequisites needed to integrate it, not unrelated backend behavior. Reconstruct the delivered contract from primary sources:

- Read the PRD, issue, plan, or specification when present.
- Inspect `git status`, the relevant diff, and recent commits. Record the checkout, HEAD, and relevant working-tree state internally to identify the version being documented. Do not assume the diff contains the entire feature.
- Trace exposed routes through authorization, validation, business logic, persistence, serialization, error mapping, and applicable configuration. Compare DTOs and generated schemas with that execution path; declarations alone do not prove runtime payloads or permissions.
- Read focused tests and fixtures to corroborate behavior and obtain realistic examples. Run relevant existing checks where practical; distinguish code inspection, tests read, tests actually passed or failed, and checks not run.
- Search field and enum names across the repository to uncover behavior defined away from the endpoint.
- Use executable code and applicable configuration for implemented behavior; specifications establish intent, not implementation. Identify environment-dependent behavior and its prerequisites.
- Investigate disagreements between code, tests, schemas, and prose by tracing the controlling execution path. If the disagreement remains unresolved, retain it as a contract gap rather than silently choosing a source.

Maintain an internal evidence ledger linking each required frontend decision and factual contract rule to:

- supporting symbols or exact file locations, with relevant tests when available
- its location in the handoff
- verification performed and any remaining evidence gap

Account for decisions about calls, payloads, action eligibility, result interpretation, and next actions, including combinations of fields, permissions, and states. Naming, comments, a single example, or an unsuccessful search cannot establish a contract guarantee.

This investigation establishes the contract; it is not the document outline. Publish only facts that pass the frontend relevance rule. For example, if a database constraint produces a duplicate-name error, document the API condition and error response, not the index name or SQL definition.

## Write the document

Keep the handoff self-contained for this feature, not a system manual. Treat the sections below as coverage checks; combine them as appropriate and omit empty or irrelevant sections.

Use exact field/value predicates. Document guarantees observable through the API and frontend obligations; include labeled UI recommendations only when requested or necessary to explain an integration consequence.

Do not create sections titled "Open questions", "Ambiguities", or equivalent. Place unresolved mismatches and limitations in the relevant API, field, flow, rollout, or verification section. When a gap prevents a required frontend decision, mark the affected operation as blocked, state the exact missing rule and decision it prevents, and distinguish independently implementable operations. Do not invent a fallback or call a blocked operation implementation-ready.

### Feature overview

Briefly state the user-visible capability, affected frontend surfaces, changed behavior, and necessary prerequisites. Include rationale or unchanged behavior only when it affects integration decisions.

### Integration flow

For each frontend action, specify its trigger, eligibility conditions, required inputs, API call, observable result, and next action. Cover materially different branches, state transitions, refresh or polling behavior, and terminal states. Make ownership clear: what frontend sends, which response values the server controls, and what the user can change.

### API and payload contract

For new or changed endpoints, document the contract needed for this integration:

- HTTP method and full path
- purpose and when to call it
- authentication, authorization, and relevant role rules
- path, query, header, and body inputs
- success status
- meaningful error statuses, error payloads, and recovery behavior
- pagination, sorting, filtering, idempotency, concurrency, caching, or rate-limit semantics

For existing prerequisites, include only calls, inputs, outputs, and rules needed by this flow. Keep necessary facts here, not solely behind links.

Define each request and response payload needed by the integration once, combining its necessary shape and field semantics. Include all required request fields, optional inputs used by the flow, and response fields the frontend must interpret. Include relevant nested objects and collections; reference shared definitions. Specify each documented field's exact name, type, presence, and nullability. Select documented fields by their use in frontend calls and result handling, not by the completeness of internal DTOs or persistence models.

Explain semantics the shape cannot convey:

- meaning, ownership, allowed enum values, and their behavioral implications
- validation, cross-field constraints, defaults, normalization, lifecycle, and immutability
- formats, units, precision, time zones, and ordering where relevant

Distinguish absent, `null`, empty string, empty array, zero, and false when behavior differs. Prose must add information, not repeat types or presence rules.

Add examples only to clarify otherwise unclear behavior or materially different branches. Use clearly illustrative, internally consistent values valid under the contract; validate with existing tools where practical.

### Frontend implementation guidance

Include only additional feature-specific work, such as required cache invalidation, restrictions on optimistic updates, or repository-supported client regeneration. A checklist may organize this work, but must not repeat the flow or contract. Omit generic frontend advice and unrelated architecture choices.

### Rollout and verification

State the availability, compatibility, feature flags, client configuration, and test-data prerequisites the frontend must know. For a backend-owned prerequisite, name the required capability or environment state and responsible team, not the migration, deployment, seed, or cleanup procedure. Include operational steps only when the frontend team must perform them; establish that ownership from project evidence rather than assigning backend work to the reader.

Give frontend verification scenarios for the happy path and materially different permission, validation, state, and failure branches. Each scenario specifies inputs or initial state, frontend actions or API calls, and expected observable outcomes. Keep backend-only assertions and test commands in the evidence ledger unless the frontend integration workflow requires the reader to use them. Distinguish proposed scenarios from checks actually performed.

## Quality gate

Before finishing:

1. Apply frontend relevance first. For each paragraph, table row, and example, identify the specific frontend decision or frontend verification scenario it supports. If none exists, remove it. If another item already supplies the needed fact, consolidate them. Backend traceability or verification of backend internals alone does not justify inclusion.
2. Check evidence against the document: every rule needed for the scoped frontend actions and verification is represented, including necessary prerequisites and unchanged behavior. Completeness applies to the integration contract, not every backend fact found during investigation.
3. Check the document against evidence: every factual contract claim has a ledger entry; recommendations and illustrative values are distinguishable from guarantees. Unsupported claims fail this gate: investigate them or explicitly mark the affected decision unresolved.
4. Perform an implementation dry run using only the handoff as the specification. Derive payloads, action eligibility predicates, state transitions, and error-recovery behavior for every flow, then compare them with repository evidence. Any required guess, contradiction, or unexplained branch fails this check. Repair the document and repeat; if evidence cannot resolve a rule, mark the affected operation blocked.
5. Confirm contracts, flows, examples, and frontend verification scenarios agree, including cross-field constraints. Check that any reported verification claims match the checks performed on the recorded version. Preserve necessary contract distinctions rather than shortening to a fixed word limit.
6. Ensure the document contains no secrets, production credentials, private customer data, or invented values presented as facts.

The handoff is implementation-ready only when every required frontend decision is explicit, evidence-backed, and consistent across the document. Otherwise, report the specific blocked operations and distinguish the portions ready to implement.

Report the created document path, readiness, and any blocked operations. Do not modify backend or frontend implementation unless the user also requested those changes.
