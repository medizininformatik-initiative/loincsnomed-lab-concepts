# Analysis Scripts

This directory contains all experiment, visualization, and comparison scripts for the MII Lab SNOMED-LOINC mapping project.

## Directory Structure

```
analysis/
├── experiments/          # Scripts that run experiments and generate value sets
│   ├── interpolar/      # Interpolar mapping experiments
│   └── ecl/             # ECL query-based experiments
├── visualization/        # Scripts for visualizing results
└── comparison/          # Scripts for comparing different approaches
```

## Experiments

### Interpolar Experiments
- **`create_valuesets_from_interpolar.py`**: Generate value sets from Interpolar mapping (quantitative only)
- **`create_valuesets_from_interpolar_filtered.py`**: Generate value sets with filtered comparability levels

### ECL Experiments
- **`ecl_descendants_baseline_run_all.py`**: Baseline ECL experiment using simple descendants
- **`ecl_fixed_component_run_all.py`**: ECL with fixed Component attribute
- **`ecl_component_descendants_run_all.py`**: ECL with Component descendants
- **`ecl_fixed_component_property_run_all.py`**: ECL with fixed Component + Property
- **`ecl_fixed_component_system_run_all.py`**: ECL with fixed Component + System

## Visualization

- **`ecl_descendants_baseline_visualize.py`**: Visualize baseline ECL results
- **`create_comparison_charts.py`**: Create comparison charts across experiments
- **`analyze_ecl_interpolar_discrepancies.py`**: Analyze discrepancies between ECL and Interpolar

## Comparison

- **`compare_with_filtered_interpolar.py`**: Compare experiments with filtered Interpolar results
- **`inspect_interpolar_columns.py`**: Inspect and analyze Interpolar data columns

## Output

All experiments write their output to the `../output/` directory.

## Running Experiments

All experiment scripts can be run from the project root:
```bash
python analysis/experiments/interpolar/create_valuesets_from_interpolar.py
python analysis/experiments/ecl/ecl_fixed_component_run_all.py
```

Or from the analysis directory:
```bash
cd analysis
python experiments/interpolar/create_valuesets_from_interpolar.py
```
