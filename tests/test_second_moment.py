import pytest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Composite Booms", "Scripts")))

from second_moment import calculate_thin_shell_properties, sweep_angle


def test_thin_shell_baseline_cad_values():
    # Evaluate at baseline CAD parameters: R = 15.1 mm, theta = 90 deg, w = 10 mm, t = 0.2 mm
    props = calculate_thin_shell_properties(
        R=15.1e-3,
        theta_rad=math.pi / 2.0,
        w=10.0e-3,
        t=0.2e-3,
        E=35.5e9,
    )
    # Area: ~13.49 mm^2
    assert math.isclose(props["area"] * 1e6, 13.487, rel_tol=1e-2)

    # Centroid: ~15.28 mm from base of web
    assert math.isclose(props["y_bar"] * 1000, 15.28, rel_tol=1e-2)

    # Ixx (parallel to web): ~839 mm^4 (derived in vault Boom-Facts.md)
    assert 835.0 < props["Ixx"] * 1e12 < 845.0

    # Iyy (along web axis): ~490 mm^4 (derived in vault Boom-Facts.md)
    assert 485.0 < props["Iyy"] * 1e12 < 495.0

    # Bending stiffnesses: EI_xx ~ 29.8 N m^2, EI_yy ~ 17.4 N m^2
    assert 29.0 < props["EI_xx"] < 31.0
    assert 17.0 < props["EI_yy"] < 18.0


def test_thin_shell_divergence_from_erroneous_solid_quadrature():
    props = calculate_thin_shell_properties(R=15.1e-3, theta_rad=math.pi / 2.0, w=10.0e-3, t=0.2e-3)

    # In upstream Second_Moment_of_Area.py, solid area integration yielded ~77,312 mm^4
    # Thin shell is 839 mm^4, almost two orders of magnitude lower due to actual thin wall physics
    assert props["Ixx"] * 1e12 < 1000.0


def test_angle_sweep_execution():
    sweep = sweep_angle(h_flattened=33.7e-3, w=10.0e-3, t=0.2e-3, n_points=50)
    assert len(sweep["angles_deg"]) == 50
    assert sweep["max_ixx"]["val"] > 0
    assert sweep["max_iyy"]["val"] > 0
