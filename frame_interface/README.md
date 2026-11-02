# Svarog Deployable Booms: Frame Interface Subsystem

## Overview
This subsystem defines the structural and mechanical interface between the 4-boom deployer cassette and the Svarog spacecraft chassis (1U reference structure and 4U payload module).

## Structural Heritage & Reference Model
- **Reference Model:** Uses the verified Atrium 1U reference frame (`cad/atrium_1u_reference.step`) and parametric geometry generator (`cad/frame_geometry.py`).
- **Material:** Structural Aluminium 6061-T6 (tensile yield strength $276\text{ MPa}$, ultimate strength $310\text{ MPa}$, density $2.70\text{ g/cm}^3$).
- **Frame Envelope:** $100.0 \times 100.0 \times 100.0\text{ mm}$ (1U baseline) scalable to $200.0 \times 200.0 \times 100.0\text{ mm}$ (4U payload volume).
- **Rail Geometry:** 4 L-angle corner rails with $8.5\text{ mm}$ leg width, $1.6\text{ mm}$ rail wall thickness, and $6.0 \times 6.0 \times 3.0\text{ mm}$ corner contact pads conforming to CubeSat Design Specifications (CDS).

## Mechanical & Electrical Interface Boundaries
1. **Cassette Structural Hardpoints:**
   - Cassette baseplate attaches directly to interior rail corner tapped bosses using M3 stainless steel fasteners.
   - Designed to react $20\text{g}$ longitudinal launch load and $5\text{g}$ lateral dynamic acceleration without structural deflection that could pinch the co-wound boom spool.
2. **Egress Cutouts:**
   - Four rectangular egress apertures ($35\text{ mm}$ width $\times 12\text{ mm}$ height) positioned symmetrically on the four transverse frame faces.
   - Apertures align with the deployer roller exit throats to provide non-contact clearance during high-speed boom extension.
3. **Electrical Bonding & Grounding:**
   - Conductive Alodine 1200 / MIL-DTL-5541 chemical conversion coating on aluminium interface faces.
   - Chassis bonding resistance $< 2.5\text{ m}\Omega$ to provide static discharge paths from the carbon composite booms (which accumulate space plasma charge) to central spacecraft bus ground.

## Tracking & Design Status
> [!IMPORTANT]
> **No Invented Geometry Policy:** The reference 1U frame CAD is included directly from the Imperial Svarog CAD workshop deliverables. The specific cassette mounting bracket hole pattern and pyrotechnic/burn-wire door release latches are not yet frozen and are tracked in the issue tracker without inventing arbitrary fastener locations.

- Tracking Issue: [Issue #5: Frame Interface: Mounting bracket hole pattern and egress hatch release mechanism](https://github.com/thomasvanpul/Project_Svarog/issues/5)
- Included CAD:
  - `cad/atrium_1u_reference.step`: Full 3D STEP geometry of the structural frame.
  - `cad/frame_geometry.py`: Parametric Fusion 360 script used to generate the reference geometry.
