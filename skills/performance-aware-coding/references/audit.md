# Performance audit

Read this when the user asks for a performance audit, asks why something is slow, or asks you to find bottlenecks. The method in `SKILL.md` still applies; this file adds scope, verification, measurement, ranking, and the report. An audit reports findings and changes no files unless the user asks for fixes.

## 1. Set the scope and workload

- Audit what the user names: a path, endpoint, job, page, query, or flow. If nothing is named, audit the repository, starting from its entry points: routes, handlers, jobs, consumers, commands, and pages.
- For a symptom such as "X is slow", start at that path and follow the calls it makes. Do not audit unrelated code.
- Find the expected workload in the repository before judging cost: README, deploy and scaling config, page-size and rate limits, seed or fixture volumes, schemas, and any telemetry or budgets the project references. State the workload you assumed and where it came from. If nothing is stated, say so and choose a conservative assumption.
- In a large repository, go deep on hot paths: per request, record, render, message, or retry, and loops over data that grows. Name the areas you did not read.

## 2. Collect candidates

Use the cues under "Look for concrete costs" in `SKILL.md`. For each candidate, note the location, what repeats and per what, how it grows with data or traffic, and where it sits: user-blocking, on a shared resource, in the background, or cold.

## 3. Verify each candidate before it becomes a finding

Re-read the lines, their callers, and the data they receive. Drop or downgrade a candidate when one of these holds:

- **Bounded input:** a constant list, an enforced page size, a validated limit, or a schema constraint keeps it small.
- **Cold path:** start-up, a one-off migration or script, an admin task, or test- or development-only code.
- **Already avoided:** memoization or caching (check its key and lifetime), batching, eager loading or prefetching, or a library that already does the work.
- **Dependent calls:** a later call needs an earlier result, so the calls cannot run concurrently.
- **Cheap transport:** an in-process or embedded store turns a per-item query into a function call rather than a network round trip. Measure it before ranking it.
- **Not a repeated sequence:** an N+1 pattern is one query or call shape repeated per item, one after another, under one parent operation. A high call count alone is a hint, not proof; calls that differ in shape or already run concurrently are a different problem, if any.

A candidate without a concrete case of when it costs something is not a finding, and neither is an already-good metric or a near-zero saving. Leave out style preferences and vague worries.

## 4. Measure when the code runs locally

Read `references/measure.md` before running anything; it covers method, tool choice, and the safety limits for measuring without asking.

1. Time the whole affected path with a representative workload, then profile it to see where the time or resource goes.
2. Attribute each finding's share of the objective from the profile or a targeted measurement.
3. To confirm the effect of a likely fix, try it in a scratch copy or as a temporary change, measure before and after with the same workload, and revert it.

Label every finding:

- **MEASURED:** numbers from a run in this session, with the command, workload, and raw output path.
- **INFERRED:** code reasoning only. Name the measurement that would confirm or refute it.

If the code cannot run locally, or measuring would cross a limit in `references/measure.md`, report INFERRED findings and the measurements needed. Never present an estimate as a measurement.

## 5. Rank

- **Fix now:** a hot path with a measured or clearly large cost at the stated workload, or unbounded growth that the workload already reaches.
- **Worth doing:** a real cost with a smaller share, lower frequency, or a fix with a meaningful trade-off.
- **Watch:** cheap today but grows with data or traffic, or a cold path worth knowing about.

Within each group, order by measured share of the objective, then by growth. A measurement that contradicts the code reading wins; say so.

## 6. Report

Report in the chat. Write a file such as `PERF_AUDIT.md` only when the user asks. Use plain words and explain a technical term the first time it appears. Number findings across groups so the user can say "fix 1 and 3". Report at most 20 findings and say how many were left out.

```markdown
**What this does:** one line. **Workload assumed:** numbers and their source.
**Scope:** what was read. **Not read:** areas skipped.

### Fix now
1. **Short title** (`path/to/file:L10-L24`) · MEASURED
   - **What happens:** the mechanism, how often it runs, and how it grows.
   - **Evidence:** numbers, command, workload, raw output path; or the code reasoning and the measurement still needed.
   - **Fix:** the proportionate change. **Trade-off:** what it costs or risks.
   - **If skipped:** the impact at the stated workload.

### Worth doing
### Watch

**Verdict:** fix 1 and 2 first.
**Not checked:** what this audit did not cover.
**Measurements still needed:** one line per INFERRED finding.
```

If nothing survives verification, say "No material costs found" and list what was checked and measured. Do not claim more coverage than was measured: name the paths, pages, datasets, and environment the numbers came from.

The N+1 gate above follows PostHog's signals-scout-apm skill: https://github.com/PostHog/posthog/tree/master/products/signals/skills/signals-scout-apm

## 7. After the report

Change code only when the user asks. After applying the fixes the user picks, rerun the same measurement and compare before and after, for example with `scripts/perfstat.py compare`. Report the result even when it disproves the finding.
