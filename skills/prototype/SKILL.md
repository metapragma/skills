---
name: prototype
description: Build a throwaway prototype or small executable experiment to answer a design question. Use for exploring UI or state models, or settling uncertain behavior or timing through observation.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify the question from the user's prompt and surrounding code. Distinguish
observable facts from product choices: investigate facts with existing evidence
or a small experiment, and ask about preferences or intended behavior only when
they materially affect the answer. A read-only question does not authorize
creating a prototype merely because a fact could be measured.

- **"What actually happens, or how long does it take?"** -> [EXPERIMENT.md](EXPERIMENT.md). Use the smallest executable check against the relevant real code. A script or existing harness is enough; no interactive demo is required.
- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file — free-play buttons plus tabbed guided walkthroughs — that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

Choose the branch by the evidence needed, not the file's location. Observing a
parser's handling of escaped quotes calls for an experiment; letting a domain
expert explore a proposed state machine calls for a logic demo. Clarify genuinely
different goals, otherwise state a reasonable interpretation and proceed.

## Rules that apply to all branches

1. **Throwaway from day one, and clearly marked as such.** Put small experiments in an isolated scratch location with the target checkout recorded. Place interactive demos near the module or page when useful, clearly named as prototypes. For throwaway UI routes, follow the project's routing convention.
2. **Trivial to run.** Give one command for an experiment or UI prototype, using the project's existing runtime and tools. A self-contained logic demo can open directly in a browser. State required setup rather than hiding it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** Build only what makes the question observable. An experiment may use a focused assertion or existing test harness; do not build a production-grade test suite or abstraction around the prototype.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Keep the rerunnable artifact and record the question, observations, conclusion, and limitations. Return its path and the exact command or URL. Promotion to production, commits, branches, tracker updates, and publication require separate scope and authorization. When authorized to archive a prototype on a throwaway branch, preserve its evidence and link it from the implementation work; keep prototype-only code out of production.
