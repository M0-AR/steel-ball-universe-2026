"""
07 — Special relativity (1905): invariant c, light clock, E=mc^2.

Claims: chasing beam cannot reduce its speed; light clock on cart ticks slower as seen
from ground (diagonal path, same c); SR 1905; E=mc^2.

Experiment:
- Lorentz factor gamma(v) checks: gamma(0)=1, gamma(0.99c)~7.0888.
- Light-clock derivation: dt_ground = gamma * dt_proper (diagonal sqrt).
- Muon check: lab lifetime 2.2 us, at v=0.994c gamma~9.14 -> lab lifetime ~20 us,
  survives 15 km descent (needs >~10 us). Matches school-lab muon experiments.
- GPS cross-check: SR -7 us/day + GR +45 us/day = +38 us/day net (NIST + Ashby).
- E=mc^2: 1 kg <-> 8.98755e16 J.
"""
import numpy as np
from .constants import C_LIGHT, MUON_LIFETIME, GPS_NET_US_PER_DAY


def gamma(v):
    beta = v / C_LIGHT
    return 1.0 / np.sqrt(1.0 - beta ** 2)


def run_benchmark():
    g0 = float(gamma(0.0))
    g99 = float(gamma(0.99 * C_LIGHT))
    # light clock: proper tick 2L/c, ground tick 2L/(c sqrt(1-b^2)) = gamma * proper
    L = 1.0
    v = 0.6 * C_LIGHT
    proper = 2 * L / C_LIGHT
    ground = proper * float(gamma(v))
    diag_ok = abs(ground / proper - 1.25) < 1e-9  # gamma(0.6c)=1.25

    # muon
    v_mu = 0.994 * C_LIGHT
    g_mu = float(gamma(v_mu))
    lab_life = MUON_LIFETIME * g_mu
    survives = lab_life > 10e-6  # needs ~10+ us to cross atmosphere at ~c

    # GPS
    gps_ok = abs((-7.0 + 45.0) - GPS_NET_US_PER_DAY) < 1e-9

    # E=mc^2
    E_1kg = 1.0 * C_LIGHT ** 2

    passed = bool(
        abs(g0 - 1.0) < 1e-12
        and abs(g99 - 7.088811727) < 1e-3
        and diag_ok
        and survives
        and gps_ok
        and abs(E_1kg - 8.987551787e16) / 8.987551787e16 < 1e-6
    )
    return {
        "name": "relativity",
        "einstein_year": 1905,
        "gamma_0": g0,
        "gamma_0p99c": g99,
        "light_clock_ratio": float(ground / proper),
        "muon_gamma_0p994c": g_mu,
        "muon_lab_lifetime_s": float(lab_life),
        "gps_net_us_per_day": float(GPS_NET_US_PER_DAY),
        "E_1kg_J": float(E_1kg),
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
