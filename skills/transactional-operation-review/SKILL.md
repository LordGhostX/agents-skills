---
name: transactional-operation-review
description: Review retried or asynchronous side effects for duplicate execution, lost results, and unsafe recovery. Use for payment, fulfillment, queued mutation, or similar operation correctness reviews and authorized fixes; not a general performance or security audit.
---

# Transactional Operation Review

Trace one logical intent through retries, persistence, external effects, and recovery. Find where the same intent can cause another effect, a committed result can be lost, or a legitimate later intent can be suppressed. Judge the actual guarantees and supported workload rather than requiring a particular database, queue, or lock design.

## Establish the operation

Read project guidance and identify the requested operation, reviewed revision, expected effect, actors, and accepted retry/recovery policy. Review requests are read-only; apply fixes only within existing authorization. Keep unrelated architecture changes separate.

Locate the caller, authentication/authorization boundary, identity generation, durable state, worker/provider call, result storage, response, and recovery entry points. Include offline queues only when they carry this operation. For simple bounded work, inspect the relevant path without expanding into a system-wide financial audit.

## Check identity and authority

- Determine what identifies one intent and where that identity survives client retry, worker restart, app restart, or rescheduling. A new user intent needs a new identity; retrying an uncertain operation must not silently create one.
- Check the actual isolation boundary: principal, tenant, operation type/route, and provider account where applicable. Authenticate and authorize before effects or disclosure of replayed results. For webhook/system actors, verify their own credentials and resource scope rather than imposing customer authentication.
- Inspect how effect-relevant input is bound to identity. Reusing an identity with changed input must follow the documented conflict policy; canonicalization must not discard meaningful distinctions.
- Check retention against supported retry and reconciliation windows. Expired cache entries, leases, or provider keys are not evidence that no effect occurred.

## Trace failure and recovery

Read the [failure-window matrix](references/failure-window-matrix.md) when checking asynchronous work, external effects, or crash recovery. For each applicable boundary, establish what can already have committed, what survives failure, and how a retry decides whether to replay, resume, reconcile, or reject.

An authoritative record or equivalent durable constraint must support the claimed deduplication. Inspect how business changes and recoverable outcomes stay consistent; a response cache alone is insufficient evidence. An external service does not join a local database transaction merely because the call occurs inside it. Verify the provider's actual idempotency scope, retention, replay, lookup, and failure contracts using current primary documentation and configured API versions when those details affect the conclusion.

Distinguish a lease ownership token, which can protect release, from a fencing value actually enforced by the resource. Trace stale workers after lease expiry; checking ownership before an unprotected effect can still leave a race. Inspect durable claims, provider deduplication, or resource checks rather than assuming a finite lock guarantees one effect.

For notifications/events, distinguish retries of one occurrence from a later valid occurrence. For exact quantities, check the accepted range and representation across request, storage, response, and consumer arithmetic; preserve the documented contract rather than prescribing a universal wire type.

## Validate and report

Use the smallest permitted check that preserves the mechanism: controlled completion order, injected failures, persistent-state inspection, contract tracing, or provider sandbox checks where available. A successful HTTP status does not establish one committed effect. Record final business state, operation state, and external result where relevant. Separate source reasoning, controlled doubles, real local integration, and live provider evidence.

Use the [examples](references/examples.md) when choosing a failure case or checking whether a recommendation is proportional. They are illustrative inputs, not defects to assume in every implementation.

Report the reviewed operation/revision, applicable failure windows, concrete findings, smallest corrections, accepted tradeoffs, and verification gaps. A finding needs a reachable sequence, expected/actual behavior, consequence, and decisive evidence. Missing infrastructure is a verification gap, not proof of a defect. No findings is a valid result bounded to actual coverage.

After authorized edits, verify both the failure case and legitimate retries/new operations, run applicable repository checks, and inspect the diff. Stop at the agreed operation scope or execution limit. Do not install tooling, call live providers, publish, or redesign surrounding systems merely because this skill is invoked.
