#!/usr/bin/env python3
"""
Test that the ECL script updates work correctly.
Simulates the key parts of ecl_descendants_baseline_run_all.py.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add local scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from loinc_display_fetcher import LOINCDisplayFetcher

print("Testing ECL Script Integration with LOINC Display Fetcher")
print("="*70)

# Simulate ECL query results (these would normally come from the server)
simulated_ecl_results = {
    '1920-8': {
        'primary_loinc': '1920-8',
        'snomed_concept_id': '12345678',
        'ecl_expression': '<< 363787002',
        'loinc_codes_found': ['1920-8', '30239-8', '88112-8']
    },
    '2345-7': {
        'primary_loinc': '2345-7',
        'snomed_concept_id': '87654321',
        'ecl_expression': '<< 123456789',
        'loinc_codes_found': ['2345-7', '2951-2']
    }
}

print("\n1. Simulating ECL query results collection...")
print(f"   Found {len(simulated_ecl_results)} primary codes")

# Collect all unique LOINC codes (simulating what the script does)
all_ecl_loinc_codes = set()
for ecl_data in simulated_ecl_results.values():
    all_ecl_loinc_codes.update(ecl_data['loinc_codes_found'])

print(f"   Total unique LOINC codes: {len(all_ecl_loinc_codes)}")
print(f"   Codes: {sorted(all_ecl_loinc_codes)}")

# Initialize fetcher and batch fetch displays
print("\n2. Initializing LOINC display fetcher...")
loinc_fetcher = LOINCDisplayFetcher(verbose=True)

print("\n3. Batch fetching LOINC displays...")
loinc_displays = loinc_fetcher.fetch_displays(sorted(all_ecl_loinc_codes))

# Create test value sets (simulating what the script does)
print("\n4. Creating test ValueSets with displays...")
output_dir = Path('output/test_ecl_valuesets')
output_dir.mkdir(parents=True, exist_ok=True)

for primary_loinc, ecl_data in simulated_ecl_results.items():
    ecl_loinc_codes = ecl_data['loinc_codes_found']

    valueset = {
        "resourceType": "ValueSet",
        "id": f"test-ecl-{primary_loinc.replace('-', '')}",
        "url": f"https://test.example.org/ValueSet/test-ecl-{primary_loinc.replace('-', '')}",
        "version": "1.0",
        "name": f"TestECL{primary_loinc.replace('-', '')}",
        "title": f"Test ECL ValueSet for {primary_loinc}",
        "status": "draft",
        "experimental": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "publisher": "Test",
        "description": f"Test ECL ValueSet for LOINC {primary_loinc} (SNOMED {ecl_data['snomed_concept_id']})",
        "compose": {
            "include": [
                {
                    "system": "http://loinc.org",
                    "concept": [
                        {"code": code, "display": loinc_displays.get(code, f"LOINC {code}")}
                        for code in sorted(ecl_loinc_codes)
                    ]
                }
            ]
        }
    }

    vs_file = output_dir / f"valueset-test-ecl-{primary_loinc.replace('-', '')}.json"
    with open(vs_file, 'w', encoding='utf-8') as f:
        json.dump(valueset, f, indent=2, ensure_ascii=False)

    print(f"\n   Created: {vs_file.name}")
    print(f"   Contains {len(ecl_loinc_codes)} codes:")
    for concept in valueset['compose']['include'][0]['concept']:
        print(f"     - {concept['code']}: {concept['display']}")

print("\n" + "="*70)
print("Test complete! ✓")
print(f"Output directory: {output_dir}")
print("\nVerify that the displays are correct LOINC names, not placeholders.")
