# Boom mould v4: closed three-piece tool (draft, 2 Nov 2026)

Status: draft for the structures team, not signed off by the council. Nothing here is cut yet.
It supersedes the two-piece oven tool in `../tooling_spec_and_cutlist.md` for the autoclave route.

## Concept

- **A and B**: two lower blocks, side by side on a base plate. Each has a rounded top inner corner (the tool face).
  The prepreg wraps over that corner and runs down between them, so A and B clamp the V and the two flanges co-cure
  back to back into the 10 mm web (web lands 0.40 apart).
- **C**: a silicone top plug (Mold Max XLS II, 204 C), cast in place on the closed A+B pair, with a drilled 30 x 3
  aluminium spine in its top. Under autoclave pressure it presses normal to every flange face, down to about 3 mm
  above the web root. A rigid wooden top piece would stop at about 7 mm (the flanges meet at zero angle).
- **Envelope bag** round A + B + C + base, breather under it, vacuum take-off through the bag.
- This follows the Caltech TRAC process (Leclerc, Pedivellano and Pellegrino 2018): bolted mandrels, silicone V plug,
  bag round everything, autoclave cure.

## Spring-in: the 0.835 factor is the right sign

Leclerc et al. measured this process: tool R12.7 at 90 deg cured to R10.6 at 105 deg. The flange curls tighter,
so the tool must be larger than the part. `K_SPRING_IN = 0.835` in `params.py` is exactly 10.6 / 12.7, and
`R_MANDREL = 15.1 / 0.835 = 18.08 mm` is right for Caltech's 0.05-0.07 mm thin-ply.

A draft earlier on 2 Nov (calc3, R14.83) flipped the sign and would have cured near R12.4; it is withdrawn.
The older notes in `../README.md` and `../thermal_tolerances_analysis.md` estimated 1 to 2 deg of spring-in;
the measured value on this process is 15 deg (90 to 105).

Our flange is 0.2 mm woven, which probably springs in less, and the bracket depends on the model
(constant radius ratio gives R15.2 to R18.0; constant curvature change gives R19.6). So:
cure coupon pairs at R15.2, R16.5, R18.0 and R19.6, rough the long blocks only, and finish their arc once the
coupons are read. A convex corner can be recut smaller, never larger.

## Key numbers (from `calc4_output.txt`)

| Item | Value |
|---|---|
| Block | 390 x 30.0 x 54, one 35 mm phenolic birch strip each, sheet parallel to the web (no glueline) |
| Clamping | 5 x M6 at 2 N m (about 1.5 kN each, about 2 MPa on the web); 2 reamed 6 mm dowels |
| Autoclave on the web | 1.4 to 2.9 MPa extra at 3 to 7 bar gauge + vacuum (net area ratio 3.6) |
| Butt faces | relieved 0.5 each side; 0.36 mm stops at the trim ends only |
| Bleed | 1 x 1 mm gallery 10 mm below the root |
| Plug | 390 x 60, about 0.47 kg silicone, cast over a 0.22-0.25 mm spacer; no FEP across the V |
| Plug growth | 15.2 mm free over 390 at 150 C, hence the aluminium spine |

## Materials in the autoclave

Imperial's composites autoclave is not the limit (the Composites Centre lists 450 C and 28 bar). The wood is:
phenolic birch ply is fine for a cure at or below about 130 C, baked dry and sealed. For 150 to 180 C, cut the
same drawing in 6082 aluminium, as Caltech did. No bonded aluminium liner: the CTE mismatch (about 1 mm over 390 mm
at 130 K) bows the tool or tears the bond. Sources and URLs: `research-v4-autoclave.md`.

## Files

- `calc4.py` -> `calc4_output.txt`: every number above, tagged [src], [der] or [assume].
- `drawing4.py` -> `mould_v4.png`, `.pdf`, `.dxf`: section, exploded view, root detail, side elevation.
- `review-v4-adversarial.md`: the adversarial review and what it changed.

## Open questions for the team

1. Which prepreg and what cure temperature (wood at or below 130 C, aluminium above)?
2. Will the lab accept wood tooling in the autoclave, and what release and sealant do they stock?
3. Is the layup woven [0, 45] 2 x 0.1 mm? Thin-ply UD would spring in nearer Caltech's 17%.
