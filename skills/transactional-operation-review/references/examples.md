# Review examples

Use these to choose focused evidence. They do not certify any application or provider integration.

## Commit succeeds; result delivery fails

A reservation service commits the booking and operation result in one database transaction. Writing a Redis response cache then fails. The retry first loads the committed operation and returns its stored booking reference after authorization.

The cache failure alone is not a duplicate-booking defect. Verify the fallback is reachable and the operation result corresponds to the committed booking. As a contrasting case, if retry checks only Redis and inserts a new booking after the cache miss, reproduce the interruption and inspect both booking rows and operation identity. Recommend repairing that window rather than requiring a replacement queue architecture.

## External outcome is unknown

A fulfillment request times out. The worker marks it failed, deletes its operation claim, and generates a new provider key on retry. The provider may already have accepted the first request.

Check the provider contract and operation trace. A controlled accepted-but-response-lost transport can demonstrate local retry behavior, but cannot prove a real provider's deduplication semantics. Preserve the original provider identity and use supported lookup/reconciliation before a second effect. If no provider mechanism can establish the outcome, report that limitation and the product's recovery decision; do not invent an exactly-once guarantee.

## A lease expires while work is paused

Worker A acquires a lease with random token A, then pauses. Worker B acquires a replacement and performs an effect. A resumes and performs another effect; its compare-and-delete release correctly refuses to delete B's lease.

Safe release did not prevent the stale effect. Inspect what the actual resource/provider enforces. Conversely, if both attempts use a provider-supported durable operation identity that deduplicates within the relevant scope/window, do not label the lease alone a confirmed duplicate-effect defect without tracing that counter-evidence.

## Retry identity is too broad or too short-lived

- A tenant-neutral response cache uses only a client key. Determine whether a different authorized caller can receive the original private result; trace authentication and lookup, not just the key's spelling.
- An offline queue serializes the intent but generates a new operation key after restart. Check the persisted record and restart/retry behavior for the same intent. A new intentional purchase must still be distinguishable.
- Notification identity uses only entity ID and event type. A second legitimate approval request on the same entity is dropped. Reuse occurrence identity for delivery retries, while assigning a distinct identity to the new request.

## Precision and proportionality

For an API accepting integer values beyond a consumer's exact numeric range, round-trip a supported boundary value through the actual parser/serializer and arithmetic path. A database bigint and a decimal-looking UI do not prove exact transport. If the API enforces a safe range, account for it before recommending a wire-format migration.

A small local counter updated under an appropriate database transaction may already meet its requirements. Do not prescribe a distributed lock, financial ledger, outbox, or additional state machine without a concrete failure that the current design cannot handle.
