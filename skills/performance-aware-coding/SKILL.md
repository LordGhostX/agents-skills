---
name: performance-aware-coding
description: Use during implementation or review when changes touch repeated work, growing data, rendering, I/O, persistence, or resource use, and when investigating a performance issue. Provides stack-neutral cost analysis, on-demand ecosystem research, and evidence-based validation.
---

# Performance-Aware Coding

Help prevent avoidable performance costs while preserving behavior. Apply a brief cost check when a change touches work that repeats, sits on a latency-sensitive path, or grows with data or traffic. Do deeper investigation when the user asks for it, the code or workload suggests material impact, or evidence points to a bottleneck. This guidance applies across interactive UI, APIs, data access, background work, command-line tools, and other runtime paths; do not divide the method by language or framework.

## Choose the right depth

- **While implementing a feature:** inspect the affected path and do a quick cost pass. Call out or change a concern only when there is a concrete mechanism and a plausible impact; don't turn routine work into a performance audit.
- **When investigating or reviewing performance:** map the path and workload, use measurements or the smallest useful diagnostic to locate the bottleneck, rank candidate fixes, and validate the result.
- **When there is no concrete issue:** say so briefly when relevant. No findings is a valid result; do not generate generic advice to fill space.

## Understand the path and workload

1. Read applicable repository instructions. Inspect the changed code, its entry point, immediate callers, and the next relevant operations. Keep the investigation scoped to the path that could carry the cost.
2. Locate where the work runs: for example, once per page load, interaction, request, record, retry, batch, or scheduled job. Note whether it is user-blocking, on a shared resource, or off the critical path.
3. Use repository evidence to understand bounds and workload: collection sizes, page limits, payloads, request rates, concurrency, refresh frequency, existing performance budgets, telemetry, and benchmarks. Ask the user only for missing information that could materially change the recommendation; otherwise proceed and label the uncertainty.
4. Name the performance objective that matters for this path. It may be response or interaction latency, tail latency, throughput, CPU, memory, allocations, I/O, query count, payload size, startup time, or another concrete measure. Avoid optimizing a proxy that does not represent the user's goal.

## Research the actual stack as needed

- Identify the runtime, framework, dependency versions, data stores, providers, and build tools from manifests and actual call sites. Do not assume an API, execution model, cache behavior, or performance characteristic based on familiarity with another stack.
- When a decision depends on a library or runtime detail, inspect the installed version's types, implementation, and current primary documentation. For profiler commands and platform behavior, look up the current tool guidance for the project in front of you.
- Prefer tools already configured in the repository. Choose a profiler or trace that can answer the question at hand; do not install dependencies or add instrumentation merely because a tool is commonly used.
- Use general performance principles first, then translate them into the detected stack. Do not preload or reproduce separate language playbooks when targeted research can resolve the specific question.

## Look for concrete costs

These are cues for inspection, not findings on their own:

- **Repeated work:** a full scan, sort, normalization, parse, date/string formatting, conversion, or serialization repeated for each item; nested loops or repeated lookups whose cost grows with the input.
- **Chatty I/O:** a query or network/provider call inside a per-item loop, duplicate reads, one update per record, repeated setup/probe calls, or sequential request dependencies that create a waterfall.
- **Excess data movement:** cloning or copying large values, repeated encoding/decoding, rebuilding equivalent objects, transferring fields the caller does not use, or expensive work on a UI/main thread or request path.
- **Unbounded work:** missing pagination or limits, unbounded buffers or queues, excessive retries, uncontrolled fan-out, or work that grows with input size without a justified bound.
- **Contention and waiting:** lock or pool contention, blocked event loops or threads, serialized independent operations, and background work competing with critical paths.
- **Frontend delivery and interaction:** repeated data fetches, avoidable waterfalls, oversized assets or bundles, expensive render/update work, layout or main-thread blocking, and work done before it is needed.
- **Backend request and data paths:** N+1 access patterns, repeated provider calls, poor query shapes, unnecessary setup work, oversized responses, and expensive per-request computation.

For each candidate, connect the code location to its repetition or growth, where it sits in the path, and the workload under which it matters. Check for counter-evidence such as small enforced limits, existing memoization, batching, caching, lazy loading, or a library that already performs the work.

## Select a proportionate fix

- Prefer removing unnecessary work and fixing algorithmic or structural causes before tuning small operations. A suitable lookup structure may replace repeated scans; one batch operation may replace per-item I/O; an existing result may be reused instead of fetched or derived again.
- Combine or parallelize independent work only when the API and semantics support it. Bound concurrency and preserve required ordering, cancellation, failure handling, and resource limits. A lower wall-clock time can still increase CPU, memory, provider load, or failure risk.
- Add an index or change a query based on the actual query shape and plan. An index also costs storage and write work; a query that is already fast may not benefit.
- Cache only when repeated reads and reuse justify it. Establish freshness requirements, key completeness, invalidation, memory limits, and stampede behavior. A cache can add a network hop and a correctness bug.
- Precompute or compress only when repeated use, transfer savings, or response requirements justify the memory, refresh, CPU, or startup cost. Compare equivalent payloads and workloads before tuning levels or formats.
- Treat representation, pool-size, concurrency, and micro-optimization changes as hypotheses until their relevant cost is understood. Avoid speculative wrappers, broad refactors, or complexity for small or cold paths.
- Preserve observable behavior: returned values, ordering, error behavior, side effects, consistency, precision, and important freshness guarantees. A performance change that breaks those is not an optimization.

## Measure and verify meaningful changes

1. State the hypothesis in a falsifiable way: which work or metric should change, on which path, and under what workload.
2. Use an existing benchmark, profiler, trace, query plan, browser performance trace, or telemetry when it fits. If evidence is insufficient, add the smallest safe measurement that can distinguish the likely bottleneck; do not begin with an unsupported rewrite.
3. Compare before and after using the same representative workload, data, relevant environment, and measurement method. Keep other changes out of the comparison where practical. Include success and failure paths when they affect the workload, and account for warm versus cold behavior when it changes the result.
4. Measure the target and relevant trade-offs. Depending on the hypothesis, that may include latency distribution, throughput, errors, CPU, memory or allocations, database/network operations, payload or bundle size, and freshness or contention. Do not report every metric when it is unrelated.
5. Check correctness separately. Functional tests passing do not establish an end-to-end speedup; a microbenchmark does not prove the whole request or user journey improved. Clear code structure can prove fewer operations or better asymptotic growth, but do not call an unmeasured end-to-end effect measured.
6. If a comparable baseline cannot be obtained, report what is established, what remains an inference, and the specific measurement needed. Never invent timings, workload sizes, cache hit rates, or benchmark results.

For routine implementation, do not add benchmark infrastructure or a performance gate unless it is needed for a material claim, an existing project requirement, or a performance regression that should remain guarded.

## Report and retain lessons

For meaningful performance work, summarize the mechanism, affected path and conditions, change, evidence, and relevant trade-offs. Distinguish measured results from code-based reasoning and unknowns. If a recommendation was disproved by measurement, say so and retain that result rather than defending the original guess.

When a confirmed regression or mid-change correction yields a reusable lesson, report a concise proposed rule for the skill's maintainer: the trigger, mechanism, conditions, verified remedy, and trade-off. Never edit this skill, its files, or a separate learning log automatically. A maintainer decides whether and how to incorporate the lesson.
