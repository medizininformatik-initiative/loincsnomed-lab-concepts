#!/usr/bin/env python3
"""
ECL Permutation Analyzer for LOINC-SNOMED (Python 2.7+ compatible)
====================================================================
Simplified version without dataclasses for older Python versions.

ARCHITECTURE OVERVIEW:
======================
HYBRID APPROACH: Local Files + Public API

Step 1: LOINC → SNOMED (local file)
Step 2: Extract attributes (local file)
Step 3: Build ECL queries (local)
Step 4: Execute ECL (API)
Step 5: Compare results (local)
"""

import requests
import json
import time
import csv
from terminology_server_adapters import create_adapter

# Configuration - can be overridden via command line or config file
DEFAULT_SERVER_TYPE = "loincsnomed"  # or "ontoserver"
DEFAULT_SERVER_CONFIG = {}  # Empty for loincsnomed defaults

def get_concept_details(concept_id):
    """
    Get full concept details including descriptions and identifiers.

    Args:
        concept_id: SNOMED concept ID

    Returns:
        dict with FSN, PT, and LOINC code if available
    """
    url = "{}/{}/concepts/{}".format(API_BASE, BRANCH, concept_id)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Extract FSN
            fsn = None
            for desc in data.get('descriptions', []):
                if desc.get('type', {}).get('conceptId') == '900000000000003001':  # FSN type
                    fsn = desc.get('term')
                    break

            return {
                'concept_id': concept_id,
                'fsn': fsn or data.get('fsn', {}).get('term', 'Unknown'),
                'pt': data.get('pt', {}).get('term', 'Unknown')
            }
        else:
            return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}
    except Exception as e:
        print("    Warning: Could not get details for {}: {}".format(concept_id, str(e)))
        return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}


def load_loinc_mappings(identifier_file, description_file=None):
    """
    Load LOINC mappings into memory for fast lookup.

    Args:
        identifier_file: Path to sct2_Identifier_Snapshot_*.txt
        description_file: Path to sct2_Description_Snapshot_*.txt (optional)

    Returns:
        dict mapping concept_id to {'loinc_code': str, 'loinc_label': str}
    """
    mappings = {}

    # Load LOINC codes from identifier file
    try:
        with open(identifier_file, 'r') as f:
            next(f)  # Skip header
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 6 and parts[2] == '1':  # Active only
                    concept_id = parts[5]
                    loinc_code = parts[0]
                    mappings[concept_id] = {'loinc_code': loinc_code, 'loinc_label': None}
    except Exception as e:
        print("Warning: Could not read identifier file: {}".format(str(e)))

    # Load LOINC labels from description file
    if description_file:
        try:
            with open(description_file, 'r') as f:
                next(f)  # Skip header
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 9 and parts[2] == '1':  # Active
                        concept_id = parts[4]
                        type_id = parts[6]  # FSN=900000000000003001, PT=900000000000013009
                        term = parts[7]

                        if concept_id in mappings and type_id == '900000000000013009':  # Synonym/PT
                            current_label = mappings[concept_id]['loinc_label']

                            # Priority 1: LOINC long common name with brackets (preferred)
                            if '[' in term and ']' in term and '(observable entity)' not in term:
                                if not current_label or '[' not in current_label:
                                    mappings[concept_id]['loinc_label'] = term

                            # Priority 2: Human-readable format without technical suffixes
                            elif (not current_label and
                                  '(observable entity)' not in term and
                                  ':' not in term):  # Exclude LOINC short format
                                mappings[concept_id]['loinc_label'] = term
        except Exception as e:
            print("Warning: Could not read description file: {}".format(str(e)))

    return mappings


