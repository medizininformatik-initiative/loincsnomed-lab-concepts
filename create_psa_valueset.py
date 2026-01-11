#!/usr/bin/env python3
"""
Generate PSA (Prostate Specific Antigen) ValueSet from dashboard results
"""
import json
import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add the scripts directory to path to import utilities
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'scripts'))
from loinc_display_fetcher import fetch_displays_async

# PSA LOINC codes from the ECL component descendants experiment (Exp 2)
# These are all PSA-related codes found in blood/plasma/serum
psa_loinc_codes = [
    "100716-0", "10508-0", "10886-0", "109229-5", "109230-3",
    "110243-3", "110671-5", "12841-3", "19195-7", "19197-3",
    "19198-1", "19199-9", "19200-5", "19201-3", "19203-9",
    "19204-7", "19205-4", "19206-2", "2857-1", "33667-7",
    "34611-4", "35741-8", "47738-0", "48167-1", "59221-2",
    "59223-8", "59224-6", "59230-3", "59231-1", "59232-9",
    "59235-2", "59236-0", "59237-8", "59238-6", "59239-4",
    "83112-3", "83113-1"
]

print(f"Fetching display labels for {len(psa_loinc_codes)} PSA LOINC codes...")
loinc_displays = asyncio.run(fetch_displays_async(psa_loinc_codes, verbose=True, max_concurrent=15))

# Create FHIR ValueSet
valueset = {
    "resourceType": "ValueSet",
    "id": "psa-loinc-snomed",
    "url": "https://www.medizininformatik-initiative.de/fhir/ext/modul-labor/ValueSet/psa-loinc-snomed",
    "version": "1.0",
    "name": "PSALoincSnomed",
    "title": "Prostate Specific Antigen (PSA) LOINC Codes",
    "status": "draft",
    "experimental": True,
    "date": datetime.now().strftime("%Y-%m-%d"),
    "publisher": "MII",
    "description": "ValueSet containing LOINC codes for Prostate Specific Antigen (PSA) measurements in blood, serum, and plasma. Generated from LOINCSNOMED edition using ECL component descendants query (SNOMED Component: 102687007 |Prostate specific antigen|).",
    "compose": {
        "include": [
            {
                "system": "http://loinc.org",
                "concept": [
                    {
                        "code": code,
                        "display": loinc_displays.get(code, f"LOINC {code}")
                    }
                    for code in sorted(psa_loinc_codes)
                ]
            }
        ]
    }
}

# Create output directory
output_dir = project_root / 'output' / 'valuesets'
output_dir.mkdir(parents=True, exist_ok=True)

# Write to file
output_file = output_dir / "valueset-psa-loinc-snomed.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(valueset, f, indent=2, ensure_ascii=False)

print(f"\n✓ Created PSA ValueSet: {output_file}")
print(f"✓ Total codes: {len(psa_loinc_codes)}")
print(f"✓ Primary code: 2857-1 (Prostate specific Ag [Mass/volume] in Serum or Plasma)")
