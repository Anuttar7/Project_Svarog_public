import pytest
import math
import sys
import os

# Add scripts path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Composite Booms", "Scripts")))

import params
from sizing import (
    calculate_geometry,
    calculate_strains,
    calculate_stresses,
    calculate_failure,
    calculate_packaging,
    run_sizing_report,
)


def test_geometry_calculations():
    geom = calculate_geometry(
        R_cured=15.1e-3,
        theta_rad=math.pi / 2.0,
        w=10.0e-3,
        t=0.2e-3,
        L=2.1,
        k_spring_in=0.835,
        density=1451.0,
    )
    # Arc length s = R * theta = 15.1 * pi/2 = 23.718 mm
    assert math.isclose(geom["arc_length"], 15.1e-3 * math.pi / 2.0, rel_tol=1e-4)
    # Flattened height = s + w = 33.718 mm
    assert math.isclose(geom["flattened_height"], 0.033718, rel_tol=1e-3)
    # Perimeter = 2*s + w = 57.436 mm
    assert math.isclose(geom["perimeter"], 0.057436, rel_tol=1e-3)
    # Area = 2 * t * (s + w) = 2 * 0.2e-3 * 0.033718 = 1.3487e-5 m^2 (13.49 mm^2)
    assert math.isclose(geom["area_cross"] * 1e6, 13.49, rel_tol=1e-2)
    # Total mass = 1451 * 1.3487e-5 * 2.1 = ~41.1 grams
    assert 40.0 < geom["total_mass"] * 1000 < 42.0
    # Required mandrel radius = R_cured / 0.835 = 18.08 mm
    assert math.isclose(geom["R_mandrel"] * 1000, 18.08, rel_tol=1e-2)


def test_strains_within_elastic_limit():
    strains = calculate_strains(
        t=0.2e-3,
        R_cured=15.1e-3,
        R_hub=35.0e-3,
        eps_yield=0.010,
    )
    # Transverse strain: 0.2e-3 / (2 * 15.1e-3) = 0.00662 (0.662%)
    assert math.isclose(strains["eps_transverse"], 0.0066225, rel_tol=1e-3)
    assert strains["transverse_safe"] is True

    # Coiling strain: 0.2e-3 / (2 * 35.0e-3) = 0.002857 (0.286%)
    assert math.isclose(strains["eps_coiling"], 0.0028571, rel_tol=1e-3)
    assert strains["coiling_safe"] is True

    # Strain limit minimum hub radius: 0.2e-3 / (2 * 0.01) = 10.0 mm
    assert math.isclose(strains["R_hub_min_strain"] * 1000, 10.0, rel_tol=1e-4)


def test_stresses_bug_fix_factor_of_two():
    # Verify coiling stress formula uses 2*R in denominator
    # With E = 35.5 GPa, t = 0.2 mm, R_hub = 35 mm:
    # sigma_nominal = 35.5e9 * 0.2e-3 / (2 * 0.035) = 101.43 MPa
    stresses = calculate_stresses(
        E=35.5e9,
        t=0.2e-3,
        R_hub=35.0e-3,
        R_cured=15.1e-3,
        scf=2.8,
    )
    assert math.isclose(stresses["sigma_coiling_nominal"] / 1e6, 101.428, rel_tol=1e-3)
    # Peak stress in transition = 2.8 * 101.43 = 284.0 MPa
    assert math.isclose(stresses["sigma_coiling_peak"] / 1e6, 284.0, rel_tol=1e-2)


def test_safety_factor_passes_on_realistic_hub():
    # Evaluate failure criterion on a 70 mm spool (R = 35 mm)
    stresses = calculate_stresses(E=35.5e9, t=0.2e-3, R_hub=35.0e-3, R_cured=15.1e-3, scf=2.8)
    failure = calculate_failure(stresses["sigma_coiling_peak"])

    # Allowable strength: min(645 MPa, 437 MPa) = 437 MPa
    assert failure["sigma_allowable"] / 1e6 == 437.0
    # Safety factor = 437 / 284.0 = ~1.54 >= 1.5 (PASS)
    assert failure["safety_factor"] >= 1.5
    assert failure["safe"] is True


def test_packaging_bug_fix_radial_buildup():
    # With L = 2.1 m, D_hub = 70 mm (0.07 m):
    # circumference = pi * 0.07 = 0.2199 m -> n_wraps = 9.55 wraps
    pkg = calculate_packaging(L=2.1, D_hub=0.070, t=0.2e-3, fh=33.7e-3, n_booms=1)

    assert math.isclose(pkg["n_wraps"], 9.549, rel_tol=1e-2)
    # Real outer diameter: 70 mm + 2 * 9.55 * 0.4 mm = 77.6 mm
    assert 76.0 < pkg["D_packaged"] * 1000 < 79.0

    # Upstream erroneous calculation produced > 300 mm diameter!
    assert pkg["D_packaged_upstream_err"] * 1000 > 300.0


def test_integrated_report():
    rep = run_sizing_report()
    assert rep["failure"]["safe"] is True
    assert rep["failure"]["safety_factor"] >= 1.5
