# Svarog Composite Deployable Booms: High-Temperature Boom Mould Design

## Mission & Tooling Context
Based on the Imperial Composites Laboratory requirements and task `icss-briefs/2026-10-30T1300-boom-mould-by-sunday`, this subsystem establishes the tooling design, thermal tolerance budget, and cut list for manufacturing the composite TRAC boom sections.

- **Lab Oven:** Imperial College Composites Laboratory oven with an internal chamber of $500\text{ mm} \times 500\text{ mm}$ (horizontal orientation required by Aditya).
- **Tooling Concept:** High-temperature tooling core rated to $200^\circ\text{C}$ with a precision formed aluminium face sheet, bagged using Easy Composites vacuum consumables (VB200 film rated to $200^\circ\text{C}$, AT-200Y high-temperature sealant tape rated to $204^\circ\text{C}$).
- **Target Part:** TRAC composite boom section with mid-surface radius $R = 15.10\text{ mm}$, subtended angle $90^\circ$, flat central bonding web $w = 10.0\text{ mm}$, and cured flange thickness $t = 0.20\text{ mm}$ (two $0.10\text{ mm}$ woven plies).

---

## 1. Usable Section Length in the 500 x 500 mm Oven

To manufacture composite boom segments horizontally inside the $500\text{ mm} \times 500\text{ mm}$ internal chamber, clearances must be budgeted for:
1. **Oven Wall & Airflow Clearances:** $25\text{ mm}$ per side ($50\text{ mm}$ total) to ensure uniform convective circulation and prevent bag contact with oven heating elements or door seals.
2. **Vacuum Sealant Tape Allowance:** $15\text{ mm}$ width per side ($30\text{ mm}$ total) for AT-200Y / ST150 mastic tape.
3. **Breather & Pleat Margins:** $20\text{ mm}$ per side ($40\text{ mm}$ total) between the tool end and the tape line to prevent resin bridging and bag tensioning.
4. **Laminate End Trim Allowance:** $20\text{ mm}$ per side ($40\text{ mm}$ total) discarded post-cure to eliminate fiber wash, dry spots, and frayed fiber ends.

### Maximum Usable Section Lengths:
- **Straight Along One Side ($500\text{ mm}$ envelope):**
  - Maximum rigid tool length: $500 - 2 \times 25\text{ mm} = 450\text{ mm}$.
  - Usable trimmed boom length: $450 - 2 \times (15 + 20) = \mathbf{380\text{ to }400\text{ mm}}$.
  - Section count for $2.1\text{ m}$ boom: $\lceil 2100 / 380 \rceil = \mathbf{6\text{ sections}}$.
  - Section count for $3.0\text{ m}$ full boom: $\lceil 3000 / 380 \rceil = \mathbf{8\text{ sections}}$.
- **Along the Oven Diagonal ($707.1\text{ mm}$ envelope):**
  - Tool base width is $W = 80\text{ mm}$ (flange arc $23.7\text{ mm} + 10\text{ mm}$ web $+ 2 \times 23\text{ mm}$ sealing lands).
  - Geometry-limited diagonal tool length: $D_{eff} = \sqrt{500^2 + 500^2} - W = 707.1 - 80.0 = 627.1\text{ mm}$.
  - Subtracting $2 \times 25\text{ mm}$ oven wall clearances: $L_{tool} \approx 577\text{ mm}$.
  - Subtracting tape and trim waste: **Maximum usable trimmed boom length = $\mathbf{500.0\text{ mm}}$**.
  - Section count for $2.1\text{ m}$ boom: $\lceil 2100 / 500 \rceil = \mathbf{5\text{ sections}}$ (or 4.2).
  - Section count for $3.0\text{ m}$ full boom: $\lceil 3000 / 500 \rceil = \mathbf{6\text{ sections}}$.

---

## 2. Thermal Expansion Mismatch & Tolerances

- **Cure Temperature Cycle:** Room temperature $T_0 = 20^\circ\text{C}$ to cure temperature $T_{cure} = 180^\circ\text{C}$ ($\Delta T = 160^\circ\text{C}$; up to $\Delta T = 180^\circ\text{C}$ at $200^\circ\text{C}$).
- **Coefficients of Thermal Expansion (CTE):**
  - Aluminium (6082/6061 face sheet): $\alpha_{Al} = 23.4 \times 10^{-6}\text{ K}^{-1}$ ($23.4\text{ ppm/}^\circ\text{C}$).
  - Wood Substrate (along grain / in-plane): $\alpha_{wood,\parallel} \approx 5.0 \times 10^{-6}\text{ K}^{-1}$ ($5.0\text{ ppm/}^\circ\text{C}$).
  - Carbon Fiber Laminate (axial $0^\circ$): $\alpha_{CFRP,0^\circ} \approx -0.5 \times 10^{-6}\text{ K}^{-1}$.
