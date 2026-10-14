# Library

The surface of a library is its public API, as a consumer calls it.

## Checks

- **Public API only.** Test through exported entry points. Test-only exports of
  internals check the implementation, not the contract.
- **Consumer build.** Build a minimal consumer project against the packaged
  artifact, not the source tree. This catches export maps, missing files, and
  type declarations that tests run from the source tree miss.
- **Supported matrix.** Cover the language and runtime versions and the
  platforms the package claims to support.
- **Properties.** For parsers, encoders, data structures, and numeric code, use
  property-based tests: round-trips, invariants, and comparison with a simple
  reference implementation.
- **Compatibility.** When a public signature or behavior changes, compare it
  with the last released version, using an API-diff tool if the ecosystem has
  one. Record breaking changes.
