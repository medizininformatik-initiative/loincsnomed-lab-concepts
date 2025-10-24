#!/usr/bin/env python3
"""
Test Refined Leukocytes (WBC Count) ECL Query
==============================================
Leukocytes: White blood cell count

Component: Fixed 52501007 |Leukocyte| (no descendants to exclude precursors)
Property: 118550005 |Number concentration|
System: Blood specimen
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

# Add helper repo to path
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter

# Add local scripts to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from loinc_display_fetcher import fetch_displays_async

# Configuration
LOINC_SNOMED_MAPPING_PATH = os.getenv('loinc_snomed_mapping_path')
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_leukocytes'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("REFINED LEUKOCYTES (WBC COUNT) ECL TEST")
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

# Define ECL queries for leukocytes
# Component: 52501007 |Leukocyte| (fixed, no descendants)
# Property: 118550005 |Number concentration|
ecl_queries = {
    'leukocytes_fixed_component_excl_cord': """
<< 363787002 |Observable entity| :
    << 246093002 |Component| = 52501007 |Leukocyte|,
    << 370130000 |Property| = << 118550005 |Number concentration|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|,
    << 704327008 |Direct site| != << 122556008 |Cord blood specimen|
""".strip(),
    'leukocytes_fixed_component_incl_cord': """
<< 363787002 |Observable entity| :
    << 246093002 |Component| = 52501007 |Leukocyte|,
    << 370130000 |Property| = << 118550005 |Number concentration|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|
""".strip()
}

# Execute queries
print("[3/4] Executing leukocyte ECL queries...")
results = {}

for query_name, ecl_query in ecl_queries.items():
    print(f"\n  Testing: {query_name}")
    print(f"  ECL: {ecl_query[:80]}...")

    result = execute_ecl_query(ecl_query, loinc_mappings, limit=1000, server_adapter=adapter)

    # Extract LOINC codes
    loinc_codes = []
    snomed_to_loinc = {}

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
        'ecl': ecl_query,
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
for query_result in results.values():
    all_loinc_codes.update(query_result['loinc_codes'])

loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False))
print(f"  [OK] Fetched {len(loinc_displays)} displays")

# Save results
output_file = OUTPUT_DIR / 'leukocytes_ecl_test_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Create CSV
import pandas as pd
rows = []
for loinc_code in sorted(all_loinc_codes):
    # Determine which queries found this code
    in_fixed_excl = 'Yes' if loinc_code in results['leukocytes_fixed_component_excl_cord']['loinc_codes'] else ''
    in_fixed_incl = 'Yes' if loinc_code in results['leukocytes_fixed_component_incl_cord']['loinc_codes'] else ''

    # Get SNOMED IDs
    snomed_ids = []
    if loinc_code in results['leukocytes_fixed_component_excl_cord']['snomed_to_loinc_mapping']:
        snomed_ids = [m['snomed_id'] for m in results['leukocytes_fixed_component_excl_cord']['snomed_to_loinc_mapping'][loinc_code]]
    elif loinc_code in results['leukocytes_fixed_component_incl_cord']['snomed_to_loinc_mapping']:
        snomed_ids = [m['snomed_id'] for m in results['leukocytes_fixed_component_incl_cord']['snomed_to_loinc_mapping'][loinc_code]]

    rows.append({
        'LOINC_Code': loinc_code,
        'LOINC_Display': loinc_displays.get(loinc_code, ''),
        'FixedComp_Excl_Cord': in_fixed_excl,
        'FixedComp_Incl_Cord': in_fixed_incl,
        'SNOMED_IDs': '; '.join(snomed_ids) if snomed_ids else ''
    })

df_out = pd.DataFrame(rows)
csv_file = OUTPUT_DIR / 'leukocytes_ecl_comparison.csv'
df_out.to_csv(csv_file, index=False)

print(f"\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {output_file}")
print(f"  - {csv_file}")
print(f"\nRows in CSV: {len(df_out)}")
