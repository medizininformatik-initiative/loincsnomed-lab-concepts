#!/usr/bin/env python3
"""
Create Singular Concept Comparison Table
=========================================
Generates a detailed comparison table for a SINGLE primary LOINC concept,
showing all secondary LOINC codes from Interpolar and their presence across
different ECL approaches.

This is focused on reviewing one concept at a time (e.g., hemoglobin, leukocytes)
rather than all concepts together.

Usage:
    python create_singular_concept_table.py <PRIMARY_LOINC_CODE>

Example:
    python create_singular_concept_table.py 59260-0

Output:
    - output/singular_concepts/<primary_code>/detailed_comparison.csv
    - output/singular_concepts/<primary_code>/summary.json
"""

import pandas as pd
import json
import os
import sys
import asyncio
from pathlib import Path
from collections import defaultdict

# Add scripts to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from loinc_display_fetcher import fetch_displays_async

# Configuration
INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
OUTPUT_BASE_DIR = PROJECT_ROOT / 'output' / 'singular_concepts'

# ECL experiment paths
EXPERIMENTS = {
    'ecl_descendants_baseline': PROJECT_ROOT / 'output' / 'ecl_descendants_baseline' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component': PROJECT_ROOT / 'output' / 'ecl_fixed_component' / 'comparison_interpolar_vs_ecl.json',
    'ecl_component_descendants': PROJECT_ROOT / 'output' / 'ecl_component_descendants' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component_property': PROJECT_ROOT / 'output' / 'ecl_fixed_component_property' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component_system': PROJECT_ROOT / 'output' / 'ecl_fixed_component_system' / 'comparison_interpolar_vs_ecl.json',
}

def load_interpolar_data(primary_loinc):
    """Load Interpolar data for a specific primary LOINC code."""
    print(f"\n[1/4] Loading Interpolar data for {primary_loinc}...")

    df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)

    # Filter for this primary code
    df_primary = df[df['LOINC_PRIMARY'] == primary_loinc].copy()

    if len(df_primary) == 0:
        print(f"  ERROR: No data found for primary LOINC {primary_loinc}")
        return None

    # Extract primary concept info
    primary_name = df_primary.iloc[0]['GERMAN_NAME_LOINC_PRIMARY']

    # Extract secondary codes with comparability levels
    secondary_codes = {}
    for _, row in df_primary.iterrows():
        loinc = row['LOINC']
        comparability = row['COMPARABILITY_TO_LOINC_PRIMARY']

        if pd.notna(loinc) and pd.notna(comparability):
            secondary_codes[loinc] = comparability

    print(f"  [OK] Primary: {primary_loinc} - {primary_name}")
    print(f"  [OK] Found {len(secondary_codes)} secondary LOINC codes")

    return {
        'primary_loinc': primary_loinc,
        'primary_name': primary_name,
        'secondary_codes': secondary_codes
    }

def load_ecl_experiment_data(primary_loinc):
    """Load ECL experiment results for this primary LOINC."""
    print(f"\n[2/4] Loading ECL experiment results for {primary_loinc}...")

    experiment_data = {}

    for exp_name, path in EXPERIMENTS.items():
        if not path.exists():
            print(f"  [SKIP] {exp_name}: file not found")
            experiment_data[exp_name] = {'ecl_codes': []}
            continue

        with open(path, 'r', encoding='utf-8') as f:
            results = json.load(f)

        # Find this primary code's results
        primary_result = None
        for result in results:
            if result.get('primary_loinc') == primary_loinc:
                primary_result = result
                break

        if primary_result:
            ecl_codes = set(primary_result.get('ecl_codes', []))
            experiment_data[exp_name] = {
                'ecl_codes': ecl_codes,
                'ecl_count': len(ecl_codes)
            }
            print(f"  [OK] {exp_name}: {len(ecl_codes)} codes")
        else:
            print(f"  [SKIP] {exp_name}: primary code not found in results")
            experiment_data[exp_name] = {'ecl_codes': set()}

    return experiment_data

