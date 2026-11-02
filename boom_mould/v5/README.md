# Boom mould v5: the v4 closed tool with a floating aluminium liner (draft, 2 Nov 2026)

Status: draft for the structures team. Nothing is cut yet. It builds on `../v4/` (same blocks, plug, bag and autoclave route) and changes only the forming face.

## Why the aluminium sheet goes back on

Version 4 dropped the sheet for two reasons. A vacuum bag could not press a badly formed sheet flat, and glued to the wood it would tear off, because over the cure it grows nearly a millimetre more than the plywood. v5 bends it over a tighter former first (R14.8) so it already fits the block, and does not glue it: one screw in the middle and two in slots, through a 6 mm return flange on the outer face, with release film underneath, so it slides every cure. The laminate then cures against smooth metal, and the wood's end grain and moisture stay behind the sheet. One of the five coupon pairs runs without the sheet; if it comes out as good, the long tool goes without it.

## Files

| File | What it is |
|---|---|
| `calc5.py`, `calc5_output.txt` | liner geometry, forming and springback, seating, thermal growth and friction, tolerances, fixing. Imports `../v4/calc4.py` |
| `drawing5.py`, `mould_v5.pdf`, `mould_v5.png` | A3 sheet: section, root detail, plan, liner blank, coupon table, notes |
| `pack_v5.pdf` | 2-page handout for the team |
| `session_2026-11-02.pdf` | 1-page sheet for the 2 Nov session |
| `svarog_mould_v5_print.pdf` | drawing, handout and session sheet in one file |
| `review-v5-adversarial.md` | engineering review of v5 and what changed because of it |
| `readability-review-v5.md` | design review of the documents, 4 rounds to a pass |
| `model-split-v5.md`, `bake-v5/` | which AI model did which part and the comparison behind it |

Run `python3 calc5.py` then `python3 drawing5.py` from this folder.

## Open

Prepreg cure temperature (wood is limited to about 130 °C); whether the lab vents the bag in the autoclave; whether the 1050A sheet was ordered and in which temper (H14 needed); the 130 °C friction pull test (above 0.15, use 5754-H22).
