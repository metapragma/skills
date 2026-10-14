# Staged portable skills

These drafts are not installed. Nothing has been added to `skills/` or
`skill-sources.json`.

- `upstream/` contains untouched downloaded sources and upstream legal notices.
- `ready/deslop/` and `ready/test-audit/` contain self-contained adaptations.

Source: https://github.com/openclaw/openclaw

Commit: `91264b958cf11cda9b166fb134f22ca1c796c14c`

Downloaded: 2026-09-26

Original paths: `.agents/skills/deslop/` and `.agents/skills/test-audit/`.
Both adaptations retain the upstream MIT license and source attribution.

## Portability changes

### Deslop

- Discover the comparison base instead of assuming `origin/main`.
- Support explicitly requested uncommitted changes.
- Remove Oxlint assumptions and the required `autoreview` dependency.
- Preserve behavior-neutral cleanup and report uncertain behavioral changes.
- Use the target repository's validation commands.

### Test Audit

- Preserve the four-question authoring gate, low-value patterns, retention
  criteria, candidate evidence, and before/after verification.
- Replace Vitest, OpenClaw CI scripts, directory layouts, and mandatory skills
  with repository-native discovery and validation.
- Omit campaign mode and its orchestration, merge policy, and Telegram examples.
  The original `CAMPAIGN.md` remains in `upstream/` for comparison.
- Remove deletion/LOC incentives and automatic publication or continuation.
- Treat test-only dependency injection and static tests as design questions,
  rather than categorically rejecting them across all codebases.
- Keep review-only requests read-only and preserve independent contracts before
  deleting tests.

No executable code was imported. These are locally maintained adaptations;
future upstream updates should be reviewed rather than copied over the drafts.
