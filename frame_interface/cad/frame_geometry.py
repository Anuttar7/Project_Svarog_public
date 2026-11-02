"""Atrium reference 1U frame for the Svarog 10 g / SF 2 challenge, built in Fusion through the MCP bridge.

Run:  python3 ~/Developer/scripts/fusion_run.py frame_geometry.py   (Fusion open, MCP on 127.0.0.1:27182)
Units in the dict P are mm; Fusion works in cm, so every length goes through mm(). Z is the 100 mm height.
Frame = 4 L-angle rails + 6x6 contact pads + top/bottom open rings + X-braces on the +-Y faces + corner
gussets on the open +-X faces. AI-made (Claude).
"""
import json
import adsk.core
import adsk.fusion

# why fixed: Atrium reference frame dimensions in mm (rail leg 8.5 and pad 6.0 from the CubeSat and competition rules), the design under test
P = dict(cube=100.0, leg=8.5, t_rail=1.6, pad=6.0, pad_h=3.0, ring_w=6.0, ring_t=1.6, brace_w=3.0,
         # why fixed: Atrium reference frame dimensions in mm (rail leg 8.5 and pad 6.0 from the CubeSat and competition rules), the design under test
         brace_t=1.6, gus_leg=18.0, gus_w=3.0, gus_t=1.6)
RHO = 1.24  # g/cm3 PLA; why fixed: the Svarog workshop-2 material card
P.update(globals().get("OVERRIDE", {}))  # the driver prepends OVERRIDE = {...}

# why fixed: mm to cm: Fusion's internal unit is cm
K = 0.1
app = adsk.core.Application.get()
tbm = adsk.fusion.TemporaryBRepManager.get()


def pt(x, y, z):
    return adsk.core.Point3D.create(x * K, y * K, z * K)


