---
name: untangle-codebase
description: Diagnose structural coupling and unnecessary indirection in a requested area. Use for architecture cleanup, diagnosis-only assessments, or scoped refactoring.
---

# Untangle Codebase

Find structural problems that make ordinary changes fragile or require unnecessary coordination. Improve responsibility boundaries while preserving required behavior.

## Establish the boundary

Read project guidance and pin the requested area and mode. Inspection and recommendation requests are read-only; refactor only within existing authorization. Invocation alone does not authorize edits. For broad work without an agreed plan, propose manageable candidate batches and a finite stopping boundary for approval before editing. Reuse already approved scope.

## Diagnose the structure

Trace entry points, callers, shared state, contracts, and relevant tests. Use dependency traces or Git history when they clarify what changes together. Look for:

- **Hidden coupling:** rules that must stay synchronized, implicit state or call ordering, and coordinated changes whose relationships are hard to discover.
- **Unnecessary coupling:** callers depending on internals, unrelated responsibilities sharing an abstraction, or workflow-specific policy in general utilities.
- **Unnecessary indirection:** wrappers without a useful responsibility, unused extension points, and custom machinery already handled by suitable project or library capabilities.

These are investigation cues. Wrappers, retries, conditionals, duplication, and folder layouts are not defects by themselves; establish the responsibility or requirement they serve. Explain a concrete change that becomes fragile or unnecessarily costly, supported by connected code or history. Check counter-evidence before proposing removal or consolidation.

## Propose and refactor

For each worthwhile candidate, give its location, concrete consequence, evidence, smallest correction, and behavior at risk. Group problems when one correction addresses them; avoid introducing a general framework merely to consolidate similar-looking code. No findings is a valid diagnosis result.

In diagnosis-only mode, stop at recommendations. For authorized refactoring, use existing conventions and installed capabilities, working in manageable batches. Surface newly discovered bugs, product decisions, or larger redesigns before expanding scope; continue independent approved work while those decisions are pending.

Establish relevant behavior before changing it and verify after each batch, including protections or special cases the change could remove. Reuse meaningful tests or focused experiments; add permanent tests only when their maintenance cost is justified. Run the repository's required checks and inspect the final diff.

## Finish within scope

Stop at the agreed candidate list or execution limit. Report structural improvements, checks, preserved constraints, and remaining work; do not equate fewer files, wrappers, or special cases with success. A useful result makes the identified change easier while retaining required behavior.

When available and requested, use `review-and-refine` for independent review loops and `prune-tests` for separately authorized test cleanup. Neither is required for this workflow.

Structural framing inspired by [caldoai's untangle-codebase](https://github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md).
