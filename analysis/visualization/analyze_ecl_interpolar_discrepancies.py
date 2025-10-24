#!/usr/bin/env python3
"""
Deep Analysis of ECL vs Interpolar Discrepancies
=================================================
Creates detailed cross-tables and examples showing:
1. What codes ECL finds that Interpolar doesn't have
2. What codes Interpolar has that ECL misses
3. Patterns in the discrepancies

This helps understand if ECL is "too broad" or if Interpolar is just a subset.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuration
import sys
if len(sys.argv) < 2:
    print("Usage: python analyze_ecl_interpolar_discrepancies.py <experiment_dir>")
    print("Example: python analyze_ecl_interpolar_discrepancies.py output/ecl_fixed_component")
    sys.exit(1)

EXPERIMENT_DIR = Path(sys.argv[1])
OUTPUT_DIR = EXPERIMENT_DIR / 'discrepancy_analysis'
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print(f"ECL vs INTERPOLAR DISCREPANCY ANALYSIS: {EXPERIMENT_DIR.name}")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load comparison results (with filtered Interpolar)
with open(EXPERIMENT_DIR / 'comparison_interpolar_filtered_vs_ecl.json', 'r', encoding='utf-8') as f:
    comparison = json.load(f)

print(f"[OK] Loaded comparison for {len(comparison)} primary codes\n")

# ==============================================================================
# Analysis 1: Summary Cross-Table
# ==============================================================================
print("[Analysis 1] Creating summary cross-table...")

summary_data = []
for result in comparison:
    primary = result['primary_loinc']
    interpolar_count = result['interpolar_filtered_count']
    ecl_count = result['ecl_count']
    overlap = result['overlap_count']
    interpolar_only = result['interpolar_only_count']
    ecl_only = result['ecl_only_count']

    summary_data.append({
        'Primary LOINC': primary,
        'Interpolar': interpolar_count,
        'ECL': ecl_count,
        'Both': overlap,
        'Interpolar Only': interpolar_only,
        'ECL Only': ecl_only,
        'Precision': result['precision'],
        'Recall': result['recall'],
        'Coverage Ratio': round(ecl_count / interpolar_count, 2) if interpolar_count > 0 else 0
    })

df_summary = pd.DataFrame(summary_data)
df_summary = df_summary.sort_values('ECL Only', ascending=False)

df_summary.to_csv(OUTPUT_DIR / 'summary_cross_table.csv', index=False)
print(f"  [OK] Saved: summary_cross_table.csv")

# Print top 10 by ECL-only codes
print("\n  Top 10 primary codes by 'ECL Only' count:")
print(df_summary[['Primary LOINC', 'Interpolar', 'ECL', 'Both', 'ECL Only', 'Precision']].head(10).to_string(index=False))

# ==============================================================================
# Analysis 2: Detailed Examples of ECL-Only Codes
# ==============================================================================
print("\n[Analysis 2] Analyzing ECL-only codes in detail...")

# Pick a few representative examples
example_codes = df_summary.head(5)['Primary LOINC'].tolist()

examples_output = []

for primary in example_codes:
    result = next(r for r in comparison if r['primary_loinc'] == primary)

    ecl_only_codes = result['ecl_only_codes'][:20]  # Limit to first 20

    examples_output.append({
        'primary_loinc': primary,
        'interpolar_count': result['interpolar_filtered_count'],
        'ecl_count': result['ecl_count'],
        'ecl_only_count': result['ecl_only_count'],
        'sample_ecl_only_codes': ecl_only_codes,
        'precision': result['precision'],
        'recall': result['recall']
    })

with open(OUTPUT_DIR / 'ecl_only_examples.json', 'w', encoding='utf-8') as f:
    json.dump(examples_output, f, indent=2, ensure_ascii=False)

print(f"  [OK] Saved: ecl_only_examples.json")
print(f"  Showing first ECL-only codes for top 5 primary codes")

# ==============================================================================
# Analysis 3: Interpolar-Only Codes (Missed by ECL)
# ==============================================================================
print("\n[Analysis 3] Analyzing Interpolar-only codes (missed by ECL)...")

missed_summary = []
for result in comparison:
    interpolar_only = result['interpolar_only_codes']
    if len(interpolar_only) > 0:
        missed_summary.append({
            'primary_loinc': result['primary_loinc'],
            'interpolar_count': result['interpolar_filtered_count'],
            'missed_count': result['interpolar_only_count'],
            'missed_codes': interpolar_only,
            'recall': result['recall']
        })

missed_summary = sorted(missed_summary, key=lambda x: x['missed_count'], reverse=True)

with open(OUTPUT_DIR / 'interpolar_only_examples.json', 'w', encoding='utf-8') as f:
    json.dump(missed_summary, f, indent=2, ensure_ascii=False)

print(f"  [OK] Saved: interpolar_only_examples.json")

if len(missed_summary) > 0:
    print(f"\n  Primary codes with missed Interpolar codes:")
    for item in missed_summary[:10]:
        print(f"    {item['primary_loinc']}: Missed {item['missed_count']}/{item['interpolar_count']} codes (Recall={item['recall']:.2f})")

# ==============================================================================
# Analysis 4: Pattern Detection
# ==============================================================================
print("\n[Analysis 4] Detecting patterns...")

# Pattern 1: How many primary codes have perfect recall?
perfect_recall = df_summary[df_summary['Recall'] == 1.0]
print(f"  Primary codes with 100% recall: {len(perfect_recall)}/{len(df_summary)} ({len(perfect_recall)/len(df_summary)*100:.1f}%)")

# Pattern 2: Distribution of ECL/Interpolar ratio
print(f"\n  ECL/Interpolar Coverage Ratio distribution:")
print(f"    Min:    {df_summary['Coverage Ratio'].min():.2f}x")
print(f"    Max:    {df_summary['Coverage Ratio'].max():.2f}x")
print(f"    Median: {df_summary['Coverage Ratio'].median():.2f}x")
print(f"    Mean:   {df_summary['Coverage Ratio'].mean():.2f}x")

# Pattern 3: Correlation between ECL count and precision
corr = df_summary['ECL'].corr(df_summary['Precision'])
print(f"\n  Correlation between ECL count and Precision: {corr:.3f}")
if corr < -0.3:
    print(f"    -> Negative correlation: More ECL codes -> Lower precision")
    print(f"    -> Suggests ECL is retrieving many codes not in Interpolar")

# ==============================================================================
# Analysis 5: Categorize Primary Codes by Behavior
# ==============================================================================
print("\n[Analysis 5] Categorizing primary codes by ECL behavior...")

categories = {
    'High Precision, High Recall (>0.7, >0.9)': [],
    'Low Precision, High Recall (<0.3, >0.9)': [],
    'High Precision, Low Recall (>0.7, <0.9)': [],
    'Low Precision, Low Recall (<0.3, <0.9)': []
}

for _, row in df_summary.iterrows():
    p, r = row['Precision'], row['Recall']
    primary = row['Primary LOINC']

    if p > 0.7 and r > 0.9:
        categories['High Precision, High Recall (>0.7, >0.9)'].append(primary)
    elif p < 0.3 and r > 0.9:
        categories['Low Precision, High Recall (<0.3, >0.9)'].append(primary)
    elif p > 0.7 and r < 0.9:
        categories['High Precision, Low Recall (>0.7, <0.9)'].append(primary)
    elif p < 0.3 and r < 0.9:
        categories['Low Precision, Low Recall (<0.3, <0.9)'].append(primary)

for category, codes in categories.items():
    print(f"\n  {category}: {len(codes)} codes")
    if len(codes) > 0 and len(codes) <= 10:
        print(f"    {', '.join(codes)}")

# Save categorization
with open(OUTPUT_DIR / 'categorization.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

# ==============================================================================
# Complete
# ==============================================================================
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"Output directory: {OUTPUT_DIR}")
print(f"Files created:")
print(f"  - summary_cross_table.csv")
print(f"  - ecl_only_examples.json")
print(f"  - interpolar_only_examples.json")
print(f"  - categorization.json")
print(f"\nNext steps:")
print(f"  1. Review ecl_only_examples.json to understand what ECL retrieves")
print(f"  2. Check if ECL-only codes are clinically valid but unused")
print(f"  3. Review interpolar_only_examples.json to understand recall issues")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
