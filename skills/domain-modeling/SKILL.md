---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, editing its domain glossary, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, test
edge-case scenarios, and record approved definitions and decisions in their owning documents.
This skill changes the model; merely reading the glossary for vocabulary does not require it.

## Resolve the project's domain sources

Read `docs/agents/domain.md` when present, even if the agent entrypoint does not link it.
Follow the project's authority, document ownership, and approval rules. If no mapping exists,
inspect repository instructions and existing domain documents before choosing a destination.
A `CONTEXT.md` may be a navigation index rather than a glossary; follow its pointers. Resolve
conflicting mappings before editing. Do not create a second glossary or rename existing documents.

Use the configured vocabulary source wherever this skill mentions the glossary. Preserve its
existing structure, including domain invariants when the project intentionally keeps them there.
Read only the contexts relevant to the task; an existing context map can route to them.

## Default file structure

The following layout is a fallback for projects with no existing convention, not a required schema.

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create missing documents lazily, only when an authorized edit needs them. Use the fallback paths
only after confirming there is no existing source for that purpose.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the configured glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Record approved domain changes

When a term is resolved, record it in the configured glossary if the task authorizes that edit
and project approval requirements are satisfied. Agreement on meaning is not automatically
approval to change a protected domain document. Otherwise present the proposed wording for
approval and keep it distinct from accepted vocabulary. Do not route around approval by writing
a competing glossary. Preserve the project's format; [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)
is a fallback for new glossaries.

Keep feature behavior and implementation decisions in their owning specification or ADR, not
in glossary entries. Preserve existing non-glossary sections in a combined domain document.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Follow the project's ADR location, format, and
acceptance process; [ADR-FORMAT.md](./ADR-FORMAT.md) supplies defaults. A proposal remains a draft
until approved, and does not supersede an accepted decision merely because it was written later.
