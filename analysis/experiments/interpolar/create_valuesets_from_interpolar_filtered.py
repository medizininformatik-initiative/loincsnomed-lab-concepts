#!/usr/bin/env python3
"""
Create FHIR ValueSets from Interpolar LOINC Mapping - FILTERED VERSION
=======================================================================
Only includes codes with COMPARABILITY_TO_LOINC_PRIMARY:
- "1 - quantitativ"
- "2 - cutoff_Fragestellung"

Excludes: "3 - qualitativ", "4 - berechnet", "5 - nein", "unklar"
"""

import pandas as pd
import json
import os
import sys
import asyncio
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Add the scripts directory to path to import utilities
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from loinc_display_fetcher import fetch_displays_async

# Configuration
INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'valuesets_interpolar_filtered'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("CREATE FILTERED INTERPOLAR VALUESETS")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
print("Filter: COMPARABILITY_TO_LOINC_PRIMARY in ['1 - quantitativ', '2 - cutoff_Fragestellung']")

# ==============================================================================
# STEP 1: Read Excel File
# ==============================================================================
print("\n[STEP 1/3] Reading Interpolar mapping Excel file...")
df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)
print(f"  [OK] Loaded {len(df)} total rows")

# ==============================================================================
# STEP 2: Filter by Comparability
# ==============================================================================
print("\n[STEP 2/3] Filtering by comparability...")

# Show all comparability levels before filtering
print("\n  Comparability levels in source data:")
for val, count in df['COMPARABILITY_TO_LOINC_PRIMARY'].value_counts().items():
    print(f"    {val}: {count} codes")

# Apply filter: Keep only "1 - quantitativ" and "2 - cutoff_Fragestellung"
df_filtered = df[df['COMPARABILITY_TO_LOINC_PRIMARY'].isin([
    '1 - quantitativ',
    '2 - cutoff_Fragestellung'
])].copy()

print(f"\n  [OK] After filtering: {len(df_filtered)} rows retained")
print(f"  [OK] Excluded: {len(df) - len(df_filtered)} rows")

# ==============================================================================
# STEP 3: Group by Primary Code and Create ValueSets
# ==============================================================================
print("\n[STEP 3/3] Creating FHIR ValueSets...")

# Group secondary codes by primary code
primary_to_secondary = defaultdict(list)
primary_to_name = {}

for _, row in df_filtered.iterrows():
    loinc = row['LOINC']
    primary = row['LOINC_PRIMARY']
    name = row['GERMAN_NAME_LOINC_PRIMARY']

    if pd.notna(primary):
        # Store name
        if primary not in primary_to_name and pd.notna(name):
            primary_to_name[primary] = name

        # Add secondary code
        if pd.notna(loinc):
            primary_to_secondary[primary].append(loinc)

# Remove duplicates
for primary in primary_to_secondary:
    primary_to_secondary[primary] = list(set(primary_to_secondary[primary]))

print(f"  [OK] Found {len(primary_to_secondary)} unique primary LOINC codes")
print(f"  [OK] Total secondary codes: {sum(len(v) for v in primary_to_secondary.values())}")

# Collect all unique LOINC codes
all_loinc_codes = set()
for codes in primary_to_secondary.values():
    all_loinc_codes.update(codes)

# Fetch all display labels in parallel
print(f"  Fetching display labels for {len(all_loinc_codes)} unique LOINC codes (in parallel)...")
loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=True, max_concurrent=15))

# Create FHIR ValueSets
created_count = 0
for primary_loinc, secondary_codes in primary_to_secondary.items():
    german_name = primary_to_name.get(primary_loinc, primary_loinc)

    valueset = {
        "resourceType": "ValueSet",
        "id": f"interpolar-filtered-loinc-{primary_loinc.replace('-', '')}",
        "url": f"https://www.medizininformatik-initiative.de/fhir/ext/modul-labor/ValueSet/interpolar-filtered-loinc-{primary_loinc.replace('-', '')}",
        "version": "1.0",
        "name": f"InterpolarFiltered{primary_loinc.replace('-', '')}",
        "title": f"Interpolar LOINC (Filtered): {german_name}",
        "status": "draft",
        "experimental": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "publisher": "MII INTERPOLAR - Filtered (1-quantitativ + 2-cutoff)",
        "description": f"Interpolar LOINC codes for primary code {primary_loinc}. Includes only comparability levels '1 - quantitativ' and '2 - cutoff_Fragestellung'. Total codes: {len(secondary_codes)}",
        "compose": {
            "include": [
                {
                    "system": "http://loinc.org",
                    "concept": [
                        {"code": code, "display": loinc_displays.get(code, f"LOINC {code}")}
                        for code in sorted(secondary_codes)
                    ]
                }
            ]
        }
    }

    # Save ValueSet
    output_file = OUTPUT_DIR / f"valueset-interpolar-filtered-loinc-{primary_loinc.replace('-', '')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(valueset, f, indent=2, ensure_ascii=False)

    created_count += 1

print(f"  [OK] Created {created_count} FHIR ValueSets")

# ==============================================================================
# Summary Report
# ==============================================================================
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total primary codes: {len(primary_to_secondary)}")
print(f"Total secondary codes: {sum(len(v) for v in primary_to_secondary.values())}")
print(f"Output directory: {OUTPUT_DIR}")
print(f"\nComparability levels included:")
print(f"  - 1 - quantitativ")
print(f"  - 2 - cutoff_Fragestellung")
print(f"\nComparability levels excluded:")
print(f"  - 3 - qualitativ")
print(f"  - 4 - berechnet")
print(f"  - 5 - nein")
print(f"  - unklar")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
