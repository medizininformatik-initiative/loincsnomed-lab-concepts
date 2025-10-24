#!/usr/bin/env python3
"""
LOINC Concept Analyzer
======================
Runs comprehensive ECL analysis for any LOINC concept (not limited to CBC/blood components).

This script:
1. Loads LOINC-SNOMED mappings
2. Extracts SNOMED attributes (Component, Property, Direct site, Time aspect, etc.)
3. Runs ALL ECL experiment approaches:
   - ECL Descendants Baseline
   - ECL Fixed Component
   - ECL Component Descendants
   - ECL Fixed Component Property
   - ECL Fixed Component System
4. Runs refined queries with custom exclusions (e.g., Excl Cord Blood, Excl Plasma, Excl Urine)
5. Compares with Interpolar reference
6. Generates comprehensive comparison CSV and JSON report

Usage:
    python cbc_component_analyzer.py <primary_loinc_code> <output_name> [--exclude-specimens <specimen_sctids>]

Examples:
    python cbc_component_analyzer.py 26453-1 erythrocytes
    python cbc_component_analyzer.py 26515-7 platelets --exclude-specimens 119361006
    python cbc_component_analyzer.py 2160-0 creatinine --exclude-specimens "122575003,122556008"

Specimen exclusion examples:
    - 122556008: Cord blood specimen
    - 119361006: Plasma specimen
    - 122575003: Urine specimen
"""

import sys
import os
import json
import asyncio
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Add local scripts to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'scripts'))
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter
from loinc_display_fetcher import fetch_displays_async

# Configuration
LOINC_SNOMED_MAPPING_PATH = os.getenv('loinc_snomed_mapping_path')
SNOMED_TERMINOLOGY_PATH = os.getenv('SNOMED_TERMINOLOGY_PATH')
if not SNOMED_TERMINOLOGY_PATH:
    print("ERROR: SNOMED_TERMINOLOGY_PATH not set in .env")
    print("Please add: SNOMED_TERMINOLOGY_PATH=/path/to/snomed/Snapshot/Terminology")
    sys.exit(1)
SNOMED_TERMINOLOGY_DIR = Path(SNOMED_TERMINOLOGY_PATH)
RELATIONSHIP_FILE = SNOMED_TERMINOLOGY_DIR / 'sct2_Relationship_Snapshot_LO1010000_20250921.txt'
INPUT_EXCEL = project_root / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
TOP300_XLSX = project_root / 'input' / 'Top300 Stand 2018-08-08.xlsx'

# SNOMED attribute IDs
COMPONENT_ATTRIBUTE_ID = "246093002"
PROPERTY_ATTRIBUTE_ID = "370130000"
DIRECT_SITE_ATTRIBUTE_ID = "704327008"

# Universal quantitative measurement property (parent of all mass/molar concentration types)
MEASUREMENT_PROPERTY_SCTID = "685451010000100"
MEASUREMENT_PROPERTY_LABEL = "Measurement property (qualifier value)"