def vec(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


def box(x0, x1, y0, y1, z0, z1):
    c = pt((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    o = adsk.core.OrientedBoundingBox3D.create(c, vec(1, 0, 0), vec(0, 1, 0), (x1 - x0) * K, (y1 - y0) * K, (z1 - z0) * K)
    return tbm.createBox(o)


def strut(u0, v0, u1, v1, off, plane, width, thick):
    """Rectangular strut from (u0,v0) to (u1,v1) in a face plane: width in-plane, thick out-of-plane.
    plane 'XZ' sits at Y=off, plane 'YZ' at X=off."""
    import math
    L = math.hypot(u1 - u0, v1 - v0)
    du, dv = (u1 - u0) / L, (v1 - v0) / L
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    if plane == "XZ":
        c, d1, d2 = pt(cu, off, cv), vec(du, 0, dv), vec(0, 1, 0)
    else:
        c, d1, d2 = pt(off, cu, cv), vec(0, du, dv), vec(1, 0, 0)
    return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, d1, d2, L * K, thick * K, width * K))


def union(parts):
    out = parts[0]
    for p in parts[1:]:
        tbm.booleanOperation(out, p, adsk.fusion.BooleanTypes.UnionBooleanType)
    return out


def build(p):
    c, lg, tr, pad, ph = p["cube"], p["leg"], p["t_rail"], p["pad"], p["pad_h"]
    rw, rt = p["ring_w"], p["ring_t"]
    parts = []
    for sx in (0, 1):
        for sy in (0, 1):
            x0 = 0 if sx == 0 else c - lg
            y0 = 0 if sy == 0 else c - lg
            # L-angle: two legs meeting at the outer corner
            xa = (0, tr) if sx == 0 else (c - tr, c)
            ya = (0, tr) if sy == 0 else (c - tr, c)
            parts.append(box(x0, x0 + lg, ya[0], ya[1], 0, c))
            parts.append(box(xa[0], xa[1], y0, y0 + lg, 0, c))
            # 6x6 contact pads at both ends, tucked into the corner
            px = (0, pad) if sx == 0 else (c - pad, c)
            py = (0, pad) if sy == 0 else (c - pad, c)
            parts.append(box(px[0], px[1], py[0], py[1], 0, ph))
            parts.append(box(px[0], px[1], py[0], py[1], c - ph, c))
    for z0 in (0, c - rt):  # open rings (bars along the 4 edges)
        parts.append(box(0, c, 0, rw, z0, z0 + rt))
        parts.append(box(0, c, c - rw, c, z0, z0 + rt))
        parts.append(box(0, rw, 0, c, z0, z0 + rt))
        parts.append(box(c - rw, c, 0, c, z0, z0 + rt))
    bw, bt = p["brace_w"], p["brace_t"]
    for y in (bt / 2, c - bt / 2) if bw > 0 else ():  # X-braces on the +-Y faces (XZ planes)
        zlo, zhi = rt, c - rt
        parts.append(strut(lg, zlo, c - lg, zhi, y, "XZ", bw, bt))
        parts.append(strut(lg, zhi, c - lg, zlo, y, "XZ", bw, bt))
    g, gw, gt = p["gus_leg"], p["gus_w"], p["gus_t"]
    for x in (gt / 2, c - gt / 2) if g > 0 else ():  # corner gussets on the open +-X faces (YZ planes), leave the middle open
        zlo, zhi = rt, c - rt
        for (ya, za, yb, zb) in ((lg, zlo + g, lg + g, zlo), (c - lg, zlo + g, c - lg - g, zlo),
                                 (lg, zhi - g, lg + g, zhi), (c - lg, zhi - g, c - lg - g, zhi)):
            parts.append(strut(ya, za, yb, zb, x, "YZ", gw, gt))
    dw, dyw = p.get("diag_w", 0), p.get("diagy_w", 0)
    # one diagonal per face; the 40 x 40 mm window stays free in the triangle above it
    ext = p.get("diag_ext", 0)  # diagonal ends run into the rail legs by ext mm, as in fe_check.py
    for x in (gt / 2, c - gt / 2) if dw > 0 else ():
        parts.append(strut(lg - ext, rt, c - lg + ext, c - rt, x, "YZ", dw, gt))
    for y in (bt / 2, c - bt / 2) if dyw > 0 else ():
        parts.append(strut(lg - ext, rt, c - lg + ext, c - rt, y, "XZ", dyw, bt))
    return union(parts)


def vol_cm3(b):
    return b.volume


body = build(P)
vol = body.volume  # cm3
# why fixed: cm3 to mm3 is a fixed unit conversion; rounding digits are display only
report = dict(P=P, volume_mm3=round(vol * 1000, 1), mass_g=round(vol * RHO, 3))
# keep-out and opening checks: intersect copies with the keep-out tools; volume must be 0
def hit(tool):
    cp = tbm.copy(body)
    ok = tbm.booleanOperation(cp, tool, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    # why fixed: cm3 to mm3 is a fixed unit conversion; rounding digits are display only
    return round(cp.volume * 1000, 3) if ok else 0.0

c = P["cube"]
# why fixed: competition brief keep-out: central 70 mm void (15 to 85) and 40 x 40 mm side openings
report["keepout_70_cube_overlap_mm3"] = hit(box(15, 85, 15, 85, 15, 85))
# why fixed: competition brief keep-out: central 70 mm void (15 to 85) and 40 x 40 mm side openings
report["open_face_40x40_overlap_mm3"] = [hit(box(-1, P["gus_t"] + 0.5, P["leg"], P["leg"] + 40, 55, 95)), hit(box(P["leg"], P["leg"] + 40, -1, P["brace_t"] + 0.5, 55, 95))]
# why fixed: competition brief: 12 mm diameter base pass-through, radius 6
cyl = tbm.createCylinderOrCone(pt(c / 2, c / 2, -1), 6.0 * K, pt(c / 2, c / 2, P["ring_t"] + 1), 6.0 * K)
report["base_12mm_hole_overlap_mm3"] = hit(cyl)
bb = body.boundingBox
# why fixed: cm to mm is a fixed unit conversion
report["bbox_mm"] = [round((bb.maxPoint.x - bb.minPoint.x) * 10, 2), round((bb.maxPoint.y - bb.minPoint.y) * 10, 2), round((bb.maxPoint.z - bb.minPoint.z) * 10, 2)]
print(json.dumps(report))
