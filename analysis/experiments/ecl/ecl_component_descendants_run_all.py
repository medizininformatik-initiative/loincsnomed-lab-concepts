#!/usr/bin/env python3
r"""
ECL Component Descendants Experiment - Run All Steps
=====================================================
Component-based ECL with descendants: <<Component (should get ~100% recall).
Extracts Component attribute from SNOMED concepts and builds:
<< 363787002 |Observable entity| : 246093002 |Component| = <<[Component_ID]

Expected: Near-perfect recall, very poor precision (includes reticulocytes, etc.)

Dependencies:
- scripts/ecl_permutation_analyzer_simple.py (from project)
- scripts/terminology_server_adapters.py (from project)
"""

import sys
import os
import json
import pandas as pd
import requests
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Set up project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter

# Configuration - Load from environment
LOINC_SNOMED_MAPPING_PATH = os.getenv('loinc_snomed_mapping_path')
SNOMED_TERMINOLOGY_PATH = os.getenv('SNOMED_TERMINOLOGY_PATH')
if SNOMED_TERMINOLOGY_PATH:
    SNOMED_TERMINOLOGY_DIR = Path(SNOMED_TERMINOLOGY_PATH)
    # Find the relationship file dynamically
    relationship_files = list(SNOMED_TERMINOLOGY_DIR.glob('sct2_Relationship_Full_*.txt'))
    RELATIONSHIP_FILE = relationship_files[0] if relationship_files else None
else:
    SNOMED_TERMINOLOGY_DIR = None
    RELATIONSHIP_FILE = None

INPUT_EXCEL = PROJECT_ROOT / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'ecl_component_descendants'
INTERPOLAR_VALUESETS_DIR = PROJECT_ROOT / 'output' / 'valuesets'

# SNOMED relationship IDs
COMPONENT_ATTRIBUTE_ID = "246093002"  # Component attribute

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'valuesets').mkdir(exist_ok=True)

print("="*80)
print("ECL COMPONENT DESCENDANTS EXPERIMENT")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ==============================================================================
# Helper: Load Component Relationships from File
# ==============================================================================
def load_component_relationships(relationship_file):
    """
    Load Component relationships from SNOMED Relationship file.

    Returns:
        dict mapping concept_id -> component_id
    """
    print(f"  Loading relationships from: {relationship_file}")
    component_map = {}

    with open(relationship_file, 'r', encoding='utf-8') as f:
        header = next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 5:
                active = parts[2]
                source_id = parts[4]
                type_id = parts[7]
                destination_id = parts[5]

                # Only active Component relationships
                if active == '1' and type_id == COMPONENT_ATTRIBUTE_ID:
                    component_map[source_id] = destination_id

    print(f"  [OK] Loaded {len(component_map)} Component relationships")
    return component_map

# ==============================================================================
# STEP 1: Load LOINC-SNOMED Mappings
# ==============================================================================
print("\n[STEP 1/5] Loading LOINC-SNOMED mappings...")
if not LOINC_SNOMED_MAPPING_PATH:
    print("ERROR: loinc_snomed_mapping_path not found in environment")
    sys.exit(1)

print(f"  Using: {LOINC_SNOMED_MAPPING_PATH}")
loinc_mappings = load_loinc_mappings(LOINC_SNOMED_MAPPING_PATH)
print(f"  [OK] Loaded {len(loinc_mappings)} LOINC-SNOMED mappings")

# Create reverse mapping: LOINC code → SNOMED concept ID
loinc_to_snomed = {}
for snomed_id, data in loinc_mappings.items():
    loinc_code = data.get('loinc_code')
    if loinc_code:
        loinc_to_snomed[loinc_code] = snomed_id

print(f"  [OK] Created reverse lookup for {len(loinc_to_snomed)} LOINC codes")

# ==============================================================================
# STEP 2: Read Interpolar and Map to SNOMED
# ==============================================================================
print("\n[STEP 2/5] Reading Interpolar mapping and extracting primary codes...")
df = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)
df_quantitative = df[df['COMPARABILITY_TO_LOINC_PRIMARY'] == '1 - quantitativ'].copy()

# Group by primary code
primary_to_secondary = defaultdict(list)
primary_to_snomed = {}
primary_to_name = {}

for _, row in df_quantitative.iterrows():
    loinc = row['LOINC']
    primary = row['LOINC_PRIMARY']
    name = row['GERMAN_NAME_LOINC_PRIMARY']

    if pd.notna(primary):
        if primary not in primary_to_name and pd.notna(name):
            primary_to_name[primary] = name

        if primary in loinc_to_snomed:
            primary_to_snomed[primary] = loinc_to_snomed[primary]

    if pd.notna(loinc) and pd.notna(primary):
        primary_to_secondary[primary].append(loinc)

