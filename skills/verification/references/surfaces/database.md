# Database

Behavior that depends on SQL, permissions, transactions, or migrations needs a
real, disposable database. Use the same engine and the same major version as
production.

## Instance

- Start one owned container per run. Name it after the run, and publish it on
  a dynamic loopback port.
- Write an ownership mark into the database itself, for example a database
  comment that holds the container name. Check the mark before any destructive
  step.
- Apply migrations with the deployment's own semantics: the same tool, role,
  and order. When the test path patches migrations or bootstraps missing
  objects, record those steps as substitutions.
- Connect the application with its restricted runtime role, not as a
  superuser.

## Checks

- **Persistence rules.** Exercise constraints, triggers, row-level policies,
  and the runtime role's grants through the real repositories.
- **Transactions.** A late failure rolls back every required effect: state,
  audit, and enqueued work. Nothing is published for a transaction that never
  committed.
- **Migrations on populated data.**
  1. Load representative data at the predecessor schema.
  2. Migrate.
  3. Check the transformed data, preserved history, grants, and a few runtime
     reads and writes.

  A migration that passes only on an empty database proves little.
- **Required cases.** List the database cases that must run in a manifest. The
  runner fails when a listed case is missing, skipped, or cached.

## Gotchas

- Tests that skip when their database URL is unset count as gaps, not as
  passes. Wire every such variable into the runner, or list the gap.
- Before you connect, make sure a loopback address isn't a tunnel to a shared
  database.
- Two agents need two databases.
