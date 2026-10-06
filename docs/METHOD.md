# METHOD — zero-to-hero verification ladder

For each narrative sentence we (1) restate as falsifiable claim, (2) choose ground truth (constant, exact identity, or literature value), (3) set a priori tolerance, (4) implement the cheapest honest simulation that can fail, (5) run `pytest` + `run_all_benchmarks`, (6) record PASS/FAIL in `reports/benchmark.json`. No file was written before its supporting search completed (RESEARCH_LOG order).

Physics modules use only `numpy`/`scipy`/`matplotlib`; live module uses stdlib `urllib` (no key) with seeded `data/live_*_snapshot.json` fallback so `docker compose up` works offline (marked `cached`). Hidden-pattern module includes a preregistered null (market odd-law) to prove falsifiability.

Tolerances are in code (`*_benchmark()` return dicts) and mirrored in `tests/`. Figures are derived artifacts, never inputs. To extend: add `src/<claim>.py` with `run_benchmark()->dict(name,pass,...)`, register in `run_all_benchmarks.collect()`, add a `test_*`, and re-run `make reproduce`.
