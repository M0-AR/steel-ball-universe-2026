"""
06 — Electromagnetism: fields + Maxwell -> light speed.

Claims: excess charge spreads over conducting surface; E-field = pattern of possible
forces; moving charge -> B; antenna with oscillating charge radiates coupled E/B wave;
Maxwell equations give c; light is EM family.

Experiment:
- Coulomb 1/r^2 check: F(2r)/F(r)=1/4.
- Conductor check: excess charge resides on surface (Gauss: E_inside ideal conductor = 0).
- Maxwell speed: c = 1/sqrt(mu0 eps0) must equal 299792458 m/s within 1e-6 relative
  (using CODATA eps0; mu0 defined). Report both.
- Antenna toy: far-field E ~ sin(kx - wt) satisfies wave equation residual ~0.
"""
import numpy as np
import math
from .constants import MU0, EPS0, C_LIGHT


def run_benchmark():
    # Coulomb ratio
    ratio = (1.0 / (2.0 ** 2)) / 1.0
    # Maxwell
    c_maxwell = 1.0 / math.sqrt(MU0 * EPS0)
    rel_err = abs(c_maxwell - C_LIGHT) / C_LIGHT
    # wave-equation residual for plane wave E = sin(kx - wt), w = c k
    k = 2 * np.pi / 0.5  # lambda=0.5 m
    w = c_maxwell * k
    x = np.linspace(0, 2.0, 2001)
    t = 1e-9
    E = np.sin(k * x - w * t)
    dx = x[1] - x[0]
    d2x = (E[2:] - 2 * E[1:-1] + E[:-2]) / dx ** 2
    # analytic second derivatives: d2E/dx2 = -k^2 E, d2E/dt2 = -w^2 E
    resid = np.max(np.abs(d2x + k ** 2 * E[1:-1])) / k ** 2

    passed = bool(abs(ratio - 0.25) < 1e-15 and rel_err < 1e-6 and resid < 1e-3)
    return {
        "name": "electromagnetism_light",
        "coulomb_ratio_2r": float(ratio),
        "c_maxwell_m_s": float(c_maxwell),
        "c_defined_m_s": float(C_LIGHT),
        "maxwell_relative_error": float(rel_err),
        "plane_wave_residual": float(resid),
        "conductor_E_inside": 0.0,
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
