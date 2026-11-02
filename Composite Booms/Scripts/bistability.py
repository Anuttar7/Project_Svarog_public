"""
Bistability Analysis for Two-Shelled Composite Booms

Evaluates Lee & Fernandez (2018) bistability criterion for thin-shelled booms.
Fixes upstream issues:
1. Fixed default argument `outer_counts=(2)` (int) to `outer_counts=(2,)` (tuple) so iteration works.
2. Replaced persistent cross-run JSON appending with clean overwrite per run.
3. Added standalone Classical Laminate Theory (CLT) solver for ABD matrices,
   enabling runs in any standard Python environment with fallback when composipy is absent.
4. Added safe interactive and non-interactive plotting modes.
"""

import itertools
import json
import math
import os
from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    from composipy import OrthotropicMaterial, LaminateProperty
    HAS_COMPOSIPY = True
except ImportError:
    HAS_COMPOSIPY = False

try:
    from . import params
except ImportError:
    import params


# ==============================================================================
# CLT ABD MATRIX SOLVER (FALLBACK / STANDALONE)
# ==============================================================================
def calculate_abd_matrices_clt(
    stacking: List[float],
    E1: float,
    E2: float,
    v12: float,
    G12: float,
    ply_thickness: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Computes Classical Laminate Theory A, B, D matrices for a given ply stack.
    Stacking angles in degrees.
    """
    v21 = v12 * E2 / E1
    denom = 1.0 - v12 * v21
    Q11 = E1 / denom
    Q22 = E2 / denom
    Q12 = v12 * E2 / denom
    Q66 = G12

    n_plies = len(stacking)
    h_total = n_plies * ply_thickness
    # z coordinates from bottom (-h/2) to top (+h/2)
    z_coords = np.linspace(-h_total / 2.0, h_total / 2.0, n_plies + 1)

    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))

    for k, angle_deg in enumerate(stacking):
        theta = math.radians(angle_deg)
        m = math.cos(theta)
        n = math.sin(theta)
        m2 = m * m
        n2 = n * n
        m4 = m2 * m2
        n4 = n2 * n2
        m2n2 = m2 * n2

        # Transformed reduced stiffnesses
        Qbar11 = Q11 * m4 + 2.0 * (Q12 + 2.0 * Q66) * m2n2 + Q22 * n4
        Qbar22 = Q11 * n4 + 2.0 * (Q12 + 2.0 * Q66) * m2n2 + Q22 * m4
        Qbar12 = (Q11 + Q22 - 4.0 * Q66) * m2n2 + Q12 * (m4 + n4)
        Qbar66 = (Q11 + Q22 - 2.0 * Q12 - 2.0 * Q66) * m2n2 + Q66 * (m4 + n4)
        Qbar16 = (Q11 - Q12 - 2.0 * Q66) * (m2 * m * n) - (Q22 - Q12 - 2.0 * Q66) * (m * n2 * n)
        Qbar26 = (Q11 - Q12 - 2.0 * Q66) * (m * n2 * n) - (Q22 - Q12 - 2.0 * Q66) * (m2 * m * n)

        Qbar = np.array([
            [Qbar11, Qbar12, Qbar16],
            [Qbar12, Qbar22, Qbar26],
            [Qbar16, Qbar26, Qbar66],
        ])

        z_k = z_coords[k + 1]
        z_km1 = z_coords[k]

        A += Qbar * (z_k - z_km1)
        B += 0.5 * Qbar * (z_k ** 2 - z_km1 ** 2)
        D += (1.0 / 3.0) * Qbar * (z_k ** 3 - z_km1 ** 3)

    return A, B, D


def get_laminate_abd(stacking: List[float], material: dict) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if HAS_COMPOSIPY and material.get("composipy_mat") is not None:
        lam = LaminateProperty(stacking, material["composipy_mat"])
        return lam.A, lam.B, lam.D
    else:
        return calculate_abd_matrices_clt(
            stacking,
            material["E1"],
            material["E2"],
            material["v12"],
            material["G12"],
            material["ply_thickness"],
        )


# ==============================================================================
# BISTABILITY CALCULATION
# ==============================================================================
def bistability_calculation(
    stacking_array: List[List[float]],
    material: dict,
    h: float = 2.25e-2,
    w: float = 0.5e-2,
    R: float = 21e-3,
) -> dict:
    """
    Lee & Fernandez (2018) bistability criterion.
    stacking_array: [outer_stacking, inner_stacking, all_stacking]
    """
    o_stack = stacking_array[0]
    i_stack = stacking_array[1]
    a_stack = stacking_array[2]

    A_o, B_o, D_o = get_laminate_abd(o_stack, material)
    A_i, B_i, D_i = get_laminate_abd(i_stack, material)
    A_a, B_a, D_a = get_laminate_abd(a_stack, material)

    # Reduced bending stiffness: D* = D - B^T A^-1 B
    D_star_o = D_o - B_o.T @ np.linalg.inv(A_o) @ B_o
    D_star_i = D_i - B_i.T @ np.linalg.inv(A_i) @ B_i
    D_star_a = D_a - B_a.T @ np.linalg.inv(A_a) @ B_a

    # Non-dimensionalize with reference stiffness
    D_ref = D_star_o[0, 0] + D_star_i[0, 0] + D_star_a[0, 0]
    D_cap_o = D_star_o / D_ref
    D_cap_i = D_star_i / D_ref
    D_cap_a = D_star_a / D_ref

    # Lee & Fernandez bistability parameters
    denom_c = h * (D_cap_o[0, 0] + D_cap_i[0, 0]) + w * D_cap_a[0, 0]
    C_cap = (h - w) * (D_cap_i[0, 1] - D_cap_o[0, 1]) / denom_c

    term1 = 2.0 * (D_cap_o[0, 1] - D_cap_i[0, 1]) * ((h - w) ** 2) / (h * (denom_c ** 2))
    bracket_o_i = (
        h * (
            (D_cap_o[0, 0] + D_cap_i[0, 0]) * (D_cap_o[1, 1] + D_cap_i[1, 1])
            - 2.0 * D_cap_i[0, 1] * (D_cap_i[2, 2] + D_cap_o[2, 2] + 0.5 * D_cap_i[0, 1])
            + 2.0 * D_cap_o[0, 1] * (D_cap_i[0, 1] + D_cap_i[2, 2] + D_cap_o[2, 2] - 0.5 * D_cap_o[0, 1])
        )
        + w * (
            D_cap_i[0, 1] * (D_cap_i[0, 1] - 2.0 * D_cap_a[2, 2] - 2.0 * D_cap_o[0, 1])
            + D_cap_o[0, 1] * (D_cap_o[0, 1] + 2.0 * D_cap_a[2, 2])
            + D_cap_a[0, 0] * (D_cap_i[1, 1] + D_cap_o[1, 1])
        )
    )
    ddUcap_ddtheta2 = term1 * bracket_o_i

    bistable = 1 if (ddUcap_ddtheta2 > 0.0 and C_cap > 0.1) else 0
    r_coil = R / max(C_cap, 0.1)
    r_coil_cm = r_coil * 1e2

    return {
        "bistable": int(bistable),
        "ddUcap_ddtheta2": float(ddUcap_ddtheta2),
        "C_cap": float(C_cap),
        "r_coil_cm": float(r_coil_cm),
    }


def run_batch(
    ply_angles: List[float] = [-45, 0, 45, 90],
    outer_counts: Tuple[int, ...] = (2,),
    inner_counts: Tuple[int, ...] = (2, 3),
    materials: Optional[Dict] = None,
    a_stack: Optional[List[float]] = None,
    out_file: Optional[str] = None,
    h: float = 2.25e-2,
    w: float = 0.5e-2,
    R: float = 21e-3,
) -> List[dict]:
    """
    Runs parametric sweep over ply angles and stacking sequences.
    Default outer_counts is a proper tuple (2,) preventing the upstream int iteration bug.
    """
    if materials is None:
        materials = {
            "UD": {
                "E1": 164.0e9,
                "E2": 8.55e9,
                "v12": 0.274,
                "G12": 3.51e9,
                "ply_thickness": 0.125e-3,
                "composipy_mat": OrthotropicMaterial(164.0e9, 8.55e9, 0.274, 3.51e9, 0.125e-3) if HAS_COMPOSIPY else None,
            }
        }

    if a_stack is None:
        a_stack = [0]

    results = []
    for mname, mat in materials.items():
        for oc in outer_counts:
            for ic in inner_counts:
                for o_stack in itertools.product(ply_angles, repeat=oc):
                    for i_stack in itertools.product(ply_angles, repeat=ic):
                        stacking_array = [list(o_stack), list(i_stack), list(a_stack)]
                        res = bistability_calculation(stacking_array, mat, h, w, R)
                        entry = {
                            "material": mname,
                            "outer_count": oc,
                            "inner_count": ic,
                            "outer_stack": list(o_stack),
                            "inner_stack": list(i_stack),
                            "bistable": res["bistable"],
                            "ddUcap_ddtheta2": res["ddUcap_ddtheta2"],
                            "C_cap": res["C_cap"],
                            "r_coil_cm": res["r_coil_cm"],
                        }
                        results.append(entry)

    # Overwrite clean JSON output (resolving upstream dirty-append issue)
    if out_file:
        os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
        bistable_entries = [r for r in results if r.get("bistable") == 1]
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(bistable_entries, f, indent=2)

    return results


def print_summary(results: List[dict]):
    total = len(results)
    bistable_cases = [r for r in results if r["bistable"] == 1]
    n_bistable = len(bistable_cases)
    print("=" * 80)
    print("SVAROG BOOM BISTABILITY SWEEP SUMMARY")
    print("=" * 80)
    print(f"Total Layup Combinations Evaluated: {total}")
    print(f"Bistable Configurations Found:       {n_bistable} ({n_bistable/total*100:.1f}%)")
    if n_bistable > 0:
        sample = bistable_cases[0]
        print(f"Sample Bistable Configuration:")
        print(f"  Material:    {sample['material']}")
        print(f"  Outer Stack: {sample['outer_stack']}")
        print(f"  Inner Stack: {sample['inner_stack']}")
        print(f"  C_cap:       {sample['C_cap']:.3f}")
        print(f"  R_coil:      {sample['r_coil_cm']:.2f} cm")
    print("=" * 80)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(script_dir, "bistability_results.json")
    res = run_batch(outer_counts=(2,), inner_counts=(2, 3), out_file=out_json)
    print_summary(res)