def execute_ecl_query(ecl_expression, loinc_mappings=None, limit=1000, server_adapter=None):
    """
    Execute ECL query against SNOMED API and enrich with details.

    Args:
        ecl_expression: ECL query string
        loinc_mappings: Pre-loaded dict mapping concept_id to LOINC data
        limit: Max results
        server_adapter: TerminologyServerAdapter instance (if None, creates default)

    Returns:
        dict with 'total', 'items', 'execution_time', 'detailed_concepts'
    """
    if server_adapter is None:
        server_adapter = create_adapter(DEFAULT_SERVER_TYPE, **DEFAULT_SERVER_CONFIG)

    print("  Executing query...")

    result = server_adapter.execute_ecl_query(ecl_expression, limit=limit)

    if result.get('items'):
        # Enrich with FSN and LOINC codes
        print("  Enriching {} concepts with FSN and LOINC codes...".format(len(result.get('items', []))))
        detailed_concepts = []

        for i, item in enumerate(result.get('items', [])):
            concept_id = item['conceptId']

            # Get FSN (from item if available, else fetch)
            fsn = item.get('fsn', {}).get('term', 'Unknown')
            pt = item.get('pt', {}).get('term', 'Unknown')

            # Get LOINC code and label from pre-loaded mappings
            loinc_code = None
            loinc_label = None
            if loinc_mappings and concept_id in loinc_mappings:
                loinc_code = loinc_mappings[concept_id]['loinc_code']
                loinc_label = loinc_mappings[concept_id]['loinc_label']

            detailed_concepts.append({
                'concept_id': concept_id,
                'fsn': fsn,
                'pt': pt,
                'loinc_code': loinc_code,
                'loinc_label': loinc_label
            })

            # Progress indicator for large sets
            if (i + 1) % 50 == 0:
                print("    Processed {}/{}...".format(i + 1, len(result.get('items', []))))

        result['detailed_concepts'] = detailed_concepts

    return result


def build_ecl_query(component_id, direct_site_id,
                   component_descendants=False, site_descendants=False,
                   exclude_components=None, exclude_sites=None,
                   require_time_aspect=None, require_scale_type=None,
                   method_constraint=None):
    """
    Build ECL query with permutations and custom constraints.

    Args:
        component_id: Component SNOMED ID
        direct_site_id: Direct site SNOMED ID
        component_descendants: Use << for component
        site_descendants: Use << for site
        exclude_components: List of component IDs to exclude (e.g., reticulocytes)
        exclude_sites: List of site IDs to exclude (e.g., cord blood)
        require_time_aspect: SNOMED ID for time aspect (e.g., 123029007 for point-in-time)
        require_scale_type: SNOMED ID for scale type (e.g., 30766002 for quantitative)
        method_constraint: SNOMED ID for method constraint

    Returns:
        ECL expression string
    """
    comp_prefix = "<<" if component_descendants else ""
    site_prefix = "<<" if site_descendants else ""

    # Base query
    ecl = ("<< 363787002 |Observable entity| : "
           "<<246093002 |Component| = {comp_prefix}{component_id}, "
           "<<704327008 |Direct site| = {site_prefix}{direct_site_id}").format(
               comp_prefix=comp_prefix,
               component_id=component_id,
               site_prefix=site_prefix,
               direct_site_id=direct_site_id
           )

    # Add optional constraints
    if require_time_aspect:
        ecl += ", <<370132008 |Time aspect| = {}".format(require_time_aspect)

    if require_scale_type:
        ecl += ", <<370134009 |Scale type| = {}".format(require_scale_type)

    if method_constraint:
        ecl += ", <<370130000 |Property| = {}".format(method_constraint)

    # Handle exclusions with MINUS operator
    if exclude_components:
        for exc_comp in exclude_components:
            ecl = "({}) MINUS (<< 363787002 : <<246093002 = <<{})".format(ecl, exc_comp)

    if exclude_sites:
        for exc_site in exclude_sites:
            ecl = "({}) MINUS (<< 363787002 : <<704327008 = <<{})".format(ecl, exc_site)

    return ecl


