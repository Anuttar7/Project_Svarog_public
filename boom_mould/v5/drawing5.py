"""Svarog boom mould v5 drawing sheet: A3 landscape, one sheet, every view dimensioned.

Writes beside this script: mould_v5.pdf and mould_v5.png.
Geometry from calc5.py (which imports calc4.py). x = 0 centreline, y = 0 web root, z along the tool, mm.
Views: A section of the closed tool; B root detail; C plan of block A; D liner flat blank; tables.
"""
from __future__ import annotations

import contextlib
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    from calc5 import GEOM5 as g  # noqa: E402

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

plt.rcParams.update({"font.family": "Helvetica Neue", "font.size": 8, "axes.linewidth": 0.6})  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

R, RW, G, TL = g["R"], g["R_WOOD"], g["G"], g["T_LINER"]
WEB, GAL, TIP, T = g["WEB_LAND"], g["GALLERY"], g["TIP_LAND"], g["T_LAM"]
WEB_LAM = g["WEB"]  # laminate web, 10; the wood web land is 13 so the liner runs past it
RET = g["RETURN"]
BW, BH, YB, BOLT_Y = g["BLK_W"], g["BLK_H"], g["Y_BOT"], g["BOLT_Y5"]
L, PLUG_TOP, XB = g["L"], g["R"] + g["PLUG_OVER"], -g["X_BUTT"]
BASE_T = 18.0      # why fixed: base plate, one sheet of 18 mm ply, as v4 [src drawing4]
BASE_M = 7.0       # why fixed: base overhang each side for bag and slots, as v4 [src drawing4]
N = 60             # why fixed: arc polyline resolution, figure only
INK, MID, FAINT = "#1a1a1a", "#555555", "#9a9a9a"
FILL = dict(wood="#e8dcc6", al="#b8c4cc", plug="#dfe7ee", lam=INK, base="#d9ccb4")
BOLT_Z = [15 + 90 * i for i in range(5)]   # why fixed: v4 bolt stations, pitch 90 from 15 [src calc4]
DOWEL_Z = (60.0, 330.0)                    # why fixed: midway between end bolt pairs [assume]
SCREW_Z = (L / 2 - g["PIN_SLOT_Z"], L / 2, L / 2 + g["PIN_SLOT_Z"])
TRIM = 15.0                                # why fixed: trim allowance each end, v4 [src calc4]


def arc(cx: float, r: float, sign: int) -> list[tuple[float, float]]:
    return [(cx - sign * r * math.cos(math.radians(90 * i / N)), r * math.sin(math.radians(90 * i / N))) for i in range(N + 1)]  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def block_poly(sign: int) -> list[tuple[float, float]]:
    """Wood block outline (left sign=-1): wood web land, wood arc, wood tip land, outer face, base, relieved butt."""
    cx = sign * (G + R)
    xl = sign * (G + TL)
    pts = [(sign * XB, YB), (sign * XB, -WEB - GAL), (xl, -WEB - GAL), (xl, 0)]
    pts += arc(cx, RW, sign)[1:]
    pts += [(sign * (G + R + TIP), R - TL), (sign * (G + BW), R - TL), (sign * (G + BW), YB)]
    return pts


def liner_pts(sign: int) -> list[tuple[float, float]]:
    cx = sign * (G + R)
    xo = sign * (G + BW)
    inner = [(sign * (G + TL), -WEB + 0.5), (sign * (G + TL), 0)] + arc(cx, RW, sign)[1:] + [(xo, R - TL), (xo, R - TL - RET)]  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    outer = [(sign * G, -WEB + 0.5), (sign * G, 0)] + arc(cx, R, sign)[1:] + [(xo + sign * TL, R), (xo + sign * TL, R - TL - RET)]  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    return inner + outer[::-1]


