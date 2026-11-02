# Adversarial review, Svarog mould v4 (closed three-piece tool), 2026-11-02

Scope read: calc4.py, calc4_output.txt, drawing4.py, mould_v4.png, explainer_v4.html, research-v4-autoclave.md,
against spec3.md section 3a, review-adversarial-2026-11-02.md and the three Leclerc texts in the STRUM Drive.
Every number below was recomputed in Python (scratch script, not committed). Verdict: the architecture is right
and the spring-in sign fix is right; two things in the tool as drawn will defeat the web and the flange root, and
several headline numbers are overstated.

## BLOCKER 1: the 0.40 shim stop equals the nominal cured web, and the blocks tip onto it, so the web root goes unpressed

Evidence: calc4 `SLOT = 0.40 # shim stack = the cured web, 2 x 0.2`; drawing A shows the shim strip in the butt zone
y -34..-14; spec3 change 2 had set the slot 0.50 with removable shims and the web thickness taken from the coupon.
Physics, two parts. (a) A stop at exactly the nominal cured thickness is reached whenever the real consolidated web is
thinner than nominal (woven ply thickness varies with resin content and bleed). Once the blocks bear on the shims, the
web gets a fixed gap and no pressure: the 2 Nov blocker 2 again, under a new name. (b) Statics of one block (rigid body,
per unit length, p = bag pressure): outer face 54p inward acting at y = -9; plug pushes the arc face outward with 18p
(horizontal projection of the R18 arc) at y = +9. Taking moments about the base contact centre, a web resultant at
mid-web (y = -5) needs 468p of restoring moment from the base; the base can give at most 30p x 15 mm = 450p. The block
therefore rotates top-outward and closes at the bottom: the shims (below the web) bear first and the web is pressed
hardest at y = -10 and least at the root, y = 0, which is the joint that matters. Snug cross bolts at y = -23.5 sit below
the web and do not resist this.
Fix: make the web lands the only contact. Relieve both butt faces 0.3 mm per side below the gallery so they can never
be a stop. If a crush limit is kept, use short steel shims at the bolt stations only, set at 0.34-0.36 (below any
plausible cured web), and replace them from the coupon's measured web thickness. Put the base screws near the inner
(slot-side) edge, snug, so they hold the inner bottom edge down against the tipping moment. Section the first coupon
web at three heights and measure.

## BLOCKER 2: one FEP sheet between plug and layup bridges the zero-angle cusp, so the plug cannot reach the flange root

Evidence: explainer layer 4 and drawing note: "FEP film between plug and layup". calc4 section 3: gap between the two
laminates 0.06 mm at 1 mm above the root, 0.22 at 2 mm, 0.50 at 3 mm (I get 0.055, 0.22, 0.498 with the exact offset
circle). Explainer: "Below that the two flanges have already met, and the blocks squeeze them."
Physics: the flanges meet only at h <= 0. Between 0 and 3 mm their V-side faces see neither block nor plug; the blocks'
lateral load reaches the web only. A 0.05 mm FEP film draped from one flange to the other cannot follow into a gap that
closes as h^2; it spans the cusp like the bag did in the v3 review, and the plug presses the film, not the root. Second,
the plug is cast "over a 0.2 mm spacer (one ply of release film + wax)": one ply of release film plus wax is about
0.03-0.06 mm, not 0.2, and uncured prepreg is 0.23-0.25 per flange. The cast plug is ~0.15-0.2 mm oversize on every
face and its tip is a silicone feather that tears on the first demould and leaves rubber in the co-cure zone.
Fix: no FEP across the V. Leclerc (2017, 2018) names no film; Mold Max XLS II releases from epoxy. If film is wanted for
the plug's length growth, use one strip per flange that stops 3 mm above the root, never into the web slot (film in the
slot unbonds the web). Cast the plug over a real spacer of measured 0.22-0.25 mm (an offcut of uncured or cured laminate,
or wax sheet) laid over arcs and tip lands, degassed silicone. Accept the 0-3 mm cusp as a resin fillet and check it in
the coupon micrograph; Leclerc's own micrographs show this transition varies sample to sample.

## HIGH 3: the closing force is overstated by 1.5x, and friction cuts it further

calc4 section 5 uses the full 54 mm outer face and ignores the plug pushing the blocks apart. Net inward load is
p(54 - 18) = 36p, not 54p: 1.44 MPa on the web at 3 bar + vacuum (calc says 2.16), 2.88 MPa at 7 bar (calc 4.32);
5.6 kN, not 8.4 kN. Base friction (vertical plug load 30p, mu 0.3-0.5) takes it to 0.84-1.08 MPa at 3 bar. Snug base
screws add preload friction on top. Still above p, so the mechanism works, but "area ratio 5.4" on the drawing and in
the explainer is wrong; say 3.6 before friction. Also: many autoclave practices vent the bag after ~1.5 bar, in which
case net p is the gauge value only (0.3 MPa at 3 bar). Ask which the lab runs.

