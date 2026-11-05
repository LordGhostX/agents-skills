# Goal mode

Work normally when goal tools are absent. Create a goal only on explicit user request; inspect an existing goal's objective before using it and never replace an unrelated one. Do not infer numeric token budgets. Follow actual runtime lifecycle/budget contracts.

An active goal does not bypass plan approval or pending scope/product decisions. Continue independent approved work while input is pending; otherwise report the dependency. Do not busy-poll, repeatedly ask, invent work, or manufacture status changes to force suspension.

Completion follows the approved mode: review-only can finish with defects reported; review-and-fix requires verified authorized corrections, integrated review, required checks, and accounting for accepted deferrals. Pending decisions are not accepted deferrals. Neither objective promises to find every bug.

Use the [iteration record](iteration.md#progress-and-resumption) to preserve scope, versions, assignments, decisions, evidence, and next steps across continuations. Inspect current source and agents on resume before repeating work. A narrower review's completion does not complete a broader goal.

Check available budget/progress before another wave; account for delegated work where observable and disclose gaps. Estimates are not hard aggregate limits. Reserve room for verification, cleanup, and handoff; do not silently extend limits or mark success because budget is nearly exhausted. Apply the [limit rules](iteration.md#limits-and-resources) to active reviewers too.

On an explicit pause, stop new work, halt owned delegates safely, checkpoint, and follow the runtime's pause contract. Never pause without the user's request, resume yourself, or misuse complete/blocked for ordinary waits; blocked requires the tool's actual conditions. System budget stops take precedence: report incomplete work and next steps.

Before completing a goal, compare the objective with actual reviewed versions, coverage, findings, and verification. Report unresolved items and material gaps. Goal mode grants persistence, not additional permission for commits, publication, or deployment.
