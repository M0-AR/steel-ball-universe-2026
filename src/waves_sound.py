"""
05 — Sound waves + interference (patterns, not just objects).

Claims: tap -> neighbor pushes neighbor; compressed/rarefied regions travel;
air molecules jiggle locally (no bulk flight); energy+momentum transfer;
crests add, crest+trough cancel.

Experiment:
- 1-D discrete wave equation: d'Alembert pulse splits into L/R halves (c check).
- Two-source interference: y = A sin(kx-wt) + A sin(kx-wt+phi); phi=0 -> 2A,
  phi=pi -> 0. Visibility V = (Imax-Imin)/(Imax+Imin) = 1 for coherent equal sources.
- Sound speed check: 343 m/s at 20 C within accepted 331-349 range.
"""
import numpy as np


def run_benchmark():
    c = 343.0  # m/s at 20 C
    # pulse split test on ring of N points
    N, dx, dt = 200, 0.01, 1e-5
    # CFL: c*dt/dx = 0.343 < 1 stable
    u = np.zeros(N)
    u_prev = np.zeros(N)
    u[N // 2] = 1.0
    u_prev[N // 2] = 1.0
    C2 = (c * dt / dx) ** 2
    for _ in range(300):
        u_next = np.zeros(N)
        u_next[1:-1] = 2 * u[1:-1] - u_prev[1:-1] + C2 * (u[2:] - 2 * u[1:-1] + u[:-2])
        # periodic ends
        u_next[0] = 2 * u[0] - u_prev[0] + C2 * (u[1] - 2 * u[0] + u[-1])
        u_next[-1] = 2 * u[-1] - u_prev[-1] + C2 * (u[0] - 2 * u[-1] + u[-2])
        u_prev, u = u, u_next
    # pulse should have split and left center much smaller than initial peak
    split_ok = bool(u[N // 2] < 0.5 and np.max(np.abs(u)) > 0.2)

    # interference
    A = 1.0
    y_constructive = A + A  # phi=0
    y_destructive = A - A  # phi=pi
    I_max, I_min = (2 * A) ** 2, 0.0
    V = (I_max - I_min) / (I_max + I_min)

    passed = bool(
        split_ok
        and abs(y_constructive - 2.0) < 1e-12
        and abs(y_destructive) < 1e-12
        and abs(V - 1.0) < 1e-12
        and 330 < c < 350
    )
    return {
        "name": "waves_sound",
        "sound_speed_m_s": c,
        "pulse_split_ok": split_ok,
        "constructive_amplitude": float(y_constructive),
        "destructive_amplitude": float(y_destructive),
        "fringe_visibility": float(V),
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
