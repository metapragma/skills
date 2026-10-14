# Supported session sources

The executing runtime and the sources being assessed are separate. Any runtime
that can read local files and run Python can use these parsers. Do not infer the
executing runtime from files on disk or stop because it differs from a source.

| Source | Collector ID | Default location |
| --- | --- | --- |
| Claude Code | `claude` | `~/.claude/projects` JSONL |
| Codex | `codex` | `~/.codex/sessions` and `archived_sessions` rollout JSONL |
| Warp | `warp` | Local channel `warp.sqlite` databases, opened read-only |
| Pi | `pi` | `~/.pi/agent/sessions` JSONL |
| Grok Build | `grok` | `~/.grok/sessions` chat-history JSONL |
| ZCode | `zcode` | `~/.zcode/cli/rollout` model-io JSONL |

`--harness auto` and `--harness all` scan every available supported source.
`--harness ID` requests one. Overrides are `--claude-home`, `--codex-home`,
`--pi-home`, `--grok-home`, `--zcode-home`, `--warp-data-dir`, and repeatable
`--warp-db`. Claude and Codex also honor `CLAUDE_CONFIG_DIR` and `CODEX_HOME`.
Run `collect_sessions.py --help` for all options.

Collection defaults to all projects and no cap. The lookback window uses file
modification times, or Warp's conversation update time; a matching file can
contain older turns. `--days 0` removes that window. Parent sessions are included
by default; `--include-subagents` adds child sessions. Empty, unreadable, or
unrecognized files may produce no session. Compare source counts, in-scope
counts, and considered counts; explain gaps rather than assuming full coverage.

`--repo PATH` matches that project and verified Git worktrees. Sources without
project metadata cannot be assigned to a project and are excluded by this
filter. `--max-sessions N` keeps the newest sessions without preferring skill
references. Reference counts still cover all considered sessions.

Project skill discovery checks `.agents/skills`, `.claude/skills`, and
`.codex/skills` under inferred Git roots. `--include-global-skills` adds skills
under the configured homes and `~/.agents/skills` and `~/.claude/skills`.
Use repeatable `--skills-dir PATH` for other locations. Resolved symlinks are
deduplicated; different files with the same skill name retain separate hashes.
Catalog snapshots describe current files, not historical applicability.

Transcripts retain a bounded head and tail, with explicit omission and truncation
markers. JSONL locations address physical lines, including invalid lines.
`inspect_evidence.py` verifies and reads the original collected byte prefix.
Warp evidence is a saved redacted snapshot of decoded visible messages;
unsupported protobuf variants or oversized conversations can be skipped.
ZCode reconstructs only the last request's context window, so it cannot establish
events lost from that context. Do not infer full-session behavior from it.
