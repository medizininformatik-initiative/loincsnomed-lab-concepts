#!/usr/bin/env python3
"""
Compare Pre-coordinated vs Post-coordinated Methemoglobin Queries
==================================================================
Tests two approaches:
1. Pre-coordinated: << 719541010000106 |Measurement of methemoglobin in blood|
2. Post-coordinated ECL: Component=Methemoglobin + Property=Measurement + Site=Blood

This tests if the LOINCSNOMED edition maintains semantic equivalence between
pre-coordinated concepts and their post-coordinated ECL expressions.
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
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin'

print("=" * 80)
print("METHEMOGLOBIN: PRE-COORDINATED VS POST-COORDINATED")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load LOINC-SNOMED mappings
print("[1/5] Loading LOINC-SNOMED mappings...")
loinc_mappings = load_loinc_mappings(LOINC_SNOMED_MAPPING_PATH)
print(f"  [OK] Loaded {len(loinc_mappings)} mappings\n")

# Create terminology server adapter
print("[2/5] Connecting to LOINCSNOMED Snowstorm...")
adapter = create_adapter('loincsnomed')
print(f"  [OK] Connected\n")

# Define queries
queries = {
    'precoordinated': {
        'name': 'Pre-coordinated (Is-A)',
        'ecl': '<< 719541010000106 |Measurement of methemoglobin in blood|'
    },
    'postcoordinated': {
        'name': 'Post-coordinated (ECL - exact component)',
        'ecl': """<< 363787002 |Observable entity| :
    << 246093002 |Component| = 27840003 |Methemoglobin|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|""".replace('\n', ' ').strip()
    },
    'postcoordinated_descendants': {
        'name': 'Post-coordinated (ECL - component descendants)',
        'ecl': """<< 363787002 |Observable entity| :
    << 246093002 |Component| = << 27840003 |Methemoglobin|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|""".replace('\n', ' ').strip()
    }
}

# Execute queries
print("[3/5] Executing both query approaches...\n")
results = {}

for approach, query_info in queries.items():
    print(f"  Testing: {query_info['name']}")
    print(f"  ECL: {query_info['ecl'][:80]}...")

    result = execute_ecl_query(query_info['ecl'], loinc_mappings, limit=1000, server_adapter=adapter)

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

    results[approach] = {
        'ecl': query_info['ecl'],
        'snomed_concept_count': result.get('total', 0),
        'loinc_code_count': len(loinc_codes),
        'loinc_codes': loinc_codes,
        'snomed_to_loinc_mapping': snomed_to_loinc,
        'execution_time': result.get('execution_time', 0)
    }

    print(f"  Result: {result.get('total', 0)} SNOMED concepts -> {len(loinc_codes)} LOINC codes\n")

# Compare results
print("[4/5] Comparing results...")
precoord_codes = set(results['precoordinated']['loinc_codes'])
postcoord_codes = set(results['postcoordinated']['loinc_codes'])
postcoord_desc_codes = set(results['postcoordinated_descendants']['loinc_codes'])

print(f"\n  Pre-coordinated:              {len(precoord_codes)} codes")
print(f"  Post-coord (exact):           {len(postcoord_codes)} codes")
print(f"  Post-coord (descendants):     {len(postcoord_desc_codes)} codes")

# Compare exact vs pre-coord
overlap_exact = precoord_codes & postcoord_codes
precoord_only_exact = precoord_codes - postcoord_codes
postcoord_only_exact = postcoord_codes - precoord_codes

print(f"\n  Exact component vs Pre-coord:")
print(f"    Overlap:        {len(overlap_exact)} codes")
print(f"    Pre-coord only: {len(precoord_only_exact)} codes")
print(f"    Post-coord only: {len(postcoord_only_exact)} codes")

# Compare descendants vs pre-coord
overlap_desc = precoord_codes & postcoord_desc_codes
precoord_only_desc = precoord_codes - postcoord_desc_codes
postcoord_only_desc = postcoord_desc_codes - precoord_codes

print(f"\n  Component descendants vs Pre-coord:")
print(f"    Overlap:        {len(overlap_desc)} codes")
print(f"    Pre-coord only: {len(precoord_only_desc)} codes")
print(f"    Post-coord only: {len(postcoord_only_desc)} codes")

if precoord_codes == postcoord_desc_codes:
    print(f"\n  [OK] IDENTICAL: Pre-coord and post-coord descendants are IDENTICAL!")
else:
    print(f"\n  [!!] DIFFERENT: Pre-coord and post-coord descendants still differ")

# Load Interpolar data for comparison
print("\n[5/5] Comparing with Interpolar...")
import pandas as pd
INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)
df_quant = df[df['COMPARABILITY_TO_LOINC_PRIMARY'] == '1 - quantitativ'].copy()

interpolar_primaries = ['2614-6', '56040-9']
interpolar_codes = set()
for primary in interpolar_primaries:
    codes = df_quant[df_quant['LOINC_PRIMARY'] == primary]['LOINC'].dropna().unique()
    interpolar_codes.update(codes)
    interpolar_codes.add(primary)

print(f"  Interpolar: {len(interpolar_codes)} codes")

for approach in ['precoordinated', 'postcoordinated', 'postcoordinated_descendants']:
    ecl_codes = set(results[approach]['loinc_codes'])
    overlap_interp = interpolar_codes & ecl_codes
    print(f"  {approach}: {len(overlap_interp)}/{len(interpolar_codes)} overlap ({len(overlap_interp)/len(interpolar_codes)*100:.1f}%)")

# Fetch displays for all codes
all_codes = precoord_codes | postcoord_codes | postcoord_desc_codes | interpolar_codes
loinc_displays = asyncio.run(fetch_displays_async(sorted(all_codes), verbose=False))

# Save results
results['comparison'] = {
    'precoord_only_vs_exact': sorted(list(precoord_only_exact)),
    'postcoord_exact_only': sorted(list(postcoord_only_exact)),
    'overlap_exact': sorted(list(overlap_exact)),
    'precoord_only_vs_desc': sorted(list(precoord_only_desc)),
    'postcoord_desc_only': sorted(list(postcoord_only_desc)),
    'overlap_desc': sorted(list(overlap_desc)),
    'interpolar_codes': sorted(list(interpolar_codes)),
    'are_identical_exact': precoord_codes == postcoord_codes,
    'are_identical_desc': precoord_codes == postcoord_desc_codes
}

output_file = OUTPUT_DIR / 'methemoglobin_precoord_vs_postcoord.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Create detailed CSV
rows = []
for loinc_code in sorted(all_codes):
    row = {
        'LOINC_Code': loinc_code,
        'LOINC_Display': loinc_displays.get(loinc_code, ''),
        'In_Interpolar': 'Yes' if loinc_code in interpolar_codes else '',
        'In_PreCoord': 'Yes' if loinc_code in precoord_codes else '',
        'In_PostCoord_Exact': 'Yes' if loinc_code in postcoord_codes else '',
        'In_PostCoord_Descendants': 'Yes' if loinc_code in postcoord_desc_codes else ''
    }
    rows.append(row)

df_out = pd.DataFrame(rows)
csv_file = OUTPUT_DIR / 'methemoglobin_precoord_vs_postcoord.csv'
df_out.to_csv(csv_file, index=False)

print(f"\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nKey Findings:")
if results['comparison']['are_identical_exact']:
    print("  [OK] Pre-coord and post-coord (exact) are IDENTICAL")
else:
    print("  [!!] Pre-coord and post-coord (exact) are DIFFERENT")

if results['comparison']['are_identical_desc']:
    print("  [OK] Pre-coord and post-coord (descendants) are IDENTICAL")
    print("    => Using component descendants fixes the semantic gap!")
else:
    print("  [!!] Pre-coord and post-coord (descendants) still differ")

print(f"\nOutput files:")
print(f"  - {output_file}")
print(f"  - {csv_file}")
