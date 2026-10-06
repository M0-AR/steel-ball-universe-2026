"""Pytest gate: every narrative claim must pass its numeric benchmark (except live-data,
which is allowed to degrade to cache but must still be internally consistent)."""
from src import (
    galileo_ramp,
    inertia_newton,
    gravity_orbit,
    energy_entropy,
    waves_sound,
    electromagnetism_light,
    relativity,
    quantum_double_slit,
    standard_model,
    cosmology_gap,
    hidden_patterns,
)


def test_galileo_odd_numbers():
    assert galileo_ramp.run_benchmark()["pass"]


def test_inertia_newton_1687():
    assert inertia_newton.run_benchmark()["pass"]


def test_gravity_orbit_79kms_and_quarter_at_2R():
    r = gravity_orbit.run_benchmark()
    assert r["pass"]
    assert 7.5 < r["v1_km_s"] < 8.2
    assert abs(r["inverse_square_ratio_2R"] - 0.25) < 1e-12


def test_energy_entropy_direction():
    assert energy_entropy.run_benchmark()["pass"]


def test_waves_interference():
    assert waves_sound.run_benchmark()["pass"]


def test_maxwell_light_speed():
    r = electromagnetism_light.run_benchmark()
    assert r["pass"]
    assert r["maxwell_relative_error"] < 1e-6


def test_relativity_1905():
    assert relativity.run_benchmark()["pass"]


def test_quantum_doubleslit():
    assert quantum_double_slit.run_benchmark()["pass"]


def test_standard_model_17():
    r = standard_model.run_benchmark()
    assert r["pass"]
    assert r["total_named_entries"] == 17


def test_cosmology_5pct_and_open_qg():
    r = cosmology_gap.run_benchmark()
    assert r["pass"]
    assert 4.0 < r["baryonic_percent"] < 6.0


def test_hidden_patterns_with_null_control():
    assert hidden_patterns.run_benchmark()["pass"]
