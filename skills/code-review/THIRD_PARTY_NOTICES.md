# Third-Party Notices

The primary Matt Pocock source is tracked in `skill-sources.json`. The review
criteria and `references/risk-checks.md` also adapt ideas from Addy Osmani's
`agent-skills`, reviewed at commit
`2686b620fc1fed2e8f60c704839c766b8594c6b6`:

- https://github.com/addyosmani/agent-skills/blob/2686b620fc1fed2e8f60c704839c766b8594c6b6/skills/code-review-and-quality/SKILL.md
- https://github.com/addyosmani/agent-skills/blob/2686b620fc1fed2e8f60c704839c766b8594c6b6/references/security-checklist.md
- https://github.com/addyosmani/agent-skills/blob/2686b620fc1fed2e8f60c704839c766b8594c6b6/references/performance-checklist.md

This is a selective local adaptation, not a full import. It retains the local
candidate-selection workflow and replaces universal thresholds and workflow
mandates with evidence-based, change-specific checks.

## Addy Osmani: MIT License

Copyright (c) 2025 Addy Osmani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## pstack: Blast Radius

The Change Propagation guidance selectively adapts
[blast-radius](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/blast-radius/SKILL.md)
at commit `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`. It retains indirect-consumer
tracing, version-specific semantics, and evidence for decisive safety assumptions.
It removes mandatory companion skills and multi-model review, permits several
assumptions, and preserves read-only scope and limited verification claims.

## pstack: Reader Load and Shared Mutable State

The structural review and Shared Mutable State guidance selectively adapt these
principles at the same pinned pstack commit:

- [Minimize Reader Load](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/principle-minimize-reader-load/SKILL.md)
- [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md)

The adaptation requires concrete comprehension costs or failure paths, preserves
useful modules and shared invariants, and checks coordination across actual
writers. It does not impose fixed metrics, automatic wrapper removal, or fixes
during read-only review.

## pstack: Interrogate

`references/lead-judgment.md` and the independent second-reviewer option adapt
[interrogate](https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/interrogate)
and its `references/lead-judgment.md` at commit
`d73344bee8cf22e53b9d5f4cf5749d38ba38c174`. The adaptation keeps the lead
reviewer's filters and the act on, consider, noted, and dismissed buckets. It
drops the configured multi-model reviewer panel: independence comes from a
fresh context, and the report says when the reviewer shares the author's
model family.

## Lauren Tan: MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
