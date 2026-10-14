# CLI and TUI

A command-line tool has no server to keep alive. Build it once, then run each
case as a fresh process in its own isolated state.

## Launch

Build the binary or install it into a scratch prefix. Give each case:

- its own working directory;
- its own `HOME` or config directory;
- its own environment.

That way, cases never read the user's real configuration or credentials.

## Drive

- **Non-interactive commands.** Run the command, then assert the exit code,
  stdout, and stderr separately. Also check the files it wrote and any network
  calls it made, through a capture sink.
- **Interactive TUIs.** Drive them through a PTY harness: `expect`, `tmux
  send-keys` with `capture-pane`, or the language's PTY library. Wait for
  prompt strings, not for fixed sleeps.
- **Golden output.** Compare against golden files only after normalizing
  timestamps, paths, and colors. Treat updates to the golden files as integrity
  items.

## Gotchas

- `--dry-run` may still write caches or call the network. Observe what it
  actually skips.
- Some help or version paths exit 0 without loading configuration. They prove
  the binary starts, not that it works.
