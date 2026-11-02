# Svarog TRAC boom, 3D model

Parametric model of the TRAC boom: deployed (2.1 m), coiled on a hub, and a spool with the coiled boom. Built by
`trac_boom_model.py` from `Composite Booms/Scripts/params.py`, so the numbers have one source. The section is checked against
`Composite Booms/Sims+CAD/Composite Boom.step` (area 13.4876 mm2, arc radii R15.0 / R15.2, 30.4 x 25.2 mm) every run; the
results are in `model_check.txt`. The dimensions table is `DIMENSIONS.md`.

| File | What |
|---|---|
| `trac_boom_deployed_2100.stl` / `.step` | boom, 2100 mm, deployed |
| `trac_boom_coiled.stl` / `.step` | flattened tape wound on the 35 mm hub, 9.02 wraps, 2100 mm of boom |
| `spool_with_coiled_boom.stl` / `.step` | one spool (hub + two end discs) carrying one coiled boom |
| `spool_empty.stl` / `.step` | the spool alone |
| `section.png` | the cross-section |

Decided at the 2 Nov structures session: bistable booms, four separate spools (one per boom). Not decided: the drive (one
motor with gears, or four motors). So the spool has no bore, shaft or gears; the end discs (2 mm thick, 2 mm over the coil)
and the 0.01 mm gap between wraps are drawing aids, marked INDICATIVE in the script.

Things to know:
- The tape is modelled as `sizing.py` counts it: height web + one arc length (33.72 mm), thickness two flanges (0.4 mm). `docs/REVIEW-NOTES.md` lists the flattened thickness as an open point.
- The STEP `Composite Boom Full Length.step` is 3000 mm long; `params.py` and this model use 2.1 m.
- The deployed STL mass check: 28 324 mm3 x 1451 kg/m3 = 41.1 g per boom, 164 g for four, as in the specification.

Rebuild: `pip install cadquery && python boom_3d/trac_boom_model.py`.
