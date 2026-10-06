"""
Reference constants (CODATA 2018 / IAU / NIST values used as ground truth).

Every benchmark compares simulation output against these, not against itself.
Sources verified via web research 2026-10-06:
- Museo Galileo inclined-plane / IMEKO 2025-2026 reconstructions (odd numbers 1:3:5:7, s ~ t^2)
- NIST Putting Einstein to the Test (1905 SR, GPS 38 us/day)
- GPS relativity review (Ashby, PMC5253894): SV offset +442.5e-12 measured vs +446.5e-12 predicted
- Maxwell c = 1/sqrt(mu0*eps0); mu0 exact 4pi*1e-7, c exact 299792458 m/s (SI 2019 redefinition)
- First circular-orbit speed near Earth ~7.9 km/s (Newton cannon)
- Standard Model counting: 12 matter fermions + 4 gauge-boson types (photon, gluon, W, Z) + Higgs = 17 named entries
- Cosmic budget ~5% ordinary matter (Planck 2018: 4.9% baryonic, 26.8% dark matter, 68.3% dark energy)
"""
import math

# Exact SI (2019 redefinition)
C_LIGHT = 299792458.0  # m/s exact
MU0 = 4e-7 * math.pi  # N/A^2 exact (prior exact; kept for Maxwell derivation check)
EPS0 = 8.8541878128e-12  # F/m (CODATA 2018)
# Derived Maxwell speed — must match C_LIGHT within tolerance
C_MAXWELL = 1.0 / math.sqrt(MU0 * EPS0)

G_GRAV = 6.67430e-11  # m^3 kg^-1 s^-2 (CODATA 2018)
M_EARTH = 5.97237e24  # kg
R_EARTH = 6371000.0  # m mean radius
G_SURFACE = 9.80665  # m/s^2 standard gravity

# First cosmic velocity v1 = sqrt(GM/R) ~ 7.9 km/s
V1_ORBITAL = math.sqrt(G_GRAV * M_EARTH / R_EARTH)  # ~7909 m/s

MUON_LIFETIME = 2.197e-6  # s rest lifetime (~2.2 us)
ELECTRON_MASS_KG = 9.1093837015e-31
ELECTRONVOLT_J = 1.602176634e-19

# GPS relativity: net +38 us/day faster in orbit (SR -7 us/day + GR +45 us/day)
GPS_NET_US_PER_DAY = 38.0
GPS_SR_US_PER_DAY = -7.0
GPS_GR_US_PER_DAY = 45.0

# Cosmology (Planck 2018 TT,TE,EE+lowE+lensing+BAO)
OMEGA_B = 0.049
OMEGA_CDM = 0.268
OMEGA_LAMBDA = 0.683
H0_KM_S_MPC = 67.4
