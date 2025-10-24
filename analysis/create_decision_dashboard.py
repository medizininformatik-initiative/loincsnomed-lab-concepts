#!/usr/bin/env python3
"""
ECL Decision Dashboard Generator
=================================
Creates a single-page HTML dashboard showing all ECL experiment results
to facilitate inclusion/exclusion decisions.

For each LOINC parameter, shows:
1. All ECL experiment results (1-7) side by side
2. LOINC codes found in each experiment
3. Overlap with Interpolar reference
4. Differences between approaches (e.g., Fixed vs Descendants)
5. Specimen types found (to inform exclusion decisions)
6. SNOMED attributes (Component, Property, Direct site)

Usage:
    python create_decision_dashboard.py <primary_loinc> <output_name>

Example:
    python create_decision_dashboard.py 14682-9 creatinine
"""

import sys
import os
import json
import asyncio
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
SNOMED_TERMINOLOGY_PATH = os.getenv('loinc_snomed_terminology_path')
if not SNOMED_TERMINOLOGY_PATH:
    print("ERROR: loinc_snomed_terminology_path not set in .env")
    sys.exit(1)

SNOMED_TERMINOLOGY_DIR = Path(SNOMED_TERMINOLOGY_PATH)
RELATIONSHIP_FILE = SNOMED_TERMINOLOGY_DIR / 'sct2_Relationship_Snapshot_LO1010000_20250921.txt'
CONCEPT_FILE = SNOMED_TERMINOLOGY_DIR / 'sct2_Concept_Snapshot_LO1010000_20250921.txt'
DESCRIPTION_FILE = SNOMED_TERMINOLOGY_DIR / 'sct2_Description_Snapshot-en_LO1010000_20250921.txt'
INPUT_EXCEL = project_root / 'input' / 'LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx'
MII300_VALUESET = project_root / 'output' / 'valuesets' / 'valueset-mii-top-300-loinc.json'

# SNOMED attribute IDs
COMPONENT_ATTRIBUTE_ID = "246093002"
PROPERTY_ATTRIBUTE_ID = "370130000"
DIRECT_SITE_ATTRIBUTE_ID = "704327008"
MEASUREMENT_PROPERTY_SCTID = "685451010000100"
MEASUREMENT_PROPERTY_LABEL = "Measurement property (qualifier value)"

def get_snomed_fsn(concept_id, description_file):
    """Get Fully Specified Name for a SNOMED concept."""
    if not concept_id:
        return "N/A"

    with open(description_file, 'r', encoding='utf-8') as f:
        header = next(f).strip().split('\t')
        # Find column indices
        concept_idx = header.index('conceptId')
        active_idx = header.index('active')
        type_idx = header.index('typeId')
        term_idx = header.index('term')

        for line in f:
            parts = line.strip().split('\t')
            if len(parts) > max(concept_idx, active_idx, type_idx, term_idx):
                active = parts[active_idx]
                concept = parts[concept_idx]
                type_id = parts[type_idx]
                term = parts[term_idx]

                if active == '1' and concept == concept_id and type_id == '900000000000003001':  # FSN
                    return term
    return f"[{concept_id}] (FSN not found)"

def load_snomed_attributes(relationship_file, concept_id):
    """Extract Component, Property, and Direct site attributes."""
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

def extract_specimen_types(loinc_mappings, snomed_concepts, adapter):
    """Extract specimen types from SNOMED concepts using terminology server."""
    specimens = {}

    for concept_id in snomed_concepts:
        if concept_id in loinc_mappings:
            # Look for Direct site relationships
            with open(RELATIONSHIP_FILE, 'r', encoding='utf-8') as f:
                next(f)
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 8:
                        active = parts[2]
                        source_id = parts[4]
                        type_id = parts[7]
                        destination_id = parts[5]

                        if active == '1' and source_id == concept_id and type_id == DIRECT_SITE_ATTRIBUTE_ID:
                            # Use terminology server to get FSN (faster and has all concepts)
                            if destination_id not in specimens:
                                details = adapter.get_concept_details(destination_id)
                                specimens[destination_id] = details.get('fsn', f'[{destination_id}] (not found)')

    return specimens

