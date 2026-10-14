# Third-Party Notices

The primary Matt Pocock source is tracked in `skill-sources.json`. The Reader Load
and Shared Mutable State sections selectively adapt these pstack principles at
commit `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`:

- [Minimize Reader Load](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/principle-minimize-reader-load/SKILL.md)
- [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md)

The adaptation assesses tracing and mutable-state costs without fixed layer or
time limits. It preserves useful modules and shared invariants, checks independent
ownership before synchronization, and requires actual coordination when sharing
is necessary. It does not mandate wrapper deletion or unrelated redesigns.

`SKETCH-FIRST.md` and `DESIGN-RED-FLAGS.md` adapt pstack's
[architect](https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/architect)
skill and its `references/design-red-flags.md` at commit
`d73344bee8cf22e53b9d5f4cf5749d38ba38c174`. The adaptation keeps grounding,
usage-first sketching, implementing against the sketch, the scrap signals, and
the red flags. It drops the multi-model arena, the configured runner models,
and the automatic run of other skills, and uses this skill's vocabulary.

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
