#!/usr/bin/env python3
"""
Bistability Script.py (Maintained script wrapper)
Lee & Fernandez (2018) bistability analysis for two-shelled composite booms.
Fixes upstream issues:
- Fixed default outer_counts=(2) int iteration crash to outer_counts=(2,).
- Clean JSON overwrite prevents cross-run geometry pollution.
- Integrated Classical Laminate Theory ABD solver for robust execution.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bistability import run_batch, print_summary

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(script_dir, "bistability_results.json")
    results = run_batch(outer_counts=(2,), inner_counts=(2, 3), out_file=out_json)
    print_summary(results)
    print(f"Results cleanly written to: {out_json}")
