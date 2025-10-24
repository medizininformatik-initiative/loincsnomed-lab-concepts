#!/usr/bin/env python3
"""
Extract ALL query results from generated dashboards.
Creates a comprehensive table showing SNOMED concept counts for ALL experiments.
"""

from pathlib import Path
import re

# Define dashboards to extract
DASHBOARDS = [
    {'name': 'Hemoglobin', 'file': 'output/decision_dashboards/hemoglobin_decision_dashboard.html'},
    {'name': 'Erythrocytes', 'file': 'output/decision_dashboards/erythrocytes_decision_dashboard.html'},
    {'name': 'Leukocytes', 'file': 'output/decision_dashboards/leukocytes_decision_dashboard.html'},
    {'name': 'Platelets', 'file': 'output/decision_dashboards/platelets_decision_dashboard.html'},
    {'name': 'Hematocrit', 'file': 'output/decision_dashboards/hematocrit_decision_dashboard.html'},
    {'name': 'MCV', 'file': 'output/decision_dashboards/mcv_decision_dashboard.html'},
    {'name': 'MCH', 'file': 'output/decision_dashboards/mch_decision_dashboard.html'},
    {'name': 'MCHC', 'file': 'output/decision_dashboards/mchc_decision_dashboard.html'},
    {'name': 'Methemoglobin', 'file': 'output/decision_dashboards/methemoglobin_decision_dashboard.html'},
    {'name': 'Potassium', 'file': 'output/decision_dashboards/potassium_decision_dashboard.html'},
    {'name': 'Nitrite Urine', 'file': 'output/decision_dashboards/nitrite_urine_decision_dashboard.html'},
]

def extract_loinc(html_content):
    """Extract primary LOINC code from dashboard"""
    match = re.search(r'Primary LOINC: <strong>([\d-]+)</strong>', html_content)
    return match.group(1) if match else 'N/A'

def extract_experiment_counts(html_content):
    """Extract SNOMED concept counts for all experiments"""
    experiments = {
        'Exp0': 0,
        'Exp1': 0,
        'Exp2': 0,
        'Exp3': 0,
        'Exp4': 0,
        'Exp5': 0,
        'V2': []
    }

    # Exp 0: Precoord Descendants
    match = re.search(r'<h4>Precoord Descendants</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp0'] = int(match.group(1))

    # Exp 1: Fixed Component
    match = re.search(r'<h4>Fixed Component</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp1'] = int(match.group(1))

    # Exp 2: Component Descendants
    match = re.search(r'<h4>Component Descendants</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp2'] = int(match.group(1))

    # Exp 3: Fixed Component Property
    match = re.search(r'<h4>Fixed Component Property</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp3'] = int(match.group(1))

    # Exp 4: Fixed Component System
    match = re.search(r'<h4>Fixed Component System</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp4'] = int(match.group(1))

    # Exp 5: Refined Query V1
    match = re.search(r'<h4>Refined Query V1</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if match:
        experiments['Exp5'] = int(match.group(1))

    # V2: All Refined Query V2 variants
    v2_matches = re.findall(r'<h4>Refined Query V2[^<]*</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if v2_matches:
        experiments['V2'] = [int(m) for m in v2_matches]

    return experiments

def extract_interpolar_count(html_content):
    """Extract Interpolar reference count by counting rows with class='interpolar'"""
    # Count <tr class="interpolar"> rows in the table
    matches = re.findall(r'<tr class="interpolar">', html_content)
    return len(matches)

def format_v2_counts(v2_list):
    """Format V2 counts - show sum and breakdown if multiple"""
    if not v2_list:
        return '0'
    if len(v2_list) == 1:
        return str(v2_list[0])
    # Multiple V2 queries
    total = sum(v2_list)
    breakdown = '+'.join(str(x) for x in v2_list)
    return f"{total} ({breakdown})"

def main():
    print("=" * 140)
    print("COMPREHENSIVE DASHBOARD RESULTS - ALL ECL EXPERIMENTS")
    print("=" * 140)
    print()
    print(f"{'Parameter':<20} {'LOINC':<10} {'Exp0':<8} {'Exp1':<8} {'Exp2':<8} {'Exp3':<8} {'Exp4':<8} {'Exp5':<8} {'V2':<18} {'Interpolar':<12}")
    print("-" * 140)

    for dashboard in DASHBOARDS:
        filepath = Path(dashboard['file'])

        if not filepath.exists():
            print(f"{dashboard['name']:<20} {'N/A':<10} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<18} {'N/A':<12}")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            loinc = extract_loinc(content)
            exps = extract_experiment_counts(content)
            interpolar = extract_interpolar_count(content)

            v2_str = format_v2_counts(exps['V2'])

            print(f"{dashboard['name']:<20} {loinc:<10} {exps['Exp0']:<8} {exps['Exp1']:<8} {exps['Exp2']:<8} {exps['Exp3']:<8} {exps['Exp4']:<8} {exps['Exp5']:<8} {v2_str:<18} {interpolar:<12}")

        except Exception as e:
            print(f"{dashboard['name']:<20} ERROR: {str(e)}")

    print()
    print("=" * 140)
    print("Legend:")
    print("  Exp0: Precoordinated Descendants (baseline)")
    print("  Exp1: Fixed Component (descendant system/property)")
    print("  Exp2: Component Descendants (exploration)")
    print("  Exp3: Fixed Component + Property")
    print("  Exp4: Fixed Component + System (blood specimen)")
    print("  Exp5: Refined Query V1 (universal Measurement property)")
    print("  V2:   Refined Query V2 (custom ECL with property/component filtering)")
    print("        For parameters with multiple V2 queries (e.g., Methemoglobin, Nitrite), shows: total (query1+query2)")
    print("  Interpolar: Reference codes from Interpolar mapping (level 1+2)")
    print("=" * 140)
    print()
    print("Key Insights:")
    print("  - Exp0 is the baseline (pre-coordinated hierarchy)")
    print("  - Exp5 (V1) uses universal Measurement property - may be 0 for special properties (e.g., MCH Entitic mass)")
    print("  - V2 is the refined approach with specific property/component targeting")
    print("  - MCV/MCHC use 'Inheres in' relationship, not Component - post-coord queries (Exp1-5) may fail")
    print("=" * 140)

if __name__ == '__main__':
    main()
