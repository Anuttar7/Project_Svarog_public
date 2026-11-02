# Review notes: open discrepancies

Found by re-running the code and re-computing the documents' arithmetic at commit a9be8db. Nothing here has been changed in the existing files; each item names the file to fix once the team decides the right value. Status: open.

## Needs a team decision

| # | Where | Finding | Check |
|---|---|---|---|
| 1 | `spool/README.md`, `spool/sizing_calculations.md` | Stowed diameter for four co-wound booms is given as 85 to 88 mm (87.1 mm in the calculation). The calculation's own formula `70 + 2 x (9.5 x 0.45)` gives 78.6 mm; it counts the radial growth of one boom, not four. By area, four 0.4 mm tapes on a 70 mm hub give `D = 2 x sqrt(0.035^2 + 4 x 2.1 x 0.0004 / pi)` = 95.8 mm (98.6 mm with 0.05 mm film). `calculate_packaging(n_booms=4)` gives 100.6 mm. | Side retention flanges are specified at 95 mm outer diameter, smaller than the coil. Also the README says "over 110 mm" radial margin; the calculation gives 56 mm. |
| 2 | `spool/*.md`, `README.md` | 437 MPa is described as the Budiansky-Argon microbuckling allowable. In `sizing.py` it is `SIGMA_C_LIMIT` (the Ansys compressive limit); the Budiansky-Argon value from the code's inputs is 645 MPa. `sizing_calculations.md` derives 990 MPa from other inputs (gamma_y 0.015, phi 2 degrees against the code's 0.0212 and 5 degrees) and an uncomputed "knock-down factor". | `python run_all.py sizing` |
| 3 | `spool/sizing_calculations.md` | The peak stress route (110.8 MPa x K_t 2.5) gives 277 MPa, not the 284.0 MPa the code produces (101.4 MPa x scf 2.8). The 2.8 has no source. | Source or replace `scf` in `sizing.py`. |
| 4 | `deployment_mechanism/README.md` | Coiling moment `E*Ixx/R_hub` = 0.85 N m per boom uses the open-section stiffness (EI 29.8 N m2). A coiled boom is a flattened tape, EI about `E*b*t^3/12` = 8e-4 N m2, giving about 0.02 N m. The figure is conservative but sizes the motor about 40 times high. | Decide which state the motor must work against (flattening cost is separate). |
| 5 | `deployment_mechanism/README.md` vs `specifications.md` | Deploy time 20 to 45 s vs 40 +/- 5 s; retract 30 to 60 s vs 45 +/- 15 s; encoder accuracy 1 mm vs 5 mm. | Pick one set. |
| 6 | `deployment_mechanism/specifications.md` vs `references/references.md` | Lateral load 5 g vs 15 g for the REXUS manual. | Check the manual section. |
| 7 | `frame_interface/*.md` | "4U (200 x 200 x 100 mm)": a 4U CubeSat is 100 x 100 x 400 mm. The 35 x 12 mm egress cut-outs are not in `atrium_1u_reference.step`, which has 40 x 40 mm open faces and X-braces. The model is PLA (`RHO = 1.24` in `frame_geometry.py`), the documents say 6061-T6. `frame_geometry.py` refers to `fe_check.py`, which is not in the repository. | |
| 8 | `Composite Booms/Scripts/bistability.py` | Uses `h = 22.5 mm`, `w = 5 mm`, `R = 21 mm` and a 164 GPa unidirectional material, not `params.py` (R 15.1 mm, w 10 mm, woven 35.5 GPa). Quick sweep: 0 of 256 layups bistable; `bistability_results.json` is `[]`. | Which geometry is the flight design? |
| 9 | `second_moment.py` `sweep_angle` | The Ixx optimum is at the 5 degree edge of the range. | Treat as a trend, not an optimum, or add a manufacturing constraint. |
| 10 | `spool/README.md`, `deployment_mechanism/README.md`, `frame_interface/interface_spec.md` | Hardware details with no source in any `sources.md`: 150:1 gearbox, PEEK/PTFE rollers, 0.05 mm PTFE slip film, Alodine 1200 coating, 2.5 mOhm bonding limit, 95 mm flanges, M3 fasteners, "safety factor > 10 / > 20". | Mark as proposals until the sub-team confirms. |

## Housekeeping

- Fernandez 2017 is NASA/TM-2017-219569 in the `sources.md` files and NASA/TM-2017-219665 in `references/references.md` and `REDACTIONS.md`. One is wrong.
- `references/references.md` and the `sources.md` files cite internal planning notes and task names, and `frame_geometry.py` says it was AI-made. Remove these before the repository is shared beyond its owner.
- `README.md` quotes the upstream packed diameter as 328.5 mm; `print_report` shows 714 mm for "upstream" because it re-runs the old formula with the flattened height (33.7 mm) instead of the 20 mm upstream used.
- `calculate_packaging` counts 0.4 mm of radius per wrap while `calculate_strains` uses one flange (0.2 mm). Decide what the flattened tape thickness is.
- Ansys: neither project has a completed solve (issues #1 and #2).
