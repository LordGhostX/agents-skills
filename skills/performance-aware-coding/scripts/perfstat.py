#!/usr/bin/env python3
"""perfstat: repeat-time a command and compare two sets of samples. Stdlib only.

Usage:
  perfstat.py run [--warmup 3] [--runs 20] [--timeout 120] [--out FILE] -- CMD [ARGS...]
      Runs CMD --warmup times (discarded), then --runs times, without a shell.
      Writes one wall-clock duration in milliseconds per line to FILE (or
      stdout) and a summary to stderr. Timings include process start-up; time
      in-process work with the stack's own benchmark tool instead.
      If CMD exits non-zero or times out, the run stops with exit code 2:
      a failing command is not a timing.
  perfstat.py summary FILE
      Prints n, median, p95, p99, min and max.
  perfstat.py compare BEFORE AFTER [--confidence 0.95] [--resamples 5000] [--seed 0]
      Prints both summaries, the change in the median, and a bootstrap
      confidence interval for that change. The verdict is "lower" or "higher"
      only when the interval excludes zero and each side has at least 10
      samples; otherwise "inconclusive".
  perfstat.py --self-test

Sample files hold one number per line, where lower is better (milliseconds,
bytes, query counts). Blank lines and lines starting with # are ignored.
p95 is shown from 20 samples and p99 from 100; below that it prints n/a.
"""
import argparse
import random
import statistics
import subprocess
import sys
import time

MIN_VERDICT_N = 10
PCT_MIN_N = {95: 20, 99: 100}


def read_samples(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f]
    values = [float(ln) for ln in lines if ln and not ln.startswith("#")]
    if not values:
        raise SystemExit(f"no samples in {path}")
    return values


def percentile(values, pct):
    if len(values) < PCT_MIN_N[pct]:
        return None
    return statistics.quantiles(values, n=100, method="inclusive")[pct - 1]


def summary(values):
    return {
        "n": len(values),
        "median": statistics.median(values),
        "p95": percentile(values, 95),
        "p99": percentile(values, 99),
        "min": min(values),
        "max": max(values),
    }


def fmt(x):
    return "n/a" if x is None else f"{x:.3f}"


def summary_line(label, s):
    return (f"{label}: n={s['n']} median={fmt(s['median'])} p95={fmt(s['p95'])} "
            f"p99={fmt(s['p99'])} min={fmt(s['min'])} max={fmt(s['max'])}")


def compare(before, after, confidence=0.95, resamples=5000, seed=0):
    rng = random.Random(seed)
    diffs = sorted(
        statistics.median(rng.choices(after, k=len(after)))
        - statistics.median(rng.choices(before, k=len(before)))
        for _ in range(resamples)
    )
    tail = (1 - confidence) / 2
    lo = diffs[int(tail * (resamples - 1))]
    hi = diffs[int((1 - tail) * (resamples - 1))]
    base = statistics.median(before)
    diff = statistics.median(after) - base
    if min(len(before), len(after)) < MIN_VERDICT_N:
        verdict = f"inconclusive: need >= {MIN_VERDICT_N} samples per side"
    elif hi < 0:
        verdict = "lower"
    elif lo > 0:
        verdict = "higher"
    else:
        verdict = "inconclusive: interval includes 0"
    return {
        "diff": diff,
        "pct": diff / base * 100 if base else None,
        "lo": lo,
        "hi": hi,
        "confidence": confidence,
        "verdict": verdict,
    }


def time_command(cmd, warmup, runs, timeout):
    samples = []
    for i in range(warmup + runs):
        start = time.perf_counter()
        try:
            done = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                  timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"run {i + 1}: timed out after {timeout}s", file=sys.stderr)
            raise SystemExit(2)
        elapsed = (time.perf_counter() - start) * 1000
        if done.returncode != 0:
            tail = done.stderr.decode(errors="replace").strip()[-500:]
            print(f"run {i + 1}: exit {done.returncode}\n{tail}", file=sys.stderr)
            raise SystemExit(2)
        if i >= warmup:
            samples.append(elapsed)
    return samples


