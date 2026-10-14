Custom workflow. Some ideas influenced by Matt Pocock and Addy Osmani as well as pstack.

Start most work with `/pragma-mode <goal>`. It matches the task to a playbook
and runs the skills below as its steps. `/setup-info` recommends a skill when
you want one step on its own.

- [Playbooks](skills/pragma-mode/playbooks/): one file per kind of task, such
  as bug fix, feature, refactoring, or perf.
- [Principles](skills/pragma-mode/principles/): one file per engineering
  principle the playbooks apply.
- An [interactive graph](https://metapragma.github.io/skills/wiring-map.html)
 of which skills, playbooks, and principles
  each file calls.
