# Third-Party Notices

Pragma mode adapts parts of [pstack](https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack)
at commit `d73344bee8cf22e53b9d5f4cf5749d38ba38c174`. The MIT license is in
[LICENSE](LICENSE).

| Local file | Source |
|---|---|
| `SKILL.md` | `skills/poteto-mode/SKILL.md` and `skills/figure-it-out/SKILL.md` |
| `playbooks/investigation.md` | `skills/poteto-mode/playbooks/investigation.md` |
| `playbooks/bug-fix.md` | `skills/poteto-mode/playbooks/bug-fix.md` |
| `playbooks/feature.md` | `skills/poteto-mode/playbooks/feature.md` |
| `playbooks/committing.md` | `skills/poteto-mode/playbooks/opening-a-pr.md` |
| `playbooks/refactoring.md` | `skills/poteto-mode/playbooks/refactoring.md` |
| `playbooks/perf.md` | `skills/poteto-mode/playbooks/perf-issue.md` |
| `playbooks/hillclimb.md` | `skills/poteto-mode/playbooks/hillclimb.md` |
| `playbooks/forensics.md` | `skills/poteto-mode/playbooks/runtime-forensics.md` and `trace-forensics.md` |
| `playbooks/prototype.md` | `skills/poteto-mode/playbooks/prototype.md` |
| `playbooks/pickup-and-pause.md` | `skills/poteto-mode/playbooks/session-pickup.md` and `pause-safely.md` |
| `playbooks/skill-change.md` | `skills/poteto-mode/playbooks/authoring-a-skill.md` and `eval.md` |
| `references/decision-log.md`, `scripts/log.sh` | `skills/show-me-your-work/` |
| `principles/<name>.md` | `skills/principle-<name>/SKILL.md` |

`playbooks/feature-large.md` is local. It sequences this repository's own
planning skills.

## Adaptations

- The steps call this repository's skills by path. Each playbook keeps
  pstack's ownership line, step order, and reply contract.
- The house rules keep this repository's authorization posture. Commits,
  pushes, pull requests, tracker writes, and messages need the user's
  go-ahead. `principle-never-block-on-the-human` is not adopted; its "run it
  instead of asking" idea is kept as the Facts before questions rule.
- Delegation names the kind of work instead of a model, and briefs point at
  this skill instead of a dedicated subagent. Cursor-specific mechanics are
  removed: custom mode frontmatter, the per-role model rule, task tool
  parameters, transcript paths, and `cursor-team-kit` dependencies.
- The bug-fix playbook relaxes this repository's tdd seam confirmation and
  allows the reproduction command as the regression check when a test is
  impractical.
- `migrate-callers-then-delete-legacy-apis` excludes consumer-facing
  contracts, and `outcome-oriented-execution` requires telling the user before
  planned breakage.
- Runtime and trace forensics merge into one playbook with two branches, as do
  session pickup and pause safely. Pause leaves changes uncommitted unless the
  user approves a checkpoint commit. Hillclimb commits kept changes only when
  the user approved commits for the run.
- The eval and the decision log drop transcript paths and the cross-model
  review requirement. Independence comes from a fresh context, and the report
  says when a judge shares the candidates' model family.
- Reply rules drop pstack's punctuation bans and defer prose style to the
  user's and project's own instructions.
