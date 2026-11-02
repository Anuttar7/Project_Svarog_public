"""
Second Moment of Area Calculator (Thin Shell Integration)

Calculates the section properties (Area, Centroid, Ixx, Iyy, J, EI) of a TRAC boom
using thin-walled shell mechanics rather than filled planar area integrals.

Geometry:
- Web: Length w, wall thickness 2*t (bonded land)
- Flanges: Two circular arc shells of radius R, angle theta, thickness t each
"""

import math
import os
import numpy as np
try:
    from . import params
except ImportError:
    import params


def calculate_thin_shell_properties(
    R: float = params.R_CURED,
    theta_rad: float = params.THETA_RAD,
    w: float = params.WEB_WIDTH,
    t: float = params.THICKNESS,
    E: float = params.E_WOVEN_AXIAL,
) -> dict:
    """
    Computes exact closed-form thin-shell second moments of area.
    Coordinates:
      x = 0 is plane of symmetry (web lies along y from 0 to w).
      y = 0 is the base of the flat web.
    """
    # Flange arc length
    s = R * theta_rad

    # Cross-sectional area: web (length w, thickness 2t) + two flanges (length s, thickness t)
    A_web = w * (2.0 * t)
    A_flanges = 2.0 * (s * t)
    A_total = A_web + A_flanges

    # First moment about base y=0: Q_x = integral(y * dA)
    # Web: integral_0^w y * (2t) dy = t * w^2
    Q_x_web = t * (w ** 2)
    # Flanges: 2 * integral_0^theta (w + R*sin(phi)) * t * R dphi
    # = 2 * t * R * [w * theta + R * (1 - cos(theta))]
    Q_x_flanges = 2.0 * t * R * (w * theta_rad + R * (1.0 - math.cos(theta_rad)))
    Q_x = Q_x_web + Q_x_flanges

    # Centroid
    y_bar = Q_x / A_total
    x_bar = 0.0  # By symmetry

    # Second moment Ixx,0 about y=0:
    # Web: integral_0^w y^2 * (2t) dy = (2/3) * t * w^3
    Ixx_web_0 = (2.0 / 3.0) * t * (w ** 3)

    # Flanges: 2 * integral_0^theta (w + R*sin(phi))^2 * t * R dphi
    # Expansion: w^2 + 2*w*R*sin(phi) + R^2*sin^2(phi)
    # int sin^2(phi) = theta/2 - sin(2*theta)/4
    int_sin2 = theta_rad / 2.0 - math.sin(2.0 * theta_rad) / 4.0
    Ixx_flanges_0 = 2.0 * t * R * (
        (w ** 2) * theta_rad
        + 2.0 * w * R * (1.0 - math.cos(theta_rad))
        + (R ** 2) * int_sin2
    )
    Ixx_0 = Ixx_web_0 + Ixx_flanges_0

    # Parallel axis theorem: Ixx about centroidal axis
    Ixx = Ixx_0 - A_total * (y_bar ** 2)

    # Second moment Iyy about symmetry axis x=0:
    # Web lies along x=0, so its Iyy is (w * (2t)^3) / 12 (thin wall: negligible, but included)
    Iyy_web = (w * ((2.0 * t) ** 3)) / 12.0

    # Flanges: 2 * integral_0^theta (R*(1 - cos(phi)))^2 * t * R dphi
    # (1 - cos(phi))^2 = 1 - 2*cos(phi) + cos^2(phi)
    # int cos^2(phi) = theta/2 + sin(2*theta)/4
    int_cos2 = theta_rad / 2.0 + math.sin(2.0 * theta_rad) / 4.0
    int_term_yy = theta_rad - 2.0 * math.sin(theta_rad) + int_cos2
    Iyy_flanges = 2.0 * t * (R ** 3) * int_term_yy
    Iyy = Iyy_web + Iyy_flanges

    # St. Venant Torsion Constant for open thin-walled shell: J = sum(1/3 * b_i * t_i^3)
    J_torsion = (1.0 / 3.0) * w * ((2.0 * t) ** 3) + (2.0 / 3.0) * s * (t ** 3)

    # Bending stiffnesses
    EI_xx = E * Ixx
    EI_yy = E * Iyy

    return {
        "R": R,
        "theta_deg": math.degrees(theta_rad),
        "theta_rad": theta_rad,
        "w": w,
        "t": t,
        "area": A_total,
        "y_bar": y_bar,
        "Ixx": Ixx,
        "Iyy": Iyy,
        "J_torsion": J_torsion,
        "EI_xx": EI_xx,
        "EI_yy": EI_yy,
    }