def create_comparison_table(interpolar_data, experiment_data):
    """Create detailed comparison table for this concept."""
    print(f"\n[3/4] Building comparison table...")

    primary_loinc = interpolar_data['primary_loinc']
    secondary_codes = interpolar_data['secondary_codes']

    # Collect all unique LOINC codes (from Interpolar + all ECL experiments)
    all_loinc_codes = set(secondary_codes.keys())
    all_loinc_codes.add(primary_loinc)

    for exp_name, exp_data in experiment_data.items():
        all_loinc_codes.update(exp_data['ecl_codes'])

    print(f"  Found {len(all_loinc_codes)} unique LOINC codes total")

    # Fetch LOINC display names
    print(f"  Fetching display names...")
    loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False))

    # Build table rows
    rows = []
    for loinc_code in sorted(all_loinc_codes):
        row = {
            'LOINC_Code': loinc_code,
            'LOINC_Display': loinc_displays.get(loinc_code, ''),
            'Is_Primary': 'Yes' if loinc_code == primary_loinc else '',
            'Interpolar_Comparability': secondary_codes.get(loinc_code, ''),
            'In_Interpolar': 'Yes' if loinc_code in secondary_codes or loinc_code == primary_loinc else '',
        }

        # Add columns for each ECL approach
        for exp_name in EXPERIMENTS.keys():
            ecl_codes = experiment_data.get(exp_name, {}).get('ecl_codes', set())
            row[f'{exp_name}_Present'] = 'Yes' if loinc_code in ecl_codes else ''

        rows.append(row)

    df = pd.DataFrame(rows)

    print(f"  [OK] Created table with {len(df)} rows, {len(df.columns)} columns")

    return df

def create_summary(interpolar_data, experiment_data, df_comparison):
    """Create summary statistics for this concept."""
    print(f"\n[4/4] Creating summary...")

    primary_loinc = interpolar_data['primary_loinc']
    primary_name = interpolar_data['primary_name']
    secondary_codes = interpolar_data['secondary_codes']

    # Count Interpolar codes
    interpolar_count = len(secondary_codes) + 1  # +1 for primary

    # Summary for each experiment
    experiment_summaries = {}
    for exp_name, exp_data in experiment_data.items():
        ecl_codes = exp_data['ecl_codes']

        # Calculate overlap with Interpolar
        interpolar_set = set(secondary_codes.keys())
        interpolar_set.add(primary_loinc)

        overlap = interpolar_set & ecl_codes

        experiment_summaries[exp_name] = {
            'ecl_count': len(ecl_codes),
            'overlap_count': len(overlap),
            'ecl_only_count': len(ecl_codes - interpolar_set),
            'interpolar_only_count': len(interpolar_set - ecl_codes),
            'overlap_codes': sorted(list(overlap)),
            'ecl_only_codes': sorted(list(ecl_codes - interpolar_set)),
            'interpolar_only_codes': sorted(list(interpolar_set - ecl_codes))
        }

    # Convert pandas int64 to regular int for JSON serialization
    comparability_counts = pd.Series(secondary_codes.values()).value_counts()
    comparability_breakdown = {str(k): int(v) for k, v in comparability_counts.items()}

    summary = {
        'primary_loinc': primary_loinc,
        'primary_name': primary_name,
        'interpolar_count': interpolar_count,
        'interpolar_codes': sorted(list(secondary_codes.keys()) + [primary_loinc]),
        'comparability_breakdown': comparability_breakdown,
        'experiments': experiment_summaries
    }

    print(f"  [OK] Summary created")
    print(f"\n  Interpolar: {interpolar_count} codes")
    for exp_name, exp_summary in experiment_summaries.items():
        print(f"  {exp_name}: {exp_summary['ecl_count']} codes ({exp_summary['overlap_count']} overlap)")

    return summary

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_singular_concept_table.py <PRIMARY_LOINC_CODE>")
        print("\nExample: python create_singular_concept_table.py 59260-0")
        sys.exit(1)

    primary_loinc = sys.argv[1].strip()

    print("=" * 80)
    print(f"SINGULAR CONCEPT COMPARISON TABLE")
    print(f"Primary LOINC: {primary_loinc}")
    print("=" * 80)

    # Load data
    interpolar_data = load_interpolar_data(primary_loinc)
    if not interpolar_data:
        sys.exit(1)

    experiment_data = load_ecl_experiment_data(primary_loinc)

    # Create comparison table
    df_comparison = create_comparison_table(interpolar_data, experiment_data)

    # Create summary
    summary = create_summary(interpolar_data, experiment_data, df_comparison)

    # Save outputs
    output_dir = OUTPUT_BASE_DIR / primary_loinc.replace('-', '')
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_file = output_dir / 'detailed_comparison.csv'
    df_comparison.to_csv(csv_file, index=False)

    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)
    print(f"\nOutput directory: {output_dir}")
    print(f"  - detailed_comparison.csv ({len(df_comparison)} rows)")
    print(f"  - summary.json")

if __name__ == '__main__':
    main()
