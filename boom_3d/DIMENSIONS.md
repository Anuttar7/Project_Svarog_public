# Dimensions

## Boom
### Input (Design) Parameters
| Quantity | Value | Source |
|---|---|---|
| Flange mid-surface radius | 15.1 mm | params.py R_CURED |
| Flange inner radius | 15.0 mm | R - t/2 |
| Flange outer radius | 15.2 mm | R + t/2 |
| Flange opening angle | 90.0 deg | params.py THETA_DEG |
| Flange angle subtended at centre | TO BE CONFIRMED | params.py |
| Flange thickness (each) | 0.2 mm | params.py THICKNESS (two 0.1 mm plies) |
| Web height (bonded land) | 10.0 mm | params.py WEB_WIDTH |
| Deployed length | 2.1 m | params.py LENGTH (2.1 m) |
| Flattened tape height | 33.7190 | w + R*theta|
| Flattened tape thickness | 0.400 | 2t |
| Hub radius / diameter | 35.0 / 70.0 | design limitation |

### Derived Parameters
| Quantity | Value | Source |
|---|---|---|
| Occupied Cross Sectional Area | 766.08 mm2 | (15.2 mm + 15.2 mm) x (10 mm + 15.2 mm) |
| Actual Cross Sectional area | 13.4876 mm2 | (10mm*2*0.2mm) + 2*(15.1mm*pi/2) |
| Centroid y-coordinate | 15.28 mm | derived |
| Ixx,c | 890.1 mm4 | derived |
| Iyy,c | 490.62 mm4 | derived |

### Quantities not yet Identified
| Quantity | Value | Source |
|---|---|---|
| Wraps for 2.1 m on the hub | 9.02 | spiral, mid-line length = L |
| Coil outer radius / diameter | 39.10 / 78.20 | hub + wraps x pitch |
| Spool end discs | 2.0 thick, R 41.10 | INDICATIVE, not decided |
| Wrap clearance in the model | 0.01 | INDICATIVE, keeps the spiral a valid solid |

Open points carried from `docs/REVIEW-NOTES.md`: the flattened tape thickness (0.4 mm here, as `sizing.py` counts it) and the
hub radius are the project's own working values, not measured. The CAD STEP `Composite Boom Full Length.step` is 3000 mm;
this model follows params.py (2100 mm).
