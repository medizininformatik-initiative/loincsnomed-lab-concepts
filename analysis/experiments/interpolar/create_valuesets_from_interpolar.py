import pandas as pd
import json
import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add the scripts directory to path to import utilities
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, os.path.join(project_root, 'scripts'))
from loinc_display_fetcher import fetch_displays_async

# Read the Interpolar mapping file
print("Reading Interpolar mapping file...")
project_root = Path(__file__).parent.parent.parent.parent
input_file = project_root / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
df = pd.read_excel(input_file, sheet_name='LOINC Mapping Interpolar', header=18)

# Filter for quantitative comparability only
df_quantitative = df[df['COMPARABILITY_TO_LOINC_PRIMARY'] == '1 - quantitativ'].copy()

# Group secondary LOINCs by their primary LOINC
primary_to_secondary = defaultdict(list)
primary_to_name = {}

for _, row in df_quantitative.iterrows():
    loinc = row['LOINC']
    primary = row['LOINC_PRIMARY']
    name = row['GERMAN_NAME_LOINC_PRIMARY']

    if pd.notna(loinc) and pd.notna(primary):
        # Store the name of the primary code
        if primary not in primary_to_name and pd.notna(name):
            primary_to_name[primary] = name

        # Add all LOINCs (including the primary itself if it appears in the LOINC column)
        primary_to_secondary[primary].append(loinc)

# Remove duplicates
for primary in primary_to_secondary:
    primary_to_secondary[primary] = list(set(primary_to_secondary[primary]))

print(f"Found {len(primary_to_secondary)} primary LOINC codes")
print(f"Total secondary mappings: {sum(len(v) for v in primary_to_secondary.values())}")

# Collect all unique LOINC codes that need display labels
all_loinc_codes = set()
for codes in primary_to_secondary.values():
    all_loinc_codes.update(codes)

# Fetch all display labels in parallel (async)
print(f"\nFetching display labels for {len(all_loinc_codes)} unique LOINC codes (in parallel)...")
loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=True, max_concurrent=15))

# Create output directory
output_dir = project_root / 'output' / 'valuesets'
output_dir.mkdir(parents=True, exist_ok=True)

# Create a FHIR ValueSet for each primary code
for primary, secondary_codes in primary_to_secondary.items():
    # Get the name for this primary code
    name = primary_to_name.get(primary, f"LOINC {primary}")

    # Create FHIR ValueSet
    valueset = {
        "resourceType": "ValueSet",
        "id": f"interpolar-loinc-{primary.replace('-', '')}",
        "url": f"https://www.medizininformatik-initiative.de/fhir/ext/modul-labor/ValueSet/interpolar-loinc-{primary.replace('-', '')}",
        "version": "3.6",
        "name": f"InterpolarLOINC{primary.replace('-', '')}",
        "title": f"Interpolar LOINC Group: {name}",
        "status": "draft",
        "experimental": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "publisher": "MII INTERPOLAR",
        "description": f"ValueSet containing LOINC primary code {primary} and all quantitatively comparable secondary codes from Interpolar mapping v3.6",
        "compose": {
            "include": [
                {
                    "system": "http://loinc.org",
                    "concept": [
                        {
                            "code": code,
                            "display": loinc_displays.get(code, f"LOINC {code}")
                        }
                        for code in sorted(secondary_codes)
                    ]
                }
            ]
        }
    }

    # Write to file
    output_file = output_dir / f"valueset-interpolar-loinc-{primary.replace('-', '')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(valueset, f, indent=2, ensure_ascii=False)

    print(f"Created {output_file.name} with {len(secondary_codes)} codes")

print(f"\nAll ValueSets created in: {output_dir}")

# Create summary file
summary = {
    "total_primary_codes": len(primary_to_secondary),
    "total_secondary_codes": sum(len(v) for v in primary_to_secondary.values()),
    "primary_codes": {
        primary: {
            "name": primary_to_name.get(primary, ""),
            "secondary_count": len(codes),
            "secondary_codes": sorted(codes)
        }
        for primary, codes in primary_to_secondary.items()
    }
}

summary_file = output_dir / "interpolar_mapping_summary.json"
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"Created summary file: {summary_file}")
