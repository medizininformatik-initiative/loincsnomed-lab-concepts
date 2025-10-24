#!/usr/bin/env python3
"""
Blood Work Analysis Runner
===========================
Runs comprehensive ECL analysis for all blood work lab parameters.

This script executes cbc_component_analyzer.py for:

CBC Parameters:
- Erythrocytes (RBC)
- Hemoglobin
- Hematocrit
- Leukocytes (WBC)
- Platelets
- MCV (Mean Corpuscular Volume)
- MCH (Mean Corpuscular Hemoglobin)
- MCHC (Mean Corpuscular Hemoglobin Concentration)

Additional Lab Parameters:
- Creatinine in Blood
- HbA1c (Hemoglobin A1c)
- Methemoglobin
- Potassium (Kalium) in Blood
- Nitrite in Urine

Usage:
    python run_blood_work_analysis.py [--only <parameter_name>]

Examples:
    python run_blood_work_analysis.py                    # Run all analyses
    python run_blood_work_analysis.py --only creatinine  # Run only creatinine
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import argparse

# Lab parameters configuration
# Format: (primary_loinc, output_name, [specimen_exclusions])
LAB_PARAMETERS = {
    # CBC Parameters - run all ECL variations first, refine later
    'erythrocytes': ('26453-1', 'erythrocytes', []),
    'hemoglobin': ('718-7', 'hemoglobin', []),
    'hematocrit': ('4544-3', 'hematocrit', []),
    'leukocytes': ('6690-2', 'leukocytes', []),
    'platelets': ('26515-7', 'platelets', []),
    'mcv': ('787-2', 'mcv', []),
    'mch': ('785-6', 'mch', []),
    'mchc': ('786-4', 'mchc', []),

    # Additional Lab Parameters - run all ECL variations first, refine later
    'creatinine': ('14682-9', 'creatinine_blood', []),
    'hba1c': ('4548-4', 'hba1c', []),
    'methemoglobin': ('2614-6', 'methemoglobin', []),
    'potassium': ('6298-4', 'potassium_blood', []),
    'nitrite': ('5802-4', 'nitrite_urine', []),
}

def run_analysis(param_key, primary_loinc, output_name, exclude_specimens):
    """
    Run cbc_component_analyzer.py for a single parameter.

    Args:
        param_key: Short name for logging (e.g., 'erythrocytes')
        primary_loinc: Primary LOINC code
        output_name: Output directory name
        exclude_specimens: List of SNOMED specimen IDs to exclude

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "=" * 80)
    print(f"ANALYZING: {param_key.upper()} ({primary_loinc})")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    cmd = [
        'python',
        'analysis/cbc_component_analyzer.py',
        primary_loinc,
        output_name
    ]

    if exclude_specimens:
        cmd.extend(['--exclude-specimens', ','.join(exclude_specimens)])

    print(f"Command: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"\n[OK] Completed: {param_key}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Failed: {param_key}")
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Run blood work ECL analysis for all lab parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--only',
                        help='Run analysis for only one parameter',
                        choices=list(LAB_PARAMETERS.keys()))

    args = parser.parse_args()

    print("=" * 80)
    print("BLOOD WORK ANALYSIS RUNNER")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Determine which parameters to run
    if args.only:
        parameters_to_run = {args.only: LAB_PARAMETERS[args.only]}
        print(f"\nRunning analysis for: {args.only}")
    else:
        parameters_to_run = LAB_PARAMETERS
        print(f"\nRunning analysis for all {len(LAB_PARAMETERS)} parameters")

    print(f"\nParameters:")
    for param_key, (loinc, name, exclusions) in parameters_to_run.items():
        excl_desc = f" (excluding {len(exclusions)} specimen types)" if exclusions else ""
        print(f"  - {param_key}: {loinc}{excl_desc}")

    # Run analyses
    results = {}

    for param_key, (primary_loinc, output_name, exclude_specimens) in parameters_to_run.items():
        success = run_analysis(param_key, primary_loinc, output_name, exclude_specimens)
        results[param_key] = 'SUCCESS' if success else 'FAILED'

    # Summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults:")

    for param_key, status in results.items():
        status_symbol = "[OK]" if status == 'SUCCESS' else "[!!]"
        print(f"  {status_symbol} {param_key}: {status}")

    success_count = sum(1 for s in results.values() if s == 'SUCCESS')
    total_count = len(results)

    print(f"\nTotal: {success_count}/{total_count} successful")

    if success_count == total_count:
        print("\n[OK] All analyses completed successfully!")
        return 0
    else:
        print("\n[!!] Some analyses failed. Check logs above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
