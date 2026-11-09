# Workflow and evidence matrix

Use one row per meaningful transition or handoff, combining fields or omitting inapplicable ones for small reviews. This is a working aid, not a required reporting framework.

| Actor / resource | Trigger and precondition | Authorized transition | Initiator result | Counterparty visibility and next action | Failure / recovery owner | Evidence and status |
| --- | --- | --- | --- | --- | --- | --- |
| Requester / approval request | Submit a draft in their workspace | Draft to awaiting approval | Pending request reference | Assigned approver sees the request and may approve or reject | Requester can see validation failures; delivery retry owned by the documented process | Source trace, test or observed journey; state the actual evidence level |

Derive further rows from the feature's requirements, including recovery handoffs that materially affect completion. Avoid inventing mandatory roles, pages, wallets, channels, or state transitions.

## Evidence notes

Retain the requirement/decision source, reviewed revision, relevant route/control/state locations, check prerequisites, and observations on both sides. For confirmed defects, record a reachable sequence and distinguish the required result from an inferred preference.

Useful dispositions:

- **Verified within coverage:** the stated check establishes this handoff under the tested conditions.
- **Confirmed defect:** source or runtime evidence establishes a required reachable handoff fails.
- **Accepted tradeoff:** the authoritative requirement explicitly accepts this behavior; record the owner or decision source.
- **Needs decision:** evidence cannot determine what the product should do.
- **Unverified:** a required check could not be performed; name the missing prerequisite and what evidence would resolve it.

Do not turn missing runtime access into a defect, or turn passing tests for one actor into verification of all actors. Distinguish mocked transport, real local persistence, source tracing, browser observation, and live provider behavior.

## High-value boundary questions

- Can the assigned actor discover the pending work with their actual permissions and workspace context?
- Does a revision/rejection/cancellation expose the reason and supported next action where required?
- Does refreshing or reconnecting preserve pending versus completed state and avoid showing stale actions as valid?
- Can a guest capability, staff action, or account-claim handoff reach the intended resource without broadening access? Apply these only if the feature has such a path.
- If a manual recovery path is accepted, who owns it, what context is available, and how is resolution communicated?
- Are asynchronous confirmations reflected in the durable state and readers used by all affected actors?

For requirements-to-evidence reviews, add requirement IDs to the relevant rows. Keep uncovered requirements explicit; a matrix with every cell filled is not proof of implementation completeness.
