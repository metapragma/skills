# Post-Deploy

Local evidence covers the candidate revision. It doesn't cover the deployed
environment: rollout order, configuration, data, and infrastructure. Post-deploy
checks close that gap. They run against a shared system, so each one needs
explicit permission.

## Permission

Before the first post-deploy action, state the target, the operations, and
their effects, then get approval. Approval covers that target and run only.
Read-only checks still need the target named.

## Checks

- **Revision.** The deployed revision matches the candidate. The API and its
  migrations are deployed together, in the intended order.
- **Smoke journeys.** Run a short scripted set: liveness, one authenticated
  read, and one denial. Mutate only with dedicated test records, and remove or
  annul them afterward.
- **Telemetry.** Compare error rate and latency for the changed routes before
  and after the deploy.

Record post-deploy evidence separately from local evidence, with its own
target and timestamp.
