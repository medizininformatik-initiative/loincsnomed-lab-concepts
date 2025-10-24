#!/usr/bin/env python3
"""
Generate a centralized summary table of all dashboard results.
Reads config files and generates a comprehensive overview.
"""

import json
import os
from pathlib import Path

# Define all parameters with their LOINC codes and config files
PARAMETERS = [
    {
        'name': 'Hemoglobin',
        'loinc': '59260-0',
        'config': 'config/hemoglobin_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/hemoglobin_decision_dashboard.html'
    },
    {
        'name': 'Erythrocytes',
        'loinc': '26453-1',
        'config': 'config/erythrocytes_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/erythrocytes_decision_dashboard.html'
    },
    {
        'name': 'Leukocytes',
        'loinc': '26464-8',
        'config': 'config/leukocytes_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/leukocytes_decision_dashboard.html'
    },
    {
        'name': 'Platelets',
        'loinc': '26515-7',
        'config': 'config/platelets_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/platelets_decision_dashboard.html'
    },
    {
        'name': 'Hematocrit',
        'loinc': '20570-8',
        'config': 'config/hematocrit_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/hematocrit_decision_dashboard.html'
    },
    {
        'name': 'MCV',
        'loinc': '787-2',
        'config': 'config/mcv_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/mcv_decision_dashboard.html'
    },
    {
        'name': 'MCH',
        'loinc': '28539-5',
        'config': 'config/mch_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/mch_decision_dashboard.html'
    },
    {
        'name': 'MCHC',
        'loinc': '786-4',
        'config': 'config/mchc_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/mchc_decision_dashboard.html'
    },
    {
        'name': 'Methemoglobin (Quant)',
        'loinc': '2614-6',
        'config': 'config/methemoglobin_custom_ecl.json',
        'config_query': 'refined_query_v2_quant',
        'dashboard': 'output/decision_dashboards/methemoglobin_decision_dashboard.html'
    },
    {
        'name': 'Methemoglobin (Ratio)',
        'loinc': '2614-6',
        'config': 'config/methemoglobin_custom_ecl.json',
        'config_query': 'refined_query_v2_ratio',
        'dashboard': 'output/decision_dashboards/methemoglobin_ratio_decision_dashboard.html'
    },
    {
        'name': 'Potassium',
        'loinc': '6298-4',
        'config': 'config/potassium_custom_ecl.json',
        'dashboard': 'output/decision_dashboards/potassium_decision_dashboard.html'
    },
    {
        'name': 'Nitrite Urine (Quant)',
        'loinc': '32710-6',
        'config': 'config/nitrite_urine_custom_ecl.json',
        'config_query': 'refined_query_v2_quant',
        'dashboard': 'output/decision_dashboards/nitrite_urine_decision_dashboard.html'
    },
    {
        'name': 'Nitrite Urine (Qual)',
        'loinc': '32710-6',
        'config': 'config/nitrite_urine_custom_ecl.json',
        'config_query': 'refined_query_v2_qual',
        'dashboard': 'output/decision_dashboards/nitrite_urine_decision_dashboard.html'
    }
]

def load_config(config_path, query_id='refined_query_v2'):
    """Load ECL config file and extract query info"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Find the query
        for query in config.get('queries', []):
            if query['id'] == query_id:
                return {
                    'description': config.get('description', ''),
                    'query_name': query.get('name', ''),
                    'query_description': query.get('description', ''),
                    'ecl': query.get('ecl', ''),
                    'note': config.get('note', '')
                }
        return None
    except Exception as e:
        print(f"Error loading {config_path}: {e}")
        return None

def main():
    print("=" * 80)
    print("DASHBOARD SUMMARY - ECL REFINED QUERY V2 RESULTS")
    print("=" * 80)
    print()

    # Print header
    print(f"{'Parameter':<30} {'LOINC':<12} {'Query Type':<40} {'Config File':<40}")
    print("-" * 122)

    # Load and print each parameter
    for param in PARAMETERS:
        config_path = param['config']
        query_id = param.get('config_query', 'refined_query_v2')

        if os.path.exists(config_path):
            config_info = load_config(config_path, query_id)
            if config_info:
                # Truncate long query names
                query_name = config_info['query_name']
                if len(query_name) > 38:
                    query_name = query_name[:35] + '...'

                print(f"{param['name']:<30} {param['loinc']:<12} {query_name:<40} {config_path:<40}")
            else:
                print(f"{param['name']:<30} {param['loinc']:<12} {'Query not found':<40} {config_path:<40}")
        else:
            print(f"{param['name']:<30} {param['loinc']:<12} {'Config not found':<40} {config_path:<40}")

    print()
    print("=" * 80)
    print("DETAILED QUERY INFORMATION")
    print("=" * 80)
    print()

    # Print detailed info for each parameter
    for param in PARAMETERS:
        config_path = param['config']
        query_id = param.get('config_query', 'refined_query_v2')

        print(f"\n{'='*80}")
        print(f"{param['name']} (LOINC {param['loinc']})")
        print(f"{'='*80}")

        if os.path.exists(config_path):
            config_info = load_config(config_path, query_id)
            if config_info:
                print(f"\nQuery: {config_info['query_name']}")
                print(f"\nDescription: {config_info['query_description']}")

                if config_info.get('note'):
                    print(f"\n[!] SPECIAL NOTE: {config_info['note']}")

                print(f"\nECL Query:")
                print(f"{config_info['ecl']}")
            else:
                print(f"\n[!] Query '{query_id}' not found in config file")
        else:
            print(f"\n[!] Config file not found: {config_path}")

    print("\n" + "=" * 80)
    print("SUMMARY COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
