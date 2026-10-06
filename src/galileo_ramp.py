"""
01 — Galileo ramp: odd-number law 1:3:5:7 and s ~ t^2.

Claim in narrative: bells at gaps 1,3,5,7 ring at equal ticks -> uniform acceleration.
Verified: Museo Galileo inclined-plane (5 bells, odd-number spacing); IMEKO MetroArchaeo
2025-2026 reconstructions (11/33/55/77 cm = 1:3:5:7 ratios, total 176 cm); Galileo Discorsi
1638 Two New Sciences: spaces as squares of times.

Experiment:
- Analytic sliding point mass: s = 1/2 a t^2, a = g sin(theta).
- Rolling solid sphere without slipping: a = g sin(theta) / (1 + 2/5) = 5/7 g sin(theta).
- Check successive-interval distances ratio -> [1,3,5,7] within 1e-9.
- Check s_total ratios = n^2: [1,4,9,16].
- Numerical integration (explicit Euler at small dt) must agree with analytic to <0.5%.
"""
import numpy as np
from .constants import G_SURFACE


def analytic_positions(times, a):
    times = np.asarray(times, dtype=float)
    return 0.5 * a * times ** 2


def interval_ratios(positions):
    positions = np.asarray(positions, dtype=float)
    intervals = np.diff(positions, prepend=0.0)
    return intervals / intervals[0]


def rolling_acceleration(theta_rad, g=G_SURFACE):
    # solid sphere I = 2/5 m r^2
    return g * np.sin(theta_rad) / (1.0 + 2.0 / 5.0)


def simulate_euler(a, t_end, dt=1e-4):
    n = int(t_end / dt)
    v, x = 0.0, 0.0
    for _ in range(n):
        v += a * dt
        x += v * dt
    return x


def run_benchmark(theta_deg=3.0):
    theta = np.deg2rad(theta_deg)
    a_slide = G_SURFACE * np.sin(theta)
    a_roll = rolling_acceleration(theta)
    # equal ticks t = 1,2,3,4 (arbitrary units)
    ticks = np.array([1.0, 2.0, 3.0, 4.0])
    pos = analytic_positions(ticks, a_roll)
    ratios = interval_ratios(pos)
    expected_ratios = np.array([1.0, 3.0, 5.0, 7.0])
    total_ratios = pos / pos[0]
    expected_totals = np.array([1.0, 4.0, 9.0, 16.0])

    # numerical check
    t_end = 2.0
    x_num = simulate_euler(a_roll, t_end)
    x_exact = 0.5 * a_roll * t_end ** 2

    return {
        "name": "galileo_ramp",
        "theta_deg": theta_deg,
        "a_slide_m_s2": float(a_slide),
        "a_roll_m_s2": float(a_roll),
        "roll_factor_5_7": float(a_roll / a_slide),
        "interval_ratios": [float(r) for r in ratios],
        "expected_odd": [1.0, 3.0, 5.0, 7.0],
        "max_odd_error": float(np.max(np.abs(ratios - expected_ratios))),
        "total_ratios": [float(r) for r in total_ratios],
        "max_square_error": float(np.max(np.abs(total_ratios - expected_totals))),
        "euler_relative_error": float(abs(x_num - x_exact) / x_exact),
        "pass": bool(
            np.max(np.abs(ratios - expected_ratios)) < 1e-9
            and np.max(np.abs(total_ratios - expected_totals)) < 1e-9
            and abs(a_roll / a_slide - 5.0 / 7.0) < 1e-12
            and abs(x_num - x_exact) / x_exact < 5e-3
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
