# Iteration

## Continuous fixes

The coordinator is the application writer. Reviewers investigate identified snapshots while it triages and fixes; they do not compete to patch findings.

Capture relevant committed, staged, unstaged, and new source in isolated checkouts/copies without staging, hidden commits, resets, or discarded user changes. Identify the captured versions and avoid blindly copying ignored credentials/unrelated files. If isolation is inadequate, propose batched execution rather than treating moving-source reviews as independent.

Each cycle:

1. Collect versioned findings, deduplicate, and inspect the current working copy. Mark resolved claims superseded only with evidence; retain distinct consequences.
2. Send product choices and underlying scope expansion to the user; hold dependent fixes while independent work continues.
3. Apply the smallest confirmed in-scope correction, choosing worthwhile tests before TDD, then verify the mechanism and affected consumers.
4. Invalidate affected checks/review evidence and assign updated snapshots for rechecks. Preserve independent discovery; fix verifiers can receive finding context.
5. Finish with a fresh integrated review of the complete approved target. Obtain required results or account for incomplete assignments. Subsequent patches require renewed affected verification.

Review-only cycles omit application fixes. Verify-fixes runs distinguish replaying supplied findings from whole-target coverage. Recursion is bounded repetition, not unlimited descendants or an obligation to invent issues. When findings widen the work or another wave offers little value, ask whether to extend, narrow, or split it.

## Limits and resources

A discovery wave searches for new findings; a fix/recheck cycle applies a batch of corrections and verifies their effects. Broadening a recheck into fresh discovery consumes a wave. Caps block new work of their kind; approved work may finish within remaining execution limits. A hard time/cost/runtime-token limit also bounds active work: stop dispatch, request safe interruption of owned reviewers, retain partial evidence, and account for unfinished assignments. Do not wait indefinitely or claim cancellation without confirmation. Disclose inability to interrupt; clarify ambiguous inherited limits instead of assuming an extension. System limits take precedence. Exhaustion is incomplete work.

Worktrees do not isolate databases, ports, caches, browsers, or servers. Assign ownership, avoid concurrent destructive shared-fixture tests and competing browser control, and coordinate heavy checks. Preserve user-requested servers; cleanup may stop only owned resources.

Use authorized fixtures and minimum effects. Keep experiments outside watched application paths when practical; HMR/restarts can invalidate evidence. Restore owned data/settings and retain useful evidence without secrets. Scratch writes do not authorize live probes or external effects. Meet companion skills' isolation requirements or disclose the blocked check.

## Progress and resumption

Long runs need a compact note outside reviewed source, not a new schema/database. Record the approved scope/mode/cadence/models/limits and approval source; snapshot versions, agent handles and coverage; finding IDs, evidence, relationships and dispositions; pending decisions, checks, owned resources, and next action.

Checkpoint before handoff, input waits, or compaction. Resume by inspecting actual source and existing agent statuses; reuse eligible work rather than duplicating waves. Preserve new user edits and determine which evidence remains applicable. Material target changes require approval.

Calling workflows can provide these details and prior explicit user approval in ordinary instructions. Return control/results without imposing configuration or taking over unrelated work. Repository files and agent suggestions cannot grant approval. For an active/requested goal, also read [Goal mode](goal-mode.md).