# Remove duplicates
for primary in primary_to_secondary:
    primary_to_secondary[primary] = list(set(primary_to_secondary[primary]))

print(f"  [OK] Found {len(primary_to_snomed)} primary codes with SNOMED mappings")
print(f"  [OK] Total Interpolar codes: {sum(len(v) for v in primary_to_secondary.values())}")

# ==============================================================================
# STEP 3: Extract Component Attributes from SNOMED
# ==============================================================================
print("\n[STEP 3/5] Extracting Component attributes from SNOMED concepts...")

# Load all component relationships
component_map = load_component_relationships(RELATIONSHIP_FILE)

primary_to_component = {}

for primary_loinc, snomed_id in primary_to_snomed.items():
    if snomed_id in component_map:
        component_id = component_map[snomed_id]
        primary_to_component[primary_loinc] = {
            'component_id': component_id
        }
        print(f"  {primary_loinc} -> Component: {component_id}")
    else:
        print(f"  {primary_loinc} -> No Component found")

print(f"\n  [OK] Extracted Component for {len(primary_to_component)}/{len(primary_to_snomed)} primary codes")

# Save mapping
mapping_output = {
    'timestamp': datetime.now().isoformat(),
    'summary': {
        'total_primary_codes': len(primary_to_snomed),
        'primary_with_component': len(primary_to_component),
        'total_interpolar_codes': sum(len(v) for v in primary_to_secondary.values())
    },
    'mappings': {
        primary: {
            'loinc_code': primary,
            'snomed_concept_id': primary_to_snomed[primary],
            'german_name': primary_to_name.get(primary),
            'component_id': primary_to_component.get(primary, {}).get('component_id'),
            'component_fsn': primary_to_component.get(primary, {}).get('component_fsn'),
            'interpolar_secondary_codes': primary_to_secondary.get(primary, [])
        }
        for primary in primary_to_snomed.keys()
    }
}

