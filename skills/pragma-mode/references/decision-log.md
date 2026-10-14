# Decision log

A reviewable trail for long or multi-step work: one TSV file, one row per
decision. Playbooks that need it say so. The log records what was decided and
done, not private reasoning, and never secrets.

## Format

Columns, each cell on one line:

- **ts.** ISO 8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, in one line.
- **why.** The reason in plain words.
- **evidence.** A pointer that proves it: a commit SHA, `file:line`, a command,
  or an artifact path. Never a paragraph.
- **result.** The outcome: `tests green`, `reverted`, `kept`, `inconclusive`,
  `open`.

```
ts	phase	decision	why	evidence	result
2026-10-14T09:02:00Z	frame	measured the export before changing it	need the old number to compare against	scripts/bench-export.sh	p50 41 ms, 7 runs
2026-10-14T10:15:00Z	attempt-3	batched the row inserts	the profile showed one commit per row	commit 7c21e0a	kept, p50 33 ms
2026-10-14T10:40:00Z	attempt-4	cached the schema lookup	looked hot in the profile	worktree reset	reverted, no change past noise
```

## Logging a row

Append rows with [scripts/log.sh](../scripts/log.sh), using the path of this
skill's `scripts` folder:

```bash
bash <pragma-mode>/scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```

It stamps the time, writes the header on first use, keeps each cell on one
line, and quotes cells a spreadsheet would read as formulas.

Log decision points and checkpoints: a fork chosen, a unit finished with its
check result, a pivot or revert with its trigger, a blocker found. For a loop,
log one row per iteration. Skip the trivial.

When a different session adds to an existing log, its first row has the phase
`start` and names the session. Read the last rows before writing, so you know
whether another session wrote since.

## Where it lives

Keep it at `decisions.tsv` in the working directory, or `.audit/<task>.tsv`
when several efforts run at once, and keep it out of version control. Commit it
only when a reviewer needs the trail to trust the result, and only with the
user's go-ahead.

## Rules

- Append only. A wrong call gets a new row that supersedes it.
- Before handing back, walk your rows against what actually happened. Each row
  maps to a real decision, and its evidence resolves. A fork or revert that
  shaped the work but isn't logged is a gap: add it.
