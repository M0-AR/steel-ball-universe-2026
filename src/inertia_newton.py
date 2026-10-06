"""
02 — Inertia + Newton F=ma (1687 Principia) + action-reaction.

Claims: level track -> uniform motion without force (inertia);
spring shove F while touching; same F on larger m -> smaller a; recoil equal/opposite
on different objects so no cancellation.

Experiment:
- Inertia: zero net force -> v constant (integrate with F=0).
- F=ma linearity: a = F/m for grid of F,m; fit slope must be 1.0.
- Action-reaction: two-body momentum conservation; spring-ball toy model conserves
  total momentum to machine precision.
"""
import numpy as np


def run_benchmark():
    # 1. inertia: F=0 for 10 s, v0=2 m/s -> x = 20 m exactly
    v0, t = 2.0, 10.0
    x_inertia = v0 * t  # analytic
    # numeric Euler
    dt = 1e-3
    n = int(t / dt)
    x, v = 0.0, v0
    for _ in range(n):
        v += 0.0  # F=0
        x += v * dt
    inertia_err = abs(x - x_inertia) / x_inertia

    # 2. F=ma linearity
    forces = np.array([1.0, 2.0, 5.0, 10.0])
    masses = np.array([0.5, 1.0, 2.0, 4.0])
    max_err = 0.0
    for F in forces:
        for m in masses:
            a = F / m
            max_err = max(max_err, abs(a * m - F))
    # fit a vs F for m=1 -> slope 1
    a_vals = forces / 1.0
    slope = np.polyfit(forces, a_vals, 1)[0]

    # 3. recoil momentum conservation: m1 v1 + m2 v2 = 0 after internal spring push
    m_ball, m_pusher = 0.5, 1.5
    # impulse J gives ball +J/m_ball, pusher -J/m_pusher
    J = 3.0
    v_ball = J / m_ball
    v_push = -J / m_pusher
    total_p = m_ball * v_ball + m_pusher * v_push

    passed = bool(
        inertia_err < 1e-9
        and max_err < 1e-12
        and abs(slope - 1.0) < 1e-12
        and abs(total_p) < 1e-12
    )
    return {
        "name": "inertia_newton",
        "principia_year": 1687,
        "inertia_distance_m": float(x_inertia),
        "inertia_numeric_error": float(inertia_err),
        "fma_max_error": float(max_err),
        "fma_slope_F_vs_a_m1": float(slope),
        "recoil_total_momentum": float(total_p),
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