def run_permutations(component_id, component_name,
                    direct_site_id, direct_site_name,
                    loinc_mappings=None,
                    exclude_components=None,
                    exclude_sites=None,
                    require_time_aspect=None,
                    require_scale_type=None,
                    method_constraint=None,
                    server_adapter=None):
    """
    Run all 4 permutations for a component/site pair with optional constraints.

    Args:
        component_id: Component SNOMED ID
        component_name: Component name
        direct_site_id: Site SNOMED ID
        direct_site_name: Site name
        loinc_mappings: Pre-loaded LOINC mapping dict
        exclude_components: List of component IDs to exclude
        exclude_sites: List of site IDs to exclude
        require_time_aspect: Time aspect constraint
        require_scale_type: Scale type constraint
        method_constraint: Method constraint

    Returns:
        list of result dictionaries
    """
    print("\n" + "=" * 80)
    print("Component: {} ({})".format(component_name, component_id))
    print("Direct Site: {} ({})".format(direct_site_name, direct_site_id))
    if exclude_components:
        print("Excluding components: {}".format(exclude_components))
    if exclude_sites:
        print("Excluding sites: {}".format(exclude_sites))
    print("=" * 80)

    permutations = [
        (False, False, "Fixed", "Fixed"),
        (False, True, "Fixed", "Descendants"),
        (True, False, "Descendants", "Fixed"),
        (True, True, "Descendants", "Descendants"),
    ]

    results = []

    for comp_desc, site_desc, comp_label, site_label in permutations:
        print("\nPermutation: Component={}, Site={}".format(comp_label, site_label))

        ecl = build_ecl_query(
            component_id, direct_site_id,
            component_descendants=comp_desc,
            site_descendants=site_desc,
            exclude_components=exclude_components,
            exclude_sites=exclude_sites,
            require_time_aspect=require_time_aspect,
            require_scale_type=require_scale_type,
            method_constraint=method_constraint
        )

        print("  ECL: {}".format(ecl))

        response = execute_ecl_query(ecl, loinc_mappings=loinc_mappings, server_adapter=server_adapter)

        # Extract concept IDs and detailed info
        concept_ids = set()
        concept_names = []
        detailed_concepts = response.get('detailed_concepts', [])

        for concept in detailed_concepts:
            concept_ids.add(concept['concept_id'])
            loinc_suffix = " [LOINC: {}]".format(concept['loinc_code']) if concept['loinc_code'] else ""
            concept_names.append("{} ({}){}".format(
                concept['pt'], concept['concept_id'], loinc_suffix))

        result = {
            'ecl': ecl,
            'component_mode': comp_label,
            'site_mode': site_label,
            'total': response.get('total', 0),
            'concept_ids': concept_ids,
            'detailed_concepts': detailed_concepts,  # Full details
            'concept_names': concept_names[:10],  # First 10 for display
            'execution_time': response.get('execution_time', 0)
        }

        results.append(result)
        print("  Result: {} concepts in value set".format(result['total']))
        print("  Execution time: {:.2f}s".format(result['execution_time']))

        # Rate limiting
        time.sleep(0.5)

    return results


def compare_results(results):
    """
    Compare the 4 permutation results.

    Args:
        results: list of 4 result dicts

    Returns:
        comparison dictionary
    """
    if len(results) != 4:
        return {"error": "Expected 4 results"}

    fixed_fixed = results[0]
    fixed_desc_site = results[1]
    desc_comp_fixed = results[2]
    desc_comp_desc_site = results[3]

    comparison = {
        'baseline': fixed_fixed['total'],
        'added_by_site_descendants': len(fixed_desc_site['concept_ids'] - fixed_fixed['concept_ids']),
        'added_by_component_descendants': len(desc_comp_fixed['concept_ids'] - fixed_fixed['concept_ids']),
        'full_descendants': desc_comp_desc_site['total']
    }

    return comparison


def print_report(results, comparison):
    """Print human-readable report."""
    print("\n" + "=" * 80)
    print("PERMUTATION ANALYSIS REPORT")
    print("=" * 80)

    print("\nRESULTS:")
    print("-" * 80)
    for i, r in enumerate(results, 1):
        print("{}. Component={}, Site={}".format(i, r['component_mode'], r['site_mode']))
        print("   Total concepts: {}".format(r['total']))
        print("   Execution time: {:.2f}s".format(r['execution_time']))
        if r['concept_names']:
            print("   Sample concepts (first 5):")
            for name in r['concept_names'][:5]:
                print("     - {}".format(name))
        print()

    print("COMPARISON:")
    print("-" * 80)
    print("Baseline (Fixed/Fixed): {}".format(comparison['baseline']))
    print("Added by site descendants: +{}".format(comparison['added_by_site_descendants']))
    print("Added by component descendants: +{}".format(comparison['added_by_component_descendants']))
    print("Total with both descendants: {}".format(comparison['full_descendants']))
    print()


def save_results(results, comparison, output_prefix):
    """Save results to files with full concept details."""
    # JSON - Full details with ConceptID, FSN, PT, and LOINC
    json_file = "{}_results.json".format(output_prefix)
    json_data = {
        'permutations': [
            {
                'ecl': r['ecl'],
                'component_mode': r['component_mode'],
                'site_mode': r['site_mode'],
                'total': r['total'],
                'execution_time': r['execution_time'],
                'concepts': [
                    {
                        'concept_id': c['concept_id'],
                        'fsn': c['fsn'],
                        'pt': c['pt'],
                        'loinc_code': c['loinc_code'],
                        'loinc_label': c.get('loinc_label')
                    }
                    for c in r['detailed_concepts']
                ]
            }
            for r in results
        ],
        'comparison': comparison
    }

    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print("Saved: {}".format(json_file))

    # CSV - One row per concept with all details
    csv_file = "{}_concepts.csv".format(output_prefix)
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Permutation', 'Component_Mode', 'Site_Mode',
            'Concept_ID', 'FSN', 'Preferred_Term', 'LOINC_Code', 'LOINC_Label'
        ])

        for i, r in enumerate(results, 1):
            perm_label = "{}-{}".format(r['component_mode'], r['site_mode'])
            for c in r['detailed_concepts']:
                writer.writerow([
                    i,
                    r['component_mode'],
                    r['site_mode'],
                    c['concept_id'],
                    c['fsn'],
                    c['pt'],
                    c['loinc_code'] or '',
                    c.get('loinc_label', '')
                ])
    print("Saved: {}".format(csv_file))


