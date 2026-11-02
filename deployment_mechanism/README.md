# Svarog Deployable Booms: Deployment Mechanism Subsystem

## Overview
This subsystem houses the central deployment drive cassette for the four orthogonal composite TRAC deployable booms of Project Svarog, sized for a REXUS sounding rocket payload module.

## Heritage & Lessons Learned (BEXUS 34 & 36)
- **Heritage:** Inherited from the BEXUS 36 deployer architecture (four deployable booms on a single central spool, spring-loaded anti-blooming clasps, rolling exit guides, motor with Hall effect sensor for extension measurement, four spring-loaded egress hatches).
- **Failure Mode & Flight Lesson:** In the BEXUS 34 flight campaign, spring steel booms experienced uncontrolled radial expansion ("blooming") inside the spool chamber during deceleration/vibration. The blooming booms caught on the inner edges of the door cutouts, causing deployment to jam at ~0.5 m of the 2.0 m target length.
- **Subsystem Mandate:** Uncontrolled blooming must be prevented by continuous circumferential constraint (spring-loaded anti-blooming clasps/tangent guide rollers) and rolling constraint guides at each of the four exit ports.

## Subsystem Architecture
1. **Central Spool Cassette:**
   - Single central hub driving all four booms simultaneously.
   - Fits within an allocated envelope of approximately $200 \times 200 \times 50\text{ mm}$.
2. **Drive Motor & Transmission:**
   - Target deployment duration: 20 to 45 seconds (nominal 40 s).
   - Target retraction duration: 30 to 60 seconds.
   - Peak uncoiling bending moment resistance:
     $$M_{bend} \approx \frac{E_{xx} \cdot I_{xx}}{R_{hub}} = \frac{35.5\text{ GPa} \times 839.1\text{ mm}^4}{35\text{ mm}} \approx 0.851\text{ N}\cdot\text{m per boom}$$
     Total steady-state resistive torque for 4 booms: $\approx 3.4\text{ N}\cdot\text{m}$.
   - Brushless DC motor with planetary reduction gearbox (ratio $\approx 150:1$) providing required torque margin ($\ge 1.5$).
   - Magnetic Hall effect quadrature encoder on motor shaft to measure deployed length to $\pm 1\text{ mm}$ accuracy.
3. **Anti-Blooming Clasps & Roller Guides:**
   - Four sprung follower arms with low-friction PEEK/PTFE rollers pressing radially inward on the outer coiled layer.
   - Transition rollers positioned at each exit throat to flatten the curved $90^\circ$ circular flanges into a planar tape before exiting through the frame boundary.
4. **Egress Hatch Assemblies:**
   - Four spring-loaded outer doors sealed during launch to protect internal mechanism from ascent aero-thermal and acoustic loads.
   - Microswitch deployment indicators confirming hatch release and initial boom emergence.

## Tracking & Design Status
> [!IMPORTANT]
> **No Invented Geometry Policy:** Detailed CAD models, motor mounting brackets, and roller hinge links have not yet been finalised by the mechanical sub-team. Per repository design standards, no fictional geometry has been invented.

- Tracking Issue: [Issue #3: Deployment Mechanism: Detailed CAD, motor sizing, and exit guide kinematics](https://github.com/thomasvanpul/Project_Svarog/issues/3)
- Open engineering questions: Drive motor part number, gearbox back-drive braking torque, and hatch burn-wire release release timing.
