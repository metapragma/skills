---
name: how
description: Explain how a subsystem or piece of code works, deep enough for an engineer to start working in it.
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/how"
---

# How

Explain how the code in question works, at the level a senior engineer needs
to build a working mental model: enough to start changing it with confidence,
not so much that it reads like annotated source.

1. **Scope and form.** Restate the question in one line. When the scope is
   ambiguous, state your interpretation and proceed; the user can redirect.
   Pick the form:
   - **Walkthrough** (default): the full explanation.
   - **Map**: one layer up. The relevant modules and their callers, for an
     area the user doesn't know yet.
   - **Short post**: a scannable explanation of a diff or a small scope, per
     [references/short-post.md](references/short-post.md).
2. **Vocabulary.** Read the project's domain glossary when one exists
   (`CONTEXT.md`, or the layout `docs/agents/domain.md` names) and use its
   terms throughout.
3. **Explore.** Read the code; never guess from names.
   - **Simple** (one module, one function, a narrow question): trace it
     yourself.
   - **Complex** (a subsystem across files or services): split it into two to
     four exploration angles. When the harness offers subagents, give each
     angle to a read-only explorer with
     [references/explorer-brief.md](references/explorer-brief.md). Otherwise
     work through the angles yourself, one at a time.

   Done when you can describe the whole flow without hand-waving, and every
   part you couldn't trace is written down as an open question.
4. **Explain.** Write the answer in the chosen form, per
   [references/explanation.md](references/explanation.md). Check any claim an
   explorer made that the explanation depends on, by reading the cited code.

**Reply:** the explanation itself, with the open questions at the end.
