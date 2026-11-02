"""
TRAC Boom Design Calculator (Sizing & Mechanics Analysis)

Corrected formulation addressing upstream bugs:
1. Coiling Stress: Uses sigma = E * t / (2 * R_hub) instead of E * t / R_hub.
2. Coil Packaging: Increments diameter by flattened tape thickness (2*t = 0.4 mm per wrap)
   instead of 2 * flattened_height (40 mm per wrap).
3. Modulus Alignment: Uses woven fabric axial modulus (~35.5 GPa) matching CAD layup,
   with optional UD comparison.
4. Flattened Height: Treats flattened height as arc length (s = R * theta) rather than chord.
5. Safety Factor: Non-circular calculation evaluated at specified hub radius against
   matrix-supported fiber microbuckling.
"""

import math
import numpy as np
try:
    from . import params
except ImportError:
    import params


def calculate_geometry(
    R_cured: float = params.R_CURED,
    theta_rad: float = params.THETA_RAD,
    w: float = params.WEB_WIDTH,
    t: float = params.THICKNESS,
    L: float = params.LENGTH,
    k_spring_in: float = params.K_SPRING_IN,
    density: float = params.DENSITY,
) -> dict:
    """
    Computes cured boom geometry from mid-surface arc and web dimensions.
    All inputs and outputs in SI units (meters, radians, kg).
    """
    # Arc length of each flange: s = R * theta
    s = R_cured * theta_rad

    # Flattened height (web plus one arc length when pressed flat)
    flattened_height = s + w

    # Perimeter of the cross-section
    perimeter = 2.0 * s + w

    # Cross-sectional area: two flanges of thickness t, bonded along web (thickness 2*t)
    # Area = 2 * (s * t) + (w * 2*t) = 2 * t * (s + w)
    # Note: web has two bonded flanges, total thickness = 2*t
    A_cross = 2.0 * t * (s + w)

    # Linear mass and total boom mass
    linear_mass = density * A_cross
    total_mass = linear_mass * L

    # Required mandrel radius before spring-in
    R_mandrel = R_cured / k_spring_in

    return {
        "R_cured": R_cured,
        "theta_rad": theta_rad,
        "theta_deg": math.degrees(theta_rad),
        "web_width": w,
        "thickness": t,
        "length": L,
        "arc_length": s,
        "flattened_height": flattened_height,
        "perimeter": perimeter,
        "area_cross": A_cross,
        "linear_mass": linear_mass,
        "total_mass": total_mass,
        "R_mandrel": R_mandrel,
    }


def calculate_strains(
    t: float = params.THICKNESS,
    R_cured: float = params.R_CURED,
    R_hub: float = params.DEFAULT_R_HUB,
    eps_yield: float = params.EPS_YIELD,
) -> dict:
    """
    Computes transverse flattening and longitudinal coiling strains.
    """
    # Transverse strain from unbending flange to flat plate: eps_22 = t / (2 * R_cured)
    eps_transverse = t / (2.0 * R_cured)

    # Longitudinal strain when wrapping flat tape around hub of radius R_hub: eps_11 = t / (2 * R_hub)
    eps_coiling = t / (2.0 * R_hub)

    # Minimum hub radius to satisfy strain yield limit: R_hub_min = t / (2 * eps_yield)
    R_hub_min_strain = t / (2.0 * eps_yield)

    # Minimum flange radius to allow flattening without yielding
    R_flange_min = t / (2.0 * eps_yield)

    return {
        "eps_transverse": eps_transverse,
        "eps_coiling": eps_coiling,
        "eps_yield": eps_yield,
        "R_hub_evaluated": R_hub,
        "R_hub_min_strain": R_hub_min_strain,
        "R_flange_min": R_flange_min,
        "transverse_safe": eps_transverse <= eps_yield,
        "coiling_safe": eps_coiling <= eps_yield,
    }


