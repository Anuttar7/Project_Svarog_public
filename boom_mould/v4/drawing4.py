"""Svarog boom mould v4 drawing: closed three-piece tool, all views dimensioned.

Writes beside this script:
  mould_v4.png / mould_v4.pdf  (A3 landscape sheet: section, exploded, root detail, side, plan)
  mould_v4.dxf                 (section profiles for Fusion: Insert > Insert DXF, mm)
Geometry from calc4.py (single source). x = 0 centreline, y = 0 web root, mm.
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import io, contextlib  # noqa: E401,E402
with contextlib.redirect_stdout(io.StringIO()):
    from calc4 import GEOM  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, Rectangle, Circle  # noqa: E402

g = GEOM
R, G, WEB, GAL, TIP = g["R"], g["G"], g["WEB"], g["GALLERY"], g["TIP_LAND"]
BW, BH, YB, BOLT_Y, T = g["BLK_W"], g["BLK_H"], g["Y_BOT"], g["BOLT_Y"], g["T_LAM"]
BW = BW + G  # outer face x; the block itself is BLK_W wide, from x = G to G + BLK_W
L, PLUG_TOP = g["L"], g["R"] + g["PLUG_OVER"]
BASE_T = 18.0   # why fixed: base plate is one sheet of the same 18 mm ply [assume]
BASE_MARGIN = 7.0  # why fixed: base plate overhang each side for the bag and slots [assume]
N_ARC = 60      # why fixed: polyline resolution of the arc in the figure only
COL = dict(wood="#d9b98a", plug="#9bb7d4", lam="#111111", bag="#c0392b", shim="#7f8c8d", base="#c8a878")


def arc_pts(sign: int, r: float, n: int = N_ARC) -> list[tuple[float, float]]:
    """Tool-face arc for the left (sign=-1) or right (+1) block, root to tip."""
    cx = sign * (G + R)
    return [(cx - sign * r * math.cos(math.radians(90 * i / n)), r * math.sin(math.radians(90 * i / n)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            for i in range(n + 1)]


def block_poly(sign: int) -> list[tuple[float, float]]:
    face = arc_pts(sign, R)
    gal = [(sign * G, -WEB), (sign * (G + GAL), -WEB), (sign * (G + GAL), -WEB - GAL), (sign * G, -WEB - GAL)]
    rl = sign * (G + g["RELIEF"])
    return ([(rl, YB), (rl, -WEB - GAL)] + gal[::-1][1:] + face + [(sign * BW, R), (sign * BW, YB)])


def lam_pts(sign: int) -> list[tuple[float, float]]:
    """Laminate centre path: down the web, round the arc, to the trim line."""
    cx, rr = sign * (G + R), R + T / 2
    trim = g["TRIM_DEG"]
    pts = [(sign * (G - T / 2), -WEB)]
    pts += [(cx - sign * rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a)))
            for a in [trim * i / N_ARC for i in range(N_ARC + 1)]]
    return pts


def plug_poly() -> list[tuple[float, float]]:
    """Silicone plug: fills the V above the laminate down to where the gap is 0.5 mm."""
    left = [(x + T, y) for x, y in arc_pts(-1, R)]   # laminate outer surface, approx
    left = [(x, y) for x, y in left if y >= g["H_PLUG_MIN"]]
    right = [(-x, y) for x, y in left]
    return [(-BW, PLUG_TOP), (-BW, R + T)] + left[::-1] + right + [(BW, R + T), (BW, PLUG_TOP)]


def dim_h(ax, x0, x1, y, txt, fs=7):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.text((x0 + x1) / 2, y + 0.8, txt, ha="center", va="bottom", fontsize=fs)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def dim_v(ax, y0, y1, x, txt, fs=7):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.text(x + 0.8, (y0 + y1) / 2, txt, ha="left", va="center", fontsize=fs, rotation=90)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def section(ax, explode: float = 0.0, bag: bool = True) -> None:
    dx, dy = explode, explode * 1.4  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    for s in (-1, 1):
        ax.add_patch(Polygon([(x + s * dx, y) for x, y in block_poly(s)], fc=COL["wood"], ec="k", lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.add_patch(Rectangle((s * dx - BW if s < 0 else s * dx, BOLT_Y - 3.0), BW, 6.0, fc="w", ec="k", lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        xs, ys = zip(*lam_pts(s))
        ax.plot([x + s * dx for x in xs], ys, c=COL["lam"], lw=1.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.plot([-BW - dx, BW + dx], [BOLT_Y] * 2, c="#555", lw=0.6, ls="-.")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Polygon([(x, y + dy) for x, y in plug_poly()], fc=COL["plug"], ec="#2c5d8a", lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Rectangle((-15, PLUG_TOP - 4 + dy), 30, 3, fc="#aaa", ec="k", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Rectangle((-BW - BASE_MARGIN, YB - BASE_T - dy * 0.3), 2 * (BW + BASE_MARGIN), BASE_T,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
                           fc=COL["base"], ec="k", lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    if bag:
        m = 3.0  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.add_patch(Rectangle((-BW - BASE_MARGIN - m, YB - BASE_T - m), 2 * (BW + BASE_MARGIN + m),
                               PLUG_TOP - YB + BASE_T + 2 * m, fill=False, ec=COL["bag"], lw=1.2, ls="--"))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


fig = plt.figure(figsize=(16.54, 11.69))  # why fixed: A3 landscape in inches
fig.suptitle("Svarog TRAC boom mould v4: closed three-piece tool (2 lower V clamps + silicone top plug), "
             "envelope bag round all, autoclave", fontsize=13, weight="bold", x=0.02, ha="left")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# A: assembled section
ax = fig.add_axes([0.02, 0.38, 0.40, 0.55])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
section(ax)
ax.set_title("A  Section, assembled and bagged (mm)", loc="left", fontsize=10)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_h(ax, -BW, BW, PLUG_TOP + 6, f"{2*BW:.1f} (plug and blocks)")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_h(ax, -BW, -G, YB - 24, f"{BW - G:.2f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_v(ax, YB, R, BW + 9, f"{BH:.0f} block")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_v(ax, R, PLUG_TOP, BW + 3, f"{g['PLUG_OVER']:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_v(ax, YB - BASE_T, YB, -BW - 16, f"{BASE_T:.0f} base")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"tool face R{R} shown; final radius\nfrom the coupon pairs (R15.2-R19.6)", (-(G + R) + R * math.cos(math.radians(45)),  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            R * math.sin(math.radians(45))), (-56, 30), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("silicone plug C\n(cast on the closed pair)", (8, 22), (20, 42), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("Al spine 30 x 3, drilled,\nsilicone locks through", (0, PLUG_TOP - 2.5), (-40, 38), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"M6 x 80 cross bolt, y {BOLT_Y:.1f}\n{g['TORQUE']:.0f} N m, clamps the web", (BW / 2, BOLT_Y), (36, -18), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"butt faces relieved {g['RELIEF']} each side;\n{g['STOP']} stops at trim ends only", (0, YB + 10), (10, -44), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("envelope bag + breather\nround everything", (BW + BASE_MARGIN + 3, 0), (40, 8), fontsize=7, color=COL["bag"])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("block A", (-BW / 2, -30), fontsize=8, ha="center")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("block B", (BW / 2, -30), fontsize=8, ha="center")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-66, 66)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(YB - BASE_T - 8, PLUG_TOP + 14)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_aspect("equal")
ax.axis("off")

# B: exploded
ax = fig.add_axes([0.43, 0.52, 0.27, 0.41])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
section(ax, explode=12, bag=False)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_title("B  Exploded: A and B clamp the V, C presses from the top", loc="left", fontsize=10)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(0, PLUG_TOP + 22, "C", ha="center", fontsize=12, weight="bold")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(-BW - 6, -45, "A", fontsize=12, weight="bold")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(BW + 2, -45, "B", fontsize=12, weight="bold")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-60, 60)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(YB - BASE_T - 12, PLUG_TOP + 28)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_aspect("equal")
ax.axis("off")

# C: root detail
ax = fig.add_axes([0.71, 0.52, 0.28, 0.41])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
section(ax, bag=False)
ax.set_title("C  Root detail: web, merge point, plug tip, gallery", loc="left", fontsize=10)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-6, 6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(-12.5, 6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_aspect("equal")
ax.axis("off")
dim_v(ax, -WEB, 0, 3.5, f"web {WEB:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"plug tip ~{g['H_PLUG_MIN']:.1f} above root\n(gap 0.5)", (0, g["H_PLUG_MIN"]), (1.2, 4.8), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate("0-3 mm: neither tool fully\nreaches; section coupon here", (0, 0.8), (-5.8, 3.5), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"bleed gallery {GAL:.0f} x {GAL:.0f}", (G + 0.5, -WEB - 0.5), (1.5, -11.8), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.annotate(f"web lands {2*G:.2f} apart (cured web)", (-G, -5), (-5.8, -8), fontsize=7,  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
            arrowprops=dict(arrowstyle="->", lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# D: side elevation
ax = fig.add_axes([0.43, 0.08, 0.55, 0.38])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_title("D  Side elevation of block A (B mirrors; bolt and dowel holes drilled through both blocks together)", loc="left", fontsize=10)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((0, YB), L, BH, fc=COL["wood"], ec="k", lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((-BASE_MARGIN, YB - BASE_T), L + 2 * BASE_MARGIN, BASE_T, fc=COL["base"], ec="k", lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((-8, R), L + 16, g["PLUG_OVER"], fc=COL["plug"], ec="#2c5d8a", lw=0.8, alpha=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
pitch = (L - 30) / (g["BOLT_N"] - 1)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for i in range(g["BOLT_N"]):
    ax.add_patch(Circle((15 + i * pitch, BOLT_Y), 3.0, fc="w", ec="k", lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for x in (15 + pitch / 2, L - 15 - pitch / 2):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Circle((x, BOLT_Y), 3.0, fc="#333", ec="k", lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for x in (40, L / 2, L - 40):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.plot([x - 6, x + 6], [YB - BASE_T / 2] * 2, c="k", lw=2.5)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([15, 15], [YB, R], ls="--", c="r", lw=0.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([L - 15, L - 15], [YB, R], ls="--", c="r", lw=0.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_h(ax, 0, L, R + g["PLUG_OVER"] + 8, f"{L:.0f} tool")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_h(ax, 15, L - 15, R + g["PLUG_OVER"] + 3, f"{L-30:.0f} part (red: trim)")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_h(ax, 15, 15 + pitch, BOLT_Y + 7, f"{pitch:.0f} pitch, {g['BOLT_N']} x M6")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim_v(ax, YB, BOLT_Y, L + 4, f"{BOLT_Y - YB:.1f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(15 + pitch / 2, BOLT_Y - 10, "6 mm reamed dowel (2 off, filled)", fontsize=7, ha="center")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(40, YB - BASE_T - 7, "base screws in slotted holes; the slots run ACROSS the tool (seen end-on here) so the blocks can close",  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(L + 10, R + 4, "plug overhangs\n8 each end: free\nto grow ~15 mm\nat 150 C", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-20, L + 60)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(YB - BASE_T - 14, R + g["PLUG_OVER"] + 16)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_aspect("equal")
ax.axis("off")

# notes
fig.text(0.02, 0.05, (  # why fixed: figure layout for the dimensioned drawing (notes block position), no requirement behind it
    f"Tool face R{R} shown. Spring-in measured on this process (Leclerc et al. 2017/2018, Caltech: mould R12.7 cured R10.6, 90 -> 105 deg) puts the tool ABOVE the part.\n"
    f"calc3's R14.83 had the sign backwards. Tomorrow: coupon pairs at R{g['COUPON_R']}; ROUGH the long blocks only; finish the arc once the coupons are read.\n"
    "Blocks: one 35 mm phenolic birch strip each, sheet parallel to the web land (no glueline); rough, bake to constant mass, finish, seal.\n"
    "Plug C: Mold Max XLS II (204 C) cast on the closed pair over a measured 0.22-0.25 mm spacer; drilled Al spine; no FEP across the V.\n"
    f"Clamp: bolts at {g['TORQUE']:.0f} N m clamp the web as at Caltech; butt faces relieved; autoclave adds 1.4-2.9 MPa (net area ratio 3.6). Bag round everything.\n"
    "Sources: calc4_output.txt, research-v4-autoclave.md, review-v4-adversarial.md. Draft 2 Nov 2026 for the 18:00 session; nothing cut yet."),
    fontsize=8, va="bottom")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

fig.savefig(os.path.join(HERE, "mould_v4.png"), dpi=110)  # why fixed: screen legibility at A3
fig.savefig(os.path.join(HERE, "mould_v4.pdf"))


def write_dxf(path: str) -> None:
    """Section profiles only, as LWPOLYLINE-free LINE entities (R12 DXF, any reader)."""
    ents = []
    for s in (-1, 1):
        p = block_poly(s)
        ents += [("BLOCK_A" if s < 0 else "BLOCK_B", p[i], p[(i + 1) % len(p)]) for i in range(len(p))]
    p = plug_poly()
    ents += [("PLUG", p[i], p[(i + 1) % len(p)]) for i in range(len(p))]
    for s in (-1, 1):
        p = lam_pts(s)
        ents += [("LAMINATE", p[i], p[i + 1]) for i in range(len(p) - 1)]
    with open(path, "w") as f:
        f.write("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n")
        for layer, a, b in ents:
            f.write(f"0\nLINE\n8\n{layer}\n10\n{a[0]:.4f}\n20\n{a[1]:.4f}\n30\n0\n11\n{b[0]:.4f}\n21\n{b[1]:.4f}\n31\n0\n")
        f.write("0\nENDSEC\n0\nEOF\n")


write_dxf(os.path.join(HERE, "mould_v4.dxf"))
print("wrote mould_v4.png, mould_v4.pdf, mould_v4.dxf")
