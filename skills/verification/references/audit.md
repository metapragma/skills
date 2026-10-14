# Audit Mode

Keep a project's verification paths honest as the code changes. Compare the
config, the commands, and the journeys with the source and with live behavior.
Then correct any proven drift. Reading the source alone can't establish a
clean result.

## Scope

Edit only these:

- the project config;
- the journey files;
- the project's verification tool and its journeys.

Product code, shared test tooling, requirements, and CI settings are outside
this mode's scope. When the user asks for an audit without fixes, keep every
file read-only and report the corrections you propose.

## 1. Pin the Target

Record:

- the revision, plus any uncommitted changes;
- the config contents;
- the list of journeys and commands you are auditing.

Recheck affected findings if relevant code changes while the run is in
progress.

## 2. Compare With Source

Account for every journey and every command in scope.

- Look for journeys that are missing, duplicated, or dead. Check each one
  against the source entry points: routes, commands, and schemas.
- Inspect recent changes for new user paths that the config doesn't cover yet.
- When the implementation, the tests, and the requirements disagree,
  investigate the conflict. The newest code isn't automatically the intended
  behavior.

## 3. Run Live

1. Run doctor.
2. Run up.
3. Drive each journey in scope.
4. Run down.
5. Confirm the evidence is still there.

Mark each journey `passed`, `failed`, `blocked`, or `not run`. Run doctor again
after anything unexpected. You may correct a defect in a project-owned helper
and retry it once. If the journey is still blocked after that, record the
prerequisite and continue with the safe, independent journeys.

## 4. Classify and Correct

- **Recipe drift.** The config disagrees with established intended behavior.
  Correct the config, then rerun the affected journeys.
- **Helper gap.** The product works, but a helper can't drive or observe it
  reliably. Repair the helper, confirm that it still signals failure, and run it
  live.
- **Product regression.** The product fails a journey whose expectation is
  right. Preserve the reproduction and report it. The expectation stays as it
  is.
- **Unresolved intent.** The evidence doesn't show whether a change was
  intended. Keep the discrepancy visible and ask.
- **Missing prerequisite.** Record the journey as blocked, not as passed.

Edit a recipe only where it misled a run or contradicts the source. Leave
recipes that work as they are; changing them causes churn.

## Report

Report corrections and coverage separately. Coverage is complete only when
every in-scope journey passed on the recorded revision. Otherwise, list each
failure, each blocker, and each journey that didn't run. Also report product
regressions, unresolved intent, and the cleanup outcome.