def main():
    """Run permutation analysis with custom constraints."""
    print("=" * 80)
    print("LOINC-SNOMED ECL PERMUTATION ANALYZER")
    print("Enhanced with Custom Constraints")
    print("=" * 80)
    print()
    print("ARCHITECTURE: Hybrid Approach")
    print("  Local: LOINC lookup from identifier file")
    print("  API: ECL query execution + concept details")
    print("=" * 80)

    # Path to LOINC-SNOMED files
    # Update these paths to your actual file location!
    base_path = "../terminologies/LOINCSSNOMED/SnomedCT_LOINCExtension_PRODUCTION_LO1010000_20250921T120000Z/Snapshot/Terminology"
    identifier_file = base_path + "/sct2_Identifier_Snapshot_LO1010000_20250921.txt"
    description_file = base_path + "/sct2_Description_Snapshot-en_LO1010000_20250921.txt"

    # Load LOINC mappings once for performance
    print("Loading LOINC mappings...")
    loinc_mappings = load_loinc_mappings(identifier_file, description_file)
    print("Loaded {} LOINC mappings".format(len(loinc_mappings)))

    # Example 1: Hemoglobin test case (standard - no exclusions)
    # Based on LOINC 718-7 → SNOMED 168331010000106
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Hemoglobin (Standard)")
    print("=" * 80)
    component_id = "38082009"  # Hemoglobin (substance)
    component_name = "Hemoglobin"
    direct_site_id = "119297000"  # Blood specimen
    direct_site_name = "Blood specimen"

    # Run permutations (no exclusions)
    results = run_permutations(
        component_id, component_name,
        direct_site_id, direct_site_name,
        loinc_mappings=loinc_mappings
    )

    # Compare
    comparison = compare_results(results)

    # Print report
    print_report(results, comparison)

    # Save results
    save_results(results, comparison, "ecl_results/hemoglobin_blood")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nKey Findings:")
    print("  - Baseline (exact match): {} concepts".format(comparison['baseline']))
    print("  - Using descendant sites adds: {} concepts".format(
        comparison['added_by_site_descendants']))
    print("  - Using descendant components adds: {} concepts".format(
        comparison['added_by_component_descendants']))
    print("  - Total with both: {} concepts".format(comparison['full_descendants']))

    # ========================================================================
    # EXAMPLE 2: Erythrocyte count (EXCLUDING reticulocytes and cord blood)
    # ========================================================================
    # Uncomment to run this example:
    #
    # print("\n" + "=" * 80)
    # print("EXAMPLE 2: Erythrocyte count (Excluding Reticulocytes & Cord Blood)")
    # print("=" * 80)
    #
    # component_id = "41898006"  # Erythrocyte (cell)
    # component_name = "Erythrocyte"
    # direct_site_id = "119297000"  # Blood specimen
    # direct_site_name = "Blood specimen"
    #
    # # Clinical constraint: Exclude reticulocytes and cord blood
    # exclude_components = ["14202001"]  # Reticulocyte (cell)
    # exclude_sites = ["122554006"]  # Cord blood specimen
    #
    # results_eryth = run_permutations(
    #     component_id, component_name,
    #     direct_site_id, direct_site_name,
    #     loinc_mappings=loinc_mappings,
    #     exclude_components=exclude_components,
    #     exclude_sites=exclude_sites
    # )
    #
    # comparison_eryth = compare_results(results_eryth)
    # print_report(results_eryth, comparison_eryth)
    # save_results(results_eryth, comparison_eryth, "ecl_results/erythrocyte_blood_filtered")
    #
    # print("\nErythrocyte Analysis Complete!")
    # print("Note: Reticulocytes and cord blood specimens excluded as requested")


if __name__ == "__main__":
    main()