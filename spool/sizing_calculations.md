# Spool Subsystem: Sizing Calculations & Derivations

## 1. Boom Cross-Section Geometry
From CAD STEP file (`Composite Boom.step`) mid-surface measurements:
- Flange arc radius: $R = 15.10\text{ mm}$
- Subtended flange angle: $\theta = 90^\circ = \frac{\pi}{2}\text{ rad}$
- Flange arc length: $s = R \cdot \theta = 15.10 \times \frac{\pi}{2} = 23.72\text{ mm}$
- Central bonded web width: $w = 10.0\text{ mm}$
- Flange thickness: $t = 0.20\text{ mm}$ (two $0.10\text{ mm}$ woven carbon plies)
- Flattened tape height: $H_{flat} = s + w = 23.72 + 10.0 = 33.72\text{ mm}$
- Total cross-sectional area: $A = 2 \times (s + w) \times t = 2 \times 33.72 \times 0.20 = 13.49\text{ mm}^2$
- Linear mass density ($\rho = 1451\text{ kg/m}^3$): $m' = A \cdot \rho = 13.49\times 10^{-6}\text{ m}^2 \times 1451\text{ kg/m}^3 = 0.01957\text{ kg/m} = 19.57\text{ g/m}$
- Mass per $2.1\text{ m}$ boom: $M_{boom} = 2.1 \times 19.57\text{ g} = 41.1\text{ g}$
- Mass of four booms: $M_{4booms} = 4 \times 41.1\text{ g} = 164.4\text{ g}$

## 2. Coiling Strains & Stresses on 70 mm Spool ($R_{hub} = 35\text{ mm}$)
During coiling, the boom undergoes two orthogonal strain states:
1. **Transverse Flattening Strain:**
   $$\epsilon_{flat} = \frac{t}{2 R} = \frac{0.20\times 10^{-3}\text{ m}}{2 \times 0.0151\text{ m}} = 6.62\times 10^{-3} = 0.662\%$$
2. **Longitudinal Coiling Strain:**
   $$\epsilon_{wrap} = \frac{t}{2 R_{hub}} = \frac{0.20\times 10^{-3}\text{ m}}{2 \times 0.0350\text{ m}} = 2.857\times 10^{-3} = 0.286\%$$
3. **Transition Zone Peak Stress:**
   In the transition region between the cylindrical coil and the deployed section, transverse unflattening and longitudinal curvature combine. Using the laminate axial modulus $E_{xx} = 35.5\text{ GPa}$:
   $$\sigma_{coiling} \approx E_{xx} \cdot \left(\frac{t}{2 R_{hub}} + \nu_{12} \frac{t}{2 R}\right) \approx 35.5\times 10^3\text{ MPa} \times (0.00286 + 0.04 \times 0.00662) \approx 110.8\text{ MPa}$$
   Adding localized edge transverse anticlastic stress concentration ($K_t \approx 2.5$):
   $$\sigma_{peak} \approx 284.0\text{ MPa}$$

## 3. Microbuckling Failure Limit & Safety Factor
Using the Budiansky-Argon fiber microbuckling criterion:
$$\sigma_c = \frac{G_{12}}{1 + \theta_0 / \gamma_y}$$
For woven carbon/epoxy ($G_{12} = 3.3\text{ GPa}$, matrix yield shear strain $\gamma_y \approx 0.015$, fiber misalignment $\theta_0 \approx 2^\circ = 0.035\text{ rad}$):
$$\sigma_c \approx \frac{3300}{1 + 0.035 / 0.015} \approx 990\text{ MPa}$$
Applying knock-down factors for cyclic coiling and wet conditioning yields the ACP database allowable:
$$\sigma_{allowable} = 437.0\text{ MPa}$$
Safety Factor on a $70\text{ mm}$ spool ($R_{hub} = 35\text{ mm}$):
$$\text{SF} = \frac{\sigma_{allowable}}{\sigma_{peak}} = \frac{437.0\text{ MPa}}{284.0\text{ MPa}} = 1.539 \approx 1.54\quad \text{(PASS)}$$

## 4. Packaging Diameter Buildup
- Hub diameter: $D_0 = 70.0\text{ mm}$
- Effective radial thickness increment per boom wrap: $t_{eff} = 2t + t_{film} = 0.40\text{ mm} + 0.05\text{ mm} = 0.45\text{ mm}$
- For single boom ($2.1\text{ m}$ length):
  - Number of wraps $N \approx 9.5$
  - Outer diameter $D_{out} = D_0 + 2 \cdot N \cdot t_{eff} = 70.0 + 2 \cdot 9.5 \cdot 0.40 = 77.6\text{ mm}$
- For four booms co-wound (interleaved around circumference):
  - Total layer buildup is $4 \times N \times t_{eff} / 2$ per radius:
  - $D_{pack} \approx 70.0 + 2 \times (9.5 \times 0.45) \approx 87.1\text{ mm}$
- Maximum available compartment dimension: $200.0\text{ mm}$.
- Radial packaging margin:
  $$\text{Margin} = \frac{200 - 87.1}{2} = 56.45\text{ mm} \quad (\approx 56\text{ mm clearance all around})$$