def sweep_angle(
    h_flattened: float = 33.7e-3,
    w: float = params.WEB_WIDTH,
    t: float = params.THICKNESS,
    n_points: int = 200,
) -> dict:
    """
    Sweeps opening angle from 5 deg to 90 deg at fixed flattened height
    to find the angle maximizing thin-shell bending stiffness.
    """
    angles_deg = np.linspace(5.0, 90.0, n_points)
    angles_rad = np.deg2rad(angles_deg)

    # At fixed flattened height, arc length s = h_flattened - w = R * theta -> R = (h - w) / theta
    radii = (h_flattened - w) / angles_rad

    ixx_vals = np.zeros(n_points)
    iyy_vals = np.zeros(n_points)

    for i in range(n_points):
        props = calculate_thin_shell_properties(radii[i], angles_rad[i], w, t)
        ixx_vals[i] = props["Ixx"]
        iyy_vals[i] = props["Iyy"]

    max_ixx_idx = int(np.argmax(ixx_vals))
    max_iyy_idx = int(np.argmax(iyy_vals))

    return {
        "angles_deg": angles_deg,
        "radii": radii,
        "ixx_vals": ixx_vals,
        "iyy_vals": iyy_vals,
        "max_ixx": {
            "val": float(ixx_vals[max_ixx_idx]),
            "angle_deg": float(angles_deg[max_ixx_idx]),
            "radius": float(radii[max_ixx_idx]),
        },
        "max_iyy": {
            "val": float(iyy_vals[max_iyy_idx]),
            "angle_deg": float(angles_deg[max_iyy_idx]),
            "radius": float(radii[max_iyy_idx]),
        },
    }


def plot_profile(props: dict, save_path: str = None) -> str:
    """
    Generates cross-sectional profile plot without LaTeX dependency.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    R = props["R"]
    theta = props["theta_rad"]
    w = props["w"]

    phi = np.linspace(0, theta, 100)
    x_right = R * (1.0 - np.cos(phi)) * 1e3  # [mm]
    y_right = (w + R * np.sin(phi)) * 1e3    # [mm]

    x_left = -x_right
    y_left = y_right

    plt.figure(figsize=(7, 5))
    plt.plot(x_right, y_right, "b-", lw=2, label="Right Flange")
    plt.plot(x_left, y_left, "r-", lw=2, label="Left Flange")
    plt.plot([0, 0], [0, w * 1e3], "k-", lw=3, label="Bonded Web")
    plt.axhline(props["y_bar"] * 1e3, color="gray", linestyle="--", label=f"Centroid (y={props['y_bar']*1e3:.1f} mm)")

    plt.title(f"Svarog TRAC Boom Thin-Shell Cross Section\n(R={R*1e3:.1f} mm, theta={props['theta_deg']:.0f} deg, w={w*1e3:.1f} mm)")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.grid(True, alpha=0.3)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend(loc="upper left")

    out_file = save_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "second_moment_profile.png")
    plt.savefig(out_file, dpi=150, bbox_inches="tight")
    plt.close()
    return out_file


def print_report(props: dict):
    print("=" * 80)
    print("TRAC BOOM SECOND MOMENT OF AREA REPORT (THIN-SHELL FORMULATION)")
    print("=" * 80)
    print(f"Inputs:")
    print(f"  Flange Mid-Surface Radius (R):  {props['R']*1000:.2f} mm")
    print(f"  Opening Subtended Angle:        {props['theta_deg']:.1f} deg ({props['theta_rad']:.3f} rad)")
    print(f"  Web Width (bonded land):        {props['w']*1000:.2f} mm")
    print(f"  Single Wall Thickness (t):      {props['t']*1e6:.1f} um ({props['t']*1000:.3f} mm)")
    print("-" * 80)
    print(f"Thin-Shell Section Properties:")
    print(f"  Cross-Sectional Area (A):       {props['area']*1e6:.2f} mm^2")
    print(f"  Centroid Location (y_bar):      {props['y_bar']*1000:.2f} mm (from web bottom)")
    print(f"  Ixx (bending perp to web):      {props['Ixx']*1e12:.1f} mm^4  ({props['Ixx']:.4e} m^4)")
    print(f"  Iyy (bending along web axis):   {props['Iyy']*1e12:.1f} mm^4  ({props['Iyy']:.4e} m^4)")
    print(f"  Torsion Constant (J):           {props['J_torsion']*1e12:.3f} mm^4")
    print(f"  Bending Stiffness EI_xx:        {props['EI_xx']:.2f} N m^2")
    print(f"  Bending Stiffness EI_yy:        {props['EI_yy']:.2f} N m^2")
    print("=" * 80)


if __name__ == "__main__":
    props = calculate_thin_shell_properties()
    print_report(props)
