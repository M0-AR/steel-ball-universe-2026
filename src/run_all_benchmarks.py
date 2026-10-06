"""
Master runner: executes every benchmark, writes reports/benchmark.json,
optionally renders figures, exits non-zero on any failure (CI-friendly).

Usage:
  python -m src.run_all_benchmarks --output reports/benchmark.json --figures reports/
  pytest tests/ -v
"""
import argparse
import json
import os
import sys
import time

from . import galileo_ramp as m_galileo
from . import inertia_newton as m_inertia
from . import gravity_orbit as m_gravity
from . import energy_entropy as m_energy
from . import waves_sound as m_waves
from . import electromagnetism_light as m_em
from . import relativity as m_rel
from . import quantum_double_slit as m_q
from . import standard_model as m_sm
from . import cosmology_gap as m_cosmo
from . import live_market_verification as m_live
from . import hidden_patterns as m_hidden


def collect():
    results = []
    results.append(m_galileo.run_benchmark())
    results.append(m_inertia.run_benchmark())
    results.append(m_gravity.run_benchmark())
    results.append(m_energy.run_benchmark())
    results.append(m_waves.run_benchmark())
    results.append(m_em.run_benchmark())
    results.append(m_rel.run_benchmark())
    results.append(m_q.run_benchmark())
    results.append(m_sm.run_benchmark())
    results.append(m_cosmo.run_benchmark())
    live = m_live.run_benchmark()
    results.append(live)
    # feed live BTC prices into null-pattern test when available
    try:
        prices = None
        btc = live.get("checks", {}).get("btc", {})
        # live module caches snapshots; re-read cache for pattern input
        import glob as _glob
        cands = _glob.glob(os.path.join(os.path.dirname(__file__), "..", "data", "live_btc_snapshot.json"))
        if cands:
            with open(cands[0]) as f:
                snap = json.load(f)
            prices = snap.get("daily_prices") or ([snap.get("spot_usd")] * 5)
    except Exception:
        prices = None
    results.append(m_hidden.run_benchmark(market_prices=prices))
    return results


def render_figures(figdir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as e:
        print(f"[figures] matplotlib unavailable: {e}", file=sys.stderr)
        return []
    os.makedirs(figdir, exist_ok=True)
    made = []
    # Fig 1: odd intervals + squares
    odds = np.array([1, 3, 5, 7], dtype=float)
    ticks = np.arange(1, 5)
    plt.figure()
    plt.bar(ticks, odds)
    plt.xlabel("equal time tick")
    plt.ylabel("distance in tick (units of first)")
    plt.title("Galileo odd-number law 1:3:5:7")
    p = os.path.join(figdir, "fig01_odd_numbers.png")
    plt.savefig(p, dpi=150, bbox_inches="tight")
    plt.close()
    made.append(p)
    # Fig 2: orbit
    th = np.linspace(0, 2 * np.pi, 400)
    plt.figure()
    plt.plot(np.cos(th), np.sin(th))
    plt.gca().set_aspect("equal")
    plt.title("Newton cannon: circular orbit (unit circle)")
    p2 = os.path.join(figdir, "fig02_orbit.png")
    plt.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close()
    made.append(p2)
    # Fig 3: double-slit theory curve
    from .quantum_double_slit import intensity
    ys = np.linspace(-1.5e-3, 1.5e-3, 1000)
    plt.figure()
    plt.plot(ys * 1e3, intensity(ys))
    plt.xlabel("screen y (mm)")
    plt.ylabel("relative intensity")
    plt.title("Double-slit buildup envelope (single-particle sampling target)")
    p3 = os.path.join(figdir, "fig03_doubleslit.png")
    plt.savefig(p3, dpi=150, bbox_inches="tight")
    plt.close()
    made.append(p3)
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="reports/benchmark.json")
    ap.add_argument("--figures", default="reports/")
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    results = collect()
    dt = time.time() - t0
    overall = all(r.get("pass", False) for r in results)
    payload = {"date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "overall_pass": bool(overall),
               "elapsed_s": dt,
               "n_benchmarks": len(results),
               "n_passed": sum(1 for r in results if r.get("pass")),
               "results": results}
    figs = [] if args.no_figures else render_figures(args.figures)
    payload["figures"] = figs

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(payload, f, indent=2)

    for r in results:
        print(f"[{'PASS' if r.get('pass') else 'FAIL'}] {r.get('name')}")
    print(f"overall={'PASS' if overall else 'FAIL'}  {payload['n_passed']}/{len(results)}  -> {args.output}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
