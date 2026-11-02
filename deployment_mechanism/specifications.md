# Deployment Mechanism Specifications & Requirements

## 1. Functional Requirements
- **FR-01 (Deployment):** Deploy four orthogonal composite TRAC booms simultaneously to a length of $2.1\text{ m}$ (minimum $1.0\text{ m}$) within $40\pm 5\text{ seconds}$.
- **FR-02 (Observation Dwell):** Maintain full extension for a minimum scientific observation duration of $5\text{ seconds}$ up to mission-determined dwell duration.
- **FR-03 (Retraction):** Fully retract all four booms into the stowed spool configuration within $45\pm 15\text{ seconds}$ before atmospheric re-entry.
- **FR-04 (Position Feedback):** Measure deployed boom extension length via redundant Hall effect encoder channels with an axial precision better than $\pm 5\text{ mm}$.
- **FR-05 (Blooming Suppression):** Prevent circumferential radial blooming of coiled laminate layers under ascent vibration ($20\text{g}$ axial load) and despin deceleration ($3-4\text{ Hz}$ to $0.08\text{ Hz}$).

## 2. Environmental & Launch Loads
- **Axial Launch Acceleration:** $20\text{g}$ peak along sounding rocket longitudinal axis (REXUS User Manual §5.10.1).
- **Radial/Lateral Acceleration:** $5\text{g}$ static equivalent.
- **Spin / De-spin Dynamics:** Spin rate $3\text{ to }4\text{ Hz}$ during powered ascent; de-spun via yo-yo mechanism to $0.08\text{ Hz}$ prior to deployment.
- **Re-entry Shock:** $20\text{g}$ peak deceleration in arbitrary orientation; landing velocity approximately $8\text{ m/s}$ (REXUS User Manual §5.10.2).
- **Vibration Spectrum:** NSRHB qualification acceptance vibration envelope (Table 10-2).

## 3. Physical & Interface Budgets
- **Volume Envelope:** $200\text{ mm} \times 200\text{ mm} \times 50\text{ mm}$ (allocated payload cassette module).
- **Mass Allocation:** Target $< 1.20\text{ kg}$ total for cassette (including 4 booms $\approx 164\text{ g}$, motor $\approx 250\text{ g}$, spool core, guide rollers, and structure).
- **Peak Electrical Power:** $12\text{ V}$ bus, maximum $2.5\text{ A}$ current draw ($30\text{ W}$ peak electrical power during high-torque startup).

## 4. Mechanical Interface Requirements
- **Interface to Structure:** Bolted interface to 1U/4U structural frame using M3 stainless steel fasteners with prevailing torque locknuts.
- **Boom Exit Geometry:** Four rectangular egress ports ($35\text{ mm} \times 12\text{ mm}$) centered on the four transverse faces.
- **Egress Guides:** Dual-roller throat (entrance $R_{roll} = 8\text{ mm}$, exit radius $R_{exit} = 15.1\text{ mm}$) to guide transition from flat coiling tape to $90^\circ$ curved TRAC shell.