def calculate_stresses(
    E: float = params.E_WOVEN_AXIAL,
    t: float = params.THICKNESS,
    R_hub: float = params.DEFAULT_R_HUB,
    R_cured: float = params.R_CURED,
    scf: float = 2.8,
) -> dict:
    """
    Computes nominal and peak coiling stresses.
    Corrects factor-of-2 error in upstream script.
    """
    # Nominal coiling stress in fully coiled cylindrical state: sigma = E * eps = E * t / (2 * R_hub)
    sigma_coiling_nominal = E * t / (2.0 * R_hub)

    # Peak stress in transition region (where boom flattens and bends simultaneously)
    sigma_coiling_peak = scf * sigma_coiling_nominal

    # Transverse flattening stress: sigma_22 = E * t / (2 * R_cured)
    sigma_transverse = E * t / (2.0 * R_cured)

    return {
        "E_modulus": E,
        "sigma_coiling_nominal": sigma_coiling_nominal,
        "sigma_coiling_peak": sigma_coiling_peak,
        "sigma_transverse": sigma_transverse,
        "scf": scf,
    }


def calculate_failure(
    sigma_peak: float,
    G12: float = params.G12,
    tau_y: float = params.TAU_Y,
    phi_rad: float = params.PHI_RAD,
    sigma_c_limit: float = params.SIGMA_C_LIMIT,
) -> dict:
    """
    Evaluates fiber microbuckling compressive failure and safety factor.
    """
    # Matrix yield shear strain
    gamma_y = tau_y / G12

    # Budiansky-Argon fiber microbuckling compressive strength
    # sigma_c = G12 / (1 + phi / gamma_y)
    sigma_microbuckling = G12 / (1.0 + phi_rad / gamma_y)

    # Critical failure strength (use microbuckling or material compressive limit)
    sigma_allowable = min(sigma_microbuckling, sigma_c_limit) if sigma_c_limit else sigma_microbuckling

    # Safety factor in transition zone
    safety_factor = sigma_allowable / sigma_peak

    return {
        "gamma_y": gamma_y,
        "sigma_microbuckling": sigma_microbuckling,
        "sigma_allowable": sigma_allowable,
        "sigma_peak": sigma_peak,
        "safety_factor": safety_factor,
        "safe": safety_factor >= 1.5,
    }


def calculate_packaging(
    L: float = params.LENGTH,
    D_hub: float = 2.0 * params.DEFAULT_R_HUB,
    t: float = params.THICKNESS,
    fh: float = None,
    n_booms: int = 1,
) -> dict:
    """
    Computes spool packaging dimensions.
    Corrects packaging diameter error (thickness vs flattened height).
    """
    # Flattened boom tape thickness (two flanges bonded together)
    t_tape = 2.0 * t

    # Number of wraps around the spool
    circumference_hub = math.pi * D_hub
    n_wraps = L / circumference_hub if circumference_hub > 0 else 0.0

    # Real radial buildup per wrap: each wrap adds n_booms * t_tape to the spool radius,
    # meaning the outer diameter increases by 2 * n_wraps * (n_booms * t_tape)
    D_packaged_correct = D_hub + 2.0 * n_wraps * (n_booms * t_tape)

    # Erroneous upstream calculation for comparison (added 2 * n_wraps * fh)
    fh_val = fh if fh is not None else 20.0e-3
    D_packaged_upstream_err = D_hub + 2.0 * n_wraps * fh_val

    # Packaged cylindrical volume: V = pi * (D/2)^2 * spool_width
    # where spool_width is approximately the flattened height
    spool_width = fh_val
    V_packaged = math.pi * (D_packaged_correct / 2.0) ** 2 * spool_width

    return {
        "n_wraps": n_wraps,
        "t_tape": t_tape,
        "D_hub": D_hub,
        "D_packaged": D_packaged_correct,
        "D_packaged_upstream_err": D_packaged_upstream_err,
        "V_packaged": V_packaged,
    }


def run_sizing_report(
    R_cured: float = params.R_CURED,
    theta_deg: float = params.THETA_DEG,
    w: float = params.WEB_WIDTH,
    t: float = params.THICKNESS,
    L: float = params.LENGTH,
    R_hub: float = params.DEFAULT_R_HUB,
    E: float = params.E_WOVEN_AXIAL,
) -> dict:
    """
    Full integrated sizing pipeline producing complete metrics.
    """
    geom = calculate_geometry(R_cured, math.radians(theta_deg), w, t, L)
    strains = calculate_strains(t, R_cured, R_hub)
    stresses = calculate_stresses(E, t, R_hub, R_cured)
    failure = calculate_failure(stresses["sigma_coiling_peak"])
    pkg = calculate_packaging(L, 2.0 * R_hub, t, geom["flattened_height"])

    return {
        "geometry": geom,
        "strains": strains,
        "stresses": stresses,
        "failure": failure,
        "packaging": pkg,
    }


