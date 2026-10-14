# Evidence

The evidence record tells a reviewer what actually ran, against which
revision, and with what result. The project's `verify` command writes it.
The agent's report summarizes it.

## Record

Write `record.json` in the run directory,
`.verification/runs/<UTC timestamp>-<short revision>/`, which git ignores.

```json
{
  "revision": { "commit": "<sha>", "dirty_diff_sha256": "<sha or null>" },
  "started_at": "<UTC>",
  "duration_s": 0,
  "environment": { "os": "", "toolchains": {}, "images": {}, "runtime": "local|ci|remote" },
  "checks": [
    {
      "id": "api",
      "command": "task verify:api",
      "status": "passed|failed|blocked|not_run",
      "exit_code": 0,
      "tests_run": 0,
      "tests_skipped": 0,
      "reason": "",
      "log": "logs/api.log"
    }
  ],
  "substitutions": ["auth stubbed in composed tests"],
  "integrity": [],
  "flaky": [],
  "artifacts": []
}
```

- **`revision`.** Binds the record to one candidate. A record for an earlier
  revision is not evidence for the current one.
- **`status`.**
  - `passed`: the check ran and its assertions held.
  - `failed`: the check ran and an assertion failed.
  - `blocked`: a named prerequisite prevented the check from running.
  - `not_run`: the check was outside this run's scope.
- **`tests_run`.** Counts tests that actually executed. Zero means `failed`.
- **`substitutions`.** Lists every stub, fake, mock, or shared environment
  that stood in for a real dependency.
- **`integrity`.** Holds the findings from [integrity.md](integrity.md).
- **`flaky`.** Lists checks that passed only on a retry. Report them; don't
  hide them.
- **`artifacts`.** Paths to files the run produced.

## Observation

Effects prove more than responses do. After a journey, read the durable state
that the requirement names: rows, audit entries, queued work, files, and
messages captured by local sinks. Read it with the role the application uses,
not with a superuser, when access rules matter. Keep one greppable log per run:
server, worker, and browser console output, each line tagged with its source.

## Artifacts

Screenshots, video, and recorded requests and responses are for humans to
check quickly. Capture them when the user asks, or when the project config
requires them for a surface. They don't replace a check that can produce a
verdict.

## Report Table

End the handoff with this table:

```markdown
| Check | Status | Tests | Notes |
| --- | --- | --- | --- |
| fast | passed | 42 | |
| api | blocked | 0 | Docker unavailable in sandbox; owner: user |
| integrity | passed | — | no test or config weakening |
Revision: <sha> (+ uncommitted changes) · Evidence: .verification/runs/<dir>
```

Every `blocked` or `not run` row names the gap and who owns it.
