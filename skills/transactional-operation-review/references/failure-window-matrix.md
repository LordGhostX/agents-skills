# Failure-window matrix

Use rows relevant to the operation. Prefer an existing operation record or database constraint that already provides the required guarantee over new machinery. The table describes questions, not a required implementation.

| Boundary | What to establish | Failure/retry question |
| --- | --- | --- |
| Before accepting intent | Caller authority, resource scope, input binding, identity origin | Can another actor replay private data or reuse a key for a different effect? |
| After accepting, before effect | Durable intent or a proven no-effect state; work ownership | If execution stops here, can recovery find the operation and distinguish it from a new intent? |
| During local mutation | Transaction/constraint behavior and recoverable outcome | Can the business change commit while retry logic concludes nothing happened? |
| Before sending externally | Persisted provider identity, destination/account scope | Can a restarted worker issue the same intent under a different provider identity? |
| After send, before response | Provider contract, lookup/reconciliation, pending state | If the response is lost, what proves whether the effect happened? |
| After commit, before response/cache | Durable result or a way to reconstruct it safely | Does failed delivery cause a second mutation or recover the existing result? |
| After lease/claim expiry | What rejects stale effects at the protected resource | Can the old worker still act after a replacement begins? |
| During delayed retry | Identity retention, provider retention, terminal-state policy | Does an expired key accidentally turn old uncertain work into a new operation? |
| After a later valid event | Immutable occurrence identity and consumer deduplication | Are retries suppressed without suppressing a new valid transition? |

For each investigated window retain:

- **Setup:** revision, operation, accepted behavior, relevant state and caller authority.
- **Sequence:** the exact interruption/completion order and retry entry point.
- **Evidence:** source locations, probe/check command and prerequisites, durable state, returned result, external evidence if available.
- **Conclusion:** established behavior, consequence, applicability, and unverified boundaries.

Redact credentials and unnecessary personal data. Keep probes isolated from user work. Unknown external outcomes remain unknown until an authoritative observation or reconciliation policy resolves them; a local exception or elapsed timeout is not that observation.

## Implementation-specific contracts

Check the project's actual dependencies and provider documentation before recommending changes. These primary references illustrate why assumptions need verification; they are not required technologies:

- [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) explains ownership-safe release, timing assumptions, and fencing considerations. A lock-release token is not proof that the protected resource rejects stale writes.
- [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests) documents API-specific replay and retention behavior. Do not generalize one provider/API version's guarantees to another or assume indefinite deduplication.
- [JavaScript safe integer range](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER) explains why a full-range integer storage type does not by itself establish exact client arithmetic.

Recheck the current contract when applying these references. A source link supports a platform rule; it does not establish that the reviewed application uses that rule correctly.
