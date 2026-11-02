# Svarog Deployable Booms: Spool Subsystem

## Overview
The spool subsystem provides the central cylindrical hub and co-winding storage core for all four composite TRAC booms in the stowed pre-deployment state.

## Core Sizing & Packaging Physics
- **Hub Sizing Verification:**
  - Upstream code bug previously suggested a massive $180\text{ mm}$ minimum hub diameter due to erroneous stress formulas and using 128 GPa UD modulus.
  - Svarog fork analysis established that a **$70.0\text{ mm}$ diameter hub ($R_{hub} = 35.0\text{ mm}$)** is structurally safe, delivering:
    - Peak coiling bending strain: $\epsilon = \frac{t}{2 R_{hub}} = \frac{0.2\times 10^{-3}}{2 \times 0.035} = 0.286\%$
    - Peak combined transition coiling stress: $\sigma_{max} = 284.0\text{ MPa}$
    - Microbuckling allowable (Budiansky-Argon criterion): $\sigma_c = 437.0\text{ MPa}$
    - Safety Factor: **$\text{SF} = 1.54$ (PASS, robust margin $\ge 1.5$)**
- **Packaged Radial Buildup:**
  - Flattened tape wall thickness per boom: $2t = 0.4\text{ mm}$ ($2 \times 0.2\text{ mm}$ bonded flanges).
  - Flattened tape width: $s + w = 33.7\text{ mm}$ (arc length $23.7\text{ mm} + 10.0\text{ mm}$ web).
  - For four co-wound booms ($2.1\text{ m}$ length):
    - Circumference of 70 mm hub: $C = \pi \times 70 \approx 220\text{ mm}$.
    - Number of wraps per boom: $N = \frac{2100}{220} \approx 9.5\text{ wraps}$.
    - Total radial growth for 4 interleaved booms: $\Delta R \approx 9.5 \times (4 \times 0.2\text{ mm}) \approx 7.6\text{ mm}$ to $9.0\text{ mm}$ with slip-sheets.
    - Outer packaged diameter: **$\approx 85\text{ to }88\text{ mm}$**, leaving over $110\text{ mm}$ of radial margin inside the $200\text{ mm}$ payload bay.

## Subsystem Architecture
1. **Central Spool Core:**
   - Machined 6061-T6 aluminium cylinder, outer diameter $70.0\text{ mm}$, internal bore for drive shaft and bearing integration.
   - Anchor slots for securing the root clamp of each of the four composite boom webs.
2. **Side Retention Flanges:**
   - Axial retaining discs (outer diameter $95.0\text{ mm}$, thickness $2.0\text{ mm}$) to constrain the coiled tapes axially against lateral launch shock and vibration.
3. **Inter-Boom Slip Sheets (Separator Films):**
   - Interleaved $0.05\text{ mm}$ PTFE or fluoropolymer film co-wound between boom layers.
   - Prevents high-friction carbon-to-carbon abrasion, binding, and static friction lock during low-temperature deployment.
4. **Launch Inertial Reaction:**
   - Total mass of 4 coiled booms ($4 \times 41.2\text{ g}$): $M_{booms} \approx 165\text{ g}$.
   - Under $20\text{g}$ axial launch acceleration, inertial shear load on the spool flanges is $F_{launch} = 0.165\text{ kg} \times 20 \times 9.81\text{ m/s}^2 \approx 32.4\text{ N}$.
   - Flange stiffness and root fastening easily support this load with safety factors exceeding 20.

## Tracking & Design Status
> [!IMPORTANT]
> **No Invented Geometry Policy:** Specific bolt circles, bearing part numbers, and root anchor geometry have not yet been approved by the sub-team. No CAD files with unverified dimensions are added.

- Tracking Issue: [Issue #4: Spool: Flange retention CAD, shaft coupling, and inter-boom slip-sheet routing](https://github.com/thomasvanpul/Project_Svarog/issues/4)
- Open engineering questions: Root attachment clamp method (bonded doubler vs flush clamping screws) and slip-sheet rewind tensioning.
