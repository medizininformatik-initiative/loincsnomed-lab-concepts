#!/usr/bin/env python3
"""
Create HTML Report for Hemoglobin Analysis
===========================================
Generates an HTML table showing all hemoglobin LOINC codes sorted by
how many approaches found them (most to least).
"""

import pandas as pd
import json
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_CSV = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin' / 'detailed_comparison.csv'
REFINED_CSV = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin' / 'refined_ecl_comparison.csv'
REFINED_JSON = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin' / 'refined_ecl_test_results.json'
TOP300_XLSX = PROJECT_ROOT / 'input' / 'Top300 Stand 2018-08-08.xlsx'
OUTPUT_HTML = PROJECT_ROOT / 'output' / 'singular_concepts' / 'blood_count_hemoglobin' / 'hemoglobin_comparison.html'

print("=" * 80)
print("CREATING HEMOGLOBIN HTML REPORT")
print("=" * 80)

# Load detailed comparison
print("\nLoading comparison data...")
df = pd.read_csv(INPUT_CSV)

# Load refined ECL results (SNOMED columns as string to preserve IDs)
df_refined = pd.read_csv(REFINED_CSV, dtype={
    'hemoglobin_excl_cord_SNOMED': str,
    'hemoglobin_incl_cord_SNOMED': str
})

# Load refined ECL JSON for SNOMED FSN labels
with open(REFINED_JSON, 'r', encoding='utf-8') as f:
    refined_json = json.load(f)

# Build LOINC -> SNOMED FSN mapping from excl_cord results
loinc_to_snomed_fsn = {}
excl_mapping = refined_json['hemoglobin_excl_cord']['snomed_to_loinc_mapping']
for loinc_code, snomed_list in excl_mapping.items():
    fsn_list = [item['snomed_fsn'] for item in snomed_list if item.get('snomed_fsn')]
    if fsn_list:
        loinc_to_snomed_fsn[loinc_code] = '<br>'.join(fsn_list)

# Merge the refined ECL columns (including SNOMED mappings)
df = df.merge(
    df_refined[['LOINC_Code', 'Excl_Cord_Blood', 'Incl_Cord_Blood',
                'hemoglobin_excl_cord_SNOMED', 'hemoglobin_incl_cord_SNOMED']],
    on='LOINC_Code',
    how='left'
)

# Add SNOMED FSN column
df['SNOMED_FSN'] = df['LOINC_Code'].map(loinc_to_snomed_fsn).fillna('')

# Load LOINC300 data
print("  Loading LOINC300 data...")
df_top300 = pd.read_excel(TOP300_XLSX)
loinc300_codes = set(df_top300['primär'].dropna().unique()) | set(df_top300['sekundär'].dropna().unique())
df['In_LOINC300'] = df['LOINC_Code'].isin(loinc300_codes)
print(f"  [OK] Loaded {len(loinc300_codes)} LOINC300 codes")

# Count how many approaches found each code
approach_columns = [
    'In_Interpolar',
    'ecl_descendants_baseline_Present',
    'ecl_fixed_component_Present',
    'ecl_component_descendants_Present',
    'ecl_fixed_component_property_Present',
    'ecl_fixed_component_system_Present',
    'Excl_Cord_Blood',
    'Incl_Cord_Blood'
]

def count_yes(row):
    """Count number of 'Yes' values in approach columns."""
    return sum(1 for col in approach_columns if row.get(col) == 'Yes')

df['Approach_Count'] = df.apply(count_yes, axis=1)

# Sort by approach count (descending), then by LOINC code
df = df.sort_values(['Approach_Count', 'LOINC_Code'], ascending=[False, True])

print(f"  [OK] Loaded {len(df)} LOINC codes")