def load_snomed_attributes(relationship_file, concept_id):
    """
    Extract Component, Property, and Direct site attributes for a SNOMED concept.

    Returns:
        dict with 'component', 'property', 'direct_site' keys
    """
    attributes = {}

    with open(relationship_file, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 5:
                active = parts[2]
                source_id = parts[4]
                type_id = parts[7]
                destination_id = parts[5]

                if active == '1' and source_id == concept_id:
                    if type_id == COMPONENT_ATTRIBUTE_ID:
                        attributes['component'] = destination_id
                    elif type_id == PROPERTY_ATTRIBUTE_ID:
                        attributes['property'] = destination_id
                    elif type_id == DIRECT_SITE_ATTRIBUTE_ID:
                        attributes['direct_site'] = destination_id

    return attributes

def run_ecl_experiment(ecl_name, ecl_expression, loinc_mappings, adapter):
    """
    Execute a single ECL query experiment.

    Returns:
        dict with 'loinc_codes', 'snomed_concept_count', 'execution_time'
    """
    print(f"    ECL: {ecl_expression}")
    result = execute_ecl_query(ecl_expression, loinc_mappings, limit=1000, server_adapter=adapter)

    # Extract LOINC codes
    loinc_codes = []
    for concept in result.get('detailed_concepts', []):
        if concept.get('loinc_code'):
            loinc_codes.append(concept['loinc_code'])

    loinc_codes = list(set(loinc_codes))

    print(f"    Result: {result.get('total', 0)} SNOMED concepts, {len(loinc_codes)} LOINC codes")

    return {
        'ecl_expression': ecl_expression,
        'loinc_codes': loinc_codes,
        'snomed_concept_count': result.get('total', 0),
        'execution_time': result.get('execution_time', 0)
    }

def analyze_cbc_component(primary_loinc, component_name, exclude_specimens=None):
    """
    Run comprehensive ECL analysis for any LOINC concept.

    Args:
        primary_loinc: Primary LOINC code
        component_name: Output directory name
        exclude_specimens: List of SNOMED specimen concept IDs to exclude (e.g., ['122556008', '119361006'])
    """
    if exclude_specimens is None:
        exclude_specimens = []

    print("=" * 80)
    print(f"LOINC CONCEPT ANALYZER: {component_name.upper()}")
    print("=" * 80)
    print(f"Primary LOINC: {primary_loinc}")
    if exclude_specimens:
        print(f"Excluding specimens: {', '.join(exclude_specimens)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Setup output directory - more generic naming
    output_dir = project_root / 'output' / 'singular_concepts' / component_name.lower()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load LOINC-SNOMED mappings
    print("[STEP 1/7] Loading LOINC-SNOMED mappings...")
    if not LOINC_SNOMED_MAPPING_PATH:
        print("ERROR: loinc_snomed_mapping_path not found in environment")
        sys.exit(1)

    loinc_mappings = load_loinc_mappings(LOINC_SNOMED_MAPPING_PATH)
    print(f"  [OK] Loaded {len(loinc_mappings)} mappings")

    # Get SNOMED concept ID for primary LOINC
    loinc_to_snomed = {data['loinc_code']: sctid for sctid, data in loinc_mappings.items() if data.get('loinc_code')}

    if primary_loinc not in loinc_to_snomed:
        print(f"ERROR: Primary LOINC {primary_loinc} not found in SNOMED mappings")
        sys.exit(1)

    snomed_concept_id = loinc_to_snomed[primary_loinc]
    print(f"  SNOMED Concept ID: {snomed_concept_id}")

    # Extract SNOMED attributes
    print("\n[STEP 2/7] Extracting SNOMED attributes...")
    attributes = load_snomed_attributes(RELATIONSHIP_FILE, snomed_concept_id)
    print(f"  Component: {attributes.get('component', 'N/A')}")
    print(f"  Property: {attributes.get('property', 'N/A')}")
    print(f"  Direct site: {attributes.get('direct_site', 'N/A')}")

    if not attributes.get('component'):
        print("  WARNING: No Component attribute found - trying pre-coordinated descendants approach")

    # Load Interpolar reference data
    print("\n[STEP 3/7] Loading Interpolar reference data...")
    df_interpolar = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)
    df_quant = df_interpolar[df_interpolar['COMPARABILITY_TO_LOINC_PRIMARY'] == '1 - quantitativ'].copy()

    interpolar_codes = set(df_quant[df_quant['LOINC_PRIMARY'] == primary_loinc]['LOINC'].dropna().unique())
    interpolar_codes.add(primary_loinc)  # Include primary itself
    print(f"  [OK] Found {len(interpolar_codes)} Interpolar codes for {primary_loinc}")

    # Load LOINC300 data
    df_top300 = pd.read_excel(TOP300_XLSX)
    loinc300_codes = set(df_top300['primär'].dropna().unique()) | set(df_top300['sekundär'].dropna().unique())
    print(f"  [OK] Loaded {len(loinc300_codes)} LOINC300 codes")

    # Connect to terminology server
    print("\n[STEP 4/7] Connecting to terminology server...")
    adapter = create_adapter('loincsnomed')
    print("  [OK] Connected to LOINCSNOMED Snowstorm")

    # Run ECL experiments
    print(f"\n[STEP 5/7] Running ECL experiments...")
    ecl_results = {}

    # 1. ECL Descendants Baseline (if has Component attribute)
    if attributes.get('component'):
        print("\n  [1/7] ECL Descendants Baseline (<< Component)")
        ecl_results['ecl_descendants_baseline'] = run_ecl_experiment(
            'ecl_descendants_baseline',
            f"<< {attributes['component']}",
            loinc_mappings,
            adapter
        )

    # 2. ECL Fixed Component (if has Component attribute)
    if attributes.get('component'):
        print("\n  [2/7] ECL Fixed Component")
        ecl_results['ecl_fixed_component'] = run_ecl_experiment(
            'ecl_fixed_component',
            f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']}",
            loinc_mappings,
            adapter
        )

    # 3. ECL Component Descendants (if has Component attribute)
    if attributes.get('component'):
        print("\n  [3/7] ECL Component Descendants")
        ecl_results['ecl_component_descendants'] = run_ecl_experiment(
            'ecl_component_descendants',
            f"<< 363787002 |Observable entity| : 246093002 |Component| = << {attributes['component']}",
            loinc_mappings,
            adapter
        )

    # 4. ECL Fixed Component Property (if has both)
    if attributes.get('component') and attributes.get('property'):
        print("\n  [4/7] ECL Fixed Component Property")
        ecl_results['ecl_fixed_component_property'] = run_ecl_experiment(
            'ecl_fixed_component_property',
            f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']}, 370130000 |Property| = {attributes['property']}",
            loinc_mappings,
            adapter
        )

    # 5. ECL Fixed Component System (if has component and direct site)
    if attributes.get('component') and attributes.get('direct_site'):
        print("\n  [5/7] ECL Fixed Component System")
        ecl_results['ecl_fixed_component_system'] = run_ecl_experiment(
            'ecl_fixed_component_system',
            f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']}, 704327008 |Direct site| = << {attributes['direct_site']}",
            loinc_mappings,
            adapter
        )

    # 6. Refined Query: With specimen exclusions (if has all three attributes)
    # Uses universal Measurement property to capture all quantitative variations
    if attributes.get('component') and attributes.get('property') and attributes.get('direct_site'):
        if exclude_specimens:
            exclusion_desc = f" (excluding {len(exclude_specimens)} specimen type(s))"
            print(f"\n  [6/7] Refined ECL: With Exclusions{exclusion_desc}")
        else:
            print("\n  [6/7] Refined ECL: Base (no exclusions)")

        excl_ecl = f"""<< 363787002 |Observable entity| :
    246093002 |Component| = {attributes['component']},
    370130000 |Property| = << {MEASUREMENT_PROPERTY_SCTID} |{MEASUREMENT_PROPERTY_LABEL}|,
    704327008 |Direct site| = << {attributes['direct_site']}"""

        # Add exclusions
        for specimen_id in exclude_specimens:
            excl_ecl += f",\n    704327008 |Direct site| != << {specimen_id}"

        ecl_results['refined_with_exclusions'] = run_ecl_experiment(
            'refined_with_exclusions',
            excl_ecl,
            loinc_mappings,
            adapter
        )

    # 7. Refined Query: Base (no exclusions) - always run for comparison
    # Uses universal Measurement property to capture all quantitative variations
    if attributes.get('component') and attributes.get('property') and attributes.get('direct_site'):
        print("\n  [7/7] Refined ECL: Full (no exclusions, for comparison)")
        base_ecl = f"""<< 363787002 |Observable entity| :
    246093002 |Component| = {attributes['component']},
    370130000 |Property| = << {MEASUREMENT_PROPERTY_SCTID} |{MEASUREMENT_PROPERTY_LABEL}|,
    704327008 |Direct site| = << {attributes['direct_site']}"""

        ecl_results['refined_base'] = run_ecl_experiment(
            'refined_base',
            base_ecl,
            loinc_mappings,
            adapter
        )

    # 8. Pre-coordinated Descendants (fallback for calculated indices)
    if not attributes.get('component'):
        print("\n  [1/1] Pre-coordinated Descendants")
        ecl_results['precoord_descendants'] = run_ecl_experiment(
            'precoord_descendants',
            f"<< {snomed_concept_id}",
            loinc_mappings,
            adapter
        )

    # Collect all LOINC codes found across all experiments
    print("\n[STEP 6/7] Collecting and analyzing results...")
    all_loinc_codes = set()
    for exp_name, exp_data in ecl_results.items():
        all_loinc_codes.update(exp_data['loinc_codes'])

    print(f"  Total unique LOINC codes found: {len(all_loinc_codes)}")

    # Fetch LOINC display names
    print(f"  Fetching display names for {len(all_loinc_codes)} LOINC codes...")
    loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False, max_concurrent=15))

    # Determine refined query approach (Component + Property + Direct site)
    # This is the most specific technical definition, not a quality judgment
    refined_approach = None
    if 'refined_with_exclusions' in ecl_results:
        refined_approach = 'refined_with_exclusions'
    elif 'refined_base' in ecl_results:
        refined_approach = 'refined_base'
    elif 'precoord_descendants' in ecl_results:
        # For pre-coordinated concepts (like MCV/MCH/MCHC)
        refined_approach = 'precoord_descendants'

    if refined_approach:
        refined_codes = ecl_results[refined_approach]['loinc_codes']
        print(f"\n  Refined query approach: {refined_approach} ({len(refined_codes)} codes)")

    # Build comprehensive comparison table
    comparison_rows = []

    for loinc_code in sorted(all_loinc_codes):
        row = {
            'LOINC_Code': loinc_code,
            'LOINC_Display': loinc_displays.get(loinc_code, f'LOINC {loinc_code}'),
            'Is_Primary': 'Yes' if loinc_code == primary_loinc else '',
            'In_Interpolar': 'Yes' if loinc_code in interpolar_codes else '',
            'In_LOINC300': 'Yes' if loinc_code in loinc300_codes else ''
        }

        # Add presence in each ECL experiment
        for exp_name, exp_data in ecl_results.items():
            row[f'{exp_name}_Present'] = 'Yes' if loinc_code in exp_data['loinc_codes'] else ''

        # Add "Refined_Query" flag for codes found by most specific query
        # This is a technical designation (Component + Property + Direct site), not a clinical judgment
        if refined_approach and loinc_code in ecl_results[refined_approach]['loinc_codes']:
            row['Refined_Query'] = 'Yes'
        else:
            row['Refined_Query'] = ''

        # Count how many approaches found this code
        approach_count = sum(1 for key, val in row.items() if key.endswith('_Present') and val == 'Yes')
        if row['In_Interpolar'] == 'Yes':
            approach_count += 1
        row['Approach_Count'] = approach_count

        comparison_rows.append(row)

    df_comparison = pd.DataFrame(comparison_rows)
    df_comparison = df_comparison.sort_values(['Approach_Count', 'LOINC_Code'], ascending=[False, True])

    # Save comparison CSV
    comparison_csv = output_dir / f'{component_name.lower()}_ecl_comparison.csv'
    df_comparison.to_csv(comparison_csv, index=False)
    print(f"  [OK] Saved: {comparison_csv}")

    # Save detailed results JSON
    results_json = {
        'timestamp': datetime.now().isoformat(),
        'primary_loinc': primary_loinc,
        'component_name': component_name,
        'snomed_concept_id': snomed_concept_id,
        'attributes': attributes,
        'experiments': ecl_results,
        'summary': {
            'total_loinc_codes': len(all_loinc_codes),
            'interpolar_codes': len(interpolar_codes),
            'loinc300_codes': len([c for c in all_loinc_codes if c in loinc300_codes])
        }
    }

    results_json_file = output_dir / f'{component_name.lower()}_ecl_results.json'
    with open(results_json_file, 'w', encoding='utf-8') as f:
        json.dump(results_json, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Saved: {results_json_file}")

    # Calculate statistics vs Interpolar
    print("\n[STEP 7/7] Calculating statistics vs Interpolar...")

    for exp_name, exp_data in ecl_results.items():
        exp_codes = set(exp_data['loinc_codes'])
        overlap = exp_codes & interpolar_codes

        precision = len(overlap) / len(exp_codes) if exp_codes else 0
        recall = len(overlap) / len(interpolar_codes) if interpolar_codes else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        print(f"\n  {exp_name}:")
        print(f"    Codes: {len(exp_codes)}")
        print(f"    Precision: {precision:.3f}")
        print(f"    Recall: {recall:.3f}")
        print(f"    F1: {f1:.3f}")

    # Complete
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nOutput directory: {output_dir}")
    print(f"  - {comparison_csv.name}")
    print(f"  - {results_json_file.name}")

    return output_dir, df_comparison

def main():
    parser = argparse.ArgumentParser(
        description='Analyze any LOINC concept using comprehensive ECL experiments',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Erythrocytes (no exclusions)
  python cbc_component_analyzer.py 26453-1 erythrocytes

  # Platelets (exclude plasma)
  python cbc_component_analyzer.py 26515-7 platelets --exclude-specimens 119361006

  # Creatinine (exclude urine and cord blood)
  python cbc_component_analyzer.py 2160-0 creatinine --exclude-specimens "122575003,122556008"

Common specimen SNOMED IDs:
  122556008 - Cord blood specimen
  119361006 - Plasma specimen
  122575003 - Urine specimen
  119342007 - Saliva specimen
  119339001 - Stool specimen
        """
    )
    parser.add_argument('primary_loinc', help='Primary LOINC code')
    parser.add_argument('output_name', help='Output directory name (e.g., erythrocytes, platelets, creatinine)')
    parser.add_argument('--exclude-specimens',
                        help='Comma-separated list of SNOMED specimen concept IDs to exclude',
                        default='')

    args = parser.parse_args()

    # Parse specimen exclusions
    exclude_specimens = []
    if args.exclude_specimens:
        exclude_specimens = [s.strip() for s in args.exclude_specimens.split(',') if s.strip()]

    analyze_cbc_component(args.primary_loinc, args.output_name, exclude_specimens)

if __name__ == '__main__':
    main()
