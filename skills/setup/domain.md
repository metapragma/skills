# Domain Docs

Setup template: adapt these defaults to the project's existing paths and rules before writing
`docs/agents/domain.md`. Preserve valid existing mappings.

## Sources

- Vocabulary: `CONTEXT.md` by default; use the existing glossary or domain document when present.
- Context routing: follow the project's context map, if any, to relevant vocabulary sources.
- Decisions: `docs/adr/` by default; preserve existing ADR locations, formats, and status rules.
- Feature behavior: the relevant specification or ticket, not glossary entries.

Record whether `CONTEXT.md` is a glossary or an index. An index routes to authoritative documents;
it is not a destination for new definitions. Load only sources relevant to the current task.

## Edits And Approval

Record the project's domain-edit and ADR-acceptance requirements here. A resolved term is a
candidate edit, not automatic authorization to change a protected source. Present proposed wording
when approval is still needed. Preserve combined domain documents and their non-glossary sections.

Create missing documents only for authorized content when no existing owner serves that purpose.
Use the default glossary layout only in projects without an established convention.

## Usage

Use the configured vocabulary in questions, hypotheses, tickets, code, and explanations. Surface
conflicts with authoritative terms or accepted ADRs; keep proposals distinct from approved decisions.
