# Code guide

How the analysis code in this repository is put together, how to run it, and how to change it. Numbers below were produced by running the code at commit a9be8db.

## Run it

```bash
python run_all.py all --quick      # all three analyses, abbreviated bistability sweep (about 2 s)
python run_all.py sizing           # geometry, strains, stress, safety factor, spool size
python run_all.py second-moment    # section properties and angle sweep, writes a PNG
python run_all.py bistability      # layup sweep, writes bistability_results.json
pytest -v                          # 17 tests
```

Requires `numpy` and `matplotlib`. `composipy` is optional: if it is installed `bistability.py` uses it, otherwise it uses its own Classical Laminate Theory solver.

## Layout

```
run_all.py                              command line entry point (argparse sub-commands)
Composite Booms/Scripts/
    params.py                           every boom dimension and material constant, SI units
    sizing.py                           geometry, strain, stress, microbuckling, packaging
    second_moment.py                    thin-shell section properties, angle sweep, profile plot
    bistability.py                      Classical Laminate Theory (CLT) and the Lee and Fernandez criterion
    Sizing Script.py                    wrapper kept for the old file name
    Second_Moment_of_Area.py            wrapper kept for the old file name
    Bistability Script.py               wrapper kept for the old file name
tests/                                  one test file per module plus the command line
frame_interface/cad/frame_geometry.py   Fusion 360 script, not part of the analysis suite
```

`run_all.py` adds `Composite Booms/Scripts` to `sys.path` and imports the modules by plain name. Each module also tries `from . import params` first, so it works both as a package and as a script.

## Data flow

```
params.py --> sizing.py          run_sizing_report() -> dict(geometry, strains, stresses, failure, packaging)
params.py --> second_moment.py   calculate_thin_shell_properties() -> dict;  sweep_angle() -> dict
bistability.py                   own defaults (see Known gaps); does not read params.py
```

All functions take SI units (metres, pascals, radians) and return dictionaries. Printing is separate (`print_report`, `print_summary`), so the calculators can be imported without side effects.

## sizing.py

| Function | Computes | Key formula |
|---|---|---|
| `calculate_geometry` | arc length, flattened height, area, mass, mandrel radius | `s = R*theta`; `H = s + w`; `A = 2*t*(s + w)`; `R_mandrel = R / 0.835` |
| `calculate_strains` | flattening and coiling strain, minimum hub radius | `eps = t / (2*R)`; `R_hub_min = t / (2*eps_yield)` |
| `calculate_stresses` | nominal and peak coiling stress | `sigma = E*t / (2*R_hub)`; peak = `scf` x nominal, `scf = 2.8` |
| `calculate_failure` | microbuckling strength, allowable, safety factor | `sigma_c = G12 / (1 + phi/gamma_y)`; allowable = min(sigma_c, `SIGMA_C_LIMIT`); `SF = allowable / peak` |
| `calculate_packaging` | wraps, packed diameter, volume | `n = L / (pi*D_hub)`; `D = D_hub + 2*n*n_booms*2t` |
| `run_sizing_report` | all of the above in order | |

Reference output (defaults): peak stress 284.0 MPa, microbuckling 645.3 MPa, allowable 437.0 MPa (the Ansys compressive limit is the smaller), safety factor 1.54, packed diameter 77.6 mm for one boom.

Modelling choices to know about:
- `calculate_packaging` counts `2t` (0.4 mm) of radius per wrap per boom, while `calculate_strains` uses `t` (one flange). The two assume different things about the flattened tape.
- `n_wraps` uses the hub circumference only, so it overestimates the wraps slightly (the radius grows as it winds).
- `scf = 2.8` is a fixed default with no source in the repository.
- The pass line for the safety factor is 1.5 (`calculate_failure`).

## second_moment.py

`calculate_thin_shell_properties` integrates the wall, not a filled area. Axes: `y` runs from the base of the web up to the flange tips, `x` is the symmetry axis. The web has thickness `2t`, each flange `t`. It returns area, centroid height `y_bar`, `Ixx` (bending that moves the flange tips toward or away from the web), `Iyy`, torsion constant `J`, and `EI = E*I`.

Reference output: area 13.49 mm2, y_bar 15.28 mm, Ixx 839.1 mm4, Iyy 490.6 mm4, J 0.340 mm4, EI_xx 29.8 N m2.

`sweep_angle` varies the flange angle from 5 to 90 degrees at a fixed flattened height (33.7 mm), so the radius changes with the angle. The Ixx maximum lands on the 5 degree edge of the range (R 272 mm, 1,274 mm4): a nearly flat tall plate. Read it as "stiffness rises as the flange flattens", not as a design optimum.

`plot_profile` writes `second_moment_profile.png` next to the module. It uses the `Agg` backend, so it needs no display and no LaTeX.

## bistability.py

- `calculate_abd_matrices_clt(stacking, E1, E2, v12, G12, ply_thickness)` returns the A, B and D matrices for a ply stack (angles in degrees). B is non-zero for unsymmetric stacks.
- `bistability_calculation(stacking_array, material, h, w, R)` applies the Lee and Fernandez (2018) criterion to `[outer, inner, all]` stacks. It reduces each D by `D* = D - B^T A^-1 B`, normalises, and calls the layup bistable when the second derivative of strain energy is positive and the coiling parameter `C_cap` exceeds 0.1.
- `run_batch` tries every stack of the angles -45, 0, 45, 90 for the given outer and inner ply counts, and writes only the bistable ones to the JSON file (overwritten each run).

Defaults here are separate from `params.py`: `h = 22.5 mm`, `w = 5 mm`, `R = 21 mm`, and a unidirectional material (E1 164 GPa, E2 8.55 GPa, v12 0.274, G12 3.51 GPa, ply 0.125 mm).

Reference output: `--quick` evaluates 256 layups and finds 0 bistable, so `bistability_results.json` is `[]`.

## Tests

| File | Covers |
|---|---|
| `tests/test_sizing.py` | geometry, strains, stress, safety factor, packaging against hand values |
| `tests/test_second_moment.py` | thin-shell properties and the angle sweep |
| `tests/test_bistability.py` | ABD solver, default tuple argument, clean JSON overwrite |
| `tests/test_cli.py` | `run_all.py` sub-commands |

## Changing things

- A dimension or material constant: edit `params.py` only. Re-run `pytest`; the tests that compare against hand values will tell you which outputs moved.
- A new analysis: add a module in `Composite Booms/Scripts/` that reads `params.py`, return a dict, keep printing in a separate function, then add a sub-command in `run_all.py` and a test file.
- Tests compare to hand-computed values; if a deliberate model change moves them, update the expected value and say why in the commit message.

## Known gaps

See `docs/REVIEW-NOTES.md`.
