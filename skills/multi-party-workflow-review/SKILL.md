---
name: multi-party-workflow-review
description: Review a feature across participating users, counterparties, and operational roles to find missing next actions, visibility, or recovery paths. Use for cross-role workflow completeness and scoped fixes, not a general code review or a requirement to add more personas.
---

# Multi-Party Workflow Review

Check whether each participating actor can move the requested workflow toward its agreed outcome, observe the result, and recover from applicable failures. Individual screens or endpoints working in isolation do not establish that the handoffs between actors work.

## Establish the intended flow

Read project guidance and identify the requested feature, reviewed revision, authoritative requirements, relevant actors, and accepted tradeoffs. Derive actors from the product; do not prescribe guest, organization, finance, or admin roles. A single-user utility may need no multi-party analysis.

Use requirements and connected implementation to distinguish missing behavior from an unresolved product choice. Reuse prior decisions. Ask only for missing decisions that materially change the conclusion while continuing independent review. Inspection is read-only; fixes require existing authorization for the affected scope.

## Follow the handoffs

Trace the initiating actor through the durable state change and each affected actor's next action. Follow actual routes, guards/policies, jobs, data readers, UI controls, and relevant tests rather than judging a screen inventory alone.

For each applicable transition check:

- **Authority and ownership:** who may act, on which resource/version, under which state and organization context? Can an action be reached through a supported path and is the server boundary enforced?
- **Visible result:** what does the initiator see, what does the counterparty see, and how do they distinguish pending, completed, rejected, cancelled, unavailable, and failed outcomes?
- **Next action:** who owns the next step, can they actually perform it, and does their result become visible to the other participant? A displayed button without a usable operation is not a completed handoff.
- **Recovery:** when applicable, trace rejection, revision, expiry, cancellation, repeated submission, failed delivery, and staff intervention. Check the real policy; not every transition needs reversal or every product needs automated recovery.
- **Async completion:** separate request acceptance from completion. Inspect durable work and freshness of readers; a notification is not itself proof that the underlying operation completed. Check notification behavior only where the requirement or supported user path depends on it.

Use the [workflow matrix](references/workflow-matrix.md) for a retained map or requirements-to-evidence deliverable. Read the [examples](references/examples.md) when distinguishing a defect from an accepted manual process or a verification gap. Load only the material useful to the current feature.

## Test the boundary that could fail

Select a representative supported journey and consequential recovery paths, proportional to the feature. Use existing tests and permitted runtime checks; preserve real application authorization and state transitions when they are the mechanism under review. For UI issues, exercise actual navigation, controls, and observable state when available. Static source traces or controlled fixtures remain useful evidence with explicit limits.

Observe both sides of the handoff. A successful initiator request, isolated screenshot, or mocked notification alone cannot show that the counterparty can complete their next step. If access, a provider sandbox, or an operational role is unavailable, record what remains unverified rather than inventing results or adding access bypasses.

## Report within scope

Return the workflow/revision, participating actors, completed handoffs, actionable defects, accepted manual processes/tradeoffs, unresolved product decisions, and verification gaps. Link findings to the affected transition and decisive evidence: trigger, expected/actual behavior, consequence, and smallest correction.

Do not equate an undocumented screen with a missing requirement or prescribe an entire new role suite. No findings is valid within the reviewed coverage. After authorized fixes, check the affected actors and recovery paths together, run applicable repository checks, and inspect the diff. Stop at the agreed feature or execution limit; do not silently expand into a redesign, independent-review campaign, or publication workflow.
