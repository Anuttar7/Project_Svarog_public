#!/usr/bin/env python3
"""
Second_Moment_of_Area.py (Maintained script wrapper)
Calculates thin-shell second moments of area and sweeps opening angles.
Fixes upstream issues:
- Replaced solid filled-area integration with thin-walled shell formulation (0.2 mm wall).
- Removed dependency on external LaTeX system (plt.rcParams['text.usetex'] = False).
- Saves profile plot to file without GUI blocking.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from second_moment import calculate_thin_shell_properties, sweep_angle, plot_profile, print_report

if __name__ == "__main__":
    props = calculate_thin_shell_properties()
    print_report(props)
    
    print("\nRunning opening angle sweep (5 to 90 deg)...")
    sweep = sweep_angle()
    print(f"Thin-shell Maximum Ixx: {sweep['max_ixx']['val']*1e12:.1f} mm^4 at angle {sweep['max_ixx']['angle_deg']:.1f} deg (R={sweep['max_ixx']['radius']*1e3:.1f} mm)")
    print(f"Thin-shell Maximum Iyy: {sweep['max_iyy']['val']*1e12:.1f} mm^4 at angle {sweep['max_iyy']['angle_deg']:.1f} deg (R={sweep['max_iyy']['radius']*1e3:.1f} mm)")
    
    out_img = plot_profile(props)
    print(f"Cross-section plot saved to: {out_img}")
