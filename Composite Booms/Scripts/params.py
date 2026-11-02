"""
Svarog TRAC Boom Parameters (Single Source of Truth)

Baseline geometry derived from CAD STEP model (Composite Boom.step):
- Flange arc radius: 15.0 mm inside, 15.2 mm outside -> 15.1 mm mid-surface
- Flange subtended angle: 90.0 deg (pi/2 rad)
- Web width (bonded region): 10.0 mm
- Laminate thickness: 0.20 mm per flange (two 0.1 mm woven carbon plies)
- Boom deployed length: 2.1 m (REXUS target)
"""

import math
import numpy as np

# ==============================================================================
# BASELINE CAD GEOMETRY (SI UNITS: meters, radians)
# ==============================================================================
R_CURED = 15.1e-3        # [m] Cured mid-surface flange radius (15.1 mm)
THETA_DEG = 90.0         # [deg] Flange subtended opening angle
THETA_RAD = math.radians(THETA_DEG)  # [rad] pi / 2
WEB_WIDTH = 10.0e-3      # [m] Flat web width (bonded flange land)
THICKNESS = 0.2e-3       # [m] Single flange laminate thickness (200 um)
LENGTH = 2.1             # [m] Full deployed boom length

# Manufacturing & Tooling
# Spring-in: Leclerc et al. 2017/2018 (Caltech TRAC) measured tool R12.7 -> cured R10.6 (90 -> 105 deg),
# so the cured radius is SMALLER than the tool and the tool must be larger: 10.6 / 12.7 = 0.835.
# That is for 0.05-0.07 mm thin-ply; our 0.2 mm woven flange likely springs in less. The tool radius
# is set from coupons at R15.2/16.5/18.0/19.6 mm (boom_mould/v4/README.md); 0.835 gives the R18.08 entry.
K_SPRING_IN = 0.835      # Empirical spring-in factor (R_cured / R_mandrel)
R_MANDREL = R_CURED / K_SPRING_IN  # [m] Required mould/mandrel radius (~18.08 mm)

# ==============================================================================
# LAMINATE MATERIAL PROPERTIES
# ==============================================================================
# Ansys ACP Model Baseline: Epoxy Carbon Woven (230 GPa) Wet
# Layup: [0/90, +/-45] woven fabric, 0.1 mm/ply -> 0.2 mm total per flange
E_WOVEN_AXIAL = 35.5e9   # [Pa] Effective axial laminate tensile/bending modulus
E_UD_AXIAL = 128.0e9     # [Pa] Reference unidirectional modulus (comparison only)
G12 = 3.3e9              # [Pa] In-plane shear modulus (Ansys material.apdl)
TAU_Y = 70.0e6           # [Pa] Matrix shear yield strength
PHI_RAD = math.radians(5.0)  # [rad] Initial fiber misalignment angle (5 deg)
DENSITY = 1451.0         # [kg/m^3] Cured composite density
SIGMA_C_LIMIT = 437.0e6  # [Pa] Longitudinal compressive yield strength (Ansys)
EPS_YIELD = 0.010        # [unitless] Maximum allowable design strain limit (1.0%)

# Default spooling / coiling hub radius for packaging calculations
DEFAULT_R_HUB = 35.0e-3  # [m] 35 mm hub radius (70 mm diameter)