- **Differential Expansion over $500\text{ mm}$ Length:**
  $$\Delta L_{mismatch} = L \cdot (\alpha_{Al} - \alpha_{wood}) \cdot \Delta T = 500\text{ mm} \times (23.4 - 5.0)\times 10^{-6}\text{ K}^{-1} \times 160\text{ K} = \mathbf{1.472\text{ mm}}$$
  At $200^\circ\text{C}$ ($\Delta T = 180^\circ\text{C}$): $\Delta L_{mismatch} = \mathbf{1.656\text{ mm}}$ ($\mathbf{0.33\%}$ length strain).
- **Bimetallic Curvature Hazard & Mechanical Relief:**
  If the aluminium face sheet is rigidly bonded/glued to the wood backing along its entire length, this $1.5\text{ to }1.7\text{ mm}$ differential expansion creates severe bimetallic warping, bowing the mould upwards by several millimetres and destroying boom straightness.
  **Design Solution:** The aluminium face sheet **MUST NOT** be continuously bonded to the wood. It is fixed with a rigid dowel pin at the longitudinal mid-span (datum center), and secured at the ends with slotted shoulder screws with Belleville spring washers. This allows the aluminium to slide longitudinally under thermal expansion while maintaining strict transverse alignment.
- **Cross-Sectional Growth & Spring-In:**
  - Radial growth at $180^\circ\text{C}$: $\Delta R = 15.10\text{ mm} \times 23.4\times 10^{-6} \times 160 = \mathbf{+0.056\text{ mm}}$ ($+56\,\mu\text{m}$, or $+0.37\%$).
  - Web growth at $180^\circ\text{C}$: $\Delta w = 10.0\text{ mm} \times 23.4\times 10^{-6} \times 160 = \mathbf{+0.037\text{ mm}}$ ($+37\,\mu\text{m}$).
  - Laminate Spring-in: Upon cooldown, through-thickness contraction exceeds in-plane contraction, causing the curved flanges to close inwards. **Corrected 2 Nov 2026:** Leclerc et al. measured $90^\circ \to 105^\circ$ and R12.7 to R10.6 on this process (about $15^\circ$, not $1^\circ$ to $2^\circ$); the factor $0.835$ is that ratio and the tool is larger than the part. Tool radius is set from coupons at R15.2/16.5/18.0/19.6 mm; see `v4/README.md`.

---

## 3. Tooling Substrate Material Analysis: Surviving 200 °C

1. **Standard MDF (Medium-Density Fibreboard): Strictly Rejected**
   - Binder: Standard MDF uses urea-formaldehyde or melamine-urea resins that undergo rapid thermal degradation and off-gassing starting at $100-120^\circ\text{C}$.
   - Entrapped moisture turns to steam under vacuum at $>100^\circ\text{C}$, causing severe internal blistering, delamination, and sudden vacuum bag puncture.
2. **Standard Birch Plywood (WBP exterior glue): High Risk / Not Recommended for 200 °C**
   - Phenol-formaldehyde glues survive short exposures up to $140-150^\circ\text{C}$, but degrade, embrittle, and char when cycled to $180-200^\circ\text{C}$.
3. **Recommended Material 1: Densified Laminated Wood (Permali / Jabroc / Delignit)**
   - Manufactured by compressing beech wood veneers under high pressure ($>10\text{ MPa}$) while fully impregnating with thermosetting phenolic resin.
   - Temperature rating: Continuous service up to $180-200^\circ\text{C}$.
   - Compressive strength: $>130\text{ MPa}$; low moisture absorption ($< 1\%$).
   - Excellent dimensional stability and vacuum tightness when edge-sealed with high-temperature epoxy.
4. **Recommended Material 2: High-Temperature Epoxy Tooling Board (Alchemie Lab 1000 / Necuron 1300)**
   - Synthetic epoxy block specifically formulated for prepreg tooling.
   - Temperature resistance up to $190^\circ\text{C}$, completely non-porous, CTE matched at $35-45\text{ ppm/}^\circ\text{C}$, no moisture outgassing.

---

## 4. Tracking & Design Status
> [!IMPORTANT]
> **No Invented Geometry Policy:** Detailed CNC toolpaths, dowel hole drill patterns, and segment splice joint geometries are marked as tracking issues. No unverified CAD files have been fabricated.

- Tracking Issue: [Issue #6: Boom Mould: 500 mm oven tooling, differential thermal expansion relief, and vacuum bag edge seals](https://github.com/thomasvanpul/Project_Svarog/issues/6)
- Companion Documents:
  - `oven_clearance_and_section_length.md`: Clearances, angles, and section count derivations.
  - `thermal_tolerances_analysis.md`: Detailed thermo-elastic mismatch calculations and spring-in equations.
  - `tooling_spec_and_cutlist.md`: Bill of materials, cut list, and vacuum bagging schedule.
  - `sources.md`: Technical datasheets and bibliographic references.
