
#!/usr/bin/env python3
"""
Create comparison charts for ECL experiments
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Load data
system_df = pd.read_csv('output/ecl_fixed_component_system/comparison_summary.csv')
property_df = pd.read_csv('output/ecl_fixed_component_property/comparison_summary.csv')

# Add experiment labels
system_df['Experiment'] = 'System (Direct Site)'
property_df['Experiment'] = 'Property'

# Combine
combined_df = pd.concat([system_df, property_df])

# Create output directory
output_dir = Path('output/comparison_charts')
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Chart 1: Overall Metrics Comparison (Bar Chart)
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

metrics_summary = combined_df.groupby('Experiment')[['Precision', 'Recall', 'F1 Score']].mean()

metrics_summary.plot(kind='bar', ax=ax, rot=0)
ax.set_title('Overall Performance: System vs Property', fontsize=16, fontweight='bold')
ax.set_ylabel('Score', fontsize=12)
ax.set_xlabel('Experiment', fontsize=12)
ax.set_ylim(0, 1)
ax.legend(title='Metric', fontsize=10)
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, fmt='%.3f', padding=3)

plt.tight_layout()
plt.savefig(output_dir / 'overall_metrics_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: overall_metrics_comparison.png")
plt.close()

# ============================================================================
# Chart 2: Per-Test F1 Score Comparison (Side-by-side)
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

# Pivot for side-by-side comparison
pivot_df = combined_df.pivot(index='Primary LOINC', columns='Experiment', values='F1 Score')
pivot_df = pivot_df.sort_values('System (Direct Site)', ascending=False)

pivot_df.plot(kind='barh', ax=ax, width=0.8)
ax.set_title('F1 Score per Test: System vs Property', fontsize=16, fontweight='bold')
ax.set_xlabel('F1 Score', fontsize=12)
ax.set_ylabel('Primary LOINC Code', fontsize=12)
ax.set_xlim(0, 1)
ax.legend(title='Experiment', fontsize=10)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'f1_per_test_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: f1_per_test_comparison.png")
plt.close()

# ============================================================================
# Chart 3: Precision vs Recall Scatter Plot
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

for exp_name in ['System (Direct Site)', 'Property']:
    exp_data = combined_df[combined_df['Experiment'] == exp_name]
    ax.scatter(exp_data['Recall'], exp_data['Precision'],
               label=exp_name, alpha=0.6, s=100)

ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Perfect (P=R)')
ax.set_xlabel('Recall', fontsize=12)
ax.set_ylabel('Precision', fontsize=12)
ax.set_title('Precision vs Recall: System vs Property', fontsize=16, fontweight='bold')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'precision_recall_scatter.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: precision_recall_scatter.png")
plt.close()

# ============================================================================
# Chart 4: Distribution of F1 Scores (Box Plot)
# ============================================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

sns.boxplot(data=combined_df, x='Experiment', y='F1 Score', ax=ax)
sns.swarmplot(data=combined_df, x='Experiment', y='F1 Score',
              ax=ax, color='black', alpha=0.5, size=4)

ax.set_title('Distribution of F1 Scores', fontsize=16, fontweight='bold')
ax.set_ylabel('F1 Score', fontsize=12)
ax.set_xlabel('Experiment', fontsize=12)
ax.set_ylim(-0.05, 1.05)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'f1_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: f1_distribution.png")
plt.close()

# ============================================================================
# Chart 5: Top 10 Improvements/Regressions
# ============================================================================
# Calculate differences
diff_df = system_df.set_index('Primary LOINC')[['F1 Score']].rename(columns={'F1 Score': 'System_F1'})
diff_df['Property_F1'] = property_df.set_index('Primary LOINC')['F1 Score']
diff_df['Difference'] = diff_df['System_F1'] - diff_df['Property_F1']
diff_df['Test_Name'] = system_df.set_index('Primary LOINC')['German Name']

# Top improvements and regressions
top_improvements = diff_df.nlargest(10, 'Difference')
top_regressions = diff_df.nsmallest(10, 'Difference')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Top improvements (System better)
top_improvements.plot(kind='barh', y='Difference', ax=ax1, color='green', alpha=0.7)
ax1.set_title('Top 10: System Outperforms Property (System F1 - Property F1)',
              fontsize=14, fontweight='bold')
ax1.set_xlabel('F1 Score Difference', fontsize=11)
ax1.set_ylabel('')
ax1.grid(axis='x', alpha=0.3)
ax1.legend().remove()

# Top regressions (Property better)
top_regressions.plot(kind='barh', y='Difference', ax=ax2, color='red', alpha=0.7)
ax2.set_title('Top 10: Property Outperforms System (System F1 - Property F1)',
              fontsize=14, fontweight='bold')
ax2.set_xlabel('F1 Score Difference', fontsize=11)
ax2.set_ylabel('')
ax2.grid(axis='x', alpha=0.3)
ax2.legend().remove()

plt.tight_layout()
plt.savefig(output_dir / 'top_differences.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: top_differences.png")
plt.close()

# ============================================================================
# Chart 6: Heatmap of Metrics
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 12))

# Prepare data for heatmaps
system_heatmap = system_df.set_index('Primary LOINC')[['Precision', 'Recall', 'F1 Score']].T
property_heatmap = property_df.set_index('Primary LOINC')[['Precision', 'Recall', 'F1 Score']].T

# System heatmap
sns.heatmap(system_heatmap, annot=True, fmt='.2f', cmap='RdYlGn',
            vmin=0, vmax=1, ax=ax1, cbar_kws={'label': 'Score'})
ax1.set_title('System (Direct Site) - All Metrics', fontsize=14, fontweight='bold')
ax1.set_xlabel('Primary LOINC Code', fontsize=11)
ax1.set_ylabel('Metric', fontsize=11)

# Property heatmap
sns.heatmap(property_heatmap, annot=True, fmt='.2f', cmap='RdYlGn',
            vmin=0, vmax=1, ax=ax2, cbar_kws={'label': 'Score'})
ax2.set_title('Property - All Metrics', fontsize=14, fontweight='bold')
ax2.set_xlabel('Primary LOINC Code', fontsize=11)
ax2.set_ylabel('Metric', fontsize=11)

plt.tight_layout()
plt.savefig(output_dir / 'metrics_heatmap.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: metrics_heatmap.png")
plt.close()

print(f"\n✓ All charts saved to: {output_dir}")
print("\nSummary Statistics:")
print("="*60)
print("\nSystem (Direct Site):")
print(f"  Avg Precision: {system_df['Precision'].mean():.3f}")
print(f"  Avg Recall:    {system_df['Recall'].mean():.3f}")
print(f"  Avg F1 Score:  {system_df['F1 Score'].mean():.3f}")
print("\nProperty:")
print(f"  Avg Precision: {property_df['Precision'].mean():.3f}")
print(f"  Avg Recall:    {property_df['Recall'].mean():.3f}")
print(f"  Avg F1 Score:  {property_df['F1 Score'].mean():.3f}")