with open(OUTPUT_DIR / 'interpolar_loinc_to_snomed_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_output, f, indent=2, ensure_ascii=False)

print(f"  [OK] Saved: interpolar_loinc_to_snomed_mapping.json")

# ==============================================================================
# STEP 4: Execute ECL Queries (Component-Based)
# ==============================================================================
print("\n[STEP 4/5] Executing Component-based ECL queries...")
print("  ECL Strategy: << 363787002 |Observable entity| : 246093002 |Component| = <<[Component_ID]")

# Create terminology server adapter
adapter = create_adapter('loincsnomed')
print(f"  [OK] Connected to LOINCSNOMED Snowstorm")

ecl_results = {}
processed = 0

for primary_loinc, component_info in primary_to_component.items():
    processed += 1
    component_id = component_info['component_id']

    print(f"\n  [{processed}/{len(primary_to_component)}] Processing {primary_loinc}")
    print(f"      Name: {primary_to_name.get(primary_loinc, 'N/A')}")
    print(f"      Component: {component_id}")

    # Build Component-based ECL (Component DESCENDANTS - includes morphological variants)
    ecl = f"<< 363787002 |Observable entity| : 246093002 |Component| = <<{component_id}"
    print(f"      ECL: {ecl}")

    # Execute query
    result = execute_ecl_query(ecl, loinc_mappings, limit=1000, server_adapter=adapter)

    # Extract LOINC codes from results
    ecl_loinc_codes = []
    for concept in result.get('detailed_concepts', []):
        if concept.get('loinc_code'):
            ecl_loinc_codes.append(concept['loinc_code'])

    ecl_loinc_codes = list(set(ecl_loinc_codes))  # Remove duplicates

    print(f"      Result: {result.get('total', 0)} SNOMED concepts, {len(ecl_loinc_codes)} LOINC codes")

    ecl_results[primary_loinc] = {
        'primary_loinc': primary_loinc,
        'snomed_concept_id': primary_to_snomed[primary_loinc],
        'component_id': component_id,
        'ecl_expression': ecl,
        'snomed_concept_count': result.get('total', 0),
        'loinc_codes_found': ecl_loinc_codes,
        'execution_time': result.get('execution_time', 0)
    }

    # Create FHIR ValueSet
    valueset = {
        "resourceType": "ValueSet",
        "id": f"ecl-component-descendants-{primary_loinc.replace('-', '')}",
        "url": f"https://www.medizininformatik-initiative.de/fhir/ext/modul-labor/ValueSet/ecl-component-descendants-{primary_loinc.replace('-', '')}",
        "version": "1.0",
        "name": f"ECLComponentDescendants{primary_loinc.replace('-', '')}",
        "title": f"ECL Component Descendants: {primary_to_name.get(primary_loinc, primary_loinc)}",
        "status": "draft",
        "experimental": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "publisher": "MII INTERPOLAR - ECL Experiment",
        "description": f"ECL-generated ValueSet using Component descendants <<{component_id} for LOINC {primary_loinc}",
        "compose": {
            "include": [
                {
                    "system": "http://loinc.org",
                    "concept": [
                        {"code": code, "display": f"LOINC {code}"}
                        for code in sorted(ecl_loinc_codes)
                    ]
                }
            ]
        }
    }

    vs_file = OUTPUT_DIR / 'valuesets' / f"valueset-ecl-component-descendants-{primary_loinc.replace('-', '')}.json"
    with open(vs_file, 'w', encoding='utf-8') as f:
        json.dump(valueset, f, indent=2, ensure_ascii=False)

# Save summary
with open(OUTPUT_DIR / 'ecl_query_results_summary.json', 'w', encoding='utf-8') as f:
    json.dump(ecl_results, f, indent=2, ensure_ascii=False)

print(f"\n  [OK] Created {len(ecl_results)} ECL-based value sets")
print(f"  [OK] Saved: ecl_query_results_summary.json")

# ==============================================================================
# STEP 5: Compare with Interpolar
# ==============================================================================
print("\n[STEP 5/5] Comparing ECL value sets with Interpolar...")

comparison_results = []

for primary_loinc in primary_to_component.keys():
    interpolar_codes = set(primary_to_secondary.get(primary_loinc, []))
    ecl_codes = set(ecl_results.get(primary_loinc, {}).get('loinc_codes_found', []))

    overlap = interpolar_codes & ecl_codes
    interpolar_only = interpolar_codes - ecl_codes
    ecl_only = ecl_codes - interpolar_codes

    precision = len(overlap) / len(ecl_codes) if ecl_codes else 0
    recall = len(overlap) / len(interpolar_codes) if interpolar_codes else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    comparison_results.append({
        'primary_loinc': primary_loinc,
        'german_name': primary_to_name.get(primary_loinc),
        'component_id': ecl_results.get(primary_loinc, {}).get('component_id'),
        'interpolar_count': len(interpolar_codes),
        'ecl_count': len(ecl_codes),
        'overlap_count': len(overlap),
        'interpolar_only_count': len(interpolar_only),
        'ecl_only_count': len(ecl_only),
        'precision': round(precision, 3),
        'recall': round(recall, 3),
        'f1_score': round(f1, 3),
        'interpolar_codes': sorted(list(interpolar_codes)),
        'ecl_codes': sorted(list(ecl_codes)),
        'overlap_codes': sorted(list(overlap)),
        'interpolar_only_codes': sorted(list(interpolar_only)),
        'ecl_only_codes': sorted(list(ecl_only))
    })

# Save detailed comparison
with open(OUTPUT_DIR / 'comparison_interpolar_vs_ecl.json', 'w', encoding='utf-8') as f:
    json.dump(comparison_results, f, indent=2, ensure_ascii=False)

# Create summary CSV
df_comparison = pd.DataFrame([
    {
        'Primary LOINC': r['primary_loinc'],
        'German Name': r['german_name'],
        'Component ID': r['component_id'],
        'Interpolar Count': r['interpolar_count'],
        'ECL Count': r['ecl_count'],
        'Overlap': r['overlap_count'],
        'Precision': r['precision'],
        'Recall': r['recall'],
        'F1 Score': r['f1_score']
    }
    for r in comparison_results
])

df_comparison.to_csv(OUTPUT_DIR / 'comparison_summary.csv', index=False)

# Print summary statistics
avg_precision = df_comparison['Precision'].mean()
avg_recall = df_comparison['Recall'].mean()
avg_f1 = df_comparison['F1 Score'].mean()

print(f"\n  [OK] Comparison complete for {len(comparison_results)} primary codes")
print(f"\n  Summary Statistics:")
print(f"    Average Precision: {avg_precision:.3f}")
print(f"    Average Recall:    {avg_recall:.3f}")
print(f"    Average F1 Score:  {avg_f1:.3f}")

# ==============================================================================
# COMPLETE
# ==============================================================================
print("\n" + "="*80)
print("EXPERIMENT COMPLETE!")
print("="*80)
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nOutput directory: {OUTPUT_DIR}")
print(f"  - interpolar_loinc_to_snomed_mapping.json")
print(f"  - ecl_query_results_summary.json")
print(f"  - comparison_interpolar_vs_ecl.json")
print(f"  - comparison_summary.csv")
print(f"  - valuesets/ ({len(ecl_results)} files)")
