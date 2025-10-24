#!/usr/bin/env python3
"""
Extract numerical results from generated dashboards.
Creates a compact table showing SNOMED concept counts for each parameter.
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

def extract_exp0_count(html_content):
    """Extract Exp 0 (Precoord Descendants) SNOMED concept count"""
    match = re.search(r'<h4>Precoord Descendants</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    return int(match.group(1)) if match else 0

def extract_v2_count(html_content):
    """Extract Refined Query V2 SNOMED concept count"""
    # Look for any V2 query
    matches = re.findall(r'<h4>Refined Query V2[^<]*</h4>\s*<p>Codes: <span class="stat-value">(\d+)</span>', html_content, re.DOTALL)
    if matches:
        # Return sum if multiple v2 queries (like Methemoglobin, Nitrite)
        return sum(int(m) for m in matches)
    return 0

def extract_loinc_count(html_content):
    """Extract total LOINC codes in comparison matrix"""
    # Count rows in the table (excluding header)
    matches = re.findall(r'<tr class="(?:primary|)">', html_content)
    return len(matches)

def extract_interpolar_count(html_content):
    """Extract Interpolar reference count"""
    match = re.search(r'Found (\d+) Interpolar codes', html_content)
    if match:
        return int(match.group(1))
    # Check for warning
    if 'No Interpolar reference data available' in html_content:
        return 0
    return 0

def main():
    print("=" * 100)
    print("DASHBOARD RESULTS SUMMARY - SNOMED CONCEPT COUNTS")
    print("=" * 100)
    print()
    print(f"{'Parameter':<25} {'LOINC':<12} {'Exp0':<8} {'V2':<8} {'LOINC Codes':<12} {'Interpolar':<12}")
    print("-" * 100)

    for dashboard in DASHBOARDS:
        filepath = Path(dashboard['file'])

        if not filepath.exists():
            print(f"{dashboard['name']:<25} {'N/A':<12} {'N/A':<8} {'N/A':<8} {'N/A':<12} {'N/A':<12}")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            loinc = extract_loinc(content)
            exp0 = extract_exp0_count(content)
            v2 = extract_v2_count(content)
            loinc_total = extract_loinc_count(content)
            interpolar = extract_interpolar_count(content)

            print(f"{dashboard['name']:<25} {loinc:<12} {exp0:<8} {v2:<8} {loinc_total:<12} {interpolar:<12}")

        except Exception as e:
            print(f"{dashboard['name']:<25} ERROR: {str(e)}")

    print()
    print("=" * 100)
    print("Legend:")
    print("  Exp0: Precoordinated Descendants (baseline)")
    print("  V2: Refined Query V2 (custom ECL with property/component filtering)")
    print("  LOINC Codes: Total unique LOINC codes found across all experiments")
    print("  Interpolar: Reference codes from Interpolar mapping (level 1+2)")
    print("=" * 100)

if __name__ == '__main__':
    main()
