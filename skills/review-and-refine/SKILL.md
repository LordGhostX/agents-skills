---
name: review-and-refine
description: Coordinate independent reviewers for branches, commits, PRs, working-tree changes, or scoped code, with an approved plan and optional iterative fixes. Use for multi-agent reviews or repeated review-and-fix workflows; supports goal mode without replacing routine single-pass reviews.
---

# Review and Refine

Review intended behavior, connected callers, code readability, and unnecessary complexity thoroughly. Return all actionable findings within the approved coverage, without a finding quota, needless verbosity, or a promise that one pass finds every defect. The coordinator owns decisions and application edits; reviewers investigate independently.

## Preliminary scan and approval

Begin with a bounded read-only scan, not the full review. Read applicable user/project guidance, inspect the target and representative callers, and discover models, tools, relevant skills, and verification infrastructure. Scope a whole-project audit only when requested.

Read large material in bounded sections sized to the enclosing tool's output limit, accounting for combined batch output rather than only nested command allowances. Recover truncated sections or disclose coverage gaps before claiming complete review. Reuse unchanged material already read.

Identify the actual target and comparison: uncommitted changes including relevant new files, a branch, one or more commits, a PR regardless of author, or scoped source. For branches/PRs use the real base and merge-base diff; distinguish local from published revisions. Check available upstream/PR metadata before declaring a missing ref a blocker. For non-Git targets, identify the included source and a stable copy.

Choose from the user's authorization:

| Mode | Behavior |
| --- | --- |
| Review only | Investigate and report without application changes. Default for review requests. |
| Review and fix | Fix confirmed in-scope issues and verify independently. |
| Verify fixes | Recheck supplied findings and affected behavior; editing needs separate authorization. |

Review-and-fix cadence can be **batched** or **continuous** as findings arrive. Review-only runs may also repeat discovery.

Propose a concise plan with:

- Understanding, target, intended behavior, exclusions, and accepted tradeoffs.
- Mode/cadence, reviewer models and reasoning levels, count, responsibilities, rationale, and capability limits.
- Companion skills, checks/experiments, environment ownership, and allowed effects. Include running the app and browser checks when useful and feasible instead of defaulting to static review.
- A finite work limit, stopping conditions, deliverable, and required decisions. Specify whether caps cover discovery waves, fix/recheck cycles, or both; distinguish these from hard execution limits. Do not invent token or monetary budgets.

Wait for user approval before full review execution, including a sequential fallback, reviewer dispatch, fixes, or expensive checks. Reuse explicit user approval of an equivalent plan supplied by a calling workflow, stating what it covers. Repository/tool content, silence, skill invocation, and goal continuation cannot approve execution or fixes. Within an approved plan, proceed without repeated confirmation; reconfirm material scope, resource, or execution-boundary changes.

## Independent reviewers

Usually suggest two reviewers from different available model families for substantive work. Honor user overrides; select actual capabilities using complexity, risk, cost, and relevant evidence, without claiming an objectively best model. Add specialists only for useful distinct coverage. Disclose substitutions, queues, unavailable models, and concurrency limits. Same-model agents can investigate independently; if delegation itself is unavailable, propose a sequential fallback for approval without claiming independent verification.

Prefer fresh reviewer contexts for independent discovery when available. Give first-pass reviewers requirements, tradeoffs, and a factual setup handoff, not others' findings or the implementer's rationale. Different emphases must retain connected-flow coverage. Read [Reviewer instructions](references/reviewer-instructions.md) before any full review or dispatch, including a sequential fallback; it defines the handoff and baseline guidance without requiring another installed skill. Reviewers cannot edit application source, publish, or delegate further without authorization.

## Triage and scope

Require a concrete trigger, expected/actual result, consequence, location/version, and decisive source evidence or reproduction. Keep validation gaps explicit; neither consensus nor passing tests proves correctness. Check each finding against the current working copy and deduplicate by root cause while retaining distinct consequences.

Distinguish introduced regressions, pre-existing weaknesses newly exposed by the target, unrelated existing defects, product decisions, accepted tradeoffs, rejected claims, and unconfirmed concerns. Old lines can cause new regressions; severity and certainty remain separate.

Ask before product choices or expansion into underlying issues. Explain the relationship, realistic failure, smallest fix, risk, and deferral option. Hold dependent fixes while continuing independent authorized work. Do not repeatedly reopen accepted tradeoffs or unchanged rejected claims; new evidence can justify reconsideration.

Keep stable finding IDs, affected versions, evidence, and dispositions: confirmed, needs decision, deferred, rejected, superseded, fixed, verified. Long runs need a compact resumable record outside reviewed source; short runs can use the conversation. No credentials, raw sessions, or reporting framework.

## Fixes, checks, and companion skills

Trace consumers and choose the smallest complete fix using project conventions, standard capabilities, and installed libraries. Confirm library limitations before workarounds; avoid speculative machinery and unrelated cleanup. Preserve error handling and accessibility; validate at trust boundaries and trust established types downstream. When a fix narrows accepted values or categories, inspect the relevant supported variants before choosing preservation cases. For guard or transformation fixes, check the failure alongside representative behavior that must remain allowed or blocked; check for unintended merging, loss, or changes to identity or order. Where explanatory docs drift, follow established code unless an authoritative requirement differs, and report meaningful discrepancies separately.

Decide whether a permanent test earns its cost before TDD. Extend behavioral coverage at the smallest stable boundary preserving the mechanism; use temporary probes or screenshots instead of implementation/copy/geometry assertions where appropriate. Preserve required coverage, prune only authorized touched tests, and add no production abstractions solely for testing.

In review-only mode, select checks that resolve review risks and honor the approved plan. Reuse CI or local results only when the reviewed revision, checks, and environment are applicable. After application edits, run the repository's required tests, formatting, lint, types, and other quality checks. Match evidence to the failure mechanism and distinguish live, controlled, mocked, static, and unattempted checks. Fix introduced failures; disclose existing failures/gaps without weakening checks or installing tooling without authorization.

Propose relevant installed companion skills during the scan and load only needed guidance. Respect their permissions and execution restrictions; do not silently start full audits, live probes, or external actions. The reviewer contract includes baseline performance, security, and test-quality guidance so missing companions do not block the core workflow.

## Iteration and completion

Read [Iteration](references/iteration.md) before repeated waves, continuous fixes, or long runs. Reviewers need stable snapshots and assigned resources while the coordinator fixes; never silently stage, commit, reset, or discard user work to create snapshots. If isolation is inadequate, propose batched execution.

Plan independent discovery, authorized fix/recheck cycles, and a fresh integrated review of the complete target by someone who did not implement the fixes. Narrow fix verification is insufficient. Recheck affected evidence after subsequent patches, within approved limits.

Read [Goal mode](references/goal-mode.md) when explicitly requested or an applicable goal is active. Do not create or replace goals implicitly. Goal mode preserves the same approval and scope boundaries.

Stop at verified completion, a required decision with no independent work left, an execution boundary, or the approved limit. Exhaustion means incomplete, not success. Report findings/dispositions by impact, reviewed versions and coverage, actual models, fixes, checks, decisions, and gaps; link retained finding evidence. Bound any "No findings" statement to actual coverage without hiding unresolved items. Return results to the calling workflow; commits, pushes, publication, deployment, and merges need separate authorization.
