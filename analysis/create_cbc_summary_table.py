#!/usr/bin/env python3
"""
Create CBC Summary Tables
=========================
Generates comprehensive summary tables for all CBC components analyzed.

Includes:
- Hemoglobin
- Methemoglobin
- Erythrocytes (RBC)
- Hematocrit
- Leukocytes (WBC)
- Platelets
- MCV, MCH, MCHC (Erythrocyte indices)
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'singular_concepts'

print("=" * 80)
print("CBC SUMMARY TABLES GENERATOR")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Define all CBC components and their data locations
cbc_components = {
    'Hemoglobin': {
        'dir': 'blood_count_hemoglobin',
        'csv': 'hemoglobin_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'Methemoglobin': {
        'dir': 'blood_count_methemoglobin',
        'csv': 'methemoglobin_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'Erythrocytes': {
        'dir': 'blood_count_erythrocytes',
        'csv': 'erythrocytes_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'Hematocrit': {
        'dir': 'blood_count_hematocrit',
        'csv': 'hematocrit_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'Leukocytes': {
        'dir': 'blood_count_leukocytes',
        'csv': 'leukocytes_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'Platelets': {
        'dir': 'blood_count_platelets',
        'csv': 'platelets_ecl_comparison.csv',
        'category': 'Direct Observation'
    },
    'MCV': {
        'dir': 'blood_count_erythrocyte_indices',
        'csv': 'mcv_ecl_comparison.csv',
        'category': 'Calculated Index'
    },
    'MCH': {
        'dir': 'blood_count_erythrocyte_indices',
        'csv': 'mch_ecl_comparison.csv',
        'category': 'Calculated Index'
    },
    'MCHC': {
        'dir': 'blood_count_erythrocyte_indices',
        'csv': 'mchc_ecl_comparison.csv',
        'category': 'Calculated Index'
    }
}

# Collect all data
all_data = []
summary_stats = []

print("Loading CBC component data...")
for component_name, info in cbc_components.items():
    csv_path = OUTPUT_DIR / info['dir'] / info['csv']

    if not csv_path.exists():
        print(f"  [SKIP] {component_name}: File not found")
        continue

    df = pd.read_csv(csv_path)

    # Add component name and category
    df['Component'] = component_name
    df['Category'] = info['category']

    all_data.append(df)

    # Collect summary stats
    summary_stats.append({
        'Component': component_name,
        'Category': info['category'],
        'LOINC_Count': len(df),
        'Has_Primary': 'Yes' if 'Is_Primary' in df.columns and df['Is_Primary'].eq('Yes').any() else '',
        'Primary_Code': df[df['Is_Primary'] == 'Yes']['LOINC_Code'].iloc[0] if 'Is_Primary' in df.columns and df['Is_Primary'].eq('Yes').any() else ''
    })

    print(f"  [OK] {component_name}: {len(df)} LOINC codes")

# Combine all data
print(f"\nCombining data from {len(all_data)} components...")
df_combined = pd.concat(all_data, ignore_index=True)

# Create summary statistics table
print("Creating summary statistics table...")
df_summary = pd.DataFrame(summary_stats)

# Reorder columns for better readability
cols_order = ['Component', 'Category', 'LOINC_Count']
if 'Has_Primary' in df_summary.columns:
    cols_order.extend(['Has_Primary', 'Primary_Code'])
df_summary = df_summary[cols_order]

# Save combined detailed table
detailed_output = OUTPUT_DIR / 'cbc_combined_detailed.csv'
df_combined.to_csv(detailed_output, index=False)
print(f"\n  Saved detailed table: {detailed_output}")
print(f"    Total rows: {len(df_combined)}")

# Save summary table
summary_output = OUTPUT_DIR / 'cbc_summary.csv'
df_summary.to_csv(summary_output, index=False)
print(f"  Saved summary table: {summary_output}")
print(f"    Total components: {len(df_summary)}")

# Create a pivot-style table showing LOINC codes by component
print("\nCreating component-LOINC matrix...")
# Select key columns
matrix_data = []
for component_name, info in cbc_components.items():
    csv_path = OUTPUT_DIR / info['dir'] / info['csv']
    if not csv_path.exists():
        continue

    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        matrix_data.append({
            'Component': component_name,
            'LOINC_Code': row['LOINC_Code'],
            'LOINC_Display': row.get('LOINC_Display', ''),
            'Category': info['category']
        })

df_matrix = pd.DataFrame(matrix_data)
matrix_output = OUTPUT_DIR / 'cbc_component_loinc_matrix.csv'
df_matrix.to_csv(matrix_output, index=False)
print(f"  Saved matrix table: {matrix_output}")
print(f"    Total LOINC-Component pairs: {len(df_matrix)}")

# Print summary to console
print("\n" + "=" * 80)
print("CBC SUMMARY")
print("=" * 80)
print(f"\nDirect Observations: {df_summary[df_summary['Category'] == 'Direct Observation']['LOINC_Count'].sum()} LOINC codes")
print(f"Calculated Indices: {df_summary[df_summary['Category'] == 'Calculated Index']['LOINC_Count'].sum()} LOINC codes")
print(f"\nTotal unique LOINC codes: {df_combined['LOINC_Code'].nunique()}")
print(f"Total CBC components analyzed: {len(df_summary)}")

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  1. {detailed_output}")
print(f"  2. {summary_output}")
print(f"  3. {matrix_output}")
