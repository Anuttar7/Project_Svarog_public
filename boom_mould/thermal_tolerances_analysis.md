# Thermal Tolerances & Thermo-Elastic Mismatch Analysis

## 1. Material Properties & CTE
| Material | Coefficient of Thermal Expansion (CTE, $\alpha$) | Maximum Service Temp | Source |
|---|---|---|---|
| **Aluminium 6082/6061 Face Sheet** | $23.4 \times 10^{-6}\text{ K}^{-1}$ | $250^\circ\text{C}$ (overaged) | Metals Handbook |
| **Densified Wood (Permali / Jabroc)** | $5.0 \times 10^{-6}\text{ K}^{-1}$ (in-plane $\parallel$) | $200^\circ\text{C}$ | Permali Composites TDS |
| **Epoxy Tooling Board (Lab 1000)** | $35.0 \times 10^{-6}\text{ K}^{-1}$ | $190^\circ\text{C}$ | Alchemie Ltd TDS |
| **Carbon/Epoxy Woven ($0^\circ$)** | $-0.5 \times 10^{-6}\text{ K}^{-1}$ to $+1.5 \times 10^{-6}\text{ K}^{-1}$ | $180^\circ\text{C}$ | Ansys ACP material.apdl |
| **Carbon/Epoxy Through-Thickness ($33$)** | $35.0 \times 10^{-6}\text{ K}^{-1}$ to $45.0 \times 10^{-6}\text{ K}^{-1}$ | $180^\circ\text{C}$ | Literature / Fernandez 2017 |

## 2. Longitudinal Differential Thermal Expansion
Considering an elevated cure temperature cycle from $T_0 = 20^\circ\text{C}$ to $T_{cure} = 180^\circ\text{C}$ ($\Delta T = 160\text{ K}$):
- Thermal strain of Aluminium face:
  $$\epsilon_{Al} = \alpha_{Al} \cdot \Delta T = 23.4\times 10^{-6} \times 160 = 3.744\times 10^{-3} = 0.3744\%$$
- Thermal strain of Densified Wood backing:
  $$\epsilon_{wood} = \alpha_{wood} \cdot \Delta T = 5.0\times 10^{-6} \times 160 = 0.800\times 10^{-3} = 0.0800\%$$
- Differential thermal expansion strain:
  $$\Delta\epsilon = \epsilon_{Al} - \epsilon_{wood} = (23.4 - 5.0)\times 10^{-6} \times 160 = 2.944\times 10^{-3} = 0.2944\%$$
- Total longitudinal slip over a $500.0\text{ mm}$ mould length:
  $$\Delta L_{mismatch} = L_0 \cdot \Delta\epsilon = 500.0\text{ mm} \times 2.944\times 10^{-3} = \mathbf{1.472\text{ mm}}$$
- At maximum test temperature $200^\circ\text{C}$ ($\Delta T = 180\text{ K}$):
  $$\Delta L_{mismatch} = 500.0\text{ mm} \times (18.4\times 10^{-6} \times 180) = \mathbf{1.656\text{ mm}} \quad (\mathbf{0.331\%})$$

## 3. Bimetallic Warping (Timoshenko Bimetal Model)
If the aluminium face sheet of thickness $t_1 = 1.0\text{ mm}$ were rigidly bonded with high-temperature epoxy to a wood core of thickness $t_2 = 25.0\text{ mm}$ over length $L = 500\text{ mm}$:
- The mismatch strain $\Delta\epsilon = 0.294\%$ would induce a severe thermal bending moment.
- The resulting curvature $\kappa$ causes a mid-span vertical bow:
  $$\delta \approx \frac{\kappa \cdot L^2}{8}$$
  With $\kappa \approx 3.2\times 10^{-4}\text{ mm}^{-1}$, the tool bows upwards by:
  $$\delta \approx \frac{3.2\times 10^{-4} \times 500^2}{8} \approx \mathbf{10.0\text{ mm}}$$
  A $10\text{ mm}$ bow over $500\text{ mm}$ completely destroys boom straightness, far exceeding allowable camber ($< 1\text{ mm}$).
- **Mechanical Relief Implementation:**
  The face sheet is attached to the backing tool using:
  1. A central $\varnothing 4\text{ mm}$ precision stainless steel dowel at $X = 250\text{ mm}$ acting as the stationary longitudinal datum.
  2. Four slotted shoulder screws ($8\text{ mm}$ longitudinal slot) with spring washers at $X = 50\text{ mm}$ and $X = 450\text{ mm}$.
  3. The face sheet expands freely along the slot ($\pm 0.8\text{ mm}$ at each end), eliminating all bimetallic bending moments while holding transverse alignment within $\pm 0.05\text{ mm}$.

## 4. Cross-Sectional Dimension Errors at Cure Temperature
- Mid-surface arc radius ($R = 15.10\text{ mm}$):
  $$\Delta R = 15.10\text{ mm} \times 23.4\times 10^{-6}\text{ K}^{-1} \times 160\text{ K} = \mathbf{+0.056\text{ mm}} \quad (+0.37\%)$$
- Central web width ($w = 10.00\text{ mm}$):
  $$\Delta w = 10.00\text{ mm} \times 23.4\times 10^{-6}\text{ K}^{-1} \times 160\text{ K} = \mathbf{+0.037\text{ mm}} \quad (+0.37\%)$$

## 5. Laminate Cooling Spring-In Angle
When the cured composite cools from $180^\circ\text{C}$ to $20^\circ\text{C}$ ($\Delta T = -160\text{ K}$), the difference between the through-thickness expansion ($\alpha_{33} \approx 40\text{ ppm/K}$) and the in-plane fiber expansion ($\alpha_{11} \approx 0\text{ ppm/K}$) causes spring-in of the $90^\circ$ circular flange:
$$\Delta\theta = \theta \cdot (\alpha_{33} - \alpha_{11}) \cdot \Delta T = 90^\circ \times (40 - 0)\times 10^{-6} \times (-160) = \mathbf{-0.576^\circ}$$
Applying an empirical safety multiplier of $1.5\times$ for resin-rich inner corner zones yields an expected spring-in contraction of:
$$\Delta\theta \approx -0.85^\circ \text{ to } -1.20^\circ$$
The tool mandrel radius should be machined with a corresponding spring-in factor ($0.835$ to $0.900$) as validated by coupon testing.

**Correction, 2 Nov 2026.** The estimate above understates spring-in by an order of magnitude for this geometry. Leclerc et al. (Caltech TRAC, 2017/2018) measured a 90 deg flange on an R12.7 tool cure to 105 deg at R10.6, which is where 0.835 comes from (10.6 / 12.7). A 1 deg change could not produce that factor. The tool is therefore larger than the part; the v4 plan brackets it at R15.2 to R19.6 and sets it from coupons. See `v4/README.md`.
