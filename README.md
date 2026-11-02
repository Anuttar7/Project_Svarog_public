# Project Svarog: Deployable Composite Booms

Deployable composite boom analysis, sizing, mechanism design, tooling, and finite element modeling for Project Svarog (REXUS/BEXUS cycle 17 solar sail subsystem).

This repository is Thomas's fork of Aditya Shankar's upstream repository (`adityash-ankar/Project_Svarog`). It refactors the engineering codebase with validated thin-shell mechanics, corrected sizing formulas, unit tests, single entry point CLI, pruned privacy/copyright assets, and fully documented subsystems for deployment, spool, frame interface, and high-temperature mould tooling.

---

## Repository Map

| Path | Purpose / Description | Status / Implementation |
|---|---|---|
| `run_all.py` | Unified entry point CLI for all analytical calculations | **Active** (supports `all`, `sizing`, `second-moment`, `bistability`) |
| `references/references.md` | Complete academic literature index with citations and DOIs | **Active** (replaces raw publisher PDFs for copyright compliance) |
| `REDACTIONS.md` | Log of pruned personal data (proposal docx) and duplicate files | **Documentation** |
| `tests/` | Pytest test suite covering sizing, thin-shell moments, bistability, and CLI | **17/17 passing** |
| `deployment_mechanism/` | Architecture, sizing, and anti-blooming constraints for 4-boom deployer cassette | **Subsystem Documentation & Specs** (Tracked in Issue #3) |
| `spool/` | Packaging calculations, 70 mm hub sizing ($\text{SF}=1.54$), and inter-boom slip-sheets | **Subsystem Calculations & Specs** (Tracked in Issue #4) |
| `frame_interface/` | Mechanical chassis interface, transverse egress cutouts, and reference 1U CAD | **Active Reference CAD & Specs** (Tracked in Issue #5) |
| `boom_mould/` | 500 mm oven tooling, thermal mismatch analysis, material spec, and cut list; `v4/` is the draft closed three-piece autoclave tool (2 Nov 2026) | **Tooling Engineering Design** (Tracked in Issue #6) |
| `Composite Booms/Scripts/params.py` | Single source of truth for CAD geometry ($R=15.1$ mm, $90^\circ$, $w=10$ mm) and material properties | **New** |
| `Composite Booms/Scripts/sizing.py` | Core sizing module with corrected stress, packaging diameter, and microbuckling equations | **Refactored** |
| `Composite Booms/Scripts/Sizing Script.py` | Legacy wrapper running the corrected sizing report | **Maintained** |
| `Composite Booms/Scripts/second_moment.py` | Thin-shell integration for area, centroid, $I_{xx}$, $I_{yy}$, $J$, and angle optimization sweep | **Refactored** |
| `Composite Booms/Scripts/Second_Moment_of_Area.py` | Legacy wrapper for thin-shell second moment calculations (no LaTeX requirement) | **Maintained** |
| `Composite Booms/Scripts/bistability.py` | Lee & Fernandez (2018) bistability analysis with Classical Laminate Theory ABD solver | **Refactored** (fixed int tuple bug & dirty append) |
| `Composite Booms/Scripts/Bistability Script.py` | Legacy wrapper for bistability search | **Maintained** |
| `Composite Booms/Sims+CAD/Composite Boom.step` | 200 mm TRAC section CAD geometry ($R_{mid}=15.1$ mm, $\theta=90^\circ$, $w=10$ mm, $t=0.2$ mm) | **Baseline CAD** |
| `Composite Booms/Sims+CAD/Composite Boom Full Length.step` | 3000 mm full-length boom solid model | **CAD** |
| `Composite Booms/Sims+CAD/ACP Setup.wbpj` | Ansys Workbench ACP layup & structural simulation setup | **Issue logged** (requires `CEFILTER,OFF` or scoped remote point) |
| `Composite Booms/Sims+CAD/Composite Setup - Failsafe.wbpj` | Ansys Workbench nonlinear flange flattening simulation | **Issue logged** (requires contact stabilization for element 16000 distortion) |

---

## Key Mathematical Corrections & Before/After Numbers

| Metric / Parameter | Upstream (`adityash-ankar`) | This Fork (`thomasvanpul`) | Root Cause / Physics Fix |
|---|---|---|---|
| **Peak Coiling Stress ($\sigma_{max}$)** | **7,168 MPa** (7.2 GPa!) | **284.0 MPa** | Fixed factor of 2 in bending strain ($\sigma = E t / (2 R)$) and used woven modulus (35.5 GPa) instead of 128 GPa UD. |
| **Safety Factor (Coiling)** | **0.10** (FAIL) | **1.54** (PASS) | True laminate mechanics against microbuckling allowable ($\sigma_{c} = 437\text{ MPa}$). |
| **Recommended Hub Diameter** | **180.0 mm** | **70.0 mm** | Sizing analysis proves 70 mm spool provides robust 54% margin against fiber microbuckling. |
| **Packaged Coil Diameter** | **328.5 mm** (33 cm!) | **77.6 mm** (< 8 cm) | Incremented spool diameter by flattened tape thickness ($2t = 0.4\text{ mm}$ per wrap) rather than full flattened height ($2 \times 20\text{ mm}$). |
| **Flange Flattened Height** | **20.0 mm** (chord) | **33.7 mm** (arc+web) | Upstream treated flattened width as circular chord ($2R\sin(\theta/2)$). True flattened geometry is mid-surface arc length ($R\theta + w$). |
| **Thin-Shell Second Moment ($I_{xx}$)** | **77,312 mm$^4$** | **839.1 mm$^4$** | Upstream integrated a solid planar area between curves; this fork integrates the 0.2 mm thin shell wall. |
| **Thin-Shell Second Moment ($I_{yy}$)** | **4,910 mm$^4$** | **490.5 mm$^4$** | Integrated thin-walled circular arc shell along symmetry axis. |
| **Bending Stiffness ($EI_{xx}$)** | **9,895 N m$^2$** | **29.8 N m$^2$** | Corrected thin-shell moment restores physically realistic cantilever stiffness. |
| **Bistability Script Run** | Crashed (`TypeError`) | **Passed (0 errors)** | Fixed integer-to-tuple syntax (`outer_counts=(2,)`) and clean JSON overwrite. |

---

## Subsystems Added in Round 2

1. **`deployment_mechanism/`:**
   - Architecture and timing (20-45 s deploy, 5 s dwell, 30-60 s retract; 40 s nominal).
   - Motor drive sizing: uncoiling bending resistance $M_{bend} \approx 0.85\text{ N}\cdot\text{m}$ per boom ($\approx 3.4\text{ N}\cdot\text{m}$ for 4 booms).
   - BEXUS 34 flight lessons: continuous anti-blooming roller constraints and flattening transition throats.
   - Status: Tracked in GitHub Issue #3.

2. **`spool/`:**
   - 70 mm diameter hub core ($R_{hub} = 35\text{ mm}$), $\text{SF} = 1.54$ microbuckling margin.
   - Radial buildup for 4 co-wound booms ($< 88\text{ mm}$ stowed diameter).
   - Inter-boom low-friction slip sheets (PTFE/Kapton film) preventing binding.
   - Status: Tracked in GitHub Issue #4.

3. **`frame_interface/`:**
   - 1U reference CAD (`cad/atrium_1u_reference.step`) and parametric generator (`cad/frame_geometry.py`).
   - Structural boundary conditions for 20g axial launch acceleration and 5g lateral loads.
   - 4x transverse egress window clearances ($35 \times 12\text{ mm}$) and electrical bonding.
   - Status: Tracked in GitHub Issue #5.

4. **`boom_mould/`:**
   - Sized for Imperial Composites Laboratory $500 \times 500\text{ mm}$ oven (horizontal orientation).
   - Section length analysis: maximum straight section length $380-400\text{ mm}$ (6 sections for 2.1 m boom); diagonal section length $500\text{ mm}$ (5 sections for 2.1 m boom).
   - Thermal mismatch: differential expansion between aluminium face ($23.4\text{ ppm/}^\circ\text{C}$) and wood substrate ($5.0\text{ ppm/}^\circ\text{C}$) reaches $1.47\text{ mm}$ at $180^\circ\text{C}$ ($1.66\text{ mm}$ at $200^\circ\text{C}$). Floating slotted fasteners eliminate bimetallic warping.
   - Material spec: Densified wood (Permali/Jabroc) or epoxy tooling board (Alchemie Lab 1000) selected; standard MDF strictly rejected due to binder thermal breakdown.
   - Status: Tracked in GitHub Issue #6.

---

## How to Run

### Requirements
- Python 3.8+
- Packages: `numpy`, `scipy`, `matplotlib`, `pytest` (optional: `composipy`, `plotly`)

### 1. Run Unified Suite
To run all analyses from the repository root:
```bash
python run_all.py all
```
Or with an abbreviated bistability sweep:
```bash
python run_all.py all --quick
```

### 2. Run Individual Modules
```bash
python run_all.py sizing         # Boom geometry, strains, microbuckling SF, packaging
python run_all.py second-moment  # Thin-shell Ixx, Iyy, J, and angle sweep
python run_all.py bistability    # Laminate bistability search
```

### 3. Run Unit Tests
```bash
pytest -v
```

---

## GitHub Issues & Unfinished Subsystems
Per repository policy, no fictional geometry has been invented for unreleased parts:
- **Issue #1:** ACP Setup: Solve failed on 42,026-term constraint equation (`CEFILTER,OFF`)
- **Issue #2:** Composite Setup - Failsafe: Nonlinear solve aborted on Element 16000 excessive distortion
- **Issue #3:** Deployment Mechanism: Detailed CAD, motor sizing, and exit guide kinematics
- **Issue #4:** Spool: Flange retention CAD, shaft coupling, and inter-boom slip-sheet routing
- **Issue #5:** Frame Interface: Mounting bracket hole pattern and egress hatch release mechanism
- **Issue #6:** Boom Mould: 500 mm oven tooling, differential thermal expansion relief, and vacuum bag edge seals
