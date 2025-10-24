#!/usr/bin/env python3
"""
Run All CBC Component Analyses
===============================
Batch runner that executes comprehensive ECL analysis for all CBC components.

This script runs cbc_component_analyzer.py for each CBC component:
- Hemoglobin
- Methemoglobin
- Erythrocytes
- Hematocrit
- Leukocytes
- Platelets
- MCV
- MCH
- MCHC
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# CBC components configuration
CBC_COMPONENTS = {
    'Hemoglobin': {
        'primary_loinc': '59260-0',
        'name': 'hemoglobin',
        'exclude_specimens': []
    },
    'Methemoglobin': {
        'primary_loinc': '2614-6',
        'name': 'methemoglobin',
        'exclude_specimens': []
    },
    'Erythrocytes': {
        'primary_loinc': '26453-1',
        'name': 'erythrocytes',
        'exclude_specimens': []
    },
    'Hematocrit': {
        'primary_loinc': '20570-8',
        'name': 'hematocrit',
        'exclude_specimens': []
    },
    'Leukocytes': {
        'primary_loinc': '26464-8',
        'name': 'leukocytes',
        'exclude_specimens': []
    },
    'Platelets': {
        'primary_loinc': '26515-7',
        'name': 'platelets',
        'exclude_specimens': ['119361006']  # Exclude plasma for platelets
    },
    'MCV': {
        'primary_loinc': '30428-7',
        'name': 'mcv',
        'exclude_specimens': []
    },
    'MCH': {
        'primary_loinc': '28539-5',
        'name': 'mch',
        'exclude_specimens': []
    },
    'MCHC': {
        'primary_loinc': '28540-3',
        'name': 'mchc',
        'exclude_specimens': []
    }
}

def run_analysis(component_display_name, config):
    """
    Run CBC component analyzer for a single component.
    """
    print("\n" + "=" * 80)
    print(f"ANALYZING: {component_display_name}")
    print("=" * 80)
    print(f"Primary LOINC: {config['primary_loinc']}")
    print(f"Component name: {config['name']}")
    if config['exclude_specimens']:
        print(f"Exclude specimens: {', '.join(config['exclude_specimens'])}")
    print()

    # Build command
    script_path = Path(__file__).parent / 'cbc_component_analyzer.py'
    cmd = [
        sys.executable,
        str(script_path),
        config['primary_loinc'],
        config['name']
    ]

    if config['exclude_specimens']:
        cmd.extend(['--exclude-specimens', ','.join(config['exclude_specimens'])])

    # Run the analysis
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Analysis failed for {component_display_name}")
        print(f"Exit code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    print("=" * 80)
    print("CBC COMPONENTS - BATCH ANALYSIS RUNNER")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTotal components to analyze: {len(CBC_COMPONENTS)}")
    print()

    results = {}

    for component_name, config in CBC_COMPONENTS.items():
        success = run_analysis(component_name, config)
        results[component_name] = 'SUCCESS' if success else 'FAILED'

    # Print summary
    print("\n" + "=" * 80)
    print("BATCH ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nResults Summary:")
    print("-" * 80)

    for component_name, status in results.items():
        status_icon = "[OK]" if status == 'SUCCESS' else "[FAIL]"
        print(f"  {status_icon} {component_name:20} {status}")

    # Exit with error if any failed
    if any(status == 'FAILED' for status in results.values()):
        print("\nWARNING: Some analyses failed!")
        sys.exit(1)
    else:
        print("\nAll analyses completed successfully!")

if __name__ == '__main__':
    main()
