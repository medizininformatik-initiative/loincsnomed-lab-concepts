#!/usr/bin/env python3
"""
Interactive ECL Builder
=======================
Extracts all SNOMED relationships for a LOINC code and lets you:
1. See all available attributes
2. Select which attributes to use for ECL
3. Choose fixed vs descendants for each attribute
4. Generate all permutations and run queries
"""

import sys
import csv
import json
import itertools
import os
from pathlib import Path

# Add scripts directory to path to import local modules
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from ecl_permutation_analyzer_simple import (
    load_loinc_mappings,
    execute_ecl_query
)
from terminology_server_adapters import create_adapter


# Common SNOMED relationship types
RELATIONSHIP_TYPES = {
    '116680003': 'IS-A',
    '246093002': 'Component',
    '704327008': 'Direct site',
    '704319004': 'Inheres in',
    '370130000': 'Property',
    '370132008': 'Time aspect',
    '370134009': 'Scale type',
    '246501002': 'Technique',
    '704318007': 'Property type',
    '370135005': 'Identifier',
}


def get_concept_name(concept_id: str, description_file: str) -> str:
    """Get preferred term for a concept."""
    with open(description_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['conceptId'] == concept_id and row['active'] == '1':
                # Prefer Fully Specified Name (FSN)
                if row['typeId'] == '900000000000003001':
                    return row['term']
    return f"Concept {concept_id}"


def extract_all_relationships(concept_id: str, relationship_file: str, description_file: str) -> dict:
    """
    Extract ALL relationships for a concept.

    Returns:
        Dictionary mapping relationship type ID -> {name, destination_id, destination_name}
    """
    relationships = {}

    with open(relationship_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['sourceId'] == concept_id and row['active'] == '1':
                type_id = row['typeId']

                # Skip IS-A relationships
                if type_id == '116680003':
                    continue

                dest_id = row['destinationId']
                dest_name = get_concept_name(dest_id, description_file)
                type_name = RELATIONSHIP_TYPES.get(type_id, f'Type {type_id}')

                relationships[type_id] = {
                    'type_name': type_name,
                    'destination_id': dest_id,
                    'destination_name': dest_name
                }

    return relationships


def build_ecl_from_attributes(attributes: list) -> str:
    """
    Build ECL query from selected attributes with concept names.

    Args:
        attributes: List of dicts with {type_id, type_name, dest_id, dest_name, use_descendants}

    Returns:
        ECL expression string
    """
    constraints = []

    for attr in attributes:
        type_id = attr['type_id']
        type_name = attr['type_name']
        dest_id = attr['dest_id']
        dest_name = attr['dest_name']
        use_descendants = attr['use_descendants']

        prefix = '<<' if use_descendants else ''
        constraints.append(f"<<{type_id} |{type_name}| = {prefix}{dest_id} |{dest_name}|")

    ecl = f"<< 363787002 |Observable entity| : {', '.join(constraints)}"
    return ecl


def generate_permutations(selected_attrs: list) -> list:
    """
    Generate all permutations (fixed vs descendants for each attribute).

    Args:
        selected_attrs: List of dicts with {type_id, type_name, dest_id, dest_name}

    Returns:
        List of permutation configs
    """
    n_attrs = len(selected_attrs)

    # Generate all combinations of True/False for descendants
    permutations = []
    for combination in itertools.product([False, True], repeat=n_attrs):
        attrs_config = []
        for i, attr in enumerate(selected_attrs):
            attrs_config.append({
                'type_id': attr['type_id'],
                'type_name': attr['type_name'],
                'dest_id': attr['dest_id'],
                'dest_name': attr['dest_name'],
                'use_descendants': combination[i]
            })

        permutations.append({
            'attributes': attrs_config,
            'description': ' | '.join([
                f"{a['type_name']}={'Desc' if a['use_descendants'] else 'Fixed'}"
                for a in attrs_config
            ])
        })

    return permutations


def interactive_builder(loinc_code: str, base_path: str, server_type='loincsnomed', server_config=None):
    """
    Main interactive builder function.

    Args:
        loinc_code: LOINC code to analyze
        base_path: Path to SNOMED terminology files
        server_type: 'loincsnomed' or 'ontoserver'
        server_config: Dict with server-specific config (e.g., {'base_url': '...', 'code_system_url': '...'})
    """
    if server_config is None:
        server_config = {}

    # Create server adapter
    server_adapter = create_adapter(server_type, **server_config)

    # Setup file paths
    identifier_file = base_path + "/sct2_Identifier_Snapshot_LO1010000_20250921.txt"
    description_file = base_path + "/sct2_Description_Snapshot-en_LO1010000_20250921.txt"
    relationship_file = base_path + "/sct2_Relationship_Snapshot_LO1010000_20250921.txt"

    print("=" * 80)
    print(f"INTERACTIVE ECL BUILDER FOR LOINC {loinc_code}")
    print(f"Server: {server_type}")
    print("=" * 80)

    # Step 1: Load mappings and find concept
    print("\nLoading LOINC mappings...")
    loinc_mappings = load_loinc_mappings(identifier_file, description_file)

    concept_id = None
    for cid, data in loinc_mappings.items():
        if data.get('loinc_code') == loinc_code:
            concept_id = cid
            break

    if not concept_id:
        print(f"ERROR: LOINC code {loinc_code} not found")
        return

    concept_name = get_concept_name(concept_id, description_file)
    print(f"\nFound: {concept_name}")
    print(f"SNOMED Concept ID: {concept_id}")

    # Step 2: Extract all relationships
    print("\nExtracting all relationships...")
    relationships = extract_all_relationships(concept_id, relationship_file, description_file)

    print(f"\nFound {len(relationships)} relationship types:")
    print("-" * 80)

    rel_list = []
    for i, (type_id, rel) in enumerate(relationships.items(), 1):
        print(f"{i}. {rel['type_name']} ({type_id})")
        print(f"   -> {rel['destination_name']} ({rel['destination_id']})")
        rel_list.append({
            'index': i,
            'type_id': type_id,
            'type_name': rel['type_name'],
            'dest_id': rel['destination_id'],
            'dest_name': rel['destination_name']
        })

    # Step 3: User selects attributes
    print("\n" + "=" * 80)
    print("SELECT ATTRIBUTES FOR ECL QUERY")
    print("=" * 80)
    print("Enter the numbers of attributes to use (comma-separated, e.g., 1,3,4)")
    print("Or press Enter to use all non-technical attributes")

    user_input = input("\nYour selection: ").strip()

    if user_input:
        selected_indices = [int(x.strip()) for x in user_input.split(',')]
        selected_attrs = [rel_list[i-1] for i in selected_indices]
    else:
        # Auto-select: exclude Time aspect, Scale type, Technique
        exclude_types = {'370132008', '370134009', '246501002'}
        selected_attrs = [r for r in rel_list if r['type_id'] not in exclude_types]

    print(f"\nSelected {len(selected_attrs)} attributes:")
    for attr in selected_attrs:
        print(f"  - {attr['type_name']}: {attr['dest_name']}")

    # Step 4: Generate permutations
    print(f"\nGenerating {2**len(selected_attrs)} permutations...")
    permutations = generate_permutations(selected_attrs)

    print(f"\nPermutations to execute:")
    for i, perm in enumerate(permutations, 1):
        print(f"  {i}. {perm['description']}")

    # Step 5: Execute queries
    print("\n" + "=" * 80)
    print("EXECUTING ECL QUERIES")
    print("=" * 80)

    results = []
    for i, perm in enumerate(permutations, 1):
        ecl = build_ecl_from_attributes(perm['attributes'])

        print(f"\nPermutation {i}: {perm['description']}")
        print(f"  ECL: {ecl}")
        print(f"  Executing query...")

        result = execute_ecl_query(ecl, loinc_mappings=loinc_mappings, server_adapter=server_adapter)
        enriched = result.get('detailed_concepts', [])
        print(f"  Result: {len(enriched)} concepts")

        results.append({
            'permutation': perm['description'],
            'ecl': ecl,
            'attributes': perm['attributes'],
            'concepts': enriched,
            'count': len(enriched)
        })

    # Step 6: Save results
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['permutation']}: {result['count']} concepts")

    # Save JSON results
    output_prefix = f"ecl_results/{loinc_code.replace('-', '_')}_interactive"
    output_file = output_prefix + "_results.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'loinc_code': loinc_code,
            'concept_id': concept_id,
            'concept_name': concept_name,
            'selected_attributes': selected_attrs,
            'results': results
        }, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    # Save CSV with all concepts from all permutations
    csv_file = output_prefix + "_concepts.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Permutation_Number',
            'Permutation',
            'Concept_ID',
            'FSN',
            'LOINC_Code',
            'LOINC_Label'
        ])

        # Write all concepts from each permutation
        for i, result in enumerate(results, 1):
            perm_name = result['permutation']
            for concept in result['concepts']:
                writer.writerow([
                    i,
                    perm_name,
                    concept['concept_id'],
                    concept['fsn'],
                    concept.get('loinc_code', ''),
                    concept.get('loinc_label', '')
                ])

    print(f"CSV saved to: {csv_file}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interactive_ecl_builder.py <LOINC_CODE> [BASE_PATH]")
        print("Example: python interactive_ecl_builder.py 787-2")
        print("\nBASE_PATH: Path to SNOMED terminology files (optional, reads from env if not provided)")
        sys.exit(1)

    loinc_code = sys.argv[1]

    # Get base path from command line or environment variable
    if len(sys.argv) > 2:
        base_path = sys.argv[2]
    else:
        # Try to get from environment variable
        base_path = os.getenv('SNOMED_TERMINOLOGY_PATH')
        if not base_path:
            print("ERROR: No terminology path provided!")
            print("Either:")
            print("  1. Pass as argument: python interactive_ecl_builder.py 787-2 /path/to/snomed/")
            print("  2. Set environment variable: export SNOMED_TERMINOLOGY_PATH=/path/to/snomed/")
            print("  3. Add to .env file: SNOMED_TERMINOLOGY_PATH=/path/to/snomed/")
            sys.exit(1)

    interactive_builder(loinc_code, base_path)