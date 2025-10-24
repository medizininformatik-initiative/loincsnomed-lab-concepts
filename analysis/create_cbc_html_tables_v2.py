#!/usr/bin/env python3
"""
Create CBC HTML Tables
======================
Generates nice HTML tables for all CBC components with styling and interactivity.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'singular_concepts'

print("=" * 80)
print("CBC HTML TABLES GENERATOR")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Define all CBC components - using output from cbc_component_analyzer.py
cbc_components = {
    'Hemoglobin': {
        'dir': 'hemoglobin',
        'csv': 'hemoglobin_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'Oxygen-carrying protein in red blood cells'
    },
    'Methemoglobin': {
        'dir': 'methemoglobin',
        'csv': 'methemoglobin_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'Oxidized form of hemoglobin'
    },
    'Erythrocytes': {
        'dir': 'erythrocytes',
        'csv': 'erythrocytes_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'Red blood cell count'
    },
    'Hematocrit': {
        'dir': 'hematocrit',
        'csv': 'hematocrit_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'Volume fraction of erythrocytes in blood'
    },
    'Leukocytes': {
        'dir': 'leukocytes',
        'csv': 'leukocytes_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'White blood cell count'
    },
    'Platelets': {
        'dir': 'platelets',
        'csv': 'platelets_ecl_comparison.csv',
        'category': 'Direct Observation',
        'description': 'Thrombocyte count'
    },
    'MCV': {
        'dir': 'mcv',
        'csv': 'mcv_ecl_comparison.csv',
        'category': 'Calculated Index',
        'description': 'Mean Corpuscular Volume - average RBC volume'
    },
    'MCH': {
        'dir': 'mch',
        'csv': 'mch_ecl_comparison.csv',
        'category': 'Calculated Index',
        'description': 'Mean Corpuscular Hemoglobin - average hemoglobin per RBC'
    },
    'MCHC': {
        'dir': 'mchc',
        'csv': 'mchc_ecl_comparison.csv',
        'category': 'Calculated Index',
        'description': 'Mean Corpuscular Hemoglobin Concentration'
    }
}

# Load all component data
print("Loading CBC component data...")
components_data = []
total_codes = 0
direct_obs_count = 0
calc_index_count = 0

for component_name, info in cbc_components.items():
    csv_path = OUTPUT_DIR / info['dir'] / info['csv']

    if not csv_path.exists():
        print(f"  [SKIP] {component_name}: File not found")
        continue

    df = pd.read_csv(csv_path)
    components_data.append({
        'name': component_name,
        'info': info,
        'data': df
    })

    total_codes += len(df)
    if info['category'] == 'Direct Observation':
        direct_obs_count += len(df)
    else:
        calc_index_count += len(df)

    print(f"  [OK] {component_name}: {len(df)} LOINC codes")

# Generate statistics HTML
stats_html = f"""
<div class="stat-box">
    <div class="stat-number">{len(components_data)}</div>
    <div class="stat-label">CBC Components</div>
</div>
<div class="stat-box">
    <div class="stat-number">{total_codes}</div>
    <div class="stat-label">Total LOINC Codes</div>
</div>
<div class="stat-box">
    <div class="stat-number">{direct_obs_count}</div>
    <div class="stat-label">Direct Observations</div>
</div>
<div class="stat-box">
    <div class="stat-number">{calc_index_count}</div>
    <div class="stat-label">Calculated Indices</div>
</div>
"""

# Generate summary table
print("\nGenerating summary table...")
summary_rows = []
for comp in components_data:
    df = comp['data']
    primary_code = ''
    if 'Is_Primary' in df.columns:
        primary_rows = df[df['Is_Primary'] == 'Yes']
        if len(primary_rows) > 0:
            primary_code = primary_rows.iloc[0]['LOINC_Code']

    summary_rows.append(f"""
        <tr>
            <td><strong>{comp['name']}</strong></td>
            <td>{comp['info']['description']}</td>
            <td>{comp['info']['category']}</td>
            <td style="text-align: center;">{len(df)}</td>
            <td><span class="loinc-code">{primary_code}</span></td>
        </tr>
    """)

summary_table_html = f"""
<table class="summary-table">
    <thead>
        <tr>
            <th>Component</th>
            <th>Description</th>
            <th>Category</th>
            <th style="text-align: center;">LOINC Count</th>
            <th>Primary Code</th>
        </tr>
    </thead>
    <tbody>
        {''.join(summary_rows)}
    </tbody>
