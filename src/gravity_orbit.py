"""
03 — Gravity + Newton cannon + orbit (7.9 km/s, 1/r^2).

Claims: Moon falling; airless-Earth cannon -> orbit when surface curves away as fast
as projectile falls; circular speed near surface ~7.9 km/s; force 1/4 at 2x distance.

Experiment (2-D point mass, no air):
- Verify v1 = sqrt(GM/R) matches V1_ORBITAL constant within 0.1%.
- Verify inverse-square: F(2R)/F(R) = 1/4 exactly.
- Integrate circular orbit with velocity-Verlet for one period; check radius drift <2%
  and energy drift <2%. Gentle shot (e.g. 6 km/s) must re-impact (r < R).
- Moon check: a_moon = GM/d^2 with d=384400 km -> ~0.0027 m/s^2, and centripetal
  v^2/d with v=2pi d/T (T=27.32 d) agrees within 2%.
"""
import numpy as np
from .constants import G_GRAV, M_EARTH, R_EARTH, V1_ORBITAL


def accel(pos):
    r = np.linalg.norm(pos)
    return -G_GRAV * M_EARTH * pos / r ** 3


def run_benchmark():
    # 1. v1 check
    v1 = float(np.sqrt(G_GRAV * M_EARTH / R_EARTH))
    v1_err = abs(v1 - V1_ORBITAL) / V1_ORBITAL
    v1_kms = v1 / 1000.0

    # 2. inverse square
    F1 = G_GRAV * M_EARTH * 1.0 / R_EARTH ** 2
    F2 = G_GRAV * M_EARTH * 1.0 / (2 * R_EARTH) ** 2
    ratio = F2 / F1

    # 3. circular orbit integration (velocity Verlet), one period
    T = 2 * np.pi * np.sqrt(R_EARTH ** 3 / (G_GRAV * M_EARTH))
    dt = 5.0
    steps = int(T / dt)
    pos = np.array([R_EARTH, 0.0])
    vel = np.array([0.0, v1])
    r0 = np.linalg.norm(pos)
    E0 = 0.5 * np.dot(vel, vel) - G_GRAV * M_EARTH / r0
    impacted = False
    for _ in range(steps):
        a = accel(pos)
        vel_half = vel + 0.5 * a * dt
        pos = pos + vel_half * dt
        if np.linalg.norm(pos) < R_EARTH:
            impacted = True
            break
        a_new = accel(pos)
        vel = vel_half + 0.5 * a_new * dt
    r1 = float(np.linalg.norm(pos))
    E1 = float(0.5 * np.dot(vel, vel) - G_GRAV * M_EARTH / r1)
    radius_drift = abs(r1 - r0) / r0
    energy_drift = abs(E1 - E0) / abs(E0)

    # 4. gentle shot must fall back: v=6000 m/s tangential -> suborbital
    pos2 = np.array([R_EARTH, 0.0])
    vel2 = np.array([0.0, 6000.0])
    fell = False
    for _ in range(20000):
        a = accel(pos2)
        vel2 = vel2 + a * dt
        pos2 = pos2 + vel2 * dt
        if np.linalg.norm(pos2) < R_EARTH:
            fell = True
            break
        if np.linalg.norm(pos2) > 3 * R_EARTH:
            break

    # 5. Moon consistency
    d_moon = 384400e3
    T_moon = 27.321661 * 86400.0
    a_grav = G_GRAV * M_EARTH / d_moon ** 2
    v_moon = 2 * np.pi * d_moon / T_moon
    a_cent = v_moon ** 2 / d_moon
    moon_err = abs(a_grav - a_cent) / a_grav

    passed = bool(
        v1_err < 1e-9
        and abs(ratio - 0.25) < 1e-12
        and 7.5 < v1_kms < 8.2
        and (not impacted)
        and radius_drift < 0.02
        and energy_drift < 0.02
        and fell
        and moon_err < 0.02
    )
    return {
        "name": "gravity_orbit",
        "v1_m_s": v1,
        "v1_km_s": v1_kms,
        "v1_target_km_s": 7.9,
        "inverse_square_ratio_2R": float(ratio),
        "orbit_period_s": float(T),
        "radius_drift": float(radius_drift),
        "energy_drift": float(energy_drift),
        "gentle_shot_fell_back": bool(fell),
        "moon_a_grav": float(a_grav),
        "moon_a_centripetal": float(a_cent),
        "moon_relative_error": float(moon_err),
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