def print_report(res: dict):
    g = res["geometry"]
    sn = res["strains"]
    st = res["stresses"]
    f = res["failure"]
    p = res["packaging"]

    print("=" * 80)
    print("SVAROG TRAC BOOM SIZING ANALYSIS REPORT (CORRECTED)")
    print("=" * 80)
    print(f"Geometry Baseline (CAD Model):")
    print(f"  Flange Cured Radius (R):        {g['R_cured']*1000:.2f} mm")
    print(f"  Flange Subtended Angle:         {g['theta_deg']:.1f} deg")
    print(f"  Web Width (bonded land):        {g['web_width']*1000:.2f} mm")
    print(f"  Laminate Thickness (per flange):{g['thickness']*1e6:.1f} um ({g['thickness']*1000:.3f} mm)")
    print(f"  Deployed Length:                {g['length']:.2f} m")
    print(f"  Flange Arc Length:              {g['arc_length']*1000:.2f} mm")
    print(f"  Flattened Height (arc + web):   {g['flattened_height']*1000:.2f} mm")
    print(f"  Cross-Sectional Area:           {g['area_cross']*1e6:.2f} mm^2")
    print(f"  Total Boom Mass:                {g['total_mass']*1000:.1f} g ({g['linear_mass']*1000:.2f} g/m)")
    print(f"  Mandrel Radius (spring-in 0.835):{g['R_mandrel']*1000:.2f} mm")
    print("-" * 80)
    print(f"Strain Analysis (Evaluated at Hub Radius R = {sn['R_hub_evaluated']*1000:.1f} mm):")
    print(f"  Transverse Flattening Strain:   {sn['eps_transverse']*100:.3f}% (limit: {sn['eps_yield']*100:.1f}%) -> {'PASS' if sn['transverse_safe'] else 'FAIL'}")
    print(f"  Longitudinal Coiling Strain:    {sn['eps_coiling']*100:.3f}% (limit: {sn['eps_yield']*100:.1f}%) -> {'PASS' if sn['coiling_safe'] else 'FAIL'}")
    print(f"  Minimum Hub Radius by Strain:   {sn['R_hub_min_strain']*1000:.2f} mm (Dia: {sn['R_hub_min_strain']*2000:.2f} mm)")
    print("-" * 80)
    print(f"Stress Analysis (Laminate Modulus E = {st['E_modulus']/1e9:.1f} GPa):")
    print(f"  Nominal Coiling Stress:         {st['sigma_coiling_nominal']/1e6:.1f} MPa")
    print(f"  Peak Transition Stress (SCF={st['scf']}): {st['sigma_coiling_peak']/1e6:.1f} MPa")
    print(f"  Transverse Flattening Stress:   {st['sigma_transverse']/1e6:.1f} MPa")
    print("-" * 80)
    print(f"Failure & Safety Factor Analysis:")
    print(f"  Fiber Microbuckling Strength:   {f['sigma_microbuckling']/1e6:.1f} MPa")
    print(f"  Design Allowable Strength:      {f['sigma_allowable']/1e6:.1f} MPa")
    print(f"  Safety Factor (SF):             {f['safety_factor']:.2f} -> {'SAFE (Adequate)' if f['safe'] else 'FAIL'}")
    print("-" * 80)
    print(f"Spool Packaging Analysis:")
    print(f"  Hub Diameter:                   {p['D_hub']*1000:.1f} mm")
    print(f"  Number of Wraps:                {p['n_wraps']:.1f} wraps")
    print(f"  Tape Thickness (2 plies):       {p['t_tape']*1000:.2f} mm")
    print(f"  Packaged Outer Diameter:        {p['D_packaged']*1000:.1f} mm  (Upstream bug calculated: {p['D_packaged_upstream_err']*1000:.1f} mm)")
    print(f"  Packaged Volume:                {p['V_packaged']*1e6:.1f} cm^3")
    print("=" * 80)


if __name__ == "__main__":
    report = run_sizing_report()
    print_report(report)
