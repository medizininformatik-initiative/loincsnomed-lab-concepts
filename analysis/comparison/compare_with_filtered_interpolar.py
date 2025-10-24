#!/usr/bin/env python3
"""
Compare ECL Results with Filtered Interpolar ValueSets
=======================================================
Takes an existing ECL experiment's results and compares against filtered Interpolar valuesets.
This allows us to see how precision improves when comparing against a narrower ground truth.

Usage:
  python compare_with_filtered_interpolar.py <experiment_dir>

Example:
  python compare_with_filtered_interpolar.py output/ecl_fixed_component
"""

import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def load_filtered_interpolar_codes():
    """Load filtered Interpolar valuesets and extract LOINC codes per primary."""
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    INTERPOLAR_FILTERED_DIR = PROJECT_ROOT / 'output' / 'valuesets_interpolar_filtered'

    primary_to_codes = {}

    for vs_file in INTERPOLAR_FILTERED_DIR.glob('valueset-interpolar-filtered-loinc-*.json'):
        with open(vs_file, 'r', encoding='utf-8') as f:
            valueset = json.load(f)

        # Extract primary LOINC from ID
        vs_id = valueset['id']
        primary_loinc = vs_id.replace('interpolar-filtered-loinc-', '')

        # Add hyphens back to LOINC code (e.g., "17426" -> "1742-6")
        if len(primary_loinc) >= 2:
            primary_loinc = primary_loinc[:-1] + '-' + primary_loinc[-1]

        # Extract LOINC codes
        codes = []
        for include in valueset.get('compose', {}).get('include', []):
            for concept in include.get('concept', []):
                codes.append(concept['code'])

        primary_to_codes[primary_loinc] = set(codes)

    return primary_to_codes

def compare_with_filtered(experiment_dir):
    """Compare ECL results with filtered Interpolar valuesets."""
    experiment_dir = Path(experiment_dir)
    experiment_name = experiment_dir.name

    print("="*80)
    print(f"COMPARING {experiment_name.upper()} WITH FILTERED INTERPOLAR")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load ECL results
    ecl_results_file = experiment_dir / 'ecl_query_results_summary.json'
    with open(ecl_results_file, 'r', encoding='utf-8') as f:
        ecl_results = json.load(f)

    print(f"[OK] Loaded ECL results: {len(ecl_results)} primary codes")

    # Load filtered Interpolar codes
    filtered_interpolar = load_filtered_interpolar_codes()
    print(f"[OK] Loaded filtered Interpolar: {len(filtered_interpolar)} primary codes")

    # Compare
    comparison_results = []

    for primary_loinc, ecl_data in ecl_results.items():
        if primary_loinc not in filtered_interpolar:
            print(f"  [SKIP] {primary_loinc}: Not in filtered Interpolar")
            continue

        interpolar_codes = filtered_interpolar[primary_loinc]
        ecl_codes = set(ecl_data.get('loinc_codes_found', []))

        overlap = interpolar_codes & ecl_codes
        interpolar_only = interpolar_codes - ecl_codes
        ecl_only = ecl_codes - interpolar_codes

        precision = len(overlap) / len(ecl_codes) if ecl_codes else 0
        recall = len(overlap) / len(interpolar_codes) if interpolar_codes else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        comparison_results.append({
            'primary_loinc': primary_loinc,
            'interpolar_filtered_count': len(interpolar_codes),
            'ecl_count': len(ecl_codes),
            'overlap_count': len(overlap),
            'interpolar_only_count': len(interpolar_only),
            'ecl_only_count': len(ecl_only),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1, 3),
            'interpolar_codes': sorted(list(interpolar_codes)),
            'ecl_codes': sorted(list(ecl_codes)),
            'overlap_codes': sorted(list(overlap)),
            'interpolar_only_codes': sorted(list(interpolar_only)),
            'ecl_only_codes': sorted(list(ecl_only))
        })

    # Save detailed comparison
    output_file = experiment_dir / 'comparison_interpolar_filtered_vs_ecl.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_results, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Saved: {output_file.name}")

    # Create summary CSV
    df_comparison = pd.DataFrame([
        {
            'Primary LOINC': r['primary_loinc'],
            'Interpolar Filtered Count': r['interpolar_filtered_count'],
            'ECL Count': r['ecl_count'],
            'Overlap': r['overlap_count'],
            'Precision': r['precision'],
            'Recall': r['recall'],
            'F1 Score': r['f1_score']
        }
        for r in comparison_results
    ])

    csv_file = experiment_dir / 'comparison_summary_filtered.csv'
    df_comparison.to_csv(csv_file, index=False)

    print(f"[OK] Saved: {csv_file.name}")

    # Print summary statistics
    avg_precision = df_comparison['Precision'].mean()
    avg_recall = df_comparison['Recall'].mean()
    avg_f1 = df_comparison['F1 Score'].mean()

    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS (vs Filtered Interpolar)")
    print(f"{'='*80}")
    print(f"Average Precision: {avg_precision:.3f}")
    print(f"Average Recall:    {avg_recall:.3f}")
    print(f"Average F1 Score:  {avg_f1:.3f}")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return avg_precision, avg_recall, avg_f1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compare_with_filtered_interpolar.py <experiment_dir>")
        print("Example: python compare_with_filtered_interpolar.py output/ecl_fixed_component")
        sys.exit(1)

    experiment_dir = sys.argv[1]
    compare_with_filtered(experiment_dir)
