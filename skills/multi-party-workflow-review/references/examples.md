# Review examples

These examples illustrate how to reason about handoffs. They are not universal product requirements.

## Approval rejection with a missing return path

Requirement: a requester can revise and resubmit a rejected request. The approver can reject with a reason, but the requester reader exposes only the original pending state and the edit endpoint rejects all submitted requests.

Trace rejection persistence, the requester DTO/reader, edit authorization, and UI action. The issue is the missing required return path, not merely an absent edit button. A useful finding identifies the rejected state, why the requester cannot recover, the connected source evidence, and the smallest complete repair. Verify that unauthorized users still cannot edit the request after the change.

## Cancellation accepted before a refund completes

The booking API accepts cancellation and schedules a provider refund. Both participants immediately see “refunded,” although no provider outcome has arrived. Inspect the authoritative requirement, durable refund state, provider callback/reconciliation path, and both readers.

If the contract distinguishes accepted cancellation from completed refund, the readers may be misrepresenting a pending outcome. A stubbed successful provider response does not verify real refund completion. If product policy is unclear, record the decision rather than inventing financial terms or a mandatory refund deadline.

## A manual support process is part of the product

Requirement: after a booking cutoff, cancellation requests go to support. The user can open a case, staff can see the booking and request, and resolution appears in the user's timeline.

The manual handoff is not inherently a defect. Inspect the supported path, permissions, ownership, and visibility. A missing staff view or unlinked case may break the accepted process; the absence of automatic cancellation does not. Do not add a new admin portal or automation merely to satisfy a preferred architecture.

## A claimed handoff cannot yet be tested

Source and local tests show a signed guest link can accept an invitation. The review lacks the external identity-provider sandbox needed for the subsequent account claim.

Report which link and ownership controls were traced or exercised, then mark the identity handoff unverified with the required sandbox check. Do not claim the whole journey passed, assert a vulnerability without a reachable boundary violation, or weaken authentication to finish the test.

## A single-user tool needs no counterparty

A local utility imports a file, transforms it, and saves the result for the same person. No requirement introduces a team, guest, reviewer, or staff workflow.

State that multi-party analysis is inapplicable and review only the requested task if useful. Do not generate merchant/buyer/admin screens or a cross-role matrix. The skill's value is finding required handoffs, not increasing the role count.
