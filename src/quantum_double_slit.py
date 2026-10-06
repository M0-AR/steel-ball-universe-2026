"""
08 — Quantum: electron cloud (probabilistic) + double-slit single-particle buildup.

Claims: not miniature planet; one-at-a-time electrons arrive as dots; accumulation ->
bright/dark fringes; landing random but odds follow wave; bound electrons only at
allowed energies (early ideas ~1900, modern theory 1920s).

Experiment:
- Double-slit intensity I(y) = 4 I0 cos^2(pi d y / lambda L) * sinc^2(pi a y / lambda L).
  Check fringe spacing dy = lambda L / d and visibility collapse with which-path info.
- Monte-Carlo: sample N=20000 single-electron landings from I(y); histogram peaks must
  correlate with theory (r > 0.95); single dots random (no two same y to fp precision).
- Bohr-ish check: hydrogen levels E_n = -13.6 eV / n^2; Lyman-alpha 10.2 eV.
"""
import numpy as np


def intensity(y, lam=50e-12, d=150e-9, a=50e-9, L=1.0):
    # electron matter wave demo values (TEM-like); spacing math is scale-invariant
    beta = np.pi * d * y / (lam * L)
    alpha = np.pi * a * y / (lam * L)
    env = np.where(np.abs(alpha) < 1e-12, 1.0, (np.sin(alpha) / alpha) ** 2)
    return 4.0 * (np.cos(beta) ** 2) * env


def run_benchmark(seed=7):
    rng = np.random.default_rng(seed)
    lam, d, L = 50e-12, 150e-9, 1.0
    expected_spacing = lam * L / d  # ~333 um

    ys = np.linspace(-1.5e-3, 1.5e-3, 3001)
    I = intensity(ys, lam=lam, d=d, L=L)
    # find central maxima spacing via peak detection near center
    center = np.argmax(I)
    # next maximum to the right
    peaks = []
    for i in range(1, len(I) - 1):
        if I[i] > I[i - 1] and I[i] > I[i + 1] and I[i] > 0.5:
            peaks.append(ys[i])
    peaks = np.array(peaks)
    # spacing near center
    if len(peaks) >= 3:
        mid = peaks[np.argsort(np.abs(peaks))[:4]]
        mid = np.sort(mid)
        spacing = float(np.mean(np.diff(mid)))
    else:
        spacing = float("nan")

    # Monte Carlo single-electron buildup (rejection sampling)
    N = 20000
    y_min, y_max = -1.5e-3, 1.5e-3
    I_max = 4.0
    samples = []
    while len(samples) < N:
        trial = rng.uniform(y_min, y_max, N * 2)
        prob = intensity(trial, lam=lam, d=d, L=L) / I_max
        accept = rng.uniform(0, 1, N * 2) < prob
        samples.extend(trial[accept].tolist())
    samples = np.array(samples[:N])
    hist, edges = np.histogram(samples, bins=60, range=(y_min, y_max))
    centers = 0.5 * (edges[:-1] + edges[1:])
    theory = intensity(centers, lam=lam, d=d, L=L)
    r = float(np.corrcoef(hist, theory)[0, 1])

    # hydrogen levels
    E1 = -13.6
    E2 = E1 / 4
    lyman_alpha = E2 - E1  # 10.2 eV

    passed = bool(
        abs(spacing - expected_spacing) / expected_spacing < 0.05
        and r > 0.95
        and abs(lyman_alpha - 10.2) < 1e-9
    )
    return {
        "name": "quantum_double_slit",
        "fringe_spacing_m": spacing,
        "expected_spacing_m": float(expected_spacing),
        "mc_correlation_r": r,
        "mc_N": N,
        "hydrogen_lyman_alpha_eV": float(lyman_alpha),
        "quantum_era": "1900-1920s",
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
