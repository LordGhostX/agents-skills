# performance-aware-coding evals

`evals.json` follows the skill-creator format. Each fixture is a small app with real costs and decoys that look costly but are not:

- `fixtures/py-orders`: SQLite dashboard. Real: a full sort repeated per product, a per-order customer query, and an unbounded read of a growing table. Decoys: a one-off migration loop, a cached rate lookup, a three-region loop.
- `fixtures/js-report`: Node report endpoint. Real: independent API calls awaited one by one, and settings JSON parsed per line. Decoys: dependent customer-then-account calls and a start-up-only plugin scan.

The fixtures are designed so that code reading alone ranks them wrongly: in py-orders the 20,000 per-order queries take about 9% of the time because SQLite is in-process, while the repeated sort takes about 85%.

## How to run

Copy a fixture to a temporary directory, commit it to a throwaway git repository, and give an agent the eval prompt with the skill folder to follow. Grade the final reply against `expectations`, and check `git status` in the copy afterwards.

## Results (2026-10-27)

Agent: nine coding-agent subagent runs at once on one Apple M4 laptop. Baseline: the skill as of commit `7d1ab93`.

| Eval | This version (3 runs) | Baseline (1 run) |
| --- | --- | --- |
| 1. Audit py-orders (9 expectations) | 9/9, 9/9, 9/9 | 8/9 |
| 2. Why is js-report slow (7) | 7/7, 7/7, 7/7 | 6/7 |
| 3. Add a function, no audit (3) | 3/3 | not run |

- **Same findings:** both versions found every real cost, ranked them by measurement, and left the decoys out of the urgent group. The baseline's only misses were the MEASURED and INFERRED labels this version introduces. These fixtures do not separate the two versions on accuracy for this model.
- **What changed:** every run with this version used the same report shape, labelled each finding, and gave a confidence interval for its before-and-after change. Four runs saved `scripts/perfstat.py compare` output with the raw samples; two quoted intervals without saving that output. Two runs reported a noisy machine (load average about 9 while nine evals ran) and relied on alternating before-and-after rounds to keep the comparison valid. The baseline runs gave measured medians without intervals and marked estimates in prose.
- **Cost:** runs with this version took about 1.5 to 2 times longer (6 to 9 minutes against 4 to 6) because they repeated measurements.
- **Clean up:** `git status` was clean in all eight audit copies. Eval 3 changed only the requested function.
- **Eval 3 note:** the run met all three expectations, but it timed the new query on a 1.85-million-row in-memory table, which is heavier than a quick cost pass needs.
