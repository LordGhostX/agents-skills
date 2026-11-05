# Reviewer instructions

Adapt the assignment to the actual tools. Supply the pinned source/comparison, scope, requirements/tradeoffs, guidance paths, verified setup commands, scratch locations, resource ownership, primary emphasis, allowed checks, and limit. Share setup facts while reviewers inspect source and challenge assumptions independently; withhold others' findings and the implementer's conclusions during first-pass discovery.

## Worker contract

Try to disprove intended behavior through realistic caller/user flows. Read the complete assigned change and connected callers, tests, fixtures, configuration, and exports. Your emphasis does not exclude integration boundaries. Return all actionable defects the author would reasonably fix; keep stricter design preferences as optional suggestions. Continue after the first issue. Thorough coverage matters more than a long report, and no single pass guarantees completeness.

Size bounded reads and combined batch output to the enclosing tool's limit, not just nested command allowances. Recover truncated sections or disclose coverage gaps before claiming complete review. Reuse unchanged material already read.

Keep application source read-only and experiments in assigned scratch space. Do not alter another agent's snapshot, data, browser, server, or evidence; stage/commit/push; publish; change settings; or delegate without authorization. Report confirmed candidates promptly while finishing assigned coverage. Flag decisions and blockers without expanding permissions.

## Investigation priorities

- Trace consumers, persistence, errors, and recovery. Distinguish successful, empty, pending, unavailable, and failed states. Check assumptions in unchanged consumers exposed by new behavior and whether newly rendered controls actually work.
- For async work, examine freshness, deduplication, and caller ownership separately. Trace who may commit after replacement, cancellation, remount, or context changes. Equal values/IDs do not establish freshness after A-to-B-to-A transitions. Verify operation ownership and correctly targeted recovery.
- Check installed dependency contracts before recommending workarounds or labeling code unused. Assess readability, duplication, conventions, and unnecessary complexity for meaningful maintenance risk. Keep remedies proportional to the project while preserving explicit correctness, security, and accessibility requirements.
- For performance, identify realistic workload bounds, repeated work, I/O, rendering, pagination, fan-out, invalidation, and contention. Examine counter-evidence; measure meaningful claims with equivalent workloads and include cache/index/write costs. Large hypothetical inputs and green tests do not establish a performance defect or speedup.
- For security, name the actor, resource, required control, reachable boundary violation, existing controls, and concrete consequence. Missing best practices or guessed deployment conditions are not confirmed vulnerabilities. Stay within authorized execution boundaries.
- Read tests critically: independently specified expectations, consequential edge/negative cases, and sufficient lifecycle/context setup. Mocked internals, copied implementations, arbitrary counts, or incidental appearance assertions can give false confidence.
- For visible behavior, use approved app/browser checks when relevant. Exercise native pointer/focus, loading/failure/recovery, and affected layouts rather than relying solely on synthetic clicks or static styles. Other targets need appropriate runtime evidence, not an unnecessary browser session.

## Evidence and result

Use the smallest safe check preserving the mechanism; compare the relevant baseline when introduction is uncertain. For compatibility findings, name the affected consumer and demonstrate the breakage. Explain how a change newly exposes older faulty code. Separate unrelated existing problems from regression findings. Distinguish reproducibility, applicability, and frequency: a synthetic failure in a supported flow can confirm a defect without production examples; absence from sampled data doesn't refute it. Constructed cases still need evidence of reachability or a required contract. Do not promote fixture failures, timeouts, or missing catalog entries into defects without tracing their meaning.

Distinguish decisive source tracing, live integration, controlled transport, mocked behavior, and unattempted checks. Use native input for focus, controlled completion order for races, and real relevant session/interceptor paths for auth effects. Retain compact, non-secret evidence entries for confirmed findings: revision, decisive source trace or reproduction steps, expected/actual results, gaps, and links to retained artifacts. Runnable probes need prerequisites and commands, including how to recreate resources removed during cleanup. Test the claimed failure rather than a convenient approximation; mocked delivery recovery does not prove successful live uploads. Report snapshot findings with their versions even when the working copy has since changed, and never claim unavailable tools or models ran.

Present each finding with a priority-tagged imperative title and smallest relevant location/version. Use one concise, scenario-first paragraph for expected/actual behavior, consequence, causal link, and fix direction; link detailed evidence and state uncertainty. Cite the precise project rule when it adds substantive support; omit generic guidance citations. Leave product choices open. P0 means universal critical blocker, P1 urgent defect, P2 ordinary defect, P3 lower-impact actionable defect; label unconfirmed claims as such.

Conclude with actual coverage/checks and gaps. Keep optional suggestions and documentation drift separate from blocking findings. Say "No findings" when none qualify, bounded to your coverage; do not pad the result with generic advice.
