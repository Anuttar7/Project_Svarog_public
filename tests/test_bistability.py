import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Composite Booms", "Scripts")))

from bistability import calculate_abd_matrices_clt, bistability_calculation, run_batch


def test_clt_solver_symmetric_layup_zero_b_matrix():
    # Symmetric layup [0/90/90/0] must have B matrix = 0
    A, B, D = calculate_abd_matrices_clt(
        stacking=[0, 90, 90, 0],
        E1=164e9,
        E2=8.55e9,
        v12=0.274,
        G12=3.51e9,
        ply_thickness=0.125e-3,
    )
    import numpy as np
    assert np.allclose(B, 0.0, atol=1e-8)
    assert A[0, 0] > 0
    assert D[0, 0] > 0


def test_clt_solver_unsymmetric_layup_nonzero_b_matrix():
    # Unsymmetric layup [0/90] has nonzero B matrix
    A, B, D = calculate_abd_matrices_clt(
        stacking=[0, 90],
        E1=164e9,
        E2=8.55e9,
        v12=0.274,
        G12=3.51e9,
        ply_thickness=0.125e-3,
    )
    import numpy as np
    assert not np.allclose(B, 0.0, atol=1e-3)


def test_outer_counts_tuple_iteration_bug_fixed():
    # Upstream failed with TypeError: 'int' object is not iterable when outer_counts=(2)
    # With outer_counts=(2,), it iterates properly as a 1-tuple
    mat = {
        "UD": {
            "E1": 164.0e9,
            "E2": 8.55e9,
            "v12": 0.274,
            "G12": 3.51e9,
            "ply_thickness": 0.125e-3,
            "composipy_mat": None,
        }
    }
    results = run_batch(
        ply_angles=[0, 90],
        outer_counts=(2,),
        inner_counts=(2,),
        materials=mat,
        h=2.25e-2,
        w=0.5e-2,
        R=21e-3,
    )
    # 2 angles ^ 2 outer * 2 angles ^ 2 inner = 4 * 4 = 16 cases
    assert len(results) == 16
    assert all("bistable" in r for r in results)


def test_clean_json_overwrite(tmp_path):
    out_file = str(tmp_path / "test_bistability.json")
    mat = {
        "UD": {
            "E1": 164.0e9,
            "E2": 8.55e9,
            "v12": 0.274,
            "G12": 3.51e9,
            "ply_thickness": 0.125e-3,
            "composipy_mat": None,
        }
    }
    run_batch(
        ply_angles=[0, 45],
        outer_counts=(2,),
        inner_counts=(2,),
        materials=mat,
        out_file=out_file,
    )
    assert os.path.isfile(out_file)
