# Retry and idempotency contracts

Use this reference for operations whose repetition can create duplicate effects.
Idempotency is a property to implement and verify, not a promise supplied by a
header or queue delivery setting.

## Define the caller's promise

- Identify one logical intent. A client may generate a random key once and reuse
  it for retries; generating a new key per attempt defeats deduplication. Distinct
  legitimate intents must have distinct keys.
- Scope keys to the correct caller or tenant and operation. Authorize duplicate
  requests before replaying results so the key cannot expose another user's data.
- Define which normalized request fields identify the intent. The same scoped
  key with a materially different payload must be rejected, not replayed silently.
- Choose the response for an in-flight duplicate: a documented conflict, bounded
  wait, or pending status with a way to check completion.
- Specify whether failures are retained, what a replay returns, and what happens
  after expiry. Retention must cover the longest supported retry/replay path,
  including offline clients and dead-letter queues.

## Close the failure windows

Claim an intent atomically with a unique constraint, conditional write, or an
equivalent store guarantee. A separate lookup followed by an insert can race.

An atomic claim alone does not make an external effect exactly-once. A process
can crash after the effect succeeds but before recording its result. Record
intent durably before calling out, distinguish success, failure, and unknown,
and define recovery for unknown outcomes. Depending on the system, use a shared
transaction, downstream idempotency, or reconciliation with the effect owner.
An outbox can preserve delivery intent but still needs duplicate-safe consumers.

Never treat a timeout or an expired worker lease as proof that the effect did
not happen. Do not blindly repeat an unknown operation. If ownership can move
between workers, account for the old worker completing after takeover.

## Evidence to seek

Test relevant cases through the actual boundary: sequential and simultaneous
duplicates, mismatched payloads, tenant isolation, crash windows, unknown outcomes,
recovery, and delayed replay. Show that distinct intents still produce distinct
effects. Use fault injection or controlled fixtures for crashes and timeouts;
document any guarantee the test environment cannot establish.
