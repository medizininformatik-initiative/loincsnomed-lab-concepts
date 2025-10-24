#!/usr/bin/env python3
"""
Create Comprehensive Review Table
==================================
Generates detailed comparison tables for reviewing all LOINC codes across different approaches:
- Interpolar comparability levels (1-5)
- Presence in each ECL approach (descendants, component-fixed, component-system, etc.)
- Summary metrics for each approach

Output:
- detailed_loinc_comparison.csv: Row per LOINC code with all approach columns
- approach_summary.csv: Overall performance metrics per approach
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
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'comprehensive_review'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("COMPREHENSIVE REVIEW TABLE GENERATOR")
print("=" * 80)

# ==============================================================================
# STEP 1: Load Interpolar data
# ==============================================================================
print("\n[STEP 1/4] Loading Interpolar data...")
df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)

# Create mapping: LOINC code -> comparability level
loinc_comparability = {}
for _, row in df.iterrows():
    loinc = row['LOINC']
    primary = row['LOINC_PRIMARY']
    comparability = row['COMPARABILITY_TO_LOINC_PRIMARY']

    if pd.notna(loinc) and pd.notna(primary) and pd.notna(comparability):
        loinc_comparability[loinc] = comparability

print(f"  [OK] Loaded comparability for {len(loinc_comparability)} LOINC codes")

# ==============================================================================
# STEP 2: Load ECL experiment results
# ==============================================================================
print("\n[STEP 2/4] Loading ECL experiment results...")

experiments = {
    'ecl_descendants_baseline': PROJECT_ROOT / 'output' / 'ecl_descendants_baseline' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component': PROJECT_ROOT / 'output' / 'ecl_fixed_component' / 'comparison_interpolar_vs_ecl.json',
    'ecl_component_descendants': PROJECT_ROOT / 'output' / 'ecl_component_descendants' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component_property': PROJECT_ROOT / 'output' / 'ecl_fixed_component_property' / 'comparison_interpolar_vs_ecl.json',
    'ecl_fixed_component_system': PROJECT_ROOT / 'output' / 'ecl_fixed_component_system' / 'comparison_interpolar_vs_ecl.json',
}

# Load results
experiment_results = {}
for name, path in experiments.items():
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            experiment_results[name] = json.load(f)
        print(f"  [OK] Loaded {name}: {len(experiment_results[name])} primary codes")
    else:
        print(f"  [SKIP] {name}: file not found")
        experiment_results[name] = []

# ==============================================================================
# STEP 3: Build comprehensive LOINC-level table
# ==============================================================================
print("\n[STEP 3/4] Building LOINC-level comparison table...")

# Collect all unique LOINC codes across all experiments
all_loinc_codes = set(loinc_comparability.keys())

# Add LOINC codes from ECL experiments
for exp_name, results in experiment_results.items():
    for primary_result in results:
        all_loinc_codes.update(primary_result.get('interpolar_codes', []))
        all_loinc_codes.update(primary_result.get('ecl_codes', []))

print(f"  Found {len(all_loinc_codes)} unique LOINC codes total")

# Fetch LOINC display names
print(f"  Fetching display names for all LOINC codes...")
loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False))

# Build table rows
rows = []
for loinc_code in sorted(all_loinc_codes):
    row = {
        'LOINC_Code': loinc_code,
        'LOINC_Display': loinc_displays.get(loinc_code, ''),
        'Interpolar_Comparability': loinc_comparability.get(loinc_code, ''),
    }

    # Add columns for each ECL approach
    for exp_name in experiments.keys():
        # Check if this LOINC is in Interpolar for this experiment
        in_interpolar = False
        in_ecl = False

        for primary_result in experiment_results.get(exp_name, []):
            if loinc_code in primary_result.get('interpolar_codes', []):
                in_interpolar = True
            if loinc_code in primary_result.get('ecl_codes', []):
                in_ecl = True

        row[f'{exp_name}_Interpolar'] = 'Yes' if in_interpolar else ''
        row[f'{exp_name}_ECL'] = 'Yes' if in_ecl else ''
        row[f'{exp_name}_Match'] = 'Yes' if (in_interpolar and in_ecl) else ''

    rows.append(row)

df_detailed = pd.DataFrame(rows)

# Save detailed table
output_file = OUTPUT_DIR / 'detailed_loinc_comparison.csv'
df_detailed.to_csv(output_file, index=False)
print(f"  [OK] Saved detailed table: {output_file}")
print(f"       Rows: {len(df_detailed)}, Columns: {len(df_detailed.columns)}")

# ==============================================================================
# STEP 4: Create summary metrics table
# ==============================================================================
print("\n[STEP 4/4] Creating approach summary table...")

summary_rows = []

for exp_name, results in experiment_results.items():
    if not results:
        continue

    # Calculate metrics
    total_primary = len(results)
    total_interpolar = sum(r['interpolar_count'] for r in results)
    total_ecl = sum(r['ecl_count'] for r in results)
    total_overlap = sum(r['overlap_count'] for r in results)

    avg_precision = sum(r['precision'] for r in results) / total_primary if total_primary else 0
    avg_recall = sum(r['recall'] for r in results) / total_primary if total_primary else 0
    avg_f1 = sum(r['f1_score'] for r in results) / total_primary if total_primary else 0

    # Coverage rate (what % of Interpolar codes are found by ECL)
    coverage_rate = (total_overlap / total_interpolar * 100) if total_interpolar else 0

    summary_rows.append({
        'Approach': exp_name.replace('_', ' ').title(),
        'Primary_Codes': total_primary,
        'Total_Interpolar_Codes': total_interpolar,
        'Total_ECL_Codes': total_ecl,
        'Overlap_Codes': total_overlap,
        'Coverage_Rate_%': round(coverage_rate, 2),
        'Avg_Precision': round(avg_precision, 3),
        'Avg_Recall': round(avg_recall, 3),
        'Avg_F1_Score': round(avg_f1, 3),
    })

df_summary = pd.DataFrame(summary_rows)

# Save summary table
summary_file = OUTPUT_DIR / 'approach_summary.csv'
df_summary.to_csv(summary_file, index=False)
print(f"  [OK] Saved summary table: {summary_file}")

# Print summary to console
print("\n" + "=" * 80)
print("APPROACH SUMMARY")
print("=" * 80)
print(df_summary.to_string(index=False))

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {output_file}")
print(f"  - {summary_file}")
