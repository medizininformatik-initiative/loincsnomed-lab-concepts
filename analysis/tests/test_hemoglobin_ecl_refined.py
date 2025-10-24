#!/usr/bin/env python3
"""
Test Refined Hemoglobin ECL Query
===================================
Tests the manually curated hemoglobin ECL with:
- Component = Hemoglobin (with descendants)
- Property = Measurement property (with descendants)
- Direct site = Blood specimen (with descendants)
- Excludes cord blood

Two variants:
1. Excluding cord blood
2. Including cord blood

Compares results with Interpolar data for hemoglobin (59260-0).
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Add local scripts to path (from repository root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter
from loinc_display_fetcher import fetch_displays_async

# Configuration
LOINC_SNOMED_MAPPING_PATH = os.getenv('loinc_snomed_mapping_path')
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin'

print("=" * 80)
print("REFINED HEMOGLOBIN ECL TEST")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load LOINC-SNOMED mappings
print("[1/4] Loading LOINC-SNOMED mappings...")
loinc_mappings = load_loinc_mappings(LOINC_SNOMED_MAPPING_PATH)
print(f"  [OK] Loaded {len(loinc_mappings)} mappings\n")

# Create terminology server adapter
print("[2/4] Connecting to LOINCSNOMED Snowstorm...")
adapter = create_adapter('loincsnomed')
print(f"  [OK] Connected\n")

# Define ECL queries
ecl_queries = {
    'hemoglobin_excl_cord': """
<< 363787002 |Observable entity| :
    << 246093002 |Component| = 38082009 |Hemoglobin|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|,
    << 704327008 |Direct site| != << 122556008 |Cord blood specimen|
    """.strip(),

    'hemoglobin_incl_cord': """
<< 363787002 |Observable entity| :
    << 246093002 |Component| = 38082009 |Hemoglobin|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|
    """.strip()
}

# Execute queries
print("[3/4] Executing ECL queries...")
results = {}

for query_name, ecl in ecl_queries.items():
    print(f"\n  Testing: {query_name}")
    print(f"  ECL: {ecl[:80]}...")

    result = execute_ecl_query(ecl, loinc_mappings, limit=1000, server_adapter=adapter)

    # Extract LOINC codes
    loinc_codes = []
    snomed_to_loinc = {}  # Preserve coupling

    for concept in result.get('detailed_concepts', []):
        snomed_id = concept.get('concept_id')
        loinc_code = concept.get('loinc_code')

        if loinc_code and snomed_id:
            loinc_codes.append(loinc_code)
            if loinc_code not in snomed_to_loinc:
                snomed_to_loinc[loinc_code] = []
            snomed_to_loinc[loinc_code].append({
                'snomed_id': snomed_id,
                'snomed_fsn': concept.get('fsn', '')
            })

    loinc_codes = sorted(list(set(loinc_codes)))

    results[query_name] = {
        'ecl': ecl,
        'snomed_concept_count': result.get('total', 0),
        'loinc_code_count': len(loinc_codes),
        'loinc_codes': loinc_codes,
        'snomed_to_loinc_mapping': snomed_to_loinc,
        'execution_time': result.get('execution_time', 0)
    }

    print(f"  Result: {result.get('total', 0)} SNOMED concepts -> {len(loinc_codes)} LOINC codes")

# Fetch LOINC displays
print(f"\n[4/4] Fetching LOINC display names...")
all_loinc_codes = set()
for r in results.values():
    all_loinc_codes.update(r['loinc_codes'])

loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False))
print(f"  [OK] Fetched {len(loinc_displays)} displays")

# Compare with Interpolar (load from previous analysis)
print(f"\nComparing with Interpolar...")
interpolar_file = OUTPUT_DIR / 'summary.json'
if interpolar_file.exists():
    with open(interpolar_file, 'r', encoding='utf-8') as f:
        interpolar_data = json.load(f)

    interpolar_codes = set(interpolar_data['interpolar_codes'])

    print(f"  Interpolar: {len(interpolar_codes)} codes")

    for query_name, result in results.items():
        ecl_codes = set(result['loinc_codes'])
        overlap = interpolar_codes & ecl_codes

        print(f"\n  {query_name}:")
        print(f"    ECL codes: {len(ecl_codes)}")
        print(f"    Overlap with Interpolar: {len(overlap)} ({len(overlap)/len(interpolar_codes)*100:.1f}%)")
        print(f"    Interpolar only: {len(interpolar_codes - ecl_codes)}")
        print(f"    ECL only: {len(ecl_codes - interpolar_codes)}")

        result['interpolar_comparison'] = {
            'interpolar_count': len(interpolar_codes),
            'overlap_count': len(overlap),
            'interpolar_only': sorted(list(interpolar_codes - ecl_codes)),
            'ecl_only': sorted(list(ecl_codes - interpolar_codes)),
            'overlap_codes': sorted(list(overlap))
        }
else:
    print("  Warning: No Interpolar data found for comparison")

# Save results
output_file = OUTPUT_DIR / 'refined_ecl_test_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Create detailed comparison CSV
import pandas as pd

rows = []
for loinc_code in sorted(all_loinc_codes):
    row = {
        'LOINC_Code': loinc_code,
        'LOINC_Display': loinc_displays.get(loinc_code, ''),
        'In_Interpolar': 'Yes' if loinc_code in interpolar_codes else '',
        'Excl_Cord_Blood': 'Yes' if loinc_code in results['hemoglobin_excl_cord']['loinc_codes'] else '',
        'Incl_Cord_Blood': 'Yes' if loinc_code in results['hemoglobin_incl_cord']['loinc_codes'] else '',
    }

    # Add SNOMED concepts for each variant
    for query_name in ['hemoglobin_excl_cord', 'hemoglobin_incl_cord']:
        snomed_mapping = results[query_name]['snomed_to_loinc_mapping'].get(loinc_code, [])
        snomed_ids = [m['snomed_id'] for m in snomed_mapping]
        row[f'{query_name}_SNOMED'] = '; '.join(snomed_ids) if snomed_ids else ''

    rows.append(row)

df = pd.DataFrame(rows)
csv_file = OUTPUT_DIR / 'refined_ecl_comparison.csv'
df.to_csv(csv_file, index=False)

print(f"\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {output_file}")
print(f"  - {csv_file}")
print(f"\nRows in CSV: {len(df)}")
