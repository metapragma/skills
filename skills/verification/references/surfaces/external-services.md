# External Services

Email, SMS, payments, storage, registries, and other third-party APIs. Verify
the application's side of each integration without reaching real recipients,
real money, or production data.

## Stand-Ins, Most Real First

1. **Official local emulator.** For example, Supabase Storage, LocalStack, or a
   Stripe CLI test mode.
2. **Capture sink.** Mailpit for SMTP, or a request-capture server for
   webhooks. Assert on what the sink received.
3. **Recorded contract.** Replay a recorded real response. See
   [contracts.md](contracts.md).
4. **Hand-written fake.** Last resort. List it as a substitution.

## Rules

- Point every outbound integration at a stand-in before you enable its worker.
  Confirm where it points by checking the configuration and observing the
  traffic.
- Assert the outbound effect itself: the message body, the recipient, and the
  idempotency key. Also assert the application's record of sending it.
- Exercise failure paths: timeout, rejection, a duplicate delivery, then a
  retry that reaches success, and terminal failure.
- A "test mode" or "dry run" can still touch the network. Observe what it
  skips; don't trust its name.

## Gotchas

- Senders that require implicit TLS or authentication can't reach a plain
  local sink. Configure the sink to match, or record the path as blocked.
