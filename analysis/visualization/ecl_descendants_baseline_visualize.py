#!/usr/bin/env python3
"""
ECL Descendants Baseline Experiment - Visualization
====================================================
Create charts to visualize precision, recall, and F1 metrics for baseline.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_CSV = PROJECT_ROOT / 'output' / 'ecl_descendants_baseline' / 'comparison_summary.csv'
OUTPUT_DIR = PROJECT_ROOT / 'output' / 'ecl_descendants_baseline'

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Load data
df = pd.read_csv(INPUT_CSV)

print(f"Loaded {len(df)} records")
print(f"\nSummary Statistics:")
print(f"  Average Precision: {df['Precision'].mean():.3f}")
print(f"  Average Recall:    {df['Recall'].mean():.3f}")
print(f"  Average F1 Score:  {df['F1 Score'].mean():.3f}")

# ==============================================================================
# Chart 1: Precision vs Recall Scatter Plot
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Scatter plot with F1 score as color
scatter = ax.scatter(df['Recall'], df['Precision'],
                     c=df['F1 Score'], cmap='viridis',
                     s=100, alpha=0.6, edgecolors='black')

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('F1 Score', rotation=270, labelpad=20)

# Add diagonal line (where Precision = Recall)
ax.plot([0, 1], [0, 1], 'r--', alpha=0.3, label='Precision = Recall')

# Labels and title
ax.set_xlabel('Recall', fontsize=12)
ax.set_ylabel('Precision', fontsize=12)
ax.set_title('ECL Descendants Baseline: Precision vs Recall\n(Color = F1 Score)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'chart_precision_recall_scatter.png', dpi=300, bbox_inches='tight')
print(f"\n[OK] Saved: chart_precision_recall_scatter.png")
plt.close()

# ==============================================================================
# Chart 2: F1 Scores Bar Chart (Top 20 and Bottom 20)
# ==============================================================================
df_sorted = df.sort_values('F1 Score', ascending=False)

# Top 20
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

top20 = df_sorted.head(20)
ax1.barh(range(len(top20)), top20['F1 Score'], color='green', alpha=0.7)
ax1.set_yticks(range(len(top20)))
ax1.set_yticklabels([f"{row['Primary LOINC']}" for _, row in top20.iterrows()], fontsize=8)
ax1.set_xlabel('F1 Score', fontsize=11)
ax1.set_title('Top 20 Primary Codes by F1 Score', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)
ax1.invert_yaxis()

# Bottom 20
bottom20 = df_sorted.tail(20)
ax2.barh(range(len(bottom20)), bottom20['F1 Score'], color='red', alpha=0.7)
ax2.set_yticks(range(len(bottom20)))
ax2.set_yticklabels([f"{row['Primary LOINC']}" for _, row in bottom20.iterrows()], fontsize=8)
ax2.set_xlabel('F1 Score', fontsize=11)
ax2.set_title('Bottom 20 Primary Codes by F1 Score', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'chart_f1_scores_ranked.png', dpi=300, bbox_inches='tight')
print(f"[OK] Saved: chart_f1_scores_ranked.png")
plt.close()

# ==============================================================================
# Chart 3: Distribution Histograms
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Precision distribution
axes[0, 0].hist(df['Precision'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].axvline(df['Precision'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Precision"].mean():.3f}')
axes[0, 0].set_xlabel('Precision', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Precision Distribution', fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Recall distribution
axes[0, 1].hist(df['Recall'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
axes[0, 1].axvline(df['Recall'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Recall"].mean():.3f}')
axes[0, 1].set_xlabel('Recall', fontsize=11)
axes[0, 1].set_ylabel('Frequency', fontsize=11)
axes[0, 1].set_title('Recall Distribution', fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# F1 Score distribution
axes[1, 0].hist(df['F1 Score'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].axvline(df['F1 Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["F1 Score"].mean():.3f}')
axes[1, 0].set_xlabel('F1 Score', fontsize=11)
axes[1, 0].set_ylabel('Frequency', fontsize=11)
axes[1, 0].set_title('F1 Score Distribution', fontsize=12, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Code counts comparison
axes[1, 1].scatter(df['Interpolar Count'], df['ECL Count'], alpha=0.6, s=80, edgecolors='black')
axes[1, 1].plot([0, df[['Interpolar Count', 'ECL Count']].max().max()],
                [0, df[['Interpolar Count', 'ECL Count']].max().max()],
                'r--', alpha=0.3, label='Equal counts')
axes[1, 1].set_xlabel('Interpolar Count', fontsize=11)
axes[1, 1].set_ylabel('ECL Count', fontsize=11)
axes[1, 1].set_title('Code Counts: Interpolar vs ECL', fontsize=12, fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'chart_distributions.png', dpi=300, bbox_inches='tight')
print(f"[OK] Saved: chart_distributions.png")
plt.close()

# ==============================================================================
# Chart 4: Precision-Recall-F1 Grouped Bar Chart (Sample)
# ==============================================================================
# Select 15 representative samples (mix of high/medium/low F1)
samples = pd.concat([
    df_sorted.head(5),   # Top 5
    df_sorted.iloc[20:25],  # Middle 5
    df_sorted.tail(5)    # Bottom 5
])

fig, ax = plt.subplots(figsize=(14, 8))

x = range(len(samples))
width = 0.25

bars1 = ax.bar([i - width for i in x], samples['Precision'], width, label='Precision', color='skyblue', edgecolor='black')
bars2 = ax.bar(x, samples['Recall'], width, label='Recall', color='lightcoral', edgecolor='black')
bars3 = ax.bar([i + width for i in x], samples['F1 Score'], width, label='F1 Score', color='lightgreen', edgecolor='black')

ax.set_xlabel('Primary LOINC Code', fontsize=11)
ax.set_ylabel('Score', fontsize=11)
ax.set_title('Precision, Recall, and F1 Score Comparison\n(Top 5, Middle 5, Bottom 5 by F1)', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([row['Primary LOINC'] for _, row in samples.iterrows()], rotation=45, ha='right', fontsize=9)
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'chart_metrics_comparison.png', dpi=300, bbox_inches='tight')
print(f"[OK] Saved: chart_metrics_comparison.png")
plt.close()

# ==============================================================================
# Summary
# ==============================================================================
print(f"\n{'='*80}")
print("VISUALIZATION COMPLETE!")
print(f"{'='*80}")
print(f"Charts saved to: {OUTPUT_DIR}")
print(f"  - chart_precision_recall_scatter.png")
print(f"  - chart_f1_scores_ranked.png")
print(f"  - chart_distributions.png")
print(f"  - chart_metrics_comparison.png")
