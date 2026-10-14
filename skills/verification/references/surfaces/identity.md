# Identity

Access bugs hide behind stubbed authentication. Give the agent a real local
identity, so the production verifier and the production permission path both
run.

## Local Identity

- Run the identity provider locally when the application validates tokens
  against it. Examples: a local Supabase stack, a Keycloak container, or an
  OIDC test server.
- Seed test users through the provider's admin API or its seed mechanism. Then
  add the application-side records that grant roles and tenancy.
- Mint tokens through the provider's normal grant, using test credentials from
  the project's seed files. Reuse one token per identity for the whole run,
  because local providers rate-limit sign-ins.
- A dev-only login path, such as a magic-login route or a static verifier,
  is acceptable for fast iteration only when it is gated at compile time and
  bound to loopback. Still run the real path at the gate.

## Identity Shapes

Seeded identities can differ in shape from real ones, for example in ID format,
claims, or the way they were created. Read how the production provider creates
identities, and give each real shape its own test identity. That includes legacy
or imported accounts. Code paths that validate identity fields fail only for
some shapes, and a single happy-path user doesn't reach them.

## Matrix

For every journey that changes access, check:

| Actor | Expectation |
| --- | --- |
| Permitted role, own tenant | Success and the durable effect |
| Wrong role | Denial and no state change |
| Wrong tenant or organization | Denial, and no data leaked through counts, lists, or errors |
| No token or expired token | 401 |

## Gotchas

- An application that resolves tenant or role from database rows, not from
  token claims, needs those rows seeded. A token alone isn't enough.
- Never mint tokens with a shared environment's signing secret. Use the local
  provider.
- A project's own token helper may load a local env file after reading the
  environment, so it can mint against a shared environment. Mint with a direct
  call to the local provider.
