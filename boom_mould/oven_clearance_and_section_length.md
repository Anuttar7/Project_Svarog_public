# Oven Clearance Allowances & Boom Section Length Derivations

## 1. Oven Chamber Constraints
- **Chamber Dimensions:** $500\text{ mm}$ width $\times 500\text{ mm}$ depth $\times 500\text{ mm}$ height internal.
- **Orientation:** Horizontal placement on oven rack shelf (Aditya requirement).

## 2. Clearance Budget per Edge
| Boundary Element | Dimension | Justification & Source |
|---|---|---|
| **Oven Wall Clearance** | $25\text{ mm}$ per end ($50\text{ mm}$ total) | Required for air convection circulation; prevents radiant hotspotting near side heating coils and avoids door gasket interference. |
| **Sealant Tape Width** | $15\text{ mm}$ per end ($30\text{ mm}$ total) | High-temperature vacuum mastic tape (AT-200Y or ST150) standard roll width is $12.7\text{ mm}$ ($1/2"$) to $15.0\text{ mm}$. |
| **Breather Buffer Margin** | $20\text{ mm}$ per end ($40\text{ mm}$ total) | Margin between tool edge and bag tape to allow breather cloth (BR180) to bridge bag without tension/bridging. |
| **Laminate End Trim Waste** | $20\text{ mm}$ per end ($40\text{ mm}$ total) | Trimming allowance for resin dry-spotting, weave distortion, and clean $90^\circ$ perpendicular guillotine cut. |
| **Total Tool End Overhead** | **$45\text{ mm}$ per end ($90\text{ mm}$ total)** | Combined tape + breather + trim allowance. |

## 3. Derivations

### Case A: Straight Along One Side
- Internal chamber dimension: $L_{chamber} = 500.0\text{ mm}$.
- Maximum allowable tool length:
  $$L_{tool,straight} = 500.0 - 2 \times 25.0 = 450.0\text{ mm}$$
- Maximum net trimmed boom segment length:
  $$L_{boom,straight} = 450.0 - (2 \times 15.0\text{ [tape]}) - (2 \times 20.0\text{ [trim]}) = \mathbf{380.0\text{ mm}}$$
  *(Can stretch to $400.0\text{ mm}$ if tape is applied directly to the tool end edge).*
- Number of sections needed for $2.1\text{ m}$ deployable boom:
  $$N_{sections} = \left\lceil \frac{2100\text{ mm}}{380\text{ mm}} \right\rceil = \mathbf{6\text{ sections}}$$
- Number of sections needed for $3.0\text{ m}$ full CAD boom:
  $$N_{sections} = \left\lceil \frac{3000\text{ mm}}{380\text{ mm}} \right\rceil = \mathbf{8\text{ sections}}$$

### Case B: Along the Oven Chamber Diagonal
- Chamber diagonal:
  $$D_{chamber} = \sqrt{500^2 + 500^2} = 500 \cdot \sqrt{2} \approx 707.1\text{ mm}$$
- Mould cross-sectional base width:
  - Flange arc projection: $15.1\text{ mm}$
  - Central web land: $10.0\text{ mm}$
  - Vacuum sealing lands (both sides): $2 \times 25.0\text{ mm} = 50.0\text{ mm}$
  - Margin: $4.9\text{ mm}$
  - Total tool base width: $W_{tool} \approx 80.0\text{ mm}$.
- Geometry reduction due to rectangular tool width in square chamber:
  $$D_{effective} = D_{chamber} - W_{tool} = 707.1 - 80.0 = 627.1\text{ mm}$$
- Subtracting oven corner wall clearances ($2 \times 25.0\text{ mm} = 50.0\text{ mm}$):
  $$L_{tool,diag} = 627.1 - 50.0 = 577.1\text{ mm}$$
- Subtracting vacuum tape ($30\text{ mm}$) and end trim allowances ($40\text{ mm}$):
  $$L_{boom,diag} = 577.1 - 70.0 = 507.1\text{ mm} \implies \mathbf{500.0\text{ mm}}$$
- Number of sections needed for $2.1\text{ m}$ deployable boom:
  $$N_{sections} = \left\lceil \frac{2100\text{ mm}}{500\text{ mm}} \right\rceil = \mathbf{5\text{ sections}}$$
- Number of sections needed for $3.0\text{ m}$ full CAD boom:
  $$N_{sections} = \left\lceil \frac{3000\text{ mm}}{500\text{ mm}} \right\rceil = \mathbf{6\text{ sections}}$$
