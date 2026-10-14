# Third-Party Notices

Setup and audit mode adapt two skills from the pstack collection:

- [create-verification-skill](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/create-verification-skill/SKILL.md),
  at commit `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, including the
  usable-readiness, seed-gap, and stand-in disclosure rules that upstream added
  on 2026-10-12;
- [maintain-verification-skill](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/maintain-verification-skill/SKILL.md),
  at the same commit.

The adaptation keeps these elements of the upstream skills:

- launch, doctor, drive, evidence, and cleanup;
- ownership rules;
- the passed, failed, blocked, and not-run statuses;
- the drift classification.

It differs from upstream in these ways:

- It is one global skill, not a generated project-local skill.
- Execution lives in project task-runner commands.
- Per-project details go in `docs/agents/verification.md`.
- It adds integrity, enforcement, and per-surface references.

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
