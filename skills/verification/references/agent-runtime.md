# Agent Runtime

Before you trust any check, confirm that this agent, in this harness, can run
it. A sandbox that blocks Docker or loopback ports turns real-dependency tests
into silent skips.

## Probes

Run each probe once per setup and record the result in the config's Gotchas:

| Capability | Probe |
| --- | --- |
| Containers | `docker info` (or `podman info`) succeeds, and the endpoint is local, not a remote context |
| Required images | Present in `docker images`. Pulling an image needs approval |
| Loopback bind | A process can listen on `127.0.0.1:0`. For example, run a test that uses an ephemeral listener |
| Registries | The language's package proxy is reachable, or the project vendors or caches dependencies |
| Toolchains | The versions match the project's pins |
| Runner loads | The task runner lists its tasks. Root runner files can run tools while they load, so a missing dependency breaks every task |
| Shell | Scripts run under the interpreter their shebang names. Sourcing a bash helper from zsh resolves paths differently |
| Free ports | The fixed ports the stack needs are free. Prefer dynamic ports |

## When a Probe Fails

Use the cheapest remedy that keeps the check real. Try them in this order:

1. **Ask the harness.** Request sandbox escalation for this command. Or ask the
   user to start the daemon, for example OrbStack or Docker Desktop.
2. **Remove the dependency.** Vendor dependencies, use offline mode, or point
   caches at a writable directory.
3. **Two-phase setup.** Provision once (images, dependencies, migrated
   template data), then start services in each session. Snapshots keep files,
   not processes.
4. **Remote runtime.** Run `up` and `verify` on a CI runner or remote host, and
   read the verdict and evidence from there.

A remedy that changes harness or CI configuration needs approval. When every
remedy fails, mark the dependent checks `blocked` and name the missing
capability.

## Parallel Agents

Give each agent or worktree its own instance:

- names that carry the run ID, for example `<project>-verify-<id>`;
- dynamic ports, recorded in the `up` state file;
- separate data directories or databases.

Two agents that share one instance corrupt each other's evidence. Keep a stack
that supports per-worktree isolation in that mode.