# Generate HTML
print("\nGenerating HTML...")

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hemoglobin LOINC Comparison</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .summary {
            background-color: #ecf0f1;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }
        th {
            background-color: #34495e;
            color: white;
            padding: 12px 8px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        td {
            padding: 10px 8px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .yes {
            color: #27ae60;
            font-weight: bold;
        }
        .yes-recommended {
            color: #2980b9;
            font-weight: bold;
            font-size: 18px;
        }
        .code {
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            font-weight: bold;
        }
        .count {
            background-color: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            font-weight: bold;
        }
        .recommended-col {
            background-color: #e8f4f8;
        }
        .column-header {
            writing-mode: horizontal-tb;
            text-align: center;
        }
        .approach-col {
            text-align: center;
            width: 80px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hemoglobin LOINC Code Comparison</h1>

        <div class="summary">
            <h3>Summary Statistics</h3>
            <p><strong>Total LOINC codes:</strong> """ + str(len(df)) + """</p>
            <p><strong>Primary LOINC:</strong> 59260-0</p>
            <p><strong>Interpolar codes:</strong> """ + str(df['In_Interpolar'].value_counts().get('Yes', 0)) + """</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th class="column-header">Count</th>
                    <th class="column-header">LOINC Code</th>
                    <th class="column-header">LOINC Display</th>
                    <th class="column-header">LOINCSNOMED IDs</th>
                    <th class="approach-col">LOINC300</th>
                    <th class="approach-col">Interpolar</th>
                    <th class="approach-col">ECL Descendants</th>
                    <th class="approach-col">ECL Fixed Component</th>
                    <th class="approach-col">ECL Component Descendants</th>
                    <th class="approach-col">ECL Fixed Component Property</th>
                    <th class="approach-col">ECL Fixed Component System</th>
                    <th class="approach-col recommended-col">Refined (Excl Cord) ⭐</th>
                    <th class="approach-col">Refined (Incl Cord)</th>
                </tr>
            </thead>
            <tbody>
"""

# Add rows
for _, row in df.iterrows():
    count = row['Approach_Count']
    loinc_code = row['LOINC_Code']
    display = row['LOINC_Display']
    is_primary = row.get('Is_Primary', '')

    # Get SNOMED IDs and FSN labels
    snomed_ids = row.get('hemoglobin_excl_cord_SNOMED', '')
    if pd.notna(snomed_ids) and snomed_ids and snomed_ids != 'nan':
        snomed_id_display = snomed_ids.replace('; ', '<br>')
    else:
        snomed_id_display = ''

    snomed_fsn = row.get('SNOMED_FSN', '')

    # Combine IDs and labels
    snomed_combined = f"{snomed_id_display}"
    if snomed_fsn:
        snomed_combined = f"<div style='font-family: monospace;'>{snomed_id_display}</div><div style='font-size: 10px; color: #95a5a6;'>{snomed_fsn}</div>"

    html += f"""
                <tr>
                    <td><span class="count">{count}</span></td>
                    <td><span class="code">{loinc_code}</span></td>
                    <td>{display}</td>
                    <td style="font-size: 11px; color: #7f8c8d;">{snomed_combined}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('In_LOINC300') else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('In_Interpolar') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('ecl_descendants_baseline_Present') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('ecl_fixed_component_Present') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('ecl_component_descendants_Present') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('ecl_fixed_component_property_Present') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('ecl_fixed_component_system_Present') == 'Yes' else ""}</td>
                    <td class="approach-col recommended-col">{"<span class='yes-recommended'>✓</span>" if row.get('Excl_Cord_Blood') == 'Yes' else ""}</td>
                    <td class="approach-col">{"<span class='yes'>✓</span>" if row.get('Incl_Cord_Blood') == 'Yes' else ""}</td>
                </tr>
"""

html += """
            </tbody>
        </table>

        <div class="summary" style="margin-top: 30px;">
            <h3>Legend</h3>
            <p><strong>Count:</strong> Number of approaches that found this LOINC code</p>
            <p><strong>✓:</strong> Code found by this approach</p>
            <p><strong>LOINC300:</strong> Part of MII Top 300 LOINC codes</p>
            <p><strong>Interpolar:</strong> Manually curated Interpolar mapping</p>
            <p><strong>ECL Descendants:</strong> Simple descendant query (baseline)</p>
            <p><strong>ECL Fixed Component:</strong> Fixed component, descendant system/property</p>
            <p><strong>ECL Component Descendants:</strong> Component descendants</p>
            <p><strong>ECL Fixed Component Property:</strong> Fixed component and property</p>
            <p><strong>ECL Fixed Component System:</strong> Fixed component and system</p>
            <p><strong>Refined (Excl Cord) ⭐ (RECOMMENDED):</strong> Component + Property + Blood specimen, excluding cord blood</p>
            <p><strong>Refined (Incl Cord):</strong> Component + Property + Blood specimen, including cord blood</p>
        </div>
    </div>
</body>
</html>
"""

# Save HTML
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"  [OK] Saved HTML report: {OUTPUT_HTML}")

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nOpen in browser: {OUTPUT_HTML}")