def load_cached_experiment_result(cached_json_path, primary_loinc, ecl_expression):
    """Load experiment results from cached JSON file."""
    if not cached_json_path.exists():
        return None

    with open(cached_json_path, 'r', encoding='utf-8') as f:
        cached_data = json.load(f)

    if primary_loinc not in cached_data:
        return None

    entry = cached_data[primary_loinc]
    return {
        'ecl_expression': ecl_expression,
        'loinc_codes': entry.get('loinc_codes_found', []),
        'snomed_concepts': [],  # Will populate from loinc_mappings if needed
        'snomed_concept_count': entry.get('snomed_concept_count', 0),
        'execution_time': entry.get('execution_time', 0)
    }

def run_ecl_experiment(ecl_name, ecl_expression, loinc_mappings, adapter, cached_result=None, description=None):
    """Execute a single ECL query experiment (or use cached result)."""
    if cached_result:
        print(f"    Loading cached: {ecl_name}")
        return cached_result

    print(f"    Running: {ecl_name}")
    result = execute_ecl_query(ecl_expression, loinc_mappings, limit=1000, server_adapter=adapter)

    loinc_codes = []
    snomed_concepts = []

    for concept in result.get('detailed_concepts', []):
        if concept.get('loinc_code'):
            loinc_codes.append(concept['loinc_code'])
        if concept.get('concept_id'):
            snomed_concepts.append(concept['concept_id'])

    return {
        'ecl_expression': ecl_expression,
        'loinc_codes': sorted(list(set(loinc_codes))),
        'snomed_concepts': sorted(list(set(snomed_concepts))),
        'snomed_concept_count': result.get('total', 0),
        'execution_time': result.get('execution_time', 0),
        'description': description
    }

