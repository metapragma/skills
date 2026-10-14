# Contracts

A contract is the shape that clients and providers agree on: OpenAPI, GraphQL,
protobuf, an event schema, or a typed client. Reading the spec beside the code
misses drift. Validating real responses catches it.

## Runtime Validation

- Validate every response the journeys produce against the spec: status codes,
  required fields, types, enums, and nullability. Run this inside the
  integration tests and the HTTP journeys.
- Validate requests too, when the service accepts what the spec rejects, or
  rejects what the spec allows.
- A mismatch is a finding even when the client tolerates it today.

## Consumers

When a contract changes, list its consumers and check each one:

- the frontend;
- other services;
- generated clients;
- external integrators.

A field that becomes required, or an enum value that is removed, breaks
existing clients. Record these changes as consumer-impacting in the evidence.

## Third-Party Providers

Record real provider responses once, with secrets redacted. Replay them as
contract fixtures. Re-record them on a schedule, or when the provider version
changes. A mock written by hand encodes what the author believed about the
provider, not what the provider actually returns.