def dim(ax, p1, p2, off, text, vertical=False, fs=8.8):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    (x1, y1), (x2, y2) = p1, p2
    if vertical:
        xa = off
        ax.plot([x1, xa], [y1, y1], c=FAINT, lw=0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.plot([x2, xa], [y2, y2], c=FAINT, lw=0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.annotate("", (xa, y1), (xa, y2), arrowprops=dict(arrowstyle="<|-|>", lw=0.5, color=INK, shrinkA=0, shrinkB=0, mutation_scale=6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.annotate(text, (xa, (y1 + y2) / 2), xytext=(-3, 0), textcoords="offset points", rotation=90, ha="right", va="center", fontsize=fs)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    else:
        ya = off
        ax.plot([x1, x1], [y1, ya], c=FAINT, lw=0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.plot([x2, x2], [y2, ya], c=FAINT, lw=0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.annotate("", (x1, ya), (x2, ya), arrowprops=dict(arrowstyle="<|-|>", lw=0.5, color=INK, shrinkA=0, shrinkB=0, mutation_scale=6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
        ax.annotate(text, ((x1 + x2) / 2, ya), xytext=(0, 2.5), textcoords="offset points", ha="center", va="bottom", fontsize=fs)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def label(ax, xy, xytext, text, fs=8.8):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.annotate(text, xy, xytext, fontsize=fs, color=INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.4, color=MID, shrinkA=2, shrinkB=2,  # why fixed: figure layout for the dimensioned drawing (leader line weight and gap), no requirement behind it
                                relpos=(1, 0.5) if xytext[0] < xy[0] else (0, 0.5)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def title(ax, letter, text, scale):
    ax.set_title(f"{letter}   {text}", loc="left", fontsize=10, fontweight="bold", pad=4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.text(1.0, 1.01, scale, transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color=MID)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it


def frame(ax):
    ax.set_aspect("equal")
    ax.axis("off")


fig = plt.figure(figsize=(16.54, 11.69))  # A3 landscape, inches  why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
# outer border and title block
fig.add_artist(Rectangle((0.012, 0.015), 0.976, 0.97, transform=fig.transFigure, fill=False, lw=1.0, ec=INK))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# ---------- A: section ----------
ax = fig.add_axes([0.03, 0.40, 0.46, 0.55])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
frame(ax)
title(ax, "A", "Section through the closed tool, mid-length", "")
ax.add_patch(Rectangle((-(G + BW) - BASE_M, YB - BASE_T), 2 * (G + BW + BASE_M), BASE_T, fc=FILL["base"], ec=INK, lw=0.7))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for s in (-1, 1):
    ax.add_patch(Polygon(block_poly(s), closed=True, fc=FILL["wood"], ec=INK, lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Polygon(liner_pts(s), closed=True, fc=FILL["al"], ec=INK, lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    lam = [(s * G, -WEB_LAM)] + [(s * G, 0)] + arc(s * (G + R), R, s)[1:-8]
    ax.plot([p[0] - s * T / 2 * 0 for p in lam], [p[1] for p in lam], c=FILL["lam"], lw=1.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
plug = [(-(G + R + TIP), R), (-(G + R + TIP), PLUG_TOP), (G + R + TIP, PLUG_TOP), (G + R + TIP, R)]
plug += arc(G + R, R + 0.0, 1)[::-1][:-1] + [(0, 0)] + arc(-(G + R), R, -1)[1:]
ax.add_patch(Polygon(plug, closed=True, fc=FILL["plug"], ec=INK, lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((-15, PLUG_TOP - 4), 30, 3, fc=FILL["al"], ec=INK, lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for s in (-1, 1):
    ax.plot([s * XB, s * (G + BW)], [BOLT_Y, BOLT_Y], c=MID, lw=0.6, ls=(0, (4, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([0, 0], [YB - BASE_T - 4, PLUG_TOP + 4], c=MID, lw=0.4, ls=(0, (8, 2, 1, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
m = 3.0  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((-(G + BW) - BASE_M - m, YB - BASE_T - m), 2 * (G + BW + BASE_M + m), PLUG_TOP - YB + BASE_T + 2 * m,
                       fill=False, ec=MID, lw=0.8, ls=(0, (6, 3))))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (-(G + BW), PLUG_TOP + m), (G + BW, PLUG_TOP + m), PLUG_TOP + 8, f"{2 * (G + BW):.1f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (G + BW, YB), (G + BW, R - TL), G + BW + 14, f"{BH - TL:.1f}", vertical=True)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (G + BW, R - TL), (G + BW, PLUG_TOP), G + BW + 14, f"{PLUG_TOP - R + TL:.1f}", vertical=True)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (-(G + BW), YB), (-(G + BW), YB - BASE_T), -(G + BW) - 12, f"{BASE_T:.0f}", vertical=True)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (-(G + BW), YB), (-G, YB), YB - BASE_T - 9, f"block {BW:.1f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-(G + R) + RW * 0.7, RW * 0.7), (-64, 24), f"wood arc R{RW:.1f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-(G + R) + R * 0.45, R * 0.89), (-64, 30), f"tool face R{R:.1f}\n(liner outer)")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-(G + BW) - TL, R - 4), (-64, 15), f"liner 1050A-H14,\n{TL} thick, {RET:.0f} return\nflange down the side")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-6, PLUG_TOP - 2.5), (-64, 38), "Al spine 30 × 3, drilled 6 mm at 20 pitch")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (12, PLUG_TOP - 6), (36, 38), "silicone plug C, Mold Max XLS II")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (G + BW / 2, BOLT_Y), (48, -40), f"M6 cross bolts, 5 off (hidden), y = {BOLT_Y:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (G + BW + TL, R - 3.5), (48, 12), "pan-head M3\nthrough flange")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-(G + BW) - BASE_M - m, 5), (-64, 6), "bag and breather")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(-(G + BW) / 2, YB + 6, "A", fontsize=12, fontweight="bold", ha="center")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text((G + BW) / 2, YB + 6, "B", fontsize=12, fontweight="bold", ha="center")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-66, 72)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(YB - BASE_T - 14, PLUG_TOP + 14)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# ---------- B: root detail ----------
ax = fig.add_axes([0.52, 0.585, 0.22, 0.365])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
frame(ax)
title(ax, "B", "Root detail, enlarged", "")
for s in (-1, 1):
    ax.add_patch(Polygon(block_poly(s), closed=True, fc=FILL["wood"], ec=INK, lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Polygon(liner_pts(s), closed=True, fc=FILL["al"], ec=INK, lw=0.6))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    ax.add_patch(Polygon([(s * G, -WEB_LAM), (s * G, 0)] + arc(s * (G + R), R, s)[1:20] +
                         arc(s * (G + R), R - T, s)[1:20][::-1] + [(s * (G - T), 0), (s * (G - T), -WEB_LAM)],
                         closed=True, fc=INK, ec=INK, lw=0.3))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((-G - TL, -WEB - GAL), 2 * (G + TL), GAL, fc="white", ec=INK, lw=0.5))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (0, -7), (1.6, -7.5), f"web 2 × {T} = {2 * G:.2f}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (-XB, -8.5), (XB, -8.5), -17.8, "", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(1.6, -17.8, f"butt gap {2 * XB:.2f}", va="center", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (0, -WEB - GAL / 2), (1.6, -16.5), "bleed gallery 1 × 1", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (0, -WEB_LAM), (1.6, -10.6), "laminate web ends; liner runs 2.5 further", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (-G - TL / 2, -5), (-4.4, -4.0), "liner on\nweb land", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
label(ax, (G + TL / 2, -3), (1.6, -2.5), f"liner {TL}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(0.0, -0.03, "The 0.36 stops sit between the liner faces,\nat the trim ends only (see C).", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=MID)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-4.6, 4.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(-21.5, 1.0)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# ---------- C: plan of block A ----------
ax = fig.add_axes([0.03, 0.13, 0.70, 0.24])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
frame(ax)
title(ax, "C", "Plan of block A from above; B mirrors. Drill both blocks together", "")
W = G + BW
ax.add_patch(Rectangle((0, 0), L, W, fc=FILL["wood"], ec=INK, lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.add_patch(Rectangle((0, G), L, W - G, fc=FILL["al"], ec=INK, lw=0.4))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([0, L], [W - TIP, W - TIP], c=INK, lw=0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(L * 0.62, (G + W - TIP) / 2, "arc, lined", ha="center", va="center", fontsize=8, color=MID)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(L * 0.62, W - TIP / 2, "tip land, lined", ha="center", va="center", fontsize=8, color=MID)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([TRIM, TRIM], [-3, W + 3], c=MID, lw=0.5, ls=(0, (6, 2, 1, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.plot([L - TRIM, L - TRIM], [-3, W + 3], c=MID, lw=0.5, ls=(0, (6, 2, 1, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for z in BOLT_Z:
    ax.plot([z, z], [0, W], c=MID, lw=0.6, ls=(0, (3, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for z in DOWEL_Z:
    ax.plot([z, z], [0, W], c=MID, lw=0.6, ls=(0, (1, 1.5)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for z in SCREW_Z:
    ax.plot([z], [W + 0.8], marker="o" if z == L / 2 else "s", ms=4, mfc="white", mec=INK, mew=0.6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for z in (TRIM / 2, L - TRIM / 2):
    ax.add_patch(Rectangle((z - 4, -0.2), 8, 1.0, fc=INK, ec=INK))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (0, W), (L, W), W + 14, f"{L:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (TRIM, W), (L - TRIM, W), W + 4, f"part {L - 2 * TRIM:.0f} between trim lines")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (0, 0), (BOLT_Z[0], 0), -12, f"{BOLT_Z[0]}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (BOLT_Z[0], 0), (BOLT_Z[1], 0), -19, "90 pitch, 5 bolts")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (SCREW_Z[0], 0), (SCREW_Z[1], 0), -12, f"{g['PIN_SLOT_Z']:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (SCREW_Z[1], 0), (SCREW_Z[2], 0), -12, f"{g['PIN_SLOT_Z']:.0f}")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (L, G), (L, W), L + 11, f"{BW:.1f}", vertical=True)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(L + 16, W - TIP / 2 + 6, "M3 pan head in the\nreturn flange, outer face:\nround hole at mid-length\n(circle), 3 mm slots\neither side (squares)", va="center", fontsize=8.5)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(L + 16, -14, "0.36 stops (black), web land,\noutside the trim lines", va="center", fontsize=8.5)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(DOWEL_Z[0], -27, "6 mm reamed dowels at 60 and 330 (dotted)", ha="center", fontsize=8.5)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-8, L + 85)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(-31, W + 20)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# ---------- D: liner blank ----------
ax = fig.add_axes([0.76, 0.55, 0.22, 0.40])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
frame(ax)
title(ax, "D", "Liner blank, flat, 2 per tool", "")
Wb = g["BLANK_W"]  # developed width, calc5
ax.add_patch(Rectangle((0, 0), Wb, 60, fc=FILL["al"], ec=INK, lw=0.7))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
b1, b2 = WEB - g["LINER_STOP"], WEB - g["LINER_STOP"] + (RW + TL / 2) * math.pi / 2  # liner stops 0.5 above the gallery
for b in (b1, b2):
    ax.plot([b, b], [0, 60], c=INK, lw=0.5, ls=(0, (5, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text((b1 + b2) / 2, 30, "form over\nthe wood arc\nR17.5", ha="center", va="center", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(b1 / 2, 30, "web\nland", ha="center", va="center", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
b3 = b2 + TIP
ax.plot([b3, b3], [0, 60], c=INK, lw=0.5, ls=(0, (5, 2)))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text((b2 + b3) / 2, 30, "tip\nland", ha="center", va="center", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text((b3 + Wb) / 2, 30, "re-\nturn", ha="center", va="center", fontsize=7)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (0, 60), (Wb, 60), 64, f"{Wb:.1f} developed")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (0, 0), (b1, 0), -4, f"{b1:.1f}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (b1, 0), (b2, 0), -4, f"{b2 - b1:.1f}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (b2, 0), (b3, 0), -4, f"{TIP:.0f}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
dim(ax, (b3, 0), (Wb, 0), -9, f"{RET:.0f}", fs=8)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.text(Wb / 2, -12, f"length 390; 60 shown. Pre-form over\na R{g['FORMER_R']} former, fit cold on the block\nto a 0.1 feeler, trim ends flush.", ha="center", va="top", fontsize=8.5)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_xlim(-6, Wb + 6)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ax.set_ylim(-26, 72)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

# ---------- notes, table, title block ----------
notes = (
    "NOTES\n"
    "1  Wood: one 35 mm phenolic birch strip per block, no glueline. Rough, bake to constant mass, finish, seal.\n"
    "2  Liner: 1050A-H14, 0.5 mm, micrometer at 3 points (reject spread > 0.02). Not bonded. FEP under it on the web lands, Frekote elsewhere.\n"
    "    Measure the friction coefficient (μ) in a 130 °C pull test first; if it is above 0.15 use 5754-H22.\n"
    "3  Long blocks: rough the arc only until the coupons are read. Finish all arcs on CNC; no stock cutter matches.\n"
    "4  Plug C: cast on the closed, lined pair over a measured 0.22-0.25 mm spacer. 24 h cure at room temperature.\n"
    "5  FEP on the tip lands, and under the liner on the web lands. Nothing across the V.\n"
    "6  Tolerances: web lands flat 0.05 over 390 and parallel 0.05; arc radius ±0.05; root tangent, no step."
)
fig.text(0.03, 0.14, notes, fontsize=8.6, va="top", linespacing=1.55)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ct = fig.add_axes([0.52, 0.40, 0.46, 0.12])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
ct.axis("off")
rows = [[f"R{r:.1f}", f"R{r - TL:.1f}", lab] for r, lab in zip(g["COUPON_R"], (
    "spring-in by Radford's thick-laminate formula (calculated)", "halfway between rows 1 and 3", "spring-in as Leclerc measured (part R = 0.835 × tool R, test data)", "spring-in as a fixed change in curvature"))]
rows.append(["R18.0", "R18.0, bare", "same as row 3, no liner: does the liner change the part?"])
tb = ct.table(cellText=rows, colLabels=["tool face", "wood arc", "what it tests"], loc="upper left",
              colWidths=[0.15, 0.15, 0.62], cellLoc="left")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
tb.auto_set_font_size(False)
tb.set_fontsize(9)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for (r_, c_), cell in tb.get_celld().items():
    cell.set_linewidth(0.4)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    cell.set_height(0.17)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    if r_ == 0:
        cell.set_text_props(fontweight="bold")
ct.set_title("Coupon blocks, 5 pairs, 60 long, all in one cure", loc="left", fontsize=10, fontweight="bold")  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

tbx = fig.add_axes([0.70, 0.025, 0.28, 0.10])  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
tbx.axis("off")
tbx.add_patch(Rectangle((0, 0), 1, 1, transform=tbx.transAxes, fill=False, lw=0.8))  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
for yy in (0.33, 0.66):  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
    tbx.plot([0, 1], [yy, yy], c=INK, lw=0.4, transform=tbx.transAxes)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
tbx.text(0.03, 0.82, "Svarog TRAC boom mould, v5", fontsize=11, fontweight="bold", va="center", transform=tbx.transAxes)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
tbx.text(0.03, 0.50, "Thomas van Pul   |   ICSS Project Svarog   |   2 Nov 2026", fontsize=8, va="center", transform=tbx.transAxes)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
tbx.text(0.03, 0.17, "Dimensions in mm, do not scale   |   A3   |   sheet 1 of 1   |   supersedes v4", fontsize=8, va="center", transform=tbx.transAxes)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it

for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, f"mould_v5.{ext}"), dpi=200 if ext == "png" else None)  # why fixed: figure layout for the dimensioned drawing (positions, sizes, line weights), no requirement behind it
print("wrote mould_v5.pdf and mould_v5.png")