def generate_html_dashboard(primary_loinc, component_name, snomed_concept_id, attributes, experiments, interpolar_codes, loinc_displays, specimens, adapter, mii300_codes, binary_output=False):
    """Generate HTML dashboard for decision-making."""

    # Collect all LOINC codes
    all_loinc_codes = set(interpolar_codes)
    for exp in experiments.values():
        all_loinc_codes.update(exp['loinc_codes'])

    # Build comparison matrix
    comparison_rows = []
    for loinc_code in all_loinc_codes:
        row = {
            'loinc': loinc_code,
            'display': loinc_displays.get(loinc_code, f'LOINC {loinc_code}'),
            'is_primary': loinc_code == primary_loinc,
            'in_interpolar': loinc_code in interpolar_codes,
            'in_mii300': loinc_code in mii300_codes,
            'hit_count': 0
        }

        for exp_name, exp_data in experiments.items():
            is_in_exp = loinc_code in exp_data['loinc_codes']
            row[exp_name] = is_in_exp
            if is_in_exp:
                row['hit_count'] += 1

        comparison_rows.append(row)

    # Sort by hit count (descending), then by LOINC code
    comparison_rows.sort(key=lambda x: (-x['hit_count'], x['loinc']))

    # Calculate statistics
    stats = {}
    for exp_name, exp_data in experiments.items():
        exp_codes = set(exp_data['loinc_codes'])
        overlap = exp_codes & interpolar_codes

        precision = len(overlap) / len(exp_codes) if exp_codes else 0
        recall = len(overlap) / len(interpolar_codes) if interpolar_codes else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        stats[exp_name] = {
            'codes': len(exp_codes),
            'overlap': len(overlap),
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ECL Decision Dashboard: {component_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .section {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 10px;
            text-align: left;
            position: sticky;
            top: 0;
        }}
        td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .check {{
            color: #27ae60;
            font-weight: bold;
        }}
        .primary {{
            background-color: #fff3cd;
            font-weight: bold;
        }}
        .interpolar {{
            background-color: #d1ecf1;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stat-card {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        .stat-card h4 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
        }}
        .specimen-list {{
            list-style: none;
            padding: 0;
        }}
        .specimen-list li {{
            padding: 5px;
            margin: 5px 0;
            background-color: #ecf0f1;
            border-radius: 3px;
        }}
        .ecl-query {{
            background-color: #f8f9fa;
            padding: 10px;
            border-left: 3px solid #3498db;
            font-family: monospace;
            white-space: pre-wrap;
            margin: 10px 0;
        }}
        .attributes {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .good {{ color: #27ae60; font-weight: bold; }}
        .medium {{ color: #f39c12; font-weight: bold; }}
        .poor {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ECL Decision Dashboard: {component_name.upper()}</h1>
        <p>Primary LOINC: <strong>{primary_loinc}</strong> - {loinc_displays.get(primary_loinc, 'N/A')}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="section">
        <h2>SNOMED Concept & Attributes</h2>
        <div class="attributes">
            <p><strong>Primary Observable Entity:</strong> {snomed_concept_id} - {adapter.get_concept_details(snomed_concept_id).get('fsn', 'N/A')}</p>
            <hr>
            <p><strong>Component:</strong> {attributes.get('component', 'N/A')} - {adapter.get_concept_details(attributes['component']).get('fsn', 'N/A') if attributes.get('component') else 'N/A'}</p>
            <p><strong>Property:</strong> {attributes.get('property', 'N/A')} - {adapter.get_concept_details(attributes['property']).get('fsn', 'N/A') if attributes.get('property') else 'N/A'}</p>
            <p><strong>Direct site:</strong> {attributes.get('direct_site', 'N/A')} - {adapter.get_concept_details(attributes['direct_site']).get('fsn', 'N/A') if attributes.get('direct_site') else 'N/A'}</p>
        </div>
    </div>

    <div class="section">
        <h2>ECL Experiment Statistics</h2>
        <div class="stat-grid">
"""

    for exp_name, stat in stats.items():
        recall_class = 'good' if stat['recall'] >= 0.9 else 'medium' if stat['recall'] >= 0.7 else 'poor'
        precision_class = 'good' if stat['precision'] >= 0.9 else 'medium' if stat['precision'] >= 0.7 else 'poor'

        html += f"""
            <div class="stat-card">
                <h4>{exp_name.replace('_', ' ').title()}</h4>
                <p>Codes: <span class="stat-value">{stat['codes']}</span></p>
                <p>Recall: <span class="{recall_class}">{stat['recall']:.1%}</span></p>
                <p>Precision: <span class="{precision_class}">{stat['precision']:.1%}</span></p>
                <p>F1: {stat['f1']:.3f}</p>
            </div>
"""

    html += """
        </div>
    </div>

    <div class="section">
        <h2>Specimen Types Found</h2>
        <ul class="specimen-list">
"""

    for sctid, fsn in sorted(specimens.items(), key=lambda x: x[1]):
        html += f"            <li><strong>{sctid}</strong> - {fsn}</li>\n"

    html += """
        </ul>
        <p><em>Consider excluding specimen types that are not relevant for this analysis (e.g., cord blood, plasma, urine).</em></p>
    </div>

    <div class="section">
        <h2>ECL Query Details</h2>
"""

    for exp_name, exp_data in experiments.items():
        # Add FSN labels to the ECL expression for display
        ecl_display = exp_data['ecl_expression']

        # Find all concept IDs (digits only, typically 6-18 digits for SNOMED)
        import re
        concept_ids = re.findall(r'\b(\d{6,18})\b', ecl_display)

        # Replace each concept ID with ID |FSN| format if not already labeled
        for concept_id in set(concept_ids):
            # Check if this concept ID is already labeled (has |...| after it)
            if not re.search(rf'{concept_id}\s*\|', ecl_display):
                # Get FSN and add label
                fsn = adapter.get_concept_details(concept_id).get('fsn', '')
                if fsn:
                    ecl_display = ecl_display.replace(concept_id, f"{concept_id} |{fsn}|")

        # Add description if available
        description_html = ""
        if exp_data.get('description'):
            description_html = f"<p><em>{exp_data['description']}</em></p>"

        html += f"""
        <h3>{exp_name.replace('_', ' ').title()}</h3>
        {description_html}
        <div class="ecl-query">{ecl_display}</div>
        <p>Results: {exp_data['snomed_concept_count']} SNOMED concepts, {len(exp_data['loinc_codes'])} LOINC codes</p>
"""

    html += """
    </div>

    <div class="section">
        <h2>LOINC Code Comparison Matrix</h2>
        <p>This table shows which LOINC codes were found by each ECL experiment.</p>
        <table>
            <thead>
                <tr>
                    <th>LOINC</th>
                    <th>Display Name</th>
                    <th>Interpolar</th>
                    <th>MII300</th>
"""

    for exp_name in experiments.keys():
        # Don't truncate column names - use title case and full name
        display_name = exp_name.replace('_', ' ').title()
        html += f"                    <th>{display_name}</th>\n"

    html += """
                </tr>
            </thead>
            <tbody>
"""

    # Define check mark display based on binary_output flag
    check_true = '1' if binary_output else '✓'
    check_false = '0' if binary_output else ''

    for row in comparison_rows:
        row_class = 'primary' if row['is_primary'] else 'interpolar' if row['in_interpolar'] else ''
        html += f"""
                <tr class="{row_class}">
                    <td>{row['loinc']}</td>
                    <td>{row['display']}</td>
                    <td>{check_true if row['in_interpolar'] else check_false}</td>
                    <td>{check_true if row['in_mii300'] else check_false}</td>
"""

        for exp_name in experiments.keys():
            html += f"                    <td class=\"check\">{check_true if row[exp_name] else check_false}</td>\n"

        html += "                </tr>\n"

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Decision Guidance</h2>
        <h3>Key Questions:</h3>
        <ol>
            <li><strong>Specimen Exclusions:</strong> Which specimen types should be excluded? (Review "Specimen Types Found" section)</li>
            <li><strong>Component Strategy:</strong> Fixed component or descendants? (Compare Exp 2 vs Exp 3)</li>
            <li><strong>Recall Priority:</strong> Do you need high recall (capture all relevant codes) or high precision (only exact matches)?</li>
            <li><strong>Interpolar Alignment:</strong> Should results align closely with Interpolar reference?</li>
        </ol>

        <h3>Experiment Guide:</h3>
        <ul>
            <li><strong>Exp 0 (Pre-coordinated Descendants):</strong> All descendants of the primary observable entity itself (e.g., all child concepts under "Creatinine in serum" - THIS is the true pre-coordinated hierarchy)</li>
            <li><strong>Exp 1 (Fixed Component):</strong> Observable entities with EXACTLY this component (no subcomponents)</li>
            <li><strong>Exp 2 (Component Descendants):</strong> Observable entities with this component OR its descendants (includes subcomponents like HbA1c for Hemoglobin)</li>
            <li><strong>Exp 3 (Fixed Component + Property):</strong> Adds specific property constraint (e.g., substance concentration)</li>
            <li><strong>Exp 4 (Fixed Component + System):</strong> Adds specimen/system constraint (e.g., blood specimen)</li>
            <li><strong>Exp 5 (Refined Query V1):</strong> Component + Universal Measurement Property (all quantitative types) + System - Most comprehensive</li>
        </ul>

        <h3>Why Start with Exp 0?</h3>
        <p><strong>Exp 0</strong> queries the pre-coordinated hierarchy (e.g., << "Substance concentration of creatinine in serum" concept), capturing all child observable entities in that hierarchy. This is your baseline to compare against post-coordinated approaches (Exp 1-5).</p>
    </div>
</body>
</html>
"""

    return html

def main():
    if len(sys.argv) < 3:
        print("Usage: python create_decision_dashboard.py <primary_loinc> <output_name> [custom_queries.json] [--binary]")
        print("Example: python create_decision_dashboard.py 14682-9 creatinine")
        print("Example with custom queries: python create_decision_dashboard.py 14682-9 creatinine custom_ecl.json")
        print("Example with binary output: python create_decision_dashboard.py 14682-9 creatinine custom_ecl.json --binary")
        sys.exit(1)

    primary_loinc = sys.argv[1]
    component_name = sys.argv[2]

    # Parse optional arguments
    custom_queries_file = None
    binary_output = False

    for arg in sys.argv[3:]:
        if arg == '--binary':
            binary_output = True
        elif not arg.startswith('--'):
            custom_queries_file = arg

    print("=" * 80)
    print(f"ECL DECISION DASHBOARD: {component_name.upper()}")
    print("=" * 80)
    print(f"Primary LOINC: {primary_loinc}\n")

    # Load LOINC-SNOMED mappings
    print("[1/6] Loading LOINC-SNOMED mappings...")
    loinc_mappings = load_loinc_mappings(LOINC_SNOMED_MAPPING_PATH)
    print(f"  [OK] Loaded {len(loinc_mappings)} mappings")

    # Get SNOMED concept ID
    loinc_to_snomed = {data['loinc_code']: sctid for sctid, data in loinc_mappings.items() if data.get('loinc_code')}
    if primary_loinc not in loinc_to_snomed:
        print(f"ERROR: Primary LOINC {primary_loinc} not found in SNOMED mappings")
        sys.exit(1)

    snomed_concept_id = loinc_to_snomed[primary_loinc]
    print(f"  SNOMED Concept ID: {snomed_concept_id}")

    # Extract SNOMED attributes
    print("\n[2/6] Extracting SNOMED attributes...")
    attributes = load_snomed_attributes(RELATIONSHIP_FILE, snomed_concept_id)
    print(f"  Component: {attributes.get('component', 'N/A')}")
    print(f"  Property: {attributes.get('property', 'N/A')}")
    print(f"  Direct site: {attributes.get('direct_site', 'N/A')}")

    # Load Interpolar reference
    print("\n[3/6] Loading Interpolar reference...")
    df_interpolar = pd.read_excel(INPUT_EXCEL, sheet_name='LOINC Mapping Interpolar', header=18)

    # Include both level 1 (quantitative) and level 2 (cutoff-based) comparability
    # Get all secondary codes where this is the primary
    df_comparable = df_interpolar[
        df_interpolar['COMPARABILITY_TO_LOINC_PRIMARY'].isin(['1 - quantitativ', '2 - cutoff_Fragestellung'])
    ].copy()
    interpolar_secondary_codes = set(df_comparable[df_comparable['LOINC_PRIMARY'] == primary_loinc]['LOINC'].dropna().unique())

    # Check if the primary itself appears as a LOINC code in Interpolar with level 1+2
    primary_in_interpolar = primary_loinc in df_comparable['LOINC'].values

    # Build interpolar_codes set: include secondaries + primary if it's actually in Interpolar
    interpolar_codes = interpolar_secondary_codes.copy()
    if primary_in_interpolar:
        interpolar_codes.add(primary_loinc)

    has_interpolar_reference = len(interpolar_codes) > 0

    # Load MII Top 300 codes from valueset
    try:
        with open(MII300_VALUESET, 'r', encoding='utf-8') as f:
            mii300_vs = json.load(f)
            mii300_codes = set([c['code'] for c in mii300_vs['compose']['include'][0]['concept']])
    except Exception as e:
        print(f"  WARNING: Could not load MII300 valueset: {e}")
        mii300_codes = set()

    if has_interpolar_reference:
        print(f"  [OK] Found {len(interpolar_codes)} Interpolar codes (level 1+2 comparability)")
    else:
        print(f"  [WARNING] No Interpolar reference data available for {primary_loinc}")
    print(f"  [OK] Found {len(mii300_codes)} MII Top 300 codes")

    # Connect to terminology server
    print("\n[4/6] Connecting to terminology server...")
    adapter = create_adapter('loincsnomed')
    print("  [OK] Connected")

    # Run all ECL experiments (using cached results where available)
    print("\n[5/6] Loading ECL experiments...")
    experiments = {}

    # Define cache paths
    cache_dir = project_root / 'output'
    cache_paths = {
        'precoord_descendants': cache_dir / 'ecl_descendants_baseline' / 'ecl_query_results_summary.json',
        'ecl_fixed_component': cache_dir / 'ecl_fixed_component' / 'ecl_query_results_summary.json',
        'ecl_component_descendants': cache_dir / 'ecl_component_descendants' / 'ecl_query_results_summary.json',
        'ecl_fixed_component_property': cache_dir / 'ecl_fixed_component_property' / 'ecl_query_results_summary.json',
        'ecl_fixed_component_system': cache_dir / 'ecl_fixed_component_system' / 'ecl_query_results_summary.json',
    }

    # Exp 0: Pre-coordinated hierarchy (ALWAYS run first - descendants of the primary observable entity itself)
    primary_fsn = adapter.get_concept_details(snomed_concept_id).get('fsn', '')
    ecl_precoord = f"<< {snomed_concept_id} |{primary_fsn}|"
    cached_result = load_cached_experiment_result(cache_paths['precoord_descendants'], primary_loinc, ecl_precoord)
    experiments['precoord_descendants'] = run_ecl_experiment(
        'precoord_descendants',
        ecl_precoord,
        loinc_mappings,
        adapter,
        cached_result
    )

    if attributes.get('component'):
        # Get FSN labels for readability
        comp_fsn = adapter.get_concept_details(attributes['component']).get('fsn', '')

        # Exp 1: Fixed Component
        ecl_fixed_comp = f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']} |{comp_fsn}|"
        cached_result = load_cached_experiment_result(cache_paths['ecl_fixed_component'], primary_loinc, ecl_fixed_comp)
        experiments['ecl_fixed_component'] = run_ecl_experiment(
            'ecl_fixed_component',
            ecl_fixed_comp,
            loinc_mappings,
            adapter,
            cached_result
        )

        # Exp 2: Component Descendants
        ecl_comp_desc = f"<< 363787002 |Observable entity| : 246093002 |Component| = << {attributes['component']} |{comp_fsn}|"
        cached_result = load_cached_experiment_result(cache_paths['ecl_component_descendants'], primary_loinc, ecl_comp_desc)
        experiments['ecl_component_descendants'] = run_ecl_experiment(
            'ecl_component_descendants',
            ecl_comp_desc,
            loinc_mappings,
            adapter,
            cached_result
        )

    if attributes.get('component') and attributes.get('property'):
        # Get FSN labels for readability
        comp_fsn = adapter.get_concept_details(attributes['component']).get('fsn', '')
        prop_fsn = adapter.get_concept_details(attributes['property']).get('fsn', '')

        # Exp 3: Fixed Component Property
        ecl_comp_prop = f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']} |{comp_fsn}|, 370130000 |Property| = {attributes['property']} |{prop_fsn}|"
        cached_result = load_cached_experiment_result(cache_paths['ecl_fixed_component_property'], primary_loinc, ecl_comp_prop)
        experiments['ecl_fixed_component_property'] = run_ecl_experiment(
            'ecl_fixed_component_property',
            ecl_comp_prop,
            loinc_mappings,
            adapter,
            cached_result
        )

    if attributes.get('component') and attributes.get('direct_site'):
        # Get FSN labels for readability
        comp_fsn = adapter.get_concept_details(attributes['component']).get('fsn', '')
        site_fsn = adapter.get_concept_details(attributes['direct_site']).get('fsn', '')

        # Exp 4: Fixed Component System
        ecl_comp_sys = f"<< 363787002 |Observable entity| : 246093002 |Component| = {attributes['component']} |{comp_fsn}|, 704327008 |Direct site| = << {attributes['direct_site']} |{site_fsn}|"
        cached_result = load_cached_experiment_result(cache_paths['ecl_fixed_component_system'], primary_loinc, ecl_comp_sys)
        experiments['ecl_fixed_component_system'] = run_ecl_experiment(
            'ecl_fixed_component_system',
            ecl_comp_sys,
            loinc_mappings,
            adapter,
            cached_result
        )

    if attributes.get('component') and attributes.get('property') and attributes.get('direct_site'):
        # Get FSN labels for readability
        comp_fsn = adapter.get_concept_details(attributes['component']).get('fsn', '')
        site_fsn = adapter.get_concept_details(attributes['direct_site']).get('fsn', '')

        # Exp 5: Refined Query V1 (Component + Universal Measurement Property + System)
        ecl_refined_v1 = f"""<< 363787002 |Observable entity| :
    246093002 |Component| = {attributes['component']} |{comp_fsn}|,
    370130000 |Property| = << {MEASUREMENT_PROPERTY_SCTID} |{MEASUREMENT_PROPERTY_LABEL}|,
    704327008 |Direct site| = << {attributes['direct_site']} |{site_fsn}|"""
        experiments['refined_query_v1'] = run_ecl_experiment(
            'refined_query_v1',
            ecl_refined_v1,
            loinc_mappings,
            adapter,
            None  # No cache for this one yet
        )

    # Load and execute custom queries if provided
    if custom_queries_file:
        print(f"\n[CUSTOM] Loading custom ECL queries from {custom_queries_file}...")
        try:
            with open(custom_queries_file, 'r', encoding='utf-8') as f:
                custom_queries = json.load(f)

            for query in custom_queries.get('queries', []):
                query_id = query['id']
                query_name = query.get('name', query_id)
                query_description = query.get('description', '')
                ecl_template = query['ecl']

                print(f"    Running custom query: {query_name}")

                # Execute custom ECL query
                experiments[query_id] = run_ecl_experiment(
                    query_id,
                    ecl_template,
                    loinc_mappings,
                    adapter,
                    None,
                    description=query_description
                )
        except FileNotFoundError:
            print(f"  [WARNING] Custom queries file not found: {custom_queries_file}")
        except Exception as e:
            print(f"  [WARNING] Error loading custom queries: {e}")

    # Extract specimen types
    print("\n[6/6] Extracting specimen types...")
    all_snomed_concepts = set()
    for exp in experiments.values():
        all_snomed_concepts.update(exp['snomed_concepts'])

    specimens = extract_specimen_types(loinc_mappings, all_snomed_concepts, adapter)
    print(f"  [OK] Found {len(specimens)} specimen types")

    # Fetch LOINC displays
    print("\n[7/7] Fetching LOINC display names...")
    all_loinc_codes = set(interpolar_codes)
    for exp in experiments.values():
        all_loinc_codes.update(exp['loinc_codes'])

    loinc_displays = asyncio.run(fetch_displays_async(sorted(all_loinc_codes), verbose=False))
    print(f"  [OK] Fetched {len(loinc_displays)} displays")

    # Generate HTML dashboard
    print("\nGenerating HTML dashboard...")
    if binary_output:
        print("  Using binary output (0/1) instead of checkmarks")
    html = generate_html_dashboard(
        primary_loinc,
        component_name,
        snomed_concept_id,
        attributes,
        experiments,
        interpolar_codes,
        loinc_displays,
        specimens,
        adapter,
        mii300_codes,
        binary_output
    )

    # Save dashboard
    output_dir = project_root / 'output' / 'decision_dashboards'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f'{component_name}_decision_dashboard.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n{'=' * 80}")
    print("DASHBOARD GENERATED!")
    print(f"{'=' * 80}")
    print(f"\nOutput: {output_file}")
    print(f"\nOpen in browser to review results and make inclusion/exclusion decisions.")

if __name__ == '__main__':
    main()