## HIGH 4: the R15.2-R18.0 bracket is model-dependent and R18 is not a guaranteed upper bound

The sign is right (both texts confirm the flange curls tighter). The scaling is not. calc4 scales radius by the ratio
10.6/12.7. If the shape change is a residual-stress curvature change (thin-shell warpage, which is what Leclerc blame:
"few fibres across the ply thickness"), delta-kappa is independent of tool radius: same laminate would need R19.6. If
delta-kappa scales as 1/t (71 um to 200 um), R16.4. Radford's through-thickness spring-in is thickness-independent, so
"thicker springs in less" is not Radford's argument. A balanced woven ply has near-isotropic in-plane CTE, so [0F/45F]
should warp far less than thin UD: the likely answer is near R15.5-16.5, and R18 will certainly be recut. Also, Leclerc's
AIAA 2017 and 2018 papers give nominal r = 12.5 (ratio 0.848, tool R17.7); only the IASS 2017 paper says mould 12.7.
Fix: three coupon radii, not two (R15.2, R16.5, R18.0), all in the same cure, same layup, both blocks plus plug; measure
radius and angle at mid-length. Before cutting anything, get the radius of Aditya's existing V mould and of a part off it.
Strongly consider squaring and drilling the long blanks tomorrow but leaving their radius until the coupons are read: one
cut, one bake, one seal, one plug, instead of two of each.

## HIGH 5: wood is machined before it is dried, along its least stable axis

Laminations are vertical, so x (block width, web gap, horizontal extent of the arc) is the plywood thickness direction,
which moves like solid wood across the grain (order 0.2-0.3 % per % MC). Drying 8-12 % to near 0 shrinks a 30 mm block
~0.6-0.9 mm in x and turns the R18 arc into an ellipse (horizontal semi-axis ~17.5). The plan machines, then bakes, then
"re-measures": no re-cut step, and a re-cut after sealing exposes raw wood again. "Several hours" at 90-120 C will not
dry a 30 mm section to constant mass. Fix: rough-machine, bake to constant mass (weigh an offcut, as the 2 Nov review
said), finish-machine dry, seal the same day. Any recut means re-bake and re-seal before the plug is recast.

## HIGH 6: the lamination adhesive is never named

calc4, drawing and BOM say "glue face to face"; spec3's BOM line "high-temperature laminating adhesive, Tg above cure"
was dropped. PVA and PU wood glues soften and gas at 120 C. Fix: an epoxy laminating resin post-cured above the cure
temperature, or resorcinol. Better: 30 mm (or 35/40 mm) birch ply exists; one sheet gives a 30.0 mm block with no
lamination glueline at all. Note the block needs only two 18 mm sheets: the second calc4 glueline (x = -36.2) lies
outside a 30.2 block, not "in the tip land", and the first (x = -18.2) exits exactly at the R18 arc/tip-land tangent point.

## HIGH 7: "we copy Caltech, change only the block material" is not true, and the vacuum plumbing has been lost

Leclerc clamps the mandrels "using multiple bolts, joining and pressing the two flanges". v4 makes the bolts snug and
relies on autoclave closure, adds a shim stop, an FEP film, a cast-in spine and a cast-in-place plug. Some of that may be
better; it is not a copy, and the lead should hear it as a change. Separately, spec3 section 3a added a bag take-off,
200 C hose, in-bag gauge and hot leak test; the v4 BOM has only "valve". Restore them.

## MEDIUM

8. Plug growth contradiction. Drawing D: "free to grow ~15 mm"; explainer: the spine "limits its growth". Tin-cure
   silicone does not bond to bare aluminium, so an unkeyed spine restrains nothing. Drill the spine (6 mm holes every
   20 mm) so silicone locks through; then end slip is of order the plug depth x 3.9 % (~1 mm), not 7.6 mm per end.
   Specify end dams for casting the 8 mm overhangs.
9. Drawing A draws the cross bolts as circles at x = +-15.1, which reads as longitudinal bores; they run along x and
   belong as hidden lines. The 20 mm shim strip is drawn straight through the bolt line and the dowels at y = -23.5:
   shim positions along the length are undefined and the shims would be drilled through.
10. Block width: drawing says 30.00 (correct, BW - G); calc4 "block 30.20 wide" and the explainer "square blanks to
    30.2 x 54 x 390" are wrong. M6 x 80 is fine: grip 60.4 + two washers + all-metal nut is ~70.
