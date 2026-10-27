# Measuring performance

Read this before running measurements in an audit or investigation. Sections: safety limits, trustworthy measurements, picking a tool, frontend metrics, load tests, sources.

## Safety limits for measuring without asking

Measure on your own only when all of these hold. If one would be crossed, ask first, or report the finding as INFERRED with the measurement still needed.

- **Local target:** the code under test, a local server, a local or disposable database, or a test container. Never production, staging, a shared database, or a third-party or paid API without explicit approval.
- **Nothing installed:** use tools already in the repository or runtime, plus `scripts/perfstat.py`. Ask before installing a profiler, load tool, or dependency.
- **No lasting side effects:** prefer read-only work. `EXPLAIN ANALYZE` executes the statement, so wrap a write in `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`. Seed data only into disposable databases or copies. Remove temporary instrumentation and confirm with version control that only agreed changes remain.
- **Short:** keep each measurement to about two minutes. Ask before stress, soak, or longer runs.
- **Recorded:** save raw output outside the repository, such as a temporary directory, and cite its path in the report.

## Make the measurement trustworthy

- Use the same workload, data, environment, and method before and after. Seed a realistic data volume deterministically; tiny fixtures hide costs that grow with data.
- Exclude warm-up runs unless cold behavior is the objective. Measure start-up, first request, or cache-miss cost separately when it matters.
- Repeat at the level that varies. Separate process runs capture variation that loop iterations inside one process miss.
- Report the median and spread. Report p95 or p99 only with enough samples to support them, and never report a mean alone.
- Alternate before and after runs in rounds rather than one batch and then the other, so drift and background load affect both. Changes as small as environment size or link order can shift results, so treat a small difference from one setup with suspicion. Report an interval on the change and call it inconclusive when the interval includes zero; `scripts/perfstat.py compare` does this.
- For a path that fans out to many calls, report per-component tail latency. With 100 parallel calls to servers whose p99 is one second, 63% of requests take more than one second.
- While a benchmark runs, find what limits it: for each resource (CPU, memory, disk, network, locks, pools), check utilization, saturation, and errors. A result without its limiting factor is incomplete.
- When a change shows no effect, confirm the changed code ran and that a cache did not mask it before concluding it does not help.
- A faster microbenchmark does not show the request or user journey improved. Measure the path the user cares about.

## Pick the tool

Prefer what the project already uses. Check the current documentation for the installed version before running a command.

| Question | Tool class | Examples |
| --- | --- | --- |
| How long does a command take, before and after? | Repeat timer | hyperfine, `scripts/perfstat.py` |
| Where does CPU time go? | Profiler | Python `cProfile` (an alias of `profiling.tracing` from 3.15) or py-spy; Node `--cpu-prof`; Go `runtime/pprof`; JVM async-profiler; Linux `perf` |
| Where does memory go? | Heap profiler | Python `tracemalloc`; DevTools heap snapshots; Go heap profile |
| What does one query do? | Query plan | PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`; MySQL `EXPLAIN ANALYZE` |
| Which queries cost most in total? | Query statistics | PostgreSQL `pg_stat_statements` |
| How many queries or calls does one request make? | Query log or counter | Driver or ORM query logging; a temporary counter around the call |
| Why is a page slow to load or respond? | Browser trace; lab audit | Chrome DevTools Performance panel; Lighthouse |
| How does a service behave under load? | Open-model load generator | k6 arrival-rate executors; wrk2 |

## Frontend metrics

- Core Web Vitals are "good" at LCP of 2.5 s or less, INP of 200 ms or less, and CLS of 0.1 or less, assessed at the 75th percentile of page loads, separately for mobile and desktop.
- Lab results such as Lighthouse or a single trace are not field data. Total Blocking Time is a lab proxy, not INP.
- Do not claim a full audit when only one page, trace, viewport, or device was tested. Name what was measured.

## Load tests (only when asked)

- Use an open model with a fixed arrival rate. A closed-loop tool waits for each response before sending the next request, so slow responses suppress the very requests that would have recorded them (coordinated omission).
- Step the arrival rate and hold each step long enough to settle. Report the rate where latency or errors climb, what gave way first, and whether the service recovered.
- Never target production or a shared environment without explicit approval.

## Sources

- Gil Tene, "How NOT to Measure Latency" (2013), https://www.infoq.com/presentations/latency-pitfalls/ ; wrk2, https://github.com/giltene/wrk2
- Grafana k6, open and closed models, https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/
- Brendan Gregg, the USE method, https://www.brendangregg.com/usemethod.html ; active benchmarking, https://www.brendangregg.com/activebenchmarking.html
- Mytkowicz et al., "Producing Wrong Data Without Doing Anything Obviously Wrong!" (ASPLOS 2009), https://doi.org/10.1145/1508244.1508275
- Kalibera and Jones, "Rigorous Benchmarking in Reasonable Time" (ISMM 2013), https://doi.org/10.1145/2464157.2464160 ; "Quantifying Performance Changes with Effect Size Confidence Intervals" (2012), https://www.cs.kent.ac.uk/pubs/2012/3233/
- Dean and Barroso, "The Tail at Scale" (CACM 2013), https://research.google/pubs/pub40801/
- Google SRE book, "Service Level Objectives", https://sre.google/sre-book/service-level-objectives/
- web.dev, Web Vitals, https://web.dev/articles/vitals
- PostgreSQL, EXPLAIN, https://www.postgresql.org/docs/current/sql-explain.html
- Lessons from public skills: WordPress wp-performance, https://github.com/WordPress/agent-skills/tree/trunk/skills/wp-performance ; swyx web-perf, https://github.com/swyxio/skills/tree/main/web-perf ; Addy Osmani web-quality-skills, https://github.com/addyosmani/web-quality-skills/tree/main/skills/performance
