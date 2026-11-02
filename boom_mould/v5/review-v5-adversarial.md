# Adversarial review, Svarog mould v5 (floating aluminium liner), 2026-11-02

Reviewer: Claude Sonnet 5.5 subagent, fresh context, given calc5.py, calc5_output.txt, calc4_output.txt and
review-v4-adversarial.md, told to recompute every number it challenged. The same prompt (outputs only) went to
two local models, qwen2.5:7b-instruct and llama3.2:3b; their findings and why none was kept are at the end.
Gemini (quota until 3 Nov 08:00) and Codex (until 4 Nov 10:07) were probed at 15:31 and refused.

## Sonnet findings (verbatim in substance)

VERDICT: do not cut or order as specified. The H14 liner cannot be seated or laid up on as written, the friction
check ignores the web-land pressure, and the "same as Leclerc" claim is unsupported. Geometry and arithmetic of
calc5 otherwise right.

1. BLOCKER: H14 springs from R17.5 to R21.4 free; with three tip-land screws and a free web edge, the free edge
   stands ~3.8 mm proud of the wood. Cold fit to a 0.1 mm feeler is impossible by hand. Fix: pre-form over an
   overbend former (R14.8, outer-fibre strain 1.7 %), check against a template; or O temper.
2. HIGH: p L^2/8 is a simply-supported midspan moment. A lifted lip closes only over lambda = sqrt(2m/p), end gap
   ~0.42 dkappa lambda^2: 0.72 mm at 0.09 MPa, 0.16 at 0.4, 0.08 at 0.8. The "5-10x margin" is not real.
3. HIGH: the web lands carry the block closing pressure (1.44 / 2.88 MPa), not bag pressure. At mu 0.1 that is
   28 / 56 N/mm on a 42.5 N/mm H14 yield. mu 0.1 for Frekote at 130 C is a hope. Cooldown reverses slip.
   Fix: measure mu (pull-out at 130 C); FEP/PTFE interlayer under the web lands; or pin plus slots only.
4. HIGH: "aluminium face matches Leclerc, so 0.835 is preserved" is unsupported. Mismatch strain liner/laminate
   ~0.23 %; friction could put 39-78 MPa into the 0.2 mm ply, compressive on cooling (Twigg et al. 2004: thin
   parts worst). Fix: coupons with and without liner, same cure; drop the sentence until measured.
5. MEDIUM: +-0.04 liner on each web face moves the web gap +-0.08 (~22 %). Micrometer at 3 points, reject spread
   above 0.02.
6. MEDIUM: a 90 deg countersunk M3 head cannot sit flush in 0.5 mm sheet (~1.3 mm proud); it prints into the plug.
7. MEDIUM: the liner stops 0.5 mm above the gallery but the laminate web runs the full 10 mm, so the web end
   falls past the liner edge. Liner must run >= 3 mm past the web end. State stops and dam vs the 390 liner.
8. MEDIUM: dT 110 assumes a 130 C cure; at 150 C (dT 130) growth is 0.89 mm, friction figures +18 %.

Confirmed: springback values, blank arithmetic, thermal growth, arc friction arithmetic, +-0.2 % radius effect,
v4 fixes not broken.

## What v5 did with each (calc5.py, drawing5.py, same commit)

1. Accepted. Liner pre-formed over a CNC'd overbend former (radius solved in calc5 section 2) and checked cold
   against the block with a feeler before lay-up.
2. Accepted. Lip model replaces p L^2/8; the bag is no longer relied on to seat the liner.
3. Partly accepted. The sheet is a membrane 49 mm wide, so friction is summed over the whole developed width
   (web strip at block pressure plus arc and tip land at bag pressure) against the yield of the whole section;
   the strip-only figure is also printed. FEP film under the web lands only; mu measured in a 130 C pull test
   before the long liner is fitted; 5754-H22 named as the fallback if mu > 0.15.
4. Accepted. The 0.835 sentence is gone. A fifth coupon pair at R18.0 runs bare in the same cure: the liner stays
   on the long tool only if the lined coupon is as good as the bare one.
5. Accepted.
6. Accepted, differently: the liner gets a 6 mm return flange down each block's outer face, screwed there with
   pan-head M3 under the bag only. Nothing on the tip land, nothing under the plug.
7. Accepted. Wood web land lengthened to 13 mm; gallery moved to y = -13; liner to y = -12.5; prepreg web cut to 10.
8. Accepted. Both 130 C and 150 C cures printed.

## Local models (same prompt, outputs only)

qwen2.5:7b-instruct, 4 findings: (1) "align tool face R18 with wood R17.5" misreads the 0.5 mm liner offset;
(2) "margin too conservative, aim for 1-2x" is not an engineering objection; (3) recommends mu 0.1, which calc5
already chose; (4) "1.0 mm clearance above the gallery" with no reason. Valid: 0 of 4.
llama3.2:3b, 7 findings: each restates a calc line and says "recalculate" with no number. Valid: 0 of 7.