11. No tolerances. The web land flatness and parallelism over 390 mm set a 0.40 mm web: 0.05 mm of bow is 12 %. Give
    flatness 0.05, root tangency, and the radius tolerance.
12. "Router with a fence" for R18.0 and R15.2: neither is a stock roundover radius (12.7, 15.9, 19.05 are). CNC only,
    or a ground cutter.
13. Vertical laminations put plywood edge (alternating long and end-grain veneers at ~1.4 mm pitch) on the whole arc and
    tip land: differential veneer movement prints a washboard into a 0.2 mm laminate. Seal and sand, check with a
    straightedge after the dry cycle.
14. BOM: "steel shim 0.05/0.10 + FEP 0.05, 1 each" cannot make 0.40; buy an assortment and a micrometer. Silicone: long
    plug 0.48 kg + three coupon plugs ~0.45 kg + waste exceeds one 1 kg kit, before any recast. Missing: casting dams,
    degassing, coupon bases/bolts, thermocouple, named sealer.
15. Base slots: drawing D shows horizontal bars along the tool; the note says slots across it. Draw a plan view.
16. Plug cure is 24 h at room temperature: nothing past "cast C" happens tomorrow. Say so at 18:00.

## Confirmed correct

- Spring-in sign: tool R12.7 (or 12.5) cured to R10.6 at 90 -> 105 deg, so the tool must be larger than the part;
  calc3's R14.83 was backwards. Ratio 0.8346, R17.97, R15.17 (Radford), arc -2.6 % all reproduce.
- Cut order: Monte-Carlo over the section (400k points) finds no point of an R15.2 block, same root tangent, outside
  the R18 block, tip land and full 54 mm height included. R18 -> R15.2 is a pure material removal; the tip land drops
  2.8 mm and the plug must be recast.
- Gap table, plug tip ~3.0 mm, rigid tongue stop 7.2 mm, trim at 77.1 deg (x = -14.2), bolt pitch 90 at y = -23.5,
  plug volume 0.43 L, silicone growth 11.7/15.2/18.7 mm: all reproduce.
- Pressure arithmetic (gauge + 1 bar under full vacuum) is right; only the force model is incomplete (HIGH 3).
- Bag outside everything, silicone in the V, no wood top piece, all-metal nuts, no bonded Al liner: right calls.
- Wood is not crushed at 0.8 MPa; the limits are moisture, temperature and glue, as the research note says.

## The three changes I would insist on before machining

1. Web: relieve the butt faces so the web lands are the only contact; any stop is a bolt-station shim set below the
   cured web (0.34-0.36), and the coupon's sectioned web sets the final value.
2. Plug: no FEP across the V, a measured 0.22-0.25 mm spacer for casting, a keyed spine; fix the drawing and explainer
   claims that the flanges "have met" below 3 mm and that the area ratio is 5.4.
3. Wood and radius: name a heat-rated adhesive (or use 30 mm ply), rough-bake-finish-seal in that order, three coupon
   radii, and do not cut the long blocks' radius until the coupons (or Aditya's measured mould) say what it is.

## What changed after this review (2026-11-02, commit ab65bd7 and the one after it)

Reviewer: a fresh Claude subagent, same model family. No second family was reachable this afternoon (Sonnet
timed out, Gemini quota until 11-03 08:00, Codex until 11-04, no local model), so this is a same-family review.

- BLOCKER 1: butt faces relieved 0.5 each side so only the web lands touch; the 0.40 shim stop is gone; 0.36 mm
  stops sit at the two trim ends, in line with the web (the review suggested the bolt stations; the trim ends were
  chosen so a stop cannot sit under the part); bolts CLAMP at 2 N m, as at Caltech.
- BLOCKER 2: no FEP across the V (tip lands only); plug cast over a measured 0.22-0.25 mm spacer; drilled Al spine;
  explainer no longer says the flanges "have met" below 3 mm; first coupon sectioned at the root.
- HIGH 3: net area ratio 3.6 (outer face 54 less the plug push 18), web 1.4-2.9 MPa, friction noted.
- HIGH 4: coupon radii 15.2, 16.5, 18.0, 19.6 (four, one more than asked, to cover the constant-curvature-change
  case); long blocks roughed only until the coupons are read.
- HIGH 5: order is rough, bake to constant mass, finish, seal.
- HIGH 6: one 35 mm phenolic birch strip per block (no glueline); fallback 2 x 18 mm with an epoxy whose post-cured
  Tg is above the cure temperature, glueline at x = -18.2, outside the trim.
- HIGH 7: "change only the block material" corrected; vacuum take-off, silicone hose, in-bag gauge and hot leak
  test back in the BOM and plan.
- Not changed: block width stays 30.0 with the web lands 0.40 apart.
