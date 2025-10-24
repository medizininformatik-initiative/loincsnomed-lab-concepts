#!/usr/bin/env python3
"""
Test Refined Methemoglobin ECL Query
======================================
Similar to hemoglobin, but for methemoglobin component.

Two Interpolar primaries:
- 2614-6: Methemoglobin/Hemoglobin.total
- 56040-9: Methemoglobin [Mol/Volumen]
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
print("REFINED METHEMOGLOBIN ECL TEST")
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

# Define ECL query for methemoglobin (Component = Methemoglobin substance)
# SNOMED concept for Methemoglobin: 5737002
ecl_query = """
<< 363787002 |Observable entity| :
    << 246093002 |Component| = 5737002 |Methemoglobin|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|
""".strip()

# Execute query
print("[3/4] Executing methemoglobin ECL query...")
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

print(f"  Result: {result.get('total', 0)} SNOMED concepts -> {len(loinc_codes)} LOINC codes")

# Fetch LOINC displays
print(f"\n[4/4] Fetching LOINC display names...")
loinc_displays = asyncio.run(fetch_displays_async(sorted(loinc_codes), verbose=False))
print(f"  [OK] Fetched {len(loinc_displays)} displays")

# Load Interpolar data for comparison
import pandas as pd
INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)
df_quant = df[df['COMPARABILITY_TO_LOINC_PRIMARY'] == '1 - quantitativ'].copy()

# Get methemoglobin interpolar codes
interpolar_primaries = ['2614-6', '56040-9']
interpolar_codes = set()
for primary in interpolar_primaries:
    codes = df_quant[df_quant['LOINC_PRIMARY'] == primary]['LOINC'].dropna().unique()
    interpolar_codes.update(codes)
    interpolar_codes.add(primary)

print(f"\nComparing with Interpolar...")
print(f"  Interpolar: {len(interpolar_codes)} codes")

ecl_codes_set = set(loinc_codes)
overlap = interpolar_codes & ecl_codes_set

print(f"  ECL codes: {len(ecl_codes_set)}")
print(f"  Overlap with Interpolar: {len(overlap)} ({len(overlap)/len(interpolar_codes)*100:.1f}%)")
print(f"  Interpolar only: {len(interpolar_codes - ecl_codes_set)}")
print(f"  ECL only: {len(ecl_codes_set - interpolar_codes)}")

# Save results
results = {
    'methemoglobin': {
        'ecl': ecl_query,
        'snomed_concept_count': result.get('total', 0),
        'loinc_code_count': len(loinc_codes),
        'loinc_codes': loinc_codes,
        'snomed_to_loinc_mapping': snomed_to_loinc,
        'execution_time': result.get('execution_time', 0),
        'interpolar_comparison': {
            'interpolar_count': len(interpolar_codes),
            'overlap_count': len(overlap),
            'interpolar_only': sorted(list(interpolar_codes - ecl_codes_set)),
            'ecl_only': sorted(list(ecl_codes_set - interpolar_codes)),
            'overlap_codes': sorted(list(overlap))
        }
    }
}

output_file = OUTPUT_DIR / 'methemoglobin_ecl_test_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Create CSV
import pandas as pd
rows = []
for loinc_code in sorted(set(loinc_codes) | interpolar_codes):
    snomed_mapping = snomed_to_loinc.get(loinc_code, [])
    snomed_ids = [m['snomed_id'] for m in snomed_mapping]

    rows.append({
        'LOINC_Code': loinc_code,
        'LOINC_Display': loinc_displays.get(loinc_code, ''),
        'In_Interpolar': 'Yes' if loinc_code in interpolar_codes else '',
        'In_ECL': 'Yes' if loinc_code in ecl_codes_set else '',
        'SNOMED_IDs': '; '.join(snomed_ids) if snomed_ids else ''
    })

df_out = pd.DataFrame(rows)
csv_file = OUTPUT_DIR / 'methemoglobin_ecl_comparison.csv'
df_out.to_csv(csv_file, index=False)

print(f"\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {output_file}")
print(f"  - {csv_file}")
print(f"\nRows in CSV: {len(df_out)}")
