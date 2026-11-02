# Svarog mould v4: autoclave research (2 Nov 2026)

Scope: closed three-piece mould, 390 mm long, ~30 x 54 mm blocks, carbon prepreg TRAC boom, envelope bag, autoclave 120-180 C, 3-7 bar.
Every claim carries its source. UNSOURCED means I looked and did not find one. Quotes are verbatim from the page or PDF.

## 1. Imperial composites autoclave

- Imperial has two autoclaves: "our 1 m diameter autoclave with a maximum temperature and pressure of 450ºC and 28 bar respectively, or the smaller 50 cm autoclave as appropriate." Source: Composites Centre Brochure 2025, Facilities section, https://www.imperial.ac.uk/media/imperial-college/faculty-of-engineering/aeronautics/Composites-Centre-Brochure-2025_WEB.pdf
- Same brochure: "We also have a large capacity autoclave to cure thermosets, and a smaller autoclave for use where that is appropriate." Also heated presses "maximum platen size of 500 mm x 500 mm ... 400 kN and 400ºC".
- Make/model, chamber length, building/room: UNSOURCED. The brochure gives diameters only. A comparable lab unit (Scholz, Khalifa University) is "1meter dia. and 2meter long with a maximum operating temp of 400˚C and 21 bar", https://khazna.ku.ac.ae/en/equipments/hot-air-autoclave/ . Ask the technician for the 50 cm unit's length: a 390 mm tool plus bag should fit either.
- Takeaway: the autoclave's ratings are far above the cure, so the limits come from the tooling, not the vessel.

## 2. Tooling materials at 120-180 C and 3-7 bar

| Material | Rated temperature | Compressive strength | Source |
|---|---|---|---|
| RAKU-TOOL WB-1222 (PU working board) | HDT (ISO 75) 80-90 C | 60-70 MPa | RAMPF board overview, https://www.rampf-group.com/fileadmin/Downloads/RAD/RAD-TM/boards-raku-tool-product-overview-en.pdf |
| RAKU-TOOL WB-1404 | HDT 75-80 C | 85-95 MPa | same |
| RAKU-TOOL WB-0700 (prepreg lay-up board) | HDT 130-140 C, "Temperature resistant up to 130°C", "Lay-up tools for prepregs" | 60-70 MPa | same |
| Sika LAB 975 | "for temperatures up to 130 °C", HDT 130 C | 50 MPa | https://industry.sika.com/dam/dms/global-industry/3/FLY-LAB-975-New-gb.pdf (via search snippet) |
| SikaBlock M976 EP | HDT 120 C, "master-models for composite molds made with prepregs in autoclave" | 67 MPa | https://industry.sika.com/content/dam/dms/deaddconst01/p/sikablock-m976-ep.pdf (via search snippet) |
| Phenolic-film birch ply (WISA-Form Birch) | no temperature rating published; "Moisture content 8-12 %"; film "120 g/m2 or 220 g/m2" | through-thickness compression UNSOURCED | https://www.specifiedby.com/upm/wisa-form-birch/UPM_WISA-Form-Birch_Technical_Fact-Sheet.pdf |
| MDF (incl. MR) | UNSOURCED rating; forum: "too porous to establish a vacuum, much less a seal at autoclave pressures" and may "warp, scorch, decompose, outgas, crack" | UNSOURCED | https://www.boatdesign.net/posts/63523 (2005 forum, anecdotal) |
| Beech/maple hardwood | UNSOURCED | UNSOURCED | none found |
| Aluminium 6082 | no practical limit at 180 C | n/a | CTE row in section 4 |

