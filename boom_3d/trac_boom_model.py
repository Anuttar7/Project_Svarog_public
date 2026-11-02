"""Svarog TRAC boom as a parametric 3D model: deployed (2.1 m), coiled on a hub, and a spool per boom.

Run:   python trac_boom_model.py        (needs CadQuery: pip install cadquery)
Reads: ../Composite Booms/Scripts/params.py   (single source of truth for R, theta, web, thickness, length, hub)
Reads: ../Composite Booms/Sims+CAD/Composite Boom.step   (reference section, used only to check the model)
Writes beside this script: STEP + STL of each state, DIMENSIONS.md, model_check.txt.

Coordinates, mm: z along the boom, u across (0 = web centreline), v up from the web root (v = 0).
Section as in the CAD STEP: two 0.2 mm flanges bonded back to back along a 10 mm web, then each flange opens
outward as a 90 deg arc of R15.1 mid-surface. The STEP has the same section (y = 30.2 + u, z = 30 + v).

Nothing here is decided beyond the CAD and params.py. Items marked INDICATIVE are drawing aids, not design.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import cadquery as cq

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.dirname(HERE)
SCRIPTS = os.path.join(REPO, "Composite Booms", "Scripts")
REF_STEP = os.path.join(REPO, "Composite Booms", "Sims+CAD", "Composite Boom.step")


def load_params():
    spec = importlib.util.spec_from_file_location("svarog_params", os.path.join(SCRIPTS, "params.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load_params()
MM = 1000.0
R = P.R_CURED * MM            # mid-surface flange radius
THETA = P.THETA_DEG           # flange opening angle, deg
W = P.WEB_WIDTH * MM          # web height (bonded land)
T = P.THICKNESS * MM          # single flange thickness
L = P.LENGTH * MM             # deployed length
R_HUB = P.DEFAULT_R_HUB * MM  # spool hub radius

R_IN, R_OUT = R - T / 2, R + T / 2
FLAT_H = R * math.radians(THETA) + W        # flattened tape height, sizing.py "flattened_height" (web + one arc)
TAPE_T = 2 * T                              # flattened tape thickness, sizing.py "t_tape" (two flanges)
WRAP_GAP = 0.01   # INDICATIVE: radial clearance between wraps so the spiral solid does not self-touch
DISC_T = 2.0      # INDICATIVE: spool end disc thickness
DISC_OVER = 2.0   # INDICATIVE: end disc radius beyond the outer wrap
SIDE_CLR = 0.5    # INDICATIVE: axial clearance between tape edge and each end disc


# ------------------------------------------------------------------ deployed section
def flange(sign: int) -> cq.Workplane:
    """One flange: web strip (thickness T, height W) then an arc of angle THETA. sign -1 left, +1 right."""
    uc = sign * (T + R_IN)        # arc centre u: web face is R_IN from the centre
    a = math.radians(THETA)

    def pt(r: float, phi: float) -> tuple[float, float]:
        return (uc - sign * r * math.cos(phi), W + r * math.sin(phi))

    # web faces: the bonded face is at u = 0, the free face at u = sign * T; arc inner radius lies on the free face
    return (cq.Workplane("XY").moveTo(0, 0).lineTo(sign * T, 0).lineTo(*pt(R_IN, 0))
            .threePointArc(pt(R_IN, a / 2), pt(R_IN, a)).lineTo(*pt(R_OUT, a))
            .threePointArc(pt(R_OUT, a / 2), pt(R_OUT, 0)).close())


def deployed(length: float = L) -> cq.Workplane:
    return flange(-1).extrude(length).union(flange(1).extrude(length))


# ------------------------------------------------------------------ coiled tape
def spiral_theta_end(length: float, r0: float, pitch: float) -> float:
    """Total angle so the tape mid-line has arc length `length`, mid radius r(th) = r0 + pitch*th/2pi."""
    k = pitch / (2 * math.pi)
    # s(th) = r0*th + k*th^2/2
    return (-r0 + math.sqrt(r0 * r0 + 2 * k * length)) / k


def coiled(length: float = L) -> tuple[cq.Workplane, dict]:
    """Flattened tape (height FLAT_H, thickness TAPE_T) wound on the hub as an Archimedean spiral, z = 0..FLAT_H."""
    pitch = TAPE_T + WRAP_GAP
    r_mid0 = R_HUB + TAPE_T / 2
    th_end = spiral_theta_end(length, r_mid0, pitch)
    n = int(math.degrees(th_end) / 4) + 2          # a point every 4 deg; spline between
    ths = [th_end * i / (n - 1) for i in range(n)]
    k = pitch / (2 * math.pi)
    inner = [((R_HUB + k * t) * math.cos(t), (R_HUB + k * t) * math.sin(t)) for t in ths]
    outer = [((R_HUB + TAPE_T + k * t) * math.cos(t), (R_HUB + TAPE_T + k * t) * math.sin(t)) for t in ths]
    w = (cq.Workplane("XY").moveTo(*inner[0]).spline(inner[1:], includeCurrent=True)
         .lineTo(*outer[-1]).spline(list(reversed(outer))[1:], includeCurrent=True).close())
    solid = w.extrude(FLAT_H)
    info = {"theta_end_deg": math.degrees(th_end), "wraps": th_end / (2 * math.pi), "pitch": pitch,
            "r_outer": R_HUB + TAPE_T + k * th_end}
    return solid, info


def spool(r_outer_coil: float) -> dict[str, cq.Workplane]:
    """INDICATIVE spool: hub cylinder R_HUB, two end discs. No bore, no drive: the mechanism is not decided."""
    zlo, zhi = -SIDE_CLR, FLAT_H + SIDE_CLR
    r_disc = r_outer_coil + DISC_OVER
    hub = cq.Workplane("XY").workplane(offset=zlo).circle(R_HUB).extrude(zhi - zlo)
    d0 = cq.Workplane("XY").workplane(offset=zlo - DISC_T).circle(r_disc).extrude(DISC_T)
    d1 = cq.Workplane("XY").workplane(offset=zhi).circle(r_disc).extrude(DISC_T)
    return {"spool_hub": hub, "spool_disc_a": d0, "spool_disc_b": d1}


# ------------------------------------------------------------------ build and check
dep = deployed()
coil, cinfo = coiled()
sp = spool(cinfo["r_outer"])

lines: list[str] = []
errs: list[str] = []


def check(label: str, got: float, want: float, tol: float = 0.01, unit: str = "mm") -> None:
    ok = abs(got - want) <= tol
    lines.append(f"{'ok ' if ok else 'BAD'} {label:46s} model {got:12.4f}  want {want:12.4f} {unit}  (tol {tol})")
    if not ok:
        errs.append(label)


bb = dep.val().BoundingBox()
check("deployed length (bbox z)", bb.zlen, L)
check("section width (bbox u) = 2*(R+T/2)", bb.xlen, 2 * R_OUT)
check("section height (bbox v) = W + R + T/2", bb.ylen, W + R_OUT)
area = dep.val().Volume() / L
a_th = 2 * (T * W + 0.5 * math.radians(THETA) * (R_OUT ** 2 - R_IN ** 2))
check("section area (mm2) vs analytic", area, a_th, 1e-4, "mm2")

radii = sorted({round(f._geomAdaptor().Cylinder().Radius(), 6) for f in dep.faces().vals() if f.geomType() == "CYLINDER"})
check("number of distinct arc radii", len(radii), 2, 0, "")
check("inner arc radius", radii[0], R_IN)
check("outer arc radius", radii[-1], R_OUT)
check("mid-surface radius (mean of the two)", (radii[0] + radii[-1]) / 2, R)
cyl = [f for f in dep.faces().vals() if f.geomType() == "CYLINDER"]
check("arc length of outer face / length, rad -> deg",
      math.degrees(max(f.Area() for f in cyl) / L / R_OUT), THETA, 1e-6, "deg")
web = [f for f in dep.faces().vals() if f.geomType() == "PLANE" and abs(f.Area() / L - W) < 1e-6]
check("web faces of height W (count)", len(web), 2, 0, "")
check("web thickness (two flanges, free face to free face)", abs(web[0].Center().x - web[1].Center().x) if len(web) == 2 else -1, 2 * T)

ref = cq.importers.importStep(REF_STEP)
refv = ref.val().Volume()
reflen = ref.val().BoundingBox().xlen
check("reference STEP section area vs model (mm2)", refv / reflen, area, 1e-3, "mm2")
rbb = ref.val().BoundingBox()
check("reference STEP section width (y) vs model", rbb.ylen, bb.xlen)
check("reference STEP section height (z) vs model", rbb.zlen, bb.ylen)
refrad = sorted({round(f._geomAdaptor().Cylinder().Radius(), 6) for f in ref.faces().vals() if f.geomType() == "CYLINDER"})
check("reference STEP inner radius vs model", refrad[0], radii[0])
check("reference STEP outer radius vs model", refrad[-1], radii[-1])

cb = coil.val().BoundingBox()
check("coiled tape height (z) = flattened height", cb.zlen, FLAT_H)
check("coiled outer radius vs wrap count", max(abs(cb.xmin), cb.xmax, abs(cb.ymin), cb.ymax), cinfo["r_outer"], 0.05)
check("coiled volume vs tape volume (length x H x t)", coil.val().Volume(), L * FLAT_H * TAPE_T, 0.002 * L * FLAT_H * TAPE_T, "mm3")
dep_mass = dep.val().Volume() * P.DENSITY * 1e-9 * 1e-3 * 1e3   # mm3 -> m3 (1e-9) * kg/m3, result kg
lines.append(f"info deployed volume {dep.val().Volume():.1f} mm3, mass at {P.DENSITY} kg/m3 = {dep_mass * 1000:.1f} g")
lines.append(f"info coil: {cinfo['wraps']:.3f} wraps, pitch {cinfo['pitch']} mm, outer R {cinfo['r_outer']:.3f} mm "
             f"(D {2 * cinfo['r_outer']:.2f}); tape height {FLAT_H:.4f} mm")
lines.append("info the CAD STEP 'Composite Boom Full Length.step' is 3000 mm; params.py LENGTH is 2.1 m; this model uses params.py.")

txt = "\n".join(lines)
print(txt)
with open(os.path.join(HERE, "model_check.txt"), "w") as fh:
    fh.write("model check, trac_boom_model.py against params.py and Composite Boom.step\n" + txt + "\n")
if errs:
    print("FAILED:", errs)
    sys.exit(1)

# ------------------------------------------------------------------ write
def stl(wp: cq.Workplane, name: str, tol: float = 0.005, ang: float = 0.05) -> None:
    cq.exporters.export(wp, os.path.join(HERE, name), tolerance=tol, angularTolerance=ang)


COIL_TOL, COIL_ANG = 0.01, 0.3   # chord error 0.01 mm: keeps the spiral STL small enough for GitHub's viewer


def comp(parts: list[cq.Workplane]) -> cq.Workplane:
    return cq.Workplane().add(cq.Compound.makeCompound([p.val() for p in parts]))


cq.exporters.export(dep, os.path.join(HERE, "trac_boom_deployed_2100.step"))
stl(dep, "trac_boom_deployed_2100.stl")
cq.exporters.export(coil, os.path.join(HERE, "trac_boom_coiled.step"))
stl(coil, "trac_boom_coiled.stl", COIL_TOL, COIL_ANG)
spool_parts = list(sp.values())
asm = cq.Assembly(name="svarog_spool_with_coiled_boom")
asm.add(coil, name="boom_coiled", color=cq.Color(0.15, 0.15, 0.17))
for k, v in sp.items():
    asm.add(v, name=k, color=cq.Color(0.72, 0.77, 0.80))
asm.save(os.path.join(HERE, "spool_with_coiled_boom.step"))
stl(comp([coil] + spool_parts), "spool_with_coiled_boom.stl", COIL_TOL, COIL_ANG)
stl(comp(spool_parts), "spool_empty.stl")
cq.exporters.export(comp(spool_parts), os.path.join(HERE, "spool_empty.step"))

dims = f"""# Dimensions