</table>
"""

# Generate detailed component sections with comprehensive columns
print("Generating detailed component tables...")
components_html_parts = []

# Define ECL columns to display
ecl_columns = [
    ('ecl_descendants_baseline_Present', 'ECL Desc Baseline'),
    ('ecl_fixed_component_Present', 'ECL Fixed Comp'),
    ('ecl_component_descendants_Present', 'ECL Comp Desc'),
    ('ecl_fixed_component_property_Present', 'ECL Fixed C+P'),
    ('ecl_fixed_component_system_Present', 'ECL Fixed C+S'),
    ('refined_with_exclusions_Present', 'Refined (Excl)'),
    ('refined_base_Present', 'Refined (Base)'),
    ('precoord_descendants_Present', 'Pre-coord Desc')
]

for comp in components_data:
    df = comp['data']
    category_class = 'calculated' if comp['info']['category'] == 'Calculated Index' else ''

    # Generate table rows
    rows = []
    for _, row in df.iterrows():
        is_primary = row.get('Is_Primary', '') == 'Yes'
        row_class = 'primary-code' if is_primary else ''

        primary_badge = '<span class="badge badge-yes">PRIMARY</span>' if is_primary else ''

        # Build ECL result cells
        ecl_cells = []
        for col_name, _ in ecl_columns:
            if col_name in df.columns:
                value = row.get(col_name, '')
                cell_class = 'badge badge-yes' if value == 'Yes' else ''
                cell_content = '✓' if value == 'Yes' else ''
                ecl_cells.append(f'<td><span class="{cell_class}">{cell_content}</span></td>')

        in_interpolar = '<span class="badge badge-yes">✓</span>' if row.get('In_Interpolar', '') == 'Yes' else ''
        in_loinc300 = '<span class="badge badge-yes">✓</span>' if row.get('In_LOINC300', '') == 'Yes' else ''
        is_refined = '<span class="badge badge-refined">✓</span>' if row.get('Refined_Query', '') == 'Yes' else ''

        rows.append(f"""
            <tr class="{row_class}">
                <td><span class="loinc-code">{row['LOINC_Code']}</span> {primary_badge}</td>
                <td>{row.get('LOINC_Display', '')}</td>
                <td style="text-align: center;">{is_refined}</td>
                <td style="text-align: center;">{in_interpolar}</td>
                <td style="text-align: center;">{in_loinc300}</td>
                {''.join(ecl_cells)}
                <td style="text-align: center;">{row.get('Approach_Count', 0)}</td>
            </tr>
        """)

    # Build header for ECL columns that exist in this dataset
    ecl_headers = []
    for col_name, col_display in ecl_columns:
        if col_name in df.columns:
            ecl_headers.append(f'<th style="text-align: center;">{col_display}</th>')

    component_html = f"""
    <div class="component-section">
        <div class="component-header {category_class}">
            <div class="component-title">{comp['name']}</div>
            <div class="component-description">{comp['info']['description']} ({comp['info']['category']})</div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>LOINC Code</th>
                    <th>Display Name</th>
                    <th style="text-align: center;">Refined Query</th>
                    <th style="text-align: center;">Interpolar</th>
                    <th style="text-align: center;">LOINC300</th>
                    {''.join(ecl_headers)}
                    <th style="text-align: center;">Approaches</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    """

    components_html_parts.append(component_html)

# Combine all HTML - using direct string concatenation to avoid format issues
print("Creating final HTML...")

# Read CSS from external string
css_content = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f5f5f5;
    padding: 20px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 8px;
}

h1 {
    color: #2c3e50;
    margin-bottom: 10px;
    font-size: 2em;
}

.subtitle {
    color: #7f8c8d;
    margin-bottom: 30px;
    font-size: 1.1em;
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-box {
    background: #ecf0f1;
    padding: 20px;
    border-radius: 6px;
    text-align: center;
}

.stat-number {
    font-size: 2em;
    font-weight: bold;
    color: #3498db;
}

.stat-label {
    color: #7f8c8d;
    font-size: 0.9em;
    margin-top: 5px;
}

.component-section {
    margin-bottom: 40px;
}

.component-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 6px;
    margin-bottom: 15px;
}

.component-header.calculated {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.component-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 5px;
}

.component-description {
    font-size: 0.95em;
    opacity: 0.9;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    background: white;
}

thead {
    background: #34495e;
    color: white;
}

th {
    padding: 12px;
    text-align: left;
    font-weight: 600;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

td {
    padding: 10px 12px;
    border-bottom: 1px solid #ecf0f1;
}

tbody tr:hover {
    background: #f8f9fa;
}

.primary-code {
    background: #fff3cd;
    font-weight: bold;
}

.loinc-code {
    font-family: 'Courier New', monospace;
    color: #e74c3c;
    font-weight: bold;
}

.snomed-id {
    font-family: 'Courier New', monospace;
    color: #16a085;
    font-size: 0.85em;
}

.badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.8em;
    font-weight: bold;
}

.badge-yes {
    background: #d4edda;
    color: #155724;
}

.badge-refined {
    background: #e3f2fd;
    color: #1565c0;
    font-weight: bold;
}

.summary-table {
    margin-top: 30px;
}

.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid #ecf0f1;
    text-align: center;
    color: #7f8c8d;
    font-size: 0.9em;
}

@media print {
    body {
        background: white;
    }
    .container {
        box-shadow: none;
    }
}
"""

final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBC Components - LOINC-SNOMED Mapping Analysis</title>
    <style>
{css_content}
    </style>
</head>
<body>
    <div class="container">
        <h1>CBC Components - LOINC-SNOMED Mapping Analysis</h1>
        <div class="subtitle">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="stats">
            {stats_html}
        </div>

        <h2>Summary by Component</h2>
        {summary_table_html}

        <h2>Detailed Component Analysis</h2>
        {''.join(components_html_parts)}

        <div class="footer">
            <p>Generated by CBC HTML Tables Generator</p>
            <p>LOINC-SNOMED mapping analysis for Complete Blood Count components</p>
        </div>
    </div>
</body>
</html>
"""

# Save HTML file
output_file = OUTPUT_DIR / 'cbc_components_analysis.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
print(f"\nHTML file created: {output_file}")
print(f"\nSummary:")
print(f"  - {len(components_data)} CBC components")
print(f"  - {total_codes} total LOINC codes")
print(f"  - {direct_obs_count} direct observations")
print(f"  - {calc_index_count} calculated indices")
print(f"\nOpen the file in your browser to view the formatted tables.")