- WB-1222 and WB-1404 are polyurethane boards with HDT under 90 C. They are wrong for any prepreg cure. No epoxy board in the RAMPF/Sika ranges I found goes past ~130-140 C; a 180 C cure needs metal, tooling prepreg or a dedicated high-temp board confirmed with the supplier.
- Wood at 180 C degrades: birch heated to 180 C for 1-2.5 h lost considerable strength and hardness, linked to "loss of mass and increase in concentrations of formic and acetic acid" (Sundqvist et al. 2006, seen via search snippet only; primary URL not confirmed). Birch at 200 C lost 6.4-10.2 % dry mass (Finnish study, same caveat). Hemicellulose "degradation is responsible for bending strength loss", https://bioresources.cnr.ncsu.edu/?p=3316 (snippet; exact page not confirmed).
- Wood moisture: the ply arrives at 8-12 % water (WISA above). In a 120-180 C cycle that water turns to steam behind the seal coat. Drying practice from a wood-tooling patent: the preform "is first slowly dried to prevent cracking", vacuum bag in an autoclave held "around 90° C. to 120° C. for several hours", vacuum "enhancing the process of moisture removal prior to the water turning to steam" (USPTO 6673279, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6673279 ). Practical reading: bake the machined blocks at or above cure temperature for several hours, seal while warm, then dry-cycle once.
- Another patent: keep cure "low enough that the wooden pattern or mould does not distort and can therefore be used again", https://data.epo.org/publication-server/rest/v1.2/patents/EP0076673NWB2/document.html
- Plywood used commercially for heated tools gets a separate face: "pairs of naval construction type plywood, with a carbon epoxy skin" for an OOA cure at 145 C, https://www.multiplast.eu/en/industrial-composite/civil-market/tooling/tooling-low-cost.html
- Sealers: Zyvax Sealer GP thermal stability "to 500 º F (260 º C)" (older Zyvax deck, https://www.slideshare.net/slideshow/waterworks2008/1159024 ); Zyvax notes "wood, plaster, metal, and composite all have differing levels of porosity". No sealer TDS I found names wood or MDF as a substrate: UNSOURCED for wood specifically.
- Cycles a wood tool survives in an autoclave: UNSOURCED. The only reuse number found is for concrete formwork, WISA "20 – 80 times", irrelevant to a 180 C cycle.
- Crushing: autoclave pressure 0.3-0.7 MPa is two orders below the board strengths above. Crushing is not the failure mode; moisture, degradation and movement are.

## 3. How autoclave pressure reaches the part in a closed matched tool

- Matched tooling relies on the stack seating: Maes et al. 2025, Composites Part A 196:108924: "The matched tooling showed a reduced corner pressure", "indicative of lack of contact due to bulk factor in the flange regions"; internal tooling "showed reduced pressure due to bridging, resulting in local corner thickening". https://research-information.bris.ac.uk/en/publications/shape-change-of-composite-corners-due-to-tooling-pressure-distrib/
- Hard stops: fixed mould parts act as stoppers that set enclosed-wall thickness, whereas open walls "can be controlled by the external pressure applied during cure" (US 10507600, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10507600 ). Once a rigid tool bottoms on its stops, extra autoclave pressure goes into the stops, not the laminate.
- Floating caul: "The autoclave pressure is what causes the caul 12 to be drawn into engagement with the support flange 20", and the stop restrains it "when all laminate motion has ceased" (US 6696009, https://patents.google.com/patent/US6696009 ).
- "uniform pressure on an autoclave's vacuum bag does not necessarily mean uniform pressure on the part", https://compositesworld.com/articles/press-molding-method-emulates-autoclave
- Campbell, Manufacturing Processes for Advanced Composites (Elsevier 2004), chapters on Tooling, Vacuum Bagging and Curing cover this; I could not reach the text, so no quote: UNSOURCED beyond the listing https://shop.elsevier.com/books/manufacturing-processes-for-advanced-composites/campbell-jr/978-1-85617-415-2
- Arithmetic (mine, not sourced): a floating upper piece of 390 x 30 mm projected area at 6 bar gauge plus vacuum (~0.7 MPa) receives ~8.2 kN; at 54 mm width, ~14.7 kN. That force goes into the laminate only while the piece is free to move. The two bolted lower blocks press each other only by bolt preload, and that preload falls as wood dries and creeps. Leave a gap at every stop so the floating piece never bottoms.

## 4. Fixing a 0.5 mm aluminium liner to wood

- CTE, aluminium 1050A: 23.5 x10^-6/K (20-100 C), 24.4 (20-200 C), https://my.bikar.com/en_US/products/300_021-300-021-2
- CTE, wood along grain: "typically ranging from 3.1 to 4.5 × 10−6 K−1 for hardwoods and softwoods", radial/tangential "about 5 to 10 times greater", https://www.degruyterbrill.com/document/doi/10.1515/hf-2025-0121/html (citing the Wood Handbook)
- CTE, plywood in-plane: about 3.4 x10^-6 per F (6.1 x10^-6/K); thickness "approximately 16 x 10-6 inch/inch per degree F (negligible)", attributed to APA but from a forum post, https://www.finehomebuilding.com/forum/how-much-does-a-plywood-subfloor-move . Treat as indicative.
- Differential growth over 390 mm at dT = 130 K (my arithmetic): Al 1.19-1.24 mm; ply 0.16-0.31 mm; mismatch about 0.9-1.1 mm. Wood also shrinks as it loses its 8-12 % moisture during the cycle, which widens the gap; magnitude UNSOURCED.
- A rigid bond over 390 mm has to absorb ~1 mm of shear at the ends, cycled, which is the debond-and-bow case. No source found on bonding metal facings to wood or tooling board specifically: UNSOURCED.
- PSA: 3M 9485PC TDS "Short Term Temperature Resistance 450 °F", "Long Term Temperature Resistance 121 °C"; the 3M Ireland page gives conflicting figures, https://www.3mireland.ie/3M/en_IE/p/d/b40065908/ . Fine for a 120 C cure; marginal for hours at 180 C; and a PSA lets the sheet creep, which helps with CTE but blurs location.
- Mechanical fixing with slotted holes: no source found for this application, UNSOURCED. Engineering practice (mine): fix one end with round holes, slot the rest along the length by at least 1.5 mm, countersunk screws away from the part face.

## 5. Release at 180 C

- FEP film: Airtech A4000 "260°C (500°F)" max use, with "testing prior to use" advised, https://beta.airtech.com/product-details/release-films/1515-a4000
- Frekote 700-NC: application range 13-135 C; thermal stability up to 400 C (Henkel zh-CN TDS, https://datasheets.tdx.henkel.com/LOCTITE-FREKOTE-700-NC-zh_CN.pdf ). It is a semi-permanent release for a sealed, non-porous face, so seal wood first.
- Wood-on-wood butt faces: a strip of FEP film or Frekote over the sealer. No source names wood butt joints specifically: UNSOURCED.

## 6. Silicone V-plug (Leclerc, Pedivellano & Pellegrino 2018)

- The method: layup wrapped "over two U-shaped aluminum molds", "clamped together using multiple bolts", then "A silicone plug with a V shape is added, allowing pressure to be applied along the V-groove ... The silicone used is Smooth-On's Mold Max XLS II, chosen due to its very low shrinkage during cure. Then, a vacuum bag encloses the full assembly and curing is done in autoclave." AIAA 2018-0690, https://authors.library.caltech.edu/records/rbm1k-p9p24/files/Leclerc_Pedivellano_Pellegrino2018.pdf?download=1
- Note: their molds were aluminium, not wood. The prepreg was NTPT ThinPreg 402; cure temperature is not stated in that paragraph.
- Mold Max XLS II, https://www.smooth-on.com/products/mold-max-xls-ii/ : Shore 30A; pot life 40 min; "cure for 24 hours at room temperature (73°F/23°C)"; shrinkage 0.001 in/in; maximum useful temperature 400 F (204 C); post-cure "an additional 4 hours at 150°F (65°C)". At 180 C it is within its rating but close to it; post-cure before first use so it does not outgas into the bag.
- Higher-temperature alternatives:
  - Smooth-On Mold Max 60, "heat resistant up to 560˚F/294˚C", Shore 60A, https://www.smooth-on.com/assets/pdf/catalogs/CATALOG-SO.pdf
  - Airtech Airpad HTS 5553, fibreglass-reinforced silicone, 232 C (450 F), https://beta.airtech.com/product-details/rubber/1036-airpad-hts-5553
  - Airtech Airpad (uncured non-silicone rubber sheet, no silicone contamination), 204 C (400 F), https://beta.airtech.com/product-details/rubber/1029-airpad
- Silicone CTE: a forum post gives ~250 x10^-6/K linear (https://ns1.engineersedge.com/wwwboard/posts/6918.html , weak). Volumetric is about three times linear. The silicone bulk modulus "defines the rate of pressure applied by the rubber to the preform material during thermal expansion", and the pressure "dictates the volume of silicone rubber to be used in relation to the volume of the rigid mold cavity" (NASA-hosted patent, https://ntrs.nasa.gov/api/citations/19990008579/downloads/19990008579.pdf ).
- What it does in the V (my arithmetic): dT 100-160 K x ~750 x10^-6/K gives 7.5-12 % free volume growth. If the plug is boxed in by rigid blocks with no free face, that cannot happen and pressure rises far above autoclave pressure (silicone bulk modulus around 1 GPa, UNSOURCED), enough to push blocks apart or split wood. If the plug's top face is under the bag, as Leclerc did, the extra volume bulges out and the V pressure stays near autoclave pressure plus a modest thermal increment. Design rule: give the plug a free face under the bag, or size its volume deliberately.

## 7. Spring-in sign

- L-shaped parts: "a decrease of the enclosed angle is observed" after demoulding and cooling, https://research.utwente.nl/en/publications/prediction-of-spring-forward-in-continuous-fibrepolymer-l-shaped-/ ; "Chemical shrinkage of the epoxy causes the enclosed angle of curved sections and angle components to be reduced", https://scholarworks.indianapolis.iu.edu/items/09c3f4a2-ed7b-4434-9b6f-aabd6f41f3c0/full
- Mechanism: Radford & Diefendorf 1993 (J. Reinf. Plast. Compos. 12:58-75): spring-in depends on the difference between in-plane and through-thickness properties, https://journals.sagepub.com/doi/10.1177/0021998306068072 (citing paper).
- So spring-in increases the bend (turning) angle. With the arc length fixed by the fibres, the radius gets smaller than the tool's.
- Leclerc 2018 confirms this, with one correction: the nominal radius was r = 12.5 mm, not 12.7. "nominal geometric parameters are: r = 12.5 mm, θ = 90°"; after cure "spring-in of both flanges ... r = 10.6 mm, θ = 105°" (paper above). Arc check: 12.5 x 90° = 19.63 mm; 10.6 x 105° = 19.43 mm, 1 % apart, so arc length holds. Pure arc conservation predicts 10.71 mm.

## Recommendation

1. For any cure above ~130 C, use aluminium 6082 blocks. Thermal expansion matches the liner and the silicone plug sits as in Leclerc, and nothing outgasses.
2. If it must be wood, use phenolic birch ply only for a cure at or below ~130 C. Bake it for several hours at or above cure temperature, seal it hot with a high-temperature sealer, and do one empty dry cycle in the bag before laying up.
3. Do not bond the 0.5 mm aluminium liner over 390 mm of wood. The ~1 mm differential will shear or bow it. Either drop it (seal plus FEP film or Frekote does the release job) or fix one end and slot the rest by at least 1.5 mm.
4. Never use RAKU-TOOL WB-1222 or WB-1404: HDT 75-90 C.
5. The silicone V-plug (Mold Max XLS II, 204 C rated, post-cured) needs a free face under the bag. Every rigid stop needs a gap so the floating piece never bottoms.
6. Caveat: the cure temperature of the actual prepreg is not fixed here. Get it from the prepreg TDS and the lab technician before machining, together with whether Imperial's autoclave accepts wood tooling at all (UNSOURCED).
