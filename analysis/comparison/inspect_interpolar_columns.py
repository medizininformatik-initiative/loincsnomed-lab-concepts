#!/usr/bin/env python3
"""
Quick script to inspect Interpolar Excel file columns
"""
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'

df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)

print("Columns in the Excel file:")
print(df.columns.tolist())
print("\n" + "="*80)

# Check for comparability columns
comp_cols = [col for col in df.columns if 'COMPARABILITY' in col.upper()]
print(f"\nComparability columns found: {comp_cols}")

# Sample values from COMPARABILITY_TO_LOINC_PRIMARY
if 'COMPARABILITY_TO_LOINC_PRIMARY' in df.columns:
    print("\nUnique values in COMPARABILITY_TO_LOINC_PRIMARY:")
    print(df['COMPARABILITY_TO_LOINC_PRIMARY'].value_counts())

    # Show examples of each value
    print("\n" + "="*80)
    print("Examples for each comparability level:")
    for val in df['COMPARABILITY_TO_LOINC_PRIMARY'].dropna().unique():
        print(f"\n{val}:")
        samples = df[df['COMPARABILITY_TO_LOINC_PRIMARY'] == val].head(3)
        for _, row in samples.iterrows():
            print(f"  {row['LOINC']} - {row.get('GERMAN_NAME_LOINC_PRIMARY', 'N/A')}")
