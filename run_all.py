#!/usr/bin/env python3
"""
Svarog Composite Booms Analysis Suite (Unified CLI Entry Point)

Runs all composite boom engineering analyses:
1. Sizing Calculator (Flange geometry, coiling strains, microbuckling safety, spool packaging)
2. Second Moment of Area (Thin-shell area integrals, Ixx, Iyy, J, angle optimization sweep)
3. Bistability Analysis (Lee & Fernandez 2018 criterion for two-shelled bistable booms)

Usage:
  python run_all.py all             # Run full engineering suite
  python run_all.py sizing          # Run sizing & coiling safety analysis
  python run_all.py second-moment   # Run thin-shell section property integration
  python run_all.py bistability     # Run laminate bistability search
"""

import argparse
import os
import sys

# Add scripts directory to module path
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Composite Booms", "Scripts")
if os.path.isdir(SCRIPT_DIR) and SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "params.py")):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sizing import run_sizing_report, print_report as print_sizing_report
from second_moment import calculate_thin_shell_properties, sweep_angle, plot_profile, print_report as print_moment_report
from bistability import run_batch, print_summary as print_bistability_summary


def run_sizing_cmd(args):
    print("\n[1/3] Running Svarog Boom Sizing & Packaging Analysis...")
    report = run_sizing_report()
    print_sizing_report(report)
    return report


def run_second_moment_cmd(args):
    print("\n[2/3] Running Thin-Shell Second Moment of Area Analysis...")
    props = calculate_thin_shell_properties()
    print_moment_report(props)
    
    sweep = sweep_angle()
    print(f"Angle Optimization Sweep (Fixed Flattened Height):")
    print(f"  Max Ixx: {sweep['max_ixx']['val']*1e12:.1f} mm^4 at angle {sweep['max_ixx']['angle_deg']:.1f} deg (R={sweep['max_ixx']['radius']*1e3:.1f} mm)")
    print(f"  Max Iyy: {sweep['max_iyy']['val']*1e12:.1f} mm^4 at angle {sweep['max_iyy']['angle_deg']:.1f} deg (R={sweep['max_iyy']['radius']*1e3:.1f} mm)")
    
    out_img = plot_profile(props)
    print(f"  Cross-section profile plot saved: {out_img}")
    return props


def run_bistability_cmd(args):
    print("\n[3/3] Running Laminate Bistability Analysis...")
    out_file = os.path.join(SCRIPT_DIR, "bistability_results.json")
    # In quick mode, evaluate outer_count=2, inner_count=2
    inner_counts = (2,) if getattr(args, "quick", False) else (2, 3)
    results = run_batch(outer_counts=(2,), inner_counts=inner_counts, out_file=out_file)
    print_bistability_summary(results)
    print(f"  Bistable cases saved to: {out_file}")
    return results


def run_all_cmd(args):
    print("=" * 80)
    print("SVAROG COMPOSITE BOOMS: UNIFIED ENGINEERING ANALYSIS SUITE")
    print("=" * 80)
    run_sizing_cmd(args)
    run_second_moment_cmd(args)
    run_bistability_cmd(args)
    print("\nAll analyses finished successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Unified analysis suite for Svarog deployable composite booms."
    )
    subparsers = parser.add_subparsers(dest="command", help="Analysis module to execute")

    all_parser = subparsers.add_parser("all", help="Run all analyses in sequence")
    all_parser.add_argument("--quick", action="store_true", help="Run abbreviated bistability sweep")
    all_parser.set_defaults(func=run_all_cmd)

    sizing_parser = subparsers.add_parser("sizing", help="Run boom sizing and coiling failure checks")
    sizing_parser.set_defaults(func=run_sizing_cmd)

    moment_parser = subparsers.add_parser("second-moment", help="Run thin-shell second moment integration")
    moment_parser.set_defaults(func=run_second_moment_cmd)

    bistable_parser = subparsers.add_parser("bistability", help="Run laminate bistability sweep")
    bistable_parser.add_argument("--quick", action="store_true", help="Run abbreviated sweep")
    bistable_parser.set_defaults(func=run_bistability_cmd)

    args = parser.parse_args()
    if not args.command:
        # Default to running all
        run_all_cmd(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