Generated by `trac_boom_model.py` from `Composite Booms/Scripts/params.py`. All mm unless stated.

| Quantity | Value | Source |
|---|---|---|
| Flange mid-surface radius | {R:.3f} | params.py R_CURED |
| Flange inner / outer radius | {R_IN:.3f} / {R_OUT:.3f} | R -/+ t/2 |
| Flange opening angle | {THETA:.1f} deg | params.py THETA_DEG |
| Flange thickness (each) | {T:.3f} | params.py THICKNESS (two 0.1 mm plies) |
| Web height (bonded land) | {W:.3f} | params.py WEB_WIDTH |
| Section width x height | {2 * R_OUT:.3f} x {W + R_OUT:.3f} | derived |
| Section area | {area:.4f} mm2 | derived, matches the STEP section |
| Deployed length | {L:.1f} | params.py LENGTH (2.1 m) |
| Flattened tape height | {FLAT_H:.4f} | sizing.py: web + one arc length |
| Flattened tape thickness | {TAPE_T:.3f} | sizing.py: two flanges |
| Hub radius / diameter | {R_HUB:.1f} / {2 * R_HUB:.1f} | params.py DEFAULT_R_HUB |
| Wraps for 2.1 m on the hub | {cinfo['wraps']:.2f} | spiral, mid-line length = L |
| Coil outer radius / diameter | {cinfo['r_outer']:.2f} / {2 * cinfo['r_outer']:.2f} | hub + wraps x pitch |
| Spool end discs | {DISC_T} thick, R {cinfo['r_outer'] + DISC_OVER:.2f} | INDICATIVE, not decided |
| Wrap clearance in the model | {WRAP_GAP} | INDICATIVE, keeps the spiral a valid solid |

Open points carried from `docs/REVIEW-NOTES.md`: the flattened tape thickness (0.4 mm here, as `sizing.py` counts it) and the
hub radius are the project's own working values, not measured. The CAD STEP `Composite Boom Full Length.step` is 3000 mm;
this model follows params.py (2100 mm).
"""
with open(os.path.join(HERE, "DIMENSIONS.md"), "w") as fh:
    fh.write(dims)
print("wrote step + stl for deployed, coiled, spool_with_coiled_boom, spool_empty; DIMENSIONS.md; model_check.txt")