def main(argv):
    if argv == ["--self-test"]:
        self_test()
        print("self-test: ok")
        return
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--warmup", type=int, default=3)
    r.add_argument("--runs", type=int, default=20)
    r.add_argument("--timeout", type=float, default=120)
    r.add_argument("--out")
    r.add_argument("command", nargs=argparse.REMAINDER)
    s = sub.add_parser("summary")
    s.add_argument("file")
    c = sub.add_parser("compare")
    c.add_argument("before")
    c.add_argument("after")
    c.add_argument("--confidence", type=float, default=0.95)
    c.add_argument("--resamples", type=int, default=5000)
    c.add_argument("--seed", type=int, default=0)
    a = p.parse_args(argv)

    if a.cmd == "run":
        cmd = a.command[1:] if a.command[:1] == ["--"] else a.command
        if not cmd or a.runs < 1 or a.warmup < 0:
            p.error("run needs --runs >= 1, --warmup >= 0 and a command after --")
        samples = time_command(cmd, a.warmup, a.runs, a.timeout)
        text = "".join(f"{x:.3f}\n" for x in samples)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            sys.stdout.write(text)
        print(summary_line("ms", summary(samples)), file=sys.stderr)
    elif a.cmd == "summary":
        print(summary_line(a.file, summary(read_samples(a.file))))
    else:
        before, after = read_samples(a.before), read_samples(a.after)
        res = compare(before, after, a.confidence, a.resamples, a.seed)
        print(summary_line("before", summary(before)))
        print(summary_line("after ", summary(after)))
        pct = "n/a" if res["pct"] is None else f"{res['pct']:+.1f}%"
        print(f"median change: {res['diff']:+.3f} ({pct}); "
              f"{res['confidence']:.0%} CI [{res['lo']:+.3f}, {res['hi']:+.3f}]; verdict: {res['verdict']}")


def self_test():
    import os
    import tempfile

    s = summary([float(x) for x in range(1, 101)])
    assert s["n"] == 100 and s["median"] == 50.5 and s["min"] == 1 and s["max"] == 100
    assert 94 < s["p95"] < 96 and 98 < s["p99"] < 100
    small = summary([1.0, 2.0, 3.0])
    assert small["p95"] is None and small["p99"] is None
    assert summary([float(x) for x in range(20)])["p95"] is not None

    rng = random.Random(1)
    slow = [100 + rng.gauss(0, 2) for _ in range(30)]
    fast = [80 + rng.gauss(0, 2) for _ in range(30)]
    assert compare(slow, fast)["verdict"] == "lower"
    assert compare(fast, slow)["verdict"] == "higher"
    same = [100 + rng.gauss(0, 5) for _ in range(30)]
    assert compare(slow, same)["verdict"].startswith("inconclusive")
    assert compare(slow[:5], fast[:5])["verdict"].startswith("inconclusive: need")
    assert compare(slow, fast) == compare(slow, fast), "seeded bootstrap must be repeatable"

    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "s.txt")
        with open(path, "w") as f:
            f.write("# header\n1.5\n\n2.5\n")
        assert read_samples(path) == [1.5, 2.5]

    got = time_command([sys.executable, "-c", "pass"], warmup=1, runs=3, timeout=30)
    assert len(got) == 3 and all(x > 0 for x in got)
    for bad in ([sys.executable, "-c", "raise SystemExit(3)"],
                [sys.executable, "-c", "import time; time.sleep(5)"]):
        try:
            time_command(bad, warmup=0, runs=1, timeout=0.5)
        except SystemExit as e:
            assert e.code == 2
        else:
            raise AssertionError("a failing or hung command must stop the run")


if __name__ == "__main__":
    main(sys.argv[1:])
