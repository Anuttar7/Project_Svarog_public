#!/usr/bin/env python3
"""
TRAC BOOM DESIGN CALCULATOR
Maintained script: wraps modular sizing calculations with original CLI presentation.
Fixed upstream bugs:
- Coiling stress factor of 2 corrected (sigma = E*t/(2*R))
- Spool outer diameter packaging bug corrected (adds 2*t per wrap, not 2*flattened_height)
- Axial modulus aligned with woven laminate [0/45] (35.5 GPa) with UD comparison
- Single source of truth parameters loaded from params.py
"""

import sys
import os

# Add script directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sizing import run_sizing_report, print_report

if __name__ == "__main__":
    report = run_sizing_report()
    print_report(report)
