Personal collection of local and imported agent skills

Start most work with `/pragma-mode <goal>`. It matches the task to a playbook
and runs the skills below as its steps. `/setup-info` recommends a skill when
you want one step on its own.

- [Playbooks](skills/pragma-mode/playbooks/): one file per kind of task, such
  as bug fix, feature, refactoring, or perf.
- [Principles](skills/pragma-mode/principles/): one file per engineering
  principle the playbooks apply.
- [Wiring map](https://metapragma.github.io/skills/wiring-map.html):
  an interactive graph of which skills, playbooks, and principles each file
  calls. The page is [docs/wiring-map.html](docs/wiring-map.html).
